import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# --- BẮT ĐẦU: TÍCH HỢP AI PHẢN HỒI CẢM XÚC ---
lenh_dinh_huong = """
Bạn là chatbot OpenUp, người bạn đồng hành tâm lý thân thiết của học sinh THCS. 
Nhiệm vụ đặc biệt: Khi phát hiện học sinh sử dụng các từ khóa cảm xúc như "Buồn", "Căng thẳng", "Áp lực", "Cô đơn", "Tức giận" hoặc than mệt mỏi, bạn BẮT BUỘC phải đưa ra câu trả lời gồm đủ 4 ý sau:
1. Lời động viên tích cực, thấu cảm.
2. Gợi ý một cách kiểm soát cảm xúc ngay lúc đó (hít thở sâu, uống nước...).
3. Khuyến khích học sinh tìm kiếm sự chia sẻ từ gia đình (bố mẹ, anh chị em).
4. Đề xuất một hoạt động thư giãn (viết nhật ký cảm xúc, nghe nhạc, vẽ tranh...).
Văn phong: Ấm áp, nhẹ nhàng, giống như một chuyên gia tư vấn tâm lý học đường. Xưng là "OpenUp" hoặc "mình" và gọi người dùng là "bạn".
"""

model = genai.GenerativeModel(
    "gemini-3.5-flash",
    system_instruction=lenh_dinh_huong
)
# --- KẾT THÚC: TÍCH HỢP AI PHẢN HỒI CẢM XÚC ---

# 2. GIAO DIỆN TRANG WEB
st.set_page_config(page_title="OpenUp", page_icon="💙")
# --- NÂNG CẤP 1 & 2: TẠO THANH BÊN (SIDEBAR) VÀ NÚT XÓA LỊCH SỬ ---
with st.sidebar:
    st.title("Về OpenUp")
    st.write("Không gian an toàn để các em học sinh chia sẻ cảm xúc và tìm cách kết nối với gia đình.")
    
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.messages = []
        st.success("Đã làm mới cuộc hội thoại!")
# --- BẮT ĐẦU: GIAO DIỆN THƯ VIỆN TÌNH HUỐNG ---
with st.sidebar:
    st.header("📚 Thư viện tình huống")
    st.write("Tham khảo các mẫu giao tiếp gia đình tích cực do nhóm nghiên cứu biên soạn:")
    
    # Danh sách 5 nhóm tình huống
    tinh_huong = st.selectbox(
        "Chọn một tình huống:",
        ("Chọn để xem...", 
         "Áp lực học tập và điểm số", 
         "Mâu thuẫn sử dụng điện thoại, mạng xã hội", 
         "Thiếu thời gian trò chuyện với gia đình",
         "Khó khăn trong việc chia sẻ cảm xúc",
         "Khác biệt quan điểm giữa cha mẹ và con cái")
    )
    
    # 1. Tình huống: Áp lực học tập
    if tinh_huong == "Áp lực học tập và điểm số":
        st.info(
            "**1. Mô tả:** Cha mẹ thường xuyên nhắc nhở việc học khiến con cảm thấy áp lực.\n\n"
            "**2. Phân tích:** Học sinh thấy mệt mỏi, trong khi cha mẹ xuất phát từ sự lo lắng cho tương lai của con.\n\n"
            "**3. Gợi ý:** Ghi nhận sự quan tâm của cha mẹ, đồng thời nhẹ nhàng bày tỏ nhu cầu được động viên.\n\n"
            "**4. Mẫu câu:**\n"
            "- *'Con biết ba mẹ lo cho mình, nhưng con cũng cần được động viên thay vì chỉ bị nhắc nhở.'*\n"
            "- *'Ba mẹ có thể hỏi con hôm nay ở trường như thế nào trước khi nói về điểm số được không ạ?'*"
        )
        
    # 2. Tình huống: Sử dụng điện thoại
    elif tinh_huong == "Mâu thuẫn sử dụng điện thoại, mạng xã hội":
         st.info(
            "**1. Mô tả:** Cha mẹ cấm đoán hoặc tịch thu điện thoại vì cho rằng con dùng quá nhiều.\n\n"
            "**2. Phân tích:** Cha mẹ lo con xao nhãng học tập, con thì cảm thấy mất không gian riêng tư và bị kiểm soát.\n\n"
            "**3. Gợi ý:** Chủ động đề xuất quy tắc sử dụng rõ ràng để cha mẹ yên tâm.\n\n"
            "**4. Mẫu câu:**\n"
            "- *'Con hiểu ba mẹ lo con dùng điện thoại nhiều sẽ ảnh hưởng mắt và việc học. Con hứa sẽ chỉ dùng 1 tiếng sau khi làm xong bài tập ạ.'*\n"
            "- *'Con đang dùng điện thoại để trao đổi bài tập nhóm, ba mẹ cho con xin thêm 15 phút nữa nhé!'*"
        )
         
    # 3. Tình huống: Thiếu thời gian
    elif tinh_huong == "Thiếu thời gian trò chuyện với gia đình":
         st.info(
            "**1. Mô tả:** Cha mẹ quá bận rộn với công việc, ít có thời gian hỏi han, trò chuyện cùng con.\n\n"
            "**2. Phân tích:** Con cảm thấy lạc lõng, thiếu sự quan tâm. Cha mẹ thì mệt mỏi vì áp lực tài chính và công việc.\n\n"
            "**3. Gợi ý:** Bày tỏ mong muốn được dành thời gian cùng cha mẹ một cách chân thành, chọn thời điểm cha mẹ đã nghỉ ngơi.\n\n"
            "**4. Mẫu câu:**\n"
            "- *'Bố mẹ dạo này bận rộn quá, cuối tuần này nhà mình dành chút thời gian ăn tối và nói chuyện cùng nhau được không ạ?'*\n"
            "- *'Con có chuyện ở trường muốn kể, khi nào ba mẹ làm việc xong cho con nói chuyện một lát nhé.'*"
        )
         
    # 4. Tình huống: Khó khăn chia sẻ
    elif tinh_huong == "Khó khăn trong việc chia sẻ cảm xúc":
         st.info(
            "**1. Mô tả:** Con gặp chuyện buồn nhưng không biết cách mở lời với cha mẹ vì sợ bị đánh giá hoặc la mắng.\n\n"
            "**2. Phân tích:** Tuổi dậy thì nhạy cảm, sợ tổn thương. Cha mẹ đôi khi phản ứng nhanh, chưa kịp lắng nghe đã vội trách móc.\n\n"
            "**3. Gợi ý:** Bắt đầu bằng việc xin phép được lắng nghe mà không phán xét.\n\n"
            "**4. Mẫu câu:**\n"
            "- *'Con đang có chuyện buồn và cảm thấy hơi rối. Bố mẹ có thể chỉ nghe con nói một chút mà chưa cần khuyên gì con được không ạ?'*\n"
            "- *'Con sợ nói ra ba mẹ sẽ giận, ba mẹ hứa nghe con nói hết rồi mới nhận xét nhé.'*"
        )
         
    # 5. Tình huống: Khác biệt quan điểm
    elif tinh_huong == "Khác biệt quan điểm giữa cha mẹ và con cái":
         st.info(
            "**1. Mô tả:** Cha mẹ và con cái có suy nghĩ khác nhau về sở thích, phong cách hoặc định hướng.\n\n"
            "**2. Phân tích:** Khoảng cách thế hệ dẫn đến sự khác biệt giá trị quan. Cha mẹ muốn an toàn, con muốn thể hiện cá tính.\n\n"
            "**3. Gợi ý:** Thể hiện sự tôn trọng với góc nhìn của cha mẹ trước khi trình bày suy nghĩ của riêng mình.\n\n"
            "**4. Mẫu câu:**\n"
            "- *'Con hiểu góc nhìn và sự lo lắng của bố mẹ. Nhưng bố mẹ có thể cho con cơ hội được trình bày suy nghĩ của riêng con về việc này không ạ?'*\n"
            "- *'Con biết cách này khác với ý ba mẹ, nhưng con đã tìm hiểu kỹ và muốn thử sức, ba mẹ ủng hộ con nhé.'*"
        )
# --- KẾT THÚC: GIAO DIỆN THƯ VIỆN TÌNH HUỐNG ---

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

    # 1. Bật tính năng stream=True để AI trả về từng cụm từ
    response = model.generate_content(full_prompt, stream=True)
    
    # 2. Yêu cầu giao diện gõ từng chữ ra màn hình
    with st.chat_message("assistant"):
        bot_reply = st.write_stream(chunk.text for chunk in response)
        
    # 3. Lưu lại toàn bộ câu trả lời vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
