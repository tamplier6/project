import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Импортируем модули, предполагая их наличие
try:
    from db import get_parts_for_table, get_tables
    from cutting import optimize_cutting
    from plotting import plot_cutting_plan
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}")
    exit(1)

def submit():
    try:
        # Получаем размеры материала
        material_width = float(entry_material_width.get())
        material_length = float(entry_material_length.get())

        # Проверяем, заполнены ли поля
        if material_width <= 0 or material_length <= 0:
            raise ValueError("Размеры материала должны быть больше нуля.")

        # Собираем данные о деталях
        parts = []
        for detail, entry in part_entries.items():
            try:
                width = float(entry[0].get())
                length = float(entry[1].get())

                if width <= 0 or length <= 0:
                    raise ValueError("Размеры деталей должны быть больше нуля.")

                parts.append({'name': detail, 'width': width, 'length': length})
            except ValueError:
                messagebox.showerror("Ошибка", f"Некорректные размеры для детали: {detail}")
                return

        # Оптимизация раскроя
        cutting_plan = optimize_cutting(material_width, material_length, parts)

        # Проверяем результат оптимизации
        if not cutting_plan:
            messagebox.showerror("Ошибка", "Не удалось оптимизировать раскрой. Проверьте размеры деталей и материала.")
            return

        # Построение плана раскроя
        plot_cutting_plan(material_width, material_length, cutting_plan)

    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные размеры.")

def on_table_selected(event):
    """Обработчик выбора стола, чтобы создать поля ввода для деталей"""
    try:
        # Сначала удаляем старые поля
        for widget in part_frame.winfo_children():
            widget.destroy()

        # Получаем выбранный стол
        selected_table_name = table_combobox.get()
        table = next((table for table in tables if table['name'] == selected_table_name), None)

        if not table:
            return

        table_id = table['id']

        # Получаем детали для выбранного стола из базы данных
        parts = get_parts_for_table(table_id)

        # Удаляем дублирующиеся записи деталей по имени
        unique_parts = {part['name']: part for part in parts}.values()

        # Создаем поля для ввода размеров деталей
        global part_entries
        part_entries = {}  # Сбрасываем старые записи

        tk.Label(part_frame, text="Название детали").grid(row=0, column=0)
        tk.Label(part_frame, text="Ширина").grid(row=0, column=1)
        tk.Label(part_frame, text="Длина").grid(row=0, column=2)

        for i, part in enumerate(unique_parts, start=1):
            tk.Label(part_frame, text=part['name']).grid(row=i, column=0)

            width_entry = tk.Entry(part_frame)
            width_entry.grid(row=i, column=1)
            width_entry.insert(0, part.get('width', 0))  # Заполняем значение по умолчанию

            length_entry = tk.Entry(part_frame)
            length_entry.grid(row=i, column=2)
            length_entry.insert(0, part.get('length', 0))  # Заполняем значение по умолчанию

            part_entries[part['name']] = (width_entry, length_entry)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить детали: {e}")

def setup_ui():
    """Настройка интерфейса"""
    try:
        global tables
        # Получаем все столы из базы данных
        tables = get_tables()

        # Основное окно
        root = tk.Tk()
        root.title("Оптимизация раскроя стола")

        # Ввод размеров материала
        tk.Label(root, text="Ширина материала").grid(row=0, column=0)
        global entry_material_width
        entry_material_width = tk.Entry(root)
        entry_material_width.grid(row=0, column=1)

        tk.Label(root, text="Длина материала").grid(row=1, column=0)
        global entry_material_length
        entry_material_length = tk.Entry(root)
        entry_material_length.grid(row=1, column=1)

        # Ввод стола из выпадающего списка
        tk.Label(root, text="Выберите стол").grid(row=2, column=0)
        global table_combobox
        table_combobox = ttk.Combobox(root, values=list({table['name'] for table in tables}))
        table_combobox.grid(row=2, column=1)
        table_combobox.bind("<<ComboboxSelected>>", on_table_selected)

        # Создаем контейнер для полей ввода деталей
        global part_frame
        part_frame = tk.Frame(root)
        part_frame.grid(row=3, column=0, columnspan=3)

        # Кнопка расчета раскроя
        submit_button = tk.Button(root, text="Рассчитать раскрой", command=submit)
        submit_button.grid(row=4, column=0, columnspan=3)

        root.mainloop()

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось настроить интерфейс: {e}")

# Запуск программы
setup_ui()
