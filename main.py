import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import cProfile
import time

try:
    from cutting import optimize_cutting
    from plotting import plot_cutting_plan
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}")
    exit(1)


def validate_material_size(width, length):
    """Проверяет корректность размеров материала"""
    if width <= 0 or length <= 0:
        raise ValueError("Размеры материала должны быть больше нуля.")
    if width < 10 or length < 10:
        raise ValueError("Размеры материала должны быть не менее 10 см.")
    if width > 500 or length > 500:
        raise ValueError("Размеры материала не могут превышать 500 см.")

def validate_table_type(table_type):
    """Проверяет корректность типа стола"""
    valid_types = ["Письменный стол", "Журнальный стол", "Стол с тремя полками"]
    if table_type not in valid_types:
        raise ValueError(f"Неизвестный тип стола. Допустимые варианты: {', '.join(valid_types)}.")

def validate_table_dimensions(length, width, height):
    """Проверяет корректность размеров стола"""
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Размеры стола должны быть больше нуля.")
    if length < 50 or length > 300:
        raise ValueError("Длина стола должна быть от 50 до 300 см.")
    if width < 50 or width > 150:
        raise ValueError("Ширина стола должна быть от 50 до 150 см.")
    if height < 60 or height > 150:
        raise ValueError("Высота стола должна быть от 60 до 150 см.")

def validate_table_quantity(quantity):
    """Проверяет корректность количества столов"""
    if not isinstance(quantity, int) or quantity <= 0 or quantity > 100:
        raise ValueError("Количество столов должно быть от 1 до 100.")

def get_table_parts(table_type, length, width, height, quantity):
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Все размеры должны быть положительными числами.")
    parts = []

    if table_type == "Письменный стол":
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})
        parts.append({"name": "Боковина", "width": width * 0.8, "length": height, "quantity": 2})
        parts.append({"name": "Задняя стенка", "width": width / 3, "length": length * 0.9, "quantity": 1})
    elif table_type == "Журнальный стол":
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})
        parts.append({"name": "Подстольная полка", "width": width - 3, "length": length - 3, "quantity": 1})
        parts.append({"name": "Ножка", "width": width / 7, "length": height, "quantity": 8})
    elif table_type == "Стол с тремя полками":
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})
        parts.append({"name": "Боковина", "width": width, "length": height, "quantity": 3})
        parts.append({"name": "Задняя стенка", "width": width / 3, "length": length * 0.65, "quantity": 1})
        parts.append({"name": "Задняя стенка для полок", "width": length * 0.35, "length": height, "quantity": 1})
        parts.append({"name": "Доска для полок", "width": width - 1.5, "length": length * 0.35 - 3, "quantity": 4})
        parts.append({"name": "Доска для дверцы", "width": height * 0.25, "length": length * 0.35 - 3, "quantity": 3})
    else:
        raise ValueError("Неизвестный тип стола. Допустимые варианты: 'Письменный стол', 'Журнальный стол', 'Стол с тремя полками'.")
    return parts

def analyze_performance(cutting_function, material_width, material_length, parts):
    """Функция для анализа производительности"""
    start_time = time.time()
    cutting_plan = cutting_function(material_width, material_length, parts)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return cutting_plan, elapsed_time

def analyze_material_efficiency(cutting_plan, material_width, material_length):
    """Анализ расхода материала"""
    total_area = material_width * material_length
    used_area = sum(part["width"] * part["length"] for part in cutting_plan)
    waste_area = total_area - used_area
    efficiency = (used_area / total_area) * 100
    return efficiency, waste_area

def submit():
    try:
        material_width = float(entry_material_width.get())
        material_length = float(entry_material_length.get())
        validate_material_size(material_width, material_length)

        table_type = table_combobox.get().strip()
        validate_table_type(table_type)

        length = float(entry_table_length.get())
        width = float(entry_table_width.get())
        height = float(entry_table_height.get())
        validate_table_dimensions(length, width, height)

        quantity = int(entry_table_quantity.get())
        validate_table_quantity(quantity)

        parts = get_table_parts(table_type, length, width, height, quantity)

        all_parts = []
        for part in parts:
            total_quantity = part["quantity"] * quantity
            for _ in range(total_quantity):
                all_parts.append({
                    "width": part["width"],
                    "length": part["length"],
                    "name": part["name"],
                    "quantity": 1
                })

        cutting_plan, elapsed_time = analyze_performance(optimize_cutting, material_width, material_length, all_parts)

        if not cutting_plan:
            messagebox.showerror("Ошибка", "Не удалось оптимизировать раскрой. Проверьте размеры деталей и материала.")
            return

        plot_cutting_plan(material_width, material_length, cutting_plan)

        # Анализ эффективности материала
        efficiency, waste_area = analyze_material_efficiency(cutting_plan, material_width, material_length)
        messagebox.showinfo("Анализ расхода материала",
                            f"Эффективность использования материала: {efficiency:.2f}%\n"
                            f"Отходы: {waste_area:.2f} см²\n"
                            f"Время выполнения алгоритма: {elapsed_time:.4f} секунд")

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def setup_ui():
    root = tk.Tk()
    root.title("Оптимизация раскроя стола")

    # Ввод размеров материала
    tk.Label(root, text="Ширина материала (до 500см)").grid(row=0, column=0)
    global entry_material_width
    entry_material_width = tk.Entry(root)
    entry_material_width.grid(row=0, column=1)

    tk.Label(root, text="Длина материала (до 500см)").grid(row=1, column=0)
    global entry_material_length
    entry_material_length = tk.Entry(root)
    entry_material_length.grid(row=1, column=1)

    # Ввод типа стола
    tk.Label(root, text="Тип стола").grid(row=2, column=0)
    global table_combobox
    table_combobox = ttk.Combobox(root, values=["Письменный стол", "Журнальный стол", "Стол с тремя полками"])
    table_combobox.grid(row=2, column=1)

    # Ввод размеров стола
    tk.Label(root, text="Длина стола (см)").grid(row=3, column=0)
    global entry_table_length
    entry_table_length = tk.Entry(root)
    entry_table_length.grid(row=3, column=1)

    tk.Label(root, text="Ширина стола (см)").grid(row=4, column=0)
    global entry_table_width
    entry_table_width = tk.Entry(root)
    entry_table_width.grid(row=4, column=1)

    tk.Label(root, text="Высота стола (см)").grid(row=5, column=0)
    global entry_table_height
    entry_table_height = tk.Entry(root)
    entry_table_height.grid(row=5, column=1)

    tk.Label(root, text="Количество столов (до 100)").grid(row=6, column=0)
    global entry_table_quantity
    entry_table_quantity = tk.Entry(root)
    entry_table_quantity.grid(row=6, column=1)

    # Кнопка расчета раскроя
    submit_button = tk.Button(root, text="Рассчитать раскрой", command=submit)
    submit_button.grid(row=7, column=0, columnspan=2)


    root.mainloop()


if __name__ == "__main__":
    setup_ui()
