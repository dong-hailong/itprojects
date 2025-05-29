import os, re
import json
import shutil
import copy


def extract_leading_number(filename):
    """提取文件名开头的数字"""
    match = re.match(r'^(\d+)', filename)
    return int(match.group(1)) if match else float('inf')


def list_files_sorted(folder_name, md5_id, data, vip_index):
    """列出目录下的所有文件，按前两位数排序"""
    directory = './%s' %folder_name
    print(f"\n目录 '{directory}' 中的文件（按前两位数排序）：")

    # 获取所有文件并提取前两位数
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            num = extract_leading_number(filename)
            files.append((num, filename))

    # 按前两位数排序
    files.sort(key=lambda x: x[0])

    data_list = []
    
    # 输出排序结果
    for idx, (num, filename) in enumerate(files):
        copy_data = copy.deepcopy(data)
        if int(filename.count('.')) == 2:
            # print (filename)
            filepath = './%s/%s' %(directory, filename)
            first_line = print_first_lines(filepath, md5_id).strip('#').strip()

            copy_data['course_name'] = '%s.%s' %(str(num), first_line)

            link = "https://doc.itprojects.cn/api/v1.1/course/%s/%s" %(folder_name, filename)

            copy_data['tutorial'] = link
            # print (copy_data)

            if num >= vip_index:
                copy_data['is_vip'] = True
                original_file_path = os.path.join(directory, filename)

                # 为vip课件创建副本并重命名
                encrypt_and_backup_file(original_file_path, md5_id)
            else:
                copy_data['is_vip'] = False

            data_list.append(copy_data)


    return data_list


def print_first_lines(filepath, md5_id):
    """
    输出文件夹下每个文件的第一行内容
    :param directory: 文件夹路径
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        # 读取第一行
        first_line = file.readline().strip()
        # print (first_line)
        if first_line.strip() == 'encrypt':
            newfilepath = filepath.replace('.md','.%s.md') %md5_id
            first_line = print_first_lines2(newfilepath)

    return first_line


def print_first_lines2(filepath):
    """
    输出文件夹下每个文件的第一行内容
    :param directory: 文件夹路径
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        # 读取第一行
        first_line = file.readline().strip()

    return first_line


def encrypt_and_backup_file(original_file_path, md5_id):
    """
    对指定文件进行加密备份处理：
    1. 创建备份副本（添加'_backup'后缀）
    2. 重命名副本（添加'secure_copy_'前缀）
    3. 将原文件内容替换为'encrypt'

    参数:
        original_file_path (str): 原始文件的完整路径
    返回:
        tuple: (success: bool, message: str, backup_path: str)
    """
    # 参数校验
    if not os.path.isfile(original_file_path):
        print ("错误：文件不存在 '{original_file_path}'")


    # 1. 创建备份副本路径
    dirname, filename = os.path.split(original_file_path)
    base, ext = os.path.splitext(filename)

    file_list = os.listdir(dirname)

    backup_filename = f"{base}.{md5_id}{ext}" # 副本文件名
    backup_path = os.path.join(dirname, backup_filename)


    if backup_filename in file_list:
        print ('#### 备份已存在', backup_path, backup_filename)
    else:
        # 2. 创建文件副本
        shutil.copy2(original_file_path, backup_path)

        # 3. 加密原文件（替换内容）
        with open(original_file_path, 'w', encoding='utf-8') as f:
            f.write("encrypt")

        print (filename, backup_filename)


def save_json_data(json_datas):
    # 保存到JSON文件
    json_file_name = 'coursedetail.C0002.wuziqi'
    output_filename = f"{folder_name}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_datas, f, ensure_ascii=False, indent=4)
    print(f"JSON数据已保存到文件: {output_filename}")



project_name = '五子棋-人机对战版' #项目名称
folder_name = 'coursedetail.C0002.wuziqi' #项目文件夹名
md5_id = 'bad985e3e5075b8e98592d4fd7bef049' #md5加密字符串
vip_index = 5 #从该节课开始之后的课都是VIP课程（包含本节课）


json_datas = {
    "title": project_name,
    "product_list": [],
    "catalogue_list": []
}


data =  {
        "course_name": "%s",
        "is_vip": False,
        "tutorial": "%s",
        "video": "",
        "question_answer": "",
        "product_detail": "",
        "children": []
    }



def main():

    catalogue_list = list_files_sorted(folder_name, md5_id, data, vip_index)
    json_datas['catalogue_list'] = catalogue_list


    # datas = json.dumps(json_datas, ensure_ascii=False, indent=4)
    # print (datas)
    save_json_data(json_datas)
    


if __name__ == "__main__":
    main()



