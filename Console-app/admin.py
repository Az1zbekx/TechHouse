"""Admin panel moduli"""

from utils import (
    clear_screen,
    print_header,
    print_separator,
    pause,
    get_input,
    confirm_action,
    format_currency,
    get_next_id,
)
from database import load_products, save_products, load_sales, load_users


def admin_panel() -> None:
    """Admin panel asosiy menyu"""
    while True:
        clear_screen()
        print_header("👨‍💼 ADMIN PANEL")
        print("1. ➕ Mahsulot qo'shish")
        print("2. ✏️  Mahsulotni tahrirlash")
        print("3. ❌ Mahsulotni o'chirish")
        print("4. 📋 Barcha mahsulotlarni ko'rish")
        print("5. 📊 Sotuvlar tarixini ko'rish")
        print("6. 👥 Foydalanuvchilarni ko'rish")
        print("7. 📈 Statistika")
        print("0. 🔙 Orqaga")
        print("=" * 50)

        choice = get_input("Tanlang: ", choices={"0", "1", "2", "3", "4", "5", "6", "7"})
        if choice is None:
            return

        if choice == "1":
            add_product()
        elif choice == "2":
            edit_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_all_products()
        elif choice == "5":
            view_sales()
        elif choice == "6":
            view_users()
        elif choice == "7":
            view_statistics()
        else:
            break


def _suggest_categories(products: list[dict]) -> list[str]:
    defaults = ["Oshxona", "Tozalash", "Uy"]
    found = [str(p.get("kategoriya", "")).strip() for p in products if p.get("kategoriya")]
    cats = []
    for c in defaults + found:
        if c and c not in cats:
            cats.append(c)
    return cats


def _normalize_status(s: str) -> str:
    s = (s or "").strip().lower()
    if s in {"mavjud", "bor"}:
        return "Mavjud"
    if s in {"tugagan", "yoq", "yo'q"}:
        return "Tugagan"
    # fallback: title case
    return s.title() if s else "Mavjud"


def add_product() -> None:
    clear_screen()
    print_header("➕ YANGI MAHSULOT QO'SHISH")

    products = load_products()
    new_id = get_next_id(products)

    nomi = get_input("Mahsulot nomi: ")
    if nomi is None:
        return

    narxi = get_input("Narxi ($): ", float, min_value=0.01)
    if narxi is None:
        return

    cats = _suggest_categories(products)
    print("\nKategoriyalar: " + ", ".join(cats))
    kategoriya = get_input("Kategoriya: ")
    if kategoriya is None:
        return
    kategoriya = kategoriya.strip().title()

    print("\nHolat: Mavjud / Tugagan")
    holati_raw = get_input("Holati: ", choices={"Mavjud", "Tugagan", "mavjud", "tugagan"})
    if holati_raw is None:
        return
    holati = _normalize_status(holati_raw)

    new_product = {"id": new_id, "nomi": nomi, "narxi": narxi, "kategoriya": kategoriya, "holati": holati}

    products.append(new_product)
    save_products(products)

    print(f"\n✅ Mahsulot muvaffaqiyatli qo'shildi! (ID: {new_id})")
    pause()


def edit_product() -> None:
    clear_screen()
    print_header("✏️ MAHSULOTNI TAHRIRLASH")

    products = load_products()
    view_all_products(pause_after=False)

    product_id = get_input("\nTahrirlash uchun ID kiriting (0 - bekor): ", int, min_value=0)
    if product_id in (None, 0):
        return

    product = next((p for p in products if p.get("id") == product_id), None)
    if not product:
        print("❌ Bunday ID topilmadi!")
        pause()
        return

    print("\nHozirgi ma'lumotlar:")
    print(f"Nomi: {product.get('nomi')}")
    print(f"Narxi: {format_currency(product.get('narxi', 0))}")
    print(f"Kategoriya: {product.get('kategoriya')}")
    print(f"Holati: {product.get('holati')}")
    print("\nYangi ma'lumotlar kiriting (o'zgartirmaslik uchun Enter bosing):")

    nomi = get_input(f"Yangi nomi [{product.get('nomi')}]: ", allow_empty=True)
    if nomi:
        product["nomi"] = nomi

    narxi = get_input(f"Yangi narxi [{product.get('narxi')}]: ", float, allow_empty=True, min_value=0.01)
    if narxi is not None:
        product["narxi"] = narxi

    kategoriya = get_input(f"Yangi kategoriya [{product.get('kategoriya')}]: ", allow_empty=True)
    if kategoriya:
        product["kategoriya"] = kategoriya.strip().title()

    holati_raw = get_input(
        f"Yangi holat [{product.get('holati')}]: ",
        allow_empty=True,
        choices={"", "Mavjud", "Tugagan", "mavjud", "tugagan"},
    )
    if holati_raw:
        product["holati"] = _normalize_status(holati_raw)

    save_products(products)
    print("\n✅ Mahsulot yangilandi!")
    pause()


def delete_product() -> None:
    clear_screen()
    print_header("❌ MAHSULOTNI O'CHIRISH")

    products = load_products()
    view_all_products(pause_after=False)

    delete_id = get_input("\nO'chirish uchun ID kiriting (0 - bekor): ", int, min_value=0)
    if delete_id in (None, 0):
        return

    for i, product in enumerate(products):
        if product.get("id") == delete_id:
            if confirm_action(f"'{product.get('nomi')}'ni o'chirmoqchimisiz?"):
                deleted = products.pop(i)
                save_products(products)
                print(f"✅ '{deleted.get('nomi')}' o'chirildi!")
            else:
                print("❌ Bekor qilindi.")
            pause()
            return

    print("❌ Bunday ID topilmadi!")
    pause()


def view_all_products(pause_after: bool = True) -> None:
    clear_screen()
    print_header("📋 BARCHA MAHSULOTLAR", 95)

    products = load_products()
    if not products:
        print("Mahsulotlar yo'q.")
    else:
        print(f"{'ID':<5} {'Nomi':<35} {'Narxi':<12} {'Kategoriya':<18} {'Holati':<10}")
        print_separator(95)

        for product in products:
            print(
                f"{product.get('id', ''):<5} {str(product.get('nomi','')):<35} {format_currency(product.get('narxi', 0)):<12} "
                f"{str(product.get('kategoriya','')):<18} {str(product.get('holati','')):<10}"
            )

    print("=" * 95)
    if pause_after:
        pause()


def view_sales() -> None:
    clear_screen()
    print_header("📊 SOTUVLAR TARIXI", 110)

    sales = load_sales()
    if not sales:
        print("Hozircha sotuvlar yo'q.")
        print("=" * 110)
        pause()
        return

    total_revenue = 0.0
    for i, sale in enumerate(sales, 1):
        print(f"\n🛒 Sotuv #{i}")
        print(f"   Mijoz: {sale.get('mijoz')} (Username: {sale.get('username')}) [{sale.get('azolik_turi')}] ")
        print(f"   Sana: {sale.get('sana')}")
        print("   Mahsulotlar:")

        for item in sale.get("mahsulotlar", []):
            line_total = float(item.get("narxi", 0)) * int(item.get("soni", 0))
            print(f"      - ID:{item.get('id')} | {item.get('nomi')} x{item.get('soni')} = {format_currency(line_total)}")

        print(f"   Yetkazib berish: {format_currency(sale.get('yetkazish', 0))}")
        print(f"   💰 JAMI: {format_currency(sale.get('jami', 0))}")
        print_separator(110)

        try:
            total_revenue += float(sale.get("jami", 0))
        except Exception:
            pass

    print(f"\n💵 UMUMIY DAROMAD: {format_currency(total_revenue)}")
    print("=" * 110)
    pause()


def view_users() -> None:
    clear_screen()
    print_header("👥 RO'YXATDAN O'TGAN FOYDALANUVCHILAR", 110)

    users = load_users()
    if not users:
        print("Hozircha foydalanuvchilar yo'q.")
        print("=" * 110)
        pause()
        return

    print("{:<5} {:<20} {:<15} {:<10} {:<16} {:<25}".format('ID','Ism','Username',"A'zolik",'Telefon','Email'))
    print_separator(110)

    for user in users:
        print(
            f"{user.get('id',''):<5} {str(user.get('ism','')):<20} {str(user.get('username','')):<15} "
            f"{str(user.get('azolik_turi','')):<10} {str(user.get('phone','')):<16} {str(user.get('email','')):<25}"
        )

    print("=" * 110)
    pause()


def view_statistics() -> None:
    clear_screen()
    print_header("📈 STATISTIKA")

    products = load_products()
    sales = load_sales()
    users = load_users()

    total_products = len(products)
    available_products = len([p for p in products if str(p.get("holati", "")).lower() == "mavjud"])

    total_sales = len(sales)
    try:
        total_revenue = sum(float(s.get("jami", 0)) for s in sales)
    except Exception:
        total_revenue = 0.0

    total_users = len(users)
    gold_users = len([u for u in users if u.get("azolik_turi") == "Gold"])
    silver_users = len([u for u in users if u.get("azolik_turi") == "Silver"])
    bronze_users = len([u for u in users if u.get("azolik_turi") == "Bronze"])

    print("\n📦 MAHSULOTLAR:")
    print(f"   Jami mahsulotlar: {total_products}")
    print(f"   Mavjud: {available_products}")
    print(f"   Tugagan: {total_products - available_products}")

    print("\n💰 SOTUVLAR:")
    print(f"   Jami sotuvlar: {total_sales}")
    print(f"   Umumiy daromad: {format_currency(total_revenue)}")
    if total_sales > 0:
        print(f"   O'rtacha sotuv: {format_currency(total_revenue / total_sales)}")

    print("\n👥 FOYDALANUVCHILAR:")
    print(f"   Jami: {total_users}")
    print(f"   🥇 Gold: {gold_users}")
    print(f"   🥈 Silver: {silver_users}")
    print(f"   🥉 Bronze: {bronze_users}")

    print("=" * 50)
    pause()
