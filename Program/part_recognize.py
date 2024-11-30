import cv2
import numpy as np


def split_and_draw_contours(image_path, num_segments=4):
    """
    Разделяет контур детали на заданное количество горизонтальных частей и рисует их.

    :param image_path: Путь к изображению.
    :param num_segments: Количество частей для разделения (по умолчанию 4).
    """
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print("Не удалось загрузить изображение.")
        return

    # Преобразование изображения в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Сегментация: выделение контура детали
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проверка наличия контуров
    if not contours:
        print("Контуры не найдены.")
        return

    # Выбираем самый большой контур, предполагая, что это контур детали
    contour = max(contours, key=cv2.contourArea)

    # Получаем ограничивающий прямоугольник для контура
    x, y, w, h = cv2.boundingRect(contour)

    # Высота ограничивающего прямоугольника делим на количество сегментов
    part_height = h // num_segments

    # Создаём копию изображения для рисования
    result_image = image.copy()

    # Разделяем контур на заданное количество частей и рисуем их
    for i in range(num_segments):
        part_top = y + i * part_height
        part_bottom = part_top + part_height
        part_contour = []

        # Находим все точки, которые находятся в текущей горизонтальной полосе
        for point in contour:
            px, py = point[0]
            if part_top <= py <= part_bottom:
                part_contour.append(point)

        # Если есть точки в этой части, рисуем ограничивающий прямоугольник
        if part_contour:
            part_contour = np.array(part_contour)
            part_x, part_y, part_w, part_h = cv2.boundingRect(part_contour)
            cv2.rectangle(result_image, (part_x, part_y), (part_x + part_w, part_y + part_h), (0, 255, 0), 2)

    # Отображаем результат
    cv2.imshow(f"Divided and Contoured into {num_segments} Parts", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Пример: вызов функции для изображения с заданным количеством сегментов
split_and_draw_contours('C:/Users/bossd/Desktop/i (3).png', num_segments=6)  # Указываем количество сегментов

#C:/Users/bossd/Desktop/i (3).png