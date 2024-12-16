# plotting.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
def plot_cutting_plan(material_width, material_length, cutting_plan):
    fig, ax = plt.subplots()
    ax.set_xlim(0, material_width)
    ax.set_ylim(0, material_length)

    # Рисуем материал
    ax.add_patch(patches.Rectangle((0, 0), material_width, material_length, linewidth=1, edgecolor='black', facecolor='lightgray'))

    # Рисуем детали
    for (x, y, w, h) in cutting_plan:
        ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='blue', facecolor='skyblue'))

    plt.show()
