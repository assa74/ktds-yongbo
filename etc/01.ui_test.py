import os
import streamlit as st
from openai import AzureOpenAI
import pandas as pd
import plotly.express as px

# 환경변수 (실제 배포 시 .env 파일 사용 권장)
OPENAI_ENDPOINT = "https://yb0617azureopenai002.openai.azure.com/"
OPENAI_API_KEY = "4WPNYNq47zPD34wfdSfZmS1tQZDtHRWIurmUqWqG2CQ5KBZZp9MPJQQJ99BFAC4f1cMXJ3w3AAABACOGn0g7"
CHAT_MODEL = "dev-gpt-4o-mini"
EMBEDDING_MODEL = "dev-text-embedding-3-small"
SEARCH_ENDPOINT = "https://yb0617-aisearch002.search.windows.net"
SEARCH_API_KEY = "UGC9S7WgKEieHSSr4F5KBVnrtqQYc7yIsf8hY73OYnAzSeB7HDKX"
INDEX_NAME = "rag-index"

# 매핑 변수
open_ai_endpoint = OPENAI_ENDPOINT
open_ai_key = OPENAI_API_KEY
chat_model = CHAT_MODEL
embedding_model = EMBEDDING_MODEL
search_url = SEARCH_ENDPOINT
search_key = SEARCH_API_KEY
index_name = INDEX_NAME

# Azure OpenAI 클라이언트 초기화
chat_client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=open_ai_endpoint,
    api_key=open_ai_key
)

# KT 브랜드 색상 적용 (CSS)
st.markdown("""
    <style>
        /* 전체 바탕색 및 글씨 색상 */
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        /* 사이드바 스타일 */
        .css-1d391kg {  /* 사이드바 클래스 */
            background-color: #333333;
            color: #FFFFFF;
        }
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #DA1E28;  /* KT Red */
            margin-bottom: 20px;
            text-align: center;
        }
        .step-box {
            background-color: #666666;  /* KT Gray */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 16px;
            color: #FFFFFF;
        }
        .emoji {
            font-size: 20px;
            margin-right: 10px;
        }
        .step-title {
            color: #FFFFFF;
            font-weight: bold;
        }
        .stButton>button {
            width: 100%;
            background-color: #DA1E28;  /* KT Red */
            color: #FFFFFF;
            border-radius: 5px;
            margin-top: 5px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #A8181F;  /* Darker KT Red */
        }
        /* 채팅 UI 스타일 */
        .stChatMessage {
            background-color: #FFFFFF;  /* White bubbles */
            color: #000000;  /* Black text */
            border-radius: 10px;
        }
        .stTextInput input {
            background-color: #333333;
            color: #FFFFFF;
            border: 1px solid #DA1E28;  /* KT Red border */
        }
        .stTextInput input::placeholder {
            color: #999999;  /* Lighter gray placeholder */
        }
        /* 메트릭 스타일 */
        .stMetric {
            background-color: #000000;
            color: #FFFFFF;
            border: 1px solid #DA1E28;  /* KT Red border */
        }
        /* 제목 및 텍스트 */
        h1, h2, h3, p, div {
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit 앱 기본 설정
st.title("KT 유선상품 고객 BS(Before Service) 분석 및 영업지원 에이전트")

# 초기 채팅 히스토리 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 KT 유선상품 고객의 사전점검 BS 대상 분석 및 영업지원 에이전트입니다."}
    ]

def get_openai_response(messages):
    """
    OpenAI API를 호출하여 응답 메시지를 반환합니다.
    """
    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_url,
                    "index_name": index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_key,
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": embedding_model,
                    },
                }
            }
        ],
    }
    response = chat_client.chat.completions.create(
        model=chat_model,
        messages=messages,
        extra_body=rag_params
    )
    return response.choices[0].message.content

def _handle_precheck(precheck_input, label):
    """
    공통 precheck 로직: precheck_input 메시지를 채팅 히스토리에 추가하고 OpenAI 응답 호출
    """
    try:
        if precheck_input.strip() == "_":
            st.warning("입력값이 비어 있습니다. 내용을 선택해주세요.")
            return
        st.session_state.messages.append({"role": "user", "content": precheck_input})
        with st.spinner(f"{label} 응답을 기다리는 중..."):
            assistant_response = get_openai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.chat_message("assistant").write(assistant_response)
    except Exception as e:
        st.error(f"{label} 실패: {e}")

def render_menu():
    """
    사이드바 메뉴 영역: st.sidebar.markdown과 버튼으로 옵션 표시
    """
    st.sidebar.image("./images/logo_kt.png", width=150)  # KT 로고 (실제 로고 파일로 교체 권장)
    st.sidebar.markdown("""
        <div class="sidebar-title">KT 유선상품 BS 메뉴</div>
    """, unsafe_allow_html=True)

    options = [
        {"title": "BS분석", "desc": "동 그룹별 사전점검 대상 현황", "prompt": "주소의 동 그룹으로 사전점검 대상 현황 count를 표로 정리해줘"},
        {"title": "인터넷 품질점검", "desc": "인터넷 품질점검 체크리스트", "prompt": "인터넷 품질점검 체크리스트 알려줘"},
        {"title": "TV 품질점검", "desc": "TV 품질점검 체크리스트", "prompt": "TV 품질점검 체크리스트 알려줘"},
        {"title": "VOIP 품질점검", "desc": "VOIP 품질점검 체크리스트", "prompt": "VOIP 품질점검 체크리스트 알려줘"},
        {"title": "PSTN 품질점검", "desc": "PSTN 품질점검 체크리스트", "prompt": "PSTN 품질점검 체크리스트 알려줘"},
        {"title": "인터넷 영업멘트", "desc": "인터넷 상품 영업 멘트", "prompt": "인터넷 영업멘트 알려줘"},
        {"title": "TV 영업멘트", "desc": "TV 상품 영업 멘트", "prompt": "TV 영업멘트 알려줘"},
        {"title": "VOIP 영업멘트", "desc": "VOIP 상품 영업 멘트", "prompt": "VOIP 영업멘트 알려줘"},
        {"title": "PSTN 영업멘트", "desc": "PSTN 상품 영업 멘트", "prompt": "PSTN 영업멘트 알려줘"},
        {"title": "영업 팁", "desc": "효과적인 영업 팁", "prompt": "영업 팁 알려줘"}
    ]

    for option in options:
        st.sidebar.markdown(f"""
            <div class="step-box">
                <span class="step-title">{option['title']}</span><br>
                {option['desc']}
            </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button(f"선택: {option['title']}", key=option['title']):
            _handle_precheck(option['prompt'], option['title'])

def render_chat_area():
    """
    메인 페이지 채팅 영역: 기존 채팅 히스토리와 사용자 입력 처리
    """
    # 채팅 UI
    for message in st.session_state.messages:
        if message["role"] != "system":  # 시스템 메시지 제외
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_input := st.chat_input("메시지를 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("응답을 기다리는 중..."):
            assistant_response = get_openai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.chat_message("assistant").write(assistant_response)



def main():
    render_chat_area()
    render_menu()

if __name__ == "__main__":
    main()
