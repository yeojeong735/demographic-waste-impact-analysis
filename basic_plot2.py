# 계열성 분석 : 전체 기간의 월별 평균 발생량 집계

import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np

FINAL_FILE_NAME = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
WASTE_COLUMN: str = 'SUM'
TIME_COLUMN_FOR_PARSING = 'Year and month of import'
# -------------------------------------------------------------

# 1. 데이터 로드 및 전처리
try:
    df = pd.read_csv(FINAL_FILE_NAME, encoding='utf-8')

    # 날짜 파싱 및 월/월 이름 추출
    df['날짜'] = pd.to_datetime(
        df[TIME_COLUMN_FOR_PARSING],
        format='%b-%y',
        errors='coerce'
    )
    df.dropna(subset=['날짜'], inplace=True)
    df['월'] = df['날짜'].dt.month
    df['월_이름'] = df['월'].apply(lambda x: calendar.month_abbr[x])  # 월 약자 (Jan, Feb, ...) 사용

except Exception as e:
    print(f"데이터 로드 및 전처리 중 오류가 발생했습니다: {e}")
    exit()

# 2. 분석 1: 월별 평균 집계 (막대 그래프 데이터)
sort_order = [calendar.month_abbr[i] for i in range(1, 13)]
monthly_avg_df = df.groupby('월')[WASTE_COLUMN].mean().reset_index()
monthly_avg_df['월_이름'] = pd.Categorical(
    monthly_avg_df['월'].apply(lambda x: calendar.month_abbr[x]),
    categories=sort_order,
    ordered=True
).sort_values()
monthly_avg_df = monthly_avg_df.sort_values('월_이름')

# 3. 박스 플롯을 위한 데이터 리스트 준비
monthly_data = [df[df['월'] == i][WASTE_COLUMN].values for i in range(1, 13)]

# Setup Block 실행 후 이어서 실행
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))

plt.bar(monthly_avg_df['월_이름'], monthly_avg_df[WASTE_COLUMN], color='tab:green')
plt.title('월별 평균 생활쓰레기 발생량 (Bar Chart)', fontsize=15)
plt.xlabel('월 (Month)', fontsize=12)
plt.ylabel(f'평균 발생량 ({WASTE_COLUMN})', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ticklabel_format(style='plain', axis='y') # 지수표현식 방지

# 막대 위에 값 표시
for i, avg_waste in monthly_avg_df.iterrows():
    plt.text(i, avg_waste[WASTE_COLUMN], f'{avg_waste[WASTE_COLUMN]:,.0f}',
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()