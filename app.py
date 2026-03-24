import streamlit as st
import base64
from PIL import Image
from openai import OpenAI

# 🔑 Streamlit secrets에서 API 키 불러오기
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🖼️ GPT Vision 이미지 해석 앱")

uploaded_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)

    st.write("🔍 분석 중...")

    # base64 인코딩
    base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 최신 + 빠름 + 저렴
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지를 자세히 설명해줘."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        result = response.choices[0].message.content
        st.success(result)

    except Exception as e:
        st.error(f"에러 발생: {e}")