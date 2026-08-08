# ====================== 全局配置文件 ======================
import streamlit as st

# 从Streamlit Secrets读取数据库敏感信息
DB_SECRET = st.secrets["database"]
DB_CONFIG = {
    "user": DB_SECRET["user"],
    "password": DB_SECRET["password"],
    "host": DB_SECRET["host"],
    "port": DB_SECRET["port"],
    "database": DB_SECRET["database"],
    "charset": "utf8mb4"
}

# 超时全局常量（统一一处修改，所有地方自动同步）
CONN_TIMEOUT = 3600
READ_TIMEOUT = 3600
WRITE_TIMEOUT = 3600

# SQLAlchemy SSL连接后缀（TiDB Cloud标准SSL校验）
SSL_QUERY_SUFFIX = f"&ssl_verify_cert=true&ssl_verify_identity=true&read_timeout={READ_TIMEOUT}&write_timeout={WRITE_TIMEOUT}"

# 带SSL+超时完整连接配置（pymysql使用）
# 线上环境读取CA证书路径，本地关闭证书校验避免报错
if "ca_path" in DB_SECRET:
    DB_FULL_CONFIG = {
        **DB_CONFIG,
        "connect_timeout": CONN_TIMEOUT,
        "read_timeout": READ_TIMEOUT,
        "write_timeout": WRITE_TIMEOUT,
        "ssl": {
            "ca": DB_SECRET["ca_path"],
            "verify_cert": True
        }
    }
else:
    # 本地开发降级兼容
    DB_FULL_CONFIG = {
        **DB_CONFIG,
        "connect_timeout": CONN_TIMEOUT,
        "read_timeout": READ_TIMEOUT,
        "write_timeout": WRITE_TIMEOUT,
        "ssl": {"verify_cert": False}
    }

# Excel存放根目录（修改成本地真实路径）
EXCEL_FOLDER = r"D:/pycharm/sales_fluctuations/不同克重货物销量分析"
# 所有月份Excel文件名列表
EXCEL_FILES = [
    "订单物流渠道分类202601.xlsx",
    "订单物流渠道分类202602.xlsx",
    "订单物流渠道分类202603.xlsx",
    "订单物流渠道分类202604.xlsx",
    "订单物流渠道分类202605.xlsx",
    "订单物流渠道分类202606.xlsx",
    "订单物流渠道分类202607.xlsx"
]
# 数据库表名统一配置
TABLE_ORDER_ALL = "order_all"
TABLE_WEEK_STAT = "weekly_sales_stat"
# 入库批次大小（提速关键）
INSERT_BATCH_SIZE = 5000
