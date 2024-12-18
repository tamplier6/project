import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_cutting_plan(material_width, material_length, cutting_plan):
    fig, ax = plt.subplots()

    # Устанавливаем лимиты для осей
    ax.set_xlim(0, material_width + 10)
    ax.set_ylim(0, material_length + 10)

    # Рисуем материал
    ax.add_patch(patches.Rectangle((0, 0), material_width, material_length, linewidth=1, edgecolor='black', facecolor='lightgray'))

    # Рисуем детали и добавляем подписи
    for part in cutting_plan:
        x = part["x"]
        y = part["y"]
        width = part["width"]
        length = part["length"]
        name = part["name"]

        # Рисуем прямоугольник для детали
        ax.add_patch(patches.Rectangle((x, y), width, length, linewidth=1, edgecolor='blue', facecolor='skyblue'))

    # Настройка осей
    ax.set_xlabel('Ширина материала (см)')
    ax.set_ylabel('Длина материала (см)')
    ax.set_aspect('equal', adjustable='box')

    plt.show()
