# ====================== 全局静态配置（可直接上传GitHub） ======================
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

# 数据库表名统一配置（后续改表名只改此处）
TABLE_ORDER_ALL = "order_all"
TABLE_WEEK_STAT = "weekly_sales_stat"

# 超时全局常量
CONNECT_TIMEOUT = 3600
READ_TIMEOUT = 3600
WRITE_TIMEOUT = 3600
