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

def analyze(pwd):
    score = 0
    if len(pwd) >= 8: score += 10
    if len(pwd) >= 12: score += 15
    if len(pwd) >= 16: score += 15
    if any(c.islower() for c in pwd): score += 10
    if any(c.isupper() for c in pwd): score += 15
    if any(c.isdigit() for c in pwd): score += 15
    if any(c in "!@#$%^&*" for c in pwd): score += 20
    
    score = min(score, 100)
    
    if score >= 85:
        return score, "Надежный", ft.Colors.GREEN
    elif score >= 60:
        return score, "Средний", ft.Colors.ORANGE
    else:
        return score, "Слабый", ft.Colors.RED

def main(page: ft.Page):
    page.title = "Генератор паролей"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # <--- Центрируем по горизонтали
    page.padding = 30

    # Переменная для хранения текущей длины
    current_length = ft.Ref[int]()

    password_field = ft.TextField(
        value="", 
        read_only=True, 
        text_align=ft.TextAlign.CENTER,
        text_size=20,
        border_color=ft.Colors.BLUE
    )

    # Текст, который показывает надежность
    strength_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

    def generate(e):
        length = int(slider.value)
        pwd = generate_strong_password(length)
        password_field.value = pwd
        
        # Анализируем надежность
        score, status, color = analyze(pwd)
        strength_text.value = f"Надежность: {score}% ({status})"
        strength_text.color = color

    async def copy(e):
        if password_field.value:
            await ft.Clipboard().set(password_field.value)
            page.snack_bar = ft.SnackBar(ft.Text("Пароль скопирован!"))
            page.snack_bar.open = True

    # Ползунок длины
    slider = ft.Slider(
        min=8, 
        max=32, 
        divisions=24, 
        value=16, 
        label="Длина: {value}",
        on_change=lambda e: length_label.update() 
    )
    
    length_label = ft.Text(f"Длина пароля: 16", size=16)

    page.add(
        ft.Text("🔐 Генератор паролей", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="transparent"),
        
        password_field,
        ft.Divider(height=5, color="transparent"),
        
        strength_text, # <--- Сюда выводится надежность
        ft.Divider(height=15, color="transparent"),
        
        length_label,
        slider,
        ft.Divider(height=10, color="transparent"),
        
        ft.Button(
            content="Сгенерировать", 
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
