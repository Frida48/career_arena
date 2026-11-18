"""9-cu sinif riyaziyyat: 4 bölmə × 30 sual (kodla yaradılır, cavablar hesablanır)."""
import math
from fractions import Fraction as F
from common import build_section, save, fr, dec

# ---------- 1. Ədədlər və hesablamalar ----------

def gcd_lcm(r):
    g = r.choice([2, 3, 4, 5, 6])
    a, b = g * r.choice([3, 4, 5, 7]), g * r.choice([6, 8, 9, 11])
    if math.gcd(a, b) == a or a == b:
        b += g
    l = a * b // math.gcd(a, b)
    return dict(t=f"{a} və {b} ədədlərinin ən kiçik ortaq bölünəninin (ƏKOB) ən böyük ortaq bölənə (ƏBOB) nisbətini tapın.",
                a=F(l, math.gcd(a, b)), d=[l, math.gcd(a, b), a * b, F(l, 2 * math.gcd(a, b))],
                e=f"ƏBOB({a}; {b}) = {math.gcd(a, b)}, ƏKOB({a}; {b}) = {l}. Nisbət: {l} : {math.gcd(a, b)} = {fr(F(l, math.gcd(a, b)))}.",
                topic="ƏBOB və ƏKOB", diff="medium")


def fractions_sum(r):
    a, b = r.randint(1, 5), r.choice([3, 4, 5, 6, 7])
    c, d = r.randint(1, 5), r.choice([2, 3, 8, 9, 10])
    x = F(a, b) + F(c, d)
    return dict(t=f"Hesablayın: {a}/{b} + {c}/{d}", a=x,
                d=[F(a + c, b + d), F(a * c, b * d), x + F(1, b * d), F(a + c, b * d)],
                e=f"Ortaq məxrəcə gətiririk: {a}/{b} + {c}/{d} = {fr(x)}.",
                topic="Adi kəsrlər", diff="easy")


def percent_change(r):
    p = r.choice([100, 200, 250, 400, 500, 800])
    up = r.choice([10, 20, 25, 50])
    down = r.choice([10, 20, 40])
    res = F(p) * (100 + up) / 100 * (100 - down) / 100
    return dict(t=f"Malın qiyməti {p} manat idi. Qiymət əvvəlcə {up}% artırıldı, sonra yeni qiymət {down}% endirildi. Malın son qiyməti neçə manatdır?",
                a=res, d=[F(p) * (100 + up - down) / 100, F(p) * (100 - up) / 100, F(p) * (100 + down) / 100, res + p // 10],
                fmt=dec,
                e=f"{p} · {dec(F(100 + up, 100))} · {dec(F(100 - down, 100))} = {dec(res)} manat. Faizləri sadəcə toplayıb-çıxmaq olmaz.",
                topic="Faiz", diff="medium")


def percent_of(r):
    n = r.choice([120, 240, 360, 450, 600, 750])
    p = r.choice([15, 20, 30, 40, 60])
    x = F(n * p, 100)
    return dict(t=f"Sinifdə {n} səhifəlik kitabın {p}%-i oxunub. Neçə səhifə oxunmayıb?",
                a=n - x, d=[x, n - p, F(n, p), n - x + 10],
                fmt=dec,
                e=f"Oxunan: {n} · {p}/100 = {dec(x)}. Oxunmayan: {n} − {dec(x)} = {dec(n - x)}.",
                topic="Faiz", diff="easy")


def sqrt_simplify(r):
    a, b = r.choice([2, 3, 4, 5]), r.choice([2, 3, 5, 6, 7])
    c, d = r.choice([2, 3, 4]), b
    while c == a:
        c = r.choice([2, 3, 4, 5])
    # √(a²b) + √(c²b) = (a+c)√b
    return dict(t=f"Sadələşdirin: √{a*a*b} + √{c*c*d}",
                a=_r(a + c, b), d=[_r(a * c, b), f"√{a*a*b + c*c*d}", _r(a + c + 1, b), _r(abs(a - c), b), _r(a + c - 1, b)],
                e=f"√{a*a*b} = {a}√{b}, √{c*c*d} = {c}√{b}. Cəm: {a + c}√{b}.",
                topic="Kvadrat köklər", diff="medium")


def _r(k, b):
    return f"√{b}" if k == 1 else f"{k}√{b}"


def powers(r):
    a = r.choice([2, 3, 5])
    m, n, k = r.randint(3, 7), r.randint(2, 6), r.randint(4, 9)
    e = m + n - k
    if e < -2 or e > 4:
        k = m + n - r.randint(0, 3)
        e = m + n - k
    v = F(a) ** e
    return dict(t=f"Hesablayın: ({a}^{m} · {a}^{n}) : {a}^{k}",
                a=v, d=[F(a) ** (m * n - k), F(a) ** (e + 1), F(a) ** (e - 1), a * e],
                e=f"Eyni əsaslı qüvvətlər: {a}^({m}+{n}−{k}) = {a}^{e} = {fr(v)}.",
                topic="Tam üstlü qüvvət", diff="easy")


def ratio_split(r):
    a, b = r.choice([(2, 3), (3, 5), (1, 4), (4, 5), (3, 7)])
    k = r.choice([6, 8, 12, 15, 20])
    tot = (a + b) * k
    return dict(t=f"{tot} ədədini {a} : {b} nisbətində iki hissəyə bölün. Böyük hissə neçədir?",
                a=b * k, d=[a * k, tot // 2, b * k + a, (b - a) * k],
                e=f"Bir pay: {tot} : ({a}+{b}) = {k}. Böyük hissə: {b} · {k} = {b * k}.",
                topic="Nisbət və tənasüb", diff="easy")


# ---------- 2. Cəbri ifadələr və tənliklər ----------

def linear_eq(r):
    x = r.randint(-6, 9)
    a, c = r.choice([(5, 2), (7, 3), (4, 1), (6, 2), (9, 4)])
    b = r.randint(-10, 10)
    d = (a - c) * x + b
    return dict(t=f"Tənliyi həll edin: {a}x {'+' if b >= 0 else '−'} {abs(b)} = {c}x {'+' if d >= 0 else '−'} {abs(d)}",
                a=x, d=[-x, F(d + b, a - c), F(d - b, a + c), x + 2],
                e=f"{a}x − {c}x = {d} − ({b}) ⇒ {a - c}x = {d - b} ⇒ x = {x}.",
                topic="Xətti tənlik", diff="easy")


def vieta(r):
    p, q = r.randint(-6, 7), r.randint(-6, 7)
    while p == q or p == 0 or q == 0:
        q = r.randint(-6, 7)
    s, m = p + q, p * q
    ask_sum = r.random() < 0.5
    txt = f"x² {'−' if s >= 0 else '+'} {abs(s)}x {'+' if m >= 0 else '−'} {abs(m)} = 0 tənliyinin köklərinin " + ("cəmini" if ask_sum else "hasilini") + " tapın."
    ans = s if ask_sum else m
    return dict(t=txt, a=ans, d=[-ans, (m if ask_sum else s), -(m if ask_sum else s), ans + 1],
                e=f"Viyet teoremi: x₁ + x₂ = {s}, x₁ · x₂ = {m}.",
                topic="Viyet teoremi", diff="medium")


def quad_root(r):
    p, q = r.randint(-7, 8), r.randint(-7, 8)
    while p == q:
        q = r.randint(-7, 8)
    a = r.choice([1, 2])
    b, c = -a * (p + q), a * p * q
    big = max(p, q)
    def term(k, s):
        if k == 0:
            return ""
        return f" {'+' if k > 0 else '−'} {abs(k) if abs(k) != 1 or s == '' else ''}{s}"
    lead = "x²" if a == 1 else f"{a}x²"
    return dict(t=f"{lead}{term(b, 'x')}{term(c, '')} = 0 tənliyinin böyük kökünü tapın.",
                a=big, d=[min(p, q), -big, -min(p, q), p + q],
                e=f"Diskriminant: D = {b*b - 4*a*c}. Köklər: x₁ = {min(p, q)}, x₂ = {big}.",
                topic="Kvadrat tənlik", diff="medium")


def squares_identity(r):
    s, p = r.randint(3, 9), r.randint(1, 8)
    return dict(t=f"a + b = {s} və ab = {p} olarsa, a² + b² ifadəsinin qiymətini tapın.",
                a=s * s - 2 * p, d=[s * s, s * s + 2 * p, s * s - p, 2 * s - p],
                e=f"a² + b² = (a + b)² − 2ab = {s*s} − {2*p} = {s*s - 2*p}.",
                topic="Qısa vurma düsturları", diff="medium")


def system2(r):
    x, y = r.randint(-4, 8), r.randint(-4, 8)
    a, b = r.choice([(2, 3), (3, 1), (1, 4), (5, 2)])
    return dict(t=f"Sistemi həll edin: {{ x + y = {x + y};  {a}x − {b}y = {a*x - b*y} }}. x · y hasilini tapın.",
                a=x * y, d=[x + y, x - y, -x * y, x * y + 1],
                e=f"Birinci tənlikdən y = {x + y} − x. Yerinə qoyduqda x = {x}, y = {y}. Hasil: {x * y}.",
                topic="Tənliklər sistemi", diff="medium")


def lin_ineq(r):
    a = r.choice([2, 3, 4, 5])
    b = r.randint(-9, 9)
    c = r.randint(-9, 15)
    # a x + b > c  => x > (c-b)/a ; ən kiçik tam həll
    bound = F(c - b, a)
    ans = math.floor(bound) + 1
    return dict(t=f"{a}x {'+' if b >= 0 else '−'} {abs(b)} > {c} bərabərsizliyinin ən kiçik tam həllini tapın.",
                a=ans, d=[ans - 1, ans + 1, math.floor(bound), -ans],
                e=f"{a}x > {c - b} ⇒ x > {fr(bound)}. Ən kiçik tam həll: {ans}.",
                topic="Xətti bərabərsizlik", diff="medium")


# ---------- 3. Funksiyalar və proqressiyalar ----------

def line_zero(r):
    k = r.choice([2, 3, 4, -2, -3, 5])
    x0 = r.randint(-5, 6)
    b = -k * x0
    return dict(t=f"y = {k}x {'+' if b >= 0 else '−'} {abs(b)} funksiyasının qrafiki absis oxunu hansı nöqtədə kəsir? (nöqtənin absisini yazın)",
                a=x0, d=[-x0, b, -b, F(k, 1) if k != x0 else x0 + 1],
                e=f"y = 0 ⇒ {k}x = {-b} ⇒ x = {x0}.",
                topic="Xətti funksiya", diff="easy")


def line_through(r):
    x1, x2 = r.randint(-3, 2), r.randint(3, 6)
    k, b = r.choice([1, 2, -1, 3]), r.randint(-4, 5)
    y1, y2 = k * x1 + b, k * x2 + b
    return dict(t=f"A({x1}; {y1}) və B({x2}; {y2}) nöqtələrindən keçən düz xəttin bucaq əmsalını tapın.",
                a=k, d=[-k, F(x2 - x1, y2 - y1) if y2 != y1 else 0, b, k + 1],
                e=f"k = (y₂ − y₁)/(x₂ − x₁) = ({y2} − {y1})/({x2} − {x1}) = {k}.",
                topic="Xətti funksiya", diff="medium")


def parabola_vertex(r):
    a = r.choice([1, 2, -1, 3])
    h = r.randint(-4, 5)
    c = r.randint(-6, 6)
    b = -2 * a * h
    yv = a * h * h + b * h + c
    lead = {1: "x²", -1: "−x²"}.get(a, f"{a}x²")
    ask_y = r.random() < 0.5
    return dict(t=f"y = {lead} {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)} parabolasının təpə nöqtəsinin {'ordinatını' if ask_y else 'absisini'} tapın.",
                a=yv if ask_y else h, d=[-(yv if ask_y else h), (h if ask_y else yv), c, (yv if ask_y else h) + 2],
                e=f"x₀ = −b/(2a) = {h}; y₀ = y({h}) = {yv}.",
                topic="Kvadrat funksiya", diff="medium")


def arith_nth(r):
    a1, d, n = r.randint(-5, 10), r.choice([2, 3, 4, 5, -2, -3]), r.randint(8, 20)
    an = a1 + (n - 1) * d
    return dict(t=f"Ədədi silsilədə a₁ = {a1}, d = {d}. a{_sub(n)} həddini tapın.",
                a=an, d=[a1 + n * d, a1 * d * n, an - d, a1 + (n - 2) * d],
                e=f"aₙ = a₁ + (n − 1)d = {a1} + {n - 1}·({d}) = {an}.",
                topic="Ədədi silsilə", diff="easy")


def arith_sum(r):
    a1, d, n = r.randint(1, 6), r.choice([2, 3, 4]), r.choice([10, 12, 15, 20])
    s = n * (2 * a1 + (n - 1) * d) // 2
    return dict(t=f"Ədədi silsilənin birinci həddi {a1}, fərqi {d}-dür. İlk {n} həddin cəmini tapın.",
                a=s, d=[s - n, n * (a1 + (n - 1) * d), a1 + (n - 1) * d, s + d * n],
                e=f"Sₙ = (2a₁ + (n − 1)d)·n/2 = (2·{a1} + {n - 1}·{d})·{n}/2 = {s}.",
                topic="Ədədi silsilə", diff="medium")


def geom_nth(r):
    b1, q, n = r.choice([1, 2, 3, 5]), r.choice([2, 3, -2]), r.randint(4, 7)
    bn = b1 * q ** (n - 1)
    return dict(t=f"Həndəsi silsilədə b₁ = {b1}, q = {q}. b{_sub(n)} həddini tapın.",
                a=bn, d=[b1 * q ** n, -bn, b1 * q * (n - 1), b1 * q ** (n - 2)],
                e=f"bₙ = b₁·qⁿ⁻¹ = {b1}·({q})^{n - 1} = {bn}.",
                topic="Həndəsi silsilə", diff="medium")


def func_value(r):
    a, b, c = r.choice([1, 2, -1]), r.randint(-5, 5), r.randint(-6, 6)
    k = r.randint(-3, 4)
    v = a * k * k + b * k + c
    lead = {1: "x²", -1: "−x²"}.get(a, f"{a}x²")
    return dict(t=f"f(x) = {lead} {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)} olarsa, f({k}) qiymətini tapın.",
                a=v, d=[a * k * k - b * k + c, v - 2 * c, -v, a * 2 * k + b * k + c],
                e=f"f({k}) = {a}·({k})² + ({b})·({k}) + ({c}) = {v}.",
                topic="Funksiyanın qiyməti", diff="easy")


def _sub(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


# ---------- 4. Həndəsə, statistika və ehtimal ----------

TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15), (12, 16, 20)]


def pythagoras(r):
    a, b, c = r.choice(TRIPLES)
    ask = r.choice(["c", "a"])
    if ask == "c":
        return dict(t=f"Düzbucaqlı üçbucağın katetləri {a} sm və {b} sm-dir. Hipotenuzu tapın (sm).",
                    a=c, d=[a + b, c + 1, b + 1, c - 2],
                    e=f"c = √({a}² + {b}²) = √{a*a + b*b} = {c}.", topic="Pifaqor teoremi", diff="easy")
    return dict(t=f"Düzbucaqlı üçbucağın hipotenuzu {c} sm, bir kateti {b} sm-dir. Digər kateti tapın (sm).",
                a=a, d=[c - b, a + 1, b - a if b != a else a + 2, a + 2],
                e=f"a = √({c}² − {b}²) = √{c*c - b*b} = {a}.", topic="Pifaqor teoremi", diff="easy")


def triangle_angles(r):
    a, b = r.randint(30, 80), r.randint(25, 70)
    c = 180 - a - b
    ext = r.random() < 0.5
    if ext:
        return dict(t=f"Üçbucağın iki bucağı {a}° və {b}°-dir. Üçüncü bucağa qonşu xarici bucağı tapın.",
                    a=a + b, d=[c, 180 - a, 180 - b, 90 + c], e=f"Xarici bucaq ona qonşu olmayan iki daxili bucağın cəminə bərabərdir: {a}° + {b}° = {a + b}°.",
                    topic="Üçbucağın bucaqları", diff="medium")
    return dict(t=f"Üçbucağın iki bucağı {a}° və {b}°-dir. Üçüncü bucağı tapın.",
                a=c, d=[a + b, 180 - a, 90 - b if b < 90 else c + 10, c + 10],
                e=f"180° − {a}° − {b}° = {c}°.", topic="Üçbucağın bucaqları", diff="easy")


def circle(r):
    rad = r.randint(2, 9)
    if r.random() < 0.5:
        return dict(t=f"Radiusu {rad} sm olan dairənin sahəsini tapın.",
                    a=f"{rad*rad}π sm²", d=[f"{2*rad}π sm²", f"{rad}π sm²", f"{2*rad*rad}π sm²", f"{rad*rad*4}π sm²", f"{rad*rad+1}π sm²", f"{rad*rad-1}π sm²"],
                    e=f"S = πr² = π·{rad}² = {rad*rad}π sm².", topic="Çevrə və dairə", diff="easy")
    return dict(t=f"Diametri {2*rad} sm olan çevrənin uzunluğunu tapın.",
                a=f"{2*rad}π sm", d=[f"{rad}π sm", f"{4*rad}π sm", f"{rad*rad}π sm", f"{rad*rad*4}π sm", f"{2*rad+1}π sm", f"{2*rad-1}π sm"],
                e=f"C = πd = {2*rad}π sm.", topic="Çevrə və dairə", diff="easy")


def trapezoid(r):
    a, b, h = r.randint(4, 12), r.randint(13, 20), r.choice([4, 6, 8, 10])
    return dict(t=f"Trapesiyanın oturacaqları {a} sm və {b} sm, hündürlüyü {h} sm-dir. Sahəsini tapın (sm²).",
                a=(a + b) * h // 2, d=[(a + b) * h, a * b, (b - a) * h // 2 if (b - a) * h // 2 > 0 else 1, (a + b) * h // 2 + h],
                e=f"S = (a + b)/2 · h = ({a} + {b})/2 · {h} = {(a + b) * h // 2}.",
                topic="Dördbucaqlılar", diff="easy")


def mean_median(r):
    xs = sorted(r.sample(range(2, 30), 5))
    if r.random() < 0.5:
        s = sum(xs)
        rr = r.choice(range(len(xs)))
        xs[rr] += (5 - s % 5) % 5  # cəm 5-ə bölünsün
        xs = sorted(xs)
        m = F(sum(xs), 5)
        shuffled = xs[:]
        r.shuffle(shuffled)
        return dict(t=f"{'; '.join(map(str, shuffled))} ədədlərinin ədədi ortasını tapın.",
                    a=m, d=[xs[2], m + 1, F(sum(xs), 4), max(xs) - min(xs)],
                    e=f"Cəm {sum(xs)}, say 5. Ədədi orta: {sum(xs)} : 5 = {fr(m)}.",
                    topic="Statistika", diff="easy")
    shuffled = xs[:]
    r.shuffle(shuffled)
    return dict(t=f"{'; '.join(map(str, shuffled))} ədədlər sırasının medianını tapın.",
                a=xs[2], d=[shuffled[2] if shuffled[2] != xs[2] else xs[1], xs[1], xs[3], F(sum(xs), 5)],
                e=f"Artan sıra: {'; '.join(map(str, xs))}. Ortadakı ədəd: {xs[2]}.",
                topic="Statistika", diff="easy")


def probability(r):
    red, blue, green = r.randint(2, 7), r.randint(2, 7), r.randint(1, 6)
    tot = red + blue + green
    p = F(red + green, tot)
    return dict(t=f"Qutuda {red} qırmızı, {blue} göy və {green} yaşıl kürə var. Təsadüfi götürülən kürənin göy olmaması ehtimalını tapın.",
                a=p, d=[F(blue, tot), F(red, tot), F(green, tot), F(red + green, blue)],
                e=f"Əlverişli hallar: {red} + {green} = {red + green}, bütün hallar: {tot}. P = {fr(p)}.",
                topic="Ehtimal", diff="medium")


SECTIONS = [
    ("numbers", "Ədədlər və hesablamalar", [gcd_lcm, fractions_sum, percent_change, percent_of, sqrt_simplify, powers, ratio_split]),
    ("algebra", "Cəbri ifadələr, tənliklər və bərabərsizliklər", [linear_eq, vieta, quad_root, squares_identity, system2, lin_ineq]),
    ("functions", "Funksiyalar və silsilələr", [line_zero, line_through, parabola_vertex, arith_nth, arith_sum, geom_nth, func_value]),
    ("geometry", "Həndəsə, statistika və ehtimal", [pythagoras, triangle_angles, circle, trapezoid, mean_median, probability]),
]

DESC = {
    "numbers": "ƏBOB və ƏKOB, kəsrlər, faiz, kvadrat köklər, qüvvət və nisbət.",
    "algebra": "Xətti və kvadrat tənliklər, Viyet teoremi, qısa vurma düsturları, sistemlər və bərabərsizliklər.",
    "functions": "Xətti və kvadrat funksiya, ədədi və həndəsi silsilələr.",
    "geometry": "Pifaqor teoremi, üçbucağın bucaqları, çevrə və dairə, trapesiya, statistika və ehtimal.",
}

if __name__ == "__main__":
    out = []
    for k, (sid, title, tpls) in enumerate(SECTIONS):
        out.append((sid, title, build_section(9, "math", sid, title, tpls, seed=900 + k), DESC[sid]))
    save(9, "math", out)
