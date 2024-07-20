import os

def export_code(project_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for root, dirs, files in os.walk(project_path):
            for name in files:
                file_path = os.path.join(root, name)
                relative_path = os.path.relpath(file_path, project_path)
                print(name)
                if relative_path.endswith(('.java', '.jsp', '.xml', '.properties', '.yml', '.yaml')):
                    file.write(f"{relative_path}:\n")
                    with open(file_path, 'r', encoding='utf-8') as code_file:
                        code = code_file.read()
                        file.write(code)
                        file.write("\n\n")

# 指定Springboot项目的根目录路径
project_path = "C:/Projects/jspmkk4bv"

# 指定导出文件的路径
output_file = "C:/Projects/export.txt"

export_code(project_path, output_file)