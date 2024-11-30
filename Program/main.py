import flet as ft


def main(page: ft.Page):
    # Функция для перехода после авторизации
    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.controls.clear()
            show_main_interface()
            page.update()

    # Функция для отображения главного интерфейса
    def show_main_interface():
        def upload_photo(e):
            file_picker.pick_files(allow_multiple=False)

        def file_selected(e):
            if file_picker.result and file_picker.result.files:
                file_path.value = file_picker.result.files[0].path
                image.src = file_path.value
                page.update()

        file_picker = ft.FilePicker(on_result=file_selected)
        file_path = ft.Text()
        image = ft.Image(width=400, fit=ft.ImageFit.CONTAIN)

        # Панель с настройками
        settings_panel = ft.Column([
            ft.Text("Настройки"),
            ft.TextField(label="Поле 1"),
            ft.TextField(label="Поле 2"),
            ft.ElevatedButton("Сохранить", on_click=lambda e: print("Сохранено"))
        ], width=200)

        # Основная страница
        main_layout = ft.Row([
            ft.Container(content=image, expand=1),
            settings_panel
        ])

        page.overlay.append(file_picker)
        page.controls.append(ft.Column([
            ft.ElevatedButton("Загрузить фото", on_click=upload_photo),
            file_path,
            main_layout
        ]))

    # Авторизация
    username = ft.TextField(label="Логин")
    password = ft.TextField(label="Пароль", password=True)
    login_button = ft.ElevatedButton("Войти", on_click=login)

    # Отображение начальной страницы
    page.add(ft.Column([username, password, login_button]))


ft.app(target=main)
