import json
import os
from datetime import datetime

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_alert(user_id, stock_id, price):
    path = os.path.join(DATA_FOLDER, "alerts.json")
    alerts = _read_json(path)
    alerts.setdefault(str(user_id), {})[stock_id] = price
    _write_json(path, alerts)

def save_history(user_id, stock_id, price):
    path = os.path.join(DATA_FOLDER, "history.json")
    history = _read_json(path)
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "price": price
    }
    history.setdefault(str(user_id), {}).setdefault(stock_id, []).append(entry)
    _write_json(path, history)

def load_history(user_id, stock_id):
    path = os.path.join(DATA_FOLDER, "history.json")
    history = _read_json(path)
    return history.get(str(user_id), {}).get(stock_id, [])

def add_to_portfolio(user_id, stock_id, cost):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    portfolio = _read_json(path)
    user_key = str(user_id)

    if user_key not in portfolio:
        portfolio[user_key] = []

    for item in portfolio[user_key]:
        if item["stock_id"] == stock_id:
            item["cost"] += cost
            break
    else:
        portfolio[user_key].append({
            "stock_id": stock_id,
            "cost": cost,
            "type": "ETF" if is_etf(stock_id) else "Stock"
        })

    _write_json(path, portfolio)

def remove_from_portfolio(user_id, stock_id):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    portfolio = _read_json(path)
    user_key = str(user_id)

    if user_key in portfolio:
        portfolio[user_key] = [item for item in portfolio[user_key] if item["stock_id"] != stock_id]
        _write_json(path, portfolio)

def view_portfolio(user_id):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    portfolio = _read_json(path)
    return portfolio.get(str(user_id), [])

def view_stocks(user_id):
    return [item for item in view_portfolio(user_id) if item.get("type") != "ETF"]

def view_etfs(user_id):
    return [item for item in view_portfolio(user_id) if item.get("type") == "ETF"]

def is_etf(stock_id):
    """
    ETF 判斷邏輯：
    - 可依照實際 ETF 清單或編碼規則自定
    - 簡單範例：開頭為 0 開頭、或為已知 ETF 清單
    """
    etf_prefixes = ("0", "00", "007", "0050", "0056", "006208", "00878")
    return any(stock_id.startswith(p) for p in etf_prefixes)

def load_alerts():
    path = os.path.join(DATA_FOLDER, "alerts.json")
    return _read_json(path)
