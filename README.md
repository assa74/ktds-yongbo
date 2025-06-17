## 프로젝트 1: 유선상품 고객 BS(Before Service)대상 분석 및 영업지원 에이전트
 # 1. 사전준비
  *  Agent 사전지식  : 영업맨트.docx, 유선BS품질점검 질문사항_맨트.docx, fine_data_0617_1.csv(BS대상 샘플)
  
 # 2. 시나리오
  * BS(Before Service) 대상 고객을 구별하여 선제적으로 kt품질 이슈가 없는지 확인 및 품질점검 맨트 제공 Assist
  * 고객 댁내 방문시 kt 유선통신 서비스 추가에 따른 장점 및 혜택등을 설명(영업 멘트) 제공 Assist

 # 📈 유선상품 BS 서비스 플로우
   1. **시작**
   2. ▶️ **사전점검** → BS활동을 위한 지역별 현황 분석
   3. ▶️ **품질점검** → 현장 점검시 체크할 사항
   4. ▶️ **고객 문의** → 고객 맞춤형 설명
   5. ▶️ **영업안내** → 상품별 제안 팀 및 유의사항(예시 등)

# 3. Azure 서비스 구성
  * Azure AI Search, 스토리지 계정, Azure OpenAI
  * Azure AI Foundry :  gpt40-mini, tet-embedding-3-smll 모델

# 4. 소스 구성
  * 01.rag_chat.py
    - Azure OpenAI 접속 설정
    - Streamlit을 활용한 UI/UX 구성
      . chatbot 창에 BS분석, 인터넷 품질점검 사항, TV 품질점검 사항, VOIP 품질점검 사항, PSTN 품질점검 사항 등 버튼 생성
      . 메세지 히스토리 관리
