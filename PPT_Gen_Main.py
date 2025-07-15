from PPT_Gen_functions import generate_ppt_from_user_input, get_template_path
from config import PPT_CONFIG, validate_design_number


def set_design_template(design_number: int):
    """验证设计模板是否可用"""
    if validate_design_number(design_number):
        template_path = get_template_path(design_number)
        print(f"🎨 设计模板已设置为: Design-{design_number}.pptx")
        return template_path
    else:
        available_designs = PPT_CONFIG["available_designs"]
        print(f"⚠️ 未知的设计模板: {design_number}，可用模板: {available_designs}")
        return None


def main():
    """主函数"""
    # 配置参数（可以覆盖config.py中的默认值）
    design_number = 6  # 使用 Design-3.pptx 模板
    expected_slides = 4  # 期望的幻灯片页数(额外还会包含标题页和目录页和总结页)
    custom_filename = None  # 例如: "AI教育应用报告_2024"

    # 验证设计模板
    set_design_template(design_number)

    # 用户输入示例
    user_input = """
   周汇报
参考和学习ardupilot官网：https://ardupilot.org/dev/index.html     ，了解部份无人机飞控知识（
根据nasa官方数据和公式，对无人机的力学做了跟系统的分析，并总结出部分重要公式以供支持
为无人机飞控算法划分出飞控部份；定位算法已经初具雏形，预计下周无人机能够初步实现定位功能，但不能保证效果好，后续可能需要再次修改或重构。
无人机加入电池容量功能，现在无人机续航更真实
    """

    # 生成PPT（使用配置文件中的默认参数，除非明确指定）
    try:
        filename = generate_ppt_from_user_input(
            user_input=user_input,
            expected_slides=expected_slides,
            custom_filename=custom_filename,
            design_number=design_number,
        )
        print(f"\n🎉 成功生成PPT: {filename}")
    except Exception as e:
        print(f"❌ 生成PPT时出错: {e}")


if __name__ == "__main__":
    main()
