# 서초동, 반포동 등 특정 동에 대해 여러 입력을 CSV로 만들어 일괄 예측하기
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

# 예측 입력 CSV
predict_df = pd.read_csv("predict_input.csv")
predictions = []

for _, row in predict_df.iterrows():
    prompt = f"동: {row['동']}, 인터넷: {row['인터넷']}, TV: {row['TV']}, VoIP: {row['VoIP']}, PSTN: {row['PSTN']}, 시설: {row['시설']}, 시설속도: {row['시설속도']}, 고장문의: {row['고장문의']}, 개통년도: {row['개통년도']}"
    response = client.chat.completions.create(
        model="your_fine_tuned_model_id",
        messages=[
            {"role": "system", "content": "You are a model that predicts BS대상 based on location and service data."},
            {"role": "user", "content": prompt}
        ]
    )
    predictions.append(response.choices[0].message.content)

predict_df['예측_BS대상'] = predictions
predict_df.to_csv("predictions.csv", index=False)


# 성능 평가를 위한 코드
test_df = pd.read_csv("test_data.csv")
true_labels = test_df['BS대상']
predicted_labels = predict_df['예측_BS대상'].str.replace("BS대상: ", "")

print("Accuracy:", accuracy_score(true_labels, predicted_labels))
print("F1-score:", f1_score(true_labels, predicted_labels, average='weighted'))

