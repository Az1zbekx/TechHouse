import json
import os
from datetime import datetime
from config import DATA_DIR, PRODUCTS_FILE, SALES_FILE, USERS_FILE


def ensure_data_directory() -> None:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def _backup_corrupted_file(filepath: str) -> None:
    try:
        if os.path.exists(filepath):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.rename(filepath, f"{filepath}.corrupted_{ts}.bak")
    except Exception:
        # backup is best-effort
        pass


def load_json(filepath: str, default_data=None):
    if default_data is None:
        default_data = []

    ensure_data_directory()

    if not os.path.exists(filepath):
        save_json(filepath, default_data)
        return default_data

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # basic sanity: only list/dict allowed
        if isinstance(data, (list, dict)):
            return data
        _backup_corrupted_file(filepath)
        save_json(filepath, default_data)
        return default_data
    except json.JSONDecodeError:
        _backup_corrupted_file(filepath)
        save_json(filepath, default_data)
        return default_data
    except Exception:
        # any IO errors -> fallback
        return default_data


def save_json(filepath: str, data) -> None:
    ensure_data_directory()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        # As CLI app, print is acceptable. Don't crash.
        print(f"❌ Faylga yozishda xato: {filepath} | {e}")


def load_products():
    default_products = [
        {"id": 1, "nomi": "Mikroto'lqinli pech", "narxi": 150, "kategoriya": "Oshxona", "holati": "Mavjud"},
        {"id": 2, "nomi": "Changyutgich", "narxi": 200, "kategoriya": "Tozalash", "holati": "Mavjud"},
        {"id": 3, "nomi": "Konditsioner", "narxi": 500, "kategoriya": "Uy", "holati": "Mavjud"},
        {"id": 4, "nomi": "Muzlatgich", "narxi": 800, "kategoriya": "Oshxona", "holati": "Mavjud"},
        {"id": 5, "nomi": "Kir yuvish mashinasi", "narxi": 600, "kategoriya": "Uy", "holati": "Mavjud"},
        {"id": 6, "nomi": "Televizor", "narxi": 700, "kategoriya": "Uy", "holati": "Mavjud"},
        {"id": 7, "nomi": "Blender", "narxi": 80, "kategoriya": "Oshxona", "holati": "Mavjud"},
    ]
    return load_json(PRODUCTS_FILE, default_products)


def save_products(products) -> None:
    save_json(PRODUCTS_FILE, products)


def load_sales():
    return load_json(SALES_FILE, [])


def save_sales(sales) -> None:
    save_json(SALES_FILE, sales)


def load_users():
    return load_json(USERS_FILE, [])


def save_users(users) -> None:
    save_json(USERS_FILE, users)
