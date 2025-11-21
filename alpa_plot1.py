# 1인 가구수와 쓰레기 발생량 상환 분석

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

waste_file = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
single_household_file = "./data/1인가구(연령별)_종로구.csv"

waste_column = 'SUM'
time_column = 'Year and month of import'

# -------------------------------------------------------------
# 1. 데이터 로드 및 전처리
# -------------------------------------------------------------

# 1-1. 쓰레기 데이터 로드 및 년도별 총합 계산
try:
    df_waste = pd.read_csv(waste_file, encoding='utf-8')

    # 날짜 파싱 (이전의 성공 로직 사용)
    df_waste['날짜'] = pd.to_datetime(
        df_waste[time_column],
        format='%b-%y',
        errors='coerce'
    )
    df_waste.dropna(subset=['날짜'], inplace=True)
    df_waste['년도'] = df_waste['날짜'].dt.year

    # 년도별 쓰레기 총 발생량 집계
    annual_waste = df_waste.groupby('년도')[waste_column].sum().reset_index()
    annual_waste.rename(columns={waste_column: '총_쓰레기_발생량'}, inplace=True)

except Exception as e:
    print(f"쓰레기 데이터 로드 및 처리 중 오류 발생: {e}")
    exit()


# 1-2. 1인 가구 데이터 로드 및 년도별 총합 추출 (이전의 성공 로직 사용)
try:
    df_raw = pd.read_csv(single_household_file, encoding='utf-8-sig', header=None)

    # 총합 인덱스 및 년도 지정 (이전 분석에서 확정된 인덱스)
    total_count_indices = [3, 19, 35, 51, 67, 83]
    years = [2024, 2023, 2022, 2021, 2020, 2019]

    # 데이터 추출 및 필터링 (복잡한 CSV 구조 처리)
    df_raw.columns = df_raw.iloc[2]
    df_data = df_raw.iloc[3:]
    df_total_household = df_data[
        (df_data['자치구별(2)'] == '종로구') &
        (df_data['성별(1)'] == '계')
        ]

    counts = df_total_household.iloc[0, total_count_indices].values

    annual_household = pd.DataFrame({
        '년도': years,
        '총_1인가구수': counts
    })

    annual_household['총_1인가구수'] = pd.to_numeric(
        annual_household['총_1인가구수'], errors='coerce'
    ).fillna(0).astype(int)
    annual_household = annual_household.sort_values('년도')

except Exception as e:
    print(f"1인 가구 데이터 로드 및 처리 중 오류 발생: {e}")
    exit()

# -------------------------------------------------------------
# 2. 데이터 병합 및 상관관계 분석
# -------------------------------------------------------------

# 년도별 데이터 병합
df_merged = pd.merge(annual_waste, annual_household, on='년도', how='inner')

# 상관관계 계산
correlation = df_merged['총_쓰레기_발생량'].corr(df_merged['총_1인가구수'])

print("년도별 쓰레기 발생량 vs 1인 가구 수 데이터 (2019~2024):")
print(df_merged.to_markdown(index=False, numalign="left", stralign="left"))
print(f"\n상관계수 (Correlation): {correlation:.4f}")

# -------------------------------------------------------------
# 3. 시각화: 이중 축 선 그래프 (추세 비교)
# -------------------------------------------------------------

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax1 = plt.subplots(figsize=(10, 6))
plt.title('1인 가구 증가 vs 쓰레기 발생량 추세 비교', fontsize=16, pad=15)

# 3-1. 첫 번째 축 (총 1인 가구 수) - 보라색
ax1.plot(df_merged['년도'], df_merged['총_1인가구수'], marker='o', linestyle='-', color='tab:purple', label='총 1인 가구 수')
ax1.set_xlabel('년도', fontsize=12)
ax1.set_ylabel('총 1인 가구 수 (가구)', fontsize=12, color='tab:purple')
ax1.tick_params(axis='y', labelcolor='tab:purple')
ax1.set_xticks(df_merged['년도'])
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.ticklabel_format(style='plain', axis='y')

# 3-2. 두 번째 축 (총 쓰레기 발생량) - 파란색
ax2 = ax1.twinx()
ax2.plot(df_merged['년도'], df_merged['총_쓰레기_발생량'], marker='s', linestyle='--', color='tab:blue', label='총 쓰레기 발생량')
ax2.set_ylabel(f'총 쓰레기 발생량 ({waste_column})', fontsize=12, color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.ticklabel_format(style='plain', axis='y')

# 3-3. 레이블 및 범례
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.9))
plt.tight_layout()
plt.show()
plt.close()


print(f"상관계수가 {correlation:.4f}로 계산되었습니다. 양의 값이 1에 가까울수록 두 변수가 함께 증가하는 경향이 강함을 의미합니다.")