import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================================
# FinSave 3.0 | Dark Finance + Neon Green
# =========================================================
st.set_page_config(
    page_title="FinSave 3.0 | Savings Dashboard",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Theme / responsive styling ----------
st.markdown("""
<style>
:root {
    --bg: #08111F;
    --panel: #101C2D;
    --panel-2: #142238;
    --line: #26364C;
    --muted: #9AAAC0;
    --text: #F3F7FC;
    --neon: #39F5A2;
    --neon-soft: rgba(57,245,162,.12);
}
.stApp { background: var(--bg); color: var(--text); }
[data-testid="stHeader"] { background: rgba(8,17,31,.88); }
.block-container { max-width: 1250px; padding-top: 1.6rem; padding-bottom: 2.5rem; }
h1, h2, h3 { color: var(--text) !important; letter-spacing: -.02em; }
p, label, .stMarkdown, [data-testid="stCaptionContainer"] { color: var(--text); }
.hero {
    background: radial-gradient(circle at 90% 10%, rgba(57,245,162,.18), transparent 28%),
                linear-gradient(135deg, #12223A 0%, #0C1727 65%, #102D2B 100%);
    border: 1px solid #263B4F;
    border-radius: 24px;
    padding: 28px 30px;
    margin-bottom: 22px;
}
.hero-kicker { color: var(--neon); font-size: .76rem; font-weight: 800; letter-spacing: .18em; }
.hero-title { color: #F5FAFF; font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 850; margin: 8px 0 5px; }
.hero-sub { color: #B8C7D9; font-size: 1rem; margin: 0; }
.pill {
    display: inline-block; background: var(--neon-soft); color: var(--neon);
    border: 1px solid rgba(57,245,162,.35); border-radius: 999px;
    padding: 5px 10px; font-size: .75rem; font-weight: 700;
}
.section-label { color: var(--neon); font-size: .76rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin: 8px 0 12px; }
div[data-testid="stMetric"] {
    background: linear-gradient(160deg, #142238, #0F1A2A);
    border: 1px solid #26364C; border-radius: 18px; padding: 17px 18px;
}
div[data-testid="stMetricLabel"] { color: #A9B8CB; }
div[data-testid="stMetricValue"] { color: var(--neon); font-weight: 800; font-size: clamp(1.15rem, 2vw, 1.8rem); }
div[data-testid="stMetricDelta"] { color: var(--neon); }
div[data-testid="stTabs"] button { color: #B7C6D8; font-weight: 700; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: var(--neon); }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--neon); }
div.stButton > button[kind="primary"] {
    background: var(--neon); color: #07131D; border: 0; border-radius: 12px;
    font-weight: 800; min-height: 44px;
}
div.stButton > button[kind="primary"]:hover { background: #78FFC1; color: #07131D; }
div.stDownloadButton > button {
    border: 1px solid rgba(57,245,162,.6); color: var(--neon);
    background: rgba(57,245,162,.06); border-radius: 12px; font-weight: 700;
}
div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    border: 1px solid var(--line); border-radius: 12px; overflow: hidden;
}
div[data-baseweb="input"] input, div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] textarea {
    background: #0B1727; color: var(--text); border-color: #33465F;
}
hr { border-color: var(--line); }
.small-note { color: var(--muted); font-size: .82rem; line-height: 1.55; }
@media (max-width: 700px) {
    .block-container { padding: 1rem .85rem 2rem; }
    .hero { padding: 20px 18px; border-radius: 18px; }
    .hero-title { font-size: 1.8rem; }
    div[data-testid="stMetric"] { padding: 12px; }
    div[data-testid="stMetricValue"] { font-size: 1.15rem; }
    [data-testid="stHorizontalBlock"] { gap: .55rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def money(value):
    return f"{value:,.0f} ₫".replace(",", ".")

def safe_float(value, default=0.0):
    try:
        n = float(value)
        return n if pd.notna(n) else default
    except (TypeError, ValueError):
        return default

def calc_interest(principal, annual_rate_pct, months, method):
    """Illustrative estimate; monthly compounding assumes monthly capitalization."""
    p = max(0.0, safe_float(principal))
    r = max(0.0, safe_float(annual_rate_pct)) / 100
    n = max(0, int(months))
    if method == "Lãi kép hàng tháng":
        total = p * (1 + r / 12) ** n
    else:
        total = p * (1 + r * n / 12)
    return max(0.0, total - p), total

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="hero-kicker">PERSONAL FINANCE • VERSION 3.0</div>
  <div class="hero-title">FinSave <span style="color:#39F5A2">●</span></div>
  <p class="hero-sub">Lập kế hoạch tiết kiệm. So sánh kịch bản. Hiểu rõ dòng tiền của bạn.</p>
  <div style="margin-top:16px"><span class="pill">DARK FINANCE / NEON GREEN</span></div>
</div>
""", unsafe_allow_html=True)

# ---------- Main inputs ----------
st.markdown('<div class="section-label">01 / Thiết lập khoản tiết kiệm</div>', unsafe_allow_html=True)
with st.container(border=True):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        principal = st.number_input(
            "Số tiền gửi ban đầu (VNĐ)", min_value=0, max_value=10**15,
            value=100_000_000, step=1_000_000, format="%d",
            help="Nhập số tiền gốc dự kiến gửi."
        )
        annual_rate = st.number_input(
            "Lãi suất (%/năm)", min_value=0.0, max_value=100.0,
            value=5.0, step=0.1, format="%.2f"
        )
    with col2:
        months = st.select_slider(
            "Kỳ hạn", options=[1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 60],
            value=12, format_func=lambda n: f"{n} tháng"
        )
        method = st.selectbox(
            "Phương pháp mô phỏng",
            ["Lãi đơn", "Lãi kép hàng tháng"],
            help="Lãi kép giả định lãi được nhập gốc mỗi tháng."
        )
    st.caption("Mô hình giả định lãi suất cố định trong suốt kỳ hạn và chưa tính thuế, phí hoặc quy tắc riêng của ngân hàng.")

interest, total = calc_interest(principal, annual_rate, months, method)
return_pct = (interest / principal * 100) if principal else 0.0

# Save current scenario once per explicit click
save_col, reset_col, _ = st.columns([1.2, 1.2, 3])
with save_col:
    save_clicked = st.button("＋ Lưu kịch bản", type="primary", use_container_width=True)
with reset_col:
    if st.button("Xóa lịch sử", use_container_width=True):
        st.session_state.history = []
        st.rerun()

if save_clicked:
    st.session_state.history.insert(0, {
        "Thời điểm": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Tiền gốc (VNĐ)": int(principal),
        "Lãi suất (%/năm)": float(annual_rate),
        "Kỳ hạn (tháng)": int(months),
        "Phương pháp": method,
        "Tiền lãi (VNĐ)": round(interest),
        "Tổng đáo hạn (VNĐ)": round(total),
    })
    st.session_state.history = st.session_state.history[:50]
    st.success("Đã lưu kịch bản vào lịch sử của phiên hiện tại.")

# ---------- KPI ----------
st.markdown('<div class="section-label">02 / Tổng quan tài chính</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4, gap="medium")
k1.metric("Tiền gốc", money(principal))
k2.metric("Lãi dự kiến", money(interest))
k3.metric("Tổng đáo hạn", money(total))
k4.metric("Sinh lời trên gốc", f"{return_pct:.2f}%")

# ---------- Projection data ----------
rows = []
for m in range(months + 1):
    if method == "Lãi kép hàng tháng":
        balance = principal * (1 + annual_rate / 100 / 12) ** m
    else:
        balance = principal * (1 + (annual_rate / 100) * m / 12)
    rows.append({
        "Tháng": m,
        "Tiền gốc (VNĐ)": principal,
        "Tiền lãi tích lũy (VNĐ)": balance - principal,
        "Tổng giá trị (VNĐ)": balance,
    })
projection = pd.DataFrame(rows)

# ---------- Tabs ----------
tab_chart, tab_compare, tab_history, tab_method = st.tabs([
    "📈 Biểu đồ", "🏦 So sánh ngân hàng", "🕘 Lịch sử", "ⓘ Cách tính"
])

with tab_chart:
    st.markdown("### Tăng trưởng khoản tiết kiệm")
    chart_col, stats_col = st.columns([1.7, 1], gap="large")
    with chart_col:
        long_df = projection.melt(
            id_vars=["Tháng"],
            value_vars=["Tiền gốc (VNĐ)", "Tiền lãi tích lũy (VNĐ)"],
            var_name="Thành phần", value_name="Số tiền (VNĐ)"
        )
        fig = px.area(
            long_df, x="Tháng", y="Số tiền (VNĐ)", color="Thành phần",
            color_discrete_map={
                "Tiền gốc (VNĐ)": "#263B55",
                "Tiền lãi tích lũy (VNĐ)": "#39F5A2",
            },
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#DCE7F5", legend_title_text="",
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis_title="Tháng", yaxis_title="Giá trị (VNĐ)",
            hovermode="x unified",
        )
        fig.update_xaxes(gridcolor="#23334A")
        fig.update_yaxes(gridcolor="#23334A", tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)
    with stats_col:
        st.markdown("#### Chỉ số kịch bản")
        st.metric("Kỳ hạn", f"{months} tháng")
        st.metric("Lãi suất năm", f"{annual_rate:.2f}%")
        st.metric("Tiền lãi trung bình/tháng*", money(interest / months if months else 0))
        st.caption("*Là mức bình quân tham khảo, không nhất thiết là khoản lãi ngân hàng trả hàng tháng.")
    st.markdown("#### Bảng dự phóng theo tháng")
    display_projection = projection.copy()
    for col in ["Tiền gốc (VNĐ)", "Tiền lãi tích lũy (VNĐ)", "Tổng giá trị (VNĐ)"]:
        display_projection[col] = display_projection[col].round(0).astype("int64")
    st.dataframe(display_projection, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇ Tải bảng dự phóng CSV",
        data=display_projection.to_csv(index=False).encode("utf-8-sig"),
        file_name="finsave_du_phong.csv",
        mime="text/csv",
    )

with tab_compare:
    st.markdown("### So sánh lãi suất theo cùng một khoản tiền")
    st.markdown(
        '<p class="small-note">Nhập lãi suất tham khảo mà bạn tự kiểm tra từ nguồn chính thức của ngân hàng. '
        'Bảng mặc định chỉ là dữ liệu minh họa, không phải lãi suất hiện hành.</p>',
        unsafe_allow_html=True
    )
    default_rates = pd.DataFrame({
        "Ngân hàng / phương án": ["Phương án A", "Phương án B", "Phương án C"],
        "Lãi suất (%/năm)": [4.5, 5.0, 5.2],
        "Ghi chú nguồn / ngày kiểm tra": [
            "Ví dụ - cần xác minh",
            "Ví dụ - cần xác minh",
            "Ví dụ - cần xác minh",
        ],
    })
    edited_rates = st.data_editor(
        default_rates,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Ngân hàng / phương án": st.column_config.TextColumn(required=True),
            "Lãi suất (%/năm)": st.column_config.NumberColumn(
                min_value=0.0, max_value=100.0, step=0.1, format="%.2f%%", required=True
            ),
            "Ghi chú nguồn / ngày kiểm tra": st.column_config.TextColumn(),
        },
        key="bank_rate_editor",
    )
    comparison_rows = []
    for _, row in edited_rates.iterrows():
        name = str(row.get("Ngân hàng / phương án", "")).strip()
        rate_value = safe_float(row.get("Lãi suất (%/năm)", 0))
        if not name:
            continue
        comp_interest, comp_total = calc_interest(principal, rate_value, months, method)
        comparison_rows.append({
            "Ngân hàng / phương án": name,
            "Lãi suất (%/năm)": rate_value,
            "Tiền lãi dự kiến (VNĐ)": round(comp_interest),
            "Tổng đáo hạn (VNĐ)": round(comp_total),
            "Ghi chú nguồn / ngày kiểm tra": str(row.get("Ghi chú nguồn / ngày kiểm tra", "")),
        })
    if comparison_rows:
        comparison_df = pd.DataFrame(comparison_rows).sort_values(
            "Tổng đáo hạn (VNĐ)", ascending=False
        ).reset_index(drop=True)
        best = comparison_df.iloc[0]
        st.success(
            f"Phương án có kết quả cao nhất trong bảng hiện tại: "
            f"{best['Ngân hàng / phương án']} · {money(best['Tổng đáo hạn (VNĐ)'])}. "
            "Đây chỉ là so sánh theo lãi suất bạn nhập."
        )
        st.dataframe(
            comparison_df.style.format({
                "Lãi suất (%/năm)": "{:.2f}%",
                "Tiền lãi dự kiến (VNĐ)": "{:,.0f}",
                "Tổng đáo hạn (VNĐ)": "{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "⬇ Tải bảng so sánh CSV",
            data=comparison_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="finsave_so_sanh_lai_suat.csv",
            mime="text/csv",
        )
    else:
        st.info("Thêm ít nhất một phương án có tên để xem kết quả so sánh.")

with tab_history:
    st.markdown("### Lịch sử kịch bản trong phiên")
    st.caption("Lịch sử này được lưu tạm trong session của ứng dụng. Tải lại phiên hoặc khởi động lại có thể làm mất dữ liệu.")
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Tải lịch sử CSV",
            data=history_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="finsave_lich_su.csv",
            mime="text/csv",
        )
    else:
        st.info("Chưa có kịch bản nào được lưu. Điều chỉnh thông số ở phía trên rồi nhấn “＋ Lưu kịch bản”.")

with tab_method:
    st.markdown("### Công thức và giả định")
    st.markdown("**Lãi đơn**")
    st.latex(r"I = P \times r \times \frac{n}{12}")
    st.markdown("**Lãi kép hàng tháng**")
    st.latex(r"A = P\left(1+\frac{r}{12}\right)^n")
    st.markdown("""
- `P`: tiền gốc ban đầu.
- `r`: lãi suất năm ở dạng thập phân.
- `n`: số tháng gửi.
- `I`: tiền lãi; `A`: tổng tiền gốc và lãi.
    """)
    st.warning(
        "Kết quả là mô phỏng, không phải báo giá hay cam kết của ngân hàng. "
        "Sản phẩm thực tế có thể tính lãi theo số ngày thực gửi, quy tắc làm tròn, "
        "lịch trả lãi, điều kiện rút trước hạn và quy định riêng."
    )

st.divider()
st.markdown(
    '<p class="small-note">FinSave 3.0 · Công cụ mô phỏng tài chính cá nhân · '
    'Lãi suất trong bảng so sánh do người dùng nhập và cần xác minh trước khi ra quyết định.</p>',
    unsafe_allow_html=True,
)
