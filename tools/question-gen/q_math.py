"""Riyaziyyat: 16 mövzu × 3 sinif × 60 sual (orta-çətin). Bütün cavablar kodla hesablanır."""
import math
from fractions import Fraction as F
from common import fr, dec, cop, dat, abl
from quiz import build_topic, save_grade

M, H = "medium", "hard"

TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15), (12, 16, 20)]


def sgn(k, s=""):
    """' + 3x' / ' − 3x' formatı (k=0 olduqda boş)."""
    if k == 0:
        return ""
    coef = "" if abs(k) == 1 and s else str(abs(k))
    return f" {'+' if k > 0 else '−'} {coef}{s}"


def poly2(a, b, c, var="x"):
    lead = {1: f"{var}²", -1: f"−{var}²"}.get(a, f"{a}{var}²")
    return f"{lead}{sgn(b, var)}{sgn(c)}"


TRIG = {  # rasional qiymətlər
    "sin 30°": F(1, 2), "cos 60°": F(1, 2), "sin 90°": F(1), "cos 0°": F(1), "cos 180°": F(-1),
    "sin 150°": F(1, 2), "cos 120°": F(-1, 2), "sin 270°": F(-1), "tg 45°": F(1), "tg 135°": F(-1),
    "sin² 45°": F(1, 2), "cos² 30°": F(3, 4), "sin² 60°": F(3, 4), "tg² 60°": F(3), "ctg 45°": F(1),
    "sin 210°": F(-1, 2), "cos 240°": F(-1, 2), "cos 360°": F(1),
}

SQ_FREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23]


def _ap(v, n=2):
    return f"{v:.{n}f}".replace(".", ",")


def lvl(g):
    return g - 8  # 1, 2, 3


def rt(k, m):
    """k√m formatı"""
    if m == 1:
        return str(k)
    return f"√{m}" if k == 1 else f"{k}√{m}"


def pi(v):
    v = F(v)
    if v == 1:
        return "π"
    return f"{v.numerator}π" if v.denominator == 1 else f"{v.numerator}π/{v.denominator}"


def P(n):
    return f"({n})" if n < 0 else str(n)


# =============== Ədədlər: həqiqi ədədlər ===============

def real_conj(r, g):
    while True:
        b = r.choice(SQ_FREE[: 6 + 3 * lvl(g)])
        d = r.choice([1, 2])
        a = b + d
        if math.isqrt(a) ** 2 != a:
            break
    ans = rt(2 // d, b)
    return dict(t=f"Hesablayın: 1/(√{a} − √{b}) − 1/(√{a} + √{b})", a=ans,
                d=[rt(2, a), "0", rt(1, a) if d == 2 else rt(1, b), f"√{a} + √{b}", "2"],
                e=f"Ortaq məxrəc ({a} − {b}) = {d}: [(√{a} + √{b}) − (√{a} − √{b})] / {d} = 2√{b} / {d} = {ans}.",
                diff=H)


def real_square(r, g):
    m = r.choice(SQ_FREE)
    n = r.randint(2, 3 + lvl(g))
    s = r.choice([1, -1])
    sign = "+" if s > 0 else "−"
    ans = f"{m + n * n} {sign} {rt(2 * n, m)}"
    return dict(t=f"Sadələşdirin: (√{m} {sign} {n})²", a=ans,
                d=[f"{m + n * n}", f"{m + n * n} {'−' if s > 0 else '+'} {rt(2 * n, m)}", f"{m + n} {sign} {rt(2 * n, m)}",
                   f"{m + n * n} {sign} {rt(n, m)}", f"{m - n * n} {sign} {rt(2 * n, m)}"],
                e=f"(a {sign} b)² = a² {sign} 2ab + b²: {m} {sign} 2·{n}·√{m} + {n * n} = {ans}.", diff=M)


def real_count(r, g):
    a = r.choice([x for x in range(5, 40 * lvl(g) + 30) if math.isqrt(x) ** 2 != x])
    b = r.choice([x for x in range(5, 40 * lvl(g) + 30) if math.isqrt(x) ** 2 != x])
    n = math.isqrt(a) + math.isqrt(b) + 1
    return dict(t=f"(−√{a}; √{b}) intervalında neçə tam ədəd var?", a=n,
                d=[n - 1, n + 1, n + 2, math.isqrt(b) - math.isqrt(a) + 1 if math.isqrt(b) != math.isqrt(a) else n - 2],
                e=f"√{a} ≈ {_ap(math.sqrt(a))}, √{b} ≈ {_ap(math.sqrt(b))}. "
                  f"Tam ədədlər: −{math.isqrt(a)}-dən {math.isqrt(b)}-ə qədər, cəmi {n}.", diff=M)


def real_compare(r, g):
    while True:
        a = r.choice(SQ_FREE[3:])
        p, q = r.randint(7, 30), r.randint(2, 7)
        b = r.choice(SQ_FREE[:6])
        c = r.randint(2, 4)
        k = r.choice([8, 9, 10, 11, 12, 13, 15, 17, 20, 26])
        vals = {f"√{a}": math.sqrt(a), f"{p}/{q}": p / q, f"{c}√{b}": c * math.sqrt(b),
                f"∛{k ** 2 if k < 12 else k * 3}": (k ** 2 if k < 12 else k * 3) ** (1 / 3), "π": math.pi}
        vs = sorted(vals.values())
        if all(vs[i + 1] - vs[i] > 0.05 for i in range(len(vs) - 1)):
            break
    best = max(vals, key=vals.get)
    return dict(t="Verilmiş ədədlərdən ən böyüyünü tapın: " + "; ".join(vals), a=best, d=[x for x in vals if x != best],
                e="Təqribi qiymətlər: " + ", ".join(f"{k} ≈ {_ap(v)}" for k, v in vals.items()) + ".",
                diff=H)


def real_repeating(r, g):
    if r.random() < 0.5 or g == 9:
        ab = r.randint(10, 98)
        while ab % 11 == 0:
            ab = r.randint(10, 98)
        v = F(ab, 99)
        return dict(t=f"0,({ab}) dövri kəsrini adi kəsr şəklində yazın.", a=v,
                    d=[F(ab, 100), F(ab, 90), F(ab, 999), F(ab + 1, 99)],
                    e=f"0,(ab) = ab/99 ⇒ {ab}/99 = {fr(v)}.", diff=M)
    a, b = r.randint(1, 9), r.randint(1, 9)
    while a == b:
        b = r.randint(1, 9)
    v = F(10 * a + b - a, 90)
    return dict(t=f"0,{a}({b}) dövri kəsrini adi kəsr şəklində yazın.", a=v,
                d=[F(10 * a + b, 99), F(10 * a + b, 90), F(10 * a + b, 100), F(10 * a + b - a, 99)],
                e=f"0,a(b) = (ab − a)/90 = ({10 * a + b} − {a})/90 = {fr(v)}.", diff=H)


def real_nested(r, g):
    while True:
        x, y = r.randint(2, 6 + 2 * lvl(g)), r.randint(1, 8)
        if x > y and math.isqrt(x * y) ** 2 != x * y:
            break
    s = r.choice([1, -1])
    sx = str(math.isqrt(x)) if math.isqrt(x) ** 2 == x else f"√{x}"
    sy = str(math.isqrt(y)) if math.isqrt(y) ** 2 == y else f"√{y}"
    sign = "+" if s > 0 else "−"
    ans = f"{sx} {sign} {sy}"
    return dict(t=f"Sadələşdirin: √({x + y} {sign} 2√{x * y})", a=ans,
                d=[f"{sx} {'−' if s > 0 else '+'} {sy}", f"√{x + y}", f"{sy} {sign} {sx}" if s > 0 else f"{sy} − {sx}",
                   f"√{x * y}", f"{x + y} {sign} √{x * y}"],
                e=f"{x + y} {sign} 2√{x * y} = ({sx} {sign} {sy})², çünki {x} + {y} = {x + y} və {x}·{y} = {x * y}.", diff=H)


# =============== Kəsrlər ===============

def frac_expr(r, g):
    a, b = r.randint(1, 7), r.randint(2, 9)
    c, d = r.randint(1, 7), r.randint(2, 9)
    e_, f_ = r.randint(1, 9), r.randint(2, 9)
    v = (F(a, b) + F(c, d)) / F(e_, f_)
    return dict(t=f"Hesablayın: ({a}/{b} + {c}/{d}) : {e_}/{f_}", a=v,
                d=[(F(a, b) + F(c, d)) * F(e_, f_), F(a + c, b + d) / F(e_, f_), v + 1, F(a, b) + F(c, d) / F(e_, f_)],
                e=f"{a}/{b} + {c}/{d} = {fr(F(a, b) + F(c, d))}; bölmə: {fr(F(a, b) + F(c, d))} · {f_}/{e_} = {fr(v)}.", diff=M)


def frac_continued(r, g):
    n, m = r.randint(2, 6), r.randint(2, 5)
    v = 1 / (1 + 1 / (m + F(1, n)))
    return dict(t=f"Hesablayın: 1 / (1 + 1 / ({m} + 1/{n}))", a=v,
                d=[1 / (1 + m + F(1, n)), F(m * n + 1, n), 1 + 1 / (m + F(1, n)), v + F(1, n)],
                e=f"{m} + 1/{n} = {fr(m + F(1, n))}; 1 + {fr(1 / (m + F(1, n)))} = {fr(1 + 1 / (m + F(1, n)))}; cavab {fr(v)}.", diff=H)


def frac_part(r, g):
    p, q = r.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 7), (5, 6), (3, 8)])
    m, n = r.choice([(1, 2), (3, 4), (1, 3), (2, 5), (5, 8), (1, 6)])
    x = q * n * r.randint(2, 6 + lvl(g))
    y = F(p, q) * x
    return dict(t=f"Ədədin {p}/{q} hissəsi {fr(y)}-ə bərabərdir. Həmin ədədin {m}/{n} hissəsini tapın.".replace(f"{fr(y)}-ə", dat(y)),
                a=F(m, n) * x, d=[x, F(m, n) * y, y * F(q, p) * F(n, m), F(m, n) * x + 1],
                e=f"Ədəd: {fr(y)} : {p}/{q} = {x}. Onun {m}/{n} hissəsi: {fr(F(m, n) * x)}.", diff=M)


def frac_pool(r, g):
    a, b = r.choice([(2, 3), (3, 6), (4, 12), (6, 12), (4, 6), (5, 20), (6, 3), (10, 15), (12, 4)])
    v = F(a * b, a + b)
    if r.random() < 0.5:
        return dict(t=f"Hovuzu birinci boru {a} saata, ikinci boru {b} saata doldurur. İki boru birlikdə hovuzu neçə saata doldurar?",
                    a=v, d=[F(a + b, 2), a + b, abs(a - b) if a != b else a + 1, F(a * b, abs(a - b) if a != b else 1) + 1],
                    fmt=dec, e=f"Birlikdə 1 saatda: 1/{a} + 1/{b} = {fr(F(1, a) + F(1, b))} hissə. Vaxt: {fr(v)} = {dec(v)} saat.", diff=M)
    big, small = max(a, b), min(a, b)
    if big == small:
        big += small
    w = F(big * small, big - small)
    return dict(t=f"Birinci boru hovuzu {small} saata doldurur, ikinci boru dolu hovuzu {big} saata boşaldır. İkisi birlikdə açıq olarsa, boş hovuz neçə saata dolar?",
                a=w, d=[F(big * small, big + small), big - small, big + small, w + 1], fmt=dec,
                e=f"1 saatda: 1/{small} − 1/{big} = {fr(F(1, small) - F(1, big))} hissə. Vaxt: {dec(w)} saat.", diff=H)


def frac_min(r, g):
    fs = set()
    while len(fs) < 5:
        q = r.randint(3, 12 + 3 * lvl(g))
        p = r.randint(1, q - 1)
        if math.gcd(p, q) == 1:
            fs.add(F(p, q))
    fs = list(fs)
    want_min = r.random() < 0.5
    ans = min(fs) if want_min else max(fs)
    return dict(t=f"Kəsrlərdən ən {'kiçiyini' if want_min else 'böyüyünü'} tapın: " + "; ".join(fr(x) for x in fs), a=ans,
                d=[x for x in fs if x != ans],
                e="Onluq qiymətlər: " + ", ".join(f"{fr(x)} ≈ {_ap(float(x), 3)}" for x in fs) + ".",
                diff=M)


def frac_decimal(r, g):
    a = r.choice([F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(1, 8), F(5, 8), F(3, 20)])
    b, c = r.randint(1, 5), r.randint(2, 9)
    d_ = r.choice([F(1, 2), F(3, 2), F(5, 4), F(7, 10)])
    v = a * F(b, c) + d_
    return dict(t=f"Hesablayın: {dec(a)} · {b}/{c} + {dec(d_)}", a=v,
                d=[a * F(b, c), (a + d_) * F(b, c), a + F(b, c) + d_, v + F(1, 2)],
                e=f"{dec(a)} = {fr(a)}; {fr(a)} · {b}/{c} = {fr(a * F(b, c))}; + {dec(d_)} = {fr(v)}.", diff=M)


# =============== Dərəcə və qüvvət ===============

def pow_laws(r, g):
    a = r.choice([2, 3, 5])
    m, n, k = r.randint(2, 4), r.randint(2, 3), r.randint(2, 6)
    p = m * n - k - r.randint(-2, 2)
    e_ = m * n - k - p
    v = F(a) ** e_
    return dict(t=f"Hesablayın: ({a}^{m})^{n} · {a}^(−{k}) : {a}^{p}", a=v,
                d=[F(a) ** (m + n - k - p), F(a) ** (e_ + 1), F(a) ** (-e_) if e_ else F(a), F(a) ** (m * n + k - p)],
                e=f"{a}^({m}·{n} − {k} − {p}) = {a}^{e_} = {fr(v)}.", diff=M)


def pow_base2(r, g):
    x, y, z = r.randint(2, 6), r.randint(1, 4), r.randint(3, 9)
    e_ = 2 * x + 3 * y - z
    return dict(t=f"4^{x} · 8^{y} : 2^{z} ifadəsi 2-nin neçənci qüvvətidir?", a=e_,
                d=[x + y - z, 2 * x + 3 * y + z, 4 * x + 8 * y - 2 * z, e_ + 1],
                e=f"4^{x} = 2^{2 * x}, 8^{y} = 2^{3 * y}. Üst: {2 * x} + {3 * y} − {z} = {e_}.", diff=M)


FRAC_POW = [("8^(2/3)", F(4)), ("27^(2/3)", F(9)), ("16^(3/4)", F(8)), ("32^(2/5)", F(4)), ("9^(−1/2)", F(1, 3)),
            ("25^(−1/2)", F(1, 5)), ("64^(1/3)", F(4)), ("81^(3/4)", F(27)), ("4^(−3/2)", F(1, 8)), ("125^(2/3)", F(25)),
            ("16^(−1/4)", F(1, 2)), ("49^(1/2)", F(7)), ("1000^(2/3)", F(100)), ("8^(−1/3)", F(1, 2))]


def pow_fractional(r, g):
    (n1, v1), (n2, v2) = r.sample(FRAC_POW, 2)
    op = r.choice(["+", "·"])
    v = v1 + v2 if op == "+" else v1 * v2
    return dict(t=f"Hesablayın: {n1} {op} {n2}", a=v,
                d=[v1 - v2 if op == "+" else v1 + v2, v + 1, v1, v2 if v2 != v1 else v + 2, 2 * v],
                e=f"{n1} = {fr(v1)}, {n2} = {fr(v2)}. Nəticə: {fr(v)}.", diff=M if g == 9 else H)


def pow_lastdigit(r, g):
    a = r.choice([2, 3, 7, 8, 9, 4, 13, 17])
    n = r.randint(20, 99 + 100 * lvl(g))
    ans = pow(a, n, 10)
    cyc = []
    x = a % 10
    while x not in cyc:
        cyc.append(x)
        x = x * a % 10
    return dict(t=f"{a}^{n} ədədinin son rəqəmini tapın.", a=ans,
                d=[d for d in range(10) if d != ans][:9], allow_open=True,
                e=f"Son rəqəmlər {len(cyc)} addımdan bir təkrarlanır: {', '.join(map(str, cyc))}. {n} : {len(cyc)} qalığı {n % len(cyc) or len(cyc)} ⇒ {ans}.",
                diff=H)


def pow_compare(r, g):
    k = r.choice([10, 12, 15, 20, 30])
    bases = r.sample([(2, 3), (3, 2), (5, 1), (4, 2), (7, 1), (6, 1), (2, 4), (3, 3), (10, 1)], 4)
    items = {}
    for b, m in bases:
        e_ = k * m // math.gcd(1, 1)
        items[f"{b}^{e_}"] = e_ * math.log(b)
    vals = sorted(items.values())
    if any(vals[i + 1] - vals[i] < 1e-6 for i in range(len(vals) - 1)):
        return pow_compare(r, g)
    best = max(items, key=items.get)
    extra = f"{bases[0][0]}^{k}" if f"{bases[0][0]}^{k}" not in items else "1"
    return dict(t="Ən böyük ədədi tapın: " + "; ".join(items), a=best, d=[x for x in items if x != best] + [extra],
                e="Üstləri ortaq " + str(k) + "-a gətirib əsasları müqayisə edin: " +
                  ", ".join(f"{x} = ({x.split('^')[0]}^{int(x.split('^')[1]) // k})^{k}" for x in items) + ".", diff=H)


def pow_standard(r, g):
    a, b = r.choice([2, 3, 4, 5, 6]), r.choice([2, 4, 5, 8])
    m, n = r.randint(3, 9), r.randint(-6, 4)
    v = a * b
    k = m + n
    if v >= 10:
        c, k = F(v, 10), k + 1
    else:
        c = F(v)
    ans = f"{dec(c)}·10^{k}"
    return dict(t=f"({a}·10^{m}) · ({b}·10^{n}) hasilini standart şəkildə yazın.", a=ans,
                d=[f"{v}·10^{m + n}" if v >= 10 else f"{dec(c)}·10^{k + 1}", f"{dec(c)}·10^{k - 1}", f"{dec(c)}·10^{m * n}",
                   f"{a + b}·10^{m + n}"],
                e=f"{a}·{b} = {v}, 10^{m}·10^{n} = 10^{m + n}. Standart şəkil: {ans}.", diff=M)


# =============== Modul ===============

def abs_product(r, g):
    a, b = r.randint(-9, 12), r.randint(1, 9 + lvl(g))
    while (a + b) % 2 or a == b:
        a, b = r.randint(-9, 12), r.randint(1, 9 + lvl(g))
    x1, x2 = F(a + b, 2), F(a - b, 2)
    return dict(t=f"|2x {'−' if a >= 0 else '+'} {abs(a)}| = {b} tənliyinin köklərinin hasilini tapın.", a=x1 * x2,
                d=[x1 + x2, (a + b) * (a - b), -x1 * x2, x1 * x2 + 1],
                e=f"2x = {a} ± {b} ⇒ x₁ = {fr(x1)}, x₂ = {fr(x2)}. Hasil: {fr(x1 * x2)}.", diff=M)


def abs_ineq(r, g):
    a, b = r.randint(-7, 9), r.randint(3, 9 + 2 * lvl(g))
    strict = r.random() < 0.5
    lo, hi = F(a - b, 2), F(a + b, 2)
    if strict:
        n = sum(1 for x in range(-50, 60) if lo < x < hi)
    else:
        n = sum(1 for x in range(-50, 60) if lo <= x <= hi)
    return dict(t=f"|2x {'−' if a >= 0 else '+'} {abs(a)}| {'<' if strict else '≤'} {b} bərabərsizliyinin neçə tam həlli var?",
                a=n, d=[n + 1, n - 1, b, 2 * b + 1 if 2 * b + 1 != n else n + 2],
                e=f"−{b} {'<' if strict else '≤'} 2x − ({a}) {'<' if strict else '≤'} {b} ⇒ {fr(lo)} {'<' if strict else '≤'} x {'<' if strict else '≤'} {fr(hi)}. Tam həllər: {n}.",
                diff=H)


def abs_sqrt_expr(r, g):
    m = r.choice([x for x in range(3, 60) if math.isqrt(x) ** 2 != x])
    s = math.isqrt(m)
    b, c = s - r.randint(0, 2), s + 1 + r.randint(0, 2)
    return dict(t=f"Hesablayın: |√{m} − {b}| + |√{m} − {c}|", a=c - b,
                d=[b + c, f"2√{m} − {b + c}", f"{b + c} − 2√{m}", c - b + 1],
                e=f"{b} < √{m} < {c}: (√{m} − {b}) + ({c} − √{m}) = {c - b}.", diff=H)


def abs_min_sum(r, g):
    a, b = r.randint(-8, 3), r.randint(4, 12)
    if r.random() < 0.6:
        return dict(t=f"y = |x {'−' if a >= 0 else '+'} {abs(a)}| + |x − {b}| funksiyasının ən kiçik qiymətini tapın.",
                    a=b - a, d=[a + b, abs(a), b, 0], e=f"{a} ≤ x ≤ {b} olduqda y = {b - a} (ən kiçik qiymət).", diff=M)
    c = r.randint(a + 1, b - 1)
    return dict(t=f"y = |x {'−' if a >= 0 else '+'} {abs(a)}| + |x − {c}| + |x − {b}| funksiyasının ən kiçik qiymətini tapın.",
                a=b - a, d=[b - a + abs(c), a + b + c, b - c, c - a], e=f"Minimum orta nöqtədə, x = {c}: |{c} − {a}| + 0 + |{c} − {b}| = {b - a}.",
                diff=H)


def abs_linear(r, g):
    while True:
        a, b = r.randint(-6, 12), r.randint(-6, 8)
        if (a - b) % 2 == 0 and a != -b:
            x = (a - b) // 2
            if x < a and x + b >= 0:
                break
    return dict(t=f"|x {'−' if a >= 0 else '+'} {abs(a)}| = x{sgn(b)} tənliyini həll edin.", a=x,
                d=[a + b, x + 1, -x if x else 1, a], e=f"x ≥ {a} halında həll yoxdur; x < {a} halında {a} − x = x{sgn(b)} ⇒ x = {x}.",
                diff=H)


def abs_double(r, g):
    a, b = r.randint(1, 7), r.randint(0, 9)
    roots = set()
    for v in (a + b, a - b):
        if v > 0:
            roots |= {v, -v}
        elif v == 0:
            roots.add(0)
    n = len(roots)
    return dict(t=f"||x| − {a}| = {b} tənliyinin neçə kökü var?", a=n, d=[x for x in [0, 1, 2, 3, 4, 5] if x != n],
                e=f"|x| = {a} + {b} = {a + b} və ya |x| = {a} − {b} = {a - b}. Köklər: {', '.join(map(str, sorted(roots))) or 'yoxdur'}.",
                diff=H)


# =============== Faizlər ===============

def pct_chain(r, g):
    p = r.choice([200, 400, 500, 800, 1000, 1200])
    u, d_ = r.choice([10, 20, 25, 30, 50]), r.choice([10, 20, 25, 40])
    res = F(p) * (100 + u) / 100 * (100 - d_) / 100
    return dict(t=f"Malın qiyməti {p} manat idi. Əvvəlcə {u}% bahalaşdı, sonra yeni qiymət {d_}% ucuzlaşdı. Son qiymət neçə manatdır?",
                a=res, d=[F(p) * (100 + u - d_) / 100, F(p) * (100 - u) / 100 * (100 + d_) / 100 if u != d_ else res + 10, res + 20, F(p)],
                fmt=dec, e=f"{p} · {dec(F(100 + u, 100))} · {dec(F(100 - d_, 100))} = {dec(res)}.", diff=M)


def pct_reverse(r, g):
    p = r.choice([10, 20, 25, 40, 50, 60])
    orig = r.choice([20, 40, 60, 80, 120, 160, 200, 240]) * 5
    x = F(orig) * (100 + p) / 100
    return dict(t=f"Qiyməti {p}% artırıldıqdan sonra malın qiyməti {dec(x)} manat oldu. İlkin qiymət neçə manat idi?", a=orig,
                d=[x * (100 - p) / 100, x - p, F(orig) * (100 + p) / 100 - orig, orig + p], fmt=dec,
                e=f"x · {dec(F(100 + p, 100))} = {dec(x)} ⇒ x = {orig}. Diqqət: {dec(x)}-dən {p}% çıxmaq düzgün deyil.", diff=H)


def pct_mixture(r, g):
    a, b = r.choice([2, 3, 4, 5, 6]), r.choice([1, 2, 3, 4])
    while True:
        p, q = r.choice([10, 20, 30, 40]), r.choice([50, 60, 70, 80])
        c = F(a * p + b * q, a + b)
        if "/" not in dec(c):
            break
        a, b = r.choice([2, 3, 4, 5, 6]), r.choice([1, 2, 3, 4])
    return dict(t=f"{a} kq {p}%-li və {b} kq {q}%-li duz məhlulu qarışdırıldı. Alınan məhlulun qatılığı neçə faizdir?", a=c,
                d=[F(p + q, 2), F(a * q + b * p, a + b), c + 5, F(p * q, 100)], fmt=dec,
                e=f"Duz: {a}·{p}% + {b}·{q}% = {dec(F(a * p + b * q, 100))} kq. Qatılıq: {dec(F(a * p + b * q, 100))} : {a + b} · 100% = {dec(c)}%.",
                diff=H)


def pct_compound(r, g):
    s = r.choice([1000, 2000, 5000, 10000])
    p = r.choice([5, 10, 20])
    n = 2 if g < 11 else r.choice([2, 3])
    v = F(s) * F(100 + p, 100) ** n
    return dict(t=f"Banka {s} manat illik {p}% mürəkkəb faizlə qoyuldu. {n} ildən sonra hesabda neçə manat olacaq?", a=v,
                d=[F(s) * (100 + p * n) / 100, v + s * p // 100, F(s) * F(100 + p, 100) ** (n - 1), v - 10], fmt=dec,
                e=f"{s} · {dec(F(100 + p, 100))}^{n} = {dec(v)} manat.", diff=M if n == 2 else H)


def pct_area(r, g):
    a, b = r.choice([(10, 10), (20, 20), (20, 10), (30, 20), (25, 20), (50, 20), (10, 20)])
    ch = F(100 + a, 100) * F(100 - b, 100) - 1
    pct = abs(ch * 100)
    word = "artar" if ch > 0 else "azalar" if ch < 0 else "dəyişməz"
    ans = f"{dec(pct)}% {word}" if ch != 0 else "dəyişməz"
    return dict(t=f"Düzbucaqlının uzunluğu {a}% artırıldı, eni isə {b}% azaldıldı. Sahəsi necə dəyişər?", a=ans,
                d=["dəyişməz" if ch != 0 else "1% azalar", f"{abs(a - b)}% {'artar' if a > b else 'azalar'}" if a != b else "2% artar",
                   f"{dec(pct)}% {'azalar' if ch > 0 else 'artar'}", f"{a + b}% artar", f"{dec(pct + 1)}% {word}"],
                e=f"{dec(F(100 + a, 100))} · {dec(F(100 - b, 100))} = {dec(1 + ch)} ⇒ sahə {ans}.", diff=H)


def pct_of_pct(r, g):
    p, q = r.choice([20, 25, 40, 50, 60, 75, 80]), r.choice([10, 20, 30, 40, 50, 150])
    v = F(p * q, 100)
    return dict(t=f"A ədədi B-nin {p}%-ni, B isə C-nin {q}%-ni təşkil edir. A ədədi C-nin neçə faizidir?", a=v,
                d=[p + q, F(p, q) * 100, abs(p - q), v + 10], fmt=dec,
                e=f"A = {dec(F(p, 100))}·B = {dec(F(p, 100))}·{dec(F(q, 100))}·C = {dec(v / 100)}·C ⇒ {dec(v)}%.", diff=M)


# =============== Tənliklər ===============

def eq_fractions(r, g):
    b, d = r.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 5)])
    x = r.randint(-6, 12)
    a, c = r.randint(1, 6), r.randint(1, 6)
    e_ = F(x + a, b) - F(x - c, d)
    return dict(t=f"(x + {a})/{b} − (x − {c})/{d} = {fr(e_)} tənliyini həll edin.", a=x,
                d=[-x if x else 1, x + 1, x + b, F(e_ * b * d) - a + c], e=f"Hər tərəfi {b * d}-ə vurub sadələşdiririk: x = {x}.".replace(f"{b * d}-ə", dat(b * d)),
                diff=M)


def eq_rational(r, g):
    while True:
        x, b, d_ = r.randint(-6, 10), r.randint(1, 7), r.randint(1, 7)
        if x - b != 0 and x + d_ != 0 and b + d_ != 0:
            break
    k = r.choice([1, 2, 3])
    a, c = k * (x - b), k * (x + d_)
    if a == 0 or c == 0 or a == c:
        return eq_rational(r, g)
    return dict(t=f"{a}/(x − {b}) = {c}/(x + {d_}) tənliyini həll edin.", a=x,
                d=[b, -d_, x + 1, -x if x else 2], e=f"Çarpaz vurma: {a}(x + {d_}) = {c}(x − {b}) ⇒ x = {x} (x ≠ {b}, x ≠ −{d_}).", diff=M)


def eq_param(r, g):
    p = r.randint(2, 7)
    return dict(t=f"(m² − {p * p})x = m − {p} tənliyinin həlli yoxdur. m-i tapın.", a=-p,
                d=[p, 0, p * p, -p * p], e=f"m = {p} olduqda 0·x = 0 — sonsuz həll. m = −{p} olduqda 0·x = −{2 * p} — həll yoxdur.", diff=H)


def eq_age(r, g):
    while True:
        s, k, n = r.randint(4, 15), r.randint(3, 6), r.randint(2, 20)
        m = F(k * s + n, s + n)
        if m.denominator == 1 and 1 < m < k:
            break
    return dict(t=f"Ata oğlundan {k} dəfə böyükdür. {n} ildən sonra o, oğlundan {m} dəfə böyük olacaq. Oğul indi neçə yaşındadır?",
                a=s, d=[k * s, s + n, s + 1, s - 1], e=f"{k}x + {n} = {m}(x + {n}) ⇒ x = {s}. Ata {k * s} yaşındadır.", diff=H)


def eq_speed(r, g):
    v1, v2 = r.choice([40, 50, 60, 70, 80]), r.choice([45, 55, 60, 65, 90])
    t = r.choice([2, 3, 4, 5])
    if r.random() < 0.5:
        D = (v1 + v2) * t
        return dict(t=f"Aralarındakı məsafə {D} km olan iki şəhərdən eyni vaxtda bir-birinə doğru {v1} km/saat və {v2} km/saat sürətlə iki avtomobil çıxdı. Neçə saatdan sonra görüşəcəklər?",
                    a=t, d=[F(D, abs(v1 - v2) or 1), t + 1, F(D, v1), F(D, v2)], fmt=dec,
                    e=f"Yaxınlaşma sürəti {v1 + v2} km/saat. t = {D} : {v1 + v2} = {t}.", diff=M)
    if v1 == v2:
        v2 += 10
    lo, hi = min(v1, v2), max(v1, v2)
    D = (hi - lo) * t
    return dict(t=f"Sürəti {lo} km/saat olan avtomobil yola çıxdı. O, {D} km uzaqlaşanda arxasınca {hi} km/saat sürətlə ikinci avtomobil çıxdı. İkinci avtomobil birincini neçə saata ötəcək?",
                a=t, d=[F(D, lo + hi), F(D, lo), t + 1, F(D, hi)], fmt=dec,
                e=f"Yaxınlaşma sürəti {hi} − {lo} = {hi - lo} km/saat. t = {D} : {hi - lo} = {t}.", diff=H)


def eq_biquad(r, g):
    a, b = r.sample(range(1, 6 + lvl(g)), 2)
    A, B = a * a + b * b, a * a * b * b
    if r.random() < 0.5:
        return dict(t=f"x⁴ − {A}x² + {B} = 0 tənliyinin müsbət köklərinin cəmini tapın.", a=a + b,
                    d=[A, a * b, 0, 2 * (a + b)], e=f"x² = t: t² − {A}t + {B} = 0 ⇒ t = {a * a}, {b * b}. Müsbət köklər {a} və {b}.", diff=H)
    return dict(t=f"x⁴ − {A}x² + {B} = 0 tənliyinin bütün köklərinin hasilini tapın.", a=B,
                d=[-B, a * b, A, 0], e=f"Köklər ±{a}, ±{b}. Hasil: {a}·(−{a})·{b}·(−{b}) = {B}.", diff=H)


# =============== Tənliklər sistemi ===============

def sys_linear(r, g):
    x, y = r.randint(-5, 9), r.randint(-5, 9)
    a, b, c, d_ = r.choice([(2, 3, 3, -2), (3, 1, 2, -5), (4, -3, 1, 2), (5, 2, 3, 4), (2, -5, 3, 1)])
    ask = r.choice(["x + y", "x − y", "xy"])
    val = {"x + y": x + y, "x − y": x - y, "xy": x * y}[ask]
    return dict(t=f"{{ {a}x{sgn(b, 'y')} = {a * x + b * y};  {c}x{sgn(d_, 'y')} = {c * x + d_ * y} }} sistemindən {ask} ifadəsinin qiymətini tapın.",
                a=val, d=[x + y + 1, x - y if ask != "x − y" else x + y, -val if val else 3, x * y + 1 if ask != "xy" else x + y],
                e=f"Sistemi həll edirik: x = {x}, y = {y}. {ask} = {val}.", diff=M)


def sys_word(r, g):
    n, p = r.randint(2, 9), r.randint(3, 15)
    a, b, c, d_ = r.choice([(3, 2, 2, 3), (4, 1, 2, 3), (5, 2, 3, 4), (2, 5, 3, 2)])
    return dict(t=f"{a} dəftər və {b} qələm {a * n + b * p} qəpik, {c} dəftər və {d_} qələm isə {c * n + d_ * p} qəpikdir. Bir qələm neçə qəpikdir?".replace("qəpik", "manat") if False else
                f"{a} dəftər və {b} qələm birlikdə {a * n + b * p} manat, {c} dəftər və {d_} qələm isə {c * n + d_ * p} manatdır. Bir qələm neçə manatdır?",
                a=p, d=[n, p + 1, n + p, abs(p - n) or 1], e=f"Dəftər x, qələm y: {a}x + {b}y = {a * n + b * p}, {c}x + {d_}y = {c * n + d_ * p} ⇒ x = {n}, y = {p}.",
                diff=M)


def sys_nosol(r, g):
    p, q = r.randint(1, 6), r.randint(1, 6)
    t = r.choice([2, 3, 4])
    s = r.randint(1, 9)
    u = s * t + r.choice([1, 2, -1, 5])
    return dict(t=f"{{ ax + {q * t}y = {u};  {p}x + {q}y = {s} }} sisteminin həlli olmaması üçün a nəyə bərabər olmalıdır?",
                a=p * t, d=[p, q * t, p + t, F(p, t)], e=f"Əmsallar mütənasib olmalıdır: a/{p} = {q * t}/{q} = {t} ⇒ a = {p * t}; sərbəst hədlər mütənasib deyil ({u} ≠ {s * t}).",
                diff=H)


def sys_symmetric(r, g):
    x, y = r.randint(1, 6), r.randint(-4, 7)
    while y == 0 or x == y:
        y = r.randint(-4, 7)
    s, p = x + y, x * y
    if r.random() < 0.5:
        v = F(s, p)
        return dict(t=f"x + y = {s}, xy = {p} olarsa, 1/x + 1/y ifadəsinin qiymətini tapın.", a=v,
                    d=[F(p, s) if s else 1, s * p, v + 1, F(1, s + p) if s + p else 2], e=f"1/x + 1/y = (x + y)/(xy) = {s}/{p} = {fr(v)}.", diff=M)
    v = s ** 3 - 3 * p * s
    return dict(t=f"x + y = {s}, xy = {p} olarsa, x³ + y³ ifadəsinin qiymətini tapın.", a=v,
                d=[s ** 3, s ** 3 + 3 * p * s, s ** 3 - p * s, v + s], e=f"x³ + y³ = (x + y)³ − 3xy(x + y) = {s ** 3} − {3 * p * s} = {v}.", diff=H)


def sys_three(r, g):
    x, y, z = r.randint(-3, 9), r.randint(-3, 9), r.randint(-3, 9)
    return dict(t=f"x + y = {x + y}, y + z = {y + z}, x + z = {x + z} olarsa, x + y + z neçədir?", a=x + y + z,
                d=[2 * (x + y + z), (x + y) + (y + z) + (x + z), x + y + z + 1, x * y * z if x * y * z != x + y + z else 0],
                e=f"Üç tənliyi toplasaq 2(x + y + z) = {2 * (x + y + z)} ⇒ x + y + z = {x + y + z}.", diff=M if g == 9 else H)


def sys_diff_squares(r, g):
    x, y = r.randint(3, 15), r.randint(1, 10)
    while x <= y:
        x = r.randint(3, 15)
    return dict(t=f"{{ x − y = {x - y};  x² − y² = {x * x - y * y} }} sistemindən x-i tapın.", a=x,
                d=[y, x + y, x - y, x + 1], e=f"x² − y² = (x − y)(x + y) ⇒ x + y = {x * x - y * y} : {x - y} = {x + y}. x = ({x + y} + {x - y})/2 = {x}.",
                diff=H)


# =============== Kvadrat tənliklər ===============

def _roots(r, g):
    x1, x2 = r.randint(-7, 8), r.randint(-7, 8)
    while x1 == 0 or x2 == 0 or x1 == x2:
        x1, x2 = r.randint(-7, 8), r.randint(-7, 8)
    return x1, x2


def quad_sq_sum(r, g):
    x1, x2 = _roots(r, g)
    s, p = x1 + x2, x1 * x2
    return dict(t=f"{poly2(1, -s, p)} = 0 tənliyinin kökləri x₁ və x₂-dir. x₁² + x₂² ifadəsinin qiymətini tapın.", a=s * s - 2 * p,
                d=[s * s, s * s + 2 * p, p * p, s * s - p], e=f"Viyet: x₁ + x₂ = {s}, x₁x₂ = {p}. x₁² + x₂² = {s * s} − {2 * p} = {s * s - 2 * p}.", diff=M)


def quad_recip(r, g):
    x1, x2 = _roots(r, g)
    s, p = x1 + x2, x1 * x2
    a = r.choice([1, 2, 3])
    return dict(t=f"{poly2(a, -a * s, a * p)} = 0 tənliyinin kökləri x₁ və x₂-dir. 1/x₁ + 1/x₂ ifadəsini hesablayın.", a=F(s, p),
                d=[F(p, s) if s else 1, F(-s, p), F(s, a * p) if a > 1 else F(s, p) + 1, s * p], e=f"1/x₁ + 1/x₂ = (x₁ + x₂)/(x₁x₂) = {s}/{p} = {fr(F(s, p))}.", diff=M)


def quad_one_root(r, g):
    n = r.randint(2, 9)
    a = r.choice([1, 1, 4, 9]) if g > 9 else 1
    k = 2 * n * int(math.isqrt(a))
    return dict(t=f"{'' if a == 1 else a}x² + kx + {n * n} = 0 tənliyinin yeganə kökü olması üçün k-nın müsbət qiymətini tapın.", a=k,
                d=[n, 2 * n if k != 2 * n else 4 * n, n * n, k + 2], e=f"D = k² − 4·{a}·{n * n} = 0 ⇒ k² = {k * k} ⇒ k = {k}.", diff=H)


def quad_ineq(r, g):
    p = r.randint(-6, 2)
    q = p + r.randint(3, 9)
    strict = r.random() < 0.5
    n = (q - p - 1) if strict else (q - p + 1)
    neg = r.random() < 0.4
    if neg:
        return dict(t=f"{poly2(-1, p + q, -p * q)} {'>' if strict else '≥'} 0 bərabərsizliyinin neçə tam həlli var?", a=n,
                    d=[q - p, n + 2, n - 1 if n > 1 else n + 3, 0], e=f"Hər tərəfi −1-ə vursaq: {poly2(1, -(p + q), p * q)} {'<' if strict else '≤'} 0, köklər {p} və {q}. Tam həllər: {n}.",
                    diff=H)
    return dict(t=f"{poly2(1, -(p + q), p * q)} {'<' if strict else '≤'} 0 bərabərsizliyinin neçə tam həlli var?", a=n,
                d=[q - p, n + 2, n - 1 if n > 1 else n + 3, 0], e=f"Köklər {p} və {q}; tam həllər sayı {n}.", diff=M)


def quad_diff(r, g):
    x1, x2 = _roots(r, g)
    s, p = x1 + x2, x1 * x2
    return dict(t=f"{poly2(1, -s, p)} = 0 tənliyinin kökləri arasındakı fərqin modulunu tapın.", a=abs(x1 - x2),
                d=[abs(s), abs(x1 + x2) + 1, s * s - 4 * p, abs(x1 - x2) + 2], e=f"|x₁ − x₂| = √D = √({s * s} − {4 * p}) = {abs(x1 - x2)}.", diff=M)


def quad_cubes(r, g):
    x1, x2 = _roots(r, g)
    s, p = x1 + x2, x1 * x2
    v = s ** 3 - 3 * p * s
    return dict(t=f"{poly2(1, -s, p)} = 0 tənliyinin kökləri x₁, x₂ olarsa, x₁³ + x₂³ neçədir?", a=v,
                d=[s ** 3, s ** 3 + 3 * p * s, v + p, s * p], e=f"x₁³ + x₂³ = s³ − 3ps = {s ** 3} − {3 * p * s} = {v}.", diff=H)


# =============== Proqresiyalar ===============

def prog_two_terms(r, g):
    a1, d = r.randint(-10, 15), r.choice([2, 3, 4, 5, -3, -4, 7])
    m, n = r.sample(range(2, 12), 2)
    k = r.randint(15, 25 + 10 * lvl(g))
    am, an, ak = a1 + (m - 1) * d, a1 + (n - 1) * d, a1 + (k - 1) * d
    return dict(t=f"Ədədi silsilədə a{_s(m)} = {am}, a{_s(n)} = {an}. a{_s(k)} həddini tapın.", a=ak,
                d=[ak + d, ak - d, a1 + k * d, am + (k - 1) * d], e=f"d = ({an} − {am})/({n} − {m}) = {d}, a₁ = {a1}. a{_s(k)} = {a1} + {k - 1}·{d} = {ak}.",
                diff=M)


def prog_sum(r, g):
    a1, d, n = r.randint(-5, 10), r.choice([2, 3, 4, 5]), r.choice([12, 15, 16, 20, 25, 30])
    s = n * (2 * a1 + (n - 1) * d) // 2
    a_n = a1 + (n - 1) * d
    return dict(t=f"Ədədi silsilədə a₁ = {a1}, a{_s(n)} = {a_n}. İlk {n} həddin cəmini tapın.", a=s,
                d=[n * a_n, s + a_n, (a1 + a_n) * n, s - n], e=f"Sₙ = (a₁ + aₙ)·n/2 = ({a1} + {a_n})·{n}/2 = {s}.", diff=M)


def prog_geom_sum(r, g):
    b1, q, n = r.choice([1, 2, 3]), r.choice([2, 3, -2]), r.randint(4, 6 + lvl(g))
    s = b1 * (q ** n - 1) // (q - 1)
    return dict(t=f"Həndəsi silsilədə b₁ = {b1}, q = {q}. İlk {n} həddin cəmini tapın.", a=s,
                d=[b1 * q ** (n - 1), b1 * (q ** (n + 1) - 1) // (q - 1), s + b1, b1 * q ** n], e=f"Sₙ = b₁(qⁿ − 1)/(q − 1) = {b1}·({q}^{n} − 1)/({q} − 1) = {s}.", diff=H)


def prog_infinite(r, g):
    b1 = r.randint(2, 20)
    q = r.choice([F(1, 2), F(1, 3), F(-1, 2), F(2, 3), F(1, 4), F(-1, 3), F(3, 4)])
    v = b1 / (1 - q)
    return dict(t=f"Sonsuz azalan həndəsi silsilədə b₁ = {b1}, q = {fr(q)}. Bütün hədlərin cəmini tapın.", a=v,
                d=[b1 / (1 + q), b1 * q / (1 - q), b1 / q if q else 1, v + 1], e=f"S = b₁/(1 − q) = {b1}/(1 − ({fr(q)})) = {fr(v)}.", diff=H)


def prog_multiples(r, g):
    k = r.choice([3, 4, 6, 7, 9, 11, 12, 13])
    lo, hi = r.choice([(10, 99), (100, 199), (10, 200), (50, 150)])
    first = (lo + k - 1) // k * k
    last = hi // k * k
    n = (last - first) // k + 1
    if r.random() < 0.5:
        return dict(t=f"{lo}-dən {hi}-ə qədər (daxil) {k}-ə bölünən neçə ədəd var?".replace(f"{lo}-dən", abl(lo)).replace(f"{hi}-ə", dat(hi)).replace(f"{k}-ə", dat(k)),
                    a=n, d=[n + 1, n - 1, hi // k, (hi - lo) // k], e=f"İlk: {first}, son: {last}. Say: ({last} − {first})/{k} + 1 = {n}.", diff=M)
    s = (first + last) * n // 2
    return dict(t=f"{lo}-dən {hi}-ə qədər {k}-ə bölünən bütün ədədlərin cəmini tapın.".replace(f"{lo}-dən", abl(lo)).replace(f"{hi}-ə", dat(hi)).replace(f"{k}-ə", dat(k)),
                a=s, d=[s + k, s - k, (first + last) * (n + 1) // 2, first * n], e=f"Ədədi silsilə: {first}, …, {last}; n = {n}. S = ({first} + {last})·{n}/2 = {s}.", diff=H)


def prog_from_sum(r, g):
    a, b = r.randint(1, 4), r.randint(-5, 6)
    k = r.randint(5, 15)
    ak = (a * k * k + b * k) - (a * (k - 1) ** 2 + b * (k - 1))
    return dict(t=f"Ədədi silsilənin ilk n həddinin cəmi Sₙ = {a if a != 1 else ''}n²{sgn(b, 'n')} düsturu ilə verilir. a{_s(k)} həddini tapın.", a=ak,
                d=[a * k * k + b * k, ak + 2 * a, a * k + b, ak - 2 * a], e=f"aₖ = Sₖ − Sₖ₋₁ = {a * k * k + b * k} − {a * (k - 1) ** 2 + b * (k - 1)} = {ak}.", diff=H)


def _s(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


# =============== Funksiyalar ===============

def fn_composition(r, g):
    a, b = r.choice([2, 3, -1, -2]), r.randint(-5, 5)
    c = r.randint(-4, 4)
    k = r.randint(-3, 3)
    gk = k * k + c
    v = a * gk + b
    w = (a * k + b) ** 2 + c
    if r.random() < 0.5:
        return dict(t=f"f(x) = {a}x{sgn(b)}, g(x) = x²{sgn(c)}. f(g({k})) neçədir?", a=v, d=[w, gk, v + 1, a * k + b],
                    e=f"g({k}) = {gk}; f({gk}) = {v}.", diff=M)
    return dict(t=f"f(x) = {a}x{sgn(b)}, g(x) = x²{sgn(c)}. g(f({k})) neçədir?", a=w, d=[v, a * k + b, w + 1, w - c],
                e=f"f({k}) = {a * k + b}; g({a * k + b}) = {w}.", diff=M)


def fn_inverse(r, g):
    a, b, c = r.choice([2, 3, 4, 5]), r.randint(-6, 6), r.choice([1, 2, 3])
    x = r.randint(-5, 8)
    y = F(a * x + b, c)
    return dict(t=f"f(x) = ({a}x{sgn(b)})/{c} funksiyası üçün f⁻¹({fr(y)}) qiymətini tapın." if c != 1 else f"f(x) = {a}x{sgn(b)} funksiyası üçün f⁻¹({fr(y)}) qiymətini tapın.",
                a=x, d=[F(a, 1) * y + b, (y - b) / a if c != 1 else x + 1, -x if x else 2, y], e=f"f(x) = {fr(y)} ⇒ {a}x{sgn(b)} = {fr(y * c)} ⇒ x = {x}.", diff=M)


def fn_vertex(r, g):
    a = r.choice([1, 2, -1, -2, 3])
    h, k = r.randint(-4, 5), r.randint(-9, 9)
    b, c = -2 * a * h, a * h * h + k
    word = "ən kiçik" if a > 0 else "ən böyük"
    return dict(t=f"y = {poly2(a, b, c)} funksiyasının {word} qiymətini tapın.", a=k, d=[h, c, -k if k else 1, k + a],
                e=f"x₀ = −b/(2a) = {h}, y(x₀) = {k}.", diff=M)


def fn_interval(r, g):
    a = 1
    h = r.randint(-2, 3)
    lo, hi = h - r.randint(1, 3), h + r.randint(1, 4)
    k = r.randint(-5, 5)
    f = lambda x: (x - h) ** 2 + k
    ask_max = r.random() < 0.5
    v = max(f(lo), f(hi)) if ask_max else k
    return dict(t=f"y = {poly2(1, -2 * h, h * h + k)} funksiyasının [{lo}; {hi}] parçasında ən {'böyük' if ask_max else 'kiçik'} qiymətini tapın.",
                a=v, d=list({f(lo), f(hi), k, f(lo) + f(hi), h, k - 1} - {v}), e=f"Təpə x = {h} parçaya daxildir; f({h}) = {k}, f({lo}) = {f(lo)}, f({hi}) = {f(hi)}.", diff=H)


def fn_intersections(r, g):
    a, b, c = 1, r.randint(-5, 5), r.randint(-5, 6)
    k, m = r.randint(-4, 4), r.randint(-6, 6)
    D = (b - k) ** 2 - 4 * (c - m)
    n = 2 if D > 0 else 1 if D == 0 else 0
    return dict(t=f"y = {poly2(1, b, c)} parabolası ilə y = {k if k else ''}{'x' if k else ''}{sgn(m) if k else m} düz xəttinin neçə ortaq nöqtəsi var?".replace("y = 1x", "y = x").replace("y = -1x", "y = −x"),
                a=str(n), d=["0", "1", "2", "3", "sonsuz sayda"], e=f"x²{sgn(b - k, 'x')}{sgn(c - m)} = 0, D = {D} ⇒ {n} nöqtə.", diff=H)


def fn_shift(r, g):
    a, b = r.choice([2, 3, -2, 4]), r.randint(-6, 6)
    s = r.choice([1, 2, -1, 3])
    k = r.randint(-3, 5)
    v = a * (k - s) + b
    return dict(t=f"f(x {'+' if s > 0 else '−'} {abs(s)}) = {a}x{sgn(b)} olarsa, f({k}) neçədir?", a=v,
                d=[a * k + b, a * (k + s) + b, v + a, -v if v else 1], e=f"x {'+' if s > 0 else '−'} {abs(s)} = {k} ⇒ x = {k - s}. f({k}) = {a}·{P(k - s)}{sgn(b)} = {v}.", diff=H)


def fn_domain(r, g):
    a = r.randint(-5, 2)
    b = a + r.randint(3, 9)
    c = r.randint(a + 1, b - 1)
    n = b - a + 1 - 1
    return dict(t=f"y = (√(x {'−' if a >= 0 else '+'} {abs(a)}) + √({b} − x)) / (x − {c}) funksiyasının təyin oblastında neçə tam ədəd var?".replace("(x − 0)", "x"),
                a=n, d=[n + 1, n - 1, b - a, b + a if b + a not in (n, n + 1, n - 1) else n + 2], e=f"x ∈ [{a}; {b}] və x ≠ {c}. Tam ədədlər: {b - a + 1} − 1 = {n}.", diff=H)


# =============== Üçbucaqlar və bucaqlar ===============

def tri_ratio(r, g):
    while True:
        p, q, s = sorted(r.sample(range(1, 10), 3))
        if 180 % (p + q + s) == 0:
            break
    k = 180 // (p + q + s)
    ask = r.choice(["ən böyük", "ən kiçik"])
    v = s * k if ask == "ən böyük" else p * k
    return dict(t=f"Üçbucağın bucaqları {p} : {q} : {s} nisbətindədir. Onun {ask} bucağını tapın (dərəcə).", a=v,
                d=[q * k, (s if ask == 'ən kiçik' else p) * k, 180 - v, v + k], e=f"{p + q + s} pay = 180° ⇒ 1 pay = {k}°. Cavab: {v}°.", diff=M)


def tri_isosceles(r, g):
    top = r.choice(range(20, 160, 4))
    base = (180 - top) // 2
    if r.random() < 0.5:
        return dict(t=f"Bərabəryanlı üçbucağın təpə bucağı {top}°-dir. Oturacağa bitişik bucağa qonşu xarici bucağı tapın.", a=180 - base,
                    d=[base, top, 180 - top, 90 + base], e=f"Oturacaq bucağı (180° − {top}°)/2 = {base}°, xarici bucaq 180° − {base}° = {180 - base}°.", diff=H)
    return dict(t=f"Bərabəryanlı üçbucağın oturacağındakı bucaq {base}°-dir. Təpə bucağını tapın.", a=top,
                d=[base, 180 - base, 90 - base if base < 90 else top + 10, 2 * base], e=f"180° − 2·{base}° = {top}°.", diff=M)


def tri_pyth(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 2 + lvl(g))
    a, b, c = a * k, b * k, c * k
    P_ = a + b + c
    if r.random() < 0.5:
        return dict(t=f"Düzbucaqlı üçbucağın hipotenuzu {c}, katetlərindən biri {a}-dir. Üçbucağın perimetrini tapın.".replace(f"{a}-dir", cop(a)), a=P_,
                    d=[a + c + c - a, a * b // 2, P_ + 2, 2 * c + a], e=f"Digər katet √({c}² − {a}²) = {b}. P = {a} + {b} + {c} = {P_}.", diff=M)
    return dict(t=f"Düzbucaqlı üçbucağın katetləri {a} və {b}-dir. Hipotenuza endirilmiş hündürlüyü tapın.".replace(f"{b}-dir", cop(b)), a=F(a * b, c),
                d=[F(c, 2), F(a + b, 2), F(a * b, 2), F(a * b, c) + 1], fmt=dec, e=f"h = ab/c = {a}·{b}/{c} = {dec(F(a * b, c))}.", diff=H)


def tri_similar(r, g):
    k = r.choice([F(2), F(3), F(3, 2), F(5, 2), F(4, 3), F(1, 2)])
    S1 = r.choice([4, 8, 9, 12, 16, 18, 24, 36])
    S2 = S1 * k * k
    return dict(t=f"Oxşar üçbucaqların uyğun tərəfləri {fr(k)} nisbətindədir. Birinci üçbucağın sahəsi {S1} olarsa, ikincinin sahəsini tapın.",
                a=S2, d=[S1 * k, S1 * k * k * k, S1 + k, S1 / k], fmt=dec, e=f"Sahələr nisbəti oxşarlıq əmsalının kvadratına bərabərdir: {S1}·({fr(k)})² = {dec(S2)}.", diff=M)


def tri_bisector(r, g):
    a, b = r.randint(3, 12), r.randint(3, 12)
    while a == b:
        b = r.randint(3, 12)
    c = r.randint(abs(a - b) + 1, a + b - 1)
    part = F(c * a, a + b)
    return dict(t=f"ABC üçbucağında AB = {a}, AC = {b}, BC = {c}. A bucağının tənböləni BC tərəfini BD və DC hissələrinə bölür. BD-ni tapın.",
                a=part, d=[F(c * b, a + b), F(c, 2), F(a * b, c), part + 1], fmt=dec,
                e=f"BD/DC = AB/AC = {a}/{b} ⇒ BD = {c}·{a}/({a} + {b}) = {dec(part)}.", diff=H)


def tri_median(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    return dict(t=f"Düzbucaqlı üçbucağın katetləri {a * k} və {b * k}-dir. Hipotenuza çəkilmiş medianı tapın.".replace(f"{b * k}-dir", cop(b * k)),
                a=F(c * k, 2), d=[c * k, F(a * k + b * k, 2), F(a * b * k, c), F(c * k, 2) + 1], fmt=dec,
                e=f"Hipotenuz {c * k}; düz bucaqdan çəkilən median hipotenuzun yarısıdır: {dec(F(c * k, 2))}.", diff=M)


# =============== Çoxbucaqlılar ===============

def poly_diagonals(r, g):
    n = r.randint(6, 12 + 4 * lvl(g))
    return dict(t=f"Qabarıq {n}-bucaqlının neçə diaqonalı var?", a=n * (n - 3) // 2,
                d=[n * (n - 3), n * (n - 1) // 2, n - 3, n * (n - 2) // 2], e=f"n(n − 3)/2 = {n}·{n - 3}/2 = {n * (n - 3) // 2}.", diff=M)


def poly_find_n(r, g):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    ang = F(180 * (n - 2), n)
    if r.random() < 0.5:
        return dict(t=f"Düzgün çoxbucaqlının daxili bucağı {dec(ang)}°-dir. Onun neçə tərəfi var?", a=n,
                    d=[n + 1, n - 1, n + 2, 2 * n], e=f"Xarici bucaq 180° − {dec(ang)}° = {dec(180 - ang)}°; n = 360° : {dec(180 - ang)}° = {n}.", diff=H)
    S = 180 * (n - 2)
    return dict(t=f"Qabarıq çoxbucaqlının daxili bucaqlarının cəmi {S}°-dir. Onun neçə diaqonalı var?", a=n * (n - 3) // 2,
                d=[n, n * (n - 3), n * (n - 1) // 2, (n - 1) * (n - 4) // 2], e=f"180°(n − 2) = {S}° ⇒ n = {n}; diaqonallar {n}·{n - 3}/2 = {n * (n - 3) // 2}.", diff=H)


def poly_rhombus(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    d1, d2 = 2 * a * k, 2 * b * k
    if r.random() < 0.5:
        return dict(t=f"Rombun diaqonalları {d1} və {d2}-dir. Rombun tərəfini tapın.".replace(f"{d2}-dir", cop(d2)), a=c * k,
                    d=[F(d1 + d2, 2), d1 * d2 // 2, c * k + 1, F(d1 * d2, 4)], fmt=dec, e=f"Yarım-diaqonallar {a * k} və {b * k}; tərəf √({a * k}² + {b * k}²) = {c * k}.", diff=M)
    return dict(t=f"Rombun tərəfi {c * k}, diaqonallarından biri {d1}-dir. Rombun sahəsini tapın.".replace(f"{d1}-dir", cop(d1)), a=d1 * d2 // 2,
                d=[d1 * d2, c * k * d1, (c * k) ** 2, d1 * d2 // 4], e=f"Digər diaqonal 2·√({c * k}² − {a * k}²) = {d2}. S = {d1}·{d2}/2 = {d1 * d2 // 2}.", diff=H)


def poly_trapezoid(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 2)
    small = r.randint(3, 12)
    big = small + 2 * a * k
    h = b * k
    if r.random() < 0.5:
        return dict(t=f"Bərabəryanlı trapesiyanın oturacaqları {small} və {big}, yan tərəfi {c * k}-dir. Sahəsini tapın.".replace(f"{c * k}-dir", cop(c * k)),
                    a=(small + big) * h // 2, d=[(small + big) * h, (small + big) * c * k // 2, small * h, (small + big) * h // 2 + h],
                    e=f"Hündürlük √({c * k}² − {a * k}²) = {h}. S = ({small} + {big})/2·{h} = {(small + big) * h // 2}.", diff=H)
    return dict(t=f"Trapesiyanın orta xətti {F(small + big, 2)}, hündürlüyü {h}-dir. Sahəsini tapın.".replace(f"{h}-dir", cop(h)), a=F(small + big, 2) * h,
                d=[F(small + big, 2) * h / 2, (small + big) * h, F(small + big, 2) + h, F(small + big, 2) * h + h], fmt=dec,
                e=f"S = orta xətt · hündürlük = {dec(F(small + big, 2))}·{h} = {dec(F(small + big, 2) * h)}.", diff=M)


def poly_parallelogram(r, g):
    a, b = r.randint(3, 14), r.randint(3, 14)
    ang = r.choice([30, 150, 60, 45])
    if ang in (30, 150):
        v = F(a * b, 2)
        return dict(t=f"Paraleloqramın tərəfləri {a} və {b}, aralarındakı bucaq {ang}°-dir. Sahəsini tapın.", a=v,
                    d=[a * b, F(a * b, 4), a + b, v + 1], fmt=dec, e=f"S = ab·sin {ang}° = {a}·{b}·1/2 = {dec(v)}.", diff=M)
    root = 3 if ang == 60 else 2
    v = F(a * b, 2)
    ans = f"{fr(v)}√{root}" if v != 1 else f"√{root}"
    return dict(t=f"Paraleloqramın tərəfləri {a} və {b}, aralarındakı bucaq {ang}°-dir. Sahəsini tapın.", a=ans,
                d=[f"{a * b}√{root}", f"{fr(v)}", f"{fr(v)}√{5 - root}", f"{a * b}"], e=f"S = ab·sin {ang}° = {a}·{b}·√{root}/2 = {ans}.", diff=H)


def poly_rect(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    return dict(t=f"Düzbucaqlının diaqonalı {c * k}, bir tərəfi {a * k}-dir. Sahəsini tapın.".replace(f"{a * k}-dir", cop(a * k)), a=a * b * k * k,
                d=[a * c * k * k, 2 * (a + b) * k, (a * b * k * k) // 2, c * c * k * k], e=f"Digər tərəf √({c * k}² − {a * k}²) = {b * k}. S = {a * k}·{b * k} = {a * b * k * k}.", diff=M)


# =============== Çevrə və dairə ===============

def circ_arc(r, g):
    R = r.randint(2, 18)
    ang = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270])
    L = F(ang * R, 180)
    S = F(ang * R * R, 360)
    if r.random() < 0.5:
        return dict(t=f"Radiusu {R} olan çevrədə {ang}°-li qövsün uzunluğunu tapın.", a=pi(L), d=[pi(S), pi(2 * L), pi(L / 2), pi(L + 1)],
                    e=f"l = πRα/180° = π·{R}·{ang}/180 = {pi(L)}.", diff=M)
    return dict(t=f"Radiusu {R} olan dairənin {ang}°-li sektorunun sahəsini tapın.", a=pi(S), d=[pi(L), pi(2 * S), pi(S / 2), pi(S + 1)],
                e=f"S = πR²α/360° = π·{R * R}·{ang}/360 = {pi(S)}.", diff=M)


def circ_chord(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    if r.random() < 0.5:
        return dict(t=f"Radiusu {c * k} olan çevrədə mərkəzdən {a * k} məsafədə olan vətərin uzunluğunu tapın.", a=2 * b * k,
                    d=[b * k, 2 * c * k - a * k, c * k + a * k, 2 * a * k], e=f"Vətərin yarısı √({c * k}² − {a * k}²) = {b * k}; vətər {2 * b * k}.", diff=M)
    return dict(t=f"Çevrənin mərkəzindən {c * k} məsafədəki nöqtədən çevrəyə toxunan çəkilib. Radius {a * k} olarsa, toxunanın uzunluğunu tapın.",
                a=b * k, d=[c * k - a * k, 2 * b * k, c * k + a * k, b * k + 1], e=f"Toxunan radiusa perpendikulyardır: √({c * k}² − {a * k}²) = {b * k}.", diff=H)


def circ_inradius(r, g):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 2)
    a, b, c = a * k, b * k, c * k
    if r.random() < 0.5:
        return dict(t=f"Katetləri {a} və {b} olan düzbucaqlı üçbucağa daxilə çəkilmiş çevrənin radiusunu tapın.", a=F(a + b - c, 2),
                    d=[F(c, 2), F(a * b, a + b + c) * 2, F(a + b, 2), F(a + b - c, 2) + 1], fmt=dec, e=f"r = (a + b − c)/2 = ({a} + {b} − {c})/2 = {dec(F(a + b - c, 2))}.", diff=H)
    return dict(t=f"Katetləri {a} və {b} olan düzbucaqlı üçbucağın xaricinə çəkilmiş çevrənin radiusunu tapın.", a=F(c, 2),
                d=[c, F(a + b - c, 2), F(a + b, 2), F(c, 2) + 1], fmt=dec, e=f"R = hipotenuz/2 = {c}/2 = {dec(F(c, 2))}.", diff=M)


def circ_arcs_ratio(r, g):
    while True:
        p, q, s = sorted(r.sample(range(1, 12), 3))
        if 360 % (p + q + s) == 0 and 180 % (p + q + s) == 0:
            break
    k = 180 // (p + q + s)
    return dict(t=f"Çevrəyə daxilə çəkilmiş üçbucağın təpələri çevrəni {p} : {q} : {s} nisbətində qövslərə bölür. Üçbucağın ən böyük bucağını tapın.",
                a=s * k, d=[2 * s * k, p * k, q * k, s * k + k], e=f"Qövslər {p * 2 * k}°, {q * 2 * k}°, {s * 2 * k}°; daxilə çəkilmiş bucaq qövsün yarısıdır: {s * k}°.",
                diff=H)


def circ_area_ratio(r, g):
    k = r.choice([2, 3, 4, 5, F(3, 2), F(5, 2)])
    return dict(t=f"Çevrənin radiusu {fr(k)} dəfə artırıldı. Dairənin sahəsi neçə dəfə artar?", a=F(k) ** 2,
                d=[F(k), 2 * F(k), F(k) ** 3, F(k) ** 2 + 1], fmt=dec, e=f"Sahə R²-yə mütənasibdir: ({fr(k)})² = {dec(F(k) ** 2)}.", diff=M)


def circ_inscribed(r, g):
    c = r.choice([40, 50, 64, 70, 80, 96, 110, 130, 140, 100, 124])
    if r.random() < 0.5:
        return dict(t=f"AB vətəri çevrəni iki qövsə bölür, kiçik qövs {c}°-dir. Böyük qövsə söykənən daxilə çəkilmiş bucağı tapın.",
                    a=(360 - c) // 2, d=[c // 2, 360 - c, c, 180 - c // 2 + 10], e=f"Böyük qövs 360° − {c}° = {360 - c}°, bucaq onun yarısı: {(360 - c) // 2}°.", diff=H)
    return dict(t=f"Çevrəyə daxilə çəkilmiş bucaq {c // 2}°-dir. Həmin qövsə söykənən mərkəzi bucağı tapın.", a=c,
                d=[c // 2, 180 - c // 2, 2 * c, 90 + c // 2], e=f"Mərkəzi bucaq iki dəfə böyükdür: {c}°.", diff=M)


# =============== Triqonometriya ===============

def trig_special(r, g):
    (n1, v1), (n2, v2) = r.sample(list(TRIG.items()), 2)
    a, b = r.choice([1, 2, 3, 4]), r.choice([1, 2, -2, 3, 6, -1])
    val = a * v1 + b * v2
    t1 = n1 if a == 1 else f"{a}·{n1}"
    t2 = f"{'+' if b > 0 else '−'} {'' if abs(b) == 1 else str(abs(b)) + '·'}{n2}"
    return dict(t=f"Hesablayın: {t1} {t2}", a=val, d=[a * v1 - b * v2, val + 1, -val if val else 2, a * v1, b * v2],
                e=f"{n1} = {fr(v1)}, {n2} = {fr(v2)} ⇒ {fr(val)}.", diff=M)


def trig_identity(r, g):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    if r.random() < 0.5:
        a, b = b, a
    q = r.choice(["I", "II"])
    ask = r.choice(["cos", "tg", "ctg"])
    cosv = F(b, c) if q == "I" else F(-b, c)
    vals = {"cos": cosv, "tg": F(a, c) / cosv, "ctg": cosv / F(a, c)}
    ans = vals[ask]
    return dict(t=f"sin α = {a}/{c} və α {q} rüb bucağıdır. {ask} α-nı tapın.", a=ans,
                d=[-ans, 1 / ans, F(a, c), -1 / ans, F(c, b)], e=f"cos α = {'+' if q == 'I' else '−'}√(1 − sin²α) = {fr(cosv)}; {ask} α = {fr(ans)}.",
                diff=M if q == "I" else H)


def trig_double(r, g):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    if r.random() < 0.5:
        v = F(2 * a * b, c * c)
        return dict(t=f"sin α = {a}/{c}, cos α = {b}/{c}. sin 2α-nı tapın.", a=v, d=[F(2 * a, c), F(a * b, c * c), F(b * b - a * a, c * c), F(a + b, c)],
                    e=f"sin 2α = 2 sin α cos α = {fr(v)}.", diff=M)
    v = F(b * b - a * a, c * c)
    return dict(t=f"sin α = {a}/{c}, cos α = {b}/{c}. cos 2α-nı tapın.", a=v, d=[F(2 * a * b, c * c), -v, F(b - a, c), F(a * a + b * b, c * c)],
                e=f"cos 2α = cos²α − sin²α = ({b * b} − {a * a})/{c * c} = {fr(v)}.", diff=H)


def trig_cosine_law(r, g):
    a, b = r.randint(3, 10), r.randint(3, 10)
    ang = r.choice([60, 120, 90])
    c2 = a * a + b * b - (a * b if ang == 60 else -a * b if ang == 120 else 0)
    return dict(t=f"Üçbucağın iki tərəfi {a} və {b}, onlar arasındakı bucaq {ang}°-dir. Üçüncü tərəfin kvadratını tapın.", a=c2,
                d=list({a * a + b * b, a * a + b * b + a * b, a * a + b * b - a * b, (a + b) ** 2, c2 + a} - {c2}),
                e=f"c² = a² + b² − 2ab·cos {ang}° = {c2}.", diff=H)


def trig_area(r, g):
    a, b = r.randint(3, 14), r.randint(3, 14)
    ang = r.choice([30, 150])
    return dict(t=f"Üçbucağın iki tərəfi {a} və {b}, aralarındakı bucaq {ang}°-dir. Sahəsini tapın.", a=F(a * b, 4),
                d=[F(a * b, 2), a * b, F(a * b, 8), F(a * b, 4) + 1], fmt=dec, e=f"S = ½·ab·sin {ang}° = ½·{a}·{b}·½ = {dec(F(a * b, 4))}.", diff=M)


def trig_reduction(r, g):
    pairs = [("sin(180° − α)", "sin α"), ("cos(180° − α)", "−cos α"), ("sin(90° + α)", "cos α"), ("cos(90° + α)", "−sin α"),
             ("tg(180° + α)", "tg α"), ("cos(360° − α)", "cos α"), ("sin(360° − α)", "−sin α"), ("cos(180° + α)", "−cos α"),
             ("sin(270° − α)", "−cos α"), ("cos(270° + α)", "sin α"), ("tg(90° − α)", "ctg α"), ("ctg(180° − α)", "−ctg α")]
    (e1, a1), (e2, a2) = r.sample(pairs, 2)
    pool = ["sin α", "−sin α", "cos α", "−cos α", "tg α", "−tg α", "ctg α", "−ctg α"]
    if r.random() < 0.5 or g == 9:
        return dict(t=f"Sadələşdirin: {e1}", a=a1, d=[p for p in pool if p != a1], e=f"Çevirmə düsturu: {e1} = {a1}.", diff=M)
    # cəm: eyni funksiya olarsa
    def val(s):
        sign = -1 if s.startswith("−") else 1
        return sign, s.lstrip("−")
    s1, f1 = val(a1)
    s2, f2 = val(a2)
    if f1 != f2:
        return trig_reduction(r, g)
    tot = s1 + s2
    ans = "0" if tot == 0 else (f"2{f1}" if tot == 2 else f"−2{f1}")
    return dict(t=f"Sadələşdirin: {e1} + {e2}", a=ans, d=[x for x in ["0", f"2{f1}", f"−2{f1}", f1, f"−{f1}"] if x != ans],
                e=f"{e1} = {a1}, {e2} = {a2} ⇒ {ans}.", diff=H)


# =============== Orta qiymət və moda ===============

def _nums(r, n, lo, hi):
    return [r.randint(lo, hi) for _ in range(n)]


def stat_mean(r, g):
    n = r.choice([5, 6, 8])
    while True:
        xs = _nums(r, n, 2, 40)
        if sum(xs) % n == 0:
            break
    return dict(t=f"{'; '.join(map(str, xs))} ədədlərinin ədədi ortasını tapın.", a=sum(xs) // n,
                d=[sorted(xs)[n // 2], sum(xs) // n + 1, F(sum(xs), n - 1), max(xs) - min(xs)], fmt=dec, e=f"Cəm {sum(xs)}, say {n}: {sum(xs) // n}.", diff=M)


def stat_median_even(r, g):
    n = r.choice([6, 8])
    xs = sorted(r.sample(range(1, 60), n))
    med = F(xs[n // 2 - 1] + xs[n // 2], 2)
    sh = xs[:]
    r.shuffle(sh)
    return dict(t=f"{'; '.join(map(str, sh))} ədədlər sırasının medianını tapın.", a=med,
                d=[xs[n // 2], xs[n // 2 - 1], F(sum(xs), n), sh[n // 2] if sh[n // 2] != med else med + 1], fmt=dec,
                e=f"Artan sıra: {'; '.join(map(str, xs))}. Ortadakı iki ədədin ortası: ({xs[n // 2 - 1]} + {xs[n // 2]})/2 = {dec(med)}.", diff=H)


def stat_mode_range(r, g):
    base = r.sample(range(1, 30), 5)
    m = r.choice(base)
    xs = base + [m, m]
    r.shuffle(xs)
    if r.random() < 0.5:
        return dict(t=f"{'; '.join(map(str, xs))} sırasının modasını tapın.", a=m, d=[x for x in base if x != m][:3] + [max(xs) - min(xs)],
                    e=f"Ən çox təkrarlanan ədəd {m}-dir (3 dəfə).".replace(f"{m}-dir", cop(m)), diff=M)
    return dict(t=f"{'; '.join(map(str, xs))} sırasının moda ilə yayılma (variasiya) genişliyinin cəmini tapın.", a=m + max(xs) - min(xs),
                d=[m, max(xs) - min(xs), m + max(xs), max(xs) + min(xs)], e=f"Moda {m}, genişlik {max(xs)} − {min(xs)} = {max(xs) - min(xs)}. Cəm: {m + max(xs) - min(xs)}.",
                diff=H)


def stat_missing(r, g):
    n = r.choice([5, 6, 7])
    m = r.randint(8, 30)
    xs = _nums(r, n - 1, 1, 40)
    x = n * m - sum(xs)
    if x < -20 or x > 80:
        return stat_missing(r, g)
    return dict(t=f"{n} ədədin ədədi ortası {m}-dir. Onlardan {n - 1}-i: {'; '.join(map(str, xs))}. Sonuncu ədədi tapın.".replace(f"{m}-dir", cop(m)), a=x,
                d=[m, x + 1, n * m, x - n], e=f"Cəm {n}·{m} = {n * m}; məlum ədədlərin cəmi {sum(xs)}; x = {x}.", diff=M)


def stat_add(r, g):
    n, m = r.randint(4, 12), r.randint(10, 40)
    x = r.randint(0, 90)
    v = F(n * m + x, n + 1)
    return dict(t=f"{n} ədədin ədədi ortası {m}-dir. Onlara {x} ədədi əlavə edildi. Yeni ədədi orta neçədir?".replace(f"{m}-dir", cop(m)), a=v,
                d=[F(m + x, 2), m, F(n * m + x, n), v + 1], fmt=dec, e=f"({n}·{m} + {x})/{n + 1} = {dec(v)}.", diff=H)


def stat_weighted(r, g):
    n1, n2 = r.randint(10, 30), r.randint(10, 30)
    m1, m2 = r.randint(50, 95), r.randint(50, 95)
    v = F(n1 * m1 + n2 * m2, n1 + n2)
    return dict(t=f"A sinfində {n1} şagirdin orta balı {m1}, B sinfində {n2} şagirdin orta balı {m2}-dir. İki sinfin birlikdə orta balını tapın.".replace(f"{m2}-dir", cop(m2)),
                a=v, d=[F(m1 + m2, 2), v + 1, F(m1 * n2 + m2 * n1, n1 + n2), v - 1], fmt=dec, e=f"({n1}·{m1} + {n2}·{m2})/{n1 + n2} = {dec(v)}.", diff=H)


# =============== Ehtimal ===============

def prob_dice(r, g):
    kind = r.choice(["sum", "prod", "six", "diff"])
    pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    if kind == "sum":
        s = r.randint(3, 11)
        w = sum(1 for a, b in pairs if a + b == s)
        txt = f"xalların cəminin {s} olması"
    elif kind == "prod":
        s = r.choice([6, 12, 4, 8, 18])
        w = sum(1 for a, b in pairs if a * b == s)
        txt = f"xalların hasilinin {s} olması"
    elif kind == "six":
        w, txt = 11, "ən azı birində 6 düşməsi"
    else:
        s = r.randint(1, 4)
        w = sum(1 for a, b in pairs if abs(a - b) == s)
        txt = f"xalların fərqinin modulunun {s} olması"
    p = F(w, 36)
    return dict(t=f"İki zər atılır. {txt[0].upper() + txt[1:]} ehtimalını tapın.", a=p, d=[F(w, 12), F(1, 6), p + F(1, 36), F(w + 2, 36), F(1, 36)],
                e=f"Əlverişli hallar {w}, bütün hallar 36: P = {fr(p)}.", diff=M)


def prob_coins(r, g):
    n = r.choice([3, 4])
    k = r.randint(1, n - 1)
    if r.random() < 0.5:
        p = F(math.comb(n, k), 2 ** n)
        return dict(t=f"{n} sikkə atılır. Düz {k} dəfə gerb düşməsi ehtimalını tapın.", a=p, d=[F(1, n), F(k, n), F(1, 2 ** n), p + F(1, 2 ** n)],
                    e=f"C({n}; {k}) / 2^{n} = {math.comb(n, k)}/{2 ** n} = {fr(p)}.", diff=M)
    p = 1 - F(1, 2 ** n)
    return dict(t=f"{n} sikkə atılır. Ən azı bir dəfə gerb düşməsi ehtimalını tapın.", a=p, d=[F(1, 2), F(1, 2 ** n), F(n, 2 ** n), F(n - 1, n)],
                e=f"Əks hadisə — heç gerb düşməməsi: 1/{2 ** n}. P = 1 − 1/{2 ** n} = {fr(p)}.", diff=H)


def prob_urn(r, g):
    red, blue = r.randint(2, 7), r.randint(2, 7)
    n = red + blue
    if r.random() < 0.5:
        p = F(red * (red - 1) + blue * (blue - 1), n * (n - 1))
        return dict(t=f"Qutuda {red} qırmızı və {blue} göy kürə var. Qaytarmadan ardıcıl 2 kürə götürülür. Hər ikisinin eyni rəngdə olması ehtimalını tapın.",
                    a=p, d=[F(red * red + blue * blue, n * n), 1 - p, F(1, 2), F(red * (red - 1), n * (n - 1))],
                    e=f"P = ({red}·{red - 1} + {blue}·{blue - 1}) / ({n}·{n - 1}) = {fr(p)}.", diff=H)
    p = F(2 * red * blue, n * (n - 1))
    return dict(t=f"Qutuda {red} qırmızı və {blue} göy kürə var. Qaytarmadan 2 kürə götürülür. Kürələrin müxtəlif rəngdə olması ehtimalını tapın.",
                a=p, d=[F(red * blue, n * n), 1 - p, F(red * blue, n * (n - 1)), F(1, 2) if p != F(1, 2) else F(1, 3)],
                e=f"P = 2·{red}·{blue} / ({n}·{n - 1}) = {fr(p)}.", diff=H)


def prob_divisible(r, g):
    N = r.choice([20, 30, 40, 50, 60, 100])
    a, b = r.choice([(2, 3), (3, 5), (2, 5), (4, 6), (3, 4)])
    lcm = a * b // math.gcd(a, b)
    cnt = N // a + N // b - N // lcm
    p = F(cnt, N)
    return dict(t=f"1-dən {N}-ə qədər natural ədədlərdən biri təsadüfi seçilir. Onun {a}-ə və ya {b}-ə bölünməsi ehtimalını tapın.".replace(f"{N}-ə", dat(N)).replace(f"{a}-ə", dat(a)).replace(f"{b}-ə", dat(b)),
                a=p, d=[F(N // a + N // b, N), F(N // lcm, N), F(1, a) * F(1, b), p + F(1, N)],
                e=f"{a}-ə bölünən {N // a}, {b}-ə bölünən {N // b}, hər ikisinə ({lcm}-ə) bölünən {N // lcm}. Say: {cnt}. P = {fr(p)}.".replace(f"{a}-ə", dat(a)).replace(f"{b}-ə", dat(b)).replace(f"{lcm}-ə", dat(lcm)),
                diff=H)


def prob_seats(r, g):
    n = r.randint(4, 9)
    p = F(2, n)
    return dict(t=f"{n} nəfər bir cərgədə təsadüfi oturur. Müəyyən iki nəfərin yanaşı oturması ehtimalını tapın.", a=p,
                d=[F(1, n), F(2, n - 1), F(1, n - 1), F(2, n * (n - 1))], e=f"Yanaşı oturma halları 2·{n - 1}!, bütün hallar {n}!. P = 2/{n} = {fr(p)}.", diff=H)


def prob_complement(r, g):
    p = r.choice([F(1, 3), F(2, 5), F(3, 10), F(1, 4), F(3, 8)])
    q = r.choice([F(1, 2), F(2, 3), F(3, 5), F(4, 5)])
    v = 1 - (1 - p) * (1 - q)
    return dict(t=f"İki atıcı hədəfə bir dəfə atəş açır. Birincinin vurma ehtimalı {fr(p)}, ikincinin {fr(q)}-dir. Hədəfin ən azı bir dəfə vurulması ehtimalını tapın.".replace(f"{fr(q)}-dir", cop(q)),
                a=v, d=[p * q, p + q if p + q < 1 else F(9, 10), (1 - p) * (1 - q), v - p * q], e=f"P = 1 − (1 − {fr(p)})(1 − {fr(q)}) = {fr(v)}.", diff=H)


TOPICS = {
    "num-real": [real_conj, real_square, real_count, real_compare, real_repeating, real_nested],
    "num-frac": [frac_expr, frac_continued, frac_part, frac_pool, frac_min, frac_decimal],
    "num-pow": [pow_laws, pow_base2, pow_fractional, pow_lastdigit, pow_compare, pow_standard],
    "num-abs": [abs_product, abs_ineq, abs_sqrt_expr, abs_min_sum, abs_linear, abs_double],
    "num-pct": [pct_chain, pct_reverse, pct_mixture, pct_compound, pct_area, pct_of_pct],
    "alg-eq": [eq_fractions, eq_rational, eq_param, eq_age, eq_speed, eq_biquad],
    "alg-sys": [sys_linear, sys_word, sys_nosol, sys_symmetric, sys_three, sys_diff_squares],
    "alg-quad": [quad_sq_sum, quad_recip, quad_one_root, quad_ineq, quad_diff, quad_cubes],
    "alg-prog": [prog_two_terms, prog_sum, prog_geom_sum, prog_infinite, prog_multiples, prog_from_sum],
    "alg-func": [fn_composition, fn_inverse, fn_vertex, fn_interval, fn_intersections, fn_shift, fn_domain],
    "geo-basic": [tri_ratio, tri_isosceles, tri_pyth, tri_similar, tri_bisector, tri_median],
    "geo-poly": [poly_diagonals, poly_find_n, poly_rhombus, poly_trapezoid, poly_parallelogram, poly_rect],
    "geo-circle": [circ_arc, circ_chord, circ_inradius, circ_arcs_ratio, circ_area_ratio, circ_inscribed],
    "geo-trig": [trig_special, trig_identity, trig_double, trig_cosine_law, trig_area, trig_reduction],
    "stat-avg": [stat_mean, stat_median_even, stat_mode_range, stat_missing, stat_add, stat_weighted],
    "stat-prob": [prob_dice, prob_coins, prob_urn, prob_divisible, prob_seats, prob_complement],
}

if __name__ == "__main__":
    for g in (9, 10, 11):
        topics = {tid: build_topic(g, "math", tid, tpls, seed=7000, open_every=7) for tid, tpls in TOPICS.items()}
        save_grade(g, "math", topics)
