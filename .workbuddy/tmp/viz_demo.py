# 第 11 课扩展 · 数据可视化演示
# 场景：工厂设备报警温度分析（衔接第 9 课 alarms 表数据）
import matplotlib
matplotlib.use("Agg")  # 无窗口模式，保存为图片文件
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 关键坑1：Matplotlib 默认不支持中文，必须指定中文字体，否则全是方块
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 让负号正常显示

# ---------- 数据：仿照 alarms 表 ----------
devices = ["E-101 主轴电机", "E-102 冷却水泵", "E-103 空压机"]
alarm_count = [2, 3, 0]          # 各设备报警次数
temps = [85.5, 92.3, 88.2, 95.7, 79.0]  # 报警时温度
times = np.array([1, 2, 3, 4, 5])       # 报警次序

# ---------- 图1：四宫格 subplot（一张画布放 4 张图） ----------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# 1. 折线图：温度随报警次序变化（趋势）
axes[0, 0].plot(times, temps, marker="o", color="#185FA5", linewidth=2)
axes[0, 0].set_title("报警温度趋势（折线图）")
axes[0, 0].set_xlabel("报警次序")
axes[0, 0].set_ylabel("温度 ℃")
axes[0, 0].grid(True, alpha=0.3)

# 2. 柱状图：各设备报警次数（对比）
axes[0, 1].bar(devices, alarm_count, color="#0F6E56")
axes[0, 1].set_title("各设备报警次数（柱状图）")
axes[0, 1].set_ylabel("次数")

# 3. 直方图：温度分布（数据集中在哪个区间）
axes[1, 0].hist(temps, bins=5, color="#D85A30", edgecolor="white")
axes[1, 0].set_title("报警温度分布（直方图）")
axes[1, 0].set_xlabel("温度 ℃")
axes[1, 0].set_ylabel("次数")

# 4. 散点图：温度-时间关系（看离群点）
axes[1, 1].scatter(times, temps, s=80, color="#534AB7")
axes[1, 1].set_title("温度散点（散点图）")
axes[1, 1].set_xlabel("报警次序")
axes[1, 1].set_ylabel("温度 ℃")

plt.tight_layout()
plt.savefig(r"C:\Users\YueLi\Desktop\Agent-study\阶段1-Python基础\可视化演示1_matplotlib基础.png", dpi=110)
plt.close()

# ---------- 图2：Pandas 一行流绘图 ----------
df = pd.DataFrame({
    "device": devices,
    "count":  alarm_count,
    "avg_temp": [86.85, 93.0, 0],
})
ax = df.plot.bar(x="device", y="count", legend=False,
                 color="#185FA5", title="Pandas 一行绘图：设备报警次数", figsize=(8, 5))
ax.set_ylabel("次数")
plt.tight_layout()
plt.savefig(r"C:\Users\YueLi\Desktop\Agent-study\阶段1-Python基础\可视化演示2_pandas绘图.png", dpi=110)
plt.close()

# ---------- 图3：Seaborn 风格示例 ----------
df2 = pd.DataFrame({
    "device": ["E-101"]*2 + ["E-102"]*3 + ["E-103"]*2,
    "temp":   [85.5, 88.2, 92.3, 91.0, 95.7, 79.0, 80.5],
})
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.boxplot(data=df2, x="device", y="temp", palette="Set2")
plt.title("Seaborn 箱线图：各设备温度分布")
plt.tight_layout()
plt.savefig(r"C:\Users\YueLi\Desktop\Agent-study\阶段1-Python基础\可视化演示3_seaborn.png", dpi=110)
plt.close()

print("三张图生成完毕")
