import streamlit as st

st.set_page_config(page_title="투자형 이벤트 프로토타입", layout="centered")

# -------------------
# 설정값
# -------------------
TOTAL_STEPS = 30  # 총 가격 변화 횟수 (변경하려면 PRICE_LIST 길이도 같이 맞춰야 함)

# 초기가격 + 30회 변화 후 가격 = 총 31개
# 여기 숫자들을 네가 원하는 시나리오로 바꿔서 쓰면 됨
PRICE_LIST = [
    1000, 1020, 1010, 1030, 990,
    995, 1005, 1015, 1025, 1035,
    1040, 1030, 1020, 1010, 1000,
    990, 980, 970, 960, 950,
    940, 930, 920, 910, 900,
    890, 880, 870, 860, 850,
    840,
]

# 5, 10, 15, 20, 25, 30회 시점용 힌트
HINT_LIST = [
    "힌트 1: 초반은 변동폭이 크지 않습니다. 너무 서두르지 마세요.",
    "힌트 2: 이 구간에서는 단기 반등이 한 번 올 수 있습니다.",
    "힌트 3: 중반 이후에는 가격이 점점 불안정해집니다.",
    "힌트 4: 큰 하락 이후의 반등 타이밍을 노려보세요.",
    "힌트 5: 막판에는 급등보다는 완만한 회복을 기대할 수 있습니다.",
    "힌트 6: 마지막 구간입니다. 지금까지의 평균 가격을 떠올려 보세요.",
]

# PRICE_LIST 길이 체크 (버그 방지용)
if len(PRICE_LIST) != TOTAL_STEPS + 1:
    st.error("PRICE_LIST 길이가 TOTAL_STEPS + 1 과 다릅니다. 설정을 확인하세요.")
    st.stop()

# -------------------
# 세션 상태 초기화
# -------------------
if "step" not in st.session_state:
    st.session_state.step = 0          # 0 ~ TOTAL_STEPS
if "price" not in st.session_state:
    st.session_state.price = PRICE_LIST[0]
if "money" not in st.session_state:
    st.session_state.money = 10000
if "count" not in st.session_state:
    st.session_state.count = 0
if "price_history" not in st.session_state:
    st.session_state.price_history = [PRICE_LIST[0]]
if "current_hint" not in st.session_state:
    st.session_state.current_hint = ""

# -------------------
# 상단 정보
# -------------------
st.title("투자형 이벤트 시스템 프로토타입")



# -------------------
# 버튼 영역 (레이아웃 고정)
# -------------------
col1, col2, col3, col4 = st.columns(4)

# 1) 다음 (가격 변동)
with col1:
    if st.button("다음", key="btn_next"):
        # 계산기처럼 여기에서 바로 상태 업데이트
        if st.session_state.step < TOTAL_STEPS:
            st.session_state.step += 1
            st.session_state.price = PRICE_LIST[st.session_state.step]
            st.session_state.price_history.append(st.session_state.price)

# 2) 구매
with col2:
    if st.button("구매", key="btn_buy"):
        if st.session_state.money >= st.session_state.price:
            st.session_state.money -= st.session_state.price
            st.session_state.count += 1
        else:
            st.warning("소지금이 부족합니다!")

# 3) 판매
with col3:
    if st.button("판매", key="btn_sell"):
        if st.session_state.count > 0:
            st.session_state.count -= 1
            st.session_state.money += st.session_state.price
        else:
            st.warning("보유 상품이 없습니다. 판매 불가!")

# 4) 힌트 보기 (항상 버튼은 존재)
with col4:
    if st.button("힌트 보기", key="btn_hint"):
        # 현재 step이 5,10,15,20,25,30 중 하나일 때만 힌트 있음
        if 0 < st.session_state.step <= TOTAL_STEPS and st.session_state.step % 5 == 0:
            hint_index = (st.session_state.step // 5) - 1  # 5→0, 10→1 ...
            if 0 <= hint_index < len(HINT_LIST):
                st.session_state.current_hint = HINT_LIST[hint_index]
            else:
                st.session_state.current_hint = "해당 구간 힌트가 설정되어 있지 않습니다."
        else:
            st.session_state.current_hint = "지금은 볼 수 있는 힌트가 없습니다."

st.write("---")

# -------------------
# 힌트 출력
# -------------------
if st.session_state.current_hint:
    st.info(st.session_state.current_hint)




st.subheader(f"현재 가격: {st.session_state.price:,} 원")
st.write(f"가격 변화 횟수: {st.session_state.step} / {TOTAL_STEPS} 회")
st.write(f"소지금: {st.session_state.money:,} 원")
st.write(f"보유 상품 개수: {st.session_state.count} 개")

st.write("---")



# -------------------
# 가격 변동 그래프
# -------------------
st.write("가격 변동 그래프")
st.line_chart(st.session_state.price_history)
