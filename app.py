import streamlit as st
import time
import random

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Game Chải Lông Mèo 🐱", page_icon="🐱", layout="centered")

# --- KHỞI TẠO STATE (TRẠNG THÁI GAME) ---
if "fur_collected" not in st.session_state:
    st.session_state.fur_collected = 0  # Lông đang giữ (chưa bán)
if "coins" not in st.session_state:
    st.session_state.coins = 0  # Xu hiện có
if "cat_state" not in st.session_state:
    st.session_state.cat_state = "back"  # "back" (quay lưng) hoặc "front" (quay mặt)
if "cat_turn_time" not in st.session_state:
    st.session_state.cat_turn_time = time.time() + random.randint(3, 7)  # Thời điểm mèo đổi trạng thái
if "stun_until" not in st.session_state:
    st.session_state.stun_until = 0  # Thời gian hiệu ứng vật phẩm kết thúc
if "active_item" not in st.session_state:
    st.session_state.active_item = None
if "fortune_result" not in st.session_state:
    st.session_state.fortune_result = None

# --- DANH SÁCH 15 QUẺ MAY MẮN (ĐA DẠNG CHỦ ĐỀ) ---
FORTUNES = [
    # Học tập & Sự nghiệp
    "🎓 [Học Tập] Sách mở đường đi, trí tuệ nở hoa - Năm nay thi cử thành công, bảng vàng xướng tên!",
    "✍️ [Học Tập] Công danh thăng tiến, học một biết mười - Mọi bài thi, dự án đều hoàn thành xuất sắc!",
    "💡 [Học Tập] Trí tuệ minh mẫn, học đâu hiểu đó - Kiến thức vững vàng, mở ra nhiều cơ hội mới!",
    
    # Tài lộc & Tiền bạc
    "⛵ [Tài Lộc] Thuận buồm xuôi gió - Mọi công việc làm ăn đều trôi chảy, bình an!",
    "🪙 [Tài Lộc] Tiền vô như nước sông Đà - Tài lộc dồi dào, ví tiền luôn căng đầy!",
    "🌾 [Tài Lộc] Lộc tiến vinh hoa - Mọi sự đầu tư và nỗ lực đều mang lại kết quả ngọt ngào!",
    
    # Sức khỏe
    "🌸 [Sức Khỏe] Sức khỏe dẻo dai - Thân thể khỏe mạnh, năng lượng tràn đầy suốt cả năm!",
    "☀️ [Sức Khỏe] Tâm an trí sáng - Thân thể bình an, mỗi ngày trôi qua đều nhẹ nhàng và vui vẻ!",
    "🍀 [Sức Khỏe] Phước lộc thọ toàn - Thể chất vững vàng, xua tan mọi mệt mỏi bệnh tật!",
    
    # May mắn
    "🌞 [May Mắn] Cát tường như ý - Mọi bước đi đều gặp may mắn và luôn có quý nhân phù hộ!",
    "✨ [May Mắn] Vạn sự như ý - Những mong ước bấy lâu nay sẽ sớm hiện thực hóa!",
    "🌈 [May Mắn] Mưa hòa gió thuận - Mọi điều không may đều qua đi, chào đón vạn điều tốt lành!",
    
    # Mối quan hệ
    "💕 [Mối Quan Hệ] Duyên lành đưa lối - Xung quanh luôn có bạn bè tốt, thầy cô và đồng nghiệp yêu thương!",
    "🏡 [Mối Quan Hệ] Gia đạo hòa thuận - Cả nhà êm ấm, tình cảm gắn kết, tràn ngập tiếng cười!",
    "🤝 [Mối Quan Hệ] Quý nhân trợ lực - Đi đâu cũng được mọi người yêu mến, giúp đỡ nhiệt tình!"
]

# --- HÀM CẬP NHẬT TRẠNG THÁI MÈO ---
def update_cat_state():
    current_time = time.time()
    
    # Kiểm tra xem có vật phẩm nào đang có hiệu ứng không
    if current_time < st.session_state.stun_until:
        st.session_state.cat_state = "back"  # Đang phê/chơi đồ nên luôn quay lưng
        return

    # Nếu hết thời gian hiệu ứng vật phẩm
    if st.session_state.active_item:
        st.session_state.active_item = None

    # Mèo đổi trạng thái theo thời gian ngẫu nhiên
    if current_time > st.session_state.cat_turn_time:
        if st.session_state.cat_state == "back":
            st.session_state.cat_state = "front"
            st.session_state.cat_turn_time = current_time + random.randint(2, 4)
        else:
            st.session_state.cat_state = "back"
            st.session_state.cat_turn_time = current_time + random.randint(3, 6)

update_cat_state()

# --- GIAO DIỆN CHÍNH ---
st.title("🐱 Game Chải Lông Mèo")
st.audio("aaf63b4ec0940a2a6a4ad5f7b9786871.mp4", autoplay=True, loop=True)

# Bảng thông số
col1, col2, col3 = st.columns(3)
col1.metric("🪮 Lông đang giữ", f"{st.session_state.fur_collected} sợi")
col2.metric("🪙 Xu", f"{st.session_state.coins} xu")

if st.session_state.stun_until > time.time():
    remaining = int(st.session_state.stun_until - time.time())
    col3.metric("✨ Hiệu ứng vật phẩm", f"{st.session_state.active_item} ({remaining}s)")
else:
    col3.metric("✨ Hiệu ứng", "Không có")

st.divider()

# TAB CHỨC NĂNG
tab1, tab2, tab3 = st.tabs(["🪮 Chải Lông Mèo", "🛒 Cửa Hàng (Shop)", "🔮 Bốc Quẻ Đầu Năm"])

# --- TAB 1: MÀN HÌNH CHẢI LÔNG ---
with tab1:
    st.subheader("Khu Vực Chải Lông")
    st.caption("💡 Chải lông khi mèo **quay lưng**. Nếu chải khi mèo **quay mặt lại**, mèo sẽ giận và làm mất hết lông!")

    # Hiển thị Mèo
    if st.session_state.cat_state == "back":
        st.markdown("### 🐱 Mèo đang quay lưng lại... (An toàn!)")
        st.image("7c59985cb967810af105286709184ba2.jpg", use_container_width=True)
        st.write("*(Mèo đang quay lưng nghiêng ngó xung quanh, mau chải lông đi!)*")
    else:
        st.markdown("### 😾 MÈO ĐÃ QUAY MẶT LẠI!!! (DỪNG LẠI NGAY!)")
        st.image("6b73b5cf4a17da8304ac0ac0d3e19642.jpg", use_container_width=True)
        st.write("*(Mèo đang chớp mắt nhìn bạn chằm chằm...)*")

    st.write("---")

    # Nút bấm chải lông
    if st.button("🪮 Chải 1 cái!", use_container_width=True, type="primary"):
        update_cat_state()
        
        if st.session_state.cat_state == "back":
            st.session_state.fur_collected += 1
            st.success(" Bạn đã chải được +1 lông mèo!")
        else:
            st.session_state.fur_collected = 0
            st.error("😾 MÈO PHÁT HIỆN CẢM THẤY BỊ LÀM PHỀN VÀ TỨC GIẬN! Bạn bị cào và mất hết lông đang chải!")

    time.sleep(1.5)
    st.rerun()

# --- TAB 2: CỬA HÀNG ---
with tab2:
    st.subheader("🛒 Cửa Hàng Mèo Cún")
    
    # Bán lông lấy xu
    st.markdown("#### 1. Bán Lông Mèo")
    st.write(f"Bạn đang có **{st.session_state.fur_collected}** sợi lông. Giá: 1 sợi = 10 xu.")
    if st.button("💰 Bán tất cả lông mèo"):
        if st.session_state.fur_collected > 0:
            earned = st.session_state.fur_collected * 10
            st.session_state.coins += earned
            st.success(f"Bạn đã bán {st.session_state.fur_collected} lông và nhận được {earned} xu!")
            st.session_state.fur_collected = 0
            st.rerun()
        else:
            st.warning("Bạn không có lông mèo nào để bán!")

    st.divider()

    # Mua vật phẩm
    st.markdown("#### 2. Mua Vật Phẩm Hỗ Trợ")
    
    # Vật phẩm 1: Pate
    c1, c2 = st.columns([3, 1])
    c1.write("**🥫 Pate Mèo** (100 xu)\n\n*Làm mèo choáng & ngơ ngác trong 30 giây.*")
    if c2.button("Mua Pate", key="buy_pate"):
        if st.session_state.coins >= 100:
            st.session_state.coins -= 100
            st.session_state.stun_until = time.time() + 30
            st.session_state.active_item = "Pate Mèo"
            st.success("Bạn đã cho mèo ăn Pate! Mèo bị choáng trong 30s!")
            st.rerun()
        else:
            st.error("Bạn không đủ xu!")

    # Vật phẩm 2: Cuộn len
    c1, c2 = st.columns([3, 1])
    c1.write("**🧶 Cuộn Len** (250 xu)\n\n*Làm mèo chơi đùa, không quan tâm xung quanh trong 1 phút 25 giây (85s).*")
    if c2.button("Mua Cuộn Len", key="buy_yarn"):
        if st.session_state.coins >= 250:
            st.session_state.coins -= 250
            st.session_state.stun_until = time.time() + 85
            st.session_state.active_item = "Cuộn Len"
            st.success("Bạn đã thả cuộn len! Mèo bận chơi trong 1m25s!")
            st.rerun()
        else:
            st.error("Bạn không đủ xu!")

    # Vật phẩm 3: Cỏ mèo
    c1, c2 = st.columns([3, 1])
    c1.write("**🌿 Cỏ Mèo** (475 xu)\n\n*Làm mèo phê cỏ, hoàn toàn mất chú ý trong 2 phút 30 giây (150s).*")
    if c2.button("Mua Cỏ Mèo", key="buy_catnip"):
        if st.session_state.coins >= 475:
            st.session_state.coins -= 475
            st.session_state.stun_until = time.time() + 150
            st.session_state.active_item = "Cỏ Mèo"
            st.success("Bạn đã cho mèo phê Cỏ Mèo trong 2m30s!")
            st.rerun()
        else:
            st.error("Bạn không đủ xu!")

# --- TAB 3: BỐC QUẺ ---
with tab3:
    st.subheader("🔮 Bốc Quẻ May Mắn Đầu Năm")
    st.write("Chi phí: **85 xu / lần bốc quẻ**.")
    st.caption("Dự đoán vận may về Học tập, Tài lộc, Sức khỏe, May mắn & Mối quan hệ!")

    if st.button("🎋 Bốc Quẻ Ngay (85 xu)", type="primary"):
        if st.session_state.coins >= 85:
            st.session_state.coins -= 85
            st.session_state.fortune_result = random.choice(FORTUNES)
            st.rerun()
        else:
            st.error("Bạn không đủ xu để bốc quẻ! Hãy chải lông mèo lấy xu bán nhé.")

    if st.session_state.fortune_result:
        st.success("✨ **QUẺ CỦA BẠN:**")
        st.info(f"### {st.session_state.fortune_result}")
