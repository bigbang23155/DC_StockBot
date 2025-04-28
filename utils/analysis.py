import twstock

def analyze_stock(stock_id):
    stock = twstock.Stock(stock_id)
    prices = stock.price[-20:]  # 最近20天的收盤價
    if len(prices) < 20:
        return "資料不足", "資料不足，無法分析"

    ma5 = sum(prices[-5:]) / 5
    ma10 = sum(prices[-10:]) / 10
    ma20 = sum(prices[-20:]) / 20
    current = prices[-1]

    ma_analysis = f"現價：{current} 元\nMA5：{round(ma5,2)}\nMA10：{round(ma10,2)}\nMA20：{round(ma20,2)}"
    
    # 巴菲特邏輯建議（簡單版）
    if current > ma5 > ma10 > ma20:
        buffett_suggestion = "目前處於強勢多頭排列，建議觀察拉回或持有。"
    elif current < ma5 < ma10 < ma20:
        buffett_suggestion = "目前處於弱勢空頭排列，建議保守觀望或考慮減碼。"
    else:
        buffett_suggestion = "目前走勢盤整，建議觀察量能與後續方向。"

    return ma_analysis, buffett_suggestion
