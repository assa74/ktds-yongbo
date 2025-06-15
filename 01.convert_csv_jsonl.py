# -*- coding: utf-8 -*-
# 1: 데이터 포맷 변환
# GPT-4o는 텍스트 기반 입력에 대한 모델이고, CSV 데이터를 JSONL 포맷으로 변환.
# 현재 데이터: CSV 형식 (동, PSTN, 인터넷, TV, VoIP, 시설, 시설속도, 고장문의, 개통년도, BS대상).
# 필요한 포맷: JSONL (각 행이 JSON 객체로, 입력 프롬프트와 출력으로 구성).

import pandas as pd
import json
from sklearn.model_selection import train_test_split

# 1. CSV 파일 읽기
csv_file = "fine_data_0613 2(서초구_주소_샘플_10000건_0613).csv"
df = pd.read_csv(csv_file)

# 2. 데이터 전처리
# 결측값 처리: BS대상 빈칸 → "None", 서비스 열(O → 1, 빈칸 → 0)
df['BS대상'] = df['BS대상'].fillna('None')
df['PSTN'] = df['PSTN'].apply(lambda x: 1 if x == 'O' else 0)
df['인터넷'] = df['인터넷'].apply(lambda x: 1 if x == 'O' else 0)
df['TV'] = df['TV'].apply(lambda x: 1 if x == 'O' else 0)
df['VoIP'] = df['VoIP'].apply(lambda x: 1 if x == 'O' else 0)

# 다른 결측값 처리 (필요 시)
# 예: 시설, 시설속도, 개통년도 등의 결측값을 기본값으로 채움
df['시설'] = df['시설'].fillna('Unknown')
df['시설속도'] = df['시설속도'].fillna('Unknown')
df['개통년도'] = df['개통년도'].fillna(0)
df['고장문의'] = df['고장문의'].fillna(0)

# 3. 데이터 분할 (80% 훈련, 10% 검증, 10% 테스트)
# 전체 데이터 훈련+검증(90%)과 테스트(10%)로 분할
train_val_df, test_df = train_test_split(df, test_size=0.1, random_state=42, stratify=df['BS대상'])

# 훈련+검증을 다시 훈련(80/90=88.89%)과 검증(10/90=11.11%)로 분할
# 결과적으로 전체 데이터 기준 훈련 80%, 검증 10%
train_df, val_df = train_test_split(train_val_df, test_size=0.1111, random_state=42, stratify=train_val_df['BS대상'])

# 분할된 데이터 크기 확인
print(f"훈련 데이터: {len(train_df)}건")
print(f"검증 데이터: {len(val_df)}건")
print(f"테스트 데이터: {len(test_df)}건")

# 4. JSONL 파일 생성 함수
def create_jsonl_file(df, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            # 입력 프롬프트 생성
            prompt = (f"동: {row['동']}, 인터넷: {row['인터넷']}, TV: {row['TV']}, VoIP: {row['VoIP']}, "
                      f"PSTN: {row['PSTN']}, 시설: {row['시설']}, 시설속도: {row['시설속도']}, "
                      f"고장문의: {row['고장문의']}, 개통년도: {row['개통년도']}")
            # JSONL 형식으로 데이터 생성
            jsonl_line = {
                "messages": [
                    {"role": "system", "content": "You are a model that predicts BS대상 based on location and service data."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": f"BS대상: {row['BS대상']}"}
                ]
            }
            # 파일에 쓰기
            f.write(json.dumps(jsonl_line, ensure_ascii=False) + '\n')

# 5. JSONL 파일 생성
create_jsonl_file(train_df, './data/training_data.jsonl')
create_jsonl_file(val_df,   './data/validation_data.jsonl')
create_jsonl_file(test_df,  './data/test_data.jsonl')

print("JSONL 파일 생성 완료: training_data.jsonl, validation_data.jsonl, test_data.jsonl")

# 6. CSV 파일 저장
train_df.to_csv('./data/training_data.csv', index=False)
val_df.to_csv('./data/validation_data.csv', index=False)
test_df.to_csv('./data/test_data.csv', index=False)

print("CSV 파일 저장 완료: training_data.csv, validation_data.csv, test_data.csv")
