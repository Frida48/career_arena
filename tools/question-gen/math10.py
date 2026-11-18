"""10-cu sinif riyaziyyat: 4 bölmə × 30 sual (kodla yaradılır, cavablar hesablanır)."""
import math
from fractions import Fraction as F
from common import build_section, save, fr, cop, dat, abl
from math9 import TRIPLES


def sgn(k, s=""):
    """' + 3x' / ' − 3x' formatı (k=0 olduqda boş)."""
    if k == 0:
        return ""
    coef = "" if abs(k) == 1 and s else str(abs(k))
    return f" {'+' if k > 0 else '−'} {coef}{s}"


def poly2(a, b, c, var="x"):
    lead = {1: f"{var}²", -1: f"−{var}²"}.get(a, f"{a}{var}²")
    return f"{lead}{sgn(b, var)}{sgn(c)}"


# ---------- 1. Tənliklər və bərabərsizliklər ----------

def quad_ineq_count(r):
    p = r.randint(-6, 2)
    q = p + r.randint(3, 8)
    b, c = -(p + q), p * q
    strict = r.random() < 0.5
    n = (q - p - 1) if strict else (q - p + 1)
    sign = "<" if strict else "≤"
    return dict(t=f"{poly2(1, b, c)} {sign} 0 bərabərsizliyinin neçə tam həlli var?",
                a=n, d=[q - p, n + 2, q - p - 1 if not strict else q - p + 1, abs(p) + abs(q)],
                e=f"Köklər {p} və {q}. Həllər çoxluğu {'(' if strict else '['}{p}; {q}{')' if strict else ']'}, tam həllər sayı {n}.",
                topic="Kvadrat bərabərsizlik", diff="medium")


def other_root(r):
    x1, x2 = r.randint(-6, 7), r.randint(-6, 7)
    while x1 == x2 or x1 == 0:
        x1 = r.randint(-6, 7)
    b, c = -(x1 + x2), x1 * x2
    return dict(t=f"x² + bx {'+' if c >= 0 else '−'} {abs(c)} = 0 tənliyinin bir kökü {cop(x1)}. b-ni tapın.",
                a=b, d=[-b, x2, -x2, c],
                e=f"x₁·x₂ = {c} ⇒ x₂ = {c} : {x1} = {x2}. b = −(x₁ + x₂) = {b}.",
                topic="Viyet teoremi", diff="hard")


def abs_eq(r):
    a, b = r.randint(-5, 6), r.randint(1, 8)
    return dict(t=f"|x {'−' if a >= 0 else '+'} {abs(a)}| = {b} tənliyinin köklərinin cəmini tapın.",
                a=2 * a, d=[a, 2 * b, a + b, -2 * a],
                e=f"x = {a} + {b} = {a + b} və ya x = {a} − {b} = {a - b}. Cəm: {2 * a}.",
                topic="Modullu tənliklər", diff="medium")


def irrational_eq(r):
    x = r.randint(-3, 20)
    a = r.randint(1, 9)
    while x + a < 0 or not math.isqrt(x + a) ** 2 == x + a:
        x = r.randint(-3, 20)
        a = r.randint(1, 9)
    b = math.isqrt(x + a)
    return dict(t=f"√(x + {a}) = {b} tənliyini həll edin.",
                a=x, d=[b * b, b - a, x + 1, b + a],
                e=f"Hər iki tərəfi kvadrata yüksəldirik: x + {a} = {b * b} ⇒ x = {x}.",
                topic="İrrasional tənliklər", diff="medium")


def sym_system(r):
    x, y = r.randint(1, 7), r.randint(-4, 7)
    s, p = x + y, x * y
    return dict(t=f"x + y = {s} və xy = {p} olarsa, x² + y² neçədir?",
                a=s * s - 2 * p, d=[s * s, s * s + 2 * p, s * s - p, 2 * s * p],
                e=f"x² + y² = (x + y)² − 2xy = {s * s} − {2 * p} = {s * s - 2 * p}.",
                topic="Tənliklər sistemi", diff="medium")


def rational_eq(r):
    x = r.randint(-5, 9)
    a = r.randint(1, 6)
    while x + a == 0:
        x = r.randint(-5, 9)
    k = r.choice([2, 3, 4, 5])
    rhs = k * (x + a)
    # (k x + rhs - k x ... ) sadə: rhs/(x+a) = k
    return dict(t=f"{rhs}/(x + {a}) = {k} tənliyini həll edin.",
                a=x, d=[F(rhs, k), F(rhs, k) + a, -x, x + a],
                e=f"x + {a} = {rhs} : {k} = {F(rhs, k)} ⇒ x = {x} (x ≠ −{a}).",
                topic="Kəsr-rasional tənliklər", diff="easy")


# ---------- 2. Funksiyalar ----------

def quad_min(r):
    a = r.choice([1, 2, 3])
    h, k = r.randint(-4, 4), r.randint(-9, 9)
    b, c = -2 * a * h, a * h * h + k
    return dict(t=f"y = {poly2(a, b, c)} funksiyasının ən kiçik qiymətini tapın.",
                a=k, d=[h, c, -k, k + a],
                e=f"Təpə nöqtəsi: x₀ = −b/(2a) = {h}, y(x₀) = {k}. a > 0 olduğu üçün bu ən kiçik qiymətdir.",
                topic="Kvadrat funksiya", diff="medium")


def inverse_linear(r):
    a = r.choice([2, 3, 4, 5, -2])
    b = r.randint(-7, 7)
    x = r.randint(-4, 6)
    k = a * x + b
    return dict(t=f"f(x) = {a}x{sgn(b)} funksiyası üçün f⁻¹({k}) qiymətini tapın.",
                a=x, d=[a * k + b, F(k + b, a), -x, k],
                e=f"f(x) = {k} ⇒ {a}x = {k - b} ⇒ x = {x}. Deməli, f⁻¹({k}) = {x}.",
                topic="Tərs funksiya", diff="medium")


def composition(r):
    a, b = r.choice([1, 2, 3]), r.randint(-4, 4)
    c = r.randint(-3, 5)
    k = r.randint(-3, 3)
    g = k * k + c
    v = a * g + b
    return dict(t=f"f(x) = {a if a != 1 else ''}x{sgn(b)} və g(x) = x²{sgn(c)} olarsa, f(g({k})) neçədir?",
                a=v, d=[(a * k + b) ** 2 + c, g, v + c, a * k * k + b],
                e=f"g({k}) = {g}; f({g}) = {a}·{g}{sgn(b)} = {v}.",
                topic="Mürəkkəb funksiya", diff="medium")


def abs_min(r):
    a, b = r.randint(-5, 5), r.randint(-6, 6)
    return dict(t=f"y = |x {'−' if a >= 0 else '+'} {abs(a)}|{sgn(b)} funksiyasının ən kiçik qiymətini tapın.",
                a=b, d=[a, -b, a + b, 0 if b != 0 else 1],
                e=f"|x − {a}| ≥ 0, ən kiçik qiyməti 0-dır (x = {a}). Deməli, ymin = {b}.",
                topic="Modullu funksiya", diff="easy")


def linear_from_points(r):
    a, b = r.choice([2, 3, -2, 4]), r.randint(-5, 6)
    k = r.randint(3, 8)
    return dict(t=f"f(x) = ax + b xətti funksiyası üçün f(1) = {a + b} və f(2) = {2 * a + b}. f({k}) neçədir?",
                a=a * k + b, d=[a * k, k + b, a + b * k, a * k - b],
                e=f"a = f(2) − f(1) = {a}, b = {b}. f({k}) = {a}·{k}{sgn(b)} = {a * k + b}.",
                topic="Xətti funksiya", diff="easy")


def domain_count(r):
    a = r.randint(-5, 3)
    b = a + r.randint(2, 9)
    left = "x" if a == 0 else f"x {'−' if a > 0 else '+'} {abs(a)}"
    right = "−x" if b == 0 else f"{b} − x"
    return dict(t=f"y = √({left}) + √({right}) funksiyasının təyin oblastında neçə tam ədəd var?",
                a=b - a + 1, d=[b - a, b - a - 1, b + a, b - a + 2],
                e=f"x − ({a}) ≥ 0 və {b} − x ≥ 0 ⇒ x ∈ [{a}; {b}]. Tam ədədlər: {b - a + 1}.",
                topic="Təyin oblastı", diff="medium")


# ---------- 3. Triqonometriya ----------

def rad_str(deg):
    k = F(deg, 180)
    if k == 1:
        return "π"
    if k.denominator == 1:
        return f"{k.numerator}π"
    num = "" if k.numerator == 1 else str(k.numerator)
    return f"{num}π/{k.denominator}"


def deg_to_rad(r):
    deg = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330])
    wrong = [d for d in [30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300, 330] if d != deg]
    r.shuffle(wrong)
    return dict(t=f"{deg}° bucağın radian ölçüsünü tapın.",
                a=rad_str(deg), d=[rad_str(d) for d in wrong[:6]],
                e=f"{deg}° = {deg}·π/180 = {rad_str(deg)}.",
                topic="Radian ölçü", diff="easy")


TRIG = {  # rasional qiymətlər
    "sin 30°": F(1, 2), "cos 60°": F(1, 2), "sin 90°": F(1), "cos 0°": F(1), "cos 180°": F(-1),
    "sin 150°": F(1, 2), "cos 120°": F(-1, 2), "sin 270°": F(-1), "tg 45°": F(1), "tg 135°": F(-1),
    "sin² 45°": F(1, 2), "cos² 30°": F(3, 4), "sin² 60°": F(3, 4), "tg² 60°": F(3), "ctg 45°": F(1),
    "sin 210°": F(-1, 2), "cos 240°": F(-1, 2), "cos 360°": F(1),
}


def special_angles(r):
    (n1, v1), (n2, v2) = r.sample(list(TRIG.items()), 2)
    a, b = r.choice([1, 2, 3, 4]), r.choice([1, 2, -2, 3, 6])
    val = a * v1 + b * v2
    t1 = n1 if a == 1 else f"{a}·{n1}"
    t2 = f"{'+' if b > 0 else '−'} {'' if abs(b) == 1 else str(abs(b)) + '·'}{n2}"
    return dict(t=f"Hesablayın: {t1} {t2}",
                a=val, d=[a * v1 - b * v2, val + 1, -val, a * v1, b * v2],
                e=f"{n1} = {fr(v1)}, {n2} = {fr(v2)}. Nəticə: {a}·{fr(v1)} + ({b})·{fr(v2)} = {fr(val)}.",
                topic="Xüsusi bucaqların triqonometrik funksiyaları", diff="medium")


def sin_to_cos(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    if r.random() < 0.5:
        a, b = b, a
    ask = r.choice(["cos", "tg"])
    if ask == "cos":
        return dict(t=f"sin α = {a}/{c} və α — I rüb bucağıdır. cos α-nı tapın.",
                    a=F(b, c), d=[F(a, c), F(-b, c), F(a, b), F(c, b)],
                    e=f"cos α = √(1 − sin²α) = √(1 − {a * a}/{c * c}) = {b}/{c}.",
                    topic="Əsas triqonometrik eynilik", diff="medium")
    return dict(t=f"sin α = {a}/{c} və α — II rüb bucağıdır. tg α-nı tapın.",
                a=F(-a, b), d=[F(a, b), F(b, a), F(-b, a), F(a, c)],
                e=f"II rübdə cos α < 0: cos α = −{b}/{c}. tg α = sin α / cos α = −{a}/{b}.",
                topic="Əsas triqonometrik eynilik", diff="hard")


def double_angle(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    v = F(2 * a * b, c * c)
    return dict(t=f"sin α = {a}/{c}, cos α = {b}/{c} olarsa, sin 2α-nı tapın.",
                a=v, d=[F(2 * a, c), F(a * b, c * c), F(b * b - a * a, c * c), F(a + b, c)],
                e=f"sin 2α = 2 sin α cos α = 2·{a}/{c}·{b}/{c} = {fr(v)}.",
                topic="İkiqat bucaq düsturları", diff="medium")


def cos_theorem(r):
    a, b = r.randint(3, 9), r.randint(3, 9)
    ang = r.choice([60, 120])
    c2 = a * a + b * b - (a * b if ang == 60 else -a * b)
    return dict(t=f"Üçbucağın iki tərəfi {a} və {b}, onlar arasındakı bucaq {ang}°-dir. Üçüncü tərəfin kvadratını tapın.",
                a=c2, d=[a * a + b * b, a * a + b * b + (a * b if ang == 60 else -a * b), (a + b) ** 2, c2 + a],
                e=f"c² = a² + b² − 2ab·cos {ang}° = {a * a} + {b * b} {'−' if ang == 60 else '+'} {a * b} = {c2}.",
                topic="Kosinuslar teoremi", diff="hard")


def reduction(r):
    pairs = [("sin(180° − α)", "sin α"), ("cos(180° − α)", "−cos α"), ("sin(90° + α)", "cos α"),
             ("cos(90° + α)", "−sin α"), ("tg(180° + α)", "tg α"), ("cos(360° − α)", "cos α"),
             ("sin(360° − α)", "−sin α"), ("cos(180° + α)", "−cos α")]
    expr, ans = r.choice(pairs)
    pool = ["sin α", "−sin α", "cos α", "−cos α", "tg α", "−tg α", "ctg α"]
    return dict(t=f"Sadələşdirin: {expr}",
                a=ans, d=[p for p in pool if p != ans],
                e=f"Çevirmə düsturuna görə {expr} = {ans}.",
                topic="Çevirmə düsturları", diff="medium")


# ---------- 4. Həndəsə və kombinatorika ----------

def polygon_sum(r):
    n = r.randint(5, 14)
    return dict(t=f"Qabarıq {n}-bucaqlının daxili bucaqlarının cəmini tapın (dərəcə ilə).",
                a=180 * (n - 2), d=[180 * n, 180 * (n - 1), 360 * (n - 2), 180 * (n - 3)],
                e=f"S = 180°·(n − 2) = 180°·{n - 2} = {180 * (n - 2)}°.",
                topic="Çoxbucaqlılar", diff="easy")


def regular_angle(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    ask_ext = r.random() < 0.4
    if ask_ext:
        return dict(t=f"Düzgün {n}-bucaqlının xarici bucağını tapın (dərəcə ilə).",
                    a=F(360, n), d=[F(180 * (n - 2), n), F(180, n), F(360, n - 2), F(360, n) + 10],
                    e=f"Düzgün çoxbucaqlının xarici bucağı 360°/n = {fr(F(360, n))}°.",
                    topic="Çoxbucaqlılar", diff="easy")
    return dict(t=f"Düzgün {n}-bucaqlının bir daxili bucağını tapın (dərəcə ilə).",
                a=F(180 * (n - 2), n), d=[F(360, n), F(180 * n, n - 2), 180 * (n - 2), F(180 * (n - 1), n)],
                e=f"180°·(n − 2)/n = 180°·{n - 2}/{n} = {fr(F(180 * (n - 2), n))}°.",
                topic="Çoxbucaqlılar", diff="medium")


def inscribed(r):
    c = r.choice([40, 50, 64, 70, 80, 96, 110, 130, 140])
    if r.random() < 0.5:
        return dict(t=f"Çevrənin mərkəzi bucağı {c}°-dir. Həmin qövsə söykənən daxilə çəkilmiş bucağı tapın.",
                    a=c // 2, d=[c, 2 * c, 180 - c, 90 - c // 2],
                    e=f"Daxilə çəkilmiş bucaq eyni qövsə söykənən mərkəzi bucağın yarısına bərabərdir: {c // 2}°.",
                    topic="Çevrə və bucaqlar", diff="easy")
    return dict(t=f"Çevrəyə daxilə çəkilmiş bucaq {c // 2}°-dir. Həmin qövsə söykənən mərkəzi bucağı tapın.",
                a=c, d=[c // 2, 180 - c // 2, 2 * c, 90 + c // 2],
                e=f"Mərkəzi bucaq daxilə çəkilmiş bucağın iki mislidir: {c}°.",
                topic="Çevrə və bucaqlar", diff="easy")


def combinations(r):
    n, k = r.randint(5, 10), r.choice([2, 3])
    c = math.comb(n, k)
    return dict(t=f"{n} şagirddən {k} nəfərlik nümayəndə heyətini neçə üsulla seçmək olar?",
                a=c, d=[math.perm(n, k), n * k, c + n, math.comb(n, k + 1)],
                e=f"Sıra əhəmiyyətsizdir — kombinasiya: C({n}; {k}) = {c}.",
                topic="Kombinatorika", diff="medium")


def arrangements(r):
    n, k = r.randint(5, 9), r.choice([2, 3])
    a = math.perm(n, k)
    return dict(t=f"{n} iştirakçı arasında I, II{' və III' if k == 3 else ''} yerləri neçə üsulla bölüşdürmək olar?",
                a=a, d=[math.comb(n, k), n ** k, a // 2, math.factorial(n)],
                e=f"Sıra əhəmiyyətlidir — yerləşdirmə: A({n}; {k}) = {a}.",
                topic="Kombinatorika", diff="medium")


def dice(r):
    s = r.randint(3, 11)
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
    p = F(ways, 36)
    return dict(t=f"İki zər atılır. Düşən xalların cəminin {s} olması ehtimalını tapın.",
                a=p, d=[F(1, 6), F(ways, 12), F(s, 36), F(ways + 1, 36), F(1, 36)],
                e=f"Əlverişli hallar: {ways}, bütün hallar: 36. P = {fr(p)}.",
                topic="Ehtimal", diff="medium")


SECTIONS = [
    ("equations", "Tənliklər və bərabərsizliklər", [quad_ineq_count, other_root, abs_eq, irrational_eq, sym_system, rational_eq],
     "Kvadrat bərabərsizliklər, Viyet teoremi, modullu, irrasional və kəsr-rasional tənliklər, sistemlər."),
    ("functions", "Funksiyalar", [quad_min, inverse_linear, composition, abs_min, linear_from_points, domain_count],
     "Kvadrat və modullu funksiya, tərs və mürəkkəb funksiya, təyin oblastı."),
    ("trigonometry", "Triqonometriya", [deg_to_rad, special_angles, sin_to_cos, double_angle, cos_theorem, reduction],
     "Radian ölçü, xüsusi bucaqlar, əsas eynilik, ikiqat bucaq, çevirmə düsturları, kosinuslar teoremi."),
    ("geometry", "Həndəsə və kombinatorika", [polygon_sum, regular_angle, inscribed, combinations, arrangements, dice],
     "Çoxbucaqlılar, çevrə və bucaqlar, kombinasiya, yerləşdirmə və ehtimal."),
]

if __name__ == "__main__":
    out = []
    for k, (sid, title, tpls, desc) in enumerate(SECTIONS):
        out.append((sid, title, build_section(10, "math", sid, title, tpls, seed=1000 + k), desc))
    save(10, "math", out)
