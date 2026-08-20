# 用户可视化练习验证（原样 + 补全环境）
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

engin = create_engine('mysql+pymysql://root:root123456@127.0.0.1:13306/factory_db')
df_db = pd.read_sql("SELECT * FROM alarms", engin)
print("=== alarms 数据 ===")
print(df_db)

# ===== 用户原代码 =====
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(df_db['id'], df_db['temp'])
axs[0, 1].bar(df_db['id'], df_db['temp'])
axs[1, 0].hist(df_db['temp'], bins = 10)
axs[1, 1].scatter(df_db['id'], df_db['temp'])

try:
    df_db.groupby('device_id')['temp'].mean().plot.bar(x='device_id')
except TypeError as e:
    print("\n[错误] groupby.plot.bar(x=...) 报错:", e)

try:
    sns.boxplot(data=df_db, x='device_id', y='temp')
except Exception as e:
    print("\n[错误] sns.boxplot:", e)
