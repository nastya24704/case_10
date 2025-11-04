import statistics
import csv
import json
import os.path
from collections import defaultdict, Counter
import datetime
import matplotlib.pyplot as plt
import local as lcl

# ==========================
# КАТЕГОРИИ И ПРИОРИТЕТЫ
# ==========================

def all_categories() -> dict:
  categories = {
    f'{lcl.PRODUCTS}': [f'{lcl.PRODUCTS}', f'{lcl.STORE}', f'{lcl.GROCERY}', f'{lcl.PETYOROCHKA}',
                 f'{lcl.YARCHE}', f'{lcl.MARIYA}', f'{lcl.MAGNIT}', f'{lcl.SELF}', f'{lcl.FOOD}',f'{lcl.STALL}' ],
    f'{lcl.CAFE_AND_RESTAURANT}': [f'{lcl.RESTAURANT}', f'{lcl.CAFE}', f'{lcl.LUNCH}', f'{lcl.FASTFOOD}', f'{lcl.DINNER}', f'{lcl.BREAKFAST}',
                         f'{lcl.CAFE}', f'{lcl.PIZZA}', f'{lcl.CANTEEN}', f'{lcl.DELIVERY}',  f'{lcl.KITCHEN}' ],
    f'{lcl.TRANSPORT}': [f'{lcl.TAXI}', f'{lcl.BUS}', f'{lcl.METRO}', f'{lcl.TRANSPORT}', f'{lcl.AIRPLANE}'],
    f'{lcl.INTERNET_AND_COMMUNICATION}': [f'{lcl.MOBILE}', f'{lcl.INTERNET}', f'{lcl.MTS}', f'{lcl.SERVICE}', f'{lcl.NETWORKS}',
                         f'{lcl.PHONE}', f'{lcl.BEELINE}',f'{lcl.MEGAFON}', "tele2", f'{lcl.SERVICES}'],
    f'{lcl.HOBBIES_AND_ENTERTAINMENT}': [f'{lcl.CINEMA}', f'{lcl.THEATER}', f'{lcl.CONCERT}', f'{lcl.GAMES}', f'{lcl.CINEMA_HALL}', f'{lcl.MOVIE}',
                          f'{lcl.QUEST}', f'{lcl.MUSICAL}', "standup", f'{lcl.POSTER}', "kassir", f'{lcl.READ}',
                            f'{lcl.BOOK}',f'{lcl.LEONARDO}', f'{lcl.HOBBY}', f'{lcl.CREATIVITY}'],
    f'{lcl.CLOTHES}': [f'{lcl.CLOTHES}', f'{lcl.SHOES}', f'{lcl.CLOTHING_STORE}', f'{lcl.WARDROBE}',
               f'{lcl.SHOE_STORE}', f'{lcl.ACCESSORIES}', f'{lcl.SHOWROOM}'],
    f'{lcl.HEALTH}': [f'{lcl.PHARMACY}', f'{lcl.MEDICINE}', f'{lcl.MEDICAL}', f'{lcl.DOCTOR}',
                 f'{lcl.APPOINTMENT}', f'{lcl.CLINIC}', f'{lcl.PILLS}', f'{lcl.MED}', f'{lcl.DOCTOR_2}'],
    f'{lcl.SPORTS}': [f'{lcl.SPORTS}', f'{lcl.GYM}', f'{lcl.FITNESS}', f'{lcl.SPORTS_HALL}', f'{lcl.ATHLETIC}',
              f'{lcl.HALL}', f'{lcl.POOL}', f'{lcl.TRAINING}', f'{lcl.COACH}'],
    f'{lcl.EDUCATION}': [f'{lcl.COURSE}', f'{lcl.STUDYING}', f'{lcl.SCHOOL}', f'{lcl.UNIVERSITY}',
                    f'{lcl.TUTOR}', f'{lcl.LESSON}', f'{lcl.EDUCATION}'],
    f'{lcl.UTILITIES}': [f'{lcl.UTILITY}',f'{lcl.LIGHT}',f'{lcl.UT}', f'{lcl.WATER}',
                            f'{lcl.ELECTRICITY}', f'{lcl.GAS}', f'{lcl.TRASH}', f'{lcl.HEATING}'],
    f'{lcl.DEPOSIT_INVESTMENTS}': [f'{lcl.CLIENTS}', f'{lcl.DEPOSIT}', f'{lcl.INVESTMENTS}',f'{lcl.DIVIDEND}', f'{lcl.SHARE}', f'{lcl.INTEREST}'],
    f'{lcl.SALARY_AND_INCOME}': [f'{lcl.SALARY}', f'{lcl.INCOME}', f'{lcl.ACCRUAL}', f'{lcl.STIPEND}',
                          f'{lcl.BONUS}', f'{lcl.CREDITING}', f'{lcl.PROFIT}'],
    f'{lcl.REPAYMENT_LOAN}': [f'{lcl.LOAN}', f'{lcl.MORTGAGE}', f'{lcl.REPAYMENT}', f'{lcl.INTEREST}'],
    f'{lcl.GIFTS}': [f'{lcl.GIFT}', f'{lcl.CONGRATULATION}', f'{lcl.HOLIDAY}', f'{lcl.WRAPPING}', f'{lcl.BALLS}', f'{lcl.GIFTS}'],
    f'{lcl.TAXES}': [f'{lcl.TAX}', f'{lcl.FISCAL}', f'{lcl.TAXES}', f'{lcl.NDFL}', f'{lcl.NDS}', f'{lcl.DUTY}'],
    f'{lcl.SUBSCRIPTIONS}': [f'{lcl.SUBSCRIPTION}', f'{lcl.SUBSCRIPTIONS}', f'{lcl.PLUS}', f'{lcl.IVI}', f'{lcl.OKKO}', "start", f'{lcl.MUSIC}', f'{lcl.VK}'],
    f'{lcl.MARKETPLACES}': [f'{lcl.MARKETPLACE}', f'{lcl.MARKET}', "wildberries", "ozon",
                            f'{lcl.OZON}', f'{lcl.WILDBERRIES}'],
    f'{lcl.SERVICES}': [f'{lcl.SERVICES}', f'{lcl.BEAUTY_2}', f'{lcl.HAIRDRESSER}', f'{lcl.SALON}', f'{lcl.REPAIR}', f'{lcl.MASTER}', f'{lcl.CLEANING}', ""]
  }
  return categories

def priority_categories() -> list:
  categories_priority = [
    f'{lcl.SALARY_AND_INCOME}',
    f'{lcl.PRODUCTS}',
    f'{lcl.REPAYMENT_LOAN}',
    f'{lcl.DEPOSIT_INVESTMENTS}',
    f'{lcl.CAFE_AND_RESTAURANT}',
    f'{lcl.TRANSPORT}',
    f'{lcl.TAXES}',
    f'{lcl.INTERNET_AND_COMMUNICATION}',
    f'{lcl.UTILITIES}',
    f'{lcl.HEALTH}',
    f'{lcl.CLOTHES}',
    f'{lcl.HOBBIES_AND_ENTERTAINMENT}',
    f'{lcl.EDUCATION}',
    f'{lcl.SPORTS}',
    f'{lcl.SERVICES}',
    f'{lcl.MARKETPLACES}',
    f'{lcl.SUBSCRIPTIONS}',
    f'{lcl.GIFTS}'

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
                    'type': f'{lcl.INCOME_LABEL}' if amount >= 0 else f'{lcl.EXPENSE_LABEL}'
                }
                data.append(transaction)
    except FileNotFoundError:
        print(f'⚠️ {lcl.FILE} {filename} {lcl.NOT_FOUND}')
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
                    'type': f'{lcl.INCOME_LABEL}' if amount >= 0 else f'{lcl.EXPENSE_LABEL}'
                })
    except FileNotFoundError:
        print(f'⚠️ {lcl.FILE} {filename} {lcl.NOT_FOUND}')
    except json.JSONDecodeError:
        print(f'⚠️ {lcl.JSON_FORMAT_ERROR} {filename}.')
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
    return f'{lcl.OTHER}'


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
    balance = total_income + total_expense
    transaction_count = len(transactions)
    count_income = sum(1 for t in transactions if t["amount"] > 0)
    count_expense = sum(1 for t in transactions if t["amount"] < 0)
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "transaction_count": transaction_count,
        "income_transactions": count_income,
        "expense_transactions": count_expense
    }


def calculate_by_category(transactions: list) -> dict:
    totals = defaultdict(lambda: {"sum": 0, "count": 0})
    total_expense = sum(t["amount"] for t in transactions if t["amount"] < 0)
    for t in transactions:
        cat = t.get("category", f'{lcl.NO_CATEGORY}')
        totals[cat]["sum"] += t["amount"]
        totals[cat]["count"] += 1
    for cat, val in totals.items():
        val["percent"] = (-val["sum"] / -total_expense * 100) if total_expense else 0
    sorted_categories = sorted(totals.items(), key=lambda item: abs(item[1]["sum"]), reverse=True)
    return dict(sorted_categories)


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
            monthly[key]["categories"].append(t.get("category", f'{lcl.NO_CATEGORY}'))
    for m, data in monthly.items():
        data["top_categories"] = Counter(data["categories"]).most_common(3)
    return dict(monthly)

def analyze_seasonal_trends(transactions: list) -> dict:
    quarterly = defaultdict(lambda: {"income": 0, "expenses": 0, "categories": []})
    for t in transactions:
        try:
            d = datetime.datetime.strptime(t["date"], "%Y-%m-%d")
        except Exception:
            continue
        year = d.year
        quarter = (d.month - 1) // 3 + 1
        key = f"{year}-Q{quarter}"
        amount = t["amount"]
        if amount >= 0:
            quarterly[key]["income"] += amount
        else:
            quarterly[key]["expenses"] += amount
            category = t.get("category", f'{lcl.NO_CATEGORY}')
            quarterly[key]["categories"].append(category)
    for q, data in quarterly.items():
        data["top_categories"] = Counter(data["categories"]).most_common(3)
    return dict(quarterly)

def analyze_historical_spending(transactions: list) -> dict:
    monthly_spending = defaultdict(lambda: defaultdict(float))
    for t in transactions:
        if t["amount"] < 0:
            try:
                d = datetime.datetime.strptime(t["date"], "%Y-%m-%d")
            except Exception:
                continue
            month = d.strftime("%Y-%m")
            cat = t.get("category", f'{lcl.NO_CATEGORY}')
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
    budget[f'{lcl.SAVINGS}'] = {"limit": savings, "recommended": savings}
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
            "status": "✅" f'{lcl.WITHIN_BUDGET}' if diff >= 0 else "⚠️" f'{lcl.BUDGET_EXCEEDED}'
        }
    return report


# ==========================
# ВИЗУАЛИЗАЦИЯ
# ==========================

def visualize_financial_data(transactions: list):
    """Строит график: расходы по категориям и доходы/расходы по месяцам"""
    if not transactions:
        print(f'{lcl.NO_VISUALIZATION_DATA}')
        return

    # --- Расходы по категориям ---
    expenses = defaultdict(float)
    for t in transactions:
        if t["amount"] < 0:
            expenses[t["category"]] += abs(t["amount"])
    if expenses:
        plt.figure(figsize=(8, 5))
        plt.bar(expenses.keys(), expenses.values())
        plt.title(f'{lcl.EXPENSES_BY_CATEGORY}')
        plt.xlabel(f'{lcl.CATEGORY}')
        plt.ylabel(f'{lcl.AMOUNT_RUB}')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


# ==========================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================

def smart_piggy_bank(csv_file="money.csv", json_file="transactions.json"):
    print("=" * 70)
    print("💰" f'{lcl.SMART_PIGGY_BANK}' "💡")
    print("=" * 70)

    transactions = []
    if csv_file:
        transactions += import_financial_data(csv_file)
    if json_file:
        transactions += import_financial_data(json_file)

    if not transactions:
        print("❌" f'{lcl.NO_ANALYSIS_DATA}')
        return

    transactions = categorize_all_transactions(transactions)

    stats = calculate_basic_stats(transactions)
    categories_stats = calculate_by_category(transactions)
    timeline = analyze_by_time(transactions)
    analysis = analyze_historical_spending(transactions)
    budget = create_budget_template(analysis, stats["total_income"])
    comparison = compare_budget_vs_actual(budget, transactions)

    # --- ОТЧЁТ ---
    print("\n===" f'{lcl.FINANCIAL_REPORT}' "===")
    print(f'💰 {lcl.INCOME} {stats['total_income']:.2f}')
    print(f'💸 {lcl.EXPENSES} {abs(stats['total_expense']):.2f}')
    print(f'⚖️ {lcl.BALANCE}{stats['balance']:.2f}')

    print("\n📊" f'{lcl.EXPENSES_BY_CATEGORY_TITLE}')
    for cat, data in categories_stats.items():
        print(f"  {cat}: {abs(data['sum']):.2f}" f'{lcl.RUB}' "({data['percent']:.1f}%)")

    print("\n📅" f'{lcl.MONTHLY_ANALYSIS}')
    for month, data in timeline.items():
        top = ", ".join([f"{c} ({n})" for c, n in data["top_categories"]])
        print(f"  {month}:" f'{lcl.INCOME_LABEL}' "{data['income']:.2f} |" f'{lcl.EXPENSE_LABEL}' "{abs(data['expenses']):.2f} →" f'{lcl.TOP}' "{top}")

    print("\n🎯" f'{lcl.RECOMMENDATIONS}')
    for cat, val in analysis["top_categories"]:
        print(f"  🔸 {cat}: {val:.2f}" f'{lcl.AVERAGE_RUB}')

    print("\n📋" f'{lcl.BUDGET_COMPARISON}')
    for cat, info in comparison.items():
        print(f"  {cat}:" f'{lcl.SPENT}' "{info['actual']:.2f} /" f'{lcl.LIMIT}' "{info['limit']:.2f} → {info['status']}")

    print("\n✅" f'{lcl.ANALYSIS_SUCCESS}' "\n")

    # Визуализация
    visualize_financial_data(transactions)


if __name__ == "__main__":
    smart_piggy_bank()
