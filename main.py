import flet as ft
import random
import string

# --- СЛОВАРИ ПЕРЕВОДОВ ---
TEXTS = {
    "ru": {
        "title": "🔐 Генератор паролей", "app_title": "PasswordGen", "gen_btn": "Сгенерировать",
        "copy_btn": "Копировать", "length": "Длина пароля:", "digits": "Цифры (0-9)",
        "symbols": "Спецсимволы (!@#$)", "no_confusing": "Без похожих (l, 1, O)",
        "copied": "Пароль скопирован!", "nav_gen": "Генератор", "nav_info": "Инфо",
        "about_me": "Начинающий кодер, делаю что в кайф", "tg": "Telegram", "github": "GitHub",
        "app_desc": "Безопасный офлайн-генератор.\nДанные не покидают устройство.",
        "hide": "Скрыть", "show": "Показать"
    },
    "en": {
        "title": "🔐 Password Generator", "app_title": "PasswordGen", "gen_btn": "Generate",
        "copy_btn": "Copy", "length": "Password length:", "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#$)", "no_confusing": "No confusing (l, 1, O)",
        "copied": "Password copied!", "nav_gen": "Generator", "nav_info": "Info",
        "about_me": "Beginner coder, doing what I love", "tg": "Telegram", "github": "GitHub",
        "app_desc": "Secure offline generator.\nData never leaves your device.",
        "hide": "Hide", "show": "Show"
    }
}

# --- 4 ГОТОВЫЕ ТЕМЫ ---
THEMES = {
    "dark": {"bg": ft.Colors.SURFACE, "title": ft.Colors.PURPLE_400, "border": ft.Colors.RED_400, "btn": ft.Colors.BLUE, "slider": ft.Colors.PURPLE_400, "nav_bg": ft.Colors.SURFACE_CONTAINER_HIGHEST},
    "light": {"bg": ft.Colors.WHITE, "title": ft.Colors.PURPLE_700, "border": ft.Colors.RED_400, "btn": ft.Colors.BLUE_700, "slider": ft.Colors.PURPLE_700, "nav_bg": ft.Colors.GREY_200},
    "purple": {"bg": ft.Colors.DEEP_PURPLE_900, "title": ft.Colors.PURPLE_200, "border": ft.Colors.PURPLE_300, "btn": ft.Colors.PURPLE_600, "slider": ft.Colors.PURPLE_200, "nav_bg": ft.Colors.DEEP_PURPLE_800},
    "forest": {"bg": ft.Colors.GREEN_900, "title": ft.Colors.LIGHT_GREEN_400, "border": ft.Colors.LIGHT_GREEN_400, "btn": ft.Colors.GREEN_600, "slider": ft.Colors.LIGHT_GREEN_400, "nav_bg": ft.Colors.GREEN_800}
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
    page.padding = 20
    
    current_lang = "ru"
    current_theme = "dark"
    real_password = "" # Здесь храним настоящий пароль

    title_text = ft.Text(TEXTS[current_lang]["title"], size=28, weight=ft.FontWeight.BOLD)
    
    # Поле пароля
    pwd_field = ft.TextField(value="", read_only=True, text_align=ft.TextAlign.CENTER, text_size=20)
    
    # Глаз для скрытия/показа
    eye_icon = ft.IconButton(ft.Icons.VISIBILITY, tooltip=TEXTS[current_lang]["hide"])
    
    # Полоска надежности
    strength_bar = ft.ProgressBar(width=300, value=0, bgcolor=ft.Colors.GREY_800, color=ft.Colors.RED)
    str_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

    slider = ft.Slider(min=8, max=32, divisions=24, value=16, label="Длина: {value}")
    len_label = ft.Text(f"{TEXTS[current_lang]['length']} 16", size=16)
    
    def set_len(v): 
        slider.value = v
        len_label.value = f"{TEXTS[current_lang]['length']} {v}"
        page.update()

    len_btns = ft.Row([ft.Button(content=str(v), on_click=lambda e, v=v: set_len(v), width=45, height=40) for v in [8,12,16,20,32]], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
    
    sw_d = ft.Switch(label=TEXTS[current_lang]["digits"], value=True)
    sw_s = ft.Switch(label=TEXTS[current_lang]["symbols"], value=True)
    sw_c = ft.Switch(label=TEXTS[current_lang]["no_confusing"], value=False)

    btn_gen = ft.Button(content=TEXTS[current_lang]["gen_btn"], width=300, height=50, color=ft.Colors.WHITE)
    btn_copy = ft.Button(content=TEXTS[current_lang]["copy_btn"], width=300, height=50, color=ft.Colors.WHITE)

    def toggle_visibility(e):
        nonlocal real_password
        if pwd_field.password:
            pwd_field.password = False
            pwd_field.value = real_password
            eye_icon.icon = ft.Icons.VISIBILITY_OFF
        else:
            pwd_field.password = True
            pwd_field.value = "•" * len(real_password)
            eye_icon.icon = ft.Icons.VISIBILITY
        page.update()

    eye_icon.on_click = toggle_visibility

    def generate(e):
        nonlocal real_password
        real_password = gen_pwd(int(slider.value), sw_d.value, sw_s.value, sw_c.value)
        
        # Если пароль был скрыт, обновляем звездочки
        if pwd_field.password:
            pwd_field.value = "•" * len(real_password)
        else:
            pwd_field.value = real_password
            
        # Обновляем полоску надежности
        sc, st, cl = analyze(real_password)
        strength_bar.value = sc / 100
        strength_bar.color = cl
        
        status_text = ("Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")) if current_lang == "ru" else st
        str_text.value = f"Надежность: {sc}% ({status_text})" if current_lang == "ru" else f"Strength: {sc}% ({status_text})"
        str_text.color = cl
        page.update()

    async def copy(e):
        if real_password:
            await ft.Clipboard().set(real_password)
            page.snack_bar = ft.SnackBar(content=ft.Text(TEXTS[current_lang]["copied"], color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800)
            page.snack_bar.open = True
            page.update()

    btn_gen.on_click = generate
    btn_copy.on_click = lambda e: page.run_task(copy, e)

    async def open_link(url):
        try: await page.launch_url(url, web_window_name="_blank")
        except: pass
    
    info_name = ft.Text("Евгений (makas)", size=22, weight=ft.FontWeight.BOLD)
    info_desc = ft.Text(TEXTS[current_lang]["about_me"], size=16, color=ft.Colors.GREY_400)
    btn_tg = ft.Button(content=TEXTS[current_lang]["tg"], icon=ft.Icons.SEND, on_click=lambda e: page.run_task(open_link, "https://t.me/makas_1337"), width=300, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
    btn_gh = ft.Button(content=TEXTS[current_lang]["github"], icon=ft.Icons.CODE, on_click=lambda e: page.run_task(open_link, "https://github.com/makas-innnn"), width=300, bgcolor=ft.Colors.GREY_800, color=ft.Colors.WHITE)
    app_desc = ft.Text(TEXTS[current_lang]["app_desc"], size=14, text_align=ft.TextAlign.CENTER)

    nav_bar = ft.NavigationBar(
        selected_index=0, 
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label=TEXTS[current_lang]["nav_gen"]), 
            ft.NavigationBarDestination(icon=ft.Icons.INFO, label=TEXTS[current_lang]["nav_info"])
        ]
    )

    content_area = ft.Container(expand=True, alignment=ft.Alignment.CENTER)

    def apply_theme():
        t = THEMES[current_theme]
        page.bgcolor = t["bg"]
        title_text.color = t["title"]
        pwd_field.border_color = t["border"]
        btn_gen.bgcolor = t["btn"]
        btn_copy.bgcolor = t["btn"]
        slider.active_color = t["slider"]
        sw_d.active_color = t["slider"]
        sw_s.active_color = t["slider"]
        sw_c.active_color = t["slider"]
        nav_bar.bgcolor = t["nav_bg"]
        page.appbar.bgcolor = t["nav_bg"]
        page.update()

    def toggle_theme(e):
        nonlocal current_theme
        themes_list = list(THEMES.keys())
        idx = themes_list.index(current_theme)
        current_theme = themes_list[(idx + 1) % len(themes_list)]
        apply_theme()

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

    def on_nav(e):
        content_area.content = tab_gen if e.control.selected_index == 0 else tab_info
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text(TEXTS[current_lang]["app_title"]),
        center_title=True,
        actions=[
            ft.IconButton(ft.Icons.PALETTE, on_click=toggle_theme, tooltip="Сменить тему / Change Theme"),
            ft.IconButton(ft.Icons.LANGUAGE, on_click=toggle_lang, tooltip="Сменить язык / Change Language")
        ]
    )

    # Компоновка поля пароля и глаза в одну строку
    pwd_row = ft.Row([pwd_field, eye_icon], alignment=ft.MainAxisAlignment.CENTER)

    tab_gen = ft.Column([
        title_text, pwd_row, strength_bar, str_text, len_label, slider, len_btns, 
        sw_d, sw_s, sw_c, btn_gen, btn_copy
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    
    tab_info = ft.Column([
        ft.Icon(ft.Icons.PERSON, size=80), info_name, info_desc, btn_tg, btn_gh, 
        ft.Divider(height=20, color="transparent"), ft.Text("PasswordGen v1.6", size=14, color=ft.Colors.GREY_400), app_desc
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    content_area.content = tab_gen
    page.navigation_bar = nav_bar
    page.add(content_area)
    
    apply_theme()

ft.run(main)
