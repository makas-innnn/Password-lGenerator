import flet as ft
import random
import string

def generate_strong_password(length):
    lo = random.choice(string.ascii_lowercase)
    up = random.choice(string.ascii_uppercase)
    di = random.choice(string.digits)
    sy = random.choice("!@#$%^&*")
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    rest = ""
    for i in range(length - 4):
        rest += random.choice(all_chars)
    combined = list(lo + up + di + sy + rest)
    for i in range(len(combined) - 1, 0, -1):
        j = random.randint(0, i)
        combined[i], combined[j] = combined[j], combined[i]
    return "".join(combined)

def main(page: ft.Page):
    page.title = "Генератор паролей"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30

    password_field = ft.TextField(
        value="", 
        read_only=True, 
        text_align=ft.TextAlign.CENTER,
        text_size=20,
        border_color=ft.Colors.BLUE
    )

    def generate(e):
        password_field.value = generate_strong_password(16)
        # page.update() больше не нужен, Flet обновит сам

    async def copy(e):
        if password_field.value:
            # Новый способ копирования в Flet 1.0 (асинхронный)
            await ft.Clipboard().set(password_field.value)
            page.snack_bar = ft.SnackBar(ft.Text("Пароль скопирован!"))
            page.snack_bar.open = True
            # page.update() не нужен, обновится автоматически

    page.add(
        ft.Text("🔐 Генератор паролей", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="transparent"),
        password_field,
        ft.Divider(height=10, color="transparent"),
        ft.Button(
            content="Сгенерировать",  # В новых версиях текст кнопки передается через content
            on_click=generate, 
            width=300, 
            height=50, 
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        ),
        ft.Divider(height=10, color="transparent"),
        ft.Button(
            content="Копировать",
            on_click=copy, 
            width=300, 
            height=50, 
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE
        )
    )

ft.run(main)
