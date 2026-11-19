"""Ortaq köməkçilər: formatlama, variantların qarışdırılması, Azərbaycan şəkilçiləri."""
import json
import re
import random
from fractions import Fraction as F
from pathlib import Path

LETTERS = "ABCDE"
OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "questions"


def fr(x):
    """Fraction/int -> 'a/b' və ya tam ədəd mətni."""
    if isinstance(x, str):
        return x
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def dec(x):
    """Onluq kəsri vergüllə yaz (Azərbaycan qaydası)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d != 1:  # dövri kəsr — adi kəsr kimi yaz
        return fr(x)
    s = f"{float(x):.6f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _fallback(a):
    """Rəqəm cavab üçün əlavə yanlış variantlar. «12π», «5√3 sm» kimi mətnlərdə rəqəm hissəsi dəyişdirilir."""
    if isinstance(a, str):
        m = re.match(r"^(-?\d+(?:/\d+)?)(\D.*)$", a)
        if not m:
            return []
        n, rest = F(m.group(1)), m.group(2)
        return [fr(v) + rest for v in (n + 1, n - 1, n + 2, 2 * n, n + 3, 3 * n) if v > 0]
    a = F(a)
    out = [a + 1, a - 1, a + 2, a - 2, 2 * a, -a, a + 3, a * 3, a + 5, a - 4]
    return out


# Rəqəmin oxunuşunun son sözü: (son sait, saitlə bitirmi)
_UNITS = {0: ("ı", False), 1: ("i", False), 2: ("i", True), 3: ("ü", False), 4: ("ö", False),
          5: ("e", False), 6: ("ı", True), 7: ("i", True), 8: ("i", False), 9: ("u", False)}
_TENS = {1: ("o", False), 2: ("i", True), 3: ("u", False), 4: ("ı", False), 5: ("i", True),
         6: ("ı", False), 7: ("i", False), 8: ("ə", False), 9: ("a", False)}


def _last_word(n):
    """Ədədin (və ya kəsrin surətinin) oxunuşundakı son sözün son saiti."""
    if isinstance(n, str):
        m = re.search(r"\d+", n.split("/")[0])
        n = int(m.group()) if m else 0
    n = abs(F(n).numerator)
    if n == 0 or n % 10:
        return _UNITS[n % 10]
    if n % 100:
        return _TENS[(n // 10) % 10]
    if n % 1000:
        return ("ü", False)  # yüz
    return ("i", False)  # min


def cop(n):
    """Xəbər şəkilçisi: 6 → «6-dır», 3 → «3-dür», 10 → «10-dur»."""
    v, _ = _last_word(n)
    suf = {"a": "dır", "ı": "dır", "e": "dir", "ə": "dir", "i": "dir", "o": "dur", "u": "dur", "ö": "dür", "ü": "dür"}[v]
    return f"{fr(n)}-{suf}"


def dat(n):
    """Yönlük hal: 2 → «2-yə», 6 → «6-ya», 3 → «3-ə», 10 → «10-a»."""
    v, vowel_end = _last_word(n)
    suf = "a" if v in "aıou" else "ə"
    return f"{fr(n)}-{'y' if vowel_end else ''}{suf}"


def abl(n):
    """Çıxışlıq hal: 0 → «0-dan», 1 → «1-dən», 6 → «6-dan»."""
    v, _ = _last_word(n)
    return f"{fr(n)}-{'dan' if v in 'aıou' else 'dən'}"


def make_options(rng, answer, distractors, fmt=fr):
    seen = []
    ans = fmt(answer)
    for d in list(distractors) + _fallback(answer):
        s = fmt(d)
        if s != ans and s not in seen:
            seen.append(s)
        if len(seen) == 4:
            break
    if len(seen) < 4:
        raise ValueError(f"Kifayət qədər distraktor yoxdur: {answer} {distractors}")
    opts = seen + [ans]
    rng.shuffle(opts)
    return opts, opts.index(ans)
