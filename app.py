import streamlit as st
import google.generativeai as genai

from openup_logic import (
    KENH_HO_TRO, LOI_DU_PHONG, THU_VIEN, TU_DIEN,
    xay_dung_chi_dan, xay_dung_lich_su, phat_hien_nguy_co, LocCo,
)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
TEN_MO_HINH = "gemini-3.5-flash"

model = genai.GenerativeModel(
    TEN_MO_HINH,
    system_instruction=xay_dung_chi_dan(),
    generation_config={"temperature": 0.6},
)

st.set_page_config(page_title="OpenUp", page_icon="💙")

with st.sidebar:
    st.title("Về OpenUp")
    st.write("Công cụ gợi ý cách **mở lời với bố mẹ** và hiểu bố mẹ hơn. "
             "OpenUp không phải chuyên gia tâm lý và không thay thế sự giúp đỡ của người lớn.")
    st.caption("Đừng chia sẻ họ tên, địa chỉ, số điện thoại hay thông tin nhận dạng của bạn.")

    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.messages = []
        st.success("Đã làm mới cuộc hội thoại!")

    st.header("📚 Thư viện tình huống")
    st.write("Các mẫu giao tiếp gia đình tích cực do nhóm nghiên cứu biên soạn:")
    tinh_huong = st.selectbox("Chọn một tình huống:", ["Chọn để xem..."] + list(THU_VIEN))
    if tinh_huong in THU_VIEN:
        t = THU_VIEN[tinh_huong]
        mau = "\n".join(f"- *'{c}'*" for c in t["mau_cau"])
        st.info(
            f"**1. Mô tả:** {t['mo_ta']}\n\n**2. Phân tích:** {t['phan_tich']}\n\n"
            f"**3. Gợi ý:** {t['goi_y']}\n\n**4. Mẫu câu:**\n{mau}"
        )

    st.header("📖 Từ điển nhà mình hiểu nhau")
    cau = st.selectbox("Tra một câu nói:", ["Chọn để xem..."] + [m["cau"] for m in TU_DIEN])
    for m in TU_DIEN:
        if m["cau"] == cau:
            st.info(
                f"**{m['ai_noi'].capitalize()} nói:** “{m['cau']}”\n\n"
                f"**Ý thật thường là:** {m['y_that']}\n\n"
                f"**Dễ bị nghe thành:** {m['nghe_thanh']}\n\n"
                f"**Thử nói khác:** “{m['noi_khac']}”"
            )

st.title("💙 OpenUp")
st.subheader("Mở lòng kết nối - Mở lối yêu thương")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("nguy_co"):
            st.warning(KENH_HO_TRO)

prompt = st.chat_input("Bạn đang gặp chuyện gì với bố mẹ? Hãy kể cho OpenUp nghe...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    nguy_co = phat_hien_nguy_co(prompt)
    bot_reply = ""

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=xay_dung_lich_su(st.session_state.messages))
            response = chat.send_message(prompt, stream=True)
            loc = LocCo()

            def luong():
                for chunk in response:
                    try:
                        van_ban = chunk.text
                    except ValueError:
                        van_ban = ""
                    out = loc.day(van_ban)
                    if out:
                        yield out
                out = loc.ket()
                if out:
                    yield out

            bot_reply = st.write_stream(luong())
            if loc.co:
                nguy_co = True
            if not bot_reply.strip():
                bot_reply = LOI_DU_PHONG
                st.write(bot_reply)
                nguy_co = True
        except Exception as loi:
            print("OPENUP_LOI:", repr(loi))

            bot_reply = LOI_DU_PHONG
            st.write(bot_reply)

        if nguy_co:
            st.warning(KENH_HO_TRO)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply, "nguy_co": nguy_co}
    )
