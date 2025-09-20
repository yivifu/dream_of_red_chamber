import os


def check_htm_files(directory_path):
    """
    遍历目录中所有 .htm 文件，检查文件中的注释交叉连接是否包含了章节前缀（#+文件名前五个字符）。
    如果文件中包含了该前缀，则认为注释交叉连接正确；否则，打印出文件名。

    Args:
        directory_path (str): 要扫描的目录路径
    """
    files_missing_name_in_content = []

    # 检查目录是否存在
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在。")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.htm'):
            file_path = os.path.join(directory_path, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 注释交叉连接前缀
                prefix = f'#{filename[:5]}'  # 直接取文件名前五个字符

                # 检查内容是否包含前缀，<hr/>标签是有注释的标志
                if (prefix not in content) and ('<hr/>' in content):
                    files_missing_name_in_content.append(filename)
                    print(f"'{filename}' 的内容中不包含其文件名前缀 '{prefix}'。")


            except Exception as e:
                print(f"读取或处理文件 '{filename}' 时出错: {e}")

    if len(files_missing_name_in_content) == 0:
        print("所有文件的注释交叉连接均包含了章节前缀。")



# *************************************************************************
DIRECTORY_TO_SCAN = r"D:\工作\2025\潼溪注脂评红楼梦HTML"  # 要扫描的路径

if __name__ == "__main__":
    check_htm_files(DIRECTORY_TO_SCAN)