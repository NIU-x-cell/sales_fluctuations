# ====================== 全局配置文件 ======================
# 基础数据库账号配置
DB_CONFIG = {
    "user": "WgiqQ9s6ohsVTx8.root",
    "password": "aqNB84kWuk9mmR0v",
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "database": "cross_sales",
    "charset": "utf8mb4"
}
# 超时全局常量
CONN_TIMEOUT = 3600
READ_TIMEOUT = 3600
WRITE_TIMEOUT = 3600
# SQLAlchemy SSL连接后缀
SSL_QUERY_SUFFIX = f"&ssl_verify_cert=true&ssl_verify_identity=true&read_timeout={READ_TIMEOUT}&write_timeout={WRITE_TIMEOUT}"
# pymysql连接配置，关闭证书校验兼容本地
DB_FULL_CONFIG = {
    **DB_CONFIG,
    "connect_timeout": CONN_TIMEOUT,
    "read_timeout": READ_TIMEOUT,
    "write_timeout": WRITE_TIMEOUT,
    "ssl": {"verify_cert": False}
}
# Excel本地路径（云端无效不影响）
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
# 数据表常量
TABLE_ORDER_ALL = "order_all"
TABLE_WEEK_STAT = "weekly_sales_stat"
INSERT_BATCH_SIZE = 5000
