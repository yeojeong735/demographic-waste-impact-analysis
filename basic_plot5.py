import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 파일 이름 정의
file_name = "./data/서울특별시 종로구_음식물류폐기물 및 재활용품 발생량.csv"

try:
    # 널리 사용되는 나눔고딕으로 설정 (설치 필요)
    plt.rcParams['font.family'] = 'NanumGothic'
    # 폰트가 없으면 'Malgun Gothic' (Windows 기본 폰트)으로 시도
    if 'NanumGothic' not in [f.name for f in fm.fontManager.ttflist]:
        plt.rcParams['font.family'] = 'Malgun Gothic'
except:
    # 모든 설정이 실패할 경우를 대비 (최소한의 오류 회피)
    pass

# 마이너스 기호 깨짐 방지 설정 (폰트 설정 후 필수)
plt.rcParams['axes.unicode_minus'] = False
# =======================================================

# 1. 데이터 로드 및 컬럼 이름 정리
df = pd.read_csv(file_name)
df.columns = ['Month_Year', 'Food_Waste', 'Recycled_Waste']

# 2. 'Month_Year' 컬럼을 Datetime 객체로 변환하고 인덱스로 설정
df['Date'] = pd.to_datetime(df['Month_Year'], errors='coerce')
df = df.dropna(subset=['Date'])
df.set_index('Date', inplace=True)

# 3. 쓰레기 발생량 컬럼을 숫자형으로 변환
df['Food_Waste'] = pd.to_numeric(df['Food_Waste'], errors='coerce')
df['Recycled_Waste'] = pd.to_numeric(df['Recycled_Waste'], errors='coerce')

# 4. 꺾은선 그래프 생성
plt.figure(figsize=(12, 6))

# 그래프 플롯
plt.plot(
    df.index,
    df['Food_Waste'],
    label='음식물 쓰레기 (Food Waste)',
    marker='o',
    markersize=4,
    color='red',
)
plt.plot(
    df.index,
    df['Recycled_Waste'],
    label='재활용 쓰레기 (Recycled Waste)',
    marker='x',
    markersize=4,
    color='green',
)

# 5. 그래프 포맷팅
plt.title('종로구 월별 음식물 및 재활용 쓰레기 발생량 변화', fontsize=15)
plt.xlabel('기간', fontsize=12)
plt.ylabel('발생량 (톤)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# 그래프 저장
plt.show()
plt.tight_layout()
# plt.savefig('월별_음식물_재활용_쓰레기_변화_그래프_한글수정.png')
