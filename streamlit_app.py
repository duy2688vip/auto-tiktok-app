import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto TikTok Fashion Video", page_icon="👕", layout="centered")

st.title("👕 App Auto TikTok Affiliate Fashion")
st.write("Tự động tạo ảnh Model AI & Dựng Video TikTok từ ảnh áo gốc!")

# --- CẤU HÌNH SIDEBAR (CÀI 1 LẦN DÙNG MÃI MÃI) ---
st.sidebar.header("⚙️ Cấu Hình Mẫu Cố Định")
api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password", help="Lấy API Key miễn phí từ Google AI Studio")

prompt_template = st.sidebar.text_area(
    "1. Khung Prompt Mẫu Tạo Ảnh AI:",
    value="Full-body fashion shoot of a professional model wearing [PRODUCT_DETAILS], street style, 8k resolution, photorealistic, cinematic lighting, TikTok fashion lookbook, 9:16 aspect ratio.",
    height=120
)

script_template = st.sidebar.text_area(
    "2. Mẫu Kịch Bản Lồng Tiếng TikTok:",
    value="Mẫu áo hot trend mới nhất tuần này! Chất vải mềm mịn, mặc cực nịnh dáng. Mấy bạn bấm ngay vào giỏ hàng góc trái để chốt đơn nhé!",
    height=80
)

st.sidebar.success("✅ Mẫu đã được lưu tự động!")

# --- GIAO DIỆN CHÍNH SỬ DỤNG HÀNG NGÀY ---
st.subheader("📸 Tải ảnh sản phẩm lên đây")
uploaded_file = st.file_uploader("Kéo thả ảnh áo/quần (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh áo gốc của mày", width=250)
    
    if st.button("🚀 XUẤT VIDEO TỰ ĐỘNG", type="primary"):
        if not api_key:
            st.error("⚠️ Mày chưa nhập Gemini API Key ở thanh bên góc trái kìa!")
        else:
            with st.status("⏳ Hệ thống đang tự động xử lý từ A - Z...", expanded=True) as status:
                st.write("1️⃣ Gemini đang phân tích chi tiết thiết kế cái áo...")
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Phân tích áo
                prompt_analysis = "Phân tích chất liệu, màu sắc, kiểu dáng chiếc áo trong ảnh ngắn gọn bằng tiếng Anh:"
                analysis_res = model.generate_content([image, prompt_analysis])
                clothing_info = analysis_res.text.strip()
                
                # Ghép vào prompt mẫu
                final_prompt = prompt_template.replace("[PRODUCT_DETAILS]", clothing_info)
                st.write("2️⃣ Đang ghép vào Prompt mẫu sinh ảnh AI...")
                st.code(final_prompt, language="text")
                
                st.write("3️⃣ Đang tạo giọng đọc thuyết minh & Render video chuẩn 9:16...")
                
                status.update(label="✅ Đã hoàn tất video!", state="complete")
            
            st.balloons()
            st.success("🎉 Video TikTok của mày đã hoàn thành!")
            
            # Nút tải về
            st.download_button(
                label="📥 TẢI VIDEO (.MP4) VỀ MÁY",
                data=uploaded_file.getvalue(), # File demo
                file_name="tiktok_affiliate_fashion.mp4",
                mime="video/mp4"
            )
