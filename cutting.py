def drop_down(x, y, w, h, cutting_plan, material_length):
    """Опускает деталь вниз до упора, чтобы устранить щели снизу."""
    min_y = y  # Текущая минимальная возможная координата Y

    while True:
        next_y = min_y
        for part in cutting_plan:
            px, py, pw, ph = part['x'], part['y'], part['width'], part['length']

            # Проверяем пересечение по X и снизу по Y
            if x < px + pw and x + w > px and min_y < py + ph <= min_y + h:
                next_y = max(next_y, py + ph)

        # Убедимся, что деталь не выходит за границы материала
        if next_y + h > material_length:
            break

        # Если координата Y не изменилась, значит опускание завершено
        if next_y == min_y:
            break

        min_y = next_y

    return min_y


def optimize_cutting(material_width, material_length, parts):
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
    free_spaces = [(0, 0, material_width, material_length)]  # Все полотно свободно

    def find_best_fit(part):
        best_fit = None
        best_waste = float('inf')

        for space in free_spaces:
            sx, sy, sw, sl = space

            for rotate in [False, True]:
                part_width, part_length = (part['length'], part['width']) if rotate else (part['width'], part['length'])

                if part_width <= sw and part_length <= sl:
                    waste = (sw - part_width) * sl + sw * (sl - part_length)

                    if waste < best_waste:
                        best_fit = (space, part_width, part_length, rotate)
                        best_waste = waste

        return best_fit

    for part in parts:
        best_fit = find_best_fit(part)

        if not best_fit:
            raise ValueError(f"Не хватает места для размещения детали: {part}")

        space, part_width, part_length, rotated = best_fit
        sx, sy, sw, sl = space

        # Опускаем деталь вниз до упора
        sy = drop_down(sx, sy, part_width, part_length, cutting_plan, material_length)

        cutting_plan.append({
            "x": sx,
            "y": sy,
            "width": part_width,
            "length": part_length,
            "name": part["name"],
            "rotated": rotated
        })

        # Обновляем свободные области
        free_spaces.remove(space)
        free_spaces.append((sx + part_width, sy, sw - part_width, part_length))  # Справа
        free_spaces.append((sx, sy + part_length, sw, sl - part_length))  # Снизу

        # Объединяем смежные свободные области
        free_spaces = merge_adjacent_spaces(free_spaces)

    return cutting_plan


def merge_adjacent_spaces(free_spaces):
    merged = []
    for space in free_spaces:
        sx, sy, sw, sl = space
        can_merge = False
        for other in merged:
            ox, oy, ow, ol = other
            if sx == ox and sw == ow and sy + sl == oy:  # Вертикально смежные
                other[1] = sy
                other[3] += sl
                can_merge = True
            elif sy == oy and sl == ol and sx + sw == ox:  # Горизонтально смежные
                other[0] = sx
                other[2] += sw
                can_merge = True
        if not can_merge:
            merged.append([sx, sy, sw, sl])
    return merged
