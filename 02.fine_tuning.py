# 2: GPT-4o 파인튜닝
# OpenAI API로 파인튜닝을 진행

# OpenAI의 GPT-4o 파인튜닝은 Azure OpenAI Service를 사용.
# Azure 포털 → Azure OpenAI 리소스 생성:
# 리소스 이름: "BS_Predict_GPT4o".

# 지역: East US 또는 지원되는 지역.

# 모델: GPT-4o (파인튜닝 지원 확인).

# API 키 및 엔드포인트 URL를 복사.
# Azure 포털에서 API 키와 엔드포인트 URL 복사.
# -*- coding: utf-8 -*-

from openai import OpenAI

client = OpenAI(api_key="your_azure_openai_api_key")

# 훈련 데이터 업로드
with open("training_data.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

# 검증 데이터 업로드
with open("validation_data.jsonl", "rb") as f:
    validation_file = client.files.create(file=f, purpose="fine-tune")

# 파인튜닝 작업 시작
# 설정:
# n_epochs: 3~5 (데이터 크기에 따라 조정).
# batch_size: 4~8 (GPU 메모리 고려).
# learning_rate_multiplier: 0.1~0.3 (과적합 방지).

fine_tune = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model="gpt-4o",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 0.1
    }
)
print(f"파인튜닝 작업 ID: {fine_tune.id}")

# OpenAI API로 작업 상태 확인
status = client.fine_tuning.jobs.retrieve(fine_tune.id)
print(status.status)

# 파인튜닝된 모델로 예측
prompt = "동: 서초동, 인터넷: 1, TV: 0, VoIP: 0, PSTN: 0, 시설: FTTH, 시설속도: 500M, 고장문의: 5, 개통년도: 2023"
response = client.chat.completions.create(
    model="your_fine_tuned_model_id",
    messages=[
        {"role": "system", "content": "You are a model that predicts BS대상 based on location and service data."},
        {"role": "user", "content": prompt}
    ]
)
print(response.choices[0].message.content)

