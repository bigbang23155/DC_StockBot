import twstock
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_realtime_data(stock_id):
    stock = twstock.realtime.get(stock_id)
    if not stock['success']:
        return None
    data = stock['realtime']
    return {
        'name': stock['info']['name'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'latest_trade_price': data['latest_trade_price'],
        'time': data['time']
    }

def get_kline_data(stock_id, days=2):
    stock = twstock.Stock(stock_id)
    data = stock.fetch_from(datetime.now().year - 1, 1)
    return data[-days:]

def fetch_news(stock_id):
    try:
        url = f"https://tw.stock.yahoo.com/quote/{stock_id}.TW"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        news_blocks = soup.select('li[class*="js-stream-content"] a')
        news = []
        for a in news_blocks[:5]:  # 只取最新5筆
            title = a.get_text(strip=True)
            link = a.get('href')
            if link and not link.startswith('http'):
                link = f"https://tw.stock.yahoo.com{link}"
            news.append({'title': title, 'link': link})
        return news
    except Exception as e:
        print(f"抓取新聞錯誤: {e}")
        return []
