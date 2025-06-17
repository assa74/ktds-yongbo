import streamlit as st
import plotly.express as px
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="유선상품 BS 서비스 대시보드", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 유선상품 BS 서비스 대시보드입니다. 사이드바에서 단계를 클릭하거나 채팅으로 문의해 주세요."}
    ]
if "chat_prompt" not in st.session_state:
    st.session_state.chat_prompt = "문의 입력..."  # Default placeholder

# 사이드바: 마크다운 + 버튼으로 플로우 구현
st.sidebar.markdown("""
    <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }
        .step-box {
            background-color: #f0f4f8;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 16px;
        }
        .emoji {
            font-size: 20px;
            margin-right: 10px;
        }
        .step-title {
            color: #34495e;
            font-weight: bold;
        }
        .stButton>button {
            width: 100%;
            background-color: #005BAC;
            color: white;
            border-radius: 5px;
            margin-top: 5px;
        }
        .stButton>button:hover {
            background-color: #003087;
        }
    </style>

    <div class="sidebar-title">유선상품 BS 서비스 플로우</div>
""", unsafe_allow_html=True)

# 단계 정의
steps = [
    {"emoji": "📋", "title": "1. 사전점검", "desc": "환경 및 회선 확인 후 보고서 작성", "prompt": "사전점검은 어떻게 진행되나요?"},
    {"emoji": "🔍", "title": "2. 품질점검", "desc": "현장/원격 진단으로 문제 해결", "prompt": "인터넷 속도 문제를 점검해 주세요"},
    {"emoji": "📞", "title": "3. 고객 문의", "desc": "상담원 연결, 문제 기록/해결", "prompt": "고객 지원 센터에 문의하려면 어떻게 해야 하나요?"},
    {"emoji": "📝", "title": "4. 영업안내", "desc": "상품 제안, 계약, 사후 관리", "prompt": "요금제와 상품을 안내해 주세요"}
]

# 사이드바 단계 및 버튼
for step in steps:
    st.sidebar.markdown(f"""
        <div class="step-box">
            <span class="emoji">{step['emoji']}</span>
            <span class="step-title">{step['title']}</span><br>
            {step['desc']}
        </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button(f"문의: {step['title']}", key=step['title']):
        # 클릭 시 프롬프트 직접 메시지에 추가 및 placeholder 업데이트
        prompt = step['prompt']
        st.session_state.chat_prompt = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 챗봇 응답 생성
        response = "문의를 처리 중입니다. 잠시만 기다려 주세요."
        if "사전점검" in prompt:
            response = "사전점검은 서비스 설치 전 회선 상태와 환경을 확인하는 과정입니다. 기술자가 방문해 보고서를 작성합니다."
        elif "품질점검" in prompt or "인터넷 속도" in prompt:
            response = "인터넷 속도 문제ですね? 품질점검 팀이 현장/원격 진단을 진행합니다. 예약을 원하시면 주소를 알려주세요!"
        elif "고객 문의" in prompt or "고객 지원" in prompt:
            response = "고객 문의는 24/7 상담원 연결 또는 온라인 포털로 접수 가능합니다. 문의 유형을 알려주세요!"
        elif "요금제" in prompt or "영업안내" in prompt:
            response = "요금제 문의 감사합니다! 제공 상품: [500Mbps 인터넷, IPTV 결합]. 계약 상담을 진행할까요?"
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# 메인 페이지: 대시보드
st.title("유선상품 BS 서비스 대시보드")


# 채팅 UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 채팅 입력창 (단일 placeholder 사용)
prompt = st.chat_input(st.session_state.chat_prompt)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 챗봇 응답
    response = "문의를 처리 중입니다. 잠시만 기다려 주세요."
    if "사전점검" in prompt:
        response = "사전점검은 서비스 설치 전 회선 상태와 환경을 확인하는 과정입니다. 기술자가 방문해 보고서를 작성합니다."
    elif "품질점검" in prompt or "인터넷 속도" in prompt:
        response = "인터넷 속도 문제 품질점검 팀이 현장/원격 진단을 진행합니다. 예약을 원하시면 주소를 알려주세요!"
    elif "고객 문의" in prompt or "고객 지원" in prompt:
        response = "고객 문의는 24/7 상담원 연결 또는 온라인 포털로 접수 가능합니다. 문의 유형을 알려주세요!"
    elif "요금제" in prompt or "영업안내" in prompt:
        response = "요금제 문의 감사합니다! 제공 상품: [500Mbps 인터넷, IPTV 결합]. 계약 상담을 진행할까요?"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.chat_prompt = "문의 입력..."  # 입력 후 placeholder 초기화

