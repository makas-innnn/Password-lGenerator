import flet as ft
import random
import string
import json
import os
import platform
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "passwordgen_history.json")

TEXTS = {
    "ru": {
        "title": "🔐 Генератор паролей", "app_title": "PasswordGen", "gen_btn": "Сгенерировать",
        "copy_btn": "Копировать", "length": "Длина пароля:", "digits": "Цифры (0-9)",
        "symbols": "Спецсимволы (!@#$)", "no_confusing": "Без похожих (l, 1, O)",
        "copied": "Пароль скопирован!", "nav_gen": "Генератор", "nav_check": "Проверка", "nav_info": "Инфо",
        "about_me": "Начинающий кодер, делаю что в кайф", 
        "app_desc": "Безопасный офлайн-генератор.\nДанные не покидают устройство.",
        "history": "История (последние 5)",
        "check_hint": "Введите пароль для проверки...",
        "check_result": "Надежность: {}% ({})",
        "tg_label": "Телеграм канал создателя:", "gh_label": "GitHub создателя:",
        "copy_logs": "Скопировать логи", "logs_copied": "Логи скопированы!",
        "support_btn": "Написать в поддержку", "support_copied": "Ссылка на Telegram скопирована! Напишите нам."
    },
    "en": {
        "title": "🔐 Password Generator", "app_title": "PasswordGen", "gen_btn": "Generate",
        "copy_btn": "Copy", "length": "Password length:", "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#$)", "no_confusing": "No confusing (l, 1, O)",
        "copied": "Password copied!", "nav_gen": "Generator", "nav_check": "Check", "nav_info": "Info",
        "about_me": "Beginner coder, doing what I love", 
        "app_desc": "Secure offline generator.\nData never leaves your device.",
        "history": "History (last 5)",
        "check_hint": "Enter password to check...",
        "check_result": "Strength: {}% ({})",
        "tg_label": "Creator's Telegram channel:", "gh_label": "Creator's GitHub:",
        "copy_logs": "Copy logs", "logs_copied": "Logs copied!",
        "support_btn": "Contact Support", "support_copied": "Telegram link copied! Write to us."
    }
}

THEMES = {
    "dark": {"bg": ft.Colors.SURFACE, "title": ft.Colors.PURPLE_400, "border": ft.Colors.RED_400, "btn": ft.Colors.BLUE, "slider": ft.Colors.PURPLE_400, "nav_bg": ft.Colors.SURFACE_CONTAINER_HIGHEST},
    "light": {"bg": ft.Colors.WHITE, "title": ft.Colors.PURPLE_700, "border": ft.Colors.RED_400, "btn": ft.Colors.BLUE_700, "slider": ft.Colors.PURPLE_700, "nav_bg": ft.Colors.GREY_200},
    "purple": {"bg": ft.Colors.DEEP_PURPLE_900, "title": ft.Colors.PURPLE_200, "border": ft.Colors.PURPLE_300, "btn": ft.Colors.PURPLE_600, "slider": ft.Colors.PURPLE_200, "nav_bg": ft.Colors.DEEP_PURPLE_800},
    "forest": {"bg": ft.Colors.GREEN_900, "title": ft.Colors.LIGHT_GREEN_400, "border": ft.Colors.LIGHT_GREEN_400, "btn": ft.Colors.GREEN_600, "slider": ft.Colors.LIGHT_GREEN_400, "nav_bg": ft.Colors.GREEN_800}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"history": []}

def save_data_to_file(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

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
    if not pwd: return 0, "Weak", ft.Colors.RED
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
    real_password = ""
    
    loaded_data = load_data()
    history = loaded_data.get("history", [])

    title_text = ft.Text(TEXTS[current_lang]["title"], size=28, weight=ft.FontWeight.BOLD)
    
    # --- ВКЛАДКА 1: ГЕНЕРАТОР ---
    pwd_field = ft.TextField(value="", read_only=True, text_align=ft.TextAlign.CENTER, text_size=20)
    eye_icon = ft.IconButton(ft.Icons.VISIBILITY, tooltip="Скрыть/Показать")
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

    history_title = ft.Text(TEXTS[current_lang]["history"], size=16, weight=ft.FontWeight.BOLD)
    history_col = ft.Column(spacing=5)

    async def copy_to_clipboard(val, msg):
        if not val: return
        await ft.Clipboard().set(val)
        page.snack_bar = ft.SnackBar(content=ft.Text(msg, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800)
        page.snack_bar.open = True
        page.update()

    def update_history_ui():
        history_col.controls.clear()
        for p in history:
            row = ft.Row([
                ft.Text(p, size=14, color=ft.Colors.GREY_400),
                ft.IconButton(ft.Icons.COPY, icon_size=16, tooltip="Копировать",
                    on_click=lambda e, val=p: page.run_task(copy_to_clipboard, val, TEXTS[current_lang]["copied"]))
            ], alignment=ft.MainAxisAlignment.CENTER)
            history_col.controls.append(row)

    def toggle_visibility(e):
        if pwd_field.password:
            pwd_field.password = False
            pwd_field.value = real_password
            eye_icon.icon = ft.Icons.VISIBILITY_OFF
        else:
            pwd_field.password = True
            pwd_field.value = "•" * len(real_password)
            eye_icon.icon = ft.Icons.VISIBILITY
        page.update()

    def generate(e):
        nonlocal real_password, history
        real_password = gen_pwd(int(slider.value), sw_d.value, sw_s.value, sw_c.value)
        
        if pwd_field.password:
            pwd_field.value = "•" * len(real_password)
        else:
            pwd_field.value = real_password
            
        sc, st, cl = analyze(real_password)
        strength_bar.value = sc / 100
        strength_bar.color = cl
        status_text = ("Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")) if current_lang == "ru" else st
        str_text.value = f"Надежность: {sc}% ({status_text})" if current_lang == "ru" else f"Strength: {sc}% ({status_text})"
        str_text.color = cl
        
        history.insert(0, real_password)
        if len(history) > 5: history.pop()
        update_history_ui()
        save_data_to_file({"history": history})
        page.update()

    eye_icon.on_click = toggle_visibility
    btn_gen.on_click = generate
    btn_copy.on_click = lambda e: page.run_task(copy_to_clipboard, real_password, TEXTS[current_lang]["copied"])

    pwd_row = ft.Row([pwd_field, eye_icon], alignment=ft.MainAxisAlignment.CENTER)
    tab_gen = ft.Column([
        pwd_row, strength_bar, str_text, len_label, slider, len_btns, 
        sw_d, sw_s, sw_c, btn_gen, btn_copy,
        ft.Divider(height=15, color="transparent"),
        history_title,
        history_col
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    # --- ВКЛАДКА 2: ПРОВЕРКА ---
    check_field = ft.TextField(label=TEXTS[current_lang]["check_hint"], password=True, can_reveal_password=True, text_size=16)
    check_result_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

    def check_my_pwd(e):
        if not check_field.value:
            check_result_text.value = ""
            page.update()
            return
        sc, st, cl = analyze(check_field.value)
        status_text = ("Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")) if current_lang == "ru" else st
        check_result_text.value = TEXTS[current_lang]["check_result"].format(sc, status_text)
        check_result_text.color = cl
        page.update()

    check_field.on_change = check_my_pwd
    tab_check = ft.Column([
        ft.Text("🔍", size=40, text_align=ft.TextAlign.CENTER),
        check_field,
        check_result_text
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    # --- ВКЛАДКА 3: ИНФО ---
    info_name = ft.Text("Евгений (makas)", size=22, weight=ft.FontWeight.BOLD)
    info_desc = ft.Text(TEXTS[current_lang]["about_me"], size=16, color=ft.Colors.GREY_400)
    
    tg_label = ft.Text(TEXTS[current_lang]["tg_label"], size=14, color=ft.Colors.GREY_500)
    tg_text = ft.Text("https://t.me/makas_1337", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD)
    
    gh_label = ft.Text(TEXTS[current_lang]["gh_label"], size=14, color=ft.Colors.GREY_500)
    gh_text = ft.Text("https://github.com/makas-innnn", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD)
    
    app_desc = ft.Text(TEXTS[current_lang]["app_desc"], size=14, text_align=ft.TextAlign.CENTER)

    async def copy_logs(e):
        sys_info = (
            f"--- PasswordGen Logs ---\n"
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}\n"
            f"Lang: {current_lang}, Theme: {current_theme}\n"
            f"History items: {len(history)}\n"
            f"----------------------"
        )
        await ft.Clipboard().set(sys_info)
        page.snack_bar = ft.SnackBar(content=ft.Text(TEXTS[current_lang]["logs_copied"], color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800)
        page.snack_bar.open = True
        page.update()

    async def copy_support(e):
        await ft.Clipboard().set("https://t.me/makas_ik")
        page.snack_bar = ft.SnackBar(content=ft.Text(TEXTS[current_lang]["support_copied"], color=ft.Colors.WHITE), bgcolor=ft.Colors.BLUE_800)
        page.snack_bar.open = True
        page.update()

    btn_copy_logs = ft.Button(TEXTS[current_lang]["copy_logs"], icon=ft.Icons.BUG_REPORT, on_click=lambda e: page.run_task(copy_logs, e), bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE)
    btn_support = ft.Button(TEXTS[current_lang]["support_btn"], icon=ft.Icons.SUPPORT_AGENT, on_click=lambda e: page.run_task(copy_support, e), bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    
    tab_info = ft.Column([
        ft.Icon(ft.Icons.PERSON, size=80), 
        info_name, 
        info_desc, 
        ft.Divider(height=15, color="transparent"),
        tg_label, 
        tg_text,
        ft.Divider(height=10, color="transparent"),
        gh_label, 
        gh_text,
        ft.Divider(height=20, color="transparent"), 
        ft.Text("PasswordGen v2.6", size=14, color=ft.Colors.GREY_400), 
        app_desc,
        ft.Divider(height=15, color="transparent"),
        btn_copy_logs,
        ft.Divider(height=10, color="transparent"),
        btn_support
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    # --- ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК ---
    content_container = ft.Container(expand=True, content=tab_gen)

    def switch_tab(index):
        if index == 0: content_container.content = tab_gen
        elif index == 1: content_container.content = tab_check
        else: content_container.content = tab_info
        page.update()

    txt_btn_gen = ft.Text("Генератор")
    txt_btn_check = ft.Text("Проверка")
    txt_btn_info = ft.Text("Инфо")
    
    tabs_row = ft.Row([
        ft.Button(content=txt_btn_gen, on_click=lambda e: switch_tab(0), width=100),
        ft.Button(content=txt_btn_check, on_click=lambda e: switch_tab(1), width=100),
        ft.Button(content=txt_btn_info, on_click=lambda e: switch_tab(2), width=100),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

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
        page.appbar.bgcolor = t["nav_bg"]
        page.update()

    def toggle_theme(e):
        nonlocal current_theme
        themes_list = list(THEMES.keys())
        idx = themes_list.index(current_theme)
        current_theme = themes_list[(idx + 1) % len(themes_list)]
        apply_theme()

    def toggle_lang(e):
        nonlocal current_lang
        current_lang = "en" if current_lang == "ru" else "ru"
        title_text.value = TEXTS[current_lang]["title"]
        len_label.value = f"{TEXTS[current_lang]['length']} {int(slider.value)}"
        sw_d.label = TEXTS[current_lang]["digits"]
        sw_s.label = TEXTS[current_lang]["symbols"]
        sw_c.label = TEXTS[current_lang]["no_confusing"]
        btn_gen.content = TEXTS[current_lang]["gen_btn"]
        btn_copy.content = TEXTS[current_lang]["copy_btn"]
        txt_btn_gen.value = TEXTS[current_lang]["nav_gen"]
        txt_btn_check.value = TEXTS[current_lang]["nav_check"]
        txt_btn_info.value = TEXTS[current_lang]["nav_info"]
        info_desc.value = TEXTS[current_lang]["about_me"]
        app_desc.value = TEXTS[current_lang]["app_desc"]
        history_title.value = TEXTS[current_lang]["history"]
        check_field.label = TEXTS[current_lang]["check_hint"]
        tg_label.value = TEXTS[current_lang]["tg_label"]
        gh_label.value = TEXTS[current_lang]["gh_label"]
        btn_copy_logs.content = TEXTS[current_lang]["copy_logs"]
        btn_support.content = TEXTS[current_lang]["support_btn"]
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text(TEXTS[current_lang]["app_title"]),
        center_title=True,
        actions=[
            ft.IconButton(ft.Icons.PALETTE, on_click=toggle_theme),
            ft.IconButton(ft.Icons.LANGUAGE, on_click=toggle_lang)
        ]
    )

    page.add(
        ft.Column([title_text, tabs_row, content_container], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    apply_theme()
    update_history_ui()

ft.run(main)
