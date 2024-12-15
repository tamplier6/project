# cutting.py

def optimize_cutting(material_width, material_length, parts):
    parts.sort(key=lambda x: x['width'] * x['length'], reverse=True)
    cutting_plan = []
    current_x, current_y = 0, 0
    for part in parts:
        if current_x + part['width'] <= material_width and current_y + part['length'] <= material_length:
            cutting_plan.append((current_x, current_y, part['width'], part['length']))
            current_x += part['width']
            if current_x > material_width:
                current_x = 0
                current_y += part['length']
    return cutting_plan
