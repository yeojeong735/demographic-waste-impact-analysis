# 1인 가구 vs. 쓰레기 발생량 상관관계 산점도 코드

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress  # 회귀선 계산을 위해 추가

waste_file = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
single_household_file = "./data/1인가구(연령별)_종로구.csv"

waste_column = 'SUM'
time_column = 'Year and month of import'
# -------------------------------------------------------------
# 1. 데이터 로드 및 전처리 (이전 성공 로직 통합)
# -------------------------------------------------------------

try:
    # 1-1. 쓰레기 데이터 로드 및 년도별 총합 계산
    df_waste = pd.read_csv(waste_file, encoding='utf-8')
    df_waste['날짜'] = pd.to_datetime(df_waste[time_column], format='%b-%y', errors='coerce')
    df_waste.dropna(subset=['날짜'], inplace=True)
    df_waste['년도'] = df_waste['날짜'].dt.year
    annual_waste = df_waste.groupby('년도')[waste_column].sum().reset_index()
    annual_waste.rename(columns={waste_column: '총_쓰레기_발생량'}, inplace=True)

    # 1-2. 1인 가구 데이터 로드 및 년도별 총합 추출
    df_raw = pd.read_csv(single_household_file, encoding='utf-8-sig', header=None)
    total_count_indices = [3, 19, 35, 51, 67, 83]
    years = [2024, 2023, 2022, 2021, 2020, 2019]
    df_raw.columns = df_raw.iloc[2]
    df_data = df_raw.iloc[3:]
    df_total_household = df_data[(df_data['자치구별(2)'] == '종로구') & (df_data['성별(1)'] == '계')]
    counts = df_total_household.iloc[0, total_count_indices].values
    annual_household = pd.DataFrame({'년도': years, '총_1인가구수': counts})
    annual_household['총_1인가구수'] = pd.to_numeric(annual_household['총_1인가구수'], errors='coerce').fillna(0).astype(int)
    annual_household = annual_household.sort_values('년도')

    # 1-3. 년도별 데이터 병합
    df_merged = pd.merge(annual_waste, annual_household, on='년도', how='inner')

    # 1-4. 상관관계 계산
    correlation = df_merged['총_쓰레기_발생량'].corr(df_merged['총_1인가구수'])

except Exception as e:
    print(f"데이터 로드 및 처리 중 오류 발생: {e}")
    exit()

print("데이터 병합 및 상관관계 계산 완료.")
print(f"계산된 상관계수 (r): {correlation:.4f}")

# -------------------------------------------------------------
# 2. 시각화: 산점도 및 회귀선 추가
# -------------------------------------------------------------

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# X, Y 변수 설정
X = df_merged['총_1인가구수']
Y = df_merged['총_쓰레기_발생량']

# 2-1. 산점도 그리기
ax.scatter(X, Y, color='tab:red', s=100, alpha=0.8, label='관측치')

# 2-2. 회귀선 추가 (가설 검증 시 시각적 보조 자료)
# 선형 회귀 분석 수행 (기울기(slope), 절편(intercept))
slope, intercept, r_value, p_value, std_err = linregress(X, Y)
ax.plot(X, intercept + slope * X, color='tab:blue', linestyle='--',
        label=f'회귀선 (r={correlation:.2f})')

# 2-3. 데이터 포인트에 년도 레이블 추가
for i, row in df_merged.iterrows():
    ax.text(row['총_1인가구수'], row['총_쓰레기_발생량'], f"'{row['년도'] % 100:02f}",
            ha='right', va='bottom', fontsize=9, color='gray')

# 2-4. 제목 및 레이블 설정
ax.set_title(f'1인 가구 수 vs 쓰레기 발생량 관계 (상관계수 r={correlation:.4f})', fontsize=16, pad=15)
ax.set_xlabel('총 1인 가구 수 (가구)', fontsize=12)
ax.set_ylabel(f'총 쓰레기 발생량 ({waste_column})', fontsize=12)
ax.ticklabel_format(style='plain', axis='x')
ax.ticklabel_format(style='plain', axis='y')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()