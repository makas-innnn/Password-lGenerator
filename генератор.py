import random
import string

def generate_strong_password(length):
    # Берем гарантированно по одному символу разных типов
    lo = random.choice(string.ascii_lowercase)
    up = random.choice(string.ascii_uppercase)
    di = random.choice(string.digits)
    sy = random.choice("!@#$%^&*")
    
    # Добиваем остаток
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    rest = ""
    for i in range(length - 4):
        rest += random.choice(all_chars)
    
    # Склеиваем и перемешиваем вручную (без shuffle)
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
    
    has_low = False
    has_up = False
    has_di = False
    has_sy = False
    
    for c in pwd:
        if c.islower(): has_low = True
        if c.isupper(): has_up = True
        if c.isdigit(): has_di = True
        if c in "!@#$%^&*": has_sy = True
        
    if has_low: score += 10
    if has_up: score += 15
    if has_di: score += 15
    if has_sy: score += 20
    
    if score > 100: score = 100
    
    if score >= 85:
        advice = "Идеален для: Банков, Госуслуг, Почты, ВК."
    elif score >= 60:
        advice = "Подойдет для: Инстаграм, ТикТок, ВК. Не для банка!"
    else:
        advice = "Только для: Временных аккаунтов."
        
    return score, advice

print("=== НАДЕЖНЫЕ ПАРОЛИ ===")

p1 = generate_strong_password(12)
s1, a1 = analyze(p1)
print("1. [12 симв.]:", p1)
print("Надежность:", s1, "%")
print("Совет:", a1)
print("")

p2 = generate_strong_password(16)
s2, a2 = analyze(p2)
print("2. [16 симв.]:", p2)
print("Надежность:", s2, "%")
print("Совет:", a2)
print("")

p3 = generate_strong_password(8)
s3, a3 = analyze(p3)
print("3. [8 симв.]:", p3)
print("Надежность:", s3, "%")
print("Совет:", a3)
print("")

p4 = generate_strong_password(20)
s4, a4 = analyze(p4)
print("4. [20 симв.]:", p4)
print("Надежность:", s4, "%")
print("Совет:", a4)
print("")

p5 = generate_strong_password(10)
s5, a5 = analyze(p5)
print("5. [10 симв.]:", p5)
print("Надежность:", s5, "%")
print("Совет:", a5)
print("")

print("=== ПОДБОР ===")
print("Тестируем 3-й пароль:", p3)
hacked = ""
for i in range(len(p3)):
    hacked += p3[i]
    print("Позиция", i+1, "подобрана. Результат:", hacked + "_" * (len(p3) - len(hacked)))

print("\nГотово!")
