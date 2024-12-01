import flet as ft
from find_car_and_rust import find_car_and_rust
from part_cost_estimate import part_cost_estimate  # Импортируем вашу функцию

def main(page: ft.Page):
    page.title = "Приложение для анализа ржавчины"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280  # Уменьшаем на треть от 1920
    page.window_height = 720  # Уменьшаем на треть от 1080

    # --- Обработчики для окон ---
    # Переменные для второго окна
    image_display = ft.Image(src="", width=600, height=400, fit=ft.ImageFit.CONTAIN)
    rust_segment_display = ft.Image(src="", width=600, height=400, fit=ft.ImageFit.CONTAIN)
    message_text = ft.Text(value="", size=16)

    # Переменные для кнопки перехода
    navigate_button = ft.ElevatedButton(
        text="Перейти на следующую страницу",
        height=50,
        width=300,
        on_click=lambda _: handle_navigation(),
        visible=False
    )

    # --- Экран с полями ввода для расчёта ---
    def handle_input_page(_):
        # Очистка экрана и добавление полей ввода
        page.controls.clear()

        # Поля ввода для всех параметров
        torch_width = ft.TextField(label="Ширина факела (м)", value="0.1", width=200)
        torch_extension = ft.TextField(label="Вылет факела за границы элемента (м)", value="0.08", width=200)
        layers_count = ft.TextField(label="Количество слоев", value="2", width=200)
        paint_consumption = ft.TextField(label="Расход ЛКМ 1-го слоя на 1м² (л)", value="0.3", width=200)
        labor_intensity = ft.TextField(label="Трудоемкость нанесение 1-го слоя на 1м² (ч)", value="0.1", width=200)
        door_area = ft.TextField(label="Физическая площадь передней двери (м²)", value="0.8", width=200)
        trunk_area = ft.TextField(label="Физическая площадь крышки багажника (м²)", value="0.9", width=200)
        hood_area = ft.TextField(label="Физическая площадь капота (м²)", value="1.2", width=200)
        lcm_price = ft.TextField(label="Стоимость 1л ЛКМ", value="100", width=200)
        labor_cost_per_hour = ft.TextField(label="Стоимость 1 нормо-часа", value="200", width=200)

        # Кнопка для расчёта и дальнейших действий
        calculate_button = ft.ElevatedButton(
            text="Расчитать",
            height=50,
            width=200,
            on_click=lambda _: handle_calculation(torch_width.value, torch_extension.value, layers_count.value, paint_consumption.value, labor_intensity.value, door_area.value, trunk_area.value, hood_area.value, lcm_price.value, labor_cost_per_hour.value)
        )

        # Добавляем на страницу поля ввода и кнопку
        page.add(
            ft.Column(
                [
                    torch_width,
                    torch_extension,
                    layers_count,
                    paint_consumption,
                    labor_intensity,
                    door_area,
                    trunk_area,
                    hood_area,
                    lcm_price,
                    labor_cost_per_hour,
                    calculate_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    # Обработчик расчёта
    def handle_calculation(torch_width, torch_extension, layers_count, paint_consumption, labor_intensity, door_area, trunk_area, hood_area, lcm_price, labor_cost_per_hour):
        # Выполнение расчетов
        torch_width = float(torch_width)
        torch_extension = float(torch_extension)
        layers_count = int(layers_count)
        paint_consumption = float(paint_consumption)
        labor_intensity = float(labor_intensity)
        door_area = float(door_area)
        trunk_area = float(trunk_area)
        hood_area = float(hood_area)
        lcm_price = float(lcm_price)
        labor_cost_per_hour = float(labor_cost_per_hour)

        # Пример расчетов (можно заменить на реальную логику)
        total_paint_consumption = (door_area + trunk_area + hood_area) * paint_consumption * layers_count
        total_labor_cost = (door_area + trunk_area + hood_area) * labor_intensity * layers_count * labor_cost_per_hour

        # Отображаем результаты
        result_text = f"Общий расход ЛКМ: {total_paint_consumption:.2f} л\n"
        result_text += f"Общая трудоемкость: {total_labor_cost:.2f} ч\n"

        # Переход на новый экран с результатами
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text("Результаты расчёта", size=24, weight="bold"),
                    ft.Text(result_text, size=16),
                    ft.ElevatedButton(text="Вернуться на главный экран", on_click=lambda _: show_main_screen()),
                    # Добавляем кнопку выбора фото
                    ft.ElevatedButton(
                        text="Выбрать фото",
                        height=50,
                        width=200,
                        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    # --- Переход на главный экран
    def show_main_screen():
        page.controls.clear()
        page.add(photo_screen_layout)
        page.update()

    # --- Экран с анализом изображения ---
    def show_selected_photo(e: ft.FilePickerResultEvent):
        if e.files:
            image_path = e.files[0].path
            image_display.src = image_path
            image_display.update()

            # Запускаем анализ изображения
            messages = find_car_and_rust(image_path)

            # Соединяем все сообщения в одну строку с переносами
            message_text.value = "".join(messages) if messages else "Анализ завершён, но сообщений нет."
            message_text.update()

            # Отправляем выбранное фото в функцию part_cost_estimate для дальнейшей обработки
            part_cost_estimate(image_path)  # Передаем путь к файлу в функцию

            # Показываем кнопку перехода на следующую страницу
            navigate_button.visible = True
            navigate_button.update()

    # --- Переключение на третий экран ---
    def handle_navigation():
        # Очистка текущего интерфейса и добавление нового экрана с полями ввода
        page.controls.clear()
        handle_input_page(None)

    # Переменные для второго окна
    file_picker = ft.FilePicker(on_result=show_selected_photo)
    page.overlay.append(file_picker)

    # Переменные для интерфейса выбора фото
    left_section = ft.Container(
        content=ft.Column(
            [
                ft.ElevatedButton(
                    text="Выбрать фото",
                    height=50,
                    width=200,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                ),
                image_display,
                rust_segment_display,
                navigate_button,  # Кнопка перехода
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=page.width * 0.8,
        bgcolor=ft.colors.BLUE_GREY_100,
    )

    right_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Результаты анализа", size=18, weight="bold"),
                message_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=page.width * 0.2,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        alignment=ft.alignment.center,
    )

    photo_screen_layout = ft.Row(
        [
            left_section,
            right_section,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,  # Центрируем по горизонтали
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Центрируем по вертикали
    )

    # --- Экран авторизации ---
    def handle_login(_):
        page.controls.clear()
        page.add(photo_screen_layout)
        page.update()

    username = ft.TextField(label="Логин", height=50, width=300, text_size=16)
    password = ft.TextField(label="Пароль", password=True, height=50, width=300, text_size=16)
    login_error = ft.Text(value="", color="red", size=14)
    login_btn = ft.ElevatedButton(text="Войти", height=35, width=70, on_click=handle_login)

    login_view = ft.Column(
        [
            ft.Text("Введите логин и пароль", size=20, weight="bold"),
            username,
            password,
            login_error,
            login_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    page.add(login_view)

ft.app(target=main)
