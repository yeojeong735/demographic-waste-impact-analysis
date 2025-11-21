import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# ⚠️ 사용자 정의 변수 (확정된 컬럼명 및 파일명)
# -------------------------------------------------------------
FILE_NAME_MSW = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
FILE_NAME_FR = "./data/서울특별시 종로구_음식물류폐기물 및 재활용품 발생량.csv"

COL_SUM = 'SUM'
COL_FOOD = 'Food Waste'
COL_RECYCLE = 'Recycled Waste'
COL_TIME_MSW = 'Year and month'
COL_TIME_FR = 'Year and month'
TARGET_YEAR = 2019
ROWS_FOR_2019 = 12+1
# -------------------------------------------------------------

# 1. 각 파일을 년도별로 합산 (Aggregation First Strategy)
try:
    # 1-1. 생활쓰레기 (MSW) 데이터 로드 및 년도별 합산
    df_msw = pd.read_csv(FILE_NAME_MSW, encoding='utf-8')

    # SUM 및 Time 컬럼 클리닝 및 파싱
    df_msw[COL_SUM] = df_msw[COL_SUM].astype(str).str.replace(r'[^\d\.]', '', regex=True)
    df_msw[COL_TIME_MSW] = df_msw[COL_TIME_MSW].astype(str).str.replace(r'[^\w-]', '', regex=True)

    df_msw['Year'] = pd.to_datetime(df_msw[COL_TIME_MSW], format='%b-%y', errors='coerce').dt.year
    df_msw[COL_SUM] = pd.to_numeric(df_msw[COL_SUM], errors='coerce')
    df_msw.dropna(subset=['Year', COL_SUM], inplace=True)
    annual_msw = df_msw.groupby('Year')[COL_SUM].sum().reset_index()

    # 1-2. 음식물/재활용 (F&R) 데이터 로드 및 년도별 합산
    df_fr = pd.read_csv(FILE_NAME_FR, encoding='utf-8-sig')

    # Time 컬럼 클리닝 및 파싱
    df_fr[COL_TIME_FR] = df_fr[COL_TIME_FR].astype(str).str.replace(r'[^\w-]', '', regex=True)
    df_fr['Year'] = pd.to_datetime(df_fr[COL_TIME_FR]).dt.year

    df_fr[COL_FOOD] = pd.to_numeric(df_fr[COL_FOOD], errors='coerce')
    df_fr[COL_RECYCLE] = pd.to_numeric(df_fr[COL_RECYCLE], errors='coerce')
    df_fr.dropna(subset=['Year', COL_FOOD, COL_RECYCLE], inplace=True)
    annual_fr = df_fr.groupby('Year')[[COL_FOOD, COL_RECYCLE]].sum().reset_index()

    # 1-3. 년도별 합산 데이터 병합 (Year 기준)
    # 🌟 FIX: annual_msw와 annual_fr의 merge 시 불필요한 dropna 제거
    df_annual_merged = pd.merge(
        annual_msw,
        annual_fr,
        on='Year',
        how='inner'
    )

except Exception as e:
    print(f"❌ 데이터 로드 및 년도별 합산 중 최종 오류 발생: {e}")
    exit()

# 2. 2019년 데이터 필터링 및 총량 집계
df_target = df_annual_merged[df_annual_merged['Year'] == TARGET_YEAR].copy()

if df_target.empty:
    print(f"❌ {TARGET_YEAR}년 데이터가 두 파일 모두에 존재하지 않습니다. 모든 클리닝을 거쳤음에도 데이터가 없습니다. 원본 파일을 확인해 주세요.")
    exit()

# 3. 파이 차트 값 계산
T_Total = df_target[COL_SUM].iloc[0]
T_Food = df_target[COL_FOOD].iloc[0]
T_Recycle = df_target[COL_RECYCLE].iloc[0]
T_Other = T_Total - T_Food - T_Recycle

# T_Other가 음수일 경우 0으로 처리
T_Other = max(0, T_Other)

if T_Total <= 0:
    print("❌ 2019년 총 쓰레기 발생량이 0 이하입니다. 데이터를 확인해 주세요.")
    exit()

# 4. 파이 차트 데이터 준비
labels = ['음식물류 폐기물', '재활용품', '기타/잔재물']
sizes = [T_Food, T_Recycle, T_Other]
colors = ['#ff9999', '#66b3ff', '#99ff99']

# 5. 시각화: 파이 차트
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 8))


# 퍼센트 텍스트 포맷 함수 (총 톤수도 함께 표시)
def func(pct, allvals):
    absolute = int(np.round(pct / 100. * np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:,.0f} 톤)"


ax.pie(sizes, autopct=lambda pct: func(pct, sizes), startangle=90, colors=colors,
       wedgeprops={'edgecolor': 'black', 'linewidth': 0.5},
       labels=labels, textprops={'fontsize': 12})

ax.set_title(f'🗑️ 종로구 생활쓰레기 성상 비율 ({TARGET_YEAR}년 총합)', fontsize=16, pad=20)
ax.axis('equal')

plt.tight_layout()
plt.show()