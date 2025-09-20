import os
from ebooklib import epub  # pip install ebooklib
import ebooklib
from bs4 import BeautifulSoup  # pip install beautifulsoup4


def make_epub(root_folder, output_file):
    prefix_length = 5  # 文件名前缀长度，例如ch001为5，chapter01为9
    htm_ext_names = ('.htm', '.html')  # 文件扩展名

    # 创建一个Epub书籍对象
    book = epub.EpubBook()

    # 添加书名、作者等信息
    book.set_identifier(output_file.split('.')[0])  # 使用输出文件名作为标识符
    book.set_title('潼溪注脂砚斋重评石头记')
    book.set_language('zh-CN')
    # 设置作者
    book.add_author("曹雪芹 脂砚斋 吴铭恩 潼溪")


    img_path = os.path.join(root_folder, 'images')
    # js_path = os.path.join(root_folder, 'scripts')
    css_path = os.path.join(root_folder, 'styles')
    fonts_path = os.path.join(root_folder, 'fonts')

    # 用于存储CSS和JS文件的路径
    css_files = []
    # js_files = []

    # 准备css文件
    for root, dirs, files in os.walk(css_path):
        for file in files:
            if file.endswith('.css'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    css = epub.EpubItem(uid=file, file_name=f'styles/{file}',
                                        content=content, media_type='text/css')
                    css_files.append(css)

    # 准备js文件，由于大多数EPUB阅读器不支持JS或者JS兼容性差，取消JS文件的添加
    # for root, dirs, files in os.walk(js_path):
    #     for file in files:
    #         if file.endswith('.js'):
    #             file_path = os.path.join(root, file)
    #             with open(file_path, 'r', encoding='utf-8') as f:
    #                 content = f.read()
    #                 js = epub.EpubItem(uid=file, file_name=f'scripts/{file}', content=content,
    #                                    media_type='application/javascript')
    #                 js_files.append(js)


    # 添加图片资源
    for root, dirs, files in os.walk(img_path):
        for file in files:
            file_path = os.path.join(img_path, file)
            with open(file_path, 'rb') as f:
                img_item = epub.EpubItem(
                    uid=file,
                    file_name=f'images/{file}',
                    media_type='image/jpeg',
                    content=f.read()
                )
                book.add_item(img_item)

    # 添加字体资源
    for root, dirs, files in os.walk(fonts_path):
        for file in files:
            file_path = os.path.join(fonts_path, file)
            with open(file_path, 'rb') as f:
                font_item = epub.EpubItem(
                    uid=file,
                    file_name=f'fonts/{file}',
                    media_type='font/ttf',
                    content=f.read()
                )
                book.add_item(font_item)

    chapter_files = []  # 用于存储HTML文件名的列表，用于建立导航信息
    navi_items = {}  # 导航字典，键为文件名，值为该文件中需添加进目录的标题id和标题文本的字典
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(htm_ext_names):  # 根据需要调整文件扩展名和前缀
                ext_length = 4 if file.endswith('.htm') else 5  # 文件扩展名长度，例如.htm为4，.html为5
                file_path = os.path.join(root, file)
                chapter = epub.EpubHtml(title=file[prefix_length:-ext_length], file_name=file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                    soup = BeautifulSoup(html, 'html.parser')

                    # --- 如果担个html文件中有需要添加进目录的标题 ---
                    # 查找所有需添加进目录的标题级别标签
                    head_tags = soup.find_all('h3')
                    id_list = {}  # 保存标题id和标题文本的字典
                    for head in head_tags:
                        # 在每个标题标签内查找 a 标签，此标签为该标题的书签。无书签的标题则不添加进目录
                        a_tag = head.find('a')
                        if a_tag and a_tag.get('id'):
                            head_title = a_tag.get_text(strip=True)
                            id_list[a_tag['id']] = head_title
                    # 将文件名（不含路径）作为键，id 字典作为值存入导航字典
                    navi_items[file] = id_list

                    # 删除js脚本结点
                    scripts = soup.find_all('script', src="scripts/double_line.js")
                    if scripts:
                        for script in scripts:
                            script.decompose()

                    # 删除 <div id="note"></div>，利用epub3规范特性显示注释框
                    div = soup.find('div', id='note')
                    if div:
                        div.decompose()

                    chapter.content = str(soup)

                # 添加CSS和JS文件链接到HTML页面中
                for css in css_files:
                    chapter.add_item(css)
                # for js in js_files:
                #     chapter.add_item(js)

                # 在书籍中添加处理好的HTML页面
                book.add_item(chapter)
                chapter_files.append(chapter)

    # 构建 TOC 结构
    toc = []

    for chapter in chapter_files:
        # 构建 nav.xhtml 中的链接
        nav_link = epub.Link(chapter.file_name, chapter.title, chapter.file_name)

        # 添加子章节到 TOC（如果有的话）
        section_ids = navi_items.get(chapter.file_name, {})
        if section_ids:
            subsections = [
                epub.Link(f"{chapter.file_name}#{sec_id}", display_text, sec_id)
                for sec_id, display_text in section_ids.items()
            ]
            # 创建一个章节项，包含其子章节
            toc_item = (nav_link, subsections)
        else:
            # 没有子章节，直接添加链接
            toc_item = nav_link
        
        toc.append(toc_item)

    # 设置最终的 TOC
    book.toc = tuple(toc)
    print(f"✅ 目录项已设置，共 {len(toc)} 项")

    # 添加CSS文件到书籍中
    for css in css_files:
        book.add_item(css)

    # 添加JS文件到书籍中
    # for js in js_files:
    #     book.add_item(js)

    # 设置封面图片（会自动创建 cover.xhtml）
    cover_image_path = os.path.join(img_path, 'cover.jpg')
    if os.path.exists(cover_image_path):
        with open(cover_image_path, 'rb') as f:
            book.set_cover('cover.jpg', f.read())
            print("✅ 封面已设置")
    else:
        print("⚠️ 封面图片未找到")

    # 设置书籍的spine（阅读顺序），将封面与目录也添加进来。对于epub3.0规范来说不设置的话制作出的书籍无法阅读。列表中可以用书籍章节的uid，例如下面的封面。
    book.spine = ['cover', 'nav'] + chapter_files

    # 生成目录和导航文件，并添加到书籍中。官方文档在设置book.spine后执行这个步骤
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())  # 仅对epub2.0规范的阅读器有用，epub3.0规范的阅读器会忽略

    # 检查内容是否成功读取
    # for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    #     if hasattr(item, 'title'):
    #         print(f"Title: {item.title}, File: {item.file_name}, Length: {len(item.content) if item.content else 0}")

    # 保存书籍为EPUB文件
    epub.write_epub(output_file, book, {'version': 3})


if __name__ == '__main__':
    # 输入文件夹和输出文件名
    root_folder = r'D:\工作\2025\潼溪注脂评红楼梦HTML'
    output_file = os.path.join(root_folder, 'output', '潼溪注脂砚斋重评石头记.epub')
    print(output_file)


    # 调用函数生成EPUB文件
    make_epub(root_folder, output_file)