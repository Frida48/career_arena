"""11-ci sinif riyaziyyat: 4 bölmə × 30 sual (kodla yaradılır, cavablar hesablanır)."""
import math
from fractions import Fraction as F
from common import build_section, save, fr, cop, dat, abl
from math10 import sgn

# ---------- 1. Üstlü və loqarifmik ifadələr ----------


def log_sum(r):
    base1 = r.choice([2, 3, 5])
    k1 = r.randint(2, 5 if base1 == 2 else 4 if base1 == 3 else 3)
    base2 = r.choice([b for b in [2, 3, 4, 10] if b != base1])
    k2 = r.randint(1, 3)
    return dict(t=f"Hesablayın: log{_sub(base1)} {base1 ** k1} + log{_sub(base2)} {base2 ** k2}",
                a=k1 + k2, d=[k1 * k2, base1 ** k1 + base2 ** k2, k1 + k2 + 1, abs(k1 - k2)],
                e=f"log{_sub(base1)} {base1 ** k1} = {k1}, log{_sub(base2)} {base2 ** k2} = {k2}. Cəm: {k1 + k2}.",
                topic="Loqarifm", diff="easy")


def log_props(r):
    base = r.choice([2, 3, 6])
    k = r.randint(2, 4)
    x = r.choice([d for d in range(2, 30) if (base ** k) % d == 0 and d not in (1, base ** k)])
    y = base ** k // x
    return dict(t=f"Hesablayın: log{_sub(base)} {x} + log{_sub(base)} {y}",
                a=k, d=[k + 1, x + y, F(x, y), k - 1],
                e=f"log a + log b = log(ab): log{_sub(base)} ({x}·{y}) = log{_sub(base)} {base ** k} = {k}.",
                topic="Loqarifmin xassələri", diff="medium")


def exp_eq(r):
    a = r.choice([2, 3, 5])
    x = r.randint(-3, 5)
    b = r.randint(-3, 4)
    c = x + b
    return dict(t=f"{a}^(x{sgn(b)}) = {fr(F(a) ** c)} tənliyini həll edin.",
                a=x, d=[c, x + 1, -x, c + b],
                e=f"{fr(F(a) ** c)} = {a}^{c} ⇒ x{sgn(b)} = {c} ⇒ x = {x}.",
                topic="Üstlü tənliklər", diff="medium")


def log_eq(r):
    a = r.choice([2, 3])
    c = r.randint(1, 4)
    b = r.randint(-5, 6)
    x = a ** c - b
    return dict(t=f"log{_sub(a)} (x{sgn(b)}) = {c} tənliyini həll edin.",
                a=x, d=[a ** c, a * c - b, x + b, c - b],
                e=f"x{sgn(b)} = {a}^{c} = {a ** c} ⇒ x = {x}.",
                topic="Loqarifmik tənliklər", diff="medium")


def exp_ineq(r):
    a = r.choice([2, 3])
    k = r.randint(2, 5)
    b = r.randint(-3, 3)
    # a^(x+b) > a^k  ⇒ x > k - b, ən kiçik tam: k - b + 1
    return dict(t=f"{a}^(x{sgn(b)}) > {a ** k} bərabərsizliyinin ən kiçik tam həllini tapın.",
                a=k - b + 1, d=[k - b, k + b + 1, k, k - b - 1],
                e=f"{a ** k} = {a}^{k}; əsas > 1 ⇒ x{sgn(b)} > {k} ⇒ x > {k - b}. Ən kiçik tam həll: {k - b + 1}.",
                topic="Üstlü bərabərsizliklər", diff="hard")


def log_identity(r):
    a = r.choice([2, 3, 5, 7])
    b = r.randint(3, 15)
    k = r.choice([2, 3])
    return dict(t=f"Hesablayın: {a}^(log{_sub(a)} {b}) + log{_sub(a)} {a ** k}",
                a=b + k, d=[b * k, a + b, b, a * b + k],
                e=f"a^(logₐ b) = b ⇒ {b}; log{_sub(a)} {a ** k} = {k}. Cəm: {b + k}.",
                topic="Loqarifmin xassələri", diff="medium")


def _p(n):
    return f"({n})" if n < 0 else str(n)


def _c(v):
    """Kəsr əmsalı mötərizədə: (3/2)"""
    v = F(v)
    return fr(v) if v.denominator == 1 else f"({fr(v)})"


def pi(v):
    """12 → 12π, 500/3 → 500π/3"""
    v = F(v)
    return f"{v.numerator}π" if v.denominator == 1 else f"{v.numerator}π/{v.denominator}"


def _sub(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


# ---------- 2. Törəmə ----------

def poly_str(coefs):
    """coefs: [(c, p)] → '2x³ − 3x² + 5'"""
    out = ""
    for c, p in coefs:
        if c == 0:
            continue
        var = "" if p == 0 else ("x" if p == 1 else f"x{'⁰¹²³⁴⁵⁶⁷⁸⁹'[p]}")
        mag = abs(c)
        coef = "" if (mag == 1 and p != 0) else str(mag)
        sign = ("−" if c < 0 else "") if not out else (" − " if c < 0 else " + ")
        out += f"{sign}{coef}{var}"
    return out


def deriv_at(r):
    a, b, c = r.randint(1, 4), r.randint(-5, 5), r.randint(-6, 6)
    x0 = r.randint(-2, 3)
    v = 3 * a * x0 * x0 + 2 * b * x0 + c
    return dict(t=f"f(x) = {poly_str([(a, 3), (b, 2), (c, 1), (r.randint(1, 9), 0)])} olarsa, f′({x0}) neçədir?",
                a=v, d=[a * x0 ** 3 + b * x0 ** 2 + c * x0, v + c, 3 * a * x0 + 2 * b + c, -v],
                e=f"f′(x) = {poly_str([(3 * a, 2), (2 * b, 1), (c, 0)])}; f′({x0}) = {v}.",
                topic="Törəmə", diff="easy")


def tangent_slope(r):
    a, b = r.choice([1, 2, -1, 3]), r.randint(-6, 6)
    x0 = r.randint(-3, 3)
    k = 2 * a * x0 + b
    return dict(t=f"y = {poly_str([(a, 2), (b, 1), (r.randint(-5, 5) or 1, 0)])} funksiyasının qrafikinə absisi x₀ = {x0} olan nöqtədə çəkilmiş toxunanın bucaq əmsalını tapın.",
                a=k, d=[a * x0 * x0 + b * x0, k + b, -k, 2 * a + b],
                e=f"Bucaq əmsalı k = y′(x₀). y′ = {2 * a}x{sgn(b)}, y′({x0}) = {k}.",
                topic="Toxunan", diff="medium")


def cubic_extremum(r):
    k = r.randint(1, 5)
    ask_max = r.random() < 0.5
    # f = x³ − 3k²x ⇒ f′ = 3x² − 3k² ⇒ x = ±k; maksimum x = −k, minimum x = k
    return dict(t=f"f(x) = x³ − {3 * k * k}x funksiyasının {'maksimum' if ask_max else 'minimum'} nöqtəsini tapın.",
                a=-k if ask_max else k, d=[k if ask_max else -k, 3 * k * k, k * k, 0, -k * k],
                e=f"f′(x) = 3x² − {3 * k * k} = 0 ⇒ x = ±{k}. f′ işarəsi «+ − +» olduğundan maksimum x = −{k}, minimum x = {k}.",
                topic="Ekstremum", diff="hard")


def velocity(r):
    a, b, c = r.randint(1, 3), r.randint(-4, 6), r.randint(0, 9)
    t0 = r.randint(1, 5)
    v = 2 * a * t0 + b
    return dict(t=f"Nöqtə s(t) = {poly_str([(a, 2), (b, 1), (c, 0)])} (m) qanunu ilə hərəkət edir. t = {t0} s anında sürəti tapın (m/s).",
                a=v, d=[a * t0 * t0 + b * t0 + c, 2 * a, v + c, a * t0 + b],
                e=f"v(t) = s′(t) = {2 * a}t{sgn(b)}; v({t0}) = {v} m/s.",
                topic="Törəmənin fiziki mənası", diff="medium")


def quad_max_interval(r):
    a = r.choice([1, 2])
    h = r.randint(-2, 3)
    lo, hi = h - r.randint(1, 3), h + r.randint(1, 4)
    k = r.randint(-5, 5)
    b, c = 2 * a * h, -a * h * h + k  # f = −a x² + 2ah x + c ⇒ təpə x = h
    f = lambda x: -a * x * x + b * x + c
    return dict(t=f"f(x) = {poly_str([(-a, 2), (b, 1), (c, 0)])} funksiyasının [{lo}; {hi}] parçasında ən böyük qiymətini tapın.",
                a=f(h), d=[f(lo), f(hi), h, c],
                e=f"f′(x) = {-2 * a}x{sgn(b)} = 0 ⇒ x = {h} ∈ [{lo}; {hi}]. f({h}) = {f(h)}, uclarda: f({lo}) = {f(lo)}, f({hi}) = {f(hi)}.",
                topic="Ən böyük və ən kiçik qiymət", diff="hard")


def power_rule(r):
    n = r.randint(3, 7)
    c = r.randint(2, 5)
    x0 = r.choice([1, -1, 2])
    v = c * n * x0 ** (n - 1)
    return dict(t=f"f(x) = {c}x{'⁰¹²³⁴⁵⁶⁷⁸⁹'[n]} olarsa, f′({x0}) neçədir?",
                a=v, d=[c * x0 ** n, n * x0 ** (n - 1), c * (n - 1) * x0 ** (n - 2), v + c],
                e=f"f′(x) = {c * n}x{'⁰¹²³⁴⁵⁶⁷⁸⁹'[n - 1]}; f′({x0}) = {v}.",
                topic="Törəmə", diff="easy")


# ---------- 3. İnteqral ----------

def definite_linear(r):
    c, d = r.randint(1, 6), r.randint(-4, 5)
    a, b = r.randint(-1, 2), r.randint(3, 6)
    v = F(c, 2) * (b * b - a * a) + d * (b - a)
    return dict(t=f"Hesablayın: ∫ ({c if c != 1 else ''}x{sgn(d)}) dx, sərhədlər {abl(a)} {dat(b)} qədər.",
                a=v, d=[c * (b - a) + d, F(c, 2) * b * b + d * b, v + d, c * (b * b - a * a) + d * (b - a)],
                e=f"İbtidai funksiya: {_c(F(c, 2))}x²{sgn(d, 'x')}. F({b}) − F({a}) = {fr(v)}.",
                topic="Müəyyən inteqral", diff="medium")


def antiderivative(r):
    a, b = r.choice([3, 6, 9]), r.choice([2, 4, -2, 6])
    k = r.randint(-5, 5)
    x1 = r.choice([1, 2])
    # f = a x² + b x ⇒ F = a/3 x³ + b/2 x² + C, F(0) = k
    v = F(a, 3) * x1 ** 3 + F(b, 2) * x1 ** 2 + k
    return dict(t=f"f(x) = {a}x²{sgn(b, 'x')} funksiyasının F(0) = {k} şərtini ödəyən ibtidai funksiyası üçün F({x1}) neçədir?",
                a=v, d=[v - k, a * x1 ** 2 + b * x1 + k, v + 1, 2 * a * x1 + b],
                e=f"F(x) = {_c(F(a, 3))}x³{sgn(F(b, 2), 'x²')}{sgn(k)}. F({x1}) = {fr(v)}.",
                topic="İbtidai funksiya", diff="hard")


def area_parabola(r):
    a = r.choice([3, 6, 9])
    v = F(a ** 3, 3)
    return dict(t=f"y = x² parabolası, x = 0, x = {a} düz xətləri və absis oxu ilə hüdudlanmış fiqurun sahəsini tapın.",
                a=v, d=[a * a, F(a ** 3, 2), a ** 3, F(a * a, 3)],
                e=f"S = ∫₀^{a} x² dx = {a}³/3 = {fr(v)}.",
                topic="Əyrixətli trapesiyanın sahəsi", diff="medium")


def integral_kx2(r):
    k, a = r.choice([3, 6, 9, 12]), r.randint(1, 3)
    v = F(k, 3) * a ** 3
    return dict(t=f"Hesablayın: ∫ {k}x² dx, sərhədlər 0-dan {dat(a)} qədər.",
                a=v, d=[k * a * a, 2 * k * a, k * a ** 3, v + k],
                e=f"∫ {k}x² dx = {_c(F(k, 3))}x³; 0-dan {dat(a)}: {fr(v)}.",
                topic="Müəyyən inteqral", diff="easy")


def area_between(r):
    k = r.choice([1, 2, 3, 6])
    v = F(k ** 3, 6)
    return dict(t=f"y = x² və y = {k if k != 1 else ''}x xətləri ilə hüdudlanmış fiqurun sahəsini tapın.",
                a=v, d=[F(k ** 3, 3), F(k ** 3, 2), F(k * k, 2), F(k ** 3, 6) + 1],
                e=f"Kəsişmə: x = 0 və x = {k}. S = ∫₀^{k} ({k}x − x²) dx = {k}³/2 − {k}³/3 = {fr(v)}.",
                topic="Fiqurların sahəsi", diff="hard")


def integral_poly(r):
    a = r.randint(1, 3)
    v = a ** 3 + a ** 2  # ∫0^a (3x² + 2x) dx
    return dict(t=f"Hesablayın: ∫ (3x² + 2x) dx, sərhədlər 0-dan {dat(a)} qədər.",
                a=v, d=[3 * a * a + 2 * a, a ** 3, v + a, 6 * a + 2],
                e=f"İbtidai funksiya x³ + x²; 0-dan {dat(a)}: {a ** 3} + {a ** 2} = {v}.",
                topic="Müəyyən inteqral", diff="easy")


# ---------- 4. Fəza həndəsəsi və vektorlar ----------

QUADS = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (2, 6, 9, 11), (4, 4, 7, 9), (3, 4, 12, 13), (2, 10, 11, 15)]


def box_diag(r):
    a, b, c, d = r.choice(QUADS)
    return dict(t=f"Düzbucaqlı paralelepipedin ölçüləri {a}, {b} və {cop(c)}. Diaqonalını tapın.",
                a=d, d=[a + b + c, d + 1, d - 1, a * b * c],
                e=f"d = √({a}² + {b}² + {c}²) = √{a * a + b * b + c * c} = {d}.",
                topic="Paralelepiped", diff="easy")


def cube(r):
    a = r.randint(2, 9)
    if r.random() < 0.5:
        return dict(t=f"Tilinin uzunluğu {a} olan kubun diaqonalını tapın.",
                    a=f"{a}√3", d=[f"{a}√2", f"{3 * a}", f"{a * a}√3", f"√{3 * a}", f"{a}"],
                    e=f"Kubun diaqonalı d = a√3 = {a}√3.", topic="Kub", diff="easy")
    return dict(t=f"Tilinin uzunluğu {a} olan kubun tam səthinin sahəsini tapın.",
                a=6 * a * a, d=[a ** 3, 4 * a * a, 6 * a, 12 * a],
                e=f"S = 6a² = 6·{a * a} = {6 * a * a}.", topic="Kub", diff="easy")


def cylinder(r):
    rad, h = r.randint(2, 6), r.randint(3, 10)
    return dict(t=f"Silindrin oturacağının radiusu {rad}, hündürlüyü {cop(h)}. Həcmini tapın.",
                a=pi(rad * rad * h), d=[pi(2 * rad * h), pi(rad * h), pi(rad * rad * h * 2), pi(F(rad * rad * h, 3)), pi(rad * rad * h + rad)],
                e=f"V = πr²h = π·{rad * rad}·{h} = {rad * rad * h}π.", topic="Silindr", diff="easy")


def cone(r):
    rad, h = r.choice([3, 6]), r.randint(2, 8)
    v = F(rad * rad * h, 3)
    return dict(t=f"Konusun oturacağının radiusu {rad}, hündürlüyü {cop(h)}. Həcmini tapın.",
                a=pi(v), d=[pi(rad * rad * h), pi(v * 2), pi(rad * h), pi(v + 1), pi(v + 2)],
                e=f"V = (1/3)πr²h = (1/3)·π·{rad * rad}·{h} = {pi(v)}.", topic="Konus", diff="medium")


def sphere(r):
    rad = r.randint(2, 7)
    if r.random() < 0.5:
        return dict(t=f"Radiusu {rad} olan kürənin səthinin sahəsini tapın.",
                    a=pi(4 * rad * rad), d=[pi(rad * rad), pi(2 * rad * rad), pi(F(4 * rad ** 3, 3)), pi(4 * rad), pi(8 * rad * rad)],
                    e=f"S = 4πR² = {4 * rad * rad}π.", topic="Kürə", diff="easy")
    return dict(t=f"Radiusu {rad} olan kürənin həcmini tapın.",
                a=f"{fr(F(4 * rad ** 3, 3))}π", d=[f"{4 * rad * rad}π", f"{rad ** 3}π", f"{fr(F(rad ** 3, 3))}π", f"{4 * rad ** 3}π"],
                e=f"V = (4/3)πR³ = (4/3)·{rad ** 3}π = {fr(F(4 * rad ** 3, 3))}π.", topic="Kürə", diff="medium")


def vectors(r):
    a = (r.randint(-4, 5), r.randint(-4, 5), r.randint(-3, 4))
    b = (r.randint(-4, 5), r.randint(-4, 5), r.randint(-3, 4))
    if r.random() < 0.5:
        dot = sum(x * y for x, y in zip(a, b))
        return dict(t=f"a⃗({a[0]}; {a[1]}; {a[2]}) və b⃗({b[0]}; {b[1]}; {b[2]}) vektorlarının skalyar hasilini tapın.",
                    a=dot, d=[dot + 1, -dot, sum(a) + sum(b), sum(x - y for x, y in zip(a, b))],
                    e=f"a⃗·b⃗ = " + " + ".join(f"{_p(x)}·{_p(y)}" for x, y in zip(a, b)) + f" = {dot}.",
                    topic="Vektorlar", diff="medium")
    x, y, z, d = r.choice(QUADS)
    return dict(t=f"a⃗({x}; {-y}; {z}) vektorunun uzunluğunu tapın.",
                a=d, d=[x + y + z, x - y + z, d + 2, d * d],
                e=f"|a⃗| = √({x}² + {y}² + {z}²) = √{d * d} = {d}.", topic="Vektorlar", diff="easy")


SECTIONS = [
    ("exp-log", "Üstlü və loqarifmik funksiyalar", [log_sum, log_props, exp_eq, log_eq, exp_ineq, log_identity],
     "Loqarifm və onun xassələri, üstlü və loqarifmik tənliklər, bərabərsizliklər."),
    ("derivative", "Törəmə və tətbiqləri", [deriv_at, tangent_slope, cubic_extremum, velocity, quad_max_interval, power_rule],
     "Törəmə qaydaları, toxunan, ekstremum, ən böyük qiymət və törəmənin fiziki mənası."),
    ("integral", "İbtidai funksiya və inteqral", [definite_linear, antiderivative, area_parabola, integral_kx2, area_between, integral_poly],
     "İbtidai funksiya, müəyyən inteqral və fiqurların sahəsinin hesablanması."),
    ("solid-geometry", "Fəza həndəsəsi və vektorlar", [box_diag, cube, cylinder, cone, sphere, vectors],
     "Paralelepiped, kub, silindr, konus, kürə və fəzada vektorlar."),
]

if __name__ == "__main__":
    out = []
    for k, (sid, title, tpls, desc) in enumerate(SECTIONS):
        out.append((sid, title, build_section(11, "math", sid, title, tpls, seed=1100 + k), desc))
    save(11, "math", out)
