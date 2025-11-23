import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import csv

# 파일 이름 정의
file_general_waste_avg = "./data/서울특별시 종로구_년_평균_생활쓰레기_발생량.csv"
file_food_recycled = "./data/서울특별시 종로구_음식물류폐기물 및 재활용품 발생량.csv"

# --- 1. 음식물 및 재활용 쓰레기 데이터 처리 (탭 구분자 적용) ---

try:
    # ⭐⭐ csv 모듈을 사용하여 파일의 불규칙성을 강제 해결 ⭐⭐
    clean_rows = []
    # 파일을 읽을 때 줄 끝 문자(\r\n)를 자동으로 처리하도록 newline='' 설정
    with open(file_food_recycled, 'r', encoding='utf-8', errors='ignore', newline='') as f:
        # csv.reader를 사용하여 파일 구조를 강제로 해석
        reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:  # 헤더는 건너뛰거나 따로 처리
                continue
            # 데이터는 3개 컬럼(월, 음식물, 재활용)으로 구성되어야 함
            if len(row) >= 3:
                # 불필요한 공백을 제거하고 필요한 3개 컬럼만 추가
                clean_rows.append([item.strip() for item in row[:3]])
            # 빈 행을 건너뛰는 로직

    # 깨끗해진 데이터를 Pandas DataFrame으로 변환
    df_fr = pd.DataFrame(clean_rows, columns=['Month_Year', 'Food_Waste', 'Recycled_Waste'])

    # 데이터 타입 변환 및 평균 계산
    df_fr['Food_Waste'] = pd.to_numeric(df_fr['Food_Waste'], errors='coerce')
    df_fr['Recycled_Waste'] = pd.to_numeric(df_fr['Recycled_Waste'], errors='coerce')

    df_fr['Date'] = pd.to_datetime(df_fr['Month_Year'], errors='coerce')
    df_fr['Year'] = df_fr['Date'].dt.year
    df_2019_fr = df_fr[df_fr['Year'] == 2019]
    food_waste_average = df_2019_fr['Food_Waste'].mean()
    recycled_waste_average = df_2019_fr['Recycled_Waste'].mean()

except Exception as e:
    print(f"음식물/재활용 파일 최종 처리 오류 발생: {e}")
    food_waste_average, recycled_waste_average = None, None

# --- 2. 기타 쓰레기 데이터 처리 및 IndexError 방지 ---
try:
    with open(file_general_waste_avg, 'rb') as f:
        data = f.read()
    # 2. 널 바이트(b'\x00')를 제거
    cleaned_data = data.replace(b'\x00', b'')
    # 3. 데이터 손상을 최소화하는 'latin-1'으로 디코딩
    cleaned_string = cleaned_data.decode('latin-1')
    # 인코딩 및 구분자 문제 해결 코드 유지
    df_avg = pd.read_csv(
        io.StringIO(cleaned_string),
        sep=',',
        skiprows=1,  # 헤더 건너뛰기 유지
        header=None
        # C engine이 기본값이며, universal newline mode를 지원합니다.
    )
    df_avg = df_avg.iloc[:, [0, 1]].copy()

    df_avg.columns = ['Year', 'Average_waste_total']

    # ⭐⭐ Year 컬럼을 숫자로 확실하게 변환하여 필터링 오류를 방지합니다. ⭐⭐
    df_avg['Year'] = pd.to_numeric(df_avg['Year'], errors='coerce').astype('Int64')

    # 2019년 데이터 필터링
    df_2019_avg = df_avg[df_avg['Year'] == 2019]

    # 필터링 결과가 비어있는지 확인하고 오류가 나면 처리
    if df_2019_avg.empty:
        raise ValueError("년평균 파일에서 2019년 데이터가 발견되지 않았습니다. 파일 내용을 확인해 주세요.")

    # 데이터 추출
    total_waste_average = df_2019_avg['Average_waste_total'].iloc[0]

    # 기타 쓰레기 평균 계산
    other_waste_average = total_waste_average - food_waste_average - recycled_waste_average

except Exception as e:
    print(f"데이터 처리 오류 발생: {e}")
    other_waste_average = None

# --- 3. 파이 차트 생성 ---
if all(v is not None for v in [other_waste_average, food_waste_average, recycled_waste_average]):
    data = [food_waste_average, recycled_waste_average, other_waste_average]
    labels = ['음식물 쓰레기', '재활용 쓰레기', '기타 쓰레기']

    data = [max(0, d) for d in data]

    plt.figure(figsize=(9, 9))

    plt.pie(
        data,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12, 'color': 'black'}
    )

    plt.title('2019년 종로구 폐기물 유형별 월평균 비율', fontsize=15)

    total_average = sum(data)
    legend_labels = [f'{l}: {d:.2f}톤 ({d / total_average:.1%})' for l, d in zip(labels, data)]
    plt.legend(legend_labels, title="유형 (단위: 톤/월)", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=1)

    plt.show()

    print("\n--- 2019년 폐기물 월평균 (톤/월) ---")
    print(f"음식물 쓰레기 평균: {food_waste_average:.2f}")
    print(f"재활용 쓰레기 평균: {recycled_waste_average:.2f}")
    print(f"기타 쓰레기 평균: {other_waste_average:.2f}")