# 第 10 课 · PyMySQL：用 Python 操作 MySQL

> 前置：第 9 课完成（SQL 语言）、Docker 里 MySQL 容器 `ai-mysql` 已运行。  
> 目标：用 Python 代码连接 MySQL、执行增删改查、参数化查询防注入——把第 7 周的内存版设备管理系统升级成**数据库版**。  
> 爽点：里程碑 1 你学会"Python 调 API"，今天学"Python 调数据库"——RAG 存元数据、Agent 存记忆、后端开发全都要靠它。C++ 里你写过 `QSqlDatabase` / `ODBC`，PyMySQL 的思路完全一样。

---

## 一、环境准备

**1. 安装 pymysql**（在命令行执行）：

```bash
pip install pymysql
```

**2. 确认 MySQL 容器在跑**：

```bash
docker ps          # 应看到 ai-mysql 容器，状态 Up，端口 0.0.0.0:3306->3306
```

**3. 连接参数**（记住这 5 个）：

| 参数       | 值            | 说明                    |
| -------- | ------------ | --------------------- |
| host     | `127.0.0.1`  | Docker 端口映射到了本机，填本机地址 |
| port     | `3306`       | MySQL 默认端口            |
| user     | `root`       | 容器初始化时设的用户（一般 root）   |
| password | 你的密码         | **换成你创建容器时设的密码**      |
| database | `factory_db` | 第 9 课建好的库             |

## 二、连接 + 第一个查询

```python
import pymysql

# 1. 建立连接（类比 C++: QSqlDatabase::addDatabase("QMYSQL")）
conn = pymysql.connect(
    host="127.0.0.1",       # MySQL 在哪台机器：本机就填 127.0.0.1
    port=3306,              # 端口
    user="root",            # 用户名
    password="你的密码",      # ← 改成你自己的！
    database="factory_db",  # 连哪个库（第 9 课建的）
    charset="utf8mb4"       # 字符集：支持中文（不写会乱码）
)

# 2. 创建游标（类比 C++: QSqlQuery query; 游标 = 执行 SQL 的"手"）
cursor = conn.cursor()

# 3. 执行 SQL——和第 9 课手敲的 SQL 一模一样！
cursor.execute("SELECT * FROM devices")

# 4. 取结果：fetchall() 拿全部行，每行是元组
rows = cursor.fetchall()      # [(1, 'E-101', '主轴电机', '电机', '2024-03-01', 1), ...]
for row in rows:
    print(row)

# 5. 用完关闭（类比 C++ 释放资源，成对出现）
cursor.close()
conn.close()
```

**执行流程四步走**（背下来，每段代码都是这个套路）：

```
连接 conn → 游标 cursor → execute() → fetch/commit → 关闭
```

## 三、增删改：必须 commit()！（重要）

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="你的密码",
                       database="factory_db", charset="utf8mb4")
cursor = conn.cursor()

# 增：插入一台新设备
cursor.execute(
    "INSERT INTO devices (code, name, type, install_date) "
    "VALUES ('E-301', '振动传感器', '传感器', '2026-08-14')"
)

# 🔥 关键：commit() 提交事务！不写这句，数据不真正入库
conn.commit()

# 拿到自增主键 id（刚插入的那行 id 是多少）
print("新设备 id =", cursor.lastrowid)

cursor.close()
conn.close()
```

**C++ 类比**：数据库默认是**手动提交事务**模式——`INSERT/UPDATE/DELETE` 之后必须 `commit()`，就像 C++ 里打开文件写完必须 `fflush`/`fclose`，否则数据只停在缓冲区。**忘写 commit 是 PyMySQL 第一坑**：代码不报错，但数据没写进去。

## 四、参数化查询：防 SQL 注入（安全红线）

❌ **错误写法**：把用户输入拼进 SQL 字符串

```python
code = input("要删除的设备编号：")
cursor.execute(f"DELETE FROM devices WHERE code = '{code}'")   # ❌ 千万别学！
```

如果用户输入 `' OR '1'='1`，拼出来变成：

```sql
DELETE FROM devices WHERE code = '' OR '1'='1'   -- 条件永远成立 → 删光整张表！
```

这就是 **SQL 注入**——C++ 里类比：把用户输入直接拼进 `system()` 命令。

✅ **正确写法**：`%s` 占位符 + 参数元组

```python
code = input("要删除的设备编号：")
cursor.execute("DELETE FROM devices WHERE code = %s", (code,))
#                                        ↑占位符   ↑参数用元组传
# pymysql 会自动转义特殊字符，注入字符变成普通文本，安全！
```

**规则**：**任何带用户输入的 SQL，一律参数化**。`%s` 的位置自动变成 `'值'`（带引号转义），不需要你手动加引号。

## 五、查询返回值的处理

```python
# fetchone()：只取第一行（找不到返回 None）
cursor.execute("SELECT * FROM devices WHERE code = %s", ("E-101",))
row = cursor.fetchone()
if row:
    code, name, type_, install_date, status = row[1], row[2], row[3], row[4], row[5]
    print(f"{row[1]} {row[2]} 状态={'运行' if row[5] == 1 else '停机'}")

# fetchall()：取全部行 → 列表套元组
cursor.execute("SELECT type, AVG(temp) FROM alarms GROUP BY type")
for type_, avg_temp in cursor.fetchall():
    print(type_, round(avg_temp, 1))
```

**C++ 类比**：`fetchone` ≈ 读第一行；`fetchall` ≈ 把结果集全捞进容器；`row[0]`、`row[1]` ≈ 按列下标访问（元组下标从 0 开始）。

## 六、综合案例：设备管理系统（数据库版）

把第 7 周内存版升级为 MySQL 版——**一个类封装所有数据库操作**：

```python
import pymysql

class DeviceRepo:
    """设备仓库：所有数据库操作都封装在这（类比第 7 周 DeviceService + 数据库）"""

    def __init__(self, password: str):
        # 每次操作都新建连接（简单易懂；性能要求高时用连接池，后面 RAG 项目再讲）
        self.conn = pymysql.connect(
            host="127.0.0.1", port=3306,
            user="root", password=password,
            database="factory_db", charset="utf8mb4"
        )
        self.cursor = self.conn.cursor()

    def add_device(self, code: str, name: str, type_: str):
        """新增设备"""
        self.cursor.execute(
            "INSERT INTO devices (code, name, type) VALUES (%s, %s, %s)",
            (code, name, type_)          # 参数化！安全
        )
        self.conn.commit()               # 别忘了提交
        print(f"✅ 已添加 {name}，id = {self.cursor.lastrowid}")

    def find_by_code(self, code: str):
        """按编号查设备，返回 None 表示不存在"""
        self.cursor.execute(
            "SELECT * FROM devices WHERE code = %s", (code,)
        )
        return self.cursor.fetchone()    # 没有则返回 None

    def list_all(self):
        """列出全部设备"""
        self.cursor.execute("SELECT * FROM devices")
        return self.cursor.fetchall()

    def set_status(self, code: str, status: int):
        """启停设备：1=运行 0=停机"""
        self.cursor.execute(
            "UPDATE devices SET status = %s WHERE code = %s",
            (status, code)               # 两个占位符，两个参数
        )
        self.conn.commit()
        print(f"✅ {code} 状态已更新")

    def close(self):
        """关闭连接（程序结束前调用）"""
        self.cursor.close()
        self.conn.close()

# ── 使用示例 ──────────────────────────────
if __name__ == "__main__":
    repo = DeviceRepo("你的密码")          # ← 改成你的密码
    repo.add_device("E-302", "压力变送器", "传感器")
    print(repo.find_by_code("E-101"))     # 查询
    repo.set_status("E-102", 0)           # 停机
    for d in repo.list_all():
        print(d)
    repo.close()
```

## 七、练习任务（打卡标准）

1. **连接测试**：写脚本连接 `factory_db`，执行 `SELECT COUNT(*) FROM devices` 打印设备总数（先 `docker ps` 确认容器在跑）
2. **参数化查询**：写一个 `add_alarm(device_id, temp)` 函数，插入一条报警记录（参数化防注入），commit 后用第 9 课的 SQL 验证
3. **防注入演示**：故意构造 `"E-101' OR '1'='1"` 作为查询条件，验证参数化后**不会**返回所有行（对比字符串拼接的后果）
4. **综合**：把上面的 `DeviceRepo` 跑起来，增删改查各操作一次，贴出运行结果

## 八、常见

- ❌ **忘 `commit()`** → 数据没写入但也不报错（先查有没有 commit）
- ❌ 密码错误 → `Access denied for user 'root'@'...'`（检查密码/host）
- ❌ `Unknown database 'factory_db'` → 库没建，先回第 9 课建库
- ❌ 中文乱码 → 连接加 `charset="utf8mb4"`
- ❌ `%s` 参数个数和占位符个数不匹配 → `not enough arguments for format string`
- ⚠️ 用完不 `close()` → 连接泄漏（程序可能卡死）；用 `try/finally` 或 `with` 更稳

## 九、预告

- 第 11 课：**Numpy / Pandas**——Python 数据分析双雄。拿到一批设备运行数据，怎么快速算均值/分组统计？Pandas 一行搞定，模块 5 RAG 的数据预处理主力。
- 第 9 周收官后，模块 2 语言进阶全部完成 → 进入模块 3 智能体平台（Coze / Dify）
