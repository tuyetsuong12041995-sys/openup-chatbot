import streamlit as st
import google.generativeai as genai

from openup_logic import (
    KENH_HO_TRO, LOI_DU_PHONG, LOI_QUA_TAI, NGOAI_CHU_DE, LOI_QUA_DAI, GIOI_HAN_KY_TU, THU_VIEN, TU_DIEN,
    xay_dung_chi_dan, xay_dung_lich_su, phat_hien_nguy_co, LocCo, cat_den_cau_cuoi,
)

DUNG_OPENAI = "OPENAI_API_KEY" in st.secrets

if DUNG_OPENAI:
    from openai import OpenAI
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    TEN_MO_HINH = st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TEN_MO_HINH = "gemini-3.5-flash"
    model = genai.GenerativeModel(
        TEN_MO_HINH,
        system_instruction=xay_dung_chi_dan(),
        generation_config={"temperature": 0.6},
    )


def tin_nhan_openai(lich_su, prompt):
    ds = [{"role": "system", "content": xay_dung_chi_dan()}]
    for m in lich_su:
        ds.append({"role": "user" if m["role"] == "user" else "assistant", "content": m["parts"][0]})
    ds.append({"role": "user", "content": prompt})
    return ds

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

if prompt and len(prompt) > GIOI_HAN_KY_TU:
    st.warning(LOI_QUA_DAI)
    prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    nguy_co = phat_hien_nguy_co(prompt)
    lich_su = xay_dung_lich_su(st.session_state.messages)

    def hoi_dap(stream, cho=None):
        loc = LocCo()
        van_ban = ""
        loi = False
        chi_tiet = []
        het_han_muc = False
        try:
            if DUNG_OPENAI:
                tn = tin_nhan_openai(lich_su, prompt)
                if stream:
                    for chunk in client.chat.completions.create(
                        model=TEN_MO_HINH, messages=tn, temperature=0.6, stream=True
                    ):
                        vb = chunk.choices[0].delta.content or "" if chunk.choices else ""
                        out = loc.day(vb)
                        if out:
                            van_ban += out
                            if cho is not None:
                                cho.write(van_ban + " ▌")
                else:
                    r = client.chat.completions.create(model=TEN_MO_HINH, messages=tn, temperature=0.6)
                    van_ban += loc.day(r.choices[0].message.content or "")
                van_ban += loc.ket()
                return van_ban, loi, loc.co, chi_tiet, het_han_muc, loc.ngoai
            chat = model.start_chat(history=lich_su)
            if stream:
                for chunk in chat.send_message(prompt, stream=True):
                    try:
                        vb = chunk.text
                    except ValueError as e:
                        vb = ""
                        chi_tiet.append("ValueError: " + str(e)[:200])
                        try:
                            chi_tiet.append("feedback: " + str(chunk.prompt_feedback)[:200])
                        except Exception:
                            pass
                    out = loc.day(vb)
                    if out:
                        van_ban += out
                        if cho is not None:
                            cho.write(van_ban + " ▌")
            else:
                van_ban += loc.day(chat.send_message(prompt).text)
            van_ban += loc.ket()
        except Exception as e:
            print("OPENUP_LOI:", repr(e))
            chi_tiet.append("Exception: " + repr(e)[:300])
            het_han_muc = any(k in repr(e) for k in ("ResourceExhausted", "RateLimit", "429"))
            van_ban += loc.ket()
            loi = True
        if not van_ban.strip():
            print("OPENUP_RONG:", chi_tiet)
        return van_ban, loi, loc.co, chi_tiet, het_han_muc, loc.ngoai

    with st.chat_message("assistant"):
        cho = st.empty()
        bot_reply, loi, co, chi_tiet, qua_tai, ngoai = hoi_dap(True, cho)
        if not qua_tai and not ngoai and (loi or not bot_reply.strip()) and len(bot_reply.strip()) < 30:
            bot_reply, loi, co2, ct2, qua_tai, ngoai = hoi_dap(False)
            co = co or co2
            chi_tiet = chi_tiet + ct2
        if ngoai:
            bot_reply = NGOAI_CHU_DE
        elif loi and bot_reply.strip():
            bot_reply = cat_den_cau_cuoi(bot_reply)
        if not bot_reply.strip():
            bot_reply = LOI_QUA_TAI if qua_tai else LOI_DU_PHONG
        cho.write(bot_reply)
        try:
            if st.secrets.get("DEBUG") and chi_tiet:
                st.caption("Chi tiết lỗi (chỉ hiện khi bật DEBUG): " + " | ".join(chi_tiet))
        except Exception:
            pass
        if co:
            nguy_co = True

        if nguy_co:
            st.warning(KENH_HO_TRO)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply, "nguy_co": nguy_co}
    )
