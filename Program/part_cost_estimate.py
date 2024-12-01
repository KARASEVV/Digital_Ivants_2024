import cv2
import numpy as np

# Функция для расчета площади маски
def calculate_area(mask):
    return cv2.countNonZero(mask)

# Функция для поворота изображения с корректировкой размера холста
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    matrix[0, 2] += (new_w / 2) - center[0]
    matrix[1, 2] += (new_h / 2) - center[1]
    return cv2.warpAffine(image, matrix, (new_w, new_h)), matrix

# Функция для разделения маски на сегменты и расчета площади каждого сегмента
def divide_and_calculate(mask, num_segments):
    h, w = mask.shape
    segment_height = h // num_segments
    segment_areas = []
    for i in range(num_segments):
        segment = mask[i * segment_height: (i + 1) * segment_height, :]
        segment_area = calculate_area(segment)
        segment_areas.append(segment_area)
    return segment_areas

# Основная функция для расчета затрат на покраску и трудозатрат
def part_cost_estimate(image_path):
    # Загрузка изображения и создание бинарной маски
    original_image = cv2.imread(image_path)
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Вычисляем исходную площадь маски
    original_area = calculate_area(binary_mask)

    # Параметры для поворота
    angles = range(0, 91, 15)  # Углы от 0 до 90 градусов с шагом 15
    num_segments = 4
    results = []

    # Для каждой угловой ориентации изображения
    for angle in angles:
        # Поворот изображения и маски
        rotated_image, _ = rotate_image(original_image, angle)
        rotated_mask, _ = rotate_image(binary_mask, angle)

        # Разделение маски на сегменты и расчет их площади
        segment_areas = divide_and_calculate(rotated_mask, num_segments)
        total_segment_area = sum(segment_areas)

        # Разница между исходной площадью и суммарной площадью сегментов
        area_difference = abs(original_area - total_segment_area)
        results.append((angle, original_area, total_segment_area, area_difference))

    # Находим угол с минимальной разницей
    min_difference = min(results, key=lambda x: x[3])
    optimal_angle = min_difference[0]
    optimal_difference = min_difference[3]

    # Расчет расхода краски и трудозатрат на покраску
    # Учитываем расход краски на 1 м² и количество слоев
    total_area = door_area + trunk_area + hood_area  # Общая площадь деталей
    paint_needed = paint_consumption * total_area * layers_count  # Количество краски в литрах
    labor_hours = labor_intensity * total_area * layers_count  # Часов труда для покраски
    labor_cost = labor_hours * labor_cost_per_hour  # Стоимость труда

    # Стоимость ЛКМ (краски)
    paint_cost = paint_needed * lcm_price

    # Общая стоимость
    total_cost = paint_cost + labor_cost

    # Результаты
    results_summary = {
        "optimal_angle": optimal_angle,
        "area_difference": optimal_difference,
        "paint_needed": paint_needed,
        "labor_hours": labor_hours,
        "paint_cost": paint_cost,
        "labor_cost": labor_cost,
        "total_cost": total_cost
    }

    # Возвращаем результаты
    return results_summary

# Пример использования функции
image_path = "C:/Users/Sereja/Desktop/Images & Segmentation/i.jpg"  # Путь к изображению
torch_width = 0.1
torch_extension = 0.08
layers_count = 2
paint_consumption = 0.3
labor_intensity = 0.1
door_area = 0.8
trunk_area = 0.9
hood_area = 1.2
lcm_price = 100  # Стоимость 1 литра ЛКМ
labor_cost_per_hour = 200  # Стоимость 1 нормо-часа

result = part_cost_estimate(image_path) #, torch_width, torch_extension, layers_count, paint_consumption, labor_intensity, door_area, trunk_area, hood_area, lcm_price, labor_cost_per_hour

# Выводим результаты
print(f"Optimal Angle: {result['optimal_angle']}°")
print(f"Area Difference: {result['area_difference']} pixels")
print(f"Paint Needed: {result['paint_needed']} liters")
print(f"Labor Hours: {result['labor_hours']} hours")
print(f"Paint Cost: {result['paint_cost']} units")
print(f"Labor Cost: {result['labor_cost']} units")
print(f"Total Cost: {result['total_cost']} units")
