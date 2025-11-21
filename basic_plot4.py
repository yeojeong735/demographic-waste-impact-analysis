# 20~30대 1인 가구의 변화 추세

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# 1. 데이터 로드 및 추출 (20대,30대 인구수 합산)
# -------------------------------------------------------------
file_name = "./data/1인가구(연령별)_종로구.csv"

try:
    # 1.1. 원본 CSV 로드 및 데이터 행 추출 (이전 성공 로직 사용)
    df_raw = pd.read_csv(file_name, encoding='utf-8-sig', header=None)
    df_raw.columns = df_raw.iloc[2]  # 3행(인덱스 2)의 값을 컬럼명으로 사용
    df_data = df_raw.iloc[3:].copy()

    # 1.2. 분석에 필요한 행 필터링: '종로구' & '계' (총합)
    df_filtered_row = df_data[
        (df_data['자치구별(2)'] == '종로구') &
        (df_data['성별(1)'] == '계')
        ].copy()

    # 1.3. 년도 및 컬럼 인덱스 설정
    # 각 연도별 '소계' 컬럼의 인덱스 위치를 기준으로, 20~39세 인덱스들을 추출합니다.
    # 각 연령대 그룹은 소계 인덱스 +1, +2, +3 입니다.
    block_start_indices = [3, 19, 35, 51, 67, 83]  # 2024, 2023, ..., 2019년 소계 컬럼 인덱스
    years = [2024, 2023, 2022, 2021, 2020, 2019]

    annual_20_30s_counts = []

    for start_idx in block_start_indices:
        # 추출할 컬럼 인덱스: [20~24세, 25~29세, 30~34세, 35~39세]에 해당
        indices_to_sum = [start_idx + 2, start_idx + 3, start_idx + 4, start_idx + 5]

        # 해당 연도의 세 컬럼 값을 추출하여 합산
        # .iloc[0]은 필터링된 유일한 행, indices_to_sum은 해당 컬럼 인덱스
        sum_of_group = pd.to_numeric(
            df_filtered_row.iloc[0, indices_to_sum],
            errors='coerce'
        ).sum()

        annual_20_30s_counts.append(sum_of_group)

    # 1.4. 최종 데이터프레임 생성
    df_plot = pd.DataFrame({
        '년도': years,
        '총_2030대_1인가구수': annual_20_30s_counts
    }).sort_values('년도')

    df_plot['총_2030대_1인가구수'] = df_plot['총_2030대_1인가구수'].astype(int)

except Exception as e:
    print(f"데이터 추출 중 오류가 발생했습니다. CSV 파일의 구조를 다시 확인해 주세요: {e}")
    exit()

print("2030대 1인 가구 증가 추세 분석 데이터 (2019년~2024년):")
print(df_plot.to_markdown(index=False, numalign="left", stralign="left"))

# -------------------------------------------------------------
# 2. 시각화: 장기 추세 분석 (선형 그래프)
# -------------------------------------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df_plot['년도'], df_plot['총_2030대_1인가구수'],
        marker='o', linestyle='-', color='tab:blue', linewidth=2)

ax.set_title('종로구 20~30대 1인 가구 증가 추세 (2019년~2024년)', fontsize=16, pad=15)
ax.set_xlabel('년도', fontsize=12)
ax.set_ylabel('20~30대 총 1인 가구 수 (가구)', fontsize=12)
ax.set_xticks(df_plot['년도'])
ax.ticklabel_format(style='plain', axis='y')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 데이터 레이블 추가
for i, (year, count) in df_plot[['년도', '총_2030대_1인가구수']].iterrows():
    ax.text(year, count, f'{count:,.0f}',
            ha='center', va='bottom', fontsize=10, color='tab:blue')

plt.tight_layout()
plt.show()