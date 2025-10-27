import collections
import datetime

#шаг 1 : Посчитать основные показатели
def calculate_basic_stats(transactions: list) -> dict:
    total_income = sum(t['amount'] for t in transactions
                       if t['amount'] > 0)
    total_expense = sum(t['amount'] for t in transactions
                        if t['amount'] < 0)
    balance = total_income + total_expense
    count_transactions = len(transactions)
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transaction_count': count_transactions
    }

#Шаг 2: Разложить по категориям
def calculate_by_category(transactions: list) -> dict: # transactions — список словарей
    category_totals = {}
    total_expenses = sum(t['amount'] for t in transactions
                         if t['amount'] < 0)

    for t in transactions:
        category = t.get('category', 'Без категории') #пытаемся извлечь название категории по ключу 'category', иначе
        if category not in category_totals:
            category_totals[category] = {
                'sum': 0,
                'count': 0
            }
        category_totals[category]['sum'] += t['amount']
        category_totals[category]['count'] += 1

    # Вычисляем процент от общих расходов
    for cat, data in category_totals.items():
        data['percent'] = (-data['sum'] / -total_expenses * 100) if total_expenses != 0 else 0

    return category_totals


# Функция для анализа по времени (по месяцам)
def analyze_by_time(transactions: list) -> dict:
    monthly_stats = {}

    for t in transactions:
        date_obj = datetime.datetime.strptime(t['date'], '%Y-%m-%d')
        month_key = date_obj.strftime('%Y-%m')  # например, '2024-01'
        if month_key not in monthly_stats:
            monthly_stats[month_key] = {
                'income': 0,
                'expenses': 0,
                'categories': []
            }
        if t['amount'] > 0:
            monthly_stats[month_key]['income'] += t['amount']
        elif t['amount'] < 0:
            monthly_stats[month_key]['expenses'] += t['amount']
            monthly_stats[month_key]['categories'].append(t.get('category', 'Без категории'))

    # Анализ самых частых категорий за месяц
    for month, data in monthly_stats.items():
        category_counter = collections.Counter(data['categories'])
        most_common = category_counter.most_common(3)
        data['top_categories'] = most_common

    return monthly_stats


# Пример использования
def main():
    # Пример списка транзакций с добавленной категорией
    transactions = [
        {"date": "2024-01-15", "amount": -1500.50, "description": "Продукты в Пятерочке", "category": "еда"},
        {"date": "2024-01-10", "amount": 50000, "description": "Зарплата", "category": "Заработок"},
        {"date": "2024-01-08", "amount": -350, "description": "Метро", "category": "транспорт"},
        {"date": "2024-01-05", "amount": -1200, "description": "Ресторан Суши", "category": "еда"},
        {"date": "2024-01-03", "amount": -450, "description": "Аптека", "category": "здоровье"}
    ]

    # Расчет основных показателей
    basic_stats = calculate_basic_stats(transactions)
    print("Основные показатели:")
    print(f"💰 Доходы: {basic_stats['total_income']:.2f} руб.")
    print(f"💸 Расходы: {abs(basic_stats['total_expense']):.2f} руб.")
    print(f"⚖️ Баланс: {basic_stats['balance']:.2f} руб.")

    # Расчет по категориям
    category_stats = calculate_by_category(transactions)
    print("\nРасходы по категориям:")
    for category, data in category_stats.items():
        print(f"{category}: {abs(data['sum']):.2f} руб. ({data['percent']:.1f}%)")

    # Анализ по времени
    timeline = analyze_by_time(transactions)
    print("\nАнализ по месяцам:")
    for month, data in timeline.items():
        print(f"\nМесяц: {month}")
        print(f" Доходы: {data['income']:.2f} руб.")
        print(f" Расходы: {abs(data['expenses']):.2f} руб.")
        print(" Топ категорий расхода:")
        for cat, count in data['top_categories']:
            print(f"  {cat}: {count} транзакций")
if __name__ == "__main__":
    main()
