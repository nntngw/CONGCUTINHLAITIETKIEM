
import streamlit as st
import pandas as pd

# =========================
# 1. CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="FinSave | Tính lãi tiết kiệm",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. GIAO DIỆN CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FB;
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,251,0.85);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(120deg, #102A43, #176B5B);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 2.2rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: #D8E9E5;
        font-size: 1rem;
    }

    .eyebrow {
        color: #9CE5C8;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border: 1px solid #E5EAF1;
        border-radius: 16px;
        box-shadow: 0 3px 12px rgba(16,42,67,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #176B5B;
        font-weight: 700;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: #176B5B;
        border: none;
        border-radius: 10px;
        min-height: 46px;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #125548;
        color: white;
    }

    .section-title {
        color: #102A43;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 10px 0 15px;
    }

    .note {
        color: #64748B;
        font-size: 0.85rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# 3. HÀM ĐỊNH DẠNG
# =========================
def vnd(value):
    return f"{value:,.0f} ₫"


# =========================
# 4. PHẦN ĐẦU TRANG
# =========================
st.markdown("""
<div class="hero">
    <div class="eyebrow">PERSONAL FINANCE TOOL</div>
    <h1>💎 FinSave</h1>
    <p>
        Công cụ mô phỏng lãi tiết kiệm.
        Lập kế hoạch tài chính rõ ràng, chủ động hơn mỗi ngày.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# 5. THANH ĐIỀU KHIỂN
# =========================
with st.sidebar:
    st.markdown("## ⚙️ Thiết lập")
    st.caption("Điều chỉnh thông số khoản tiết kiệm")

    principal = st.number_input(
        "Số tiền gửi ban đầu (VNĐ)",
        min_value=0,
        max_value=10**15,
        value=100_000_000,
        step=10_000_000
    )

    annual_rate = st.slider(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.1,
        format="%.1f%%"
    )

    months = st.select_slider(
        "Kỳ hạn gửi",
        options=[1, 3, 6, 9, 12, 18, 24, 36, 48, 60],
        value=12,
        format_func=lambda x: f"{x} tháng"
    )

    method = st.selectbox(
        "Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép hàng tháng"
        ]
    )

    st.divider()
    st.caption("FinSave | Phiên bản 2.0")


# =========================
# 6. TÍNH TOÁN
# =========================
rate = annual_rate / 100
monthly_rate = rate / 12

if method == "Lãi đơn":
    interest = principal * rate * months / 12
else:
    interest = principal * (
        (1 + monthly_rate) ** months - 1
    )

total = principal + interest

if principal > 0:
    return_rate = interest / principal * 100
else:
    return_rate = 0


# =========================
# 7. DASHBOARD KẾT QUẢ
# =========================
st.markdown(
    '<div class="section-title">📊 Tổng quan khoản tiết kiệm</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "💰 Tiền gốc",
        vnd(principal)
    )

with c2:
    st.metric(
        "📈 Tiền lãi dự kiến",
        vnd(interest)
    )

with c3:
    st.metric(
        "🎯 Tổng khi đáo hạn",
        vnd(total)
    )

st.caption(
    f"Kỳ hạn {months} tháng · "
    f"Lãi suất {annual_rate:.1f}%/năm · "
    f"Phương pháp: {method}"
)


# =========================
# 8. CÁC TAB NỘI DUNG
# =========================
tab1, tab2, tab3 = st.tabs([
    "📈 Tăng trưởng",
    "🧮 Chi tiết tính lãi",
    "💡 Kiến thức"
])

with tab1:
    st.subheader("Hành trình tăng trưởng tài sản")

    balances = []

    for month in range(months + 1):
        if method == "Lãi đơn":
            balance = principal * (
                1 + rate * month / 12
            )
        else:
            balance = principal * (
                (1 + monthly_rate) ** month
            )

        balances.append({
            "Tháng": month,
            "Giá trị khoản tiết kiệm": balance
        })

    df = pd.DataFrame(balances)

    st.line_chart(
        df,
        x="Tháng",
        y="Giá trị khoản tiết kiệm",
        color="#176B5B"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.metric(
            "Tỷ suất sinh lời dự kiến",
            f"{return_rate:.2f}%"
        )

    with col_b:
        st.metric(
            "Thời gian gửi",
            f"{months} tháng"
        )

with tab2:
    st.subheader("Chi tiết khoản tiết kiệm")

    details = pd.DataFrame({
        "Thông tin": [
            "Tiền gốc ban đầu",
            "Lãi suất năm",
            "Kỳ hạn",
            "Phương pháp tính",
            "Tổng tiền lãi",
            "Tổng tiền đáo hạn"
        ],
        "Giá trị": [
            vnd(principal),
            f"{annual_rate:.2f}%/năm",
            f"{months} tháng",
            method,
            vnd(interest),
            vnd(total)
        ]
    })

    st.dataframe(
        details,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Tải báo cáo CSV",
        data=details.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="bao_cao_tiet_kiem.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("**Công thức sử dụng**")

    if method == "Lãi đơn":
        st.latex(r"I=P \times r \times \frac{n}{12}")
        st.caption(
            "I: tiền lãi, P: tiền gốc, "
            "r: lãi suất năm, n: số tháng."
        )
    else:
        st.latex(r"A=P\left(1+\frac{r}{12}\right)^n")
        st.caption(
            "A: tổng tiền cuối kỳ, P: tiền gốc, "
            "r: lãi suất năm, n: số tháng."
        )

with tab3:
    st.subheader("Hiểu đúng về lãi tiết kiệm")

    with st.expander("Lãi đơn là gì?"):
        st.write(
            "Tiền lãi được tính trên số tiền gốc ban đầu. "
            "Cách tính này phù hợp để mô phỏng khoản gửi "
            "không nhập lãi vào gốc."
        )

    with st.expander("Lãi kép là gì?"):
        st.write(
            "Lãi được cộng vào số dư theo từng kỳ, "
            "sau đó tiếp tục sinh lãi trong các kỳ sau. "
            "Kết quả phụ thuộc vào tần suất nhập lãi."
        )

    with st.expander("Vì sao kết quả có thể khác ngân hàng?"):
        st.write(
            "Ngân hàng có thể tính lãi theo số ngày thực tế, "
            "quy định làm tròn, ngày gửi, ngày đáo hạn, "
            "cách trả lãi và điều kiện tái tục."
        )


# =========================
# 9. CHÂN TRANG
# =========================
st.divider()

st.markdown("""
<div class="note">
    <b>FinSave</b> · Công cụ mô phỏng tài chính cá nhân<br>
    Kết quả chỉ mang tính tham khảo, không phải cam kết
    lãi suất hoặc báo giá chính thức của ngân hàng.
</div>
""", unsafe_allow_html=True)
