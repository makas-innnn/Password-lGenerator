import flet as ft
import random
import string
import json

# --- ПЕРЕВОДЫ ---
TEXTS = {
    "ru": {
        "title": "🔐 Генератор паролей", "app_title": "PasswordGen", "gen_btn": "Сгенерировать",
        "copy_btn": "Копировать", "length": "Длина пароля:", "digits": "Цифры (0-9)",
        "symbols": "Спецсимволы (!@#$)", "no_confusing": "Без похожих (l, 1, O)",
        "copied": "Пароль скопирован!", "nav_gen": "Генератор", "nav_info": "Инфо",
        "about_me": "Начинающий кодер, делаю что в кайф", "tg": "Telegram", "github": "GitHub",
        "app_desc": "Безопасный офлайн-генератор.\nДанные не покидают устройство.",
        "tg_copied": "Ссылка на Telegram скопирована!", "gh_copied": "Ссылка на GitHub скопирована!",
        "history": "История (последние 5)",
        "check_btn": "Проверить свой пароль", "check_hint": "Введите пароль для проверки...",
        "check_result": "Надежность: {}% ({})", "nav_check": "Проверка",
        "tg_label": "Телеграм канал создателя:", "gh_label": "GitHub создателя:"
    },
    "en": {
        "title": "🔐 Password Generator", "app_title": "PasswordGen", "gen_btn": "Generate",
        "copy_btn": "Copy", "length": "Password length:", "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#$)", "no_confusing": "No confusing (l, 1, O)",
        "copied": "Password copied!", "nav_gen": "Generator", "nav_info": "Info",
        "about_me": "Beginner coder, doing what I love", "tg": "Telegram", "github": "GitHub",
        "app_desc": "Secure offline generator.\nData never leaves your device.",
        "tg_copied": "Telegram link copied!", "gh_copied": "GitHub link copied!",
        "history": "History (last 5)",
        "check_btn": "Check your password", "check_hint": "Enter password to check...",
        "check_result": "Strength: {}% ({})", "nav_check": "Check",
        "tg_label": "Creator's Telegram channel:", "gh_label": "Creator's GitHub:"
    }
}

# --- ТЕМЫ ---
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
    if not pwd: return 0, "Weak", ft.Colors.RED
    s = sum([10 if len(pwd)>=8 else 0, 15 if len(pwd)>=12 else 0, 15 if len(pwd)>=16 else 0,
             10 if any(c.islower() for c in pwd) else 0, 15 if any(c.isupper() for c in pwd) else 0,
             15 if any(c.isdigit() for c in pwd) else 0, 20 if any(c in "!@#$%^&*" for c in pwd) else 0])
    s = min(s, 100)
    return (s, "Strong", ft.Colors.GREEN) if s >= 85 else ((s, "Medium", ft.Colors.ORANGE) if s >= 60 else (s, "Weak", ft.Colors.RED))

def main(page: ft.Page):
    page.title = "PasswordGen"
    page.padding = 20
    
    state = {"lang": "ru", "theme": "dark", "pwd": "", "history": []}

    try:
        saved_hist = page.client_storage.get("history")
        if saved_hist: state["history"] = json.loads(saved_hist)
    except: pass

    title_text = ft.Text(TEXTS[state["lang"]]["title"], size=28, weight=ft.FontWeight.BOLD)
    
    # --- ВКЛАДКА 1: ГЕНЕРАТОР ---
    pwd_field = ft.TextField(value="", read_only=True, text_align=ft.TextAlign.CENTER, text_size=20)
    eye_icon = ft.IconButton(ft.Icons.VISIBILITY, tooltip="Скрыть/Показать")
    strength_bar = ft.ProgressBar(width=300, value=0, bgcolor=ft.Colors.GREY_800, color=ft.Colors.RED)
    str_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    
    slider = ft.Slider(min=8, max=32, divisions=24, value=16, label="Длина: {value}")
    len_label = ft.Text(f"{TEXTS[state['lang']]['length']} 16", size=16)

    def set_len(v): 
        slider.value = v
        len_label.value = f"{TEXTS[state['lang']]['length']} {v}"
        page.update()

    len_btns = ft.Row([ft.Button(content=str(v), on_click=lambda e, v=v: set_len(v), width=45, height=40) for v in [8,12,16,20,32]], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
    sw_d = ft.Switch(label=TEXTS[state["lang"]]["digits"], value=True)
    sw_s = ft.Switch(label=TEXTS[state["lang"]]["symbols"], value=True)
    sw_c = ft.Switch(label=TEXTS[state["lang"]]["no_confusing"], value=False)
    
    btn_gen = ft.Button(content=TEXTS[state["lang"]]["gen_btn"], width=300, height=50, color=ft.Colors.WHITE)
    btn_copy = ft.Button(content=TEXTS[state["lang"]]["copy_btn"], width=300, height=50, color=ft.Colors.WHITE)

    history_title = ft.Text(TEXTS[state["lang"]]["history"], size=16, weight=ft.FontWeight.BOLD)
    history_col = ft.Column(spacing=5)

    async def copy_to_clipboard(val, msg):
        if not val: return
        await ft.Clipboard().set(val)
        page.snack_bar = ft.SnackBar(content=ft.Text(msg, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800)
        page.snack_bar.open = True
        page.update()

    def update_history_ui():
        history_col.controls.clear()
        for p in state["history"]:
            row = ft.Row([
                ft.Text(p, size=14, color=ft.Colors.GREY_400),
                ft.IconButton(ft.Icons.COPY, icon_size=16, tooltip="Копировать",
                    on_click=lambda e, val=p: page.run_task(copy_to_clipboard, val, TEXTS[state["lang"]]["copied"]))
            ], alignment=ft.MainAxisAlignment.CENTER)
            history_col.controls.append(row)

    def toggle_visibility(e):
        if pwd_field.password:
            pwd_field.password = False
            pwd_field.value = state["pwd"]
            eye_icon.icon = ft.Icons.VISIBILITY_OFF
        else:
            pwd_field.password = True
            pwd_field.value = "•" * len(state["pwd"])
            eye_icon.icon = ft.Icons.VISIBILITY
        page.update()

    def generate(e):
        state["pwd"] = gen_pwd(int(slider.value), sw_d.value, sw_s.value, sw_c.value)
        if pwd_field.password:
            pwd_field.value = "•" * len(state["pwd"])
        else:
            pwd_field.value = state["pwd"]
            
        sc, st, cl = analyze(state["pwd"])
        strength_bar.value = sc / 100
        strength_bar.color = cl
        status_text = ("Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")) if state["lang"] == "ru" else st
        str_text.value = f"Надежность: {sc}% ({status_text})" if state["lang"] == "ru" else f"Strength: {sc}% ({status_text})"
        str_text.color = cl
        
        state["history"].insert(0, state["pwd"])
        if len(state["history"]) > 5: state["history"].pop()
        update_history_ui()
        
        try: page.client_storage.set("history", json.dumps(state["history"]))
        except: pass
            
        page.update()

    eye_icon.on_click = toggle_visibility
    btn_gen.on_click = generate
    btn_copy.on_click = lambda e: page.run_task(copy_to_clipboard, state["pwd"], TEXTS[state["lang"]]["copied"])

    pwd_row = ft.Row([pwd_field, eye_icon], alignment=ft.MainAxisAlignment.CENTER)
    tab_gen = ft.Column([
        pwd_row, strength_bar, str_text, len_label, slider, len_btns, 
        sw_d, sw_s, sw_c, btn_gen, btn_copy,
        ft.Divider(height=15, color="transparent"),
        history_title,
        history_col
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    # --- ВКЛАДКА 2: ПРОВЕРКА ---
    check_field = ft.TextField(label=TEXTS[state["lang"]]["check_hint"], password=True, can_reveal_password=True, text_size=16)
    check_result_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

    def check_my_pwd(e):
        if not check_field.value:
            check_result_text.value = ""
            page.update()
            return
        sc, st, cl = analyze(check_field.value)
        status_text = ("Надежный" if st == "Strong" else ("Средний" if st == "Medium" else "Слабый")) if state["lang"] == "ru" else st
        check_result_text.value = TEXTS[state["lang"]]["check_result"].format(sc, status_text)
        check_result_text.color = cl
        page.update()

    check_field.on_change = check_my_pwd
    tab_check = ft.Column([
        ft.Text("🔍", size=40, text_align=ft.TextAlign.CENTER),
        check_field,
        check_result_text
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    # --- ВКЛАДКА 3: ИНФО (Текст-ссылки) ---
    info_name = ft.Text("Евгений (makas)", size=22, weight=ft.FontWeight.BOLD)
    info_desc = ft.Text(TEXTS[state["lang"]]["about_me"], size=16, color=ft.Colors.GREY_400)
    
    # Просто текст с on_click (без асинхронных run_task для надежности)
    link_tg = ft.Text(
        "https://t.me/makas_1337", 
        size=16, 
        color=ft.Colors.BLUE_400, 
        weight=ft.FontWeight.BOLD,
        on_click=lambda e: page.launch_url("https://t.me/makas_1337")
    )
    link_gh = ft.Text(
        "https://github.com/makas-innnn", 
        size=16, 
        color=ft.Colors.BLUE_400, 
        weight=ft.FontWeight.BOLD,
        on_click=lambda e: page.launch_url("https://github.com/makas-innnn")
    )
    
    app_desc = ft.Text(TEXTS[state["lang"]]["app_desc"], size=14, text_align=ft.TextAlign.CENTER)
    
    tab_info = ft.Column([
        ft.Icon(ft.Icons.PERSON, size=80), info_name, info_desc, 
        ft.Divider(height=10, color="transparent"),
        ft.Text(TEXTS[state["lang"]]["tg_label"], size=14, color=ft.Colors.GREY_500),
        link_tg,
        ft.Divider(height=10, color="transparent"),
        ft.Text(TEXTS[state["lang"]]["gh_label"], size=14, color=ft.Colors.GREY_500),
        link_gh,
        ft.Divider(height=20, color="transparent"), 
        ft.Text("PasswordGen v2.3", size=14, color=ft.Colors.GREY_400), 
        app_desc
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

    # --- ТЕМЫ И ЯЗЫК ---
    def apply_theme():
        t = THEMES[state["theme"]]
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
        themes_list = list(THEMES.keys())
        idx = themes_list.index(state["theme"])
        state["theme"] = themes_list[(idx + 1) % len(themes_list)]
        apply_theme()

    def update_ui_texts():
        title_text.value = TEXTS[state["lang"]]["title"]
        len_label.value = f"{TEXTS[state['lang']]['length']} {int(slider.value)}"
        sw_d.label = TEXTS[state["lang"]]["digits"]
        sw_s.label = TEXTS[state["lang"]]["symbols"]
        sw_c.label = TEXTS[state["lang"]]["no_confusing"]
        btn_gen.content = TEXTS[state["lang"]]["gen_btn"]
        btn_copy.content = TEXTS[state["lang"]]["copy_btn"]
        txt_btn_gen.value = TEXTS[state["lang"]]["nav_gen"]
        txt_btn_check.value = TEXTS[state["lang"]]["nav_check"]
        txt_btn_info.value = TEXTS[state["lang"]]["nav_info"]
        info_desc.value = TEXTS[state["lang"]]["about_me"]
        app_desc.value = TEXTS[state["lang"]]["app_desc"]
        history_title.value = TEXTS[state["lang"]]["history"]
        check_field.label = TEXTS[state["lang"]]["check_hint"]
        tg_label.value = TEXTS[state["lang"]]["tg_label"]
        gh_label.value = TEXTS[state["lang"]]["gh_label"]
        page.update()

    def toggle_lang(e):
        state["lang"] = "en" if state["lang"] == "ru" else "ru"
        update_ui_texts()

    # Для смены текста подписей (создаем переменные для update_ui_texts)
    tg_label = ft.Text(TEXTS[state["lang"]]["tg_label"], size=14, color=ft.Colors.GREY_500)
    gh_label = ft.Text(TEXTS[state["lang"]]["gh_label"], size=14, color=ft.Colors.GREY_500)
    
    # Пересобираем tab_info с этими переменными
    tab_info = ft.Column([
        ft.Icon(ft.Icons.PERSON, size=80), info_name, info_desc, 
        ft.Divider(height=10, color="transparent"),
        tg_label, link_tg,
        ft.Divider(height=10, color="transparent"),
        gh_label, link_gh,
        ft.Divider(height=20, color="transparent"), 
        ft.Text("PasswordGen v2.3", size=14, color=ft.Colors.GREY_400), 
        app_desc
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

    page.appbar = ft.AppBar(
        title=ft.Text(TEXTS[state["lang"]]["app_title"]),
        center_title=True,
        actions=[
            ft.IconButton(ft.Icons.PALETTE, on_click=toggle_theme, tooltip="Сменить тему"),
            ft.IconButton(ft.Icons.LANGUAGE, on_click=toggle_lang, tooltip="Сменить язык")
        ]
    )

    page.add(
        ft.Column([title_text, tabs_row, content_container], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    apply_theme()
    update_history_ui()

ft.run(main)
