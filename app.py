
import streamlit as st

st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Máy tính lãi tiết kiệm")
st.write(
    "Ước tính tiền lãi và tổng số tiền nhận được "
    "khi gửi tiết kiệm."
)

st.divider()

# Nhập thông tin tiền gửi
principal = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

annual_rate = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1
)

months = st.number_input(
    "Kỳ hạn gửi (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

method = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép hàng tháng"
    ]
)

# Tính toán
rate = annual_rate / 100
time_years = months / 12

if method == "Lãi đơn":
    interest = principal * rate * time_years
else:
    interest = principal * (
        (1 + rate / 12) ** months - 1
    )

total = principal + interest

# Hiển thị kết quả
if st.button("🧮 Tính tiền lãi", type="primary"):
    st.subheader("📊 Kết quả dự kiến")

    st.metric(
        "Tiền gốc",
        f"{principal:,.0f} VNĐ"
    )

    st.metric(
        "Tiền lãi",
        f"{interest:,.0f} VNĐ"
    )

    st.metric(
        "Tổng tiền gốc và lãi",
        f"{total:,.0f} VNĐ"
    )

    if months > 0:
        st.caption(
            f"Kỳ hạn: {months} tháng | "
            f"Lãi suất: {annual_rate}%/năm"
        )

    st.info(
        "Kết quả mang tính ước tính, chưa xét thuế, "
        "phí hoặc quy tắc tính lãi riêng của ngân hàng."
    )
