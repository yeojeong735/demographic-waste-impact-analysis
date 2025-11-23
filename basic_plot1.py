# 장기 추세 분석 : 년도별 쓰레기 총 발생량 집계

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FINAL_FILE_NAME = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"
WASTE_COLUMN = 'SUM'
TIME_COLUMN_FOR_PARSING = 'Year and month'
# -------------------------------------------------------------

try:
    # 데이터 로드
    df = pd.read_csv(FINAL_FILE_NAME, encoding='utf-8')

    # 날짜 파싱 및 년도 추출
    df['날짜'] = pd.to_datetime(
        df[TIME_COLUMN_FOR_PARSING],
        format='%b-%y',
        errors='coerce'
    )
    df.dropna(subset=['날짜'], inplace=True)
    df['년도'] = df['날짜'].dt.year

    # 년도별 총 발생량 및 증감률 계산
    annual_df = df.groupby('년도')[WASTE_COLUMN].sum().reset_index()
    annual_df.rename(columns={WASTE_COLUMN: '총_발생량'}, inplace=True)
    annual_df['전년_대비_증감률'] = annual_df['총_발생량'].pct_change() * 100
    annual_df['전년_대비_증감률'] = annual_df['전년_대비_증감률'].fillna(0)

    # -------------------------------------------------------------
    # 3. 시각화
    # -------------------------------------------------------------
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # 막대 그래프 (총 발생량)
    ax1.bar(annual_df['년도'].astype(str), annual_df['총_발생량'], color='tab:blue', label='총 발생량', width=0.5)
    ax1.set_xlabel('년도', fontsize=12)
    ax1.set_ylabel(f'총 발생량 ({WASTE_COLUMN})', fontsize=10, color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.ticklabel_format(style='plain', axis='y')

    # 증감률 값을 막대 위에 표시
    for i, (year, total_waste) in annual_df[['년도', '총_발생량']].iterrows():
        ax1.text(annual_df['년도'].astype(str)[i], total_waste, f'{total_waste:,.0f}',
                 ha='center', va='bottom', fontsize=9, color='tab:blue')

    # 이중 축 설정 (증감률)
    ax2 = ax1.twinx()
    ax2.plot(annual_df['년도'].astype(str), annual_df['전년_대비_증감률'], marker='o', linestyle='-', color='tab:orange',
             label='전년 대비 증감률')
    ax2.set_ylabel('전년 대비 증감률 (%)', fontsize=10, color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}%'))

    # 증감률 값을 선 위에 표시
    for i, (year, change_rate) in annual_df[['년도', '전년_대비_증감률']].iterrows():
        ax2.text(annual_df['년도'].astype(str)[i], change_rate, f'{change_rate:.0f}%',
                 ha='center', va='bottom' if change_rate >= 0 else 'top', fontsize=9, color='tab:orange')


    ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)

    # 제목 및 범례
    plt.title('년도별 생활쓰레기 총 발생량 및 전년 대비 증감률(종로구)', fontsize=16, pad=20)
    fig.legend(loc="upper left", bbox_to_anchor=(0, 0.90))

    plt.tight_layout(rect=[0, 0, 1, 0.90])


    plt.show()
except FileNotFoundError:
    print(f"\n❌ 파일을 찾을 수 없습니다: {FINAL_FILE_NAME}. 해당 파일이 실행 환경에 존재하는지 확인해 주세요.")
except Exception as e:
    print(f"\n❌ 데이터 처리 중 예상치 못한 오류가 발생했습니다: {e}")

