import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

try:
    from cutting import optimize_cutting
    from plotting import plot_cutting_plan
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}")
    exit(1)


def get_table_parts(table_type, length, width, height, quantity):
    """
    Рассчитывает детали для заданного типа стола на основе пользовательских параметров.

    :param table_type: Тип стола ("Письменный стол", "Журнальный стол" или "Стол с тремя полками").
    :param length: Длина крышки стола (см).
    :param width: Ширина крышки стола (см).
    :param height: Высота стола (см).
    :param quantity: Количество столов.
    :return: Список деталей стола с их размерами и количеством.
    """
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Все размеры должны быть положительными числами.")

    parts = []

    if table_type == "Письменный стол":
        # Крышка стола (1 шт)
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})

        # Боковины (2 шт)
        parts.append({"name": "Боковина", "width": width * 0.8, "length": height, "quantity": 2})

        # Задняя стенка (1 шт, высота = высота стола, ширина = ширина крышки / 3)
        parts.append({"name": "Задняя стенка", "width": width / 3, "length": length * 0.9, "quantity": 1})

    elif table_type == "Журнальный стол":
        # Крышка стола (1 шт)
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})

        # Подстольная полка (1 шт, длина и ширина уменьшены на 3 см)
        parts.append({"name": "Подстольная полка", "width": width - 3, "length": length - 3, "quantity": 1})

        # Ножки (8 одинаковых ножек для каждого стола, каждая с шириной width / 7 и длиной height)
        parts.append({"name": "Ножка", "width": width / 7, "length": height, "quantity": 8})  # Умножаем на количество столов

    elif table_type == "Стол с тремя полками":
        # Крышка стола (1 шт)
        parts.append({"name": "Крышка стола", "width": width, "length": length, "quantity": 1})

        # Боковины (4 шт)
        parts.append({"name": "Боковина", "width": width, "length": height, "quantity": 4})

        # Задняя стенка (1 шт)
        parts.append({"name": "Задняя стенка", "width": width / 3, "length": length * 0.65, "quantity": 1})

        # Полки (4 шт)
        parts.append({"name": "Доска для полок", "width": width - 1.5, "length": width - 3, "quantity": 4})

        # Дверцы (3 шт)
        parts.append({"name": "Доска для дверцы", "width": height * 0.25, "length": width - 3, "quantity": 3})

    else:
        raise ValueError("Неизвестный тип стола. Допустимые варианты: 'Письменный стол', 'Журнальный стол', 'Стол с тремя полками'.")

    return parts


def submit():
    try:
        # Получаем размеры материала
        material_width = float(entry_material_width.get())
        material_length = float(entry_material_length.get())

        if material_width <= 0 or material_length <= 0:
            raise ValueError("Размеры материала должны быть больше нуля.")

        # Получаем тип стола
        table_type = table_combobox.get().strip()  # Убираем лишние пробелы

        # Проверяем правильность типа стола
        if table_type not in ["Письменный стол", "Журнальный стол", "Стол с тремя полками"]:
            messagebox.showerror("Ошибка", "Неизвестный тип стола. Допустимые варианты: 'Письменный стол', 'Журнальный стол', 'Стол с тремя полками'.")
            return

        # Получаем размеры стола
        length = float(entry_table_length.get())
        width = float(entry_table_width.get())
        height = float(entry_table_height.get())

        if length <= 0 or width <= 0 or height <= 0:
            raise ValueError("Размеры стола должны быть больше нуля.")

        # Получаем количество столов
        try:
            quantity = int(entry_table_quantity.get())
            if quantity <= 0 or quantity > 100:
                raise ValueError("Количество столов должно быть от 1 до 100.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество столов (от 1 до 100).")
            return

        # Рассчитываем детали стола, передавая параметр quantity
        parts = get_table_parts(table_type, length, width, height, quantity)

        # Преобразуем детали в список для оптимизации
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

        cutting_plan = optimize_cutting(material_width, material_length, all_parts)

        if not cutting_plan:
            messagebox.showerror("Ошибка", "Не удалось оптимизировать раскрой. Проверьте размеры деталей и материала.")
            return


        plot_cutting_plan(material_width, material_length, cutting_plan)

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))



def setup_ui():
    """Настройка интерфейса"""
    root = tk.Tk()
    root.title("Оптимизация раскроя стола")

    # Ввод размеров материала
    tk.Label(root, text="Ширина материала (см)").grid(row=0, column=0)
    global entry_material_width
    entry_material_width = tk.Entry(root)
    entry_material_width.grid(row=0, column=1)

    tk.Label(root, text="Длина материала (см)").grid(row=1, column=0)
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

    # Ввод количества столов
    tk.Label(root, text="Количество столов (до 100)").grid(row=6, column=0)
    global entry_table_quantity
    entry_table_quantity = tk.Entry(root)
    entry_table_quantity.grid(row=6, column=1)

    # Кнопка расчета раскроя
    submit_button = tk.Button(root, text="Рассчитать раскрой", command=submit)
    submit_button.grid(row=7, column=0, columnspan=2)

    root.mainloop()


# Запуск программы
if __name__ == "__main__":
    setup_ui()
