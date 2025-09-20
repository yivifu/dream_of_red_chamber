import os
from fontTools.subset import main  # pip install fonttools

def extract_unique_chars_from_htm_files(directory_path, output_file):
    """
    读取指定目录中所有 .htm 文件，提取所有字符并去重，保存到输出文件。

    Args:
        directory_path (str): 要扫描的目录路径
        output_file (str): 输出的去重字符文件路径
    """
    unique_chars = set()

    # 检查目录是否存在
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在。")
        return

    # 遍历目录中的所有文件，并对其中的HTML文件中的字符进行处理
    found_files = False
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.htm', '.html')):  # 遍历 .htm 和 .html 文件
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 将文件内容的每个字符添加到集合中（自动去重）
                    unique_chars.update(content)
                if not found_files:
                    found_files = True
                print(f"已处理文件: {filename}")
            except Exception as e:
                print(f"读取文件 '{filename}' 时出错: {e}")

    if not found_files:
        print(f"在目录 '{directory_path}' 中未找到任何HTML文件。")
        return

    # 将去重后的字符排序后写入输出文件
    try:
        sorted_chars = sorted(unique_chars)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(''.join(sorted_chars))
        print(f"去重后的字符已保存到 '{output_file}'，共 {len(sorted_chars)} 个唯一字符。")
    except Exception as e:
        print(f"写入输出文件 '{output_file}' 时出错: {e}")


def subset_font_from_chars(characters_file, font_file, output_font_file):
    """
    根据字符文件对字体文件进行子集化。

    Args:
        characters_file (str): 包含唯一字符的文本文件路径
        font_file (str): 要子集化的原始字体文件 (如 .ttf) 路径
        output_font_file (str): 输出的子集化字体文件路径
    """
    with open(characters_file, 'r', encoding='utf-8') as f:
        characters = f.read()

    # 构造参数
    args = [
        font_file,
        f"--text={characters}",
        f"--output-file={output_font_file}",
        "--hinting",
        "--flavor=woff2"  # 可选：生成 WOFF2 格式的字体，需要先pip install brotli才能支持
    ]

    # 执行子集化
    main(args)

# 请修改以下两个变量以适应您的实际情况
DIRECTORY_TO_SCAN = r"D:\工作\2025\潼溪注脂评红楼梦HTML"  # 替换为您的目录路径
CHARACTERS_FILE = r"D:\工作\2025\潼溪注脂评红楼梦HTML\output\unique_chars.txt"  # 替换为您的输出文件路径

FONT_FILE = r"D:\工作\2025\LXGWRedDream.ttf"                # 替换为您的原始字体文件路径
OUTPUT_FONT_FILE = r"D:\工作\2025\潼溪注脂评红楼梦HTML\fonts\LXGWRedDream_subset.ttf"  # 替换为期望的输出字体路径

if __name__ == "__main__":
    extract_unique_chars_from_htm_files(DIRECTORY_TO_SCAN, CHARACTERS_FILE)
    subset_font_from_chars(CHARACTERS_FILE, FONT_FILE, OUTPUT_FONT_FILE)
    print("程序执行完毕。")