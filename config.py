import streamlit as st
import os

# 捕获secrets读取失败，防止直接崩溃
try:
    DB_SECRET = st.secrets["database"]
except Exception as e:
    st.error(f"Secrets配置读取失败：{str(e)}")
    st.stop()

# 基础数据库参数
DB_CONFIG = {
    "user": DB_SECRET["user"],
    "password": DB_SECRET["password"],
    "host": DB_SECRET["host"],
    "port": DB_SECRET["port"],
    "database": DB_SECRET["database"],
    "charset": "utf8mb4"
}

# 超时常量（缩短连接超时，避免无限卡死）
CONN_TIMEOUT = 30
READ_TIMEOUT = 30
WRITE_TIMEOUT = 30

# SSL证书兼容判断：文件存在才启用ca校验，否则关闭ssl验证
ssl_param = {}
if "ca_path" in DB_SECRET and os.path.isfile(DB_SECRET["ca_path"]):
    ssl_param["ssl"] = {
        "ca": DB_SECRET["ca_path"],
        "verify_cert": True
    }
else:
    ssl_param["ssl"] = {"verify_cert": False}

# 完整pymysql连接参数
DB_FULL_CONFIG = {
    **DB_CONFIG,
    "connect_timeout": CONN_TIMEOUT,
    "read_timeout": READ_TIMEOUT,
    "write_timeout": WRITE_TIMEOUT,
    **ssl_param
}

# 全局表名
TABLE_ORDER_ALL = "order_all"
TABLE_WEEK_STAT = "weekly_sales_stat"
INSERT_BATCH_SIZE = 5000

# 本地Excel路径（线上无用，保留不影响）
EXCEL_FOLDER = r"D:/pycharm/sales_fluctuations/不同克重货物销量分析"
EXCEL_FILES = [
    "订单物流渠道分类202601.xlsx",
    "订单物流渠道分类202602.xlsx",
    "订单物流渠道分类202603.xlsx",
    "订单物流渠道分类202604.xlsx",
    "订单物流渠道分类202605.xlsx",
    "订单物流渠道分类202606.xlsx",
    "订单物流渠道分类202607.xlsx"
]
