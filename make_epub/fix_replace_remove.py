from bs4 import BeautifulSoup, NavigableString, Tag
import re
import os

def process_div_in_file(file_path):
    """处理单个文件中的 div.story"""
    print(f"处理文件: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"  读取文件失败: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    divs = soup.find_all('div', class_='story')

    modified = False

    for div in divs:
        _process_children(div, soup)
        modified = True

    if modified:
        # 备份原文件
        backup_path = file_path + ".bak"
        if not os.path.exists(backup_path):
            os.rename(file_path, backup_path)
        else:
            print(f"  警告: 备份文件已存在: {backup_path}，跳过备份")
        # 保存修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"  ✅ 已修改并保存: {file_path}")
    else:
        print(f"  ❌ 无修改: {file_path}")


def _process_children(parent, soup):
    """
    递归处理子节点
    如果 parent 是受保护的 span（class=remove/replace），则不处理其内容
    """
    if parent.name == 'sup':
        return
    # 检查当前 parent 是否是受保护的 span
    if parent.name == 'span':
        class_list = parent.get('class', [])
        if isinstance(class_list, list):
            if 'remove' in class_list or 'replace' in class_list:
                return  # 跳过处理，保留原内容

    # 安全地获取内容副本
    contents = list(parent.contents)
    for child in contents:
        if isinstance(child, NavigableString):
            text = child.string
            # 分割文本，保留括号结构
            parts = re.split(r'(\([一-龟]+?\)|\[[一-龟]+?\])', text)
            new_contents = []
            for part in parts:
                if part.startswith('(') and part.endswith(')'):
                    # inner = part[1:-1]
                    # 创建新 span
                    span = soup.new_tag("span")
                    span['class'] = ['remove']
                    span.string = part
                    new_contents.append(span)
                elif part.startswith('[') and part.endswith(']'):
                    # inner = part[1:-1]
                    span = soup.new_tag("span")
                    span['class'] = ['replace']
                    span.string = part
                    new_contents.append(span)
                else:
                    if part:  # 非空文本
                        new_contents.append(NavigableString(part))

            # 替换原始文本节点
            for new_node in reversed(new_contents):
                child.insert_after(new_node)
            child.extract()

        elif isinstance(child, Tag):
            # 递归处理子标签（除非是受保护的 span）
            _process_children(child, soup)


def main(directory):
    """主函数：遍历目录处理所有 .htm 文件"""
    if not os.path.exists(directory):
        print(f"错误: 目录不存在: {directory}")
        return

    htm_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.htm') and file.lower().startswith('ch'):
                htm_files.append(os.path.join(root, file))

    if not htm_files:
        print(f"在 {directory} 中未找到 .htm 文件")
        return

    print(f"找到 {len(htm_files)} 个 .htm 文件，开始处理...\n")

    for file_path in htm_files:
        try:
            process_div_in_file(file_path)
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

    print("\n✅ 所有文件处理完成。")


# ======================
# 使用示例
# ======================
if __name__ == '__main__':
    # 设置要处理的目录路径
    target_directory = r"D:\工作\2025\潼溪注脂评红楼梦HTML\test"  # <-- 修改为你的实际路径

    main(target_directory)