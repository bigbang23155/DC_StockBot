import twstock

def kline_pattern(stock_id):
    stock = twstock.Stock(stock_id)
    data = stock.fetch_31()
    if len(data) < 2:
        return "資料不足", "無法判斷"

    today = data[-1]
    yesterday = data[-2]

    open_price = today.open
    close_price = today.close
    high_price = today.high
    low_price = today.low

    # 長紅K / 長黑K / 十字線
    change_ratio = (close_price - open_price) / open_price
    if change_ratio > 0.02:
        return "長紅K", "強力買盤，收盤價遠高於開盤價"
    elif change_ratio < -0.02:
        return "長黑K", "強力賣壓，收盤價遠低於開盤價"
    elif abs(change_ratio) < 0.002:
        return "十字線", "開盤價接近收盤價，可能轉折"

    # 吞噬線（反轉型態）
    if (open_price < yesterday.close and close_price > yesterday.open):
        return "紅K吞黑K", "可能反轉向上訊號"
    if (open_price > yesterday.close and close_price < yesterday.open):
        return "黑K吞紅K", "可能反轉向下訊號"

    return "無明顯型態", "K線型態不明顯"
