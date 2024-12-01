import cv2
import numpy as np
from ultralytics import YOLO
import os
output_dir = "C:/Users/Sereja/Desktop/Images & Segmentation/output"
model = YOLO('yolov8n.pt')
def find_car_and_rust(image_path):
    messages = []  # Список для сообщений о статусе анализа

    try:
        # Загружаем изображение
        image = cv2.imread(image_path)
        if image is None:
            return "Ошибка: изображение не удалось загрузить."

        # Обрабатываем изображение моделью YOLO
        results = model(image)

        # Получаем рамки обнаруженных объектов
        cars_detected = [result for result in results[0].boxes if result.cls == list(model.names.values()).index("car")]

        if not cars_detected:
            messages.append("Машина не обнаружена.")
            return "\n".join(messages)

        # Преобразуем изображение в HSV для поиска ржавчины
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Задаем диапазон цветов ржавчины в HSV
        lower_rust = np.array([10, 100, 100])  # Нижняя граница оранжевого цвета
        upper_rust = np.array([30, 255, 255])  # Верхняя граница

        # Создаем маску для поиска ржавчины
        rust_mask = cv2.inRange(hsv_image, lower_rust, upper_rust)

        for car in cars_detected:
            # Получаем координаты рамки (x1, y1, x2, y2)
            x1, y1, x2, y2 = car.xyxy[0].cpu().numpy().astype(int)

            # Рассчитываем координаты квадрата
            side_length = max(x2 - x1, y2 - y1)
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

            square_x1 = int(center_x - side_length / 2)
            square_y1 = int(center_y - side_length / 2)
            square_x2 = int(center_x + side_length / 2)
            square_y2 = int(center_y + side_length / 2)

            # Обводим автомобиль квадратом
            image_with_square = image.copy()
            cv2.rectangle(image_with_square, (square_x1, square_y1), (square_x2, square_y2), (0, 255, 0), 2)

            # Рассчитываем соотношение ширины и высоты рамки
            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / height

            if aspect_ratio > 1.5:
                messages.append("Машина сфотографирована сбоку. Квадрат разделён на 4 части по вертикали.")
                step = (square_x2 - square_x1) // 4

                for i in range(1, 4):
                    x_pos = square_x1 + i * step
                    cv2.line(image_with_square, (x_pos, square_y1), (x_pos, square_y2), (255, 0, 0), 2)

            # Проверяем наличие ржавчины
            car_region = rust_mask[y1:y2, x1:x2]
            rust_in_car = np.sum(car_region) > 0

            if rust_in_car:
                messages.append("Ржавчина обнаружена на автомобиле!")

                # Определяем сегмент с ржавчиной
                car_width, car_height = x2 - x1, y2 - y1
                step_x, step_y = car_width // 4, car_height // 4

                for i in range(4):
                    for j in range(4):
                        x_start, x_end = x1 + i * step_x, x1 + (i + 1) * step_x
                        y_start, y_end = y1 + j * step_y, y1 + (j + 1) * step_y

                        if np.sum(rust_mask[y_start:y_end, x_start:x_end]) > 0:
                            messages.append(f"Ржавчина обнаружена в сегменте ({i + 1}, {j + 1}).")
                            break
                    if messages[-1].startswith("Ржавчина обнаружена в сегменте"):
                        break

            # Сохраняем изображение с квадратом и линиями
            output_image_path = os.path.join(output_dir, "processed_with_square_and_rust_detection.jpg")
            cv2.imwrite(output_image_path, image_with_square)
            messages.append(f"Изображение с квадратом и линиями сохранено по пути: {output_image_path}")

    except Exception as e:
        messages.append(f"Ошибка: {str(e)}")

    return "".join(messages)  # Возвращаем сообщения как одну строку
