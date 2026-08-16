# 第 11 课 · Numpy / Pandas：数据分析双雄

> 前置：第 10 课完成（PyMySQL）。
> 目标：掌握 Numpy 数组计算 + Pandas 表格分析（筛选/分组/清洗），能对设备运行数据做统计。
> 爽点：RAG 项目的数据预处理主力；C++ 里处理数据你写 for 循环 + vector，Pandas 一行搞定；而且 Pandas 能直接读 MySQL 查询结果——和上一课无缝衔接。

---

## 一、为什么需要 Numpy / Pandas？

**纯 Python 处理大量数值**：for 循环逐个算，慢（Python 是解释型，10 万个数逐个循环很吃亏）。
**Numpy**：底层是 C 写的数组，批量运算快几十倍。`vector` 的威力但直接对整块数据操作。
**Pandas**：像"Excel + SQL 的结合体"，管的是**带行列标签的表格**——筛选、分组、清洗数据。

```bash
pip install numpy pandas    # 装两个库（数据分析标配）
```

## 二、Numpy：多维数组（ndarray）

```python
import numpy as np

# 1. 创建数组（类比 C++: std::vector<double> v = {1,2,3};）
a = np.array([1.0, 2.0, 3.0, 4.0])
print(a)                     # [1. 2. 3. 4.]
print(a.shape)               # (4,)  ← 形状：一维，4 个元素

# 等差数列（类比 C++ for 循环生成）
b = np.arange(1, 10, 2)      # 1,3,5,7,9（start, stop, step，不含 10）
print(b)                     # [1 3 5 7 9]

# 全 0 / 全 1（初始化用）
zeros = np.zeros(5)          # [0. 0. 0. 0. 0.]
ones  = np.ones(5)           # [1. 1. 1. 1. 1.]

# 2. 索引与切片（和 Python 列表、C++ 数组下标一样）
print(a[0])                  # 1.0  第一个元素
print(a[1:3])                # [2. 3.]  切片 [1,3)
print(a[-1])                 # 4.0  最后一个（-1 = 倒数第 1）

# 3. 批量运算（🔥 Numpy 核心威力：不用写循环！）
temps = np.array([85.5, 92.3, 88.2, 95.7])
print(temps + 1)             # 每个元素 +1（对标 C++: for(...) t += 1;）
print(temps * 2)             # 每个元素 *2
print(temps > 90)            # [False  True False  True] ← 布尔数组（筛选用）
print(temps.mean())          # 90.425  平均值
print(temps.max(), temps.min())   # 95.7 85.5
print(temps.std())           # 标准差（波动多大）
```

**C++ 类比**：`temps + 1` ≈ `std::transform` 对整块数组操作；`mean()/std()`  ≈ 手写累加统计，Numpy 一行。

## 三、Pandas 核心：Series 和 DataFrame

**Series** = 一列带标签的数据（带"行名"的数组）
**DataFrame** = 二维表格（带行列标签，像 Excel 表 / SQL 结果集）

```python
import pandas as pd

# 1. Series：一列数据 + 索引标签
s = pd.Series([85.5, 92.3, 88.2], index=["E-101", "E-102", "E-103"])
print(s["E-102"])            # 92.3  按标签取（不是按下标！）
print(s.mean())              # 88.67

# 2. DataFrame：字典创建，键=列名，值=列表
df = pd.DataFrame({
    "code":   ["E-101", "E-102", "E-103", "E-104"],
    "name":   ["主轴电机", "冷却水泵", "空压机", "振动传感器"],
    "type":   ["电机", "水泵", "空压机", "传感器"],
    "temp":   [85.5, 92.3, 88.2, 45.1],
    "status": [1, 0, 1, 1],
})
print(df)                    # 一张整齐的表格
print(df.shape)              # (4, 5)  4行5列
```

**C++ 类比**：DataFrame ≈ `std::vector<std::map<std::string, 值>>` 的"表格式"封装，但自带列名访问。

## 四、DataFrame 常用操作（重点）

```python
# 1. 看数据
print(df.head(2))            # 前 2 行（数据多时看开头）
print(df.info())             # 每列类型、有无缺失（类比 SQL DESCRIBE）
print(df.describe())         # 数值列的 count/mean/min/max（一行全统计！）

# 2. 取列 / 取行
print(df["name"])            # 取一列（返回 Series）
print(df[["code", "temp"]])  # 取多列
print(df.loc[0])             # 按行标签取第 0 行
print(df.iloc[1])            # 按行位置取第 1 行

# 3. 筛选（🔥 最常用：布尔条件）
hot = df[df["temp"] > 80]    # 温度超 80 的设备（类比 SQL WHERE temp > 80）
print(hot)
motors = df[df["type"] == "电机"]
print(motors)

# 组合条件：&（且） |（或），每个条件要加括号
warning = df[(df["temp"] > 80) & (df["status"] == 1)]
print(warning)

# 4. 新增列（计算列）
df["temp_c"] = df["temp"] * 1.0   # 可以给每行算个新字段
df["alert"]  = df["temp"] > 80    # 布尔列

# 5. 分组聚合（🔥 类比 SQL GROUP BY）
by_type = df.groupby("type")["temp"].mean()   # 每种设备平均温度
print(by_type)

# 6. 排序
df.sort_values("temp", ascending=False)       # 按温度降序
```

**SQL 对照表**（把第 9 课和这里打通）：

| SQL | Pandas |
|---|---|
| `WHERE temp > 80` | `df[df["temp"] > 80]` |
| `GROUP BY type, AVG(temp)` | `df.groupby("type")["temp"].mean()` |
| `ORDER BY temp DESC` | `df.sort_values("temp", ascending=False)` |
| `LIMIT 2` | `df.head(2)` |
| `JOIN` | `pd.merge()`（下一节） |

## 五、数据清洗 + 连接 MySQL（工业场景综合）

```python
# 1. 缺失值处理（真实数据常有 NaN = 空值）
df2 = pd.DataFrame({"code": ["E-101", "E-102"], "temp": [85.5, None]})
print(df2.isna())                # 哪里是空的？ True/False 表
print(df2.dropna())              # 删掉有空值的行
print(df2.fillna(0))             # 把空值填成 0（或用均值：fillna(df2["temp"].mean())）

# 2. 读取 CSV（RAG 阶段解析文档数据常用）
# df = pd.read_csv("运行日志.csv")

# 3. 直接读 MySQL 查询结果（🔥 和第 10 课接上！）
import pymysql
import pandas as pd

conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="你的密码",
                       database="factory_db", charset="utf8mb4")
df_db = pd.read_sql("SELECT * FROM alarms", conn)   # SQL 结果直接变 DataFrame！
print(df_db.head())
conn.close()

# 4. 两张表合并（类比 SQL JOIN）
# 设备表 + 报警表按 device_id 合并
repairs = pd.DataFrame({"device_id": [1, 2], "reason": ["轴承磨损", "过载"]})
merged = pd.merge(df_db, repairs, on="device_id", how="left")
```

## 六、练习任务（打卡标准）

1. **Numpy 统计**：造一个温度数组 `np.array([85.5, 92.3, 88.2, 95.7, 79.0])`，打印均值/最大/最小/标准差，再筛出 `> 85` 的
2. **DataFrame 筛选**：用本课的设备示例 df，找出"温度 > 80 且 状态=运行"的设备，打印 code 和 temp
3. **分组聚合**：按 `type` 分组，求每种设备的平均温度和最大温度（提示：`groupby(...).agg({"temp": ["mean", "max"]})`）
4. **综合（连接上一课）**：用 `pd.read_sql` 把 `factory_db` 里 `alarms` 表读成 DataFrame，打印 `describe()` 结果 + 按 device_id 分组的平均温度

## 七、常见坑

- ❌ `pip install` 后 import 报错 → 确认装到了**你运行 Python 的那个环境**（如 venv 装错位置）
- ❌ `df["temp"] > 80` 直接 `if` 判断 → 报错（结果是数组），必须放在 `df[...]` 里当筛选条件
- ❌ 组合条件写成 `(a) and (b)` → 报错，必须用 `&`/`|` 且每个条件加括号
- ⚠️ 中文列名/数据乱码 → `pd.read_csv(..., encoding="utf-8")`；读 MySQL 连接要 `charset="utf8mb4"`
- ⚠️ `df["temp"]` 返回 Series，`df[["temp"]]` 返回 DataFrame——列名列表要双括号

## 八、第 9 周收官 + 预告

🎉 **模块 2（语言进阶）全部完成**：Python 核心语法 + OOP + 高阶特性 + MySQL + PyMySQL + Numpy/Pandas——写 RAG、Agent 的语法和数据地基已经打牢。

- **模块 3 智能体平台**（第 10–12 周）：Prompt 工程系统学习 → Coze 搭建智能体 → Dify 私有化部署（Ollama + 知识库 RAG + Agent）——你的第一个"真智能体"项目
- 如果好奇 RAG 长什么样，模块 5 见真章；模块 3 的 Dify 会提前让你摸到 RAG 的门
