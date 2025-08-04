from PPT_Gen_functions import generate_ppt_from_user_input, get_template_path
from AIFileGenerator.config import PPT_CONFIG, validate_ppt_design_number


def set_design_template(design_number: int):
    """验证设计模板是否可用"""
    if validate_ppt_design_number(design_number):
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
    design_number = 1  # 使用 Design-3.pptx 模板
    expected_slides = 6  # 期望的幻灯片页数(额外还会包含标题页和目录页和总结页)
    custom_filename = None  # 例如: "AI教育应用报告_2024"

    # 验证设计模板
    # set_design_template(design_number)

    # 用户输入示例
    user_input = """
   7月14日至15日，中央城市工作会议在北京举行。这是时隔10年，党中央再次召开的城市工作会议。习近平总书记出席会议并发表重要讲话，科学回答了做好新时代新征程城市工作的重大理论和实践问题，擘画了建设现代化人民城市的新蓝图。
这次会议从全局和战略高度，首次提出了建设现代化人民城市的目标，明确了“创新、宜居、美丽、韧性、文明、智慧”6个方面的内涵。所部署的7个方面重点任务，紧扣这一目标定位，抓住了群众最为关心、最为期盼的问题，为我们走出一条中国特色城市现代化新路子提供了重要认识论和方法论。
“城市的核心是人”“城市是人民的城市，人民城市为人民”“城市不仅要有高度，更要有温度”……习近平总书记关于城市工作的重要论述，指引我们牢牢把握人民城市的根本属性和价值追求，汇聚起磅礴伟力，推动城市发展取得了历史性成就。
数据显示，我国常住人口城镇化率从2012年的53.1%提高到2024年的67%；2013年到2024年，我国累计实现城镇新增就业超过1.5亿人；2024年，27座城市地区生产总值超过1万亿元。新时代以来，我国城市发展实现新型城镇化水平和城市发展能级、宜居宜业水平等5个方面的大幅提升。从稳步提升城镇化率，到有效破解“大城市病”、盲目扩张“摊大饼”等问题，再到升级完善城市基础设施、逐步完善公共服务功能……正是因为始终践行人民城市理念，城市在我国经济社会发展、文化传承、民生改善中的重要作用得到发挥，为推进中国式现代化提供有力支撑和强大引擎。
必须深刻认识到，以高质量发展全面推进中国式现代化，对城市发展提出了新的更高要求。经历世界历史上规模最大、速度最快的城镇化进程，我国城市发展进入新的历史方位。“我国城镇化正从快速增长期转向稳定发展期，城市发展正从大规模增量扩张阶段转向存量提质增效为主的阶段。”这一重要论断，是这次会议深刻把握我国城市发展规律作出的重大判断。建设现代化人民城市，必须深刻把握这一历史方位，主动适应这一重大变化。
从6个方面的内涵看，“创新、宜居、美丽、韧性、文明、智慧”涵盖了城市建设发展的方方面面，承载着人民对美好生活的向往。不妨以宜居来分析，这是践行人民城市理念的基本要求。能否提供优质的公共服务，则是衡量城市宜居程度的一个重要指标。
新时代以来，我们建成了世界上规模最大的城市住房保障体系，累计开工建设筹集各类保障性住房和棚改安置住房6800多万套，有效解决1.7亿人的住房问题。“十四五”期间，全国护理型养老床位占比提高到64.6%，在300多个地级市和人口大县建设了托育综合服务中心。这些实打实的发展成果，有效提升了城市生活品质、增进了民生福祉。面向未来，坚持人口、产业、城镇、交通一体规划，加快构建房地产发展新模式，提高公共服务水平，着力建设舒适便利的宜居城市，定能让现代化建设成果更多更公平惠及人民。
中国式现代化是前无古人的开创性事业，做好城市工作至关重要、责任重大。我们要把思想和行动统一到习近平总书记重要讲话精神和中央城市工作会议部署上来，进一步增强使命感，树立和践行正确政绩观，
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
