import streamlit as st
import base64
from PIL import Image
from openai import OpenAI

# 🔑 API 키 (Streamlit Cloud Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🎨 페이지 설정
st.set_page_config(
    page_title="이미지 이해 AI",
    page_icon="🖼️",
    layout="wide"
)

# 🎯 사이드바
st.sidebar.title("⚙️ 설정")

analysis_mode = st.sidebar.selectbox(
    "분석 스타일 선택",
    ["기본 설명", "자세한 분석", "짧은 요약"]
)

st.sidebar.markdown("---")
st.sidebar.info("이미지를 업로드하면 AI가 내용을 분석합니다.")

# 🏷️ 메인 타이틀
st.title("🖼️ 이미지 이해 AI")
st.markdown("GPT Vision API를 활용한 이미지 분석 웹앱입니다.")

# 📤 파일 업로드
uploaded_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=["png", "jpg", "jpeg", "webp"]
)

# 🔍 프롬프트 설정 함수
def get_prompt(mode):
    if mode == "기본 설명":
        return "이 이미지를 설명해줘."
    elif mode == "자세한 분석":
        return "이 이미지의 구성 요소, 상황, 분위기를 자세히 설명해줘."
    else:
        return "이 이미지를 한 문장으로 요약해줘."

# 📸 이미지 업로드 후 처리
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # 🔥 좌우 분할
    col1, col2 = st.columns([1, 1.2])

    # 📷 왼쪽: 이미지
    with col1:
        st.image(image, caption="업로드 이미지", use_container_width=True)

    # 🧠 오른쪽: 결과 영역
    with col2:
        st.markdown("### 🧠 분석 결과")
        result_placeholder = st.empty()

        # 초기 안내 메시지
        result_placeholder.info("👉 '분석 시작' 버튼을 눌러주세요.")

        # 🚀 분석 버튼
        if st.button("🔍 분석 시작"):
            with st.spinner("AI가 이미지를 분석 중입니다..."):
                base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": get_prompt(analysis_mode)},
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

                    result_placeholder.success("✅ 분석 완료!")
                    st.write(result)

                except Exception as e:
                    result_placeholder.error(f"에러 발생: {e}")

else:
    st.info("👆 이미지를 먼저 업로드해주세요.")
