import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_cutting_plan(material_width, material_length, cutting_plan, parts):
    fig, ax = plt.subplots()
    
    # Устанавливаем лимиты для осей, добавляя небольшие отступы
    ax.set_xlim(0, material_width + 10)
    ax.set_ylim(0, material_length + 10)

    # Рисуем материал
    ax.add_patch(patches.Rectangle((0, 0), material_width, material_length, linewidth=1, edgecolor='black', facecolor='lightgray'))

    # Рисуем детали и добавляем подписи с названиями
    for (x, y, w, h) in cutting_plan:
        # Найдем название детали для текущей области
        part_name = None
        for part in parts:
            if part["width"] == w and part["length"] == h:
                part_name = part["name"]
                break
        
        # Если название найдено, рисуем прямоугольник и добавляем текст
        if part_name:
            ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='blue', facecolor='skyblue'))


    # Подписываем оси
    ax.set_xlabel('Ширина материала (см)')
    ax.set_ylabel('Длина материала (см)')

    plt.show()
