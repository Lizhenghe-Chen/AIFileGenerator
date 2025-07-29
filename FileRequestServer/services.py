import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PPTGenProject.PPT_Gen_functions import generate_ppt_from_user_input


def mock_generate_file_from_user_input(
    user_input, userId, expected_slides, custom_filename, design_number
):
    """在Output文件夹创建txt文件并返回绝对路径"""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "Output")
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{custom_filename}.txt" if custom_filename else f"mock_{userId}.txt"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"User ID: {userId}\n")
        f.write(f"Content: {user_input}\n")
        f.write(f"Expected Slides: {expected_slides}\n")
        f.write(f"Design Number: {design_number}\n")

    return os.path.abspath(file_path)


def generate_ppt_file(request):
    """生成PPT文件并移动到用户目录"""
    fullPath = generate_ppt_from_user_input(
        user_input=request.content,
        expected_slides=request.expected_slides,
        custom_filename=request.filename,
        design_number=request.design_number,
    )
    # fullPath = mock_generate_file_from_user_input(
    #     user_input=request.content,
    #     userId=request.userId,
    #     expected_slides=request.expected_slides,
    #     custom_filename=request.filename,
    #     design_number=request.design_number,
    # )
    # 在Output文件夹下根据userId创建子文件夹
    output_base_dir = os.path.join(os.path.dirname(__file__), "..", "Output")
    user_output_dir = os.path.join(output_base_dir, request.userId)
    os.makedirs(user_output_dir, exist_ok=True)

    # 获取原文件名并构建新的目标路径
    original_filename = os.path.basename(fullPath)
    new_fullPath = os.path.join(user_output_dir, original_filename)
    new_fullPath = os.path.abspath(new_fullPath)

    # 移动文件到用户专属目录
    shutil.move(fullPath, new_fullPath)

    return new_fullPath


def get_user_file_path(userID: str, filename: str):
    """获取用户文件的完整路径"""
    output_base_dir = os.path.join(os.path.dirname(__file__), "..", "Output")
    user_output_dir = os.path.join(output_base_dir, userID)
    file_path = os.path.join(user_output_dir, filename)
    return os.path.abspath(file_path)
