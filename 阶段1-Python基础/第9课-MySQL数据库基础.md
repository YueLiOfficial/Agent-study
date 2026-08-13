# 第 9 课 · MySQL 数据库基础（SQL 语言）

> 前置：第 8 课完成（闭包/装饰器/生成器/正则）。
> 目标：理解关系型数据库核心概念，学会建库建表、增删改查、聚合分组、连接查询——把第 7 周"设备管理系统"的数据从内存/文件升级到数据库。
> 爽点：你做过 C++ 桌面端，多半用过 SQLite / SQL Server——**MySQL 的 SQL 语法和它们 90% 相同**，今天只是换个"真正的数据库"；而且这是模块 5 RAG 的数据地基，也是简历上必写的技能点。

---

## 一、为什么要用数据库？

第 7 周的设备管理系统，数据存在 Python 列表/字典里——**程序一关，数据全没了**。存文件（json/csv）也行，但有问题：

| 痛点 | 说明 |
|---|---|
| 并发 | 两个进程同时写一个文件 → 数据错乱 |
| 查询慢 | 100 万条记录找一台设备，得全文件扫一遍 |
| 无一致性 | 改一半断电，数据就坏了 |

**关系型数据库**（MySQL）就是解决这些问题的：数据存成**表**，用 SQL 语言查。

**核心概念对照 C++**：

| 数据库概念 | 类比 C++ | 说明 |
|---|---|---|
| 表（table） | struct 数组 / 一张 Excel 表 | 一类数据的集合 |
| 行（row） | 一个 struct 实例 | 一条记录 |
| 列（column） | struct 的一个字段 | 一个属性 |
| 主键（primary key） | 唯一 ID 字段 | 每行必须有且唯一的标识 |
| 外键（foreign key） | 指针/ID 引用 | 表之间的关联 |

**MySQL 是什么**：全球最流行的开源关系型数据库，阿里、腾讯、字节都在大规模使用——**就业必备技能**，学 RAG、学后端都得过这一关。

## 二、安装与启动（本机还没有 MySQL，二选一）

### 方案 A：官方图形安装（适合不想折腾）
1. 下载地址：https://dev.mysql.com/downloads/installer/ → 选 **MySQL Installer for Windows**（约 400MB）
2. 安装时选 **Developer Default**，一路 Next
3. 设置 root 密码（比如 `root123`，记住它），端口默认 3306
4. 装完开始菜单里启动 **MySQL Command Line Client**，输入密码即进入

### 方案 B：ZIP 免安装版（适合程序员，AI 可帮你自动化）
1. 下载：https://dev.mysql.com/downloads/mysql/ → 选 **Windows (x86, 64-bit), ZIP Archive**（约 230MB）
2. 解压后，在 bin 目录执行初始化 + 启动（AI 可以帮你一条龙搞定）

**验证是否装好**（任选其一）：
```bash
mysql --version          # 能看到版本号
# 或进入交互界面：
mysql -u root -p         # 输入密码后出现 mysql> 提示符
```

> ⚠️ 如果暂时装不了 MySQL，也可以用 Python 自带的 **sqlite3** 模块先学 SQL 语法（90% 通用），但**最终一定要装 MySQL**——这是就业技能，装好后再把练习重跑一遍。

## 三、建库建表（CREATE / USE）

```sql
-- 注释用 -- 后跟一个空格（或 #）
CREATE DATABASE IF NOT EXISTS factory_db;   -- 建库（工厂数据库）
USE factory_db;                              -- 切换到该库

-- 建设备表：注意每列的类型和约束
CREATE TABLE devices (
    id           INT PRIMARY KEY AUTO_INCREMENT,  -- 主键，自动增长（1,2,3...）
    code         VARCHAR(20) NOT NULL UNIQUE,     -- 设备编号 E-101，非空且唯一
    name         VARCHAR(50) NOT NULL,            -- 设备名称
    type         VARCHAR(20),                     -- 类型：电机/水泵/空压机
    install_date DATE,                            -- 安装日期（只有日期）
    status       TINYINT DEFAULT 1                -- 1=运行，0=停机
);
```

**MySQL 常用数据类型对照 C++**：

| MySQL 类型 | C++ 类比 | 说明 |
|---|---|---|
| `INT` | `int` | 整数 |
| `BIGINT` | `long long` | 大整数 |
| `VARCHAR(n)` | `std::string` | 变长字符串，最多 n 个字符 |
| `DECIMAL(10,2)` | `double`（但更精确） | 精确小数：共 10 位，2 位小数（存钱、温度） |
| `FLOAT` / `DOUBLE` | `float` / `double` | 浮点数 |
| `DATETIME` | `std::chrono` / `time_t` | 日期+时间 |
| `TINYINT` | `bool` / `char` | 小整数，常用 0/1 当布尔 |

**约束速查**：`PRIMARY KEY` 主键 · `NOT NULL` 非空 · `UNIQUE` 唯一 · `DEFAULT x` 默认值 · `AUTO_INCREMENT` 自增。

## 四、增删改查（INSERT / SELECT / UPDATE / DELETE）

```sql
-- 1. 增：插入 3 台设备（id 不用写，自动生成）
INSERT INTO devices (code, name, type, install_date) VALUES
('E-101', '主轴电机', '电机', '2024-03-01'),
('E-102', '冷却水泵', '水泵', '2024-05-12'),
('E-201', '空压机',   '空压机', '2025-01-20');

-- 2. 查：全部
SELECT * FROM devices;

-- 3. 查：只看两列 + 加条件
SELECT name, type FROM devices WHERE type = '电机';

-- 4. 查：模糊匹配（% 是通配符，任意字符）
SELECT * FROM devices WHERE name LIKE '%电机%';

-- 5. 改：把 E-102 停机
UPDATE devices SET status = 0 WHERE code = 'E-102';

-- 6. 删：删除空压机
DELETE FROM devices WHERE code = 'E-201';

-- 7. 排序 + 限量：按安装日期倒序，只要前 2 条
SELECT * FROM devices ORDER BY install_date DESC LIMIT 2;
```

> 🔥 **头号大坑**：`UPDATE` 和 `DELETE` **忘写 WHERE = 全表遭殃**！
> C++ 里你忘写 `if` 条件顶多逻辑错，SQL 里忘写 WHERE 直接删光整张表。**任何 UPDATE/DELETE 先 SELECT 验证 WHERE 对不对。**

## 五、聚合与分组（统计一列）

```sql
-- 建一张报警记录表（后面练习要用）
CREATE TABLE alarms (
    id        INT PRIMARY KEY AUTO_INCREMENT,
    device_id INT NOT NULL,               -- 哪台设备（关联 devices.id）
    temp      DECIMAL(5,1),               -- 报警时温度，如 85.5
    happened  DATETIME                    -- 报警时间
);

INSERT INTO alarms (device_id, temp, happened) VALUES
(1, 85.5, '2026-08-10 08:30:00'),
(1, 88.2, '2026-08-11 09:15:00'),
(2, 92.3, '2026-08-11 14:00:00'),
(2, 91.0, '2026-08-12 10:20:00'),
(2, 95.7, '2026-08-13 07:45:00');

-- 1. 计数 / 平均 / 最大 / 最小
SELECT COUNT(*)  AS 报警次数,      -- AS 给结果列起别名
       AVG(temp) AS 平均温度,
       MAX(temp) AS 最高温度,
       MIN(temp) AS 最低温度
FROM alarms;

-- 2. 按设备分组统计（GROUP BY：按 device_id 分成一组一组的）
SELECT device_id, COUNT(*) AS 次数, AVG(temp) AS 平均温度
FROM alarms
GROUP BY device_id;

-- 3. 分组后过滤（HAVING：对"组"过滤；WHERE 是对"行"过滤）
SELECT device_id, COUNT(*) AS 次数
FROM alarms
GROUP BY device_id
HAVING COUNT(*) >= 3;          -- 只看报警 ≥3 次的设备
```

**WHERE vs HAVING**（高频面试题）：
- `WHERE`：**分组之前**过滤行（先筛数据再分组）
- `HAVING`：**分组之后**过滤组（对聚合结果筛选）

## 六、连接查询（JOIN：多表关联）

为什么拆成两张表？如果设备信息每报一次警都复制一份，10 万条报警就有 10 万份重复的设备名——**浪费 + 改设备名要改 10 万处**。所以用 `device_id` 关联。

```sql
-- 查每条报警的设备编号和名称（INNER JOIN = 两张表按条件拼起来）
SELECT d.code, d.name, a.temp, a.happened
FROM alarms a                    -- 给表起别名：a = alarms
JOIN devices d ON a.device_id = d.id   -- 关联条件
WHERE a.temp >= 90;
```

**C++ 类比**：相当于两个 vector 按 ID 做 hash 连接——`device_id` 就是"指针"，JOIN 就是解引用取对方字段。

## 七、练习任务（打卡标准）

在 MySQL 里完整跑一遍下面流程（截图或复制输出给我检查）：

1. **建库建表**：建 `factory_db`，建 `devices` 和 `alarms` 两张表（按上文 SQL，含主键/自增/外键概念）
2. **增删改查**：插入 3 台设备 + 5 条报警；把 E-102 状态改为停机；删除你插入的第 3 台设备
3. **聚合**：查每种设备类型下，所有设备的平均温度（提示：需要 JOIN 后 GROUP BY type）——结果应该能看出哪类设备最热
4. **思考题**：为什么 `alarms` 表不直接存 `code`/`name`，而只存 `device_id`？用 50 字说清楚

## 八、常见坑

- ❌ `UPDATE/DELETE` 忘写 `WHERE` → **全表修改/删除**（先 SELECT 验证）
- ❌ SQL 语句末尾忘了分号 `;` → 命令不执行（交互模式卡住）
- ❌ 字符串用了中文引号 `"E-101"` → 语法错误（SQL 字符串用英文单引号 `'E-101'`）
- ❌ `VARCHAR` 长度设太小（如 5）存 "冷却水泵" → 报错 Data too long
- ⚠️ `NULL` 和空字符串 `''` 不一样：NULL 是"没有值"，`WHERE name IS NULL` 查 NULL，`= ''` 查空串
- ⚠️ `COUNT(*)` 统计所有行；`COUNT(列名)` 会跳过该列为 NULL 的行

## 九、预告

- 第 10 课：**PyMySQL**——用 Python 代码连 MySQL（参数化查询防注入），把设备管理系统真正变成"数据库版"
- 第 11 课：**Numpy / Pandas**——Python 数据分析双雄，模块 5 RAG 的数据预处理主力
