import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
from io import BytesIO

# 🔑 API 키
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🎨 페이지 설정
st.set_page_config(
    page_title="AI 이미지 생성기",
    page_icon="🎨",
    layout="wide"
)

# 🎯 사이드바
st.sidebar.title("⚙️ 설정")

# 🎨 스타일 선택
style_option = st.sidebar.selectbox(
    "스타일 선택",
    ["기본", "사실적", "애니메이션", "수채화", "픽셀아트"]
)

st.sidebar.markdown("---")
st.sidebar.info("한국어 입력 → 영어 변환 → 이미지 생성")

# 🏷️ 타이틀
st.title("🎨 AI 이미지 생성기")
st.markdown("프롬프트를 입력하고 다양한 스타일로 이미지를 생성하세요.")

# 📥 입력
user_prompt = st.text_input("📝 프롬프트 입력 (한국어)")

# 🎨 스타일 적용 함수
def apply_style(prompt, style):
    style_dict = {
        "기본": "",
        "사실적": "realistic, high detail, photorealistic",
        "애니메이션": "anime style, vibrant colors, studio ghibli style",
        "수채화": "watercolor painting, soft brush strokes",
        "픽셀아트": "pixel art, 8-bit style"
    }
    
    style_text = style_dict.get(style, "")
    
    if style_text:
        return f"{prompt}, {style_text}"
    return prompt

# 🌐 번역 함수
def translate_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate Korean to English."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# 🚀 실행 버튼
if st.button("🎨 이미지 생성"):
    if user_prompt.strip() == "":
        st.warning("프롬프트를 입력해주세요.")
    else:
        with st.spinner("이미지 생성 중..."):

            try:
                # 1️⃣ 번역
                translated_prompt = translate_text(user_prompt)

                # 2️⃣ 스타일 적용
                styled_prompt = apply_style(translated_prompt, style_option)

                # 🔥 좌우 레이아웃
                col1, col2 = st.columns([1, 1.2])

                with col1:
                    st.markdown("### 📝 프롬프트 정보")
                    st.write("**한국어:**", user_prompt)
                    st.write("**영어:**", translated_prompt)
                    st.write("**스타일 적용:**", style_option)

                # 3️⃣ 이미지 생성
                result = client.images.generate(
                    model="gpt-image-1",
                    prompt=styled_prompt,
                    size="1024x1024"
                )

                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)
                image = Image.open(BytesIO(image_bytes))

                with col2:
                    st.markdown("### 🖼️ 생성된 이미지")
                    st.image(image, use_container_width=True)

                    # 🔥 다운로드 버튼 추가
                    st.download_button(
                        label="📥 이미지 다운로드",
                        data=image_bytes,
                        file_name="generated_image.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"에러 발생: {e}")
