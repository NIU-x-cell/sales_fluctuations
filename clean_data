import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import plotly.graph_objects as go
from datetime import datetime, timedelta
# 导入静态配置（无密码）
from config import TABLE_ORDER_ALL, CONNECT_TIMEOUT, READ_TIMEOUT, WRITE_TIMEOUT

# -------------------------- 统一读取Secrets数据库配置 --------------------------
def get_db_secrets():
    """读取streamlit secrets里的database配置"""
    sec = st.secrets["database"]
    return {
        "user": sec["user"],
        "password": sec["password"],
        "host": sec["host"],
        "port": sec["port"],
        "database": sec["database"],
        "ca_path": sec["ca_path"]
    }

# 获取数据库密钥
DB_SEC = get_db_secrets()

def get_mysql_conn():
    """原生pymysql连接，带TiDB CA证书SSL"""
    conn = pymysql.connect(
        host=DB_SEC["host"],
        port=DB_SEC["port"],
        user=DB_SEC["user"],
        password=DB_SEC["password"],
        database=DB_SEC["database"],
        connect_timeout=CONNECT_TIMEOUT,
        read_timeout=READ_TIMEOUT,
        write_timeout=WRITE_TIMEOUT,
        ssl={
            "ca": DB_SEC["ca_path"],
            "ssl_verify_cert": True,
            "ssl_mode": "VERIFY_IDENTITY"
        }
    )
    return conn

def get_sqlalchemy_engine():
    """SQLAlchemy引擎，适配Streamlit云端SSL CA"""
    user = DB_SEC["user"]
    pwd = DB_SEC["password"]
    host = DB_SEC["host"]
    port = DB_SEC["port"]
    db = DB_SEC["database"]
    ca = DB_SEC["ca_path"]

    conn_url = (
        f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
        "?charset=utf8mb4"
        f"&ssl_ca={ca}"
        "&ssl_verify_cert=true"
        "&ssl_verify_identity=true"
        f"&connect_timeout={CONNECT_TIMEOUT}"
        f"&read_timeout={READ_TIMEOUT}"
    )
    engine = create_engine(conn_url, pool_pre_ping=True, pool_recycle=300)
    return engine

# 按月拆分批量获取周聚合数据，避免TiDB内存超限
def get_all_week_data(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    engine = get_sqlalchemy_engine()
    all_parts = []
    current = datetime(start_date.year, start_date.month, 1).date()

    while current <= end_date:
        slice_end = current + timedelta(days=30)
        if slice_end > end_date:
            slice_end = end_date

        sql = """
        SELECT
            DATE_SUB(order_datetime, INTERVAL WEEKDAY(order_datetime) DAY) AS stat_week,
            weight_type,
            COUNT(1) AS total_orders,
            SUM(sales_amount) AS total_sales
        FROM {} USE INDEX(idx_order_date_weight)
        WHERE order_datetime >= %s AND order_datetime <= %s
        GROUP BY stat_week, weight_type
        ORDER BY stat_week;
        """.format(TABLE_ORDER_ALL)

        df_part = pd.read_sql(sql, engine, params=(current, slice_end))
        all_parts.append(df_part)
        current = slice_end + timedelta(days=1)
    
    engine.dispose()
    if not all_parts:
        return pd.DataFrame()
    return pd.concat(all_parts, ignore_index=True)

# -------------------------- 页面渲染逻辑完全不变 --------------------------
st.set_page_config(page_title="Ozon跨境周销量波动分析看板", layout="wide")
st.title("跨境Ozon平台 500g上下周销量波动分析看板")
st.divider()

# 获取全表最小最大日期
conn_cursor = get_mysql_conn()
cursor = conn_cursor.cursor()
cursor.execute(f"SELECT MIN(order_datetime), MAX(order_datetime) FROM {TABLE_ORDER_ALL};")
min_db_dt, max_db_dt = cursor.fetchone()
cursor.close()
conn_cursor.close()

# 侧边栏时间筛选
with st.sidebar:
    st.header("时间筛选器")
    start_dt, end_dt = st.date_input(
        "选择统计日期区间",
        value=(min_db_dt.date(), max_db_dt.date()),
        min_value=min_db_dt.date(),
        max_value=max_db_dt.date()
    )

# 分段加载全量数据
with st.spinner("正在分段加载全部历史订单统计，请稍等..."):
    df_raw = get_all_week_data(start_dt, end_dt)

if df_raw.empty:
    st.warning("所选时间段无订单数据")
else:
    df_raw["stat_week"] = pd.to_datetime(df_raw["stat_week"])
    df_below = df_raw[df_raw["weight_type"] == "below500"].sort_values("stat_week")
    df_over = df_raw[df_raw["weight_type"] == "over500"].sort_values("stat_week")

    avg_below = df_below["total_orders"].mean() if len(df_below) > 0 else 0
    avg_over = df_over["total_orders"].mean() if len(df_over) > 0 else 0

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_below["stat_week"],
        y=df_below["total_orders"],
        name="500g以下周销量",
        mode="lines+markers",
        line_color="#2E86AB",
        marker_size=6
    ))
    fig.add_hline(
        y=avg_below,
        line_dash="dash",
        line_color="red",
        annotation_text=f"500g以下整体周均值：{round(avg_below,1)}",
        annotation_position="top left"
    )
    fig.add_trace(go.Scatter(
        x=df_over["stat_week"],
        y=df_over["total_orders"],
        name="500g以上周销量",
        mode="lines+markers",
        line_color="#A23B72",
        marker_size=6
    ))
    fig.add_hline(
        y=avg_over,
        line_dash="dash",
        line_color="red",
        annotation_text=f"500g以上整体周均值：{round(avg_over,1)}",
        annotation_position="top right"
    )
    fig.update_layout(
        title="500g以下 / 500g以上 每周销量波动曲线",
        xaxis_title="周起始日期（周一）",
        yaxis_title="周销量（工单订单数）",
        height=700,
        xaxis={"tickangle": -45, "automargin": True},
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("当前筛选区间汇总统计")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("500g以下总工单", value=df_below["total_orders"].sum())
        st.metric("500g以下总销售额", value=round(df_below["total_sales"].sum(), 2))
        st.metric("500g以下周均销量", round(avg_below, 1))
    with col2:
        st.metric("500g以上总工单", value=df_over["total_orders"].sum())
        st.metric("500g以上总销售额", value=round(df_over["total_sales"].sum(), 2))
        st.metric("500g以上周均销量", round(avg_over, 1))

    st.download_button(
        label="导出当前筛选周统计数据CSV",
        data=df_raw.to_csv(index=False, encoding="utf-8-sig"),
        file_name="跨境周销量统计_筛选数据.csv",
        mime="text/csv"
    )
