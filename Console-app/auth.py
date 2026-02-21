from datetime import datetime

from utils import (
    clear_screen,
    print_header,
    pause,
    hash_password,
    get_input,
    username_validator,
    phone_validator,
    email_validator,
)
from database import load_users, save_users
from config import MEMBERSHIP_TYPES, ADMIN_USERNAME, ADMIN_PASSWORD


def admin_login() -> bool:
    clear_screen()
    print_header("👨‍💼 ADMIN KIRISH")

    username = get_input("Username: ")
    password = get_input("Parol: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("✅ Muvaffaqiyatli kirdingiz!")
        pause()
        return True

    print("❌ Username yoki parol xato!")
    pause()
    return False


def _is_username_taken(users: list[dict], username: str) -> bool:
    username_l = username.lower()
    return any(u.get("username", "").lower() == username_l for u in users)


def _choose_membership() -> str:
    while True:
        clear_screen()
        print_header("👤 A'ZOLIK PAKETINI TANLASH")
        print("1. 🥉 Bronze (Oddiy xizmat)")
        print("2. 🥈 Silver (⭐ Ustuvor xizmat)")
        print("3. 🥇 Gold (⭐ Ustuvor xizmat + 🚚 Bepul yetkazib berish)")
        print("=" * 50)

        azolik_choice = get_input("Tanlang (1-3): ", choices={"1", "2", "3"})
        if azolik_choice is None:
            return "Bronze"
        return MEMBERSHIP_TYPES[azolik_choice]


def customer_register() -> dict | None:
    clear_screen()
    print_header("📝 RO'YXATDAN O'TISH")

    users = load_users()

    ism = get_input("Ismingiz: ")
    if ism is None:
        return None

    while True:
        username = get_input(
            "Username (login uchun): ",
            validators=[username_validator()],
        )
        if username is None:
            return None
        if _is_username_taken(users, username):
            print("❌ Bu username band! Boshqa username kiriting.")
            continue
        break

    while True:
        password = get_input("Parol: ")
        if password is None:
            return None
        password_confirm = get_input("Parolni takrorlang: ")
        if password_confirm is None:
            return None

        if len(password) < 4:
            print("❌ Parol kamida 4 ta belgidan iborat bo'lishi kerak!")
            continue

        if password != password_confirm:
            print("❌ Parollar mos kelmadi!")
            continue

        break

    phone = get_input("Telefon raqam (+998901234567): ", validators=[phone_validator()])
    if phone is None:
        return None

    email = get_input("Email: ", validators=[email_validator()])
    if email is None:
        return None

    azolik_turi = _choose_membership()

    new_user = {
        "id": max([u.get("id", 0) for u in users], default=0) + 1,
        "ism": ism,
        "username": username,
        "password": hash_password(password),
        "phone": phone,
        "email": email,
        "azolik_turi": azolik_turi,
        "sana": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    users.append(new_user)
    save_users(users)

    print("\n✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!")
    print(f"A'zolik turi: {azolik_turi}")
    pause()
    return new_user


def customer_login() -> dict | None:
    clear_screen()
    print_header("🔐 MIJOZ KIRISH")

    users = load_users()

    username = get_input("Username: ")
    if username is None:
        return None
    password = get_input("Parol: ")
    if password is None:
        return None

    hashed_password = hash_password(password)

    username_l = username.lower()
    for user in users:
        if user.get("username", "").lower() == username_l and user.get("password") == hashed_password:
            print(f"✅ Xush kelibsiz, {user.get('ism', '')}!")
            pause()
            return user

    print("❌ Username yoki parol xato!")
    pause()
    return None


def customer_auth() -> dict | None:
    while True:
        clear_screen()
        print_header("🛍️ MIJOZ PANELI")
        print("1. 🔐 Kirish")
        print("2. 📝 Ro'yxatdan o'tish")
        print("0. 🔙 Orqaga")

        choice = get_input("Tanlang: ", choices={"0", "1", "2"})
        if choice is None:
            return None

        if choice == "1":
            user = customer_login()
            if user:
                return user
        elif choice == "2":
            return customer_register()
        else:
            return None
