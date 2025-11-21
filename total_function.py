import pandas as pd
import numpy as np

# -------------------------------------------------------------
# ⚠️ 사용자 정의 변수 (확정된 컬럼명 및 파일명)
# -------------------------------------------------------------
FILE_NAME_MSW = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
COL_SUM = 'SUM'
COL_TIME_MSW = 'Year and month'
OUTPUT_FILE_NAME = "생활쓰레기_년별_평균_발생량.csv"
# -------------------------------------------------------------

# 1. 데이터 로드 및 클리닝
try:
    # 1-1. 생활쓰레기 (MSW) 데이터 로드 (UTF-8 인코딩)
    df_msw = pd.read_csv(FILE_NAME_MSW, encoding='utf-8')

    # 1-2. SUM 컬럼 클리닝 및 숫자 변환
    # (문자, 공백 등 제거 후 to_numeric)
    df_msw[COL_SUM] = df_msw[COL_SUM].astype(str).str.replace(r'[^\d\.]', '', regex=True)
    df_msw[COL_SUM] = pd.to_numeric(df_msw[COL_SUM], errors='coerce')

    # 1-3. 시간 컬럼 클리닝 및 년도 추출
    df_msw[COL_TIME_MSW] = df_msw[COL_TIME_MSW].astype(str).str.replace(r'[^\w-]', '', regex=True)
    df_msw['Year'] = pd.to_datetime(df_msw[COL_TIME_MSW], format='%b-%y', errors='coerce').dt.year

    # NaN 값 제거
    df_msw.dropna(subset=['Year', COL_SUM], inplace=True)

except Exception as e:
    print(f"데이터 로드 및 전처리 중 오류가 발생했습니다: {e}")
    exit()

# 2. 년별 평균량 계산
# 년도별로 그룹화하여 SUM의 평균을 계산
df_yearly_avg = df_msw.groupby('Year')[COL_SUM].mean().reset_index()
df_yearly_avg.rename(columns={COL_SUM: '평균_생활쓰레기_발생량'}, inplace=True)
df_yearly_avg['평균_생활쓰레기_발생량'] = df_yearly_avg['평균_생활쓰레기_발생량'].round(2)

print("년별 평균 생활쓰레기 발생량 계산 결과:")
print(df_yearly_avg.to_markdown(index=False, numalign="left", stralign="left"))

# 3. 새로운 CSV 파일로 저장
df_yearly_avg.to_csv(OUTPUT_FILE_NAME, index=False, encoding='utf-8-sig')

print(f"\n새로운 CSV 파일이 성공적으로 생성되었습니다: {OUTPUT_FILE_NAME}")