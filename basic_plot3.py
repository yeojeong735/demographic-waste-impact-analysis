# 장기 추세 분석 : 1인 가구 증가 추세(종로구)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# 1. 데이터 로드 및 추출 (인덱스 직접 지정)
# -------------------------------------------------------------
file_name = "./data/1인가구(연령별)_종로구.csv"
waste_column = 'SUM'
time_column = 'Year and month of import'

try:
    # 1.1. 원본 CSV 로드 (헤더 없이 로드)
    # 한글 인코딩 처리: utf-8-sig 또는 cp949 시도
    df_raw = pd.read_csv(file_name, encoding='utf-8-sig', header=None)

    # 1.2. 컬럼명 설정 및 데이터 행 추출
    df_raw.columns = df_raw.iloc[2]  # 3행(인덱스 2)의 값을 컬럼명으로 사용
    df_data = df_raw.iloc[3:].copy()  # 실제 데이터는 인덱스 3부터 시작

    # 1.3. 분석에 필요한 행 필터링: '종로구' & '계' (총합)
    df_total_household = df_data[
        (df_data['자치구별(2)'] == '종로구') &
        (df_data['성별(1)'] == '계')
        ].copy()

    # 1.4. 년도별 총합 인덱스 지정 및 추출
    # 각 년도의 총합('소계') 컬럼에 해당하는 df_raw 기준 컬럼 인덱스를 추출합니다.
    total_count_indices = [3, 19, 35, 51, 67, 83]
    years = [2024, 2023, 2022, 2021, 2020, 2019]

    # 해당 인덱스에 해당하는 데이터만 추출 (iloc[0]은 필터링된 유일한 행)
    counts = df_total_household.iloc[0, total_count_indices].values

    # 1.5. 최종 데이터프레임 생성
    df_plot = pd.DataFrame({
        '년도': years,
        '총_1인가구수': counts
    })

    # 1.6. 데이터 정리 및 변환
    df_plot['총_1인가구수'] = pd.to_numeric(
        df_plot['총_1인가구수'], errors='coerce'
    ).fillna(0).astype(int)
    df_plot = df_plot.sort_values('년도')

except Exception as e:
    print(f"데이터 로드 및 추출 중 오류가 발생했습니다: {e}")
    # 오류 발생 시 시각화 코드는 실행하지 않습니다.
    exit()

print("1인 가구 증가 추세 분석 데이터 추출 완료.")

# -------------------------------------------------------------
# 2. 시각화: 장기 추세 분석 (선형 그래프)
# -------------------------------------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df_plot['년도'], df_plot['총_1인가구수'], marker='o', linestyle='-', color='tab:purple', linewidth=2)

ax.set_title('종로구 1인 가구 증가 추세 (2019년~2024년)', fontsize=16, pad=15)
ax.set_xlabel('년도', fontsize=12)
ax.set_ylabel('총 1인 가구 수 (가구)', fontsize=12)
ax.set_xticks(df_plot['년도'])
ax.ticklabel_format(style='plain', axis='y')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 데이터 레이블 추가
for i, (year, count) in df_plot[['년도', '총_1인가구수']].iterrows():
    ax.text(year, count, f'{count:,.0f}',
            ha='center', va='bottom', fontsize=12, color='tab:red')

plt.tight_layout()
plt.show()