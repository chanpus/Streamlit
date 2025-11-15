import streamlit as st
import pandas as pd

st.set_page_config(page_title="투자형 이벤트 프로토타입", layout="centered")

# -------------------
# 설정값
# -------------------
ITEMS = ["상품A", "상품B", "상품C"]
TOTAL_STEPS = 30  # 0~30 : 총 31개 시세 필요

# 여기서 3개 상품의 가격 흐름을 각각 원하는 대로 넣어라
PRICE_LISTS = {
    "상품A": [
        1000, 1020, 1010, 1030, 980, 960, 970, 990, 1010, 1050,
        1080, 1070, 1090, 1110, 1100, 1080, 1060, 1070, 1090, 1120,
        1130, 1120, 1140, 1160, 1150, 1130, 1100, 1080, 1070, 1050, 1040
    ],
    "상품B": [
        800, 820, 830, 810, 790, 780, 800, 820, 830, 840,
        860, 870, 850, 840, 835, 830, 820, 810, 800, 780,
        760, 750, 760, 780, 800, 820, 830, 810, 800, 780, 770
    ],
    "상품C": [
        500, 520, 540, 560, 580, 600, 620, 640, 660, 680,
        690, 700, 710, 720, 730, 740, 760, 780, 800, 820,
        840, 860, 880, 900, 920, 940, 960, 980, 1000, 1010, 1020
    ]
}

# 길이 체크
for item in ITEMS:
    if len(PRICE_LISTS[item]) != TOTAL_STEPS + 1:
        st.error(f"{item} 가격 리스트 길이가 TOTAL_STEPS+1 와 다릅니다.")
        st.stop()

# 힌트 리스트
HINT_LIST = [
    "힌트 1: 초반은 비교적 안정적입니다.",
    "힌트 2: 중반부에 단기 반등이 있을 수 있습니다.",
    "힌트 3: 변동성이 증가합니다.",
    "힌트 4: 후반부에 큰 변동 가능성이 있습니다.",
    "힌트 5: 안정화 구간 진입.",
    "힌트 6: 마지막 구간입니다. 수익 실현을 고려하세요."
]

# -------------------
# 세션 상태 초기화
# -------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "money" not in st.session_state:
    st.session_state.money = 10000

if "holdings" not in st.session_state:
    st.session_state.holdings = {
        item: {"qty": 0, "total_cost": 0.0} for item in ITEMS
    }

if "price_histories" not in st.session_state:
    st.session_state.price_histories = {
        item: [PRICE_LISTS[item][0]] for item in ITEMS
    }

if "current_hint" not in st.session_state:
    st.session_state.current_hint = ""

if "trades" not in st.session_state:
    st.session_state.trades = []



st.title("투자형 이벤트 시스템 프로토타입 (상품 3종, 독립 가격)")

# -------------------
# 초기화 버튼
# -------------------
if st.button("페이지 정보 초기화"):
    st.session_state.step = 0
    st.session_state.money = 10000
    st.session_state.holdings = {
        item: {"qty": 0, "total_cost": 0.0} for item in ITEMS
    }
    st.session_state.price_histories = {
        item: [PRICE_LISTS[item][0]] for item in ITEMS
    }
    st.session_state.current_hint = ""
    st.session_state.trades = []
    current_prices = {item: PRICE_LISTS[item][0] for item in ITEMS}
    st.success("모든 정보 초기화 완료!")


# -------------------
# 거래 상품 선택
# -------------------
selected_item = st.selectbox("거래할 상품 선택", ITEMS)
current_price = current_prices[selected_item]
st.write(f"[{selected_item}] 현재가: {current_price:,} 원")

# -------------------
# 버튼 영역 (일정)
# -------------------
col1, col2, col3, col4 = st.columns(4)

# 1) 다음
with col1:
    if st.button("다음"):
        if st.session_state.step < TOTAL_STEPS:
            st.session_state.step += 1
            for item in ITEMS:
                new_price = PRICE_LISTS[item][st.session_state.step]
                st.session_state.price_histories[item].append(new_price)

# 2) 구매
with col2:
    if st.button("구매"):
        price = current_price
        if st.session_state.money >= price:
            st.session_state.money -= price
            h = st.session_state.holdings[selected_item]
            h["qty"] += 1
            h["total_cost"] += price

            st.session_state.trades.append({
                "턴": st.session_state.step,
                "유형": "매수",
                "상품": selected_item,
                "가격": price,
                "거래 후 소지금": st.session_state.money,
            })
        else:
            st.warning("소지금 부족!")

# 3) 판매
with col3:
    if st.button("판매"):
        h = st.session_state.holdings[selected_item]
        if h["qty"] > 0:
            avg_cost = h["total_cost"] / h["qty"]
            h["qty"] -= 1
            h["total_cost"] -= avg_cost

            st.session_state.money += current_price

            st.session_state.trades.append({
                "턴": st.session_state.step,
                "유형": "매도",
                "상품": selected_item,
                "가격": current_price,
                "거래 후 소지금": st.session_state.money,
            })
        else:
            st.warning("보유 수량 없음!")

# 4) 힌트
with col4:
    if st.button("힌트 보기"):
        if st.session_state.step % 5 == 0 and st.session_state.step > 0:
            idx = (st.session_state.step // 5) - 1
            st.session_state.current_hint = HINT_LIST[idx]
        else:
            st.session_state.current_hint = "현재 턴은 힌트 구간이 아닙니다."

st.write("---")

# -------------------
# 힌트 출력
# -------------------
if st.session_state.current_hint:
    st.info(st.session_state.current_hint)

# 현재 가격 계산
current_prices = {
    item: PRICE_LISTS[item][st.session_state.step] for item in ITEMS
}
# -------------------
# 현재 상태
# -------------------
st.subheader(f"현재 턴: {st.session_state.step} / {TOTAL_STEPS}")
st.write(f"소지금: {st.session_state.money:,} 원")

price_rows = []
for item in ITEMS:
    price_rows.append({
        "상품": item,
        "현재 가격": current_prices[item],
    })

st.table(pd.DataFrame(price_rows))

st.write("---")



# -------------------
# 가격 그래프 (3종 각각 독립)
# -------------------
st.write("가격 변동 그래프")
chart_df = pd.DataFrame(st.session_state.price_histories)
st.line_chart(chart_df)

# -------------------
# 보유 상품 상세
# -------------------
st.write("---")
st.subheader("보유 상품 현황")

rows = []
total_hold_value = 0

for item in ITEMS:
    h = st.session_state.holdings[item]
    qty = h["qty"]
    total_cost = h["total_cost"]
    cur = current_prices[item]

    if qty > 0:
        avg = total_cost / qty
        profit_abs = (cur - avg) * qty
        profit_pct = (cur / avg - 1) * 100
        value = cur * qty
    else:
        avg = 0
        profit_abs = 0
        profit_pct = 0
        value = 0

    total_hold_value += value

    rows.append({
        "상품": item,
        "보유개수": qty,
        "평균매수가": round(avg, 2),
        "현재가": cur,
        "평가액": round(value, 2),
        "손익(원)": round(profit_abs, 2),
        "손익(%)": round(profit_pct, 2)
    })

st.table(pd.DataFrame(rows))

# -------------------
# 전체 자산
# -------------------
st.write("---")
st.subheader("전체 자산 요약")

total_asset = st.session_state.money + total_hold_value

st.write(f"소지금: {st.session_state.money:,} 원")
st.write(f"보유 상품 평가액: {int(total_hold_value):,} 원")
st.write(f"총 자산: {int(total_asset):,} 원")

# -------------------
# 거래 기록
# -------------------
st.write("---")
st.subheader("거래 기록")

if len(st.session_state.trades) == 0:
    st.write("거래 내역 없음")
else:
    st.dataframe(pd.DataFrame(st.session_state.trades), use_container_width=True)

