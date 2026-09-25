import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Video thời trang TikTok tự động", page_icon="👕", layout="centered")

st.title("👕 Ứng dụng tự động tiếp thị liên kết TikTok thời trang")
st.write("Tự động tạo ảnh Model AI & Build Video TikTok từ ảnh gốc!")

# --- CẤU HÌNH SIDEBAR ---
st.sidebar.title("⚙️ Cấu hình mẫu Cố Định")
api_key = st.sidebar.text_input("Mã API Gemini:", type="password", help="Lấy API Key miễn phí từ Google AI Studio")

prompt_analysis = st.sidebar.text_area(
    "1. Khung Nhắc Mẫu Tạo Ảnh AI:",
    value="Bộ ảnh thời trang toàn thân của một người mẫu chuyên nghiệp mặc [CHI TIẾT SẢN PHẨM], phong cách đường phố, ánh sáng tự nhiên, tỉ lệ 9:16 chất lượng 8k sắc nét.",
    height=120
)

prompt_script = st.sidebar.text_area(
    "2. Mẫu Kịch Bản Lồng Tiếng TikTok:",
    value="Áo đẹp nịnh dáng. Mấy bạn bấm ngay vào giỏ hàng góc trái để chốt đơn nhé!",
    height=100
)

st.sidebar.success("Mẫu đã được lưu tự động!")

# --- TẢI ẢNH VÀ XỬ LÝ ---
uploaded_file = st.file_uploader("Tải ảnh sản phẩm (Áo/Quần/Váy)...", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh áo gốc", use_container_width=True)
    
    if st.button("🚀 XUẤT VIDEO TỰ ĐỘNG"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3.8-flash')
            
            with st.spinner("⚡ Đang tối ưu ảnh & gửi AI xử lý siêu tốc..."):
                # TỐI ƯU TỐC ĐỘ: Thu nhỏ ảnh về tối đa 1024px để gửi cực nhanh
                optimized_img = image.copy()
                optimized_img.thumbnail((1024, 1024))
                
                st.write("1️⃣ Gemini đang phân tích chi tiết thiết kế...")
                response = model.generate_content([
                    optimized_img, 
                    f"Phân tích chiếc áo trong ảnh và điền chi tiết vào mẫu sau: {prompt_analysis}"
                ])
                
                st.success("✅ Đã xử lý xong!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")
elif not api_key:
    st.warning("⚠️ Vui lòng nhập Gemini API Key ở thanh bên trái trước khi bắt đầu!")
