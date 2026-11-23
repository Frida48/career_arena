"""Riyaziyyat generatorunun nüvəsi: ədəd göstərilməsi, variantlar və cavabların müstəqil yoxlanması.

Hər şablon fn(r, g) -> dict qaytarır:
    t     — sualın mətni
    a     — düzgün cavab: int / Fraction / Num
    d     — yanlış variantlar (eyni tiplər)
    e     — izah
    chk   — MÜSTƏQİL üsulla (sadalama, koordinat, ifadənin ədədi qiyməti) hesablanmış cavab: int / Fraction / float.
            a-nın ədədi qiyməti ilə üst-üstə düşməlidir, əks halda generator dayanır.
    diff  — "medium" | "hard" (9 və 11-ci siniflərdə hər şey "hard" yazılır)
    img   — SVG (ixtiyari)
"""
import math
from fractions import Fraction as F

M, H = "medium", "hard"
MINUS = "−"


class Num:
    """Göstəriş mətni + ədədi qiymət (√, π olan cavablar üçün)."""

    def __init__(self, s, v):
        self.s, self.v = s, float(v)

    def __repr__(self):
        return f"Num({self.s!r}, {self.v})"


def val(x):
    if isinstance(x, Num):
        return x.v
    return float(F(x))


def show(x):
    """Variant mətni: kəsr a/b, mənfi işarə «−»."""
    if isinstance(x, Num):
        return x.s
    x = F(x)
    s = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return s.replace("-", MINUS)


def same(a, b, tol=1e-9):
    a, b = float(a), float(b)
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------- göstəriş köməkçiləri ----------------

def neg(s):
    return s.replace("-", MINUS)


def simp_root(k, m):
    """k√m sadələşdirilmiş: (k', m')"""
    if m == 0:
        return 0, 1
    f = 1
    i = 2
    while i * i <= m:
        while m % (i * i) == 0:
            m //= i * i
            f *= i
        i += 1
    return k * f, m


def surd(k, m=1):
    """k√m -> Num (k kəsr ola bilər)."""
    k = F(k)
    if m != 1:
        kk, m = simp_root(1, m)
        k *= kk
    v = float(k) * math.sqrt(m)
    if m == 1:
        return Num(show(k), v)
    sign = MINUS if k < 0 else ""
    k = abs(k)
    if k.denominator == 1:
        s = f"√{m}" if k == 1 else f"{k.numerator}√{m}"
    else:
        s = (f"√{m}" if k.numerator == 1 else f"{k.numerator}√{m}") + f"/{k.denominator}"
    return Num(sign + s, v * 1)


def lin_surd(a, b, m):
    """a + b√m"""
    a, b = F(a), F(b)
    kk, m = simp_root(1, m)
    b *= kk
    if m == 1:
        return Num(show(a + b), a + b)
    if b == 0:
        return Num(show(a), a)
    rs = surd(abs(b), m).s
    if a == 0:
        return Num((MINUS if b < 0 else "") + rs, float(b) * math.sqrt(m))
    return Num(f"{show(a)} {'+' if b > 0 else MINUS} {rs}", float(a) + float(b) * math.sqrt(m))


def pi_mul(q, unit=""):
    """q·π"""
    q = F(q)
    if q == 0:
        return Num("0", 0)
    sign = MINUS if q < 0 else ""
    a = abs(q)
    if a.denominator == 1:
        s = "π" if a == 1 else f"{a.numerator}π"
    else:
        s = ("π" if a.numerator == 1 else f"{a.numerator}π") + f"/{a.denominator}"
    return Num(sign + s + unit, float(q) * math.pi)


def deg(q):
    q = F(q)
    return Num(show(q) + "°", q)


def sg(k, s=""):
    """' + 3x' / ' − 3x' (k=0 -> boş)"""
    if k == 0:
        return ""
    k = F(k)
    c = show(abs(k))
    coef = "" if abs(k) == 1 and s else c
    return f" {'+' if k > 0 else MINUS} {coef}{s}"


def lead(k, s=""):
    k = F(k)
    if k == 1 and s:
        return s
    if k == -1 and s:
        return MINUS + s
    return show(k) + s


def poly(coefs, var="x"):
    """coefs: yüksək dərəcədən başlayaraq. [2, -3, 1] -> 2x² − 3x + 1"""
    n = len(coefs) - 1
    sup = {0: "", 1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}
    out = ""
    for i, c in enumerate(coefs):
        p = n - i
        if c == 0:
            continue
        mono = (var + sup[p]) if p > 0 else ""
        out += lead(c, mono) if not out else sg(c, mono)
    return out or "0"


def par(n):
    """mənfi ədədi mötərizəyə al"""
    s = show(n)
    return f"({s})" if F(n) < 0 else s


# ---------------- variantlar ----------------

def auto_near(a):
    """Rəqəm cavab üçün yaxın (oxşar) yanlış variantlar."""
    if isinstance(a, Num):
        if a.s.endswith("%"):
            from common import dec
            base = F(a.v).limit_denominator(1000)
            return [Num(neg(dec(base + k)) + "%", base + k) for k in (2, -2, 5, -5, 1, -1, 10, F(5, 2))]
        import re
        m_ = re.match(r"^(−?)(\d*)√(\d+)(?:/(\d+))?$", a.s)
        if m_:
            sgn_ = -1 if m_.group(1) else 1
            k = int(m_.group(2) or 1) * sgn_
            m = int(m_.group(3))
            dd = int(m_.group(4) or 1)
            out = [surd(F(k + 1, dd), m), surd(F(k - 1, dd), m) if k != 1 else surd(F(k, dd), m + 1), surd(F(k, dd + 1), m),
                   surd(F(k, dd), m + 1), surd(F(k, dd), m - 1) if m > 2 else surd(F(k + 2, dd), m), surd(F(2 * k, dd), m),
                   surd(F(k, 2 * dd), m), surd(F(k + 2, dd), m)]
            return [x for x in out if x.v != 0]
        m_ = re.match(r"^(−?)(\d*)π(?:/(\d+))?$", a.s)
        if m_:
            q = F(a.v / math.pi).limit_denominator(1000)
            return [pi_mul(q + k) for k in (1, -1, 2, F(1, 2), -F(1, 2), 3) if q + k != 0] + [pi_mul(2 * q), pi_mul(q / 2)]
        if a.s.endswith("°"):
            base = F(a.v).limit_denominator(1000)
            return [Num(show(base + k) + "°", base + k) for k in (6, -6, 4, -4, 10, -10, 2, 15) if base + k > 0]
        return []
    a = F(a)
    if a.denominator == 1:
        return [a + 1, a - 1, a + 2, a - 2, a + 3, a - 3, a + 4]
    n, d = a.numerator, a.denominator
    return [F(n + 1, d), F(n - 1, d), F(n, d + 1), F(n, d - 1) if d > 2 else F(n + 2, d), F(n + 2, d), F(n - 2, d)]


def options(rng, a, d, need=4):
    """5 variant: düzgün + 4 yanlış. Mətn və ədədi qiymətə görə təkrar yoxdur."""
    av, ast = val(a), show(a)
    picked, vals, texts = [], [av], {ast}
    for x in list(d) + auto_near(a):
        if x is None:
            continue
        try:
            xv, xs = val(x), show(x)
        except (ZeroDivisionError, ValueError):
            continue
        if xs in texts or any(same(xv, v) for v in vals):
            continue
        picked.append(xs)
        vals.append(xv)
        texts.add(xs)
        if len(picked) == need:
            break
    if len(picked) < need:
        raise ValueError(f"distraktor çatmır: {ast} {d}")
    opts = picked + [ast]
    rng.shuffle(opts)
    return opts, opts.index(ast)


def check(q, where):
    """a ilə müstəqil chk-ni tutuşdurur."""
    if "chk" not in q:
        raise AssertionError(f"{where}: chk yoxdur")
    c = q["chk"]
    if not same(val(q["a"]), float(c), 1e-7):
        raise AssertionError(f"{where}: CAVAB UYĞUN DEYİL a={show(q['a'])} ({val(q['a'])}) chk={float(c)}\n{q['t']}")


# ---------------- ümumi ədədi köməkçilər ----------------

def is_sq(n):
    return n >= 0 and math.isqrt(n) ** 2 == n


def az_dat(n):
    """Yönlük hal şəkilçisi ilə ədəd: 2-yə, 6-ya, 3-ə, 10-a, 40-a, 100-ə"""
    from common import dat
    s = dat(n)
    return MINUS + s[1:] if s.startswith("-") else s


def az_cop(n):
    from common import cop
    s = cop(n)
    return MINUS + s[1:] if s.startswith("-") else s


def az_abl(n):
    from common import abl
    s = abl(n)
    return MINUS + s[1:] if s.startswith("-") else s
