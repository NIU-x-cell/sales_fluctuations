# ====================== 全局配置文件 ======================
# 数据库账号（本地直接用，线上secrets覆盖）
DB_CONFIG = {
    "user": "WgiqQ9s6ohsVTx8.root",
    "password": "aqNB84kWuk9mmR0v",
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "database": "cross_sales",
    "charset": "utf8mb4"
}

# 缩短超时！线上不会无限卡死，30秒连不上直接报错
CONN_TIMEOUT = 30
READ_TIMEOUT = 30
WRITE_TIMEOUT = 30

# pymysql连接：统一关闭证书校验，线上/本地一套逻辑无冲突
DB_FULL_CONFIG = {
    **DB_CONFIG,
    "connect_timeout": CONN_TIMEOUT,
    "read_timeout": READ_TIMEOUT,
    "write_timeout": WRITE_TIMEOUT,
    "ssl": {"verify_cert": False}
}

# 数据库表名统一配置
TABLE_ORDER_ALL = "order_all"
TABLE_WEEK_STAT = "weekly_sales_stat"
# 入库批次大小
INSERT_BATCH_SIZE = 5000

# 本地Excel路径线上不生效，保留不影响运行
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
