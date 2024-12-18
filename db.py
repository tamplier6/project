import sqlite3
import json

def create_database():
    """Создает базу данных и необходимые таблицы"""
    conn = sqlite3.connect('furniture_database.db')
    cursor = conn.cursor()

    # Создание таблицы для шаблонов столов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS table_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parts TEXT NOT NULL
    )
    ''')

    # Создание таблицы для размеров материала
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS material_sizes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_width REAL NOT NULL,
        material_length REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def add_table_templates():
    """Добавляет шаблоны столов в базу данных"""
    templates = [
        {
            "name": "Письменный стол",
            "parts": [
                {"name": "Крышка стола", "width": 60, "length": 120, "quantity": 1},
                {"name": "Боковина", "width": 60, "length": 80, "quantity": 2},
                {"name": "Задняя стенка", "width": 40, "length": 108, "quantity": 1}
            ]
        },
        {
            "name": "Журнальный стол",
            "parts": [
                {"name": "Крышка стола", "width": 60, "length": 120, "quantity": 1},
                {"name": "Подстольная полка", "width": 57, "length": 117, "quantity": 1},
                {"name": "Ножка", "width": 8, "length": 70, "quantity": 8}
            ]
        },
        {
            "name": "Стол с тремя полками",
            "parts": [
                {"name": "Крышка стола", "width": 60, "length": 120, "quantity": 1},
                {"name": "Боковина", "width": 60, "length": 80, "quantity": 4},
                {"name": "Задняя стенка", "width": 40, "length": 78, "quantity": 1},
                {"name": "Доска для полок", "width": 60, "length": 60, "quantity": 4},
                {"name": "Доска для дверцы", "width": 20, "length": 57, "quantity": 3}
            ]
        }
    ]
    
    conn = sqlite3.connect('furniture_database.db')
    cursor = conn.cursor()

    for template in templates:
        cursor.execute('''
        INSERT INTO table_templates (name, parts)
        VALUES (?, ?)
        ''', (template["name"], json.dumps(template["parts"])))

    conn.commit()
    conn.close()

def get_table_template(table_type):
    """Извлекает шаблон стола из базы данных по типу стола"""
    conn = sqlite3.connect('furniture_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT parts FROM table_templates WHERE name = ?
    ''', (table_type,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return json.loads(result[0])
    else:
        return None

def add_material_size(width, length):
    """Добавляет размеры материала в базу данных"""
    conn = sqlite3.connect('furniture_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO material_sizes (material_width, material_length)
    VALUES (?, ?)
    ''', (width, length))

    conn.commit()
    conn.close()

def get_material_size():
    """Извлекает размеры материала из базы данных"""
    conn = sqlite3.connect('furniture_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT material_width, material_length FROM material_sizes ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()

    if result:
        return result
    else:
        return None
