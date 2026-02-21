import os
import hashlib
import re
from typing import Any, Callable, Iterable, Optional

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
# Accept: +998901234567, 998901234567, 901234567, 90 123 45 67, etc.
_PHONE_RE = re.compile(r"^(\+?998)?\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}$|^(\+?998)?\d{9}$")

Validator = Callable[[str], tuple[bool, str]]

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str, width: int = 50) -> None:
    print("=" * width)
    print(title.center(width))
    print("=" * width)

def print_separator(width: int = 50) -> None:
    print("-" * width)

def pause(message: str = "Davom etish uchun Enter bosing...") -> None:
    try:
        input(message)
    except KeyboardInterrupt:
        print()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def format_currency(amount: float) -> str:
    try:
        return f"${float(amount):,.2f}"
    except Exception:
        return f"${amount}"

def get_next_id(items: list[dict]) -> int:
    if not items:
        return 1
    try:
        return max(int(item.get('id', 0)) for item in items) + 1
    except Exception:
        return len(items) + 1

def confirm_action(message: str = "Tasdiqlaysizmi?") -> bool:
    """Ha/Yo'q savoli (h/y)."""
    while True:
        try:
            response = input(f"{message} (h/y): ").strip().lower()
        except KeyboardInterrupt:
            print("\n\n❌ Bekor qilindi!")
            return False

        if response in {"h", "ha"}:
            return True
        if response in {"y", "yoq", "yo'q", "n", "no"}:
            return False

        print("❌ Iltimos, 'h' (ha) yoki 'y' (yo'q) kiriting.")

def _validate_pattern(pattern: re.Pattern, msg: str) -> Validator:
    def _v(s: str) -> tuple[bool, str]:
        return (bool(pattern.match(s)), msg)
    return _v

def username_validator() -> Validator:
    return _validate_pattern(_USERNAME_RE, "Username 3-20 belgi bo'lsin (harf/son/_).")

def email_validator() -> Validator:
    return _validate_pattern(_EMAIL_RE, "Email formati noto'g'ri (masalan: user@mail.com).")

def phone_validator() -> Validator:
    return _validate_pattern(_PHONE_RE, "Telefon formati noto'g'ri (masalan: +998901234567).")

def get_input(
    prompt: str,
    input_type: type = str,
    allow_empty: bool = False,
    *,
    choices: Optional[Iterable[Any]] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    validators: Optional[list[Validator]] = None,
    normalize: Optional[Callable[[str], str]] = lambda s: s.strip(),
) -> Any:
    """
    Input olish + qat'iy validatsiya.
    - choices: ruxsat berilgan qiymatlar
    - validators: str uchun qo'shimcha validatorlar (regex, uzunlik, ...)
    - min_value/max_value: int/float uchun diapazon
    """
    if validators is None:
        validators = []

    while True:
        try:
            raw = input(prompt)
        except KeyboardInterrupt:
            print("\n\n❌ Bekor qilindi!")
            return None

        raw = raw if normalize is None else normalize(raw)

        if not allow_empty and not str(raw).strip():
            print("❌ Bo'sh qoldirish mumkin emas!")
            continue

        if allow_empty and not str(raw).strip():
            return "" if input_type is str else None

        # validators for raw string
        if input_type is str:
            failed = False
            for v in validators:
                passed, msg = v(raw)
                if not passed:
                    print(f"❌ {msg}")
                    failed = True
                    break
            if failed:
                continue

        # cast
        try:
            if input_type is int:
                value = int(raw)
            elif input_type is float:
                value = float(raw)
            else:
                value = str(raw)
        except ValueError:
            print(f"❌ Xato! {input_type.__name__} qiymat kiriting.")
            continue
        except Exception:
            print("❌ Xato! Qaytadan urinib ko'ring.")
            continue

        # range checks
        if input_type in (int, float):
            if min_value is not None and value < min_value:
                print(f"❌ Qiymat kamida {min_value} bo'lishi kerak!")
                continue
            if max_value is not None and value > max_value:
                print(f"❌ Qiymat ko'pi bilan {max_value} bo'lishi kerak!")
                continue

        # choices check (after cast)
        if choices is not None:
            allowed = set(choices)
            if value not in allowed:
                print(f"❌ Noto'g'ri tanlov! Ruxsat: {', '.join(map(str, allowed))}")
                continue

        return value
