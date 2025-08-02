"""
Word文档生成器主函数
基于OpenAI API和docxtpl模板生成Word文档
"""

from Word_Gen_functions import generate_wordDoc_from_user_input
from typing import Optional


def generate_word_document(
    learning_content: str,
    user_requirements: Optional[str] = None,
    custom_filename: Optional[str] = None,
) -> str:
    """
    根据用户输入生成Word文档的主函数

    Args:
        learning_content (str): 用户输入的内容提示
        custom_filename (str, optional): 自定义文件名（不包含扩展名）

    Returns:
        str: 生成的文档文件路径

    Raises:
        Exception: 当生成过程中出现错误时抛出异常
    """
    try:
        filename = generate_wordDoc_from_user_input(
            learning_content, user_requirements, custom_filename
        )
        print(f"\n🎉 成功生成Word文档: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 生成Word文档时出错: {e}")
        raise e


def main():
    """主函数 - 示例用法"""

    # 示例用户输入
    learning_content = """
专业教学资料  
主题：PID 控制的“抗饱和（Anti-Windup）机制”——原理、数学建模与工程实现

1. 问题背景  
在连续运行过程中，如果执行器达到其物理极限（如阀门全开、电机电压饱和），误差 e(t)=r(t)−y(t) 仍持续存在，积分器会不断累积误差 → 积分项 I(t) 迅速增大 → 系统出现严重的超调与振荡，该现象称为积分饱和（Integral Wind-up）。

2. 数学模型（标准 PID）  
u(t)=K_p e(t)+K_i∫_0^t e(τ)dτ+K_d de(t)/dt  
当 |u(t)|>u_max 时，实际输出 u_a(t)=sat(u(t))=sign(u(t))·u_max，导致 u(t)≠u_a(t)。

3. 抗饱和目标  
• 在饱和阶段抑制积分项继续增长；  
• 在退出饱和后，系统应快速、平滑地回到线性工作区。

4. 经典抗饱和策略：Back-Calculation（反馈补偿法）  
在标准 PID 之后插入“抗饱和反馈回路”，数学描述：  
e_i(t)=e(t)+K_aw(u_a(t)−u(t))  
积分器改为：  
dI/dt = K_i e_i(t)  
其中 K_aw 为抗饱和增益（1/T_t，T_t 称为跟踪时间常数）。  
• 当未饱和：u=u_a ⇒ e_i=e ⇒ 正常积分；  
• 当饱和：u_a≠u ⇒ e_i≠e，引入负反馈 e_i=e−K_awΔu，Δu=u_a−u，积分器被“拉回”。

5. 稳定性分析  
线性化假设：  
G_aw(s)=K_aw/(s+K_aw)  
可证明：只要 K_aw>0，抗饱和回路自身稳定；闭环稳定性由线性 PID 设计与 K_aw 共同决定。  
推荐整定：T_t≈√(T_i T_d)（Åström-Hägglund 规则），其中 T_i=K_p/K_i，T_d=K_d/K_p。

6. 离散实现（位置式算法）  
伪代码（C 语法）：
```c
float PID_AntiWindup(float r, float y, float u_max)
{
    static float I = 0.0f, y_prev = 0.0f;
    float e  = r - y;
    float P  = Kp * e;
    float D  = Kd * (y_prev - y) / Ts;   // 微分项用测量值差分避免微分冲击
    float u0 = P + I + D;
    float ua = fmaxf(-u_max, fminf(u0, u_max));
    float ei = e + Kaw * (ua - u0);
    I += Ki * ei * Ts;
    y_prev = y;
    return ua;
}
```

7. 工程补充  
• 对多变量系统，可将抗饱和扩展为“方向保持”算法（Directional Anti-Windup）。  
• 实际调试时，可通过阶跃测试观测：饱和阶段 I 分量应被限制；退出饱和后调节时间应缩短。  
• 对伺服电机，可结合电流环限幅、速度前馈，实现级联抗饱和。

8. 小结  
抗饱和不是额外“补丁”，而是 PID 控制器在工程可实施性上的必要组成部分；其设计应遵循：  
(1) 建立饱和非线性模型；  
(2) 选择匹配的抗饱和结构（Back-Calculation、Clamping、Observer-based 等）；  
(3) 通过线性化或小增益定理验证稳定性；  
(4) 在实际硬件上闭环验证动态性能与鲁棒性。

（完）
    """
    user_requirements = (
        "选择题必须全部为单选题！并给出至少5道题目。简答题至少4道。需要有公式考核。"
    )
    custom_filename = "Test"  # 可选的自定义文件名
    # 生成Word文档
    try:
        result_path = generate_word_document(
            learning_content, user_requirements, custom_filename
        )
        print(f"✅ 文档已保存至: {result_path}")
    except Exception as e:
        print(f"⚠️ 生成失败: {e}")


if __name__ == "__main__":
    main()
