import pandas as pd

file_name = "./data/서울특별시 종로구_생활쓰레기 월별 발생량.csv"

# 1. 파일 로드 (헤더는 그대로 사용)
df = pd.read_csv(file_name)

# 2. 원본 컬럼 이름 변수 지정 (길지만 정확합니다)
DATE_COLUMN = 'Year and month'
WASTE_COLUMN = 'SUM'

# 3. 날짜 형식 지정 및 연도 추출
# 'Jan-19' 형태의 원본 파일에 맞게 format='%b-%y'를 다시 사용합니다.
df['Date'] = pd.to_datetime(
        df[DATE_COLUMN],
        format='%b-%y',
        errors='coerce'
    )
# df['Year'] = df['Date'].dt.year

# 4. 연도별 평균 계산 (SUM 컬럼 사용)
annual_average_waste = df.groupby('Date')[WASTE_COLUMN].mean().reset_index()

# 5. 최종 결과 컬럼 이름 변경
annual_average_waste.columns = ['년도', '년_평균_생활쓰레기_발생량']

# 6. 결과를 새로운 CSV 파일로 저장
output_file_name = "./data/서울특별시 종로구_년_평균_생활쓰레기_발생량.csv"
# annual_average_waste.to_csv(output_file_name, index=False, encoding='utf-8-sig')

print("\n--- 최종 계산된 년 평균 생활쓰레기 발생량 ---")
print(annual_average_waste)
print(f"\n파일이 '{output_file_name}'으로 성공적으로 저장되었습니다.")