import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto TikTok Affiliate", page_icon="👕", layout="centered")

st.title("👕 App Auto TikTok Affiliate Fashion")
st.write("Tự động phân tích sản phẩm và tạo Prompt / Kịch bản TikTok!")

# --- CẤU HÌNH SIDEBAR ---
st.sidebar.title("⚙️ Cấu Hình Mẫu Cố Định")
raw_api_key = st.sidebar.text_input("Mã API Gemini:", type="password", help="Lấy API Key từ Google AI Studio")
api_key = raw_api_key.strip() if raw_api_key else ""

prompt_analysis = st.sidebar.text_area(
    "1. Khung Nhắc Mẫu Tạo Ảnh AI:",
    value="Full-body fashion shoot of a professional model wearing [CHI TIẾT SẢN PHẨM], street style, 8k resolution, photorealistic, cinematic lighting, TikTok fashion lookbook, 9:16 aspect ratio.",
    height=120
)

prompt_script = st.sidebar.text_area(
    "2. Mẫu Kịch Bản Lồng Tiếng TikTok:",
    value="Áo đẹp nịnh dáng. Mấy bạn bấm ngay vào giỏ hàng góc trái để chốt đơn nhé!",
    height=100
)

# --- TẢI ẢNH VÀ XỬ LÝ ---
uploaded_file = st.file_uploader("Tải ảnh sản phẩm (Áo/Quần/Váy)...", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh áo gốc", use_container_width=True)
    
    if st.button("🚀 XUẤT VIDEO TỰ ĐỘNG", type="primary"):
        try:
            genai.configure(api_key=api_key)
            
            with st.spinner("⚡ Đang quét danh sách Model khả dụng trong API Key của bạn..."):
                # Tự động lấy tất cả các model mà API Key này có quyền dùng
                all_models = list(genai.list_models())
                valid_models = [
                    m.name for m in all_models 
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                if not valid_models:
                    st.error("❌ API Key này không tìm thấy model nào hoạt động! Bạn hãy thử tạo lại API Key mới.")
                    st.stop()
                
                # Ưu tiên chọn model có chữ 'flash', nếu không có thì lấy model khả dụng đầu tiên
                chosen_model_name = None
                for m_name in valid_models:
                    if 'flash' in m_name.lower():
                        chosen_model_name = m_name
                        break
                if not chosen_model_name:
                    chosen_model_name = valid_models[0]
                    
                st.info(f"💡 Đang kết nối thành công với Model: `{chosen_model_name}`")
                model = genai.GenerativeModel(chosen_model_name)
                
            with st.spinner("⚡ Đang gửi ảnh cho AI phân tích..."):
                optimized_img = image.copy()
                optimized_img.thumbnail((1024, 1024))
                
                response = model.generate_content([
                    optimized_img, 
                    f"Phân tích chiếc áo trong ảnh ngắn gọn bằng tiếng Anh và điền vào mẫu: {prompt_analysis}"
                ])
                
                st.success("✅ Đã xử lý xong thành công!")
                st.subheader("📌 Kết quả Prompt & Kịch bản:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"⚠️ Lỗi hệ thống: {e}")
elif not api_key:
    st.warning("⚠️ Vui lòng nhập Gemini API Key ở thanh bên trái!")
