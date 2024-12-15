import sqlite3

def create_db():
    """Создание базы данных и таблиц"""
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parts (
        id INTEGER PRIMARY KEY,
        table_id INTEGER,
        name TEXT,
        width FLOAT,
        length FLOAT,
        FOREIGN KEY(table_id) REFERENCES tables(id)
    );
    """)

    # Пример данных (если они еще не были добавлены)
    cursor.execute("INSERT INTO tables (name, description) VALUES (?, ?)", ("Обычный прямой", "Прямой стол с боковыми панелями"))
    cursor.execute("INSERT INTO tables (name, description) VALUES (?, ?)", ("Угловой", "Угловой стол с полками"))
    cursor.execute("INSERT INTO tables (name, description) VALUES (?, ?)", ("Угловой с полками", "Угловой стол с полками"))
    
    cursor.execute("INSERT INTO parts (table_id, name, width, length) VALUES (?, ?, ?, ?)", (1, "столешница", 120, 60))
    cursor.execute("INSERT INTO parts (table_id, name, width, length) VALUES (?, ?, ?, ?)", (1, "боковая панель", 60, 30))
    cursor.execute("INSERT INTO parts (table_id, name, width, length) VALUES (?, ?, ?, ?)", (2, "угловая панель", 80, 80))
    cursor.execute("INSERT INTO parts (table_id, name, width, length) VALUES (?, ?, ?, ?)", (3, "столешница", 100, 50))
    cursor.execute("INSERT INTO parts (table_id, name, width, length) VALUES (?, ?, ?, ?)", (3, "полка", 50, 40))

    # Сохранение и закрытие
    conn.commit()
    conn.close()

def get_tables():
    """Получение всех столов"""
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM tables")
    tables = cursor.fetchall()
    conn.close()
    return [{'id': table[0], 'name': table[1]} for table in tables]

def get_parts_for_table(table_id):
    """Получение всех деталей для выбранного стола"""
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, width, length FROM parts WHERE table_id=?", (table_id,))
    parts = cursor.fetchall()
    conn.close()
    return [{'name': part[0], 'width': part[1], 'length': part[2]} for part in parts]

create_db()