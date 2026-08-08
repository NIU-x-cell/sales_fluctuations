# ====================== 全局配置文件 ======================
# 数据库账号硬编码，无需读取secrets，彻底规避secrets读取报错
DB_CONFIG = {
    "user": "WgiqQ9s6ohsVTx8.root",
    "password": "aqNB84kWuk9mmR0v",
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "database": "cross_sales",
    "charset": "utf8mb4"
}

# 缩短超时30秒，不会无限阻塞数据库连接
CONN_TIMEOUT = 30
READ_TIMEOUT = 30
WRITE_TIMEOUT = 30

# 统一关闭SSL证书校验，消除线上/本地证书路径差异冲突
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

# 本地Excel路径，线上不生效，保留不影响运行
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
