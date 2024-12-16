def optimize_cutting(material_width, material_length, parts):
    # Проверка на валидность размеров материала
    if material_width <= 0 or material_length <= 0:
        raise ValueError("Размеры материала должны быть положительными числами.")
    if not parts:
        raise ValueError("Список деталей пуст.")

    # Преобразуем размеры материала в целые числа
    material_width = int(material_width)
    material_length = int(material_length)

    # Сортируем детали по убыванию площади
    parts.sort(key=lambda x: x['width'] * x['length'], reverse=True)

    cutting_plan = []  # План раскроя
    free_spaces = [(0, 0, material_width, material_length)]  # Начально всё полотно свободно

    # Функция для размещения детали в наилучшее свободное место
    def find_best_fit(part):
        best_fit = None
        best_area = float('inf')

        for space in free_spaces:
            sx, sy, sw, sl = space  # Координаты свободной области

            # Проверяем, помещается ли деталь
            if part['width'] <= sw and part['length'] <= sl:
                area = sw * sl  # Площадь текущей свободной области

                # Выбираем наиболее подходящее место (минимальная площадь)
                if area < best_area:
                    best_fit = space
                    best_area = area

        return best_fit

    # Основной цикл: размещение деталей
    for part in parts:
        # Проверяем, если у детали нет ключа 'name', пропускаем её
        if "name" not in part:
            raise ValueError(f"Деталь {part} не содержит обязательного ключа 'name'.")

        # Проверяем, если деталь - ножка и её количество больше 1, она должна оставаться цельной
        if part["name"] == "Ножка" and part["quantity"] > 1:
            # Убедимся, что ножки не разрезаются
            part_copy = part.copy()
            part_copy["quantity"] = 1  # Обрабатываем ножку как одну деталь
            # Стараемся разместить все ножки вместе
            for _ in range(part["quantity"]):
                best_space = find_best_fit(part_copy)

                if not best_space:
                    raise ValueError(f"Не хватает места для размещения ножек.")

                # Размещаем ножку в найденной области
                sx, sy, sw, sl = best_space
                cutting_plan.append((sx, sy, part_copy['width'], part_copy['length']))

                # Обновляем список свободных областей
                free_spaces.remove(best_space)
                free_spaces.append((sx + part_copy['width'], sy, sw - part_copy['width'], part_copy['length']))  # Оставшаяся часть по ширине
                free_spaces.append((sx, sy + part_copy['length'], sw, sl - part_copy['length']))  # Оставшаяся часть по высоте

                # Удаляем области с нулевой или отрицательной площадью
                free_spaces = [space for space in free_spaces if space[2] > 0 and space[3] > 0]

        else:
            best_space = find_best_fit(part)

            if not best_space:
                raise ValueError("Не хватает места для размещения всех деталей.")

            # Размещаем деталь в найденной области
            sx, sy, sw, sl = best_space
            cutting_plan.append((sx, sy, part['width'], part['length']))

            # Обновляем список свободных областей
            free_spaces.remove(best_space)
            free_spaces.append((sx + part['width'], sy, sw - part['width'], part['length']))  # Оставшаяся часть по ширине
            free_spaces.append((sx, sy + part['length'], sw, sl - part['length']))  # Оставшаяся часть по высоте

            # Удаляем области с нулевой или отрицательной площадью
            free_spaces = [space for space in free_spaces if space[2] > 0 and space[3] > 0]

    return cutting_plan
