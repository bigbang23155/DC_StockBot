import json
import os
from datetime import datetime

DATA_FOLDER = "data"

# 確保資料夾存在
os.makedirs(DATA_FOLDER, exist_ok=True)

def save_alert(user_id, stock_id, price):
    path = os.path.join(DATA_FOLDER, "alerts.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            alerts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = {}

    alerts.setdefault(str(user_id), {})[stock_id] = price

    with open(path, "w", encoding="utf-8") as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)

def save_history(user_id, stock_id, price):
    path = os.path.join(DATA_FOLDER, "history.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = {}

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "price": price
    }
    history.setdefault(str(user_id), {}).setdefault(stock_id, []).append(entry)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history(user_id, stock_id):
    path = os.path.join(DATA_FOLDER, "history.json")
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
        return history.get(str(user_id), {}).get(stock_id, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_to_portfolio(user_id, stock_id, cost):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            portfolio = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        portfolio = {}

    portfolio.setdefault(str(user_id), []).append({
        "stock_id": stock_id,
        "cost": cost
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

def remove_from_portfolio(user_id, stock_id):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            portfolio = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    user_portfolio = portfolio.get(str(user_id), [])
    portfolio[str(user_id)] = [item for item in user_portfolio if item["stock_id"] != stock_id]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

def view_portfolio(user_id):
    path = os.path.join(DATA_FOLDER, "portfolio.json")
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            portfolio = json.load(f)
        return portfolio.get(str(user_id), [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
