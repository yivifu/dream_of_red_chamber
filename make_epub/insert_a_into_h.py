import os
import shutil

from bs4 import BeautifulSoup, NavigableString


def insert_a_into_h(root_folder):
    # 遍历指定目录及其子目录中的所有文件
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.htm', '.html')):  # 根据需要调整文件扩展名和前缀
                file_path = os.path.join(root, file)
                # 备份原文件
                backup_path = file_path + ".bak"
                if not os.path.exists(backup_path):
                    shutil.copy2(file_path, backup_path)
                else:
                    print(f"  警告: 备份文件已存在: {backup_path}，跳过备份")

                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    # 初始化自增长编号
                    section_counter = 1

                    # 找到所有的 h3 标签
                    h3_tags = soup.find_all('h3')

                    for h3 in h3_tags:
                        # --- 提取并移除直属文本 ---
                        direct_text_parts = []

                        # 遍历 h3 的所有直接子节点
                        for child in list(h3.children):  # 使用 list() 避免在遍历时修改列表
                            if isinstance(child, NavigableString):
                                # 如果是文本节点，将其内容添加到列表，并从父节点移除
                                text_content = str(child).strip()
                                if text_content:  # 只保留非空文本
                                    direct_text_parts.append(text_content)
                                child.extract()  # 移除该文本节点

                        # 将所有直属文本拼接成一个字符串
                        combined_text = ''.join(direct_text_parts)
                        # ----------------------------

                        # 只有当有直属文本时才创建新的 <a> 标签
                        if combined_text:
                            # 创建新的 <a> 标签
                            new_a_tag = soup.new_tag("a")
                            new_a_tag['id'] = f"section{section_counter}"
                            new_a_tag.string = combined_text  # 设置 a 标签的文本

                            # 将新的 <a> 标签插入到 h3 的最前面
                            h3.insert(0, new_a_tag)

                            # 编号递增
                            section_counter += 1

                    # 最后，将修改后的 HTML 转换回字符串
                    modified_html = str(soup)

                # 将修改后的 HTML 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_html)
                print(f"已处理文件: {file}")

if __name__ == '__main__':
    # 输入文件夹和输出文件名
    root_folder = r'D:\工作\2025\幻灭三部曲'
    insert_a_into_h(root_folder)