import twstock
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_realtime_data(stock_id):
    try:
        stock = twstock.realtime.get(stock_id)

        # 防止API回傳None或錯誤資料
        if not stock or not stock.get('success', False):
            return None

        data = stock.get('realtime', {})
        info = stock.get('info', {})

        # 防止缺少必要欄位
        if not data or not info:
            return None

        return {
            'name': info.get('name', '未知公司'),
            'open': data.get('open', '-'),
            'high': data.get('high', '-'),
            'low': data.get('low', '-'),
            'latest_trade_price': data.get('latest_trade_price', '-'),
            'time': data.get('time', '-')
        }
    except Exception as e:
        print(f"[ERROR] get_realtime_data failed: {e}")
        return None

def get_kline_data(stock_id, days=2):
    try:
        stock = twstock.Stock(stock_id)
        data = stock.fetch_from(datetime.now().year - 1, 1)

        if not data:
            return []
        return data[-days:]
    except Exception as e:
        print(f"[ERROR] get_kline_data failed: {e}")
        return []

def fetch_news(stock_id):
    try:
        url = f"https://tw.stock.yahoo.com/quote/{stock_id}.TW"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        news_blocks = soup.select('li[class*="js-stream-content"] a')

        news = []
        for a in news_blocks[:5]:  # 只取最新5則新聞
            title = a.get_text(strip=True)
            link = a.get('href')
            if link and not link.startswith('http'):
                link = f"https://tw.stock.yahoo.com{link}"
            news.append({'title': title, 'link': link})

        return news
    except Exception as e:
        print(f"[ERROR] fetch_news failed: {e}")
        return []
