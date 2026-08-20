import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

data = np.array([85.5, 92.3, 88.2, 95.7, 79.0])
print(data.mean())
print(data.max())
print(data.min())
print(data.std().round(2))
print(data[data > 85])

df = pd.DataFrame({
    "code":   ["E-101", "E-102", "E-103", "E-104"],
    "name":   ["主轴电机", "冷却水泵", "空压机", "振动传感器"],
    "type":   ["电机", "水泵", "空压机", "传感器"],
    "temp":   [85.5, 92.3, 88.2, 45.1],
    "status": [1, 0, 1, 1],
})

print(df[(df['temp'] > 80) & (df['status'] == 1)][['code', 'temp']])

df.groupby('type').agg(
    {'temp': ['mean', 'max']}
)

conn = pymysql.connect(
    host='127.0.0.1',
    port=13306,
    user='root',
    password='root123456',
    database='factory_db',
    charset='utf8mb4'
)

engin = create_engine('mysql+pymysql://root:root123456@127.0.0.1:13306/factory_db')
sql = "SELECT * FROM alarms"
df_db = pd.read_sql(sql, engin)
print(df_db.describe())
print(df_db.groupby('device_id')['temp'].mean())
