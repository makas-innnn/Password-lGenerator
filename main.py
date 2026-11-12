import flet as ft
import random
import string

# Словарь переводов
TEXTS = {
    "ru": {
        "title": "🔐 Генератор паролей",
        "app_title": "PasswordGen",
        "gen_btn": "Сгенерировать",
        "copy_btn": "Копировать",
        "length": "Длина пароля:",
        "digits": "Цифры (0-9)",
        "symbols": "Спецсимволы (!@#$)",
        "no_confusing": "Без похожих (l, 1, O)",
        "copied": "Пароль скопирован!",
        "nav_gen": "Генератор",
        "nav_info": "Инфо",
        "about_me": "Начинающий кодер, делаю что в кайф",
        "tg": "Telegram",
        "github": "GitHub",
        "app_desc": "Безопасный офлайн-генератор.\nДанные не покидают устройство."
    },
    "en": {
        "title": "🔐 Password Generator",
        "app_title": "PasswordGen",
        "gen_btn": "Generate",
        "copy_btn": "Copy",
        "length": "Password length:",
        "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#$)",
        "no_confusing": "No confusing (l, 1, O)",
        "copied": "Password copied!",
        "nav_gen": "Generator",
        "nav_info": "Info",
        "about_me": "Beginner coder, doing what I love",
        "tg": "Telegram",
        "github": "GitHub",
        "app_desc": "Secure offline generator.\nData never leaves your device."
    }
}

def gen_pwd(length, digits=True, symbols=True, no_confusing=False):
    lo, up, di, sy = string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*"
    if no_confusing:
        lo, up, di = "abcdefghijkmnpqrstuvwxyz", "ABCDEFGHJKLMNPQRSTUVWXYZ", "23456789"
    
    pwd = [random.choice(lo), random.choice(up)]
    chars = lo + up
    
    if digits: pwd.append(random.choice(di)); chars += di
    if symbols: pwd.append(random.choice(sy)); chars += sy
    
    while len(pwd) < length: pwd.append(random.choice(chars))
    random.shuffle(pwd)
    return "".join(pwd)

def analyze(pwd):
    s = sum([10 if len(pwd)>=8 else 0, 15 if len(pwd)>=12 else 0, 15 if len(pwd)>=16 else 0,
             10 if any(c.islower() for c in pwd) else 0, 15 if any(c.isupper() for c in pwd) else 0,
             15 if any(c.isdigit() for c in pwd) else 0, 20 if any(c in "!@#$%^&*" for c in pwd) else 0])
    s = min(s, 100)
    return (s, "Strong", ft.Colors.GREEN) if s >= 85 else ((s, "Medium", ft.Colors.ORANGE) if s >= 60 else (s, "Weak", ft.Colors.RED))

def main(page: ft.Page):
    page.title = "PasswordGen"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Текущий язык (по умолчанию ru)
    current_lang = "ru"

    # Элементы интерфейса, которые будут меняться
    title_text = ft.Text(TEXTS[current_lang]["title"], size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_400)
    pwd_field = ft.TextField(value="", read_only=True, text_align=ft.TextAlign.CENTER, text_size=20, border_color=ft.Colors.RED_400)
    str_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    
    slider = ft.Slider(min=8, max=32, divisions=24, value=16, label="Длина: {value}", active_color=ft.Colors.PURPLE_400)
    len_label = ft.Text(f"{TEXTS[current_lang]['length']} 16", size=16)
    
    def set_len(v): 
        slider.value = v
        len_label.value = f"{TEXTS[current_lang]['length']} {v}"
        page.update()

    len_btns = ft.Row([ft.Button(content=str(v), on_click=lambda e, v=v: set_len(v), width=45, height=40) for v in [8,12,16,20,32]], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
    
    sw_d = ft.Switch(label=TEXTS[current_lang]["digits"], value=True, active_color=ft.Colors.PURPLE_400)
    sw_s = ft.Switch(label=TEXTS[current_lang]["symbols"], value=True, active_color=ft.Colors.PURPLE_400)
    sw_c = ft.Switch(label=TEXTS[current_lang]["no_confusing"], value=False, active_color=ft.Colors.PURPLE_400)

    btn_gen = ft.Button(content=TEXTS[current_lang]["gen_btn"], on_click=lambda e: generate(e), width=300, height=50, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    btn_copy = ft.Button(content=TEXTS[current_lang]["copy_btn"], on_click=lambda e: page.run_task(copy, e), width=300, height=50, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)

    def generate(e):
        pwd = gen_pwd(int(slider.value), sw_d.value, sw_s.value, sw_c.value)
        pwd_field.value = pwd
        sc, st, cl = analyze(pwd)
        # Переводим статус надежности
        status_ru = "Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")
        status_text = status_ru if current_lang == "ru" else st
        str_text.value = f"Надежность: {sc}% ({status_text})" if current_lang == "ru" else f"Strength: {sc}% ({status_text})"
        str_text.color = cl
        page.update()

    async def copy(e):
        if pwd_field.value:
            await ft.Clipboard().set(pwd_field.value)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(TEXTS[current_lang]["copied"], color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_800
            )
            page.snack_bar.open = True
            page.update()

    # --- ВКЛАДКА 2 ---
    async def open_link(url):
        try:
            await page.launch_url(url, web_window_name="_blank")
        except Exception:
            pass
    
    info_name = ft.Text("Евгений (makas)", size=22, weight=ft.FontWeight.BOLD)
    info_desc = ft.Text(TEXTS[current_lang]["about_me"], size=16, color=ft.Colors.GREY_400)
    btn_tg = ft.Button(content=TEXTS[current_lang]["tg"], icon=ft.Icons.SEND, on_click=lambda e: page.run_task(open_link, "https://t.me/makas_1337"), width=300, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
    btn_gh = ft.Button(content=TEXTS[current_lang]["github"], icon=ft.Icons.CODE, on_click=lambda e: page.run_task(open_link, "https://github.com/makas-innnn"), width=300, bgcolor=ft.Colors.GREY_800, color=ft.Colors.WHITE)
    app_desc = ft.Text(TEXTS[current_lang]["app_desc"], size=14, text_align=ft.TextAlign.CENTER)

    # --- НАВИГАЦИЯ ---
    nav_bar = ft.NavigationBar(
        selected_index=0, 
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label=TEXTS[current_lang]["nav_gen"]), 
            ft.NavigationBarDestination(icon=ft.Icons.INFO, label=TEXTS[current_lang]["nav_info"])
        ], 
        on_change=lambda e: on_nav(e)
    )

    content_area = ft.Container(expand=True, alignment=ft.alignment.center)

    def update_ui_texts():
        title_text.value = TEXTS[current_lang]["title"]
        len_label.value = f"{TEXTS[current_lang]['length']} {int(slider.value)}"
        sw_d.label = TEXTS[current_lang]["digits"]
        sw_s.label = TEXTS[current_lang]["symbols"]
        sw_c.label = TEXTS[current_lang]["no_confusing"]
        btn_gen.content = TEXTS[current_lang]["gen_btn"]
        btn_copy.content = TEXTS[current_lang]["copy_btn"]
        nav_bar.destinations[0].label = TEXTS[current_lang]["nav_gen"]
        nav_bar.destinations[1].label = TEXTS[current_lang]["nav_info"]
        info_desc.value = TEXTS[current_lang]["about_me"]
        btn_tg.content = TEXTS[current_lang]["tg"]
        btn_gh.content = TEXTS[current_lang]["github"]
        app_desc.value = TEXTS[current_lang]["app_desc"]
        page.update()

    def toggle_lang(e):
        nonlocal current_lang
        current_lang = "en" if current_lang == "ru" else "ru"
        update_ui_texts()

    # Кнопка смены языка в AppBar
    page.appbar = ft.AppBar(
        title=ft.Text(TEXTS[current_lang]["app_title"]),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.LANGUAGE, on_click=toggle_lang, tooltip="Switch Language / Сменить язык")
        ]
    )

    tab_gen = ft.Column([title_text, pwd_field, str_text, len_label, slider, len_btns, sw_d, sw_s, sw_c, btn_gen, btn_copy], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    tab_info = ft.Column([ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.PURPLE_400), info_name, info_desc, btn_tg, btn_gh, ft.Divider(height=20, color="transparent"), ft.Text("PasswordGen v1.3", size=14, color=ft.Colors.GREY_400), app_desc], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    def on_nav(e):
        content_area.content = tab_gen if e.control.selected_index == 0 else tab_info
        page.update()

    content_area.content = tab_gen
    page.navigation_bar = nav_bar
    page.add(content_area)

ft.run(main)
