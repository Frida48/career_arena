"""Riyaziyyat · Cəbr: alg-eq, alg-sys, alg-quad, alg-prog (Ardıcıllıqlar), alg-func."""
import math
from fractions import Fraction as F

import numpy as np

from mx import Num, M, H, show, neg, par, poly, sg, lead, is_sq, surd, lin_surd


def xm(a, v="x"):
    a = F(a)
    if a == 0:
        return v
    return f"{v} − {show(a)}" if a > 0 else f"{v} + {show(-a)}"


def real_roots(coefs, tol=1e-7):
    """Polinomun həqiqi kökləri (numpy) — müstəqil yoxlama üçün"""
    rs = np.roots([float(c) for c in coefs])
    out = sorted(float(z.real) for z in rs if abs(z.imag) < tol)
    return out


def distinct(xs, tol=1e-6):
    out = []
    for x in sorted(xs):
        if not out or abs(x - out[-1]) > tol:
            out.append(x)
    return out


# ======================= alg-eq =======================

def eq_rational(r, g):
    while True:
        a = r.randint(1, 7)
        r2 = r.randint(-9, 9)
        q = r.randint(1, 6)
        if r2 in (a, -a):
            continue
        p = -2 * a - r2 + q
        k = p * a + q * a - a * r2
        if k != 0 and p != 0:
            break
    # (x + p)/(x − a) − q/(x + a) = k/(x² − a²)
    t = f"({xm(-p)})/({xm(a)}) − {q}/({xm(-a)}) = {neg(str(k))}/(x² − {a * a})"
    cand = real_roots([1, p + a - q, p * a + q * a - k])
    good = [x for x in cand if abs(x * x - a * a) > 1e-6 and abs((x + p) / (x - a) - q / (x + a) - k / (x * x - a * a)) < 1e-7]
    ask = r.choice(["kökünü", "köklərinin cəmini"]) if g != 9 else "köklərinin cəmini"
    return dict(t=f"Tənliyi həll edin və {ask} tapın: {t}", a=r2,
                d=[a + r2, a, -r2, r2 + 1, -a, r2 - 1],
                e=f"Ortaq məxrəc x² − {a * a}: ({xm(-p)})({xm(-a)}) − {q}({xm(a)}) = {neg(str(k))} ⇒ {poly([1, p + a - q, p * a + q * a - k])} = 0, "
                  f"köklər {a} və {neg(str(r2))}. x = {a} məxrəci sıfra çevirir (yad kök). Cavab: {neg(str(r2))}.",
                chk=sum(good) if good else 999, diff=H)


def eq_sqrt(r, g):
    while True:
        b = r.randint(-5, 8)
        x0 = r.randint(b + 2, b + 9)
        a = (x0 - b) ** 2 - x0
        other = 2 * b + 1 - x0  # kvadrat tənliyin ikinci kökü: x² − (2b+1)x + b² − a = 0
        if a != 0 and other != x0 and -a <= other:  # yad kök kökaltı ifadəni ödəyir, amma sağ tərəf mənfidir
            break
    cand = real_roots([1, -(2 * b + 1), b * b - a])
    good = [x for x in cand if x + a >= -1e-9 and abs(math.sqrt(max(x + a, 0)) - (x - b)) < 1e-7]
    ask = r.choice(["kökünü", "köklərinin cəmini"])
    return dict(t=f"√({xm(-a)}) = {xm(b)} tənliyinin {ask} tapın.", a=x0,
                d=[other, x0 + other, x0 + 1, x0 - 1, -x0],
                e=f"Kvadrata yüksəldin: {xm(-a)} = ({xm(b)})² ⇒ {poly([1, -(2 * b + 1), b * b - a])} = 0, x = {x0} və x = {neg(str(other))}. "
                  f"Sağ tərəf mənfi olmamalıdır: x ≥ {neg(str(b))}. x = {neg(str(other))} yad kökdür. Cavab: {x0}.".replace("+ (−", "− (").replace("− −", "+ "),
                chk=sum(good), diff=H)


def eq_biquad(r, g):
    while True:
        t1, t2 = r.randint(-9, 16), r.randint(-9, 16)
        if t1 != t2 and t1 * t2 != 0 and (t1 > 0 or t2 > 0):
            break
    s, p = t1 + t2, t1 * t2
    ask = r.choice(["count", "prod"])
    rr = real_roots([1, 0, -s, 0, p])
    if ask == "count":
        ans = sum(2 for t in (t1, t2) if t > 0)
        chk = len(distinct(rr))
        t = f"{poly([1, 0, -s, 0, p])} = 0 tənliyinin neçə həqiqi kökü var?"
        d = [0, 1, 2, 3, 4]
    else:
        pos = [t for t in (t1, t2) if t > 0]
        ans = 1
        for t in pos:
            ans *= -t
        chk = float(np.prod(distinct(rr)))
        t = f"{poly([1, 0, -s, 0, p])} = 0 tənliyinin həqiqi köklərinin hasilini tapın."
        d = [p, -p, ans * -1, abs(ans) + 1, s]
    return dict(t=t.replace("x⁴ + −", "x⁴ − "), a=ans, d=d, open=ask != "count",
                e=f"t = x² ≥ 0: {poly([1, -s, p], 't')} = 0, t = {neg(str(t1))} və t = {neg(str(t2))}. "
                  f"Yalnız müsbət t həqiqi kök verir: x = ±√t. Cavab: {neg(str(ans))}.", chk=chk, diff=H)


def eq_work(r, g):
    while True:
        x = r.randint(3, 30)
        k = r.randint(1, 15)
        T = F(x * (x + k), 2 * x + k)
        if T.denominator <= 6:
            break
    sols = [y for y in range(1, 300) if F(1, y) + F(1, y + k) == 1 / T]
    Ts = show(T) if T.denominator == 1 else show(T)
    return dict(t=f"İki usta birlikdə işi {Ts} saata bitirir. Birinci usta təklikdə ikincidən {k} saat tez bitirir. "
                  f"İkinci usta işi təklikdə neçə saata bitirər?", a=x + k,
                d=[x, x + k + 1, 2 * T, x + 2 * k, x + k - 1],
                e=f"Birinci x saat, ikinci x + {k} saat. Birlikdə saatlıq iş: 1/x + 1/(x + {k}) = {show(1 / T)} ⇒ x = {x}. İkinci usta: {x + k} saat.",
                chk=sols[0] + k if len(sols) == 1 else 999, diff=M)


def eq_boat(r, g):
    while True:
        v = r.randint(1, 5)
        u = r.randint(v + 2, 30)
        S = r.randint(2, 20) * 6
        T = F(S, u + v) + F(S, u - v)
        if T.denominator <= 4:
            break
    sols = [w for w in range(v + 1, 200) if F(S, w + v) + F(S, w - v) == T]
    return dict(t=f"Qayıq çay axını ilə {S} km gedib geri qayıtdı və bütün yola {show(T)} saat sərf etdi. "
                  f"Çayın axın sürəti {v} km/saatdırsa, qayığın durğun sudakı sürəti neçə km/saatdır?",
                a=u, d=[u + v, u - v, u + 1, u - 1, F(2 * S, T)],
                e=f"{S}/(x + {v}) + {S}/(x − {v}) = {show(T)} ⇒ x = {u} km/saat (ikinci kök mənfidir və ya x ≤ {v}).",
                chk=sols[0] if len(sols) == 1 else 999, diff=H)


def eq_subst(r, g):
    while True:
        k = r.choice([-6, -4, -2, 2, 4, 6, -3, 3, 1, -1, 5, -5])
        t1, t2 = r.sample(range(-12, 25), 2)
        D1, D2 = k * k + 4 * t1, k * k + 4 * t2
        if D1 != 0 and D2 != 0 and (D1 > 0 or D2 > 0) and not (D1 > 0 and D2 > 0 and r.random() < 0.3):
            break
    s, p = t1 + t2, t1 * t2
    inner = f"x² {sg(k, 'x')[1:]}"
    n_real = sum(2 for D in (D1, D2) if D > 0)
    ans = -k * (n_real // 2)
    rr = distinct(real_roots(np.polymul([1, k, -t1], [1, k, -t2])))
    return dict(t=f"({inner})² {sg(-s, f'({inner})')[1:]} {sg(p)[1:]} = 0 tənliyinin həqiqi köklərinin cəmini tapın.",
                a=ans, d=[-2 * k, -k, 2 * k, k, s, 0, -3 * k],
                e=f"t = {inner}: t² {sg(-s, 't')[1:]} {sg(p)[1:]} = 0, t = {neg(str(t1))}; {neg(str(t2))}. "
                  f"x² {sg(k, 'x')[1:]} − t = 0 tənliyinin diskriminantı {k * k} + 4t: t = {neg(str(t1))} üçün {neg(str(D1))}, "
                  f"t = {neg(str(t2))} üçün {neg(str(D2))}. Həqiqi kökləri olan hər tənliyin köklərinin cəmi {neg(str(-k))}. Cavab: {neg(str(ans))}.",
                chk=sum(rr), diff=H)


def eq_log(r, g):
    base = r.choice([2, 3])
    while True:
        a, b = r.randint(-6, 6), r.randint(-6, 6)
        c = r.randint(1, 4 if base == 2 else 3)
        N = base ** c
        # (x − a)(x − b) = N
        D = (a + b) ** 2 - 4 * (a * b - N)
        if a != b and is_sq(D):
            sq = math.isqrt(D)
            x1, x2 = F(a + b - sq, 2), F(a + b + sq, 2)
            if x1.denominator == 1 and x2.denominator == 1:
                break
    good = [x for x in (x1, x2) if x > a and x > b]
    rr = real_roots([1, -(a + b), a * b - N])
    chk = [x for x in rr if x - a > 1e-9 and x - b > 1e-9 and abs(math.log(x - a, base) + math.log(x - b, base) - c) < 1e-7]
    return dict(t=f"log{'₂' if base == 2 else '₃'}({xm(a)}) + log{'₂' if base == 2 else '₃'}({xm(b)}) = {c} tənliyinin köklərinin cəmini tapın.",
                a=sum(good), d=[x1 + x2, x1, a + b, sum(good) + 1, sum(good) - 1],
                e=f"({xm(a)})({xm(b)}) = {base}^{c} = {N} ⇒ x = {show(x1)} və x = {show(x2)}. "
                  f"Təyin oblastı: x > {neg(str(max(a, b)))}. Uyğun kök(lər): {', '.join(show(x) for x in good)}.",
                chk=sum(chk), diff=H)


# ======================= alg-sys =======================

def sys_tickets(r, g):
    while True:
        pa, pc = r.randint(4, 15), r.randint(2, 9)
        if pa <= pc:
            continue
        a, c = r.randint(5, 80), r.randint(5, 80)
        n, total = a + c, pa * a + pc * c
        break
    ask = r.choice(["diff", "adult"])
    ans = a - c if ask == "diff" else a
    sols = [(x, n - x) for x in range(0, n + 1) if pa * x + pc * (n - x) == total]
    chk = (sols[0][0] - sols[0][1]) if ask == "diff" else sols[0][0]
    q = "Böyüklər üçün bilet uşaqlar üçün olandan neçə ədəd çox (mənfi — az) satılıb?" if ask == "diff" else "Böyüklər üçün neçə bilet satılıb?"
    return dict(t=f"Teatrda böyük bileti {pa} manat, uşaq bileti {pc} manatdır. Cəmi {n} bilet satıldı və {total} manat gəlir əldə edildi. {q}",
                a=ans, d=[c - a if ask == "diff" else c, ans + 2, ans - 2, ans + 1, ans - 1],
                e=f"x + y = {n}, {pa}x + {pc}y = {total} ⇒ x = {a}, y = {c}.", chk=chk, diff=M)


def sys_sym(r, g):
    while True:
        s, p = r.randint(-9, 12), r.randint(-20, 30)
        if s * s - 4 * p > 0 and p != 0:
            break
    kind = r.choice(["sq", "cube"] if g == 9 else ["cube", "ratio", "four"])
    rr = real_roots([1, -s, p])
    x, y = rr
    if kind == "sq":
        ans, chk, w = s * s - 2 * p, x * x + y * y, "x² + y²"
        d = [s * s, s * s + 2 * p, s * s - p, ans + 1]
        how = f"x² + y² = (x + y)² − 2xy = {s * s} − {par(2 * p)}"
    elif kind == "cube":
        ans, chk, w = s ** 3 - 3 * p * s, x ** 3 + y ** 3, "x³ + y³"
        d = [s ** 3, s ** 3 + 3 * p * s, s ** 3 - p * s, s * (s * s - p)]
        how = f"x³ + y³ = (x + y)³ − 3xy(x + y) = {par(s ** 3)} − {par(3 * p * s)}"
    elif kind == "ratio":
        ans, chk, w = F(s * s - 2 * p, p), x / y + y / x, "x/y + y/x"
        d = [F(s * s, p), F(s * s + 2 * p, p), F(s * s - 2 * p, s) if s else F(1), F(s * s - p, p)]
        how = f"x/y + y/x = (x² + y²)/(xy) = ({s * s} − {par(2 * p)})/{par(p)}"
    else:
        q2 = s * s - 2 * p
        ans, chk, w = q2 * q2 - 2 * p * p, x ** 4 + y ** 4, "x⁴ + y⁴"
        d = [q2 * q2, q2 * q2 + 2 * p * p, q2 * q2 - p * p, s ** 4 - 2 * p * p]
        how = f"x² + y² = {q2}; x⁴ + y⁴ = (x² + y²)² − 2(xy)² = {q2 * q2} − {2 * p * p}"
    return dict(t=f"x + y = {neg(str(s))} və xy = {neg(str(p))} olarsa, {w} ifadəsinin qiymətini tapın.", a=ans, d=d,
                e=f"{how} = {show(ans)}.", chk=chk, diff=M if kind in ("sq", "cube") else H)


def sys_diffsq(r, g):
    while True:
        x, y = r.randint(-12, 15), r.randint(-12, 15)
        if x + y != 0 and x != y:
            break
    A, B = x * x - y * y, x + y
    kind = r.choice(["xy", "x2y2"])
    ans = x * y if kind == "xy" else x * x + y * y
    # müstəqil: x − y = A/B
    dd = F(A, B)
    xx, yy = (B + dd) / 2, (B - dd) / 2
    chk = xx * yy if kind == "xy" else xx * xx + yy * yy
    return dict(t=f"x² − y² = {neg(str(A))} və x + y = {neg(str(B))} olarsa, {'xy' if kind == 'xy' else 'x² + y²'} ifadəsinin qiymətini tapın.",
                a=ans, d=[-ans, ans + B, x * y if kind != "xy" else x * x + y * y, ans - 1, ans + 1],
                e=f"x − y = {neg(str(A))} : {par(B)} = {neg(str(x - y))}. x = {neg(str(x))}, y = {neg(str(y))}. Cavab: {neg(str(ans))}.",
                chk=chk, diff=M)


def sys_param(r, g):
    k = r.choice([2, 3, 4, 5, 6])
    b = r.randint(1, 12)
    sgn = r.choice([1, -1])
    c = sgn * b  # a = sgn·k: sonsuz həll, a = −sgn·k: həll yoxdur
    want = r.choice(["none", "inf"])
    none_vals = [a for a in range(-20, 21) if _rank_case(a, k, b, c) == "none"]
    inf_vals = [a for a in range(-20, 21) if _rank_case(a, k, b, c) == "inf"]
    target = none_vals if want == "none" else inf_vals
    q = "həlli yoxdur" if want == "none" else "sonsuz sayda həlli var"
    ans = -sgn * k if want == "none" else sgn * k
    return dict(t=f"a-nın hansı qiymətində {{ax + {k}y = {b}; {k}x + ay = {neg(str(c))}}} sisteminin {q}?",
                a=ans, d=[-ans, k * k, 0, ans + 1, ans - 1, 2 * ans],
                e=f"Həll yeganə deyilsə, a/{k} = {k}/a ⇒ a = ±{k}. a = {k}: {k}x + {k}y = {b} və {k}x + {k}y = {neg(str(c))}; "
                  f"a = −{k}: −{k}x + {k}y = {b} və {k}x − {k}y = {neg(str(c))}, yəni −{k}x + {k}y = {neg(str(-c))}. "
                  f"Sağ tərəflər üst-üstə düşəndə sonsuz həll, fərqli olanda həll yoxdur. Cavab: a = {neg(str(ans))}.",
                chk=target[0] if len(target) == 1 else 999, open=False, diff=H)


def _rank_case(a, k, b, c):
    det = a * a - k * k
    if det != 0:
        return "one"
    # a = ±k: ikinci sətir birinciyə mütənasibdir (k/a = a/k)
    ratio = F(k, a)  # 2-ci = ratio × 1-ci (sol tərəf)
    return "inf" if F(c) == ratio * b else "none"


def sys_three(r, g):
    x, y, z = r.randint(-6, 9), r.randint(-6, 9), r.randint(-6, 9)
    a, b, c = x + y, y + z, x + z
    ask = r.choice(["xyz", "x2"])
    ans = x * y * z if ask == "xyz" else x * x + y * y + z * z
    M_ = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]], float)
    sx, sy, sz = np.linalg.solve(M_, [a, b, c])
    chk = sx * sy * sz if ask == "xyz" else sx * sx + sy * sy + sz * sz
    return dict(t=f"x + y = {neg(str(a))}, y + z = {neg(str(b))}, x + z = {neg(str(c))} olarsa, {'xyz' if ask == 'xyz' else 'x² + y² + z²'} ifadəsinin qiymətini tapın.",
                a=ans, d=[-ans if ans else 1, ans + 1, ans - 1, (a + b + c) if ask == "xyz" else (a * a + b * b + c * c) // 2, ans + 2],
                e=f"Üç tənliyi toplayın: 2(x + y + z) = {neg(str(a + b + c))}, x + y + z = {neg(show(F(a + b + c, 2)))}. "
                  f"x = {neg(str(x))}, y = {neg(str(y))}, z = {neg(str(z))}. Cavab: {neg(str(ans))}.",
                chk=chk, diff=H)


def sys_recip(r, g):
    while True:
        x, y = r.randint(1, 12), r.randint(1, 12)
        if x != y:
            break
    A = F(1, x) + F(1, y)
    B = x + y
    ans = x * y
    # 1/x + 1/y = (x+y)/xy ⇒ xy = B/A
    chk = B / A
    ask = r.choice(["xy", "x2y2"])
    if ask == "x2y2":
        ans, chk = x * x + y * y, B * B - 2 * (B / A)
    return dict(t=f"1/x + 1/y = {show(A)} və x + y = {B} olarsa, {'xy' if ask == 'xy' else 'x² + y²'} ifadəsinin qiymətini tapın.",
                a=ans, d=[B * A if (B * A).denominator == 1 else ans + 3, ans + 2, ans - 2, B * B, ans + B],
                e=f"1/x + 1/y = (x + y)/(xy) ⇒ xy = {B} : {show(A)} = {x * y}." + (f" x² + y² = {B}² − 2·{x * y} = {ans}." if ask == "x2y2" else ""),
                chk=chk, diff=H)


def sys_linear(r, g):
    while True:
        x, y = r.randint(-9, 12), r.randint(-9, 12)
        a, b, c, d_ = r.randint(-7, 9), r.randint(-7, 9), r.randint(-7, 9), r.randint(-7, 9)
        if a * d_ - b * c != 0 and 0 not in (a, b, c, d_) and x != y:
            break
    e1, e2 = a * x + b * y, c * x + d_ * y
    det = a * d_ - b * c
    cx, cy = F(e1 * d_ - b * e2, det), F(a * e2 - c * e1, det)
    ask = r.choice(["x − y", "xy", "x + 2y"])
    f = {"x − y": lambda u, v: u - v, "xy": lambda u, v: u * v, "x + 2y": lambda u, v: u + 2 * v}[ask]
    t1 = f"{lead(a, 'x')}{sg(b, 'y')} = {neg(str(e1))}"
    t2 = f"{lead(c, 'x')}{sg(d_, 'y')} = {neg(str(e2))}"
    return dict(t=f"{{{t1}; {t2}}} sistemi üçün {ask} ifadəsinin qiymətini tapın.", a=f(x, y),
                d=[f(y, x), x + y, f(x, y) + 1, f(x, y) - 1, -f(x, y)],
                e=f"Toplama və ya əvəzləmə üsulu: x = {neg(str(x))}, y = {neg(str(y))}. {ask} = {neg(str(f(x, y)))}.",
                chk=f(cx, cy), diff=M)


# ======================= alg-quad =======================

def _quad(r, need_irr=True):
    while True:
        a = r.choice([1, 1, 2, 3, -1, 2])
        b, c = r.randint(-12, 12), r.randint(-15, 15)
        D = b * b - 4 * a * c
        if D > 0 and c != 0 and b != 0 and (not need_irr or not is_sq(D)):
            return a, b, c


def quad_vieta(r, g):
    a, b, c = _quad(r)
    s, p = F(-b, a), F(c, a)
    kinds = {9: ["sq", "abs2"], 10: ["cube", "inv2", "sq"], 11: ["ratio", "four", "shift"]}[g]
    kind = r.choice(kinds)
    x1, x2 = real_roots([a, b, c])
    if kind == "sq":
        ans, chk, w, how = s * s - 2 * p, x1 ** 2 + x2 ** 2, "x₁² + x₂²", f"(x₁ + x₂)² − 2x₁x₂ = {show(s * s)} − {par(2 * p)}"
        d = [s * s, s * s + 2 * p, s * s - p, -ans]
    elif kind == "abs2":
        ans, chk, w, how = s * s - 4 * p, (x1 - x2) ** 2, "(x₁ − x₂)²", f"(x₁ + x₂)² − 4x₁x₂ = {show(s * s)} − {par(4 * p)}"
        d = [s * s - 2 * p, s * s + 4 * p, s * s, ans / 4 if ans != 0 else 1]
    elif kind == "cube":
        ans, chk, w, how = s ** 3 - 3 * p * s, x1 ** 3 + x2 ** 3, "x₁³ + x₂³", f"(x₁ + x₂)³ − 3x₁x₂(x₁ + x₂) = {show(s ** 3)} − {par(3 * p * s)}"
        d = [s ** 3, s ** 3 + 3 * p * s, s ** 3 - p * s, -ans]
    elif kind == "inv2":
        ans, chk, w, how = (s * s - 2 * p) / (p * p), x1 ** -2 + x2 ** -2, "1/x₁² + 1/x₂²", f"(x₁² + x₂²)/(x₁x₂)² = ({show(s * s - 2 * p)})/{show(p * p)}"
        d = [(s * s - 2 * p) / p, s * s / (p * p), (s * s + 2 * p) / (p * p), 1 / ans if ans else F(1)]
    elif kind == "ratio":
        ans, chk, w, how = (s * s - 2 * p) / p, x1 / x2 + x2 / x1, "x₁/x₂ + x₂/x₁", f"(x₁² + x₂²)/(x₁x₂) = ({show(s * s - 2 * p)})/{par(p)}"
        d = [s * s / p, (s * s + 2 * p) / p, (s * s - 2 * p) / s, -ans]
    elif kind == "four":
        q2 = s * s - 2 * p
        ans, chk, w, how = q2 * q2 - 2 * p * p, x1 ** 4 + x2 ** 4, "x₁⁴ + x₂⁴", f"(x₁² + x₂²)² − 2(x₁x₂)², x₁² + x₂² = {show(q2)}: {show(q2 * q2)} − {show(2 * p * p)}"
        d = [q2 * q2, q2 * q2 + 2 * p * p, q2 * q2 - p * p, s ** 4 - 2 * p * p]
    else:  # (x₁ + 1/x₂)(x₂ + 1/x₁)
        ans, chk, w, how = p + 2 + 1 / p, (x1 + 1 / x2) * (x2 + 1 / x1), "(x₁ + 1/x₂)(x₂ + 1/x₁)", f"x₁x₂ + 2 + 1/(x₁x₂) = {show(p)} + 2 {'+' if p > 0 else '−'} {show(abs(1 / p))}"
        d = [p + 1 / p, p + 1 + 1 / p, p + 2, s + 2 + 1 / p]
    return dict(t=f"x₁ və x₂ ədədləri {poly([a, b, c])} = 0 tənliyinin kökləridir. {w} ifadəsinin qiymətini tapın.",
                a=ans, d=d, e=f"Viyet teoremi: x₁ + x₂ = {show(s)}, x₁x₂ = {show(p)}. {w} = {how} = {show(ans)}.",
                chk=chk, diff=M if kind in ("sq", "abs2") else H)


def quad_ratio_param(r, g):
    while True:
        k = r.choice([2, 3, 4, F(3, 2), 5])
        x2 = r.choice([1, 2, 3, 4, -1, -2, -3, 6])
        x1 = k * x2
        if F(x1).denominator == 1:
            break
    q = x1 * x2
    m = x1 + x2
    # x² − m x + q = 0, kökün biri digərindən k dəfə böyükdür; m > 0 və ya m < 0 şərti ilə yeganə
    sign = "müsbət" if m > 0 else "mənfi"
    cands = []
    for mm in range(-60, 61):
        D = mm * mm - 4 * q
        if D < 0:
            continue
        rr = real_roots([1, -mm, q])
        if len(rr) == 2:
            u, v = rr
            if any(abs(a1 - k * b1) < 1e-9 for a1, b1 in ((u, v), (v, u))) and (mm > 0) == (m > 0):
                cands.append(mm)
    return dict(t=f"x² − mx + {q} = 0 tənliyinin köklərindən biri digərindən {show(k)} dəfə böyükdür. m-in {sign} qiymətini tapın.".replace("+ −", "− "),
                a=m, d=[-m, m + 1, m - 1, q, int(m * 2)],
                e=f"x₁ = {show(k) if F(k).denominator == 1 else '(' + show(k) + ')·'}x₂, x₁x₂ = {show(k) if F(k).denominator == 1 else '(' + show(k) + ')·'}x₂² = {q} ⇒ x₂² = {show(F(q) / k)}, x₂ = {neg(str(x2))}, x₁ = {neg(show(x1))}. m = x₁ + x₂ = {neg(show(m))}.",
                chk=cands[0] if len(cands) == 1 else 999, diff=H)


def quad_ineq_count(r, g):
    while True:
        a = r.choice([1, 2, 3])
        r1, r2 = sorted([F(r.randint(-24, 24), r.choice([1, 2, 3])) for _ in range(2)])
        if r1 != r2 and r2 - r1 < 25:
            b, c = -a * (r1 + r2), a * r1 * r2
            if b.denominator == 1 and c.denominator == 1:
                break
    strict = r.choice([True, False])
    sign = "<" if strict else "≤"
    rel = (lambda v: v < 0) if strict else (lambda v: v <= 0)
    sols = [x for x in range(-100, 101) if rel(a * x * x + b * x + c)]
    if a > 0:
        ans = len([x for x in range(-100, 101) if (r1 < x < r2 if strict else r1 <= x <= r2)])
        how = f"Köklər {show(r1)} və {show(r2)}; a > 0, həllər köklər arasındadır."
    else:
        ans = None
        return quad_ineq_count(r, g)
    return dict(t=f"{poly([a, int(b), int(c)])} {sign} 0 bərabərsizliyini ödəyən tam ədədlərin sayını tapın.", a=ans,
                d=[ans + 1, ans - 1, ans + 2, ans - 2], e=f"{how} Tam həllər: {ans}.", chk=len(sols), diff=M)


def quad_param_min(r, g):
    """x² − 2(m + p)x + m² + q = 0 tənliyinin iki müxtəlif kökü olması üçün m-in ən kiçik tam qiyməti"""
    while True:
        p, q = r.randint(-5, 6), r.randint(-10, 20)
        # D/4 = (m+p)² − m² − q = 2pm + p² − q > 0
        if p != 0:
            break
    bound = F(q - p * p, 2 * p)
    if p > 0:
        ans = math.floor(bound) + 1
        ask = "ən kiçik"
    else:
        ans = math.ceil(bound) - 1
        ask = "ən böyük"
    good = [m for m in range(-200, 201) if (2 * (m + p)) ** 2 - 4 * (m * m + q) > 0]
    chk = min(good) if p > 0 else max(good)
    return dict(t=f"m-in hansı {ask} tam qiymətində x² − 2(m {'+' if p > 0 else '−'} {abs(p)})x + m² {'+' if q >= 0 else '−'} {abs(q)} = 0 tənliyinin iki müxtəlif həqiqi kökü var?",
                a=ans, d=[ans + 1, ans - 1, ans + 2, ans - 2, -ans],
                e=f"D/4 = (m {'+' if p > 0 else '−'} {abs(p)})² − (m² {'+' if q >= 0 else '−'} {abs(q)}) = {poly([2 * p, p * p - q], 'm')} > 0 ⇒ "
                  f"m {'>' if p > 0 else '<'} {show(bound)}. {ask.capitalize()} tam qiymət: {neg(str(ans))}.".replace("1m", "m"),
                chk=chk, diff=H)


def quad_both_pos(r, g):
    """x² − (m + a)x + (m + b) = 0 köklərinin hər ikisi müsbət olsun — [lo; hi] aralığında uyğun tam m-lərin sayı"""
    while True:
        a, b = r.randint(-4, 6), r.randint(-6, 6)
        lo, hi = -15, 15
        good = []
        for m in range(lo, hi + 1):
            S, P = m + a, m + b
            D = S * S - 4 * P
            if D > 0 and S > 0 and P > 0:
                good.append(m)
        if 3 <= len(good) <= 25:
            break
    chk = 0
    for m in range(lo, hi + 1):
        rr = real_roots([1, -(m + a), m + b])
        if len(rr) == 2 and abs(rr[0] - rr[1]) > 1e-9 and min(rr) > 1e-12:
            chk += 1
    return dict(t=f"m ∈ [{neg(str(lo))}; {hi}] tam ədədlərindən neçəsi üçün x² − (m {'+' if a >= 0 else '−'} {abs(a)})x + m {'+' if b >= 0 else '−'} {abs(b)} = 0 tənliyinin iki müxtəlif müsbət kökü var?",
                a=len(good), d=[len(good) + 1, len(good) - 1, len(good) + 2, len(good) - 2],
                e=f"Şərtlər: D > 0, x₁ + x₂ = m {'+' if a >= 0 else '−'} {abs(a)} > 0, x₁x₂ = m {'+' if b >= 0 else '−'} {abs(b)} > 0. "
                  f"Uyğun m-lər: {', '.join(neg(str(x)) for x in good)} — {len(good)} ədəd.", chk=chk, diff=H)


def quad_new_eq(r, g):
    a, b, c = _quad(r)
    if a != 1:
        a = 1
        b, c = r.randint(-9, 9), r.randint(-12, 12)
        if b * b - 4 * c <= 0 or b == 0 or c == 0:
            return quad_new_eq(r, g)
    s, p = -b, c
    k = r.randint(1, 4) * r.choice([1, -1])
    # köklər x₁ + k, x₂ + k: yeni tənlik y² − (s + 2k)y + (p + ks + k²)
    q = p + k * s + k * k
    x1, x2 = real_roots([1, b, c])
    chk = (x1 + k) * (x2 + k)
    return dict(t=f"x² {sg(b, 'x')[1:]} {sg(c)[1:]} = 0 tənliyinin kökləri x₁ və x₂-dir. Kökləri x₁ {'+' if k > 0 else '−'} {abs(k)} və x₂ {'+' if k > 0 else '−'} {abs(k)} olan "
                  f"x² + px + q = 0 tənliyində q-nü tapın.",
                a=q, d=[p + k * k, p + k * s, p - k * s + k * k, q + 1, -q],
                e=f"q = (x₁ {'+' if k > 0 else '−'} {abs(k)})(x₂ {'+' if k > 0 else '−'} {abs(k)}) = x₁x₂ {'+' if k > 0 else '−'} {abs(k)}(x₁ + x₂) + {k * k} = "
                  f"{neg(str(p))} {'+' if k * s >= 0 else '−'} {abs(k * s)} + {k * k} = {neg(str(q))}.", chk=chk, diff=H)


# ======================= alg-prog (Ardıcıllıqlar) =======================

def seq_ap(r, g):
    while True:
        a1, d = r.randint(-20, 30), r.choice([x for x in range(-7, 9) if x != 0])
        p, q = r.sample(range(2, 15), 2)
        rr_ = r.randint(3, 20)
        n = r.randint(10, 30)
        if rr_ not in (p, q):
            break
    term = lambda k: a1 + (k - 1) * d
    X, Y = term(p) + term(q), term(rr_)
    S = n * (2 * a1 + (n - 1) * d) // 2
    chk = sum(term(k) for k in range(1, n + 1))
    return dict(t=f"Ədədi silsilədə a{_sub(p)} + a{_sub(q)} = {neg(str(X))} və a{_sub(rr_)} = {neg(str(Y))} olarsa, ilk {n} həddin cəmini tapın.",
                a=S, d=[S + n * d, S - n * d, n * (a1 + term(n - 1)) // 2 if (n * (a1 + term(n - 1))) % 2 == 0 else S + d, S + term(n), S - term(n)],
                e=f"2a₁ + {p + q - 2}d = {neg(str(X))}, a₁ + {rr_ - 1}d = {neg(str(Y))} ⇒ a₁ = {neg(str(a1))}, d = {neg(str(d))}. "
                  f"S{_sub(n)} = (2a₁ + {n - 1}d)·{n}/2 = {neg(str(S))}.", chk=chk, diff=M)


def _sub(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


def seq_gp(r, g):
    while True:
        b1 = r.choice([1, 2, 3, 4, 5, -1, -2, -3, 6, 7])
        q = r.choice([2, 3, -2, -3, F(1, 2), -F(1, 2)])
        i, j = r.sample(range(2, 7), 2)
        if i < j:
            break
    term = lambda k: b1 * F(q) ** (k - 1)
    n = r.randint(5, 8)
    S = sum(term(k) for k in range(1, n + 1))
    # müstəqil: düsturla
    chk = b1 * (F(q) ** n - 1) / (F(q) - 1)
    signhint = f" (q {'>' if q > 0 else '<'} 0)" if (j - i) % 2 == 0 else ""
    return dict(t=f"Həndəsi silsilədə b{_sub(i)} = {show(term(i))} və b{_sub(j)} = {show(term(j))}{signhint}. İlk {n} həddin cəmini tapın.",
                a=S, d=[S - term(n) + term(n + 1), S - term(n), S + term(1), -S, S + term(n + 1)],
                e=(f"q^{j - i} = b{_sub(j)}/b{_sub(i)} = {show(term(j) / term(i))} ⇒ q = {show(q)}" if j - i > 1 else f"q = b{_sub(j)}/b{_sub(i)} = {show(q)}") + f", b₁ = {show(b1)}. "
                  f"S{_sub(n)} = b₁(qⁿ − 1)/(q − 1) = {show(S)}.", chk=chk, diff=H)


def seq_inf(r, g):
    while True:
        b1 = r.randint(1, 12) * r.choice([1, -1])
        q = F(r.randint(-5, 5), r.randint(2, 7))
        if q != 0 and abs(q) < 1:
            break
    S = b1 / (1 - q)
    S2 = F(b1 * b1) / (1 - q * q)
    # S2 / S = b1 / (1 + q);  S = b1/(1 − q)
    ask = r.choice(["b1", "q"])
    ans = b1 if ask == "b1" else q
    # müstəqil: qismən cəmlər
    ps = sum(float(b1) * float(q) ** k for k in range(400))
    ps2 = sum(float(b1) ** 2 * float(q) ** (2 * k) for k in range(400))
    assert abs(ps - float(S)) < 1e-9 and abs(ps2 - float(S2)) < 1e-9
    # S və S2-dən b1, q: S2/S = b1/(1+q), S = b1/(1−q) ⇒ (S2/S)(1+q) = S(1−q) ⇒ q = (S − S2/S)/(S + S2/S)
    t_ = S2 / S
    qq = (S - t_) / (S + t_)
    bb = S * (1 - qq)
    chk = bb if ask == "b1" else qq
    return dict(t=f"Sonsuz azalan həndəsi silsilənin hədlərinin cəmi {show(S)}, hədlərin kvadratlarının cəmi isə {show(S2)}-dir. "
                  f"{'Silsilənin birinci həddini' if ask == 'b1' else 'Silsilənin vuruğunu (q)'} tapın.",
                a=ans, d=[-ans, ans * 2, (1 - q) if ask == "b1" else q * q, ans + 1, 1 / F(ans), F(ans) / 2],
                e=f"b₁/(1 − q) = {show(S)}, b₁²/(1 − q²) = {show(S2)}. Bölsək: b₁/(1 + q) = {show(t_)}. "
                  f"İki tənlikdən q = {show(q)}, b₁ = {show(b1)}.", chk=chk, diff=H)


def seq_recur(r, g):
    while True:
        k = r.choice([2, 3, -2, 2])
        m = r.randint(-5, 6)
        a1 = r.randint(-4, 6)
        n = r.randint(5, 9 if k in (2, -2) else 7)
        if k != 1 and a1 * (k - 1) + m != 0:
            break
    # a_{n} = (a1 + c)k^{n−1} − c, c = m/(k−1)
    c = F(m, k - 1)
    ans = (a1 + c) * F(k) ** (n - 1) - c
    v = F(a1)
    for _ in range(n - 1):
        v = k * v + m
    return dict(t=f"Ardıcıllıq a₁ = {neg(str(a1))} və aₙ₊₁ = {k if k > 0 else '(' + neg(str(k)) + ')'}·aₙ {'+' if m >= 0 else '−'} {abs(m)} qaydası ilə verilib. a{_sub(n)} həddini tapın.".replace(" + 0 ", " ").replace(" − 0 ", " "),
                a=ans, d=[(a1 + c) * F(k) ** n - c, (a1 + c) * F(k) ** (n - 2) - c, ans + m, ans - m if m else ans + 1, -ans],
                e=f"Hədləri ardıcıl hesablayın (və ya aₙ + {show(c)} = (a₁ + {show(c)})·{par(k)}ⁿ⁻¹ ilə): a{_sub(n)} = {show(ans)}.",
                chk=v, diff=H)


def seq_quadterm(r, g):
    while True:
        p, q = r.randint(3, 30), r.randint(-20, 40)
        neg_terms = [n for n in range(1, 200) if n * n - p * n + q < 0]
        if neg_terms and len(neg_terms) >= 2:
            break
    ask = r.choice(["count", "min"])
    if ask == "count":
        chk = len(neg_terms)
        D = p * p - 4 * q
        lo, hi = (p - math.sqrt(D)) / 2, (p + math.sqrt(D)) / 2
        ans = len([n for n in range(max(1, math.floor(lo)), math.ceil(hi) + 1) if lo < n < hi])
        t = f"aₙ = n² − {p}n {'+' if q >= 0 else '−'} {abs(q)} ardıcıllığının neçə həddi mənfidir?"
        e = f"n² − {p}n {'+' if q >= 0 else '−'} {abs(q)} < 0 ⇒ {lo:.2f} < n < {hi:.2f}".replace(".", ",") + f". Natural n-lər: {ans}."
        d = [ans + 1, ans - 1, ans + 2, ans - 2]
    else:
        vals = {n: n * n - p * n + q for n in range(1, 200)}
        chk = min(vals.values())
        n0 = p // 2 if p % 2 == 0 else None
        cands = [p // 2, p // 2 + 1] if p % 2 else [p // 2]
        ans = min(n * n - p * n + q for n in cands if n >= 1)
        t = f"aₙ = n² − {p}n {'+' if q >= 0 else '−'} {abs(q)} ardıcıllığının ən kiçik həddini tapın."
        e = f"Parabolanın təpəsi n = {show(F(p, 2))}. Ən yaxın natural n: {', '.join(map(str, cands))}. Ən kiçik hədd: {neg(str(ans))}."
        d = [q - F(p * p, 4) if p % 2 else ans - 1, ans + 1, ans - 1, ans + 2, F(4 * q - p * p, 4)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=H)


def seq_multiples(r, g):
    while True:
        A, B = r.randint(10, 200), r.randint(250, 999)
        p, q = r.choice([3, 4, 6, 7, 9, 11]), r.choice([2, 5, 10, 4])
        if math.gcd(p, q) == 1 or q % p != 0:
            break
    L = p * q // math.gcd(p, q)
    s = lambda k: (B // k) * (B // k + 1) // 2 * k - ((A - 1) // k) * ((A - 1) // k + 1) // 2 * k
    ans = s(p) - s(L)
    chk = sum(x for x in range(A, B + 1) if x % p == 0 and x % q != 0)
    return dict(t=f"{_abl_num(A)} {_dat_num(B)} qədər (hər ikisi daxil) {p}-ə bölünən, lakin {q}-yə bölünməyən natural ədədlərin cəmini tapın.".replace(f"{p}-ə", _dat_num(p)).replace(f"{q}-yə", _dat_num(q)),
                a=ans, d=[s(p), s(p) - s(q), ans + L, ans - L, s(L)],
                e=f"{p}-ə bölünənlərin cəmi (ədədi silsilə): {s(p)}. Onlardan {L}-ə bölünənlər (həm {p}-ə, həm {q}-yə): {s(L)}. Fərq: {ans}.".replace(f"{p}-ə", _dat_num(p)).replace(f"{q}-yə", _dat_num(q)).replace(f"{L}-ə", _dat_num(L)),
                chk=chk, diff=H)


def _abl_num(n):
    from common import abl
    return abl(n)


def _dat_num(n):
    from common import dat
    return dat(n)


def seq_sn(r, g):
    a, b = r.randint(-5, 6), r.randint(-9, 9)
    if a == 0:
        a = 2
    k = r.randint(3, 15)
    m = r.randint(k + 3, 28)
    Sn = lambda n: a * n * n + b * n
    ask = r.choice(["term", "range"])
    if ask == "term":
        ans = Sn(k) - Sn(k - 1)
        chk = 2 * a * k + (b - a)
        t = f"Ardıcıllığın ilk n həddinin cəmi Sₙ = {poly([a, b, 0], 'n')} düsturu ilə verilir. a{_sub(k)} həddini tapın."
        e = f"a{_sub(k)} = S{_sub(k)} − S{_sub(k - 1)} = {neg(str(Sn(k)))} − {par(Sn(k - 1))} = {neg(str(ans))}."
        d = [Sn(k), 2 * a * k + b, ans + 2 * a, ans - 2 * a, Sn(k) // k if Sn(k) % k == 0 else ans + 1]
    else:
        ans = Sn(m) - Sn(k - 1)
        chk = sum(2 * a * i + (b - a) for i in range(k, m + 1))
        t = f"Ardıcıllığın ilk n həddinin cəmi Sₙ = {poly([a, b, 0], 'n')} düsturu ilə verilir. a{_sub(k)} + a{_sub(k + 1)} + … + a{_sub(m)} cəmini tapın."
        e = f"Cəm = S{_sub(m)} − S{_sub(k - 1)} = {neg(str(Sn(m)))} − {par(Sn(k - 1))} = {neg(str(ans))}."
        d = [Sn(m) - Sn(k), Sn(m), ans + 2 * a * k + b - a, ans - (2 * a * m + b - a), -ans]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=H)


def seq_ap_gp(r, g):
    """AP-nin üç həddinə ədədlər əlavə edəndə GP alınır"""
    while True:
        g0 = r.randint(1, 6)
        q = r.choice([2, 3, F(3, 2)])
        G = [g0 * F(q) ** i for i in range(3)]
        if any(x.denominator != 1 for x in G):
            continue
        a1, a2 = r.randint(0, 6), r.randint(0, 9)
        a3 = G[0] + G[2] - 2 * G[1] + 2 * a2 - a1
        A = [G[0] - a1, G[1] - a2, G[2] - a3]
        d = A[1] - A[0]
        if a3 >= 0 and d > 0 and A[0] > 0:
            break
    S = sum(A)
    x = F(S, 3)
    # müstəqil: d üzrə (x − d + a1)(x + d + a3) = (x + a2)² kvadrat tənliyi, d > 0 olanlar
    rr = real_roots([-1, (a1 - a3), (x + a1) * (x + a3) - (x + a2) ** 2])
    rr = [dd for dd in rr if dd > 1e-9 and abs(x - dd + a1) > 1e-9]
    if len(rr) != 1:
        return seq_ap_gp(r, g)
    chk = float(x) + rr[0]
    return dict(t=f"Artan ədədi silsilənin üç ardıcıl həddinin cəmi {S}-dir. Bu hədlərə uyğun olaraq {a1}, {a2} və {a3} əlavə etsək, "
                  f"həndəsi silsilə alınır. Ədədi silsilənin ən böyük həddini tapın.".replace(f"cəmi {S}-dir", f"cəmi {_cop(S)}"),
                a=A[2], d=[A[0], A[1], G[2], A[2] + 1, A[2] - 1, G[1]],
                e=f"Hədlər x − d, x, x + d; 3x = {S} ⇒ x = {show(x)}. (x − d + {a1})(x + d + {a3}) = (x + {a2})² ⇒ d = {show(d)} (d > 0). "
                  f"Ən böyük hədd: {show(x)} + {show(d)} = {show(A[2])}.", chk=chk, diff=H)


def _cop(n):
    from common import cop
    s = cop(n)
    return "−" + s[1:] if s.startswith("-") else s


def seq_fib(r, g):
    while True:
        a1, a2 = r.randint(-5, 9), r.randint(-5, 12)
        n = r.randint(6, 9)
        seq = [a1, a2]
        while len(seq) < n:
            seq.append(seq[-1] + seq[-2])
        if a1 != a2:
            break
    # a₁ və aₙ verilir, a₂ tapılır
    target = seq[n - 1]
    sols = [x for x in range(-200, 201) if _fib(a1, x, n) == target]
    return dict(t=f"Ardıcıllıqda hər hədd (üçüncüdən başlayaraq) özündən əvvəlki iki həddin cəminə bərabərdir. a₁ = {neg(str(a1))} və a{_sub(n)} = {neg(str(target))} olarsa, a₂ həddini tapın.",
                a=a2, d=[a2 + 1, a2 - 1, a2 + 2, a2 - 2, -a2],
                e=f"a₂ = x olsun: a₃ = {neg(str(a1))} + x, a₄ = {neg(str(a1))} + 2x, … a{_sub(n)} = {_fibcoef(n)[0]}·{par(a1)} + {_fibcoef(n)[1]}x = {neg(str(target))} ⇒ x = {neg(str(a2))}.",
                chk=sols[0] if len(sols) == 1 else 999, diff=M)


def _fib(a, b, n):
    s = [a, b]
    while len(s) < n:
        s.append(s[-1] + s[-2])
    return s[n - 1]


def _fibcoef(n):
    # aₙ = F_{n−2}·a₁ + F_{n−1}·a₂
    f = [0, 1]
    while len(f) < n + 1:
        f.append(f[-1] + f[-2])
    return f[n - 2], f[n - 1]


# ======================= alg-func =======================

def fn_comp_eq(r, g):
    while True:
        a, b = r.choice([2, 3, -2, -1, 1]), r.randint(-6, 6)
        p, q = r.randint(-6, 6), r.randint(-9, 9)
        c = r.randint(-10, 20)
        # f(x) = ax + b, g(x) = x² + px + q.  f(g(x)) = c ⇒ x² + px + q = (c − b)/a
        rhs = F(c - b, a)
        D = p * p - 4 * (q - rhs)
        if D > 0 and p != 0:
            break
    ans = -p
    rr = real_roots([a, a * p, a * q + b - c])
    return dict(t=f"f(x) = {poly([a, b])}, g(x) = {poly([1, p, q])}. f(g(x)) = {neg(str(c))} tənliyinin köklərinin cəmini tapın.",
                a=ans, d=[p, -p + 1, F(c - b, a), -2 * p, ans - 1],
                e=f"f(g(x)) = {poly([a, b], 'g(x)')} = {neg(str(c))} ⇒ g(x) = {show(rhs)} ⇒ {poly([1, p, q - rhs])} = 0 "
                  f"(D > 0). Köklərin cəmi {neg(str(ans))}.".replace("  ", " "), chk=sum(rr), diff=M)


def fn_inverse(r, g):
    while True:
        a, b, c, d = r.randint(-5, 6), r.randint(-9, 9), r.randint(1, 4), r.randint(-6, 6)
        k = r.randint(-8, 8)
        if a * d - b * c != 0 and c * k - a != 0 and a != 0:
            break
    # f(x) = (ax + b)/(cx + d); f⁻¹(k) = x, f(x) = k ⇒ x = (b − dk)/(ck − a)
    ans = F(b - d * k, c * k - a)
    chk = F(a * ans + b, c * ans + d)
    return dict(t=f"f(x) = ({poly([a, b])})/({poly([c, d])}) funksiyası üçün f⁻¹({neg(str(k))}) qiymətini tapın.",
                a=ans, d=[F(a * k + b, c * k + d) if c * k + d else ans + 1, -ans, F(b + d * k, c * k - a), 1 / ans if ans else ans + 2, ans + 1],
                e=f"f(x) = {neg(str(k))} tənliyini həll edin: {poly([a, b])} = {neg(str(k))}({poly([c, d])}) ⇒ x = {show(ans)}.",
                chk=ans if chk == k else 999, diff=M)


def fn_domain(r, g):
    while True:
        a, b = r.randint(3, 12), r.randint(-6, 6)
        c = r.choice([1, 4, 9, 16, 2, 3])
        dom = [x for x in range(-50, 51) if a - abs(x - b) >= 0 and x * x != c]
        if 4 < len(dom) < 30:
            break
    excl = [x for x in range(b - a, b + a + 1) if x * x == c]
    ans = 2 * a + 1 - len(excl)
    return dict(t=f"y = √({a} − |{xm(b)}|) / (x² − {c}) funksiyasının təyin oblastına neçə tam ədəd daxildir?",
                a=ans, d=[2 * a + 1, ans - 1, ans + 1, 2 * a, ans - 2],
                e=f"|{xm(b)}| ≤ {a} ⇒ {neg(str(b - a))} ≤ x ≤ {neg(str(b + a))}: {2 * a + 1} tam ədəd. x² ≠ {c} şərti "
                  f"{('çıxarır: ' + ', '.join(neg(str(x)) for x in excl)) if excl else 'bu aralıqda heç nə çıxarmır'}. Cavab: {ans}.",
                chk=len(dom), diff=H)


def fn_range_interval(r, g):
    while True:
        a = r.choice([1, 2, -1, -2])
        b, c = r.randint(-8, 8), r.randint(-10, 10)
        p = r.randint(-6, 2)
        q = r.randint(p + 2, p + 8)
        xv = F(-b, 2 * a)
        if xv.denominator <= 4:
            break
    f = lambda x: a * x * x + b * x + c
    pts = [F(p), F(q)] + ([xv] if p <= xv <= q else [])
    vals = [f(x) for x in pts]
    ans = max(vals) - min(vals)
    grid = [f(F(p) + F(i, 100)) for i in range(0, 100 * (q - p) + 1)]
    chk = max(grid) - min(grid)
    return dict(t=f"f(x) = {poly([a, b, c])} funksiyasının [{neg(str(p))}; {neg(str(q))}] parçasında ən böyük və ən kiçik qiymətlərinin fərqini tapın.",
                a=ans, d=[abs(f(F(q)) - f(F(p))), ans + 1, max(vals), ans - 1, abs(f(xv)) if f(xv) != ans else ans + 2],
                e=f"Təpə x₀ = {show(xv)} ({'parçaya düşür' if p <= xv <= q else 'parçadan kənardadır'}). "
                  f"Qiymətlər: " + ", ".join(f"f({show(x)}) = {show(f(x))}" for x in pts) + f". Fərq: {show(ans)}.",
                chk=chk, diff=H)


def fn_functional(r, g):
    while True:
        m = r.choice([2, 3, -2])
        a, b = r.randint(-6, 6), r.randint(-9, 9)
        k = r.randint(-6, 8)
        if a != 0 and m * m != 1:
            break
    # m·f(x) + f(1 − x) = ax + b
    # x → 1 − x: m·f(1 − x) + f(x) = a(1 − x) + b
    # f(x) = (m(ax + b) − (a(1 − x) + b)) / (m² − 1)
    fval = lambda x: (m * (a * x + b) - (a * (1 - x) + b)) / F(m * m - 1)
    ans = fval(F(k))
    # müstəqil: 2×2 sistemi f(k), f(1−k) üçün həll et
    A = np.array([[m, 1], [1, m]], float)
    rhs = np.array([a * k + b, a * (1 - k) + b], float)
    fk, _ = np.linalg.solve(A, rhs)
    return dict(t=f"Bütün x üçün {m}·f(x) + f(1 − x) = {poly([a, b])} bərabərliyi doğrudur. f({neg(str(k))}) qiymətini tapın.".replace(f"{m}·", f"({m})·" if m < 0 else f"{m}·"),
                a=ans, d=[F(a * k + b, m + 1), F(a * k + b, m), fval(F(1 - k)), -ans, ans + 1],
                e=f"x = {neg(str(k))} və x = {neg(str(1 - k))} qoyun: {m}f({neg(str(k))}) + f({neg(str(1 - k))}) = {neg(str(a * k + b))}, "
                  f"{m}f({neg(str(1 - k))}) + f({neg(str(k))}) = {neg(str(a * (1 - k) + b))}. Sistemdən f({neg(str(k))}) = {show(ans)}.",
                chk=fk, diff=H)


def fn_shifted(r, g):
    a, b = r.choice([2, 3, -2, 4]), r.randint(-5, 5)
    p, q, s = r.randint(-4, 4), r.randint(-6, 6), r.randint(-6, 8)
    k = r.randint(-8, 10)
    # f(ax + b) = x² + px + q;  f(k) = ? ⇒ x = (k − b)/a
    x = F(k - b, a)
    ans = x * x + p * x + q
    xs = [F(i, abs(a)) for i in range(-200, 201)]
    chk = [z * z + p * z + q for z in xs if a * z + b == k][0]
    return dict(t=f"f({poly([a, b])}) = {poly([1, p, q])} olarsa, f({neg(str(k))}) qiymətini tapın.",
                a=ans, d=[k * k + p * k + q, (F(k + b, a)) ** 2 + p * F(k + b, a) + q, F(a * k + b) ** 2 + p * (a * k + b) + q, ans + 1, ans - 1],
                e=f"{poly([a, b])} = {neg(str(k))} ⇒ x = {show(x)}. f({neg(str(k))}) = {par(x)}²{(' + ' if p > 0 else ' − ') + str(abs(p)) + '·' + par(x) if p else ''}{sg(q)} = {show(ans)}.",
                chk=chk, diff=M)


def fn_odd_periodic(r, g):
    h = r.choice([1, 2, 3])
    T = 2 * h
    c = r.choice([1, 2, 3, -1])
    N = r.randint(20, 300) * r.choice([1, -1]) + r.choice([F(1, 2), F(1, 3), 0, F(3, 2)])
    # [0; h]-da f(x) = c·x(x − h); f tək, dövrü T
    def f_impl(x):
        x = F(x)
        while x > h:
            x -= T
        while x < -h:
            x += T
        if x >= 0:
            return c * x * (x - h)
        return -(c * (-x) * (-x - h))

    ans = f_impl(N)
    # müstəqil: başqa üsul — x mod T, sonra tək davam
    y = F(N) - T * math.floor(F(N) / T)  # [0; T)
    if y <= h:
        chk = c * y * (y - h)
    else:
        z = T - y  # f(y) = f(y − T) = −f(T − y)
        chk = -(c * z * (z - h))
    ns = show(N) if F(N).denominator == 1 else show(N)
    return dict(t=f"f(x) tək funksiyadır, əsas dövrü {T}-dür və [0; {h}] parçasında f(x) = {lead(c, 'x')}(x − {h}). f({ns}) qiymətini tapın.".replace(f"dövrü {T}-dür", f"dövrü {_cop(T)}"),
                a=ans, d=[-ans, c * F(N) * (F(N) - h), ans + 1, ans * 2, ans - 1],
                e=f"Dövrə görə {ns} ədədini [−{h}; {h}] aralığına gətirin, mənfi arqument üçün f(−x) = −f(x) istifadə edin. Nəticə: {show(ans)}.",
                chk=chk, open=True, diff=H)


def fn_intersect(r, g):
    while True:
        b, c = r.randint(-8, 8), r.randint(-10, 10)
        k, m = r.randint(-6, 6), r.randint(-10, 10)
        D = (b - k) ** 2 - 4 * (c - m)
        if D > 0 and is_sq(D):
            break
    sq = math.isqrt(D)
    x1, x2 = F(k - b - sq, 2), F(k - b + sq, 2)
    y1, y2 = k * x1 + m, k * x2 + m
    ask = r.choice(["ysum", "xprod"])
    ans = y1 + y2 if ask == "ysum" else x1 * x2
    rr = real_roots([1, b - k, c - m])
    chk = sum(k * x + m for x in rr) if ask == "ysum" else rr[0] * rr[1]
    w = "kəsişmə nöqtələrinin ordinatlarının cəmini" if ask == "ysum" else "kəsişmə nöqtələrinin absislərinin hasilini"
    return dict(t=f"y = {poly([1, b, c])} parabolası ilə y = {poly([k, m])} düz xəttinin {w} tapın.",
                a=ans, d=[x1 + x2, y1 * y2 if ask == "ysum" else -ans, ans + k, ans - 1, ans + 1],
                e=f"{poly([1, b - k, c - m])} = 0 ⇒ x₁ = {show(x1)}, x₂ = {show(x2)}; y = {poly([k, m])}: y₁ = {show(y1)}, y₂ = {show(y2)}. Cavab: {show(ans)}.",
                chk=chk, diff=H)


TOPICS = {
    "alg-eq": {9: [eq_rational, eq_sqrt, eq_work, eq_biquad],
               10: [eq_rational, eq_boat, eq_biquad, eq_sqrt, eq_work],
               11: [eq_subst, eq_log, eq_sqrt, eq_rational, eq_boat]},
    "alg-sys": {9: [sys_tickets, sys_sym, sys_diffsq, sys_linear],
                10: [sys_sym, sys_param, sys_diffsq, sys_tickets, sys_linear],
                11: [sys_param, sys_three, sys_recip, sys_sym]},
    "alg-quad": {9: [quad_vieta, quad_ineq_count, quad_new_eq, quad_ratio_param],
                 10: [quad_vieta, quad_ratio_param, quad_ineq_count, quad_param_min, quad_new_eq],
                 11: [quad_vieta, quad_both_pos, quad_param_min, quad_ratio_param, quad_new_eq]},
    "alg-prog": {9: [seq_ap, seq_gp, seq_multiples, seq_fib],
                 10: [seq_inf, seq_recur, seq_quadterm, seq_ap, seq_gp, seq_fib],
                 11: [seq_ap_gp, seq_sn, seq_inf, seq_recur, seq_quadterm, seq_multiples]},
    "alg-func": {9: [fn_comp_eq, fn_shifted, fn_domain, fn_intersect],
                 10: [fn_inverse, fn_range_interval, fn_domain, fn_comp_eq, fn_shifted],
                 11: [fn_functional, fn_odd_periodic, fn_range_interval, fn_inverse, fn_intersect]},
}
