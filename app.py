import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 2. GIAO DIỆN TRANG WEB
st.set_page_config(page_title="OpenUp", page_icon="💙")
# --- NÂNG CẤP 1 & 2: TẠO THANH BÊN (SIDEBAR) VÀ NÚT XÓA LỊCH SỬ ---
with st.sidebar:
    st.title("Về OpenUp")
    st.write("Không gian an toàn để các em học sinh chia sẻ cảm xúc và tìm cách kết nối với gia đình.")
    
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.messages = []
        st.success("Đã làm mới cuộc hội thoại!")
st.title("💙 OpenUp")
st.subheader("Mở lòng kết nối - Mở lối yêu thương")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Hãy chia sẻ cảm xúc của bạn hôm nay...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    full_prompt = f"""
    Bạn là chuyên gia tâm lí học đường tên OpenUp.
    Quy tắc phản hồi:
    - Luôn nhẹ nhàng, tích cực, tuyệt đối không phán xét.
    - Dùng từ ngữ gần gũi với học sinh cấp 2 (THCS).
    - Khuyên các em cách mở lời để trò chuyện với cha mẹ.
    - Lời khuyên phải ngắn gọn, dễ hiểu, mang tính an ủi.
    
    Người dùng vừa nói: {prompt}
    """

    response = model.generate_content(full_prompt)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
