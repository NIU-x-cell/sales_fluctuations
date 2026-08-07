import os
import time
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
# 导入静态配置
from config import EXCEL_FOLDER, EXCEL_FILES, TABLE_ORDER_ALL, CONNECT_TIMEOUT, READ_TIMEOUT, WRITE_TIMEOUT
# 本地运行需手动读取streamlit secrets，命令行兼容
try:
    import streamlit as st
    DB_SEC = st.secrets["database"]
except Exception:
    # 命令行执行clean_data.py时提示创建secrets
    raise Exception("请在项目 .streamlit/secrets.toml 配置database节点后再运行")

# 组装带SSL、CA的超时连接配置
DB_CONFIG_TIMEOUT = {
    "user": DB_SEC["user"],
    "password": DB_SEC["password"],
    "host": DB_SEC["host"],
    "port": DB_SEC["port"],
    "database": DB_SEC["database"],
    "connect_timeout": CONNECT_TIMEOUT,
    "read_timeout": READ_TIMEOUT,
    "write_timeout": WRITE_TIMEOUT,
    "ssl": {
        "ca": DB_SEC["ca_path"],
        "ssl_mode": "VERIFY_IDENTITY"
    }
}

# SQLAlchemy引擎
engine = create_engine(
    f"mysql+pymysql://{DB_SEC['user']}:{DB_SEC['password']}@{DB_SEC['host']}:{DB_SEC['port']}/{DB_SEC['database']}?charset=utf8mb4&ssl_ca={DB_SEC['ca_path']}&ssl_verify_cert=true&ssl_verify_identity=true&read_timeout={READ_TIMEOUT}",
    pool_pre_ping=True, pool_recycle=300
)

def read_excel_all(file_path):
    """读取单Excel，兼容 500以下 / 500以下1；仅匹配500以上"""
    all_df = []
    sheet_names = pd.ExcelFile(file_path).sheet_names
    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, usecols=["订单时间","订单号","销售额","重量g","物流渠道","订单子状态","物流费"])
        if sheet.startswith("500以下"):
            df["weight_type"] = "below500"
        elif sheet == "500以上":
            df["weight_type"] = "over500"
        else:
            print(f"警告：未知sheet名称【{sheet}】，跳过该工作表")
            continue
        df["order_datetime"] = pd.to_datetime(df["订单时间"], format="%m/%d/%y %H:%M", yearfirst=False)
        df = df.rename(columns={
            "订单号": "order_no",
            "销售额": "sales_amount",
            "重量g": "weight_g",
            "物流渠道": "logistics_channel",
            "订单子状态": "sub_status",
            "物流费": "logistics_fee"
        })
        keep_cols = ["order_no", "sales_amount", "weight_g", "logistics_channel", "order_datetime", "sub_status", "logistics_fee", "weight_type"]
        df = df[keep_cols]
        num_cols = ["sales_amount", "weight_g", "logistics_fee"]
        df[num_cols] = df[num_cols].replace({np.nan: None})
        all_df.append(df)
    return pd.concat(all_df, ignore_index=True)

if __name__ == "__main__":
    total_data = pd.DataFrame()
    for fname in EXCEL_FILES:
        full_path = os.path.join(EXCEL_FOLDER, fname)
        print(f"正在读取文件：{fname}")
        df_single = read_excel_all(full_path)
        total_data = pd.concat([total_data, df_single], ignore_index=True)
        del df_single
    total_data = total_data.replace({np.nan: None})
    print("空值统计（确认无浮点NaN）：")
    print(total_data.isna().sum())

    if not total_data.empty:
        conn_write = pymysql.connect(**DB_CONFIG_TIMEOUT, autocommit=False)
        cur_write = conn_write.cursor()
        insert_sql = f"""
        INSERT INTO {TABLE_ORDER_ALL}
        (order_no, sales_amount, weight_g, logistics_channel, order_datetime, sub_status, logistics_fee, weight_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        batch_size = 1000
        try:
            for i in range(0, len(total_data), batch_size):
                batch = total_data.iloc[i:i + batch_size].to_numpy().tolist()
                cur_write.executemany(insert_sql, batch)
                conn_write.commit()
                print(f"已写入 {min(i + batch_size, len(total_data))}/{len(total_data)} 条订单")
        except Exception as e:
            conn_write.rollback()
            print(f"订单入库失败，已回滚：{str(e)}")
            raise
        finally:
            cur_write.close()
            conn_write.close()
    del total_data
    print("===== 原始订单全部入库完成 =====")
