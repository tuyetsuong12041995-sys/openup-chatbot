import re
import unicodedata

KENH_HO_TRO = (
    "💛 **Nếu bạn đang thấy rất tệ hoặc không an toàn, bạn không phải một mình.**\n\n"
    "- Hãy nói ngay với một người lớn bạn tin tưởng (bố mẹ, người thân, thầy cô).\n"
    "- Tổng đài quốc gia bảo vệ trẻ em: **111** (miễn phí, 24/7).\n"
    "- Khẩn cấp: **113** (công an), **115** (cấp cứu).\n"
    "- Thầy/cô tư vấn của trường: **[ĐIỀN TÊN VÀ SỐ ĐIỆN THOẠI]**.\n\n"
    "OpenUp chỉ là công cụ gợi ý cách mở lời, không thay thế chuyên gia tâm lý."
)

LOI_DU_PHONG = (
    "Xin lỗi, OpenUp đang gặp trục trặc nên chưa trả lời được. Bạn thử gửi lại sau một lát nhé. "
    "Nếu bạn cần được giúp ngay, hãy nói với một người lớn bạn tin tưởng."
)

THU_VIEN = {
    "Áp lực học tập và điểm số": {
        "mo_ta": "Cha mẹ thường xuyên nhắc nhở việc học khiến con cảm thấy áp lực.",
        "phan_tich": "Học sinh thấy mệt mỏi, trong khi cha mẹ xuất phát từ sự lo lắng cho tương lai của con.",
        "goi_y": "Ghi nhận sự quan tâm của cha mẹ, đồng thời nhẹ nhàng bày tỏ nhu cầu được động viên.",
        "mau_cau": [
            "Con biết ba mẹ lo cho mình, nhưng con cũng cần được động viên thay vì chỉ bị nhắc nhở.",
            "Ba mẹ có thể hỏi con hôm nay ở trường như thế nào trước khi nói về điểm số được không ạ?",
        ],
    },
    "Mâu thuẫn sử dụng điện thoại, mạng xã hội": {
        "mo_ta": "Cha mẹ cấm đoán hoặc tịch thu điện thoại vì cho rằng con dùng quá nhiều.",
        "phan_tich": "Cha mẹ lo con xao nhãng học tập, con thì cảm thấy mất không gian riêng tư và bị kiểm soát.",
        "goi_y": "Chủ động đề xuất quy tắc sử dụng rõ ràng để cha mẹ yên tâm.",
        "mau_cau": [
            "Con hiểu ba mẹ lo con dùng điện thoại nhiều sẽ ảnh hưởng mắt và việc học. Con hứa sẽ chỉ dùng 1 tiếng sau khi làm xong bài tập ạ.",
            "Con đang dùng điện thoại để trao đổi bài tập nhóm, ba mẹ cho con xin thêm 15 phút nữa nhé!",
        ],
    },
    "Thiếu thời gian trò chuyện với gia đình": {
        "mo_ta": "Cha mẹ quá bận rộn với công việc, ít có thời gian hỏi han, trò chuyện cùng con.",
        "phan_tich": "Con cảm thấy lạc lõng, thiếu sự quan tâm. Cha mẹ thì mệt mỏi vì áp lực tài chính và công việc.",
        "goi_y": "Bày tỏ mong muốn được dành thời gian cùng cha mẹ một cách chân thành, chọn thời điểm cha mẹ đã nghỉ ngơi.",
        "mau_cau": [
            "Bố mẹ dạo này bận rộn quá, cuối tuần này nhà mình dành chút thời gian ăn tối và nói chuyện cùng nhau được không ạ?",
            "Con có chuyện ở trường muốn kể, khi nào ba mẹ làm việc xong cho con nói chuyện một lát nhé.",
        ],
    },
    "Khó khăn trong việc chia sẻ cảm xúc": {
        "mo_ta": "Con gặp chuyện buồn nhưng không biết cách mở lời với cha mẹ vì sợ bị đánh giá hoặc la mắng.",
        "phan_tich": "Tuổi dậy thì nhạy cảm, sợ tổn thương. Cha mẹ đôi khi phản ứng nhanh, chưa kịp lắng nghe đã vội trách móc.",
        "goi_y": "Bắt đầu bằng việc xin phép được lắng nghe mà không phán xét.",
        "mau_cau": [
            "Con đang có chuyện buồn và cảm thấy hơi rối. Bố mẹ có thể chỉ nghe con nói một chút mà chưa cần khuyên gì con được không ạ?",
            "Con sợ nói ra ba mẹ sẽ giận, ba mẹ hứa nghe con nói hết rồi mới nhận xét nhé.",
        ],
    },
    "Khác biệt quan điểm giữa cha mẹ và con cái": {
        "mo_ta": "Cha mẹ và con cái có suy nghĩ khác nhau về sở thích, phong cách hoặc định hướng.",
        "phan_tich": "Khoảng cách thế hệ dẫn đến sự khác biệt giá trị quan. Cha mẹ muốn an toàn, con muốn thể hiện cá tính.",
        "goi_y": "Thể hiện sự tôn trọng với góc nhìn của cha mẹ trước khi trình bày suy nghĩ của riêng mình.",
        "mau_cau": [
            "Con hiểu góc nhìn và sự lo lắng của bố mẹ. Nhưng bố mẹ có thể cho con cơ hội được trình bày suy nghĩ của riêng con về việc này không ạ?",
            "Con biết cách này khác với ý ba mẹ, nhưng con đã tìm hiểu kỹ và muốn thử sức, ba mẹ ủng hộ con nhé.",
        ],
    },
}

TU_DIEN = [
    {"ai_noi": "con", "cau": "Con không sao.",
     "y_that": "Con đang mệt hoặc rối, chưa muốn nói lúc này.",
     "nghe_thanh": "Con đang giấu bố mẹ điều gì đó.",
     "noi_khac": "Con đang hơi mệt, lát nữa con kể bố mẹ nhé."},
    {"ai_noi": "con", "cau": "Con biết rồi.",
     "y_that": "Con đã nghe, nhưng đang thấy bị nhắc quá nhiều.",
     "nghe_thanh": "Con không tôn trọng, nói cho có.",
     "noi_khac": "Con hiểu ý bố mẹ rồi. Cho con tự sắp xếp, tối nay con báo lại nhé."},
    {"ai_noi": "con", "cau": "Bố mẹ không hiểu gì cả.",
     "y_that": "Con muốn được lắng nghe trước khi bị khuyên.",
     "nghe_thanh": "Con đang trách bố mẹ.",
     "noi_khac": "Con muốn bố mẹ nghe con nói hết đã, rồi bố mẹ góp ý sau được không ạ?"},
    {"ai_noi": "con", "cau": "Để con tự lo.",
     "y_that": "Con muốn được tin tưởng và có không gian tự xử lý.",
     "nghe_thanh": "Con không cần bố mẹ.",
     "noi_khac": "Việc này con thử tự làm trước, nếu cần con sẽ nhờ bố mẹ."},
    {"ai_noi": "con", "cau": "Con có làm gì đâu.",
     "y_that": "Con thấy bị trách oan hoặc bị nói quá lên.",
     "nghe_thanh": "Con chối tội.",
     "noi_khac": "Con thấy hơi oan. Bố mẹ cho con giải thích được không ạ?"},
    {"ai_noi": "bố mẹ", "cau": "Sao con lại như vậy?",
     "y_that": "Bố mẹ đang lo và muốn hiểu chuyện gì xảy ra.",
     "nghe_thanh": "Con đang bị trách mắng.",
     "noi_khac": "Chuyện gì khiến con thấy như vậy?"},
    {"ai_noi": "bố mẹ", "cau": "Thôi đi.",
     "y_that": "Bố mẹ đang mệt hoặc đang lo và muốn dừng cuộc nói chuyện căng thẳng.",
     "nghe_thanh": "Ý kiến của con không quan trọng.",
     "noi_khac": "Bố mẹ đang hơi mệt, mình nói tiếp sau nhé."},
    {"ai_noi": "bố mẹ", "cau": "Bố mẹ làm vậy là vì con.",
     "y_that": "Bố mẹ thương và lo cho con.",
     "nghe_thanh": "Con phải mang ơn, không được buồn hay phản đối.",
     "noi_khac": "Bố mẹ lo cho con nên mới nói vậy. Con thấy thế nào?"},
    {"ai_noi": "bố mẹ", "cau": "Nhìn con nhà người ta kìa.",
     "y_that": "Bố mẹ mong con cố gắng hơn nhưng chưa biết cách nói.",
     "nghe_thanh": "Con không bằng ai, bố mẹ thất vọng về con.",
     "noi_khac": "Bố mẹ mong con cố gắng thêm một chút, con thấy mình cần giúp gì không?"},
]

def tu_dien_thanh_van_ban():
    dong = []
    for m in TU_DIEN:
        dong.append(
            f'- {m["ai_noi"].capitalize()} nói: "{m["cau"]}" | Ý thật: {m["y_that"]} | '
            f'Dễ bị nghe thành: {m["nghe_thanh"]} | Có thể nói khác: "{m["noi_khac"]}"'
        )
    return "\n".join(dong)

def thu_vien_thanh_van_ban():
    dong = []
    for ten, t in THU_VIEN.items():
        dong.append(f'- {ten}: {t["goi_y"]} Mẫu: "{t["mau_cau"][0]}"')
    return "\n".join(dong)

CO_NGUY_CO = "[NGUY_CO]"

def xay_dung_chi_dan():
    return f"""Bạn là OpenUp, trợ lý của dự án "Hệ sinh thái OpenUp" do nhóm học sinh nghiên cứu.
Nhiệm vụ DUY NHẤT: giúp học sinh THCS/THPT tìm cách MỞ LỜI với bố mẹ và hiểu bố mẹ hơn.
Bạn KHÔNG phải chuyên gia tâm lý, không chẩn đoán, không điều trị. Xưng "mình", gọi người dùng là "bạn".
Giọng văn: ấm, ngắn gọn, đời thường như một người anh/chị lớn; không giảng đạo lý, không phán xét ai (cả con lẫn bố mẹ).

CÁCH TRẢ LỜI: viết như một tin nhắn tự nhiên của người anh/chị lớn, gồm 2-3 đoạn văn ngắn. Ý cần có theo thứ tự:
- Mở đầu bằng 1 câu đồng cảm với chuyện bạn ấy kể, dùng lời đời thường (ví dụ "Bị điểm thấp rồi còn lo bố mẹ buồn, nghe nặng lòng thật.").
- Rồi đưa 1-2 câu CỤ THỂ để bạn ấy nói với bố mẹ, đặt trong dấu ngoặc kép, xưng hô theo gia đình bạn ấy (chưa biết thì dùng "bố mẹ").
  Câu nói nên ghi nhận bố mẹ lo cho con trước rồi mới nói điều con mong muốn. Gợi ý lúc nói phù hợp (khi bố mẹ đã bình tĩnh)
  và nói ngắn gọn bố mẹ có thể đang lo điều gì.
- Cuối cùng báo trước một tình huống có thể xảy ra (bố mẹ còn giận hoặc gạt đi) và bạn ấy có thể nói gì tiếp.
  Nếu cần biết thêm để gợi ý sát hơn, hỏi tối đa MỘT câu ngắn ở cuối, không hỏi trước khi gợi ý.
Luôn có câu mở lời cụ thể ngay cả khi bạn ấy kể ít.
TUYỆT ĐỐI không ghi tên các phần như "Ghi nhận", "Cách mở lời", "Dự phòng"; không đánh số, không dùng tiêu đề hay gạch đầu dòng.
Không phỏng đoán nguyên nhân khi bạn ấy chưa kể (ví dụ không tự nói "hổng kiến thức", "chưa tập trung"). Chỉ nói những điều chắc chắn.
Tối đa khoảng 130 từ, ngắn gọn, dễ hiểu cho học sinh cấp 2.
Không liệt kê hít thở, uống nước, nghe nhạc, vẽ tranh trừ khi bạn ấy hỏi. Nếu bạn ấy chỉ nói cảm xúc, không nêu chuyện với bố mẹ:
vẫn đồng cảm rồi gợi ý một câu mở lời nhẹ để bắt đầu chia sẻ với bố mẹ.

DỮ LIỆU CỦA DỰ ÁN (ưu tiên dùng khi khớp tình huống, và nói rõ "theo Từ điển OpenUp" hoặc "theo Thư viện tình huống OpenUp"):
Từ điển nhà mình hiểu nhau:
{tu_dien_thanh_van_ban()}

Thư viện tình huống:
{thu_vien_thanh_van_ban()}
Nếu bạn ấy nhắc một câu nói có trong từ điển, hãy giải thích ý thật, cách bố mẹ/con dễ nghe nhầm, và đưa cách nói khác.
Không bịa số liệu, không nói "nghiên cứu cho thấy" khi không có trong dữ liệu trên. Đây là các cách hiểu phổ biến,
không đúng với mọi gia đình; khuyến khích hỏi lại "ý bố mẹ là gì?".

AN TOÀN (ưu tiên cao nhất):
- Nếu bạn ấy nhắc đến ý nghĩ tự làm đau mình, muốn biến mất/không muốn sống, bị đánh đập, xâm hại, hoặc bị đe dọa,
  hãy BẮT ĐẦU câu trả lời bằng đúng dòng {CO_NGUY_CO} (một mình trên dòng đầu), sau đó viết 2-3 câu ấm áp: ghi nhận,
  nói bạn ấy không đơn độc, khuyến khích nói NGAY với một người lớn tin cậy. KHÔNG soạn câu mở lời, KHÔNG tự bịa số điện thoại
  (hệ thống sẽ hiển thị kênh hỗ trợ).
- Không đưa lời khuyên y khoa, không hướng dẫn cách tự làm hại, không khuyên đối đầu hay trả đũa bố mẹ.
- Nếu hoàn cảnh là bạo hành, đừng khuyên "nói chuyện nhẹ nhàng với bố mẹ"; hãy hướng tới người lớn khác đáng tin cậy.
- Câu hỏi ngoài chủ đề: từ chối nhẹ nhàng và đưa cuộc trò chuyện về chuyện gia đình."""

def bo_dau(s):
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

_MAU_NGUY_CO = [
    r"tu sat",
    r"tu lam dau",
    r"tu lam hai",
    r"(muon|dinh|se|nghi den|nghi toi) (chet|bien mat|ket thuc (cuoc song|tat ca|doi))",
    r"khong (muon|con muon) song",
    r"\bchet (di|quach|cho xong)",
    r"song (lam gi|chi cho)",
    r"het (muon )?song",
    r"cat (tay|co tay|minh)",
    r"(uong|nuot) (thuoc|het thuoc)",
    r"(bi )?(bo me|ba|cha|me|bo|nguoi lon|anh|chi|chu|bac|duong) .{0,12}(danh|dap|bao hanh|xam hai|so mo|dong cham)\b(?! (gia|dan|co|bong|game|bai|ban)\b)",
    r"bi (danh|dap|bao hanh|xam hai|so mo|de doa|doa giet)\b(?! (gia|dan|co|bong|game|bai|ban)\b)",
    r"doa (giet|danh)",
    r"bien mat (khoi|vinh vien)",
]
_DANG_NGUY_CO = [re.compile(p) for p in _MAU_NGUY_CO]

def phat_hien_nguy_co(van_ban):
    if "tự tử" in van_ban.lower():
        return True
    t = bo_dau(van_ban)
    return any(p.search(t) for p in _DANG_NGUY_CO)

def xay_dung_lich_su(messages, toi_da=12):
    cu = messages[:-1][-toi_da:]
    ls = []
    for m in cu:
        role = "user" if m["role"] == "user" else "model"
        ls.append({"role": role, "parts": [m["content"]]})
    while ls and ls[0]["role"] != "user":
        ls.pop(0)
    return ls

class LocCo:

    def __init__(self):
        self.dem = ""
        self.da_quyet = False
        self.co = False

    def day(self, manh):
        if self.da_quyet:
            return manh
        self.dem += manh
        s = self.dem.lstrip()
        if len(s) < len(CO_NGUY_CO) and CO_NGUY_CO.startswith(s):
            return ""
        self.da_quyet = True
        if s.startswith(CO_NGUY_CO):
            self.co = True
            s = s[len(CO_NGUY_CO):].lstrip("\r\n ")
        self.dem = ""
        return s

    def ket(self):
        if self.da_quyet:
            return ""
        s = self.dem.lstrip()
        self.da_quyet = True
        if s.startswith(CO_NGUY_CO):
            self.co = True
            s = s[len(CO_NGUY_CO):].lstrip("\r\n ")
        return s
