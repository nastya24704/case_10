import statistics
import csv
import json
import os.path
from collections import defaultdict, Counter
import datetime
import matplotlib.pyplot as plt

# ==========================
# КАТЕГОРИИ И ПРИОРИТЕТЫ
# ==========================

def all_categories() -> dict:
  categories = {
    "продукты": ["продукты", "магазин", "продуктовый", "пятёрочка",
                 "ярче", "мария", "магнит", "селф", "еда","ларёк" ],
    "кафе и рестораны": ["ресторан", "кафе", "обед", "фастфуд", "ужин", "завтрак",
                         "кофейня", "пицца", "столовая", "доставка",  "кухня" ],
    "транспорт": ["такси", "автобус", "метро", "транспорт", "самолёт"],
    "интернет и связь": ["мобильный", "интернет", "мтс", "сервис", "сети",
                         "телефон", "сервис", "билайн","мегафон", "tele2", "услуги"],
    "хобби и развлечения": ["кино", "театр", "концерт", "игры", "кинотеатр", "фильм",
                          "квест", "музыкальный", "standup", "афиша", "kassir", "читай",
                            "книжный","леонардо", "хобби", "творчество"],
    "одежда": ["одежда", "обувь", "магазин одежды", "гардероб",
               "обувной", "аксессуары", "шоурум"],
    "здоровье": ["аптека", "лекарство", "медицин", "врач",
                 "приём", "клиника", "таблетки", "мед", "доктор"],
    "спорт": ["спорт", "тренажёрка", "фитнес", "спортзал", "спортивный",
              "зал", "бассейн", "тренировка", "тренер"],
    "образование": ["курс", "учеба", "школа", "университет",
                    "репетитор", "урок", "образование"],
    "коммунальные услуги": ["комунальные","свет","коммуналка", "вода",
                            "электричество", "газ", "мусор", "отопление"],
    "депозит/инвестиции": ["клиентов", "депозит", "инвестиции","дивидент", "акция", "процент"],
    "зарплата и доходы": ["зарплата", "доход", "начисление", "стипендия",
                          "премия", "зачисление", "прибыль"],
    "погашение кредита": ["кредит", "ипотека", "погашение", "процент"],
    "подарки": ["подарок", "поздравление", "праздник", "упаковка", "шары", "подарки"],
    "налоги": ["налог", "фискальный", "налоги", "ндфл", "ндс", "пошлина"],
    "подписки": ["подписка", "подписки", "плюс", "иви", "окко", "start", "музыка", "вк"],
    "маркетплейсы": ["маркетплейс", "маркет", "wildberries", "ozon",
                            "озон", "вайлдберис"],
    "услуги": ["услуги", "красоты", "парикмахерская", "салон", "ремонт", "мастер", "клининг", ""]

  }
  return categories

def priority_categories() -> list:
  categories_priority = [
    "зарплата и доходы",
    "продукты",
    "погашение кредита",
    "депозит/инвестиции",
    "кафе и рестораны",
    "транспорт",
    "налоги",
    "интернет и связь",
    "коммунальные услуги",
    "здоровье",
    "одежда",
    "развлечения и хобби",
    "образование",
    "спорт",
    "услуги",
    "маркетплейсы",
    "подписки",
    "подарки"

  ]
  return categories_priority


# ==========================
# ИМПОРТ ДАННЫХ
# ==========================

def read_csv_file(filename: str) -> list:
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row.get('amount', 0))
                transaction = {
                    'date': row.get('date', '').strip(),
                    'amount': amount,
                    'description': row.get('description', '').strip(),
                    'type': "доход" if amount >= 0 else "расход"
                }
                data.append(transaction)
    except FileNotFoundError:
        print(f"⚠️ Файл {filename} не найден.")
    return data


def read_json_file(filename: str) -> list:
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for item in json_data.get('transactions', []):
                amount = float(item.get('amount', 0))
                data.append({
                    'date': item.get('date', '').strip(),
                    'amount': amount,
                    'description': item.get('description', '').strip(),
                    'type': "доход" if amount >= 0 else "расход"
                })
    except FileNotFoundError:
        print(f"⚠️ Файл {filename} не найден.")
    except json.JSONDecodeError:
        print(f"⚠️ Ошибка формата JSON в {filename}.")
    return data


def import_financial_data(filename: str) -> list:
    if not os.path.exists(filename):
        return []
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".csv":
        return read_csv_file(filename)
    elif ext == ".json":
        return read_json_file(filename)
    return []


# ==========================
# КАТЕГОРИЗАЦИЯ
# ==========================

def categorize_transaction_with_multiple(description: str, categories: dict, categories_priority: list) -> str:
    description_low = description.lower()
    matched_categories = []

    for category in categories_priority:
        keywords = categories.get(category, [])
        if any(keyword in description_low for keyword in keywords):
            matched_categories.append(category)


    if matched_categories:
        return matched_categories[0]
    return "другое"


def categorize_all_transactions(transactions: list) -> list:
    for transaction in transactions:
        desc = transaction.get("description", "")
        category = categorize_transaction_with_multiple(desc, all_categories(), priority_categories())
        transaction["category"] = category
    return transactions


# ==========================
# АНАЛИТИКА
# ==========================

def calculate_basic_stats(transactions: list) -> dict:
    total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    total_expense = sum(t["amount"] for t in transactions if t["amount"] < 0)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income + total_expense,
        "transaction_count": len(transactions)
    }


def calculate_by_category(transactions: list) -> dict:
    totals = defaultdict(lambda: {"sum": 0, "count": 0})
    total_expense = sum(t["amount"] for t in transactions if t["amount"] < 0)
    for t in transactions:
        cat = t.get("category", "Без категории")
        totals[cat]["sum"] += t["amount"]
        totals[cat]["count"] += 1
    for cat, val in totals.items():
        val["percent"] = (-val["sum"] / -total_expense * 100) if total_expense else 0
    return dict(totals)


def analyze_by_time(transactions: list) -> dict:
    monthly = defaultdict(lambda: {"income": 0, "expenses": 0, "categories": []})
    for t in transactions:
        try:
            d = datetime.datetime.strptime(t["date"], "%Y-%m-%d")
        except Exception:
            continue
        key = d.strftime("%Y-%m")
        if t["amount"] >= 0:
            monthly[key]["income"] += t["amount"]
        else:
            monthly[key]["expenses"] += t["amount"]
            monthly[key]["categories"].append(t.get("category", "Без категории"))
    for m, data in monthly.items():
        data["top_categories"] = Counter(data["categories"]).most_common(3)
    return dict(monthly)


def analyze_historical_spending(transactions: list) -> dict:
    monthly_spending = defaultdict(lambda: defaultdict(float))
    for t in transactions:
        if t["amount"] < 0:
            try:
                d = datetime.datetime.strptime(t["date"], "%Y-%m-%d")
            except Exception:
                continue
            month = d.strftime("%Y-%m")
            cat = t.get("category", "Без категории")
            monthly_spending[cat][month] += abs(t["amount"])
    avg_spending = {
        cat: round(statistics.mean(vals.values()), 2)
        for cat, vals in monthly_spending.items() if vals
    }
    top_cats = sorted(avg_spending.items(), key=lambda x: x[1], reverse=True)[:3]
    return {
        "average_spending": avg_spending,
        "top_categories": top_cats
    }
# ==========================
# БЮДЖЕТ И СРАВНЕНИЕ
# ==========================

def create_budget_template(analysis: dict, total_income: float = None) -> dict:
    avg_spending = analysis.get("average_spending", {})
    total_expenses = sum(avg_spending.values())
    savings = round((total_income * 0.15 if total_income else total_expenses * 0.1), 2)
    budget = {cat: {"limit": round(val * 1.05, 2), "recommended": val}
              for cat, val in avg_spending.items()}
    budget["накопления"] = {"limit": savings, "recommended": savings}
    return budget


def compare_budget_vs_actual(budget: dict, transactions: list) -> dict:
    actual = defaultdict(float)
    for t in transactions:
        if t["amount"] < 0:
            actual[t["category"]] += abs(t["amount"])
    report = {}
    for cat, data in budget.items():
        limit = data["limit"]
        spent = actual.get(cat, 0)
        diff = limit - spent
        report[cat] = {
            "limit": limit,
            "actual": spent,
            "difference": diff,
            "status": "✅ В пределах бюджета" if diff >= 0 else "⚠️ Превышен бюджет"
        }
    return report


# ==========================
# ВИЗУАЛИЗАЦИЯ
# ==========================

def visualize_financial_data(transactions: list):
    """Строит график: расходы по категориям и доходы/расходы по месяцам"""
    if not transactions:
        print("Нет данных для визуализации.")
        return

    # --- Расходы по категориям ---
    expenses = defaultdict(float)
    for t in transactions:
        if t["amount"] < 0:
            expenses[t["category"]] += abs(t["amount"])
    if expenses:
        plt.figure(figsize=(8, 5))
        plt.bar(expenses.keys(), expenses.values())
        plt.title("Расходы по категориям")
        plt.xlabel("Категория")
        plt.ylabel("Сумма, руб.")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


# ==========================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================

def smart_piggy_bank(csv_file="money.csv", json_file="transactions.json"):
    print("=" * 70)
    print("💰 УМНАЯ КОПИЛКА — личный финансовый помощник 💡")
    print("=" * 70)

    transactions = []
    if csv_file:
        transactions += import_financial_data(csv_file)
    if json_file:
        transactions += import_financial_data(json_file)

    if not transactions:
        print("❌ Нет данных для анализа.")
        return

    transactions = categorize_all_transactions(transactions)

    stats = calculate_basic_stats(transactions)
    categories_stats = calculate_by_category(transactions)
    timeline = analyze_by_time(transactions)
    analysis = analyze_historical_spending(transactions)
    budget = create_budget_template(analysis, stats["total_income"])
    comparison = compare_budget_vs_actual(budget, transactions)

    # --- ОТЧЁТ ---
    print("\n=== ФИНАНСОВЫЙ ОТЧЁТ ===")
    print(f"💰 Доходы: {stats['total_income']:.2f}")
    print(f"💸 Расходы: {abs(stats['total_expense']):.2f}")
    print(f"⚖️ Баланс: {stats['balance']:.2f}")

    print("\n📊 Расходы по категориям:")
    for cat, data in categories_stats.items():
        print(f"  {cat}: {abs(data['sum']):.2f} руб. ({data['percent']:.1f}%)")

    print("\n📅 Анализ по месяцам:")
    for month, data in timeline.items():
        top = ", ".join([f"{c} ({n})" for c, n in data["top_categories"]])
        print(f"  {month}: доход {data['income']:.2f} | расход {abs(data['expenses']):.2f} → топ: {top}")

    print("\n🎯 РЕКОМЕНДАЦИИ:")
    for cat, val in analysis["top_categories"]:
        print(f"  🔸 {cat}: {val:.2f} руб. в среднем")

    print("\n📋 СРАВНЕНИЕ С БЮДЖЕТОМ:")
    for cat, info in comparison.items():
        print(f"  {cat}: потрачено {info['actual']:.2f} / лимит {info['limit']:.2f} → {info['status']}")

    print("\n✅ Анализ завершён успешно!\n")

    # Визуализация
    visualize_financial_data(transactions)


if __name__ == "__main__":
    smart_piggy_bank()
