from datetime import datetime

from utils import (
    clear_screen,
    print_header,
    print_separator,
    pause,
    get_input,
    confirm_action,
    format_currency,
)
from database import load_products, load_sales, save_sales
from config import DELIVERY_FEE, MEMBERSHIP_BENEFITS, SUPPORT_INFO


class CustomerPanel:
    def __init__(self, user: dict):
        self.user = user
        self.cart: list[dict] = []

    def run(self) -> None:
        while True:
            clear_screen()
            print_header(f"🛍️ XUSH KELIBSIZ, {self.user.get('ism','').upper()}!")
            print(f"A'zolik: {self.user.get('azolik_turi')} | Username: {self.user.get('username')}")
            print("=" * 50)
            print("1. 🛒 Mahsulotlarni ko'rish va Xarid")
            print("2. 🧺 Savatni boshqarish")
            print("3. 💳 Checkout (To'lov)")
            print("4. 👤 A'zolik ma'lumotlari")
            print("5. 📞 Support")
            print("0. 🔙 Chiqish")
            print("=" * 50)

            choice = get_input("Tanlang: ", choices={"0", "1", "2", "3", "4", "5"})
            if choice is None:
                return

            if choice == "1":
                self.product_browsing_flow()
            elif choice == "2":
                self.manage_cart()
            elif choice == "3":
                self.checkout_process()
            elif choice == "4":
                self.show_membership_info()
            elif choice == "5":
                self.show_support()
            else:
                break

    def product_browsing_flow(self) -> None:
        clear_screen()
        print_header("🛒 MAHSULOTLARNI KO'RISH")
        print("1. Barcha mahsulotlar")
        print("2. Kategoriya bo'yicha")
        print("3. Qidiruv (Nomi bo'yicha)")
        print("0. Orqaga")
        print("=" * 50)

        view_type = get_input("Tanlang: ", choices={"0", "1", "2", "3"})
        if view_type in (None, "0"):
            return

        products = load_products()
        temp_list: list[dict] = []

        if view_type == "1":
            temp_list = products
        elif view_type == "2":
            clear_screen()
            print("Mavjud kategoriyalar:")
            categories = sorted(set(p.get("kategoriya", "") for p in products))
            for cat in categories:
                print(f"  - {cat}")
            cat_input = get_input("\nKategoriya kiriting: ")
            if cat_input is None:
                return
            temp_list = [p for p in products if str(p.get("kategoriya", "")).lower() == cat_input.lower()]
        else:
            search_key = get_input("Qidirish (mahsulot nomi): ")
            if search_key is None:
                return
            temp_list = [p for p in products if search_key.lower() in str(p.get("nomi", "")).lower()]

        if not temp_list:
            print("❌ Mahsulot topilmadi!")
            pause()
            return

        self.display_products_and_add_to_cart(temp_list)

    def display_products_and_add_to_cart(self, products_list: list[dict]) -> None:
        clear_screen()
        print_header("📋 NATIJALAR", 90)
        print(f"{'ID':<5} {'Nomi':<40} {'Narxi':<12} {'Holati':<10} {'Kategoriya':<15}")
        print_separator(90)

        for item in products_list:
            print(
                f"{item.get('id', ''):<5} "
                f"{str(item.get('nomi','')):<40} "
                f"{format_currency(item.get('narxi', 0)):<12} "
                f"{str(item.get('holati','')):<10} "
                f"{str(item.get('kategoriya','')):<15}"
            )

        print("=" * 90)

        selected_id = get_input("\nSavatga solish uchun ID kiriting (0 - bekor): ", int, min_value=0)
        if selected_id in (None, 0):
            return

        mahsulot = next((p for p in products_list if p.get("id") == selected_id), None)
        if mahsulot is None:
            print("❌ Noto'g'ri ID!")
            pause()
            return

        if str(mahsulot.get("holati", "")).lower() != "mavjud":
            print("❌ Bu mahsulot hozirda mavjud emas!")
            pause()
            return

        qty = get_input("Soni: ", int, min_value=1)
        if qty is None:
            return

        for cart_item in self.cart:
            if cart_item["id"] == mahsulot["id"]:
                cart_item["soni"] += qty
                print(f"✅ Savatdagi '{mahsulot['nomi']}' soni yangilandi!")
                pause()
                return

        self.cart.append(
            {
                "id": mahsulot["id"],
                "nomi": mahsulot["nomi"],
                "narxi": mahsulot["narxi"],
                "soni": qty,
            }
        )

        print(f"✅ '{mahsulot['nomi']}' savatga qo'shildi!")
        pause()

    def manage_cart(self) -> None:
        if not self.cart:
            clear_screen()
            print("🧺 Savatingiz bo'sh!")
            pause()
            return

        while True:
            clear_screen()
            print_header("🧺 SAVAT", 90)
            print(f"{'ID':<5} {'Nomi':<35} {'Narxi':<12} {'Soni':<10} {'Jami':<12}")
            print_separator(90)

            total = 0.0
            for item in self.cart:
                item_total = float(item["narxi"]) * int(item["soni"])
                total += item_total
                print(
                    f"{item['id']:<5} {item['nomi']:<35} {format_currency(item['narxi']):<12} "
                    f"{item['soni']:<10} {format_currency(item_total):<12}"
                )

            print_separator(90)
            print(f"{'JAMI:':<62} {format_currency(total):<12}")
            print("=" * 90)

            print("\n1. Hajmini o'zgartirish")
            print("2. Mahsulotni o'chirish")
            print("3. Savatni tozalash")
            print("0. Orqaga")

            cart_action = get_input("Tanlang: ", choices={"0", "1", "2", "3"})
            if cart_action is None:
                return

            if cart_action == "1":
                self.update_cart_quantity()
            elif cart_action == "2":
                self.remove_from_cart()
            elif cart_action == "3":
                if confirm_action("Savatni tozalashni tasdiqlaysizmi?"):
                    self.cart.clear()
                    print("✅ Savat tozalandi!")
                    pause()
                    break
            else:
                break

    def update_cart_quantity(self) -> None:
        target_id = get_input("Mahsulot ID sini kiriting: ", int, min_value=1)
        if target_id is None:
            return

        for item in self.cart:
            if item["id"] == target_id:
                new_qty = get_input(f"Yangi son ({item['nomi']}): ", int, min_value=1)
                if new_qty is None:
                    return
                item["soni"] = new_qty
                print("✅ Hajm yangilandi!")
                pause()
                return

        print("❌ Bunday mahsulot savatda yo'q!")
        pause()

    def remove_from_cart(self) -> None:
        remove_id = get_input("O'chirish uchun ID kiriting: ", int, min_value=1)
        if remove_id is None:
            return

        for i, item in enumerate(self.cart):
            if item["id"] == remove_id:
                if confirm_action(f"'{item['nomi']}'ni o'chirmoqchimisiz?"):
                    removed = self.cart.pop(i)
                    print(f"✅ '{removed['nomi']}' savatdan o'chirildi!")
                else:
                    print("❌ Bekor qilindi.")
                pause()
                return

        print("❌ Bunday mahsulot savatda yo'q!")
        pause()

    def checkout_process(self) -> None:
        if not self.cart:
            clear_screen()
            print("🧺 Savat bo'sh, xarid qila olmaysiz!")
            pause()
            return

        clear_screen()
        print_header("💳 CHECKOUT (TO'LOV)", 90)

        sub_total = sum(float(item["narxi"]) * int(item["soni"]) for item in self.cart)

        print("Savatingizdagi mahsulotlar:")
        print_separator(90)
        for item in self.cart:
            line_total = float(item["narxi"]) * int(item["soni"])
            print(f"  ID:{item['id']} | {item['nomi']} x{item['soni']} = {format_currency(line_total)}")
        print_separator(90)
        print(f"Mahsulotlar narxi: {format_currency(sub_total)}\n")

        print("Yetkazib berish usuli:")
        print("1. Uyga yetkazish")
        print("2. Do'kondan olib ketish")

        delivery_method = get_input("Tanlang: ", choices={"1", "2"})
        if delivery_method is None:
            return

        delivery_fee = 0.0
        if delivery_method == "1":
            if self.user.get("azolik_turi") == "Gold":
                delivery_fee = 0.0
                print("\n🥇 Gold A'zo - Yetkazib berish BEPUL!")
            else:
                delivery_fee = float(DELIVERY_FEE)
                print(f"\nYetkazib berish narxi: {format_currency(delivery_fee)}")
        else:
            print("\n✅ Do'kondan olib ketasiz (Bepul)")

        total = sub_total + delivery_fee

        print("\n" + "=" * 90)
        print(f"💰 JAMI TO'LOV: {format_currency(total)}")
        print("=" * 90)

        if not confirm_action("\nXaridni tasdiqlaysizmi?"):
            print("❌ Xarid bekor qilindi.")
            pause()
            return

        sale = {
            "mijoz": self.user.get("ism"),
            "username": self.user.get("username"),
            "azolik_turi": self.user.get("azolik_turi"),
            "mahsulotlar": [dict(x) for x in self.cart],
            "yetkazish": delivery_fee,
            "jami": total,
            "sana": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        sales = load_sales()
        sales.append(sale)
        save_sales(sales)

        self.cart.clear()

        print("\n✅ Xaridingiz uchun rahmat!")
        print("Tez orada siz bilan bog'lanamiz!")
        pause()

    def show_membership_info(self) -> None:
        clear_screen()
        print_header("👤 A'ZOLIK MA'LUMOTLARI")
        print(f"Ism: {self.user.get('ism')}")
        print(f"Username: {self.user.get('username')}")
        print(f"Telefon: {self.user.get('phone')}")
        print(f"Email: {self.user.get('email')}")
        print(f"A'zolik turi: {self.user.get('azolik_turi')}")
        print(f"Ro'yxatdan o'tgan: {self.user.get('sana')}")
        print()
        print("Imtiyozlar:")

        benefits = MEMBERSHIP_BENEFITS.get(self.user.get("azolik_turi"), [])
        for benefit in benefits:
            print(f"  {benefit}")
        print("=" * 50)
        pause()

    def show_support(self) -> None:
        clear_screen()
        print_header("📞 QO'LLAB-QUVVATLASH")
        print("Bizning jamoamiz sizga yordam berishga tayyor!")
        print()
        print(f"📱 Telefon: {SUPPORT_INFO['phone']}")
        print(f"📧 Email: {SUPPORT_INFO['email']}")
        print(f"🌐 Website: {SUPPORT_INFO['website']}")
        print(f"⏰ Ish vaqti: {SUPPORT_INFO['hours']}")
        print("=" * 50)
        pause()
