# ====================== 全局配置文件 ======================
# MySQL 数据库配置
# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "user": "root",
#     "password": "123456",
#     "database": "cross_sales",
#     "charset": "utf8mb4"
# }
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
# 超时全局常量（统一一处修改，所有地方自动同步）
CONN_TIMEOUT = 3600
READ_TIMEOUT = 3600
WRITE_TIMEOUT = 3600
# SQLAlchemy SSL连接后缀（TiDB Cloud标准SSL校验，与TiDB服务端要求对齐）
SSL_QUERY_SUFFIX = f"&ssl_verify_cert=true&ssl_verify_identity=true&read_timeout={READ_TIMEOUT}&write_timeout={WRITE_TIMEOUT}"
# 带SSL+超时的完整数据库连接配置（供pymysql直接使用）
# 注释：TiDB Cloud必须开启SSL；Windows本地无CA证书文件，关闭证书校验避免本地运行报错
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
