"""Riyaziyyat · Ədədlər və hesablama: num-real, num-frac, num-pow, num-abs, num-pct."""
import math
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import permutations

from common import dec
from mx import Num, M, H, MINUS, surd, lin_surd, show, neg, par, is_sq

getcontext().prec = 60
SQF = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30, 31, 33]


def ap(x):
    return f"{x:.2f}".replace(".", ",")


def sq(n):
    return f"√{n}"


def pc(x):
    """Faiz cavabı: Num('12,5%', 12.5)"""
    x = F(x)
    if not terminating(x):
        return Num(neg(f"{float(x):.1f}".replace(".", ",")) + "%", float(x))
    return Num(neg(dec(x)) + "%", x)


def xm(a, v="x"):
    """«x − 3», «x + 4», «x»"""
    a = F(a)
    if a == 0:
        return v
    return f"{v} − {show(a)}" if a > 0 else f"{v} + {show(-a)}"


def terminating(x):
    d = F(x).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def order_q(r, names, vals, exact_vals, what="ədədləri"):
    """Sıralama sualı: variantlar «a < b < c» şəklində permutasiyalardır."""
    perms = list(permutations(range(3)))
    true = tuple(sorted(range(3), key=lambda i: exact_vals[i]))
    chk_true = tuple(sorted(range(3), key=lambda i: vals[i]))
    txt = lambda p: " < ".join(names[i] for i in p)
    others = [p for p in perms if p != true]
    r.shuffle(others)
    a = Num(txt(true), 1)
    d = [Num(txt(p), k + 2) for k, p in enumerate(others[:4])]
    return a, d, (1 if chk_true == true else 0)


# ======================= num-real =======================

def real_denest(r, g):
    while True:
        p, q = r.sample(SQF[:14], 2)
        if p < q:
            p, q = q, p
        if not is_sq(p * q):
            break
    S, P = p + q, p * q
    a = surd(2, q)
    chk = math.sqrt(S + 2 * math.sqrt(P)) - math.sqrt(S - 2 * math.sqrt(P))
    return dict(t=f"Hesablayın: √({S} + 2√{P}) − √({S} − 2√{P})", a=a,
                d=[surd(2, p), Num(f"√{p} − √{q}", math.sqrt(p) - math.sqrt(q)), surd(2, S), surd(1, 2 * q),
                   Num(f"2√{p} − 2√{q}", 2 * math.sqrt(p) - 2 * math.sqrt(q))],
                e=f"{S} ± 2√{P} = (√{p} ± √{q})², çünki {p} + {q} = {S} və {p}·{q} = {P}. "
                  f"Fərq: (√{p} + √{q}) − (√{p} − √{q}) = 2√{q}.", chk=chk, diff=H)


def real_count(r, g):
    a = r.choice([x for x in range(10, 200) if not is_sq(x)])
    b = r.choice([x for x in range(20, 900) if round(x ** (1 / 3)) ** 3 != x])
    lo = -math.isqrt(a)
    hi = max(x for x in range(0, 20) if x ** 3 < b)
    ans = hi - lo + 1
    chk = sum(1 for x in range(-100, 100) if (x >= 0 or x * x <= a) and x ** 3 < b)
    return dict(t=f"−√{a} ≤ x < ∛{b} bərabərsizliyini ödəyən neçə tam x ədədi var?", a=ans,
                d=[ans - 1, ans + 1, ans - 2, ans + 2],
                e=f"√{a} ≈ {ap(math.sqrt(a))}, deməli x ≥ {neg(str(lo))}. "
                  f"{hi}³ = {hi ** 3} < {b}, {hi + 1}³ = {(hi + 1) ** 3} ≥ {b}, deməli x ≤ {hi}. "
                  f"Tam ədədlər: {neg(str(lo))}, …, {hi} — cəmi {ans}.", chk=chk, diff=M)


def real_repdec(r, g):
    ab = r.randint(10, 98)
    while ab % 11 == 0:
        ab = r.randint(10, 98)
    c, de = r.randint(1, 9), r.randint(10, 98)
    while de % 11 == 0:
        de = r.randint(10, 98)
    x = F(ab, 99)
    y = F(c * 100 + de - c, 990)
    ans = x + y
    s1 = "0." + str(ab) * 20
    s2 = "0." + str(c) + str(de) * 20
    chk = float(Decimal(s1) + Decimal(s2))
    return dict(t=f"Cəmi adi kəsr şəklində yazın: 0,({ab}) + 0,{c}({de})", a=ans,
                d=[F(ab, 99) + F(c * 100 + de, 990), F(ab, 99) + F(c * 100 + de, 999), F(ab, 90) + y,
                   F(ab, 99) + F(c * 100 + de - c, 999)],
                e=f"0,({ab}) = {ab}/99; 0,{c}({de}) = ({c}{de:02d} − {c})/990 = {show(y)}. Cəm: {show(ans)}.",
                chk=chk, diff=M)


def real_order_k(r, g):
    while True:
        items = []
        for _ in range(3):
            k, m = r.randint(2, 7), r.choice([2, 3, 5, 6, 7])
            items.append((k, m))
        exact = [k * k * m for k, m in items]
        if len(set(exact)) == 3 and len({m for _, m in items}) >= 2:
            vals = [k * math.sqrt(m) for k, m in items]
            if min(abs(vals[i] - vals[j]) for i in range(3) for j in range(i + 1, 3)) < 0.6:
                break
    nm = ["a", "b", "c"]
    defs = ", ".join(f"{n} = {k}√{m}" for n, (k, m) in zip(nm, items))
    a, d, ok = order_q(r, nm, vals, exact)
    return dict(t=f"{defs}. Ədədləri artan sırada düzün.", a=a, d=d, chk=ok and 1,
                e="Kvadratlarını müqayisə edin: " + ", ".join(f"{n}² = {k * k}·{m} = {k * k * m}" for n, (k, m) in zip(nm, items))
                  + f". Ardıcıllıq: {a.s}.", open=False, diff=M)


def real_order_diff(r, g):
    """a = √(n+d) − √n tipli fərqlər: n böyüdükcə fərq kiçilir"""
    while True:
        base = r.sample(range(5, 60), 3)
        dd = r.choice([1, 2, 3])
        items = [(n + dd, n) for n in base]
        if all(not is_sq(x) and not is_sq(y) for x, y in items):
            break
    k = r.choice([2, 3])
    # üçüncüsünü başqa formada ver: (√(n+dd) − √n) əvəzinə k/(√(n+dd·k... sadəcə dd/(√x+√y))
    nm = ["a", "b", "c"]
    texts = [f"√{x} − √{y}" for x, y in items[:2]] + [f"{dd}/(√{items[2][0]} + √{items[2][1]})"]
    exact = [-(math.sqrt(x) + math.sqrt(y)) for x, y in items]  # böyük cəm → kiçik fərq
    vals = [float(Decimal(x).sqrt() - Decimal(y).sqrt()) for x, y in items]
    a, d, ok = order_q(r, nm, vals, exact)
    return dict(t=", ".join(f"{n} = {t}" for n, t in zip(nm, texts)) + ". Ədədləri artan sırada düzün.",
                a=a, d=d, chk=ok and 1, open=False,
                e=f"√x − √y = (x − y)/(√x + √y) = {dd}/(√x + √y). Surətlər eynidir, məxrəci böyük olan kiçikdir. "
                  f"Ardıcıllıq: {a.s}.", diff=H)


def real_conj(r, g):
    while True:
        a_, b_ = r.sample(range(2, 30), 2)
        if a_ < b_:
            a_, b_ = b_, a_
        if not is_sq(a_ * b_) and not is_sq(a_) and not is_sq(b_):
            break
    k = a_ - b_
    ans = lin_surd(F(a_ + b_, k), F(2, k), a_ * b_)
    chk = (math.sqrt(a_) + math.sqrt(b_)) / (math.sqrt(a_) - math.sqrt(b_))
    return dict(t=f"Sadələşdirin: (√{a_} + √{b_}) / (√{a_} − √{b_})", a=ans,
                d=[lin_surd(F(a_ + b_, k), F(1, k), a_ * b_), lin_surd(F(a_ + b_, k), F(-2, k), a_ * b_),
                   lin_surd(F(a_ - b_, a_ + b_), F(2, a_ + b_), a_ * b_), lin_surd(1, F(2, k), a_ * b_),
                   lin_surd(F(a_ + b_, k), 2, a_ * b_)],
                e=f"Surəti və məxrəci (√{a_} + √{b_})-yə vurun: ({a_} + {b_} + 2√{a_ * b_}) / ({a_} − {b_}) = {ans.s}.",
                chk=chk, diff=H)


def real_telescope(r, g):
    step = 1 if g == 10 else 2
    if step == 1:
        m = r.choice([1, 4, 9, 16, 25])
        n1 = r.choice([s * s for s in range(math.isqrt(m) + 2, 16)])
        n = n1 - 1
        terms = f"1/(√{m} + √{m + 1}) + 1/(√{m + 1} + √{m + 2}) + … + 1/(√{n} + √{n + 1})"
        ans = math.isqrt(n1) - math.isqrt(m)
        chk = sum(1 / (math.sqrt(k) + math.sqrt(k + 1)) for k in range(m, n + 1))
        e = f"1/(√k + √(k+1)) = √(k+1) − √k. Cəm teleskopik olur: √{n + 1} − √{m} = {ans}."
        d = [math.isqrt(n1) + math.isqrt(m), n1 - m, ans + 1, ans - 1, 2 * ans]
    else:
        m = r.choice([1, 9, 25, 49, 3, 5, 7])  # tək başlanğıc
        if is_sq(m):
            last2 = r.choice([s * s for s in range(math.isqrt(m) + 2, 22, 2)])  # m-lə eyni cütlük, tək kvadrat
        else:
            last2 = None
        if last2 is None or last2 % 2 != m % 2:
            m = r.choice([1, 9, 25])
            last2 = r.choice([s * s for s in range(math.isqrt(m) + 2, 22, 2)])
        n = last2 - 2
        terms = f"1/(√{m} + √{m + 2}) + 1/(√{m + 2} + √{m + 4}) + … + 1/(√{n} + √{n + 2})"
        ans = F(math.isqrt(last2) - math.isqrt(m), 2)
        chk = sum(1 / (math.sqrt(k) + math.sqrt(k + 2)) for k in range(m, n + 1, 2))
        e = (f"1/(√k + √(k+2)) = (√(k+2) − √k)/2. Cəm teleskopik olur: (√{n + 2} − √{m})/2 = {show(ans)}.")
        d = [2 * ans, ans + 1, ans - F(1, 2), F(math.isqrt(last2) + math.isqrt(m), 2), ans + F(1, 2)]
    return dict(t=f"Hesablayın: {terms}", a=ans, d=d, e=e, chk=chk, diff=H)


def real_nested_abs(r, g):
    m = r.randint(2, 6)
    n = r.choice([x for x in range(2, 45) if not is_sq(x) and abs(x - m * m) > 1])
    S, T = m * m + n, 2 * m
    if m > math.sqrt(n):
        ans, how = F(2 * m), f"{m} > √{n}, deməli |{m} − √{n}| = {m} − √{n}. Cəm: 2·{m} = {2 * m}."
        a = ans
        d = [surd(2, n), Num(f"{2 * m} + 2√{n}", 2 * m + 2 * math.sqrt(n)), F(2 * m + 1), F(m), Num(f"2√{n} − {2 * m}", 2 * math.sqrt(n) - 2 * m)]
    else:
        a = surd(2, n)
        how = f"{m} < √{n}, deməli |{m} − √{n}| = √{n} − {m}. Cəm: 2√{n}."
        d = [F(2 * m), surd(1, n), Num(f"{2 * m} + 2√{n}", 2 * m + 2 * math.sqrt(n)), surd(2, n + 1), Num(f"2√{n} − {m}", 2 * math.sqrt(n) - m)]
    chk = math.sqrt(S + T * math.sqrt(n)) + math.sqrt(S - T * math.sqrt(n))
    return dict(t=f"Hesablayın: √({S} + {T}√{n}) + √({S} − {T}√{n})", a=a, d=d,
                e=f"{S} ± {T}√{n} = ({m} ± √{n})². √((m − √n)²) = |m − √n|. {how}", chk=chk, diff=M)


PELL = [(2, 3), (3, 8), (4, 15), (5, 24), (6, 35), (7, 48), (8, 63), (9, 80), (10, 99)]


def real_pell(r, g):
    p, q = r.choice(PELL)
    s = 2 * p
    k = 2 if g == 10 else r.choice([3, 4])
    sgn = r.choice([1, -1]) if g == 11 else 1
    xs = f"{p} + √{q}" if sgn > 0 else f"{p} − √{q}"
    x = p + sgn * math.sqrt(q)
    if k == 2:
        ans, d = s * s - 2, [s * s, s * s + 2, s * s - 4, 2 * (p * p + q)]
        e = f"1/x = {p} {'−' if sgn > 0 else '+'} √{q} (çünki {p}² − {q} = 1), x + 1/x = {s}. x² + 1/x² = {s}² − 2 = {ans}."
    elif k == 3:
        ans, d = s ** 3 - 3 * s, [s ** 3, s ** 3 - s, s ** 3 + 3 * s, s ** 3 - 6 * s]
        e = f"1/x = {p} {'−' if sgn > 0 else '+'} √{q}, x + 1/x = {s}. x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x) = {s ** 3} − {3 * s} = {ans}."
    else:
        t = s * s - 2
        ans, d = t * t - 2, [t * t, t * t + 2, s ** 4 - 2, t * t - 4]
        e = f"1/x = {p} {'−' if sgn > 0 else '+'} √{q}, x + 1/x = {s}, x² + 1/x² = {t}, x⁴ + 1/x⁴ = {t}² − 2 = {ans}."
    sup = {2: "²", 3: "³", 4: "⁴"}[k]
    return dict(t=f"x = {xs} olarsa, x{sup} + 1/x{sup} ifadəsinin qiymətini tapın.", a=ans, d=d, e=e,
                chk=x ** k + x ** (-k), diff=H)


def real_recip_sq(r, g):
    while True:
        a_, b_ = r.sample(range(2, 25), 2)
        if a_ < b_:
            a_, b_ = b_, a_
        if not is_sq(a_ * b_):
            break
    k = a_ - b_
    ans = F(2 * (a_ + b_), k * k)
    x, y = 1 / (math.sqrt(a_) - math.sqrt(b_)), 1 / (math.sqrt(a_) + math.sqrt(b_))
    return dict(t=f"x = 1/(√{a_} − √{b_}) və y = 1/(√{a_} + √{b_}) olarsa, x² + y² ifadəsinin qiymətini tapın.", a=ans,
                d=[F(2 * (a_ + b_), k), F(a_ + b_, k * k), F(4 * (a_ + b_), k * k), F(2 * (a_ + b_) + 2, k * k)],
                e=f"x = (√{a_} + √{b_})/{k}, y = (√{a_} − √{b_})/{k}. x + y = 2√{a_}/{k}, xy = 1/{k}. "
                  f"x² + y² = (x + y)² − 2xy = {4 * a_}/{k * k} − 2/{k} = {show(ans)}.",
                chk=x * x + y * y, diff=H)


def real_intpart(r, g):
    while True:
        a_, b_ = r.sample(range(2, 40), 2)
        v = 2 * math.sqrt(a_ * b_)
        fr_ = v - math.floor(v)
        if not is_sq(a_ * b_) and 0.08 < fr_ < 0.92:
            break
    ans = a_ + b_ + math.isqrt(4 * a_ * b_)
    chk = math.floor(float((Decimal(a_).sqrt() + Decimal(b_).sqrt()) ** 2))
    return dict(t=f"(√{a_} + √{b_})² ədədinin tam hissəsini tapın.", a=ans,
                d=[ans + 1, ans - 1, a_ + b_, ans + 2, ans - 2],
                e=f"(√{a_} + √{b_})² = {a_ + b_} + 2√{a_ * b_} = {a_ + b_} + √{4 * a_ * b_}. "
                  f"{math.isqrt(4 * a_ * b_)}² ≤ {4 * a_ * b_} < {math.isqrt(4 * a_ * b_) + 1}², deməli tam hissə {ans}.",
                chk=chk, diff=H)


# ======================= num-frac =======================

def frac_telescope(r, g):
    if g == 9:
        a = r.randint(2, 12)
        b = r.randint(a + 5, a + 40)
        ans = F(1, a) - F(1, b + 1)
        chk = sum(F(1, k * (k + 1)) for k in range(a, b + 1))
        t = f"1/({a}·{a + 1}) + 1/({a + 1}·{a + 2}) + … + 1/({b}·{b + 1})"
        e = f"1/(k(k+1)) = 1/k − 1/(k+1). Cəm: 1/{a} − 1/{b + 1} = {show(ans)}."
        d = [F(1, a) - F(1, b), F(1, a + 1) - F(1, b + 1), F(1, a) + F(1, b + 1), F(b - a + 1, a * (b + 1) + 1)]
    elif g == 10:
        s = r.choice([2, 3, 4, 5])
        a = r.randint(1, 9)
        n = r.randint(6, 18)
        last = a + s * (n - 1)
        ans = (F(1, a) - F(1, last + s)) / s
        chk = sum(F(1, k * (k + s)) for k in range(a, last + 1, s))
        t = f"1/({a}·{a + s}) + 1/({a + s}·{a + 2 * s}) + … + 1/({last}·{last + s})"
        e = f"1/(k(k+{s})) = (1/k − 1/(k+{s}))/{s}. Cəm: (1/{a} − 1/{last + s})/{s} = {show(ans)}."
        d = [F(1, a) - F(1, last + s), (F(1, a) - F(1, last)) / s, (F(1, a) - F(1, last + s)) * s, (F(1, a + s) - F(1, last + s)) / s]
    else:
        a = r.randint(1, 8)
        b = r.randint(a + 4, a + 25)
        ans = (F(1, a * (a + 1)) - F(1, (b + 1) * (b + 2))) / 2
        chk = sum(F(1, k * (k + 1) * (k + 2)) for k in range(a, b + 1))
        t = f"1/({a}·{a + 1}·{a + 2}) + 1/({a + 1}·{a + 2}·{a + 3}) + … + 1/({b}·{b + 1}·{b + 2})"
        e = (f"1/(k(k+1)(k+2)) = ½·[1/(k(k+1)) − 1/((k+1)(k+2))]. "
             f"Cəm: ½·(1/{a * (a + 1)} − 1/{(b + 1) * (b + 2)}) = {show(ans)}.")
        d = [F(1, a * (a + 1)) - F(1, (b + 1) * (b + 2)), (F(1, a * (a + 1)) - F(1, b * (b + 1))) / 2,
             (F(1, a) - F(1, b + 2)) / 2, (F(1, a * (a + 1)) + F(1, (b + 1) * (b + 2))) / 2]
    return dict(t=f"Hesablayın: {t}", a=ans, d=d, e=e, chk=chk, diff=H)


def frac_continued(r, g):
    a, b, c, d_ = r.randint(1, 4), r.randint(2, 5), r.randint(2, 6), r.randint(2, 7)
    ans = a + 1 / (b + 1 / (c + F(1, d_)))
    chk = a + 1 / (b + 1 / (c + 1 / d_))
    return dict(t=f"Hesablayın: {a} + 1/({b} + 1/({c} + 1/{d_}))", a=ans,
                d=[a + 1 / (b + F(1, c + d_)), a + F(1, b) + F(1, c) + F(1, d_), a + 1 / (b + F(1, c + d_)) + F(1, 1000) * 0 + F(1, b * c),
                   a + 1 / (b + c + F(1, d_)), a + 1 / (b + F(1, c))],
                e=f"İçəridən başlayın: {c} + 1/{d_} = {show(c + F(1, d_))}; {b} + 1 : ({show(c + F(1, d_))}) = {show(b + 1 / (c + F(1, d_)))}; "
                  f"{a} + 1 : ({show(b + 1 / (c + F(1, d_)))}) = {show(ans)}.", chk=chk, diff=M)


def frac_remainder(r, g):
    while True:
        p, q, s = r.randint(3, 7), r.randint(2, 6), r.randint(3, 8)
        left_frac = (1 - F(1, p)) * (1 - F(1, q)) * (1 - F(1, s))
        k = r.randint(2, 12)
        N = k * left_frac.denominator
        X = N * left_frac
        if X.denominator == 1 and 100 <= N <= 3000:
            break
    # müstəqil: irəli simulyasiya
    m = F(N)
    m -= m / p
    m -= m / q
    m -= m / s
    assert m == X
    wrong = X / (1 - F(1, p) - F(1, q) - F(1, s)) if (1 - F(1, p) - F(1, q) - F(1, s)) > 0 else X * 3
    return dict(t=f"Şagird pulunun 1/{p} hissəsini kitaba, qalanın 1/{q} hissəsini dəftərə, yenə qalanın 1/{s} hissəsini "
                  f"qələmə xərclədi. Ondan {X} manat qaldı. Şagirdin əvvəlcə neçə manatı var idi?",
                a=N, d=[wrong, N + left_frac.denominator, N - left_frac.denominator, X * p, X / ((1 - F(1, p)) * (1 - F(1, q)))],
                e=f"Hər dəfə qalanın (1 − 1/n) hissəsi qalır: x·{show(1 - F(1, p))}·{show(1 - F(1, q))}·{show(1 - F(1, s))} = {X}, "
                  f"x·{show(left_frac)} = {X}, x = {N}.", chk=m * N / X, diff=H)


def frac_ratio_expr(r, g):
    while True:
        p, q = r.randint(1, 9), r.randint(1, 9)
        if math.gcd(p, q) == 1 and p != q:
            break
    a, b, c, d_ = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    t = F(p, q)
    num = a * t * t - b * t
    den = c + d_ * t
    if den == 0 or num == 0:
        return frac_ratio_expr(r, g)
    ans = num / den
    x, y = p, q
    chk = F(a * x * x - b * x * y, c * y * y + d_ * x * y)
    return dict(t=f"x : y = {p} : {q} olarsa, ({a if a > 1 else ''}x² − {b if b > 1 else ''}xy) / ({c if c > 1 else ''}y² + {d_ if d_ > 1 else ''}xy) ifadəsinin qiymətini tapın.",
                a=ans, d=[F(a * p * p - b * p, c + d_ * p) if c + d_ * p else ans + 1, F(a * q * q - b * p * q, c * p * p + d_ * p * q) if c * p * p + d_ * p * q else ans - 1,
                          -ans, F(a * p * p + b * p * q, c * q * q + d_ * p * q), 1 / ans if ans else ans + 2],
                e=f"Surəti və məxrəci y²-yə bölün, t = x/y = {show(t)}: ({a}t² − {b}t)/({c} + {d_}t) = "
                  f"({show(a * t * t)} − {show(b * t)})/({c} + {show(d_ * t)}) = {show(ans)}.",
                chk=chk, diff=H)


def frac_largest(r, g):
    while True:
        base = r.randint(20, 400)
        ks = r.sample(range(1, 9), 5)
        fr_list = [F(base + k * r.choice([1, 2]), base + k * r.choice([2, 3]) + 1) for k in ks]
        texts = [f"{f.numerator}/{f.denominator}" for f in fr_list]
        if len(set(fr_list)) == 5 and all(f.denominator > f.numerator for f in fr_list):
            break
    best = max(fr_list)
    # müstəqil: çarpaz vurma ilə
    chk_best = fr_list[0]
    for f in fr_list[1:]:
        if f.numerator * chk_best.denominator > chk_best.numerator * f.denominator:
            chk_best = f
    names = ", ".join(texts)
    return dict(t=f"Kəsrlərdən ən böyüyünü tapın: {names}", a=best, d=[f for f in fr_list if f != best],
                e=f"1 − kəsr fərqlərini və ya çarpaz hasilləri müqayisə edin. Ən böyüyü {show(best)}.",
                chk=chk_best, open=False, diff=M)


def frac_mixed_dec(r, g):
    """((m1 − d1) : d2 + f1 · d3) — adi və onluq kəsrlər qarışıq"""
    while True:
        w = r.randint(1, 4)
        m1 = w + F(r.choice([1, 3, 5, 7]), 8)
        d1 = F(r.choice([25, 75, 125, 375, 625]), 1000) * r.choice([1, 10])
        d2 = F(r.choice([5, 15, 25, 35, 45, 55, 75]), 100)
        f1 = F(r.randint(1, 8), r.choice([3, 5, 7, 9]))
        d3 = F(r.choice([12, 15, 18, 21, 24, 27, 35, 45]), 10)
        if m1 - d1 <= 0 or f1.denominator == 1:
            continue
        ans = (m1 - d1) / d2 + f1 * d3
        if ans.denominator <= 20 and ans < 60:
            break
    chk = (float(m1) - float(d1)) / float(d2) + float(f1) * float(d3)
    ms = f"{w} {(m1 - w).numerator}/{(m1 - w).denominator}"
    return dict(t=f"Hesablayın: ({ms} − {dec(d1)}) : {dec(d2)} + {show(f1)} · {dec(d3)}", a=ans,
                d=[((m1 - d1) / d2 + f1) * d3, (m1 - d1) * d2 + f1 * d3, (m1 - d1) / (d2 + f1 * d3), (m1 + d1) / d2 + f1 * d3,
                   (w + F(1, 8) - d1) / d2 + f1 * d3, ans + 1],
                e=f"{ms} − {dec(d1)} = {show(m1 - d1)}; {show(m1 - d1)} : {dec(d2)} = {show((m1 - d1) / d2)}; "
                  f"{show(f1)} · {dec(d3)} = {show(f1 * d3)}. Cəm: {show(ans)}. (Əvvəl vurma/bölmə, sonra toplama.)",
                chk=chk, diff=M)


def frac_pipes(r, g):
    while True:
        a, b, c = r.randint(3, 15), r.randint(3, 15), r.randint(4, 30)
        rate = F(1, a) + F(1, b) - F(1, c)
        if a != b and rate > 0 and c > min(a, b):
            ans = 1 / rate
            if ans.denominator <= 12:
                break
    L = math.lcm(a, b, c)
    chk = F(L, L // a + L // b - L // c)
    return dict(t=f"Hovuzu birinci boru {a} saata, ikinci boru {b} saata doldurur, üçüncü boru isə dolu hovuzu {c} saata boşaldır. "
                  f"Boş hovuzda üç boru birlikdə açılarsa, hovuz neçə saata dolar?", a=ans,
                d=[1 / (F(1, a) + F(1, b) + F(1, c)), 1 / (F(1, a) + F(1, b)), F(a + b - c) if a + b - c > 0 else ans + 2,
                   F(a * b * c, a * b + b * c + a * c), ans + 1],
                e=f"Saatlıq məhsuldarlıq: 1/{a} + 1/{b} − 1/{c} = {show(rate)}. Vaxt: 1 : {show(rate)} = {show(ans)} saat.",
                chk=chk, diff=H)


# ======================= num-pow =======================

def pow_simplify(r, g):
    while True:
        a, b, c, d_ = r.randint(3, 12), r.randint(2, 9), r.randint(2, 12), r.randint(1, 7)
        # (2^a · 6^b) / (3^c · 4^d)
        e2 = a + b - 2 * d_
        e3 = b - c
        if abs(e2) <= 5 and abs(e3) <= 3 and (e2, e3) != (0, 0):
            break
    ans = F(2) ** e2 * F(3) ** e3
    chk = F(2 ** a * 6 ** b, 3 ** c * 4 ** d_)
    return dict(t=f"Hesablayın: (2^{a} · 6^{b}) / (3^{c} · 4^{d_})", a=ans,
                d=[ans * 2, ans / 2, ans * 3, ans / 3, ans * 4],
                e=f"6^{b} = 2^{b}·3^{b}, 4^{d_} = 2^{2 * d_}. 2-nin üstü: {a} + {b} − {2 * d_} = {neg(str(e2))}; 3-ün üstü: {b} − {c} = {neg(str(e3))}. "
                  f"Nəticə: {show(ans)}.", chk=chk, diff=M)


def pow_expeq(r, g):
    base = 2 if g != 10 else r.choice([2, 3])
    while True:
        x = r.randint(-2, 7)
        k1, s1 = r.randint(1, 5), r.randint(1, 3)
        k2, s2 = r.randint(1, 5), r.randint(1, 3)
        coef = k1 * F(base) ** s1 + k2 * F(base) ** (-s2)
        N = coef * F(base) ** x
        if N.denominator == 1 and 0 < N < 5000:
            break
    t = f"{k1 if k1 > 1 else ''}{'·' if k1 > 1 else ''}{base}^(x+{s1}) + {k2 if k2 > 1 else ''}{'·' if k2 > 1 else ''}{base}^(x−{s2}) = {N}"
    # müstəqil yoxlama: tam x-ləri yoxla
    sols = [z for z in range(-10, 20) if k1 * F(base) ** (z + s1) + k2 * F(base) ** (z - s2) == N]
    return dict(t=f"Tənliyi həll edin: {t}", a=x, d=[x + 1, x - 1, x + s1, x - s2, x + 2],
                e=f"{base}^x mötərizə xaricinə: {base}^x·({k1}·{base}^{s1} + {k2}/{base}^{s2}) = {N}, "
                  f"{base}^x·{show(coef)} = {N}, {base}^x = {show(F(base) ** x)}, x = {x}.",
                chk=sols[0] if len(sols) == 1 else 999, diff=H)


def pow_lastdigit(r, g):
    a, b = r.choice([2, 3, 7, 8, 12, 13, 17, 18, 22, 23, 27, 28]), r.choice([2, 3, 4, 7, 8, 9, 13, 14, 19])
    n, m = r.randint(20, 2025), r.randint(20, 2025)
    op = r.choice(["+", "−"]) if g != 9 else "+"
    da, db = pow(a, n, 10), pow(b, m, 10)
    ans = (da + db) % 10 if op == "+" else (da - db) % 10
    chk = (a ** n + b ** m) % 10 if op == "+" else (a ** n - b ** m) % 10
    return dict(t=f"{a}^{n} {op} {b}^{m} ədədinin son rəqəmini tapın.", a=ans,
                d=[(ans + 1) % 10, (ans + 9) % 10, (ans + 2) % 10, (ans + 8) % 10, (da * db) % 10],
                e=f"{a % 10}-un qüvvətlərinin son rəqəmləri 4 addımdan bir təkrarlanır: {a}^{n} → {da}; {b}^{m} → {db}. "
                  f"Son rəqəm: {ans}.", chk=chk, open=False, diff=M)


def pow_digits(r, g):
    a, b = r.randint(10, 60), r.randint(10, 60)
    c = r.randint(1, 6)
    n = 2 ** a * 5 ** b * 3 ** c
    k = min(a, b)
    rest = 2 ** (a - k) * 5 ** (b - k) * 3 ** c
    ans = k + len(str(rest))
    return dict(t=f"2^{a} · 5^{b} · 3^{c} ədədi neçə rəqəmlidir?", a=ans, d=[ans + 1, ans - 1, ans + 2, k, ans - 2],
                e=f"2^{k}·5^{k} = 10^{k}. Qalan vuruq: {rest} ({len(str(rest))} rəqəmli). Cəmi {k} + {len(str(rest))} = {ans} rəqəm.",
                chk=len(str(n)), diff=H)


def pow_quadexp(r, g):
    base = 3 if g == 10 else r.choice([2, 3])
    while True:
        e1, e2 = r.sample(range(-1, 5), 2)
        t1, t2 = F(base) ** e1, F(base) ** e2
        p, q = t1 + t2, t1 * t2
        if p.denominator == 1 and q.denominator == 1:
            break
    ask = r.choice(["cəmini", "hasilini"]) if g == 11 else "cəmini"
    ans = e1 + e2 if ask == "cəmini" else e1 * e2
    # müstəqil: tam x üzrə yoxla
    roots = [x for x in range(-6, 10) if F(base) ** (2 * x) - p * F(base) ** x + q == 0]
    chk = sum(roots) if ask == "cəmini" else roots[0] * roots[1]
    sq_ = base * base
    t = f"{sq_}^x − {p}·{base}^x + {q} = 0"
    return dict(t=f"{t} tənliyinin köklərinin {ask} tapın.", a=ans,
                d=[p, q, ans + 1, ans - 1, e1 * e2 + 1 if ask == "cəmini" else e1 + e2],
                e=f"t = {base}^x > 0: t² − {p}t + {q} = 0, t₁ = {show(t1)}, t₂ = {show(t2)}. "
                  f"x₁ = {e1}, x₂ = {e2}; {'cəm' if ask == 'cəmini' else 'hasil'}: {ans}.",
                chk=chk if len(roots) == 2 else 999, diff=H)


def pow_fractional(r, g):
    pairs = [(8, 3), (27, 3), (16, 4), (81, 4), (32, 5), (64, 6), (125, 3), (4, 2), (9, 2), (25, 2), (49, 2), (64, 3), (216, 3)]
    (A, n1), (B, n2), (C, n3) = r.sample(pairs, 3)
    k1, k2, k3 = r.randint(1, 3), r.randint(1, 3), r.randint(1, 2)
    root = lambda X, n: round(X ** (1 / n))
    v1 = F(root(A, n1)) ** k1
    v2 = F(root(B, n2)) ** (-k2)
    v3 = F(root(C, n3)) ** k3
    ans = v1 + v2 * v3
    chk = A ** (k1 / n1) + B ** (-k2 / n2) * C ** (k3 / n3)
    return dict(t=f"Hesablayın: {A}^({k1}/{n1}) + {B}^(−{k2}/{n2}) · {C}^({k3}/{n3})", a=ans,
                d=[v1 + F(root(B, n2)) ** k2 * v3, (v1 + v2) * v3, v1 - v2 * v3, v1 + v2 / v3, ans + 1],
                e=f"{A}^({k1}/{n1}) = {show(v1)}, {B}^(−{k2}/{n2}) = {show(v2)}, {C}^({k3}/{n3}) = {show(v3)}. "
                  f"Nəticə: {show(v1)} + {show(v2)}·{show(v3)} = {show(ans)}.", chk=chk, diff=M)


def pow_order(r, g):
    while True:
        p, q, s = r.randint(20, 90), r.randint(15, 60), r.randint(10, 40)
        vals = [p * math.log(2), q * math.log(3), s * math.log(5)]
        sv = sorted(vals)
        if sv[1] - sv[0] > 0.01 and sv[2] - sv[1] > 0.01 and max(vals) - min(vals) < 8:
            break
    exact = [2 ** p, 3 ** q, 5 ** s]
    nm = ["a", "b", "c"]
    a, d, ok = order_q(r, nm, vals, exact)
    return dict(t=f"a = 2^{p}, b = 3^{q}, c = 5^{s}. Ədədləri artan sırada düzün.", a=a, d=d, chk=ok and 1, open=False,
                e=f"Ortaq üstə gətirin və ya loqarifmləri müqayisə edin: {p}·lg2 ≈ {ap(vals[0] / math.log(10))}, "
                  f"{q}·lg3 ≈ {ap(vals[1] / math.log(10))}, {s}·lg5 ≈ {ap(vals[2] / math.log(10))}. Ardıcıllıq: {a.s}.",
                diff=H)


def pow_sym(r, g):
    s = r.randint(3, 9)
    k = s * s - 2
    ask = r.choice([3, 2])
    # 2^x + 2^-x = s ; 4^x + 4^-x = k (verilir); 8^x + 8^-x = s^3 - 3s ; 16^x+16^-x = k^2-2
    if ask == 3:
        ans = s ** 3 - 3 * s
        t = f"4^x + 4^(−x) = {k} və x > 0 olarsa, 8^x + 8^(−x) ifadəsinin qiymətini tapın."
        e = (f"(2^x + 2^(−x))² = 4^x + 4^(−x) + 2 = {k + 2}, deməli 2^x + 2^(−x) = {s}. "
             f"8^x + 8^(−x) = (2^x + 2^(−x))³ − 3(2^x + 2^(−x)) = {s ** 3} − {3 * s} = {ans}.")
        d = [s ** 3, k * s, ans + 3 * s, s ** 3 + 3 * s]
    else:
        ans = k * k - 2
        t = f"4^x + 4^(−x) = {k} olarsa, 16^x + 16^(−x) ifadəsinin qiymətini tapın."
        e = f"16^x + 16^(−x) = (4^x + 4^(−x))² − 2 = {k}² − 2 = {ans}."
        d = [k * k, k * k + 2, 2 * k, k * k - 4]
    y = (s + math.sqrt(s * s - 4)) / 2  # 2^x
    chk = y ** 3 + y ** -3 if ask == 3 else y ** 4 + y ** -4
    return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=H)


# ======================= num-abs =======================

def _halves(lo, hi):
    return [F(k, 2) for k in range(2 * lo, 2 * hi + 1)]


def abs_two(r, g):
    while True:
        a, b = r.randint(-9, 9), r.randint(-9, 9)
        c = r.randint(1, 20)
        if c > abs(a - b) and a != b and (a + b + c) % 2 == 0:
            break
    x1, x2 = F(a + b - c, 2), F(a + b + c, 2)
    ask = "hasilini" if g == 9 else "kvadratlarının cəmini"
    ans = x1 * x2 if g == 9 else x1 * x1 + x2 * x2
    roots = [x for x in _halves(-40, 40) if abs(x - a) + abs(x - b) == c]
    chk = (roots[0] * roots[1] if g == 9 else roots[0] ** 2 + roots[1] ** 2) if len(roots) == 2 else 999
    ta = f"|x {'−' if a > 0 else '+'} {abs(a)}|" if a else "|x|"
    tb = f"|x {'−' if b > 0 else '+'} {abs(b)}|" if b else "|x|"
    return dict(t=f"{ta} + {tb} = {c} tənliyinin köklərinin {ask} tapın.", a=ans,
                d=[x1 + x2, ans + c, -ans, ans + 1, ans - 1] if g == 9 else [(x1 + x2) ** 2, x1 * x2, ans + 2 * c, ans - 1, ans + 1],
                e=f"Kökləri x ≤ min və x ≥ max hissələrində axtarın: x₁ = {show(x1)}, x₂ = {show(x2)} "
                  f"(aralıqda ifadə sabitdir və {abs(a - b)} ≠ {c}). Cavab: {show(ans)}.",
                chk=chk, diff=H)


def abs_count(r, g):
    if g == 9:
        k = r.randint(2, 5)
        a, b = r.randint(-15, 15), r.randint(3, 25)
        lo, hi = F(a - b, k), F(a + b, k)
        sols = [x for x in range(-60, 60) if abs(k * x - a) <= b]
        ans = math.floor(hi) - math.ceil(lo) + 1
        t = f"|{k}x {'−' if a >= 0 else '+'} {abs(a)}| ≤ {b} bərabərsizliyini ödəyən tam ədədlərin sayını tapın."
        e = f"−{b} ≤ {xm(a, f'{k}x')} ≤ {b} ⇒ {show(lo)} ≤ x ≤ {show(hi)}. Tam ədədlər: {neg(str(math.ceil(lo)))}, …, {neg(str(math.floor(hi)))} — {ans} ədəd."
    else:
        a, b = r.randint(-8, 3), r.randint(-3, 8)
        while b <= a:
            b = r.randint(-3, 8)
        c = r.randint(b - a + 2, b - a + 16)
        sols = [x for x in range(-60, 60) if abs(x - a) + abs(x - b) < c]
        lo, hi = F(a + b - c, 2), F(a + b + c, 2)
        ans = len([x for x in range(math.floor(lo), math.ceil(hi) + 1) if lo < x < hi])
        t = f"|x {'−' if a > 0 else '+'} {abs(a)}| + |x {'−' if b > 0 else '+'} {abs(b)}| < {c} bərabərsizliyini ödəyən tam ədədlərin sayını tapın."
        e = f"Sərhədlər: |{xm(a)}| + |{xm(b)}| = {c} ⇒ x = {show(lo)} və x = {show(hi)}. Həllər: {show(lo)} < x < {show(hi)}, tam ədədlər — {ans}."
    return dict(t=t.replace("−  ", "− ").replace("+ 0|", "|").replace("− 0|", "|"), a=ans, d=[ans + 1, ans - 1, ans + 2, ans - 2],
                e=e, chk=len(sols), diff=M)


def abs_minsum(r, g):
    n = 3 if g == 10 else 4
    pts = sorted(r.sample(range(-12, 15), n))
    ans = sum(abs(pts[-1 - i] - pts[i]) for i in range(n // 2))
    chk = min(sum(abs(F(x) - p) for p in pts) for x in _halves(-30, 30))
    terms = " + ".join(f"|x {'−' if p > 0 else '+'} {abs(p)}|" if p else "|x|" for p in pts)
    return dict(t=f"f(x) = {terms} funksiyasının ən kiçik qiymətini tapın.", a=ans,
                d=[ans + 1, ans - 1, pts[-1] - pts[0], sum(abs(p) for p in pts), ans + 2],
                e=f"Modulların cəminin minimumu medianda (orta nöqtələr arasında) alınır: "
                  + " + ".join(f"({show(pts[-1 - i])} − {par(pts[i])})" for i in range(n // 2)) + f" = {ans}.",
                chk=chk, diff=H)


def abs_sqrt(r, g):
    while True:
        m = r.choice([x for x in range(5, 90) if not is_sq(x)])
        s = math.sqrt(m)
        b, c = r.randint(0, 12), r.randint(0, 12)
        if b != c and abs(b - s) > 0.3 and abs(c - s) > 0.3:
            break
    # |b − √m| + |c − √m|
    v = abs(b - s) + abs(c - s)
    if (b - s) * (c - s) < 0:
        a = F(abs(b - c))
        how = f"√{m} ədədi {min(b, c)} ilə {max(b, c)} arasındadır, modullar açılır: {max(b, c)} − {min(b, c)} = {abs(b - c)}."
    elif b > s:
        a = lin_surd(b + c, -2, m)
        how = f"{b} > √{m} və {c} > √{m}: ({b} − √{m}) + ({c} − √{m}) = {a.s}."
    else:
        a = lin_surd(-b - c, 2, m)
        how = f"{b} < √{m} və {c} < √{m}: (√{m} − {b}) + (√{m} − {c}) = {a.s}."
    d = [F(abs(b - c)), lin_surd(b + c, -2, m), lin_surd(-b - c, 2, m), F(b + c), lin_surd(0, 2, m), lin_surd(b + c, 2, m), lin_surd(-b - c, 1, m), lin_surd(b + c, -1, m), lin_surd(abs(b - c), 2, m)]
    return dict(t=f"Hesablayın: √(({b} − √{m})²) + √(({c} − √{m})²)", a=a, d=d,
                e=f"√(t²) = |t|. √{m} ≈ {ap(s)}. {how}", chk=v, diff=M)


def abs_nested(r, g):
    a, b = r.randint(-6, 6), r.randint(2, 9)
    c = r.randint(1, 8)
    xs = [x for x in range(-60, 60) if abs(abs(x - a) - b) <= c]
    ans = 0
    lo_t = max(0, b - c)
    for t_ in range(lo_t, b + c + 1):
        ans += a if t_ == 0 else 2 * a
    return dict(t=f"||x {'−' if a > 0 else '+'} {abs(a)}| − {b}| ≤ {c} bərabərsizliyinin tam həllərinin cəmini tapın.".replace("|x + 0|", "|x|").replace("|x − 0|", "|x|"),
                a=ans, d=[ans + a if a else ans + 1, ans - a if a else ans - 1, len(xs), ans + b, ans - b],
                e=f"t = |{xm(a)}| ≥ 0: |t − {b}| ≤ {c} ⇒ {lo_t} ≤ t ≤ {b + c}. Hər t > 0 üçün iki həll x = {show(a)} ± t (cəmi {show(2 * a)})"
                  + (", t = 0 üçün bir həll x = " + show(a) if lo_t == 0 else "") + f". Cəm: {show(ans)}.", chk=sum(xs), diff=H)


def abs_quad_roots(r, g):
    while True:
        a, b = r.randint(1, 7), r.randint(1, 40)
        if a * a != b:
            break
    # |x² − 2ax| = b
    n = 2 + (2 if a * a > b else 0)
    xs = [-60.000317 + i * 0.001 for i in range(120001)]
    f = lambda x: abs(x * x - 2 * a * x) - b
    cnt = sum(1 for i in range(len(xs) - 1) if f(xs[i]) * f(xs[i + 1]) < 0 or f(xs[i]) == 0)
    ask_sum = r.random() < 0.5
    if ask_sum:
        ans = 2 * a + (2 * a if a * a > b else 0)
        t = f"|x² − {2 * a}x| = {b} tənliyinin bütün həqiqi köklərinin cəmini tapın."
        roots = []
        for i in range(len(xs) - 1):
            if f(xs[i]) * f(xs[i + 1]) < 0:
                lo, hi = xs[i], xs[i + 1]
                for _ in range(60):
                    mid = (lo + hi) / 2
                    if f(lo) * f(mid) <= 0:
                        hi = mid
                    else:
                        lo = mid
                roots.append((lo + hi) / 2)
        chk = sum(roots)
        d = [4 * a, 2 * a, 0, 6 * a, 8 * a] if a * a > b else [4 * a, 0, 6 * a, -2 * a, a]
    else:
        ans, chk = n, cnt
        t = f"|x² − {2 * a}x| = {b} tənliyinin neçə həqiqi kökü var?"
        d = [0, 1, 2, 3, 4]
    return dict(t=t, a=ans, d=d,
                e=f"x² − {2 * a}x = {b} — diskriminant müsbətdir, 2 kök (cəmi {2 * a}). x² − {2 * a}x = −{b}: D/4 = {a * a} − {b} "
                  + ("> 0, daha 2 kök (cəmi " + str(2 * a) + ")." if a * a > b else "< 0, kök yoxdur."),
                chk=chk, open=False, diff=H)


def abs_linear(r, g):
    while True:
        a = r.randint(-8, 8)
        k = r.choice([F(1, 2), F(1, 3), F(2, 3), 2, 3, F(3, 2)]) * r.choice([1, -1])
        c = r.randint(-6, 6)
        k = F(k)
        sols = []
        # x ≥ a: x − a = kx + c ⇒ x(1−k) = a + c
        if k != 1:
            x = (a + c) / (1 - k)
            if x >= a:
                sols.append(x)
        if k != -1:
            x = (a - c) / (1 + k)
            if x < a:
                sols.append(x)
        if len(sols) >= 1 and all(s.denominator <= 6 for s in sols):
            break
    ans = sum(sols)
    # müstəqil: 1/6 addımla bütün rasional namizədlər
    cand = [F(i, 60) for i in range(-6000, 6001)]
    chk = sum(x for x in cand if abs(x - a) == k * x + c)
    ks = show(k) if k.denominator == 1 else (f"({show(k)})" if k > 0 else f"−({show(-k)})")
    return dict(t=f"|x {'−' if a > 0 else '+'} {abs(a)}| = {ks}x {'−' if c < 0 else '+'} {abs(c)} tənliyinin köklərinin cəmini tapın.".replace("|x + 0|", "|x|").replace("|x − 0|", "|x|").replace("x + 0 ", "x ").replace("1x", "x"),
                a=ans, d=[(a + c) / (1 - k) + (a - c) / (1 + k) if k not in (1, -1) else ans + 1, ans + 1, -ans, ans - 1, ans + 2],
                e=f"x ≥ {show(a)}: {xm(a)} = {ks}x{' + ' + show(c) if c > 0 else (' − ' + show(-c) if c < 0 else '')}; x < {show(a)}: {'−x' if a == 0 else '−(' + xm(a) + ')'} = {ks}x{' + ' + show(c) if c > 0 else (' − ' + show(-c) if c < 0 else '')}. "
                  f"Şərti ödəyən köklər: {', '.join(show(s) for s in sols)}. Cəm: {show(ans)}.",
                chk=chk, diff=H)


# ======================= num-pct =======================

def pct_chain(r, g):
    while True:
        p, q, s = r.choice([10, 20, 25, 30, 40, 50]), r.choice([10, 20, 25, 30, 40, 50]), r.choice([5, 10, 15, 20, 25])
        net = (1 + F(p, 100)) * (1 - F(q, 100)) * (1 + F(s, 100)) - 1
        if net != 0 and terminating(net * 100) and abs(net * 100) < 60:
            break
    ans = net * 100
    sim = F(1000)
    sim = sim + sim * p / 100
    sim = sim - sim * q / 100
    sim = sim + sim * s / 100
    chk = (sim - 1000) / 10
    word = "artdı" if ans > 0 else "azaldı"
    return dict(t=f"Məhsulun qiyməti əvvəlcə {p}% artırıldı, sonra {q}% endirildi, daha sonra {s}% artırıldı. "
                  f"Son qiymət ilkin qiymətlə müqayisədə neçə faiz dəyişdi? (artım müsbət, azalma mənfi)",
                a=pc(ans), d=[pc(p - q + s), pc(ans + 1), pc(ans - 1), pc(-ans), pc(ans + F(1, 2))],
                e=f"Əmsallar: {dec(1 + F(p, 100))} · {dec(1 - F(q, 100))} · {dec(1 + F(s, 100))} = {dec(1 + net)}. "
                  f"Qiymət {dec(abs(ans))}% {word}.", chk=chk, diff=M)


def pct_reverse(r, g):
    while True:
        p, q = r.choice([10, 15, 20, 25, 30, 40, 50, 60]), r.choice([10, 20, 25, 30, 40, 50])
        k = (1 + F(p, 100)) * (1 - F(q, 100))
        N = r.randint(20, 400) * 10
        X = N * k
        if X.denominator == 1 and k != 1:
            break
    chk = F(N)
    chk = chk * (100 + p) / 100 * (100 - q) / 100
    return dict(t=f"Malın qiyməti {p}% artırıldıqdan sonra {q}% endirildi və {X} manat oldu. Malın ilkin qiyməti neçə manat idi?",
                a=N, d=[round(X * (1 - F(p, 100)) * (1 + F(q, 100))), round(X / (1 + F(p - q, 100))) if p != q else X, N + 10, N - 10, X, N + 50, N - 50],
                e=f"x·{dec(1 + F(p, 100))}·{dec(1 - F(q, 100))} = {X} ⇒ x·{dec(k)} = {X} ⇒ x = {N}.",
                chk=N if chk == X else -1, diff=M)


def pct_mixture(r, g):
    while True:
        m1, m2, w = r.randint(2, 12), r.randint(2, 12), r.randint(1, 8)
        a, b = r.choice([5, 10, 15, 20, 25, 30, 40]), r.choice([10, 20, 30, 35, 45, 50, 60])
        ans = F(m1 * a + m2 * b, m1 + m2 + w)
        if terminating(ans) and a != b:
            break
    salt_g = m1 * 1000 * a // 100 + m2 * 1000 * b // 100
    chk = F(salt_g, (m1 + m2 + w) * 1000) * 100
    return dict(t=f"{m1} kq {a}%-li və {m2} kq {b}%-li duz məhlulu qarışdırıldı, sonra qarışığa {w} kq su əlavə edildi. "
                  f"Alınan məhlulda duzun faizi nə qədərdir?", a=pc(ans),
                d=[pc(F(m1 * a + m2 * b, m1 + m2)), pc(F(a + b, 2)), pc(F(m1 * a + m2 * b, m1 + m2 + w + 1)), pc(ans + 1), pc(ans - 1)],
                e=f"Duz: {m1}·{dec(F(a, 100))} + {m2}·{dec(F(b, 100))} = {dec(F(m1 * a + m2 * b, 100))} kq. "
                  f"Kütlə: {m1} + {m2} + {w} = {m1 + m2 + w} kq. Faiz: {dec(ans)}%.", chk=chk, diff=M)


def pct_evap(r, g):
    while True:
        m = r.randint(2, 30) * 5
        a, b = r.choice([5, 10, 12, 15, 20, 24, 25]), r.choice([20, 25, 30, 40, 50, 60])
        if b > a:
            salt = F(m * a, 100)
            new_m = salt * 100 / b
            x = m - new_m
            if x.denominator == 1 and x > 0:
                break
    chk = F(m) - F(m * a, b)
    return dict(t=f"{m} kq {a}%-li məhluldan neçə kq su buxarlandırılmalıdır ki, məhlul {b}%-li olsun?", a=x,
                d=[F(m * (b - a), 100), new_m, x + 5, x - 5, x + 10, x - 10],
                e=f"Duz dəyişmir: {m}·{dec(F(a, 100))} = {dec(salt)} kq. Yeni kütlə: {dec(salt)} : {dec(F(b, 100))} = {dec(new_m)} kq. "
                  f"Buxarlanan su: {m} − {dec(new_m)} = {dec(x)} kq.", chk=chk, diff=H)


def pct_revenue(r, g):
    while True:
        p, q = r.choice([10, 20, 25, 50, 60]), r.choice([10, 20, 25, 40, 50])
        rev = (1 + F(p, 100)) * (1 - F(q, 100))
        need = 1 / rev - 1
        if rev < 1 and terminating(need * 100):
            break
    ans = need * 100
    # müstəqil: 100 ədəd × 100 manat
    R0 = 100 * 100
    R1 = (100 + p) * (100 - q)
    chk = (F(R0, R1) - 1) * 100
    return dict(t=f"Məhsulun qiyməti {p}% artırıldı, satış həcmi isə {q}% azaldı. Gəlirin ilkin səviyyəyə qayıtması üçün "
                  f"satış həcmi indikindən neçə faiz artmalıdır?", a=pc(ans),
                d=[pc(q - p if q > p else q), pc((1 - rev) * 100), pc(q), pc(ans + 5), pc(ans - 5), pc(ans + 10), pc(p), pc(ans + F(5, 2))],
                e=f"Gəlir əmsalı: {dec(1 + F(p, 100))}·{dec(1 - F(q, 100))} = {dec(rev)}. Həcm 1 : {dec(rev)} = {show(1 / rev)} dəfə artmalıdır, "
                  f"yəni {dec(ans)}%.", chk=chk, diff=H)


def pct_deposit(r, g):
    while True:
        rate = r.choice([5, 10, 20, 25, 50])
        N = r.randint(2, 80) * 100
        W = r.randint(1, 30) * 100
        after = (N * (1 + F(rate, 100)) - W) * (1 + F(rate, 100))
        if after.denominator == 1 and after > N:
            break
    chk = F(N)
    chk = chk * (100 + rate) / 100
    chk -= W
    chk = chk * (100 + rate) / 100
    return dict(t=f"Bankda illik {rate}% mürəkkəb faizlə əmanət qoyuldu. Birinci ilin sonunda faiz hesablandıqdan sonra "
                  f"əmanətdən {W} manat götürüldü. İkinci ilin sonunda hesabda {after} manat oldu. İlkin əmanət neçə manat idi?",
                a=N, d=[round(after / (1 + F(rate, 100)) ** 2 + W), round(after / (1 + F(rate, 100)) ** 2), N + 100, N - 100,
                        round((after / (1 + F(rate, 100)) - W) / (1 + F(rate, 100))), N + 200, N - 200],
                e=f"Tərsinə: {after} : {dec(1 + F(rate, 100))} = {show(after / (1 + F(rate, 100)))}; + {W} = {show(after / (1 + F(rate, 100)) + W)}; "
                  f": {dec(1 + F(rate, 100))} = {N}.", chk=N if chk == after else -1, diff=H)


def pct_relative(r, g):
    while True:
        p, q = r.choice([10, 20, 25, 30, 40, 50, 60]), r.choice([10, 20, 25, 30, 40, 50])
        ratio = (1 + F(p, 100)) * (1 - F(q, 100))
        ch = (ratio - 1) * 100
        if ch != 0 and terminating(ch):
            break
    C = F(1000)
    B = C * (100 - q) / 100
    A = B * (100 + p) / 100
    chk = (A / C - 1) * 100
    word = "çoxdur" if ch > 0 else "azdır"
    return dict(t=f"A ədədi B-dən {p}% çox, B ədədi isə C-dən {q}% azdır. A ədədi C-dən neçə faiz {word}?",
                a=pc(abs(ch)), d=[pc(abs(p - q)), pc(abs(ch) + 2), pc(abs(ch) + 5), pc(F(p * q, 100)), pc(abs(ch) - 1)],
                e=f"A = {dec(1 + F(p, 100))}·B = {dec(1 + F(p, 100))}·{dec(1 - F(q, 100))}·C = {dec(ratio)}·C. "
                  f"Fərq: {dec(abs(ch))}%.", chk=abs(chk), diff=H)


def pct_profit(r, g):
    while True:
        p, q = r.choice([20, 25, 30, 40, 50, 60, 80]), r.choice([10, 15, 20, 25, 30])
        pr = ((1 + F(p, 100)) * (1 - F(q, 100)) - 1) * 100
        if pr > 0 and terminating(pr):
            break
    cost = F(100)
    price = cost * (100 + p) / 100
    sale = price * (100 - q) / 100
    chk = (sale - cost) / cost * 100
    return dict(t=f"Satıcı malın qiymətini maya dəyərindən {p}% yuxarı qoydu, sonra bu qiymətə {q}% endirim etdi. "
                  f"Satıcı maya dəyərinə nəzərən neçə faiz qazanc əldə etdi?", a=pc(pr),
                d=[pc(p - q), pc(pr + 2), pc(pr - 2), pc(pr + 5), pc(F(p * (100 - q), 100))],
                e=f"Satış qiyməti: {dec(1 + F(p, 100))}·{dec(1 - F(q, 100))} = {dec(1 + pr / 100)} maya dəyəri. Qazanc: {dec(pr)}%.",
                chk=chk, diff=M)


def pct_twice(r, g):
    while True:
        x = r.choice([5, 10, 15, 20, 25, 30, 40, 50, 60])
        m = r.randint(2, 60) * 100
        n = m * (1 + F(x, 100)) ** 2
        extra = r.choice([0, 1])
        if n.denominator == 1:
            break
    if extra:
        y = r.choice([10, 20, 25])
        fin = n * (1 - F(y, 100))
        if fin.denominator != 1:
            return pct_twice(r, g)
        t = (f"İşçinin maaşı iki dəfə eyni faizlə artırıldı, sonra {y}% azaldıldı. Nəticədə maaş {m} manatdan {fin} manata çatdı. "
             f"Maaş hər dəfə neçə faiz artırılmışdı?")
        e = f"{m}·(1 + x)²·{dec(1 - F(y, 100))} = {fin} ⇒ (1 + x)² = {show(n / m)} ⇒ 1 + x = {dec(1 + F(x, 100))}, x = {x}%."
        chk = (math.sqrt(float(fin) / (m * (1 - y / 100))) - 1) * 100
        d = [pc(F(fin - m, m) * 50), pc(x + 5), pc(x - 5), pc(2 * x), pc(F((fin - m) * 100, m))]
    else:
        t = f"İşçinin maaşı iki dəfə eyni faizlə artırıldı və {m} manatdan {n} manata çatdı. Maaş hər dəfə neçə faiz artırılmışdı?"
        e = f"{m}·(1 + x)² = {n} ⇒ (1 + x)² = {show(n / m)} ⇒ 1 + x = {dec(1 + F(x, 100))}, x = {x}%."
        chk = (math.sqrt(float(n) / m) - 1) * 100
        d = [pc(F((n - m) * 50, m)), pc(x + 5), pc(x - 5), pc(2 * x), pc(F((n - m) * 100, m))]
    return dict(t=t, a=pc(x), d=d, e=e, chk=chk, diff=H)


TOPICS = {
    "num-real": {9: [real_denest, real_count, real_repdec, real_order_k, real_conj],
                 10: [real_telescope, real_nested_abs, real_order_k, real_pell, real_conj, real_count],
                 11: [real_telescope, real_recip_sq, real_intpart, real_pell, real_order_diff, real_denest]},
    "num-frac": {9: [frac_telescope, frac_continued, frac_remainder, frac_largest, frac_mixed_dec],
                 10: [frac_telescope, frac_ratio_expr, frac_mixed_dec, frac_remainder, frac_pipes],
                 11: [frac_telescope, frac_ratio_expr, frac_pipes, frac_remainder, frac_continued]},
    "num-pow": {9: [pow_simplify, pow_expeq, pow_lastdigit, pow_fractional],
                10: [pow_digits, pow_quadexp, pow_expeq, pow_fractional, pow_lastdigit, pow_simplify],
                11: [pow_quadexp, pow_order, pow_sym, pow_digits, pow_expeq]},
    "num-abs": {9: [abs_two, abs_count, abs_sqrt, abs_linear],
                10: [abs_count, abs_minsum, abs_sqrt, abs_linear, abs_two],
                11: [abs_nested, abs_quad_roots, abs_minsum, abs_linear, abs_two]},
    "num-pct": {9: [pct_chain, pct_reverse, pct_mixture, pct_profit],
                10: [pct_reverse, pct_evap, pct_relative, pct_mixture, pct_chain, pct_profit],
                11: [pct_revenue, pct_deposit, pct_relative, pct_evap, pct_chain, pct_twice]},
}
