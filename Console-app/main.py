from utils import clear_screen, print_header, pause, get_input
from auth import admin_login, customer_auth
from admin import admin_panel
from customer import CustomerPanel


def main() -> None:
    """Asosiy dastur"""
    while True:
        clear_screen()
        print_header("🏠 TECH HOUSE TIZIMIGA XUSH KELIBSIZ")
        print("1. 👨‍💼 Admin kirish")
        print("2. 🛍️  Mijoz kirish")
        print("3. 🚪 Chiqish")
        print("=" * 50)

        main_choice = get_input("Tanlang: ", choices={"1", "2", "3"})
        if main_choice is None:
            return

        if main_choice == "1":
            if admin_login():
                admin_panel()
        elif main_choice == "2":
            user = customer_auth()
            if user:
                CustomerPanel(user).run()
        else:
            clear_screen()
            print("\n👋 Xayr! Qaytib kelishingizni kutamiz!")
            break

if __name__ == "__main__":
    main()
