def read_csv_file(filename: str) -> list:
    """
    Reads transaction data from a CSV file and returns a list of transactions.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries, each representing a transaction
        with keys: 'date', 'amount', 'description', 'type'.
              Returns an empty list if the file is not found.
    """
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

    except csv.Error as e:
            print(f' {lcl.FILE_ERROR} {filename}: {e}')
    except Exception as e:
            print(f' {lcl.FILE_EXCEPTION} {filename}: {e}')
    return data


def read_json_file(filename: str) -> list:
    """
    Reads a JSON file containing transaction data and returns a list of transactions.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries, each representing a transaction with keys:
              'date', 'amount', 'description', 'type'.
    """
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

    except json.JSONDecodeError:
        print(f' {lcl.JSON_FORMAT_ERROR} {filename}.')
    except Exception as e:
            print(f' {lcl.FILE_EXCEPTION} {filename}: {e}')
    return data


def import_financial_data(filename: str) -> list:
    """
    Imports financial data from a file, supporting CSV and JSON formats.

    Args:
        filename (str): The path to the data file.

    Returns:
        list: A list of transactions extracted from the file.
        Empty list if file not found or unsupported format.
    """
    if not os.path.exists(filename):
        return []
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".csv":
        return read_csv_file(filename)
    elif ext == ".json":
        return read_json_file(filename)
    return []
