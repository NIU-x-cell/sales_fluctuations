# 【强制第一行】页面基础配置，必须所有import之前！
import streamlit as st
st.set_page_config(page_title="Ozon跨境周销量波动看板", layout="wide")

import pandas as pd
import pymysql
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# 导入统一完整配置，无需本地拼接ssl/超时
from config import DB_FULL_CONFIG, TABLE_WEEK_STAT

# 缓存周表数据，减少重复查询数据库
@st.cache_data(ttl=1800, show_spinner="加载周统计数据...")
def load_week_data():
    try:
        conn = pymysql.connect(**DB_FULL_CONFIG)
        df = pd.read_sql(f"SELECT stat_week, weight_type, total_orders, total_sales FROM {TABLE_WEEK_STAT} ORDER BY stat_week;", conn)
        conn.close()
        # 日期容错清洗
        df["stat_week"] = pd.to_datetime(df["stat_week"], errors="coerce")
        df = df.dropna(subset=["stat_week"])
        return df
    except Exception as e:
        st.error(f"数据库连接失败：{str(e)}")
        return pd.DataFrame()

st.title("跨境Ozon平台 500g上下周销量波动分析看板")
st.divider()

# 读取预聚合周表（带缓存）
df_all = load_week_data()
if df_all.empty:
    st.error("周统计表无数据，请先运行clean_data.py生成统计数据")
else:
    min_date = df_all["stat_week"].min()
    max_date = df_all["stat_week"].max()

    # 侧边时间筛选
    with st.sidebar:
        st.header("时间筛选器")
        start_dt, end_dt = st.date_input(
            "选择统计日期区间",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    # 筛选区间数据
    start_pd = pd.to_datetime(start_dt)
    end_pd = pd.to_datetime(end_dt)
    df_filter = df_all[(df_all["stat_week"] >= start_pd) & (df_all["stat_week"] <= end_pd)]

    # 拆分两类重量
    df_below = df_filter[df_filter["weight_type"] == "below500"].sort_values("stat_week")
    df_over = df_filter[df_filter["weight_type"] == "over500"].sort_values("stat_week")

    # 动态计算筛选区间内真实周均值
    avg_below = df_below["total_orders"].sum() / len(df_below) if len(df_below) > 0 else 0
    avg_over = df_over["total_orders"].sum() / len(df_over) if len(df_over) > 0 else 0

    # 创建2行1列独立画布，垂直拆分
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            "500g以下 每周工单销量趋势",
            "500g以上 每周工单销量趋势"
        ),
        vertical_spacing=0.18
    )

    # 上图：轻货 below500
    if not df_below.empty:
        fig.add_trace(go.Scatter(
            x=df_below["stat_week"],
            y=df_below["total_orders"],
            name="500g以下周销量",
            mode="lines+markers",
            line_color="#2E86AB",
            marker_size=6,
            hovertemplate="统计周：%{x}<br>订单总数：%{y:,}<extra></extra>"
        ), row=1, col=1)
        fig.add_hline(
            y=avg_below,
            line_dash="dash",
            line_color="red",
            annotation_text=f"筛选区间周均值：{round(avg_below,1)}",
            annotation_position="top left",
            row=1, col=1
        )
        fig.update_yaxes(title_text="周工单订单数", row=1, col=1)

    # 下图：重货 over500
    if not df_over.empty:
        fig.add_trace(go.Scatter(
            x=df_over["stat_week"],
            y=df_over["total_orders"],
            name="500g以上周销量",
            mode="lines+markers",
            line_color="#A23B72",
            marker_size=6,
            hovertemplate="统计周：%{x}<br>订单总数：%{y:,}<extra></extra>"
        ), row=2, col=1)
        fig.add_hline(
            y=avg_over,
            line_dash="dash",
            line_color="red",
            annotation_text=f"筛选区间周均值：{round(avg_over,1)}",
            annotation_position="top left",
            row=2, col=1
        )
        fig.update_yaxes(title_text="周工单订单数", row=2, col=1)

    # 统一全局布局配置
    fig.update_layout(
        height=800,
        xaxis={"tickangle": -45, "nticks": 35, "automargin": True},
        xaxis2={"tickangle": -45, "nticks": 35, "automargin": True},
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_white",
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # 汇总指标
    st.divider()
    st.subheader("当前筛选区间汇总统计")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("500g以下总工单", value=df_below["total_orders"].sum())
        st.metric("500g以下总销售额", value=round(df_below["total_sales"].sum(), 2))
        st.metric("500g以下筛选区间周均销量", round(avg_below, 1))
    with col2:
        st.metric("500g以上总工单", value=df_over["total_orders"].sum())
        st.metric("500g以上总销售额", value=round(df_over["total_sales"].sum(), 2))
        st.metric("500g以上筛选区间周均销量", round(avg_over, 1))

    # 导出CSV
    st.download_button(
        label="导出当前筛选周统计数据CSV",
        data=df_filter.to_csv(index=False, encoding="utf-8-sig"),
        file_name="跨境周销量统计_筛选数据.csv",
        mime="text/csv"
    )
