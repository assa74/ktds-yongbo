import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st
from streamlit_pills import pills  # 먼저: pip install streamlit-pills

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

# Streamlit 앱 기본 설정
st.title("유선상품 고객BS(Before Service)대상 분석 및 영업지원 에이전트!!!")

# 초기 채팅 히스토리 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 유선상품 고객의 사전점검 BS 대상 분석 및 영업지원 에이전트 입니다."}
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
            print("입력값이 비어 있습니다. 내용을 입력해주세요.")
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
    좌측 메뉴 영역: streamlit-pills 사용하여 품질점검 옵션을 pill 스타일로 표시합니다.
    """
    options = [
        "_",
        "BS분석",
        "인터넷 품질점검 사항",
        "TV 품질점검 사항",
        "VOIP 품질점검 사항",
        "PSTN 품질점검 사항",
        "인터넷 영업멘트",
        "TV 영업멘트",
        "VOIP 영업멘트",
        "PSTN 영업멘트",
        "영업 팁"        
    ]
    selected = pills(options=options, index=0, label="메뉴 선택")
    print(f"Selected option: {selected}")

    if selected:
        if selected == "BS분석":
            _handle_precheck("주소의 동 그룹으로 사전점검 대상 현황 count를 표로 정리해줘", "사전점검")
        elif selected == "인터넷 품질점검 사항":
            _handle_precheck("인터넷 품질점검 체크리스트 알려줘", "인터넷 품질점검")
        elif selected == "TV 품질점검 사항":
            _handle_precheck("TV 품질점검 체크리스트 알려줘", "TV 품질점검")
        elif selected == "VOIP 품질점검 사항":
            _handle_precheck("VOIP 품질점검 체크리스트 알려줘", "VOIP 품질점검")
        elif selected == "PSTN 품질점검 사항":
            _handle_precheck("PSTN 품질점검 체크리스트 알려줘", "PSTN 품질점검")
        elif selected == "인터넷 영업멘트":
            _handle_precheck("인터넷 영업멘트 알려줘", "인터넷 영업멘트")
        elif selected == "TV 영업멘트":
            _handle_precheck("TV 영업멘트 알려줘", "TV 영업멘트")
        elif selected == "VOIP 영업멘트":
            _handle_precheck("VOIP 영업멘트 알려줘", "VOIP 영업멘트")
        elif selected == "PSTN 영업멘트":
            _handle_precheck("PSTN 영업멘트 알려줘", "PSTN 영업멘트")
        elif selected == "영업 팁":
            _handle_precheck("영업 팁 알려줘", "영업 팁")

def render_chat_area():
    """
    우측 채팅 영역: 기존 채팅 히스토리와 사용자 입력 처리.
    """
    st.header("채팅")

    # 사용자 입력
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
