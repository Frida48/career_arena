"""Riyaziyyat · Statistika və ehtimal: stat-avg (yalnız 9, 10), stat-prob (çox çətin).

Ehtimal cavablarının hamısı bütün halların tam sadalanması (itertools) ilə yoxlanır.
"""
import math
import statistics
from fractions import Fraction as F
from itertools import combinations, permutations, product

from common import dec, dat, abl, cop
from mx import Num, M, H, show, neg, par

C = math.comb


def az_cop(n):
    s = cop(n)
    return "−" + s[1:] if s.startswith("-") else s


# ======================= stat-avg =======================

def avg_new(r, g):
    while True:
        n = r.randint(8, 30)
        m = F(r.randint(50, 90 * 2), 2)
        x = r.randint(30, 100)
        m2 = (n * m + x) / (n + 1)
        if m2.denominator <= 2 and x != m and m2 != m:
            break
    # müstəqil: real siyahı qur
    scores = [m] * n
    chk = (m2 * (n + 1)) - sum(scores)
    assert statistics.mean(scores + [chk]) == m2
    return dict(t=f"Sinifdəki {n} şagirdin orta balı {dec(m)} idi. Sinfə yeni şagird gəldikdən sonra orta bal {dec(m2)} oldu. Yeni şagirdin balı neçədir?",
                a=x, d=[m2 * (n + 1) - m * (n + 1), m2 + (m2 - m) * n, 2 * m2 - m, x + n, x - n], open=True,
                e=f"Əvvəlki cəm {n}·{dec(m)} = {dec(n * m)}, yeni cəm {n + 1}·{dec(m2)} = {dec((n + 1) * m2)}. Fərq: {x}.", chk=chk, diff=M)


def avg_groups(r, g):
    while True:
        n1, n2 = r.randint(5, 30), r.randint(5, 30)
        m1, m2 = r.randint(50, 95), r.randint(50, 95)
        M_ = F(n1 * m1 + n2 * m2, n1 + n2)
        if m1 != m2 and n1 != n2 and M_.denominator <= 4:
            break
    ask = r.choice(["mean", "n2"]) if g == 10 else "mean"
    data = [m1] * n1 + [m2] * n2
    if ask == "mean":
        return dict(t=f"Birinci qrupdakı {n1} şagirdin orta balı {m1}, ikinci qrupdakı {n2} şagirdin orta balı {m2}-dir. Bütün şagirdlərin orta balını tapın.".replace(f"balı {m2}-dir", f"balı {az_cop(m2)}"),
                    a=M_, d=[F(m1 + m2, 2), F(n1 * m2 + n2 * m1, n1 + n2), M_ + 1, M_ - 1, F(n1 * m1 + n2 * m2, n1 + n2 + 1)],
                    e=f"Ümumi cəm {n1}·{m1} + {n2}·{m2} = {n1 * m1 + n2 * m2}, şagird sayı {n1 + n2}. Orta: {show(M_)}.",
                    chk=statistics.mean(data), diff=M)
    sols = [k for k in range(1, 400) if F(n1 * m1 + k * m2, n1 + k) == M_]
    return dict(t=f"Birinci qrupdakı {n1} şagirdin orta balı {m1}, ikinci qrupdakı şagirdlərin orta balı {m2}-dir. Bütün şagirdlərin orta balı {dec(M_) if (M_ * 100).denominator == 1 else show(M_)} olarsa, ikinci qrupda neçə şagird var?".replace(f"balı {m2}-dir", f"balı {az_cop(m2)}"),
                a=n2, d=[n2 + 1, n2 - 1, n1, n2 + 2, n2 - 2],
                e=f"{n1}·{m1} + x·{m2} = ({n1} + x)·{show(M_)} ⇒ x = {n2}.", chk=sols[0] if len(sols) == 1 else 999, diff=H)


def avg_median_x(r, g):
    while True:
        k = 5 if g == 9 else 7
        vals = sorted(r.sample(range(1, 40), k - 1))
        # x ən böyük olsun: median = vals[k//2]
        med = vals[k // 2]
        x = k * med - sum(vals)
        if x > vals[-1]:
            break
    sols = [z for z in range(vals[-1] + 1, 400) if F(sum(vals) + z, k) == statistics.median(vals + [z])]
    shown = vals[:]
    r.shuffle(shown)
    return dict(t=f"{', '.join(map(str, shown))}, x ədədlərinin ədədi ortası medianına bərabərdir. x > {vals[-1]} olarsa, x-i tapın.",
                a=x, d=[x + 1, x - 1, med, x + k, sum(vals) // (k - 1)],
                e=f"x ən böyük ədəddirsə, median {med}. (Cəm + x)/{k} = {med} ⇒ x = {k}·{med} − {sum(vals)} = {x}.",
                chk=sols[0] if len(sols) == 1 else 999, diff=H)


def avg_variance(r, g):
    while True:
        n = r.randint(5, 7)
        data = [r.randint(1, 20) for _ in range(n)]
        if len(set(data)) > 2 and F(sum(data), n).denominator == 1:
            break
    mu = F(sum(data), n)
    var = sum((F(x) - mu) ** 2 for x in data) / n
    ask = r.choice(["var", "std"]) if var.denominator == 1 and int(var) > 0 and math.isqrt(int(var)) ** 2 == var else "var"
    chk = statistics.pvariance(data) if ask == "var" else statistics.pstdev(data)
    ans = var if ask == "var" else F(math.isqrt(int(var)))
    w = "dispersiyasını" if ask == "var" else "orta kvadratik meylini"
    return dict(t=f"{', '.join(map(str, data))} verilənlərinin {w} tapın.", a=ans,
                d=[sum((F(x) - mu) ** 2 for x in data) / (n - 1), var * n / (n - 1) + 1, ans + 1, ans * 2, F(sum(abs(F(x) - mu) for x in data), n)],
                e=f"Orta: {show(mu)}. Dispersiya: Σ(xᵢ − {show(mu)})²/{n} = {show(var)}." + (f" Orta kvadratik meyl √{show(var)} = {show(ans)}." if ask == "std" else ""),
                chk=chk, diff=H)


def avg_freq(r, g):
    while True:
        vals = sorted(r.sample(range(2, 11), 4))
        cnt = [r.randint(1, 9) for _ in vals]
        data = [v for v, c in zip(vals, cnt) for _ in range(c)]
        modes = statistics.multimode(data)
        if len(modes) == 1:
            break
    ask = r.choice(["med_mode", "mean_med"])
    med = F(statistics.median(data)).limit_denominator(10)
    mean = F(sum(data), len(data))
    if ask == "med_mode":
        ans, chk = med + modes[0], statistics.median(data) + statistics.mode(data)
        w, how = "medianı ilə modasının cəmini", f"n = {len(data)}, median = {show(med)}, moda = {modes[0]}. Cəm: {show(ans)}."
        d = [mean + modes[0], med + vals[-1], ans + 1, ans - 1, F(vals[1] + vals[2], 2) + modes[0]]
    else:
        ans, chk = mean - med, statistics.mean(data) - statistics.median(data)
        w, how = "ədədi ortası ilə medianının fərqini", f"n = {len(data)}, orta = {show(mean)}, median = {show(med)}. Fərq: {show(ans)}."
        d = [F(sum(vals), 4) - med, mean - modes[0], ans + 1, -ans, ans + F(1, 2)]
    table = "; ".join(f"{v} — {c} dəfə" for v, c in zip(vals, cnt))
    return dict(t=f"Testdə şagirdlərin balları belə paylanıb: {table}. Balların {w} tapın.", a=ans, d=d, e=how, chk=chk, diff=M)


def avg_transform(r, g):
    while True:
        n = r.randint(5, 8)
        data = [r.randint(1, 15) for _ in range(n)]
        k, b = r.choice([2, 3, -2, 4, F(1, 2)]), r.randint(-10, 10)
        if len(set(data)) > 2:
            break
    var = F(statistics.pvariance([F(x) for x in data]))
    mu = F(sum(data), n)
    ask = r.choice(["var", "mean"])
    new = [k * x + b for x in data]
    if ask == "var":
        ans, chk = k * k * var, statistics.pvariance([F(x) for x in new])
        how = f"Hər ədəd {show(k)}-ə vurulub {b}-ə əlavə olunanda dispersiya {show(k)}² = {show(k * k)} dəfə dəyişir, toplama təsir etmir: {show(k * k)}·{show(var)} = {show(ans)}."
        d = [k * var, k * k * var + b, k * var + b, var, abs(k) * var * 2]
        w = "dispersiyası"
    else:
        ans, chk = k * mu + b, statistics.mean([F(x) for x in new])
        how = f"Yeni orta = {show(k)}·{show(mu)} + ({b}) = {show(ans)}."
        d = [k * mu, mu + b, k * (mu + b), k * k * mu + b, ans + 1]
        w = "ədədi ortası"
    kb = f"{show(k)}-ə vurulub, sonra {neg(str(b))} əlavə edilərsə" if b != 0 else f"{show(k)}-ə vurularsa"
    return dict(t=f"{', '.join(map(str, data))} verilənlərinin hər biri {kb}, yeni verilənlərin {w} neçə olar?".replace(f"{show(k)}-ə", dat(k) if F(k).denominator == 1 else f"{show(k)}-ə"),
                a=ans, d=d, e=f"Əvvəlki orta {show(mu)}, dispersiya {show(var)}. {how}".replace(f"{show(k)}-ə vurulub {b}-ə", "vurulub sabit ədəd"), chk=chk, diff=H)


def avg_pairwise(r, g):
    a, b, c = r.randint(1, 60), r.randint(1, 60), r.randint(1, 60)
    p, q, s = F(a + b, 2), F(b + c, 2), F(a + c, 2)
    ans = F(a + b + c, 3)
    chk = (p + q + s) / 3
    ask = r.choice(["mean", "max"])
    if ask == "max":
        ans = max(a, b, c)
        chk = max(p + s - q, p + q - s, q + s - p)
    return dict(t=f"a və b ədədlərinin ədədi ortası {dec(p)}, b və c-nin {dec(q)}, a və c-nin isə {dec(s)}-dir. "
                  f"{'a, b, c ədədlərinin ədədi ortasını' if ask == 'mean' else 'Bu üç ədəddən ən böyüyünü'} tapın.".replace(f"isə {dec(s)}-dir", f"isə {dec(s)}"),
                a=ans, d=[p + q + s, (p + q + s) / 2, ans + 1, ans - 1, max(p, q, s)],
                e=f"a + b = {dec(2 * p)}, b + c = {dec(2 * q)}, a + c = {dec(2 * s)}. Toplasaq: 2(a + b + c) = {dec(2 * (p + q + s))}, a + b + c = {a + b + c}. "
                  + (f"Orta: {show(F(a + b + c, 3))}." if ask == "mean" else f"a = {a}, b = {b}, c = {c}. Ən böyüyü {max(a, b, c)}."),
                chk=chk, diff=M)


# ======================= stat-prob =======================

COL = [("qırmızı", "q"), ("ağ", "a"), ("göy", "g"), ("yaşıl", "y")]


def _urn(r, k_colors=2, lo=2, hi=8):
    return [r.randint(lo, hi) for _ in range(k_colors)]


def prob_urn_exact(r, g):
    while True:
        cnts = _urn(r, 3, 2, 6)
        n = sum(cnts)
        k = r.randint(3, 4)
        j = r.randint(1, min(k, cnts[0]))
        if n <= 15 and k < n:
            break
    balls = [i for i, c in enumerate(cnts) for _ in range(c)]
    good = sum(1 for comb in combinations(range(n), k) if sum(1 for t in comb if balls[t] == 0) == j)
    chk = F(good, C(n, k))
    ans = F(C(cnts[0], j) * C(n - cnts[0], k - j), C(n, k))
    p = F(cnts[0], n)
    desc = ", ".join(f"{c} {COL[i][0]}" for i, c in enumerate(cnts))
    return dict(t=f"Qutuda {desc} şar var. Təsadüfi olaraq eyni anda {k} şar götürülür. Onlardan düz {j}-nin qırmızı olması ehtimalını tapın.".replace(f"düz {j}-nin", f"düz {_gen(j)}"),
                a=ans, d=[C(k, j) * p ** j * (1 - p) ** (k - j), F(C(cnts[0], j), C(n, k)), F(C(cnts[0], j) * C(n - cnts[0], k - j), C(n, k) * 2), F(j, k) * p, ans + F(1, C(n, k))],
                e=f"Bütün hallar: C({n}, {k}) = {C(n, k)}. Əlverişli: C({cnts[0]}, {j})·C({n - cnts[0]}, {k - j}) = {C(cnts[0], j) * C(n - cnts[0], k - j)}. P = {show(ans)}.",
                chk=chk, diff=H)


def _gen(n):
    """yiyəlik hal: 1-nin, 2-sinin, 3-ünün, 4-ünün"""
    return {1: "birinin", 2: "ikisinin", 3: "üçünün", 4: "dördünün", 5: "beşinin"}[n]


def prob_dice(r, g):
    nd = 3 if g != 10 else r.choice([2, 3])
    kind = r.choice(["sum_eq", "sum_ge", "prod_div", "max_eq", "diff_ge"])
    outs = list(product(range(1, 7), repeat=nd))
    tot = len(outs)
    if kind == "sum_eq":
        s = r.randint(nd + 2, 6 * nd - 2)
        good = [o for o in outs if sum(o) == s]
        t = f"{nd} zər atılır. Düşən xalların cəminin {s} olması ehtimalını tapın."
        how = f"Cəmi {s} olan hallar: {len(good)}, bütün hallar 6^{nd} = {tot}."
    elif kind == "sum_ge":
        s = r.randint(nd + 3, 6 * nd - 1)
        good = [o for o in outs if sum(o) >= s]
        t = f"{nd} zər atılır. Düşən xalların cəminin {s}-dən kiçik olmaması ehtimalını tapın.".replace(f"{s}-dən", abl(s))
        how = f"Cəmi ≥ {s} olan hallar: {len(good)} (və ya tamamlayıcı hadisə ilə), bütün hallar {tot}."
    elif kind == "prod_div":
        k = r.choice([3, 4, 6, 5, 9, 12])
        good = [o for o in outs if math.prod(o) % k == 0]
        t = f"{nd} zər atılır. Düşən xalların hasilinin {k}-ə bölünməsi ehtimalını tapın.".replace(f"{k}-ə", dat(k))
        how = f"Hasil {k}-ə bölünən hallar: {len(good)}, bütün hallar {tot}.".replace(f"{k}-ə", dat(k))
    elif kind == "max_eq":
        m = r.randint(2, 6)
        good = [o for o in outs if max(o) == m]
        t = f"{nd} zər atılır. Düşən xallardan ən böyüyünün {m} olması ehtimalını tapın."
        how = f"P(max ≤ {m}) − P(max ≤ {m - 1}) = ({m}^{nd} − {m - 1}^{nd})/{tot} = {m ** nd - (m - 1) ** nd}/{tot}."
    else:
        dd = r.randint(1, 4)
        if nd == 3:
            nd = 2
            outs = list(product(range(1, 7), repeat=2))
            tot = 36
        good = [o for o in outs if abs(o[0] - o[1]) >= dd]
        t = f"2 zər atılır. Düşən xalların fərqinin modulunun {dd}-dən kiçik olmaması ehtimalını tapın.".replace(f"{dd}-dən", abl(dd))
        how = f"|a − b| ≥ {dd} olan hallar: {len(good)}, bütün hallar 36."
    ans = F(len(good), tot)
    # müstəqil: sayma hesabı ilə yox, ehtimalların cəmi ilə
    chk = sum(F(1, tot) for o in good)
    return dict(t=t, a=ans, d=[F(len(good), tot // 2) if len(good) * 2 <= tot else 1 - ans, F(len(good) + 1, tot), F(len(good) - 1, tot) if len(good) > 1 else F(len(good) + 2, tot),
                               1 - ans, F(len(good), 6 * nd)], e=f"{how} P = {show(ans)}.", chk=chk, diff=M if g == 10 else H)


def prob_row(r, g):
    n = r.randint(5, 7)
    kind = r.choice(["adj", "notadj_end", "between", "order3"])
    people = list(range(n))
    perms = list(permutations(people))
    A, B, Cc = 0, 1, 2
    if kind == "adj":
        good = [p for p in perms if abs(p.index(A) - p.index(B)) == 1]
        t = f"{n} nəfər, o cümlədən Anar və Bəhruz, təsadüfi qaydada bir cərgədə düzülür. Anar ilə Bəhruzun yan-yana durması ehtimalını tapın."
        how = f"Anar ilə Bəhruzu bir blok sayın: 2·{n - 1}! hal. P = 2·{n - 1}!/{n}! = 2/{n}."
    elif kind == "notadj_end":
        good = [p for p in perms if abs(p.index(A) - p.index(B)) > 1 and p.index(Cc) in (0, n - 1)]
        t = f"{n} nəfər, o cümlədən Anar, Bəhruz və Cavid, təsadüfi qaydada bir cərgədə düzülür. Cavidin cərgənin kənarında durması, Anar ilə Bəhruzun isə yan-yana durmaması ehtimalını tapın."
        how = f"Cavid kənarda: 2 yol. Qalan {n - 1} yerə {n - 1} nəfər: {math.factorial(n - 1)}, onlardan Anar və Bəhruzun yan-yana olduğu 2·{n - 2}! = {2 * math.factorial(n - 2)} hal çıxılır."
    elif kind == "between":
        good = [p for p in perms if abs(p.index(A) - p.index(B)) == 2]
        t = f"{n} nəfər, o cümlədən Anar və Bəhruz, təsadüfi qaydada bir cərgədə düzülür. Anar ilə Bəhruzun arasında düz bir nəfərin durması ehtimalını tapın."
        how = f"Anar və Bəhruzun yer cütü (i, i + 2): {n - 2} variant, 2 sıra, qalanlar {n - 2}! yolla."
    else:
        good = [p for p in perms if p.index(A) < p.index(B) < p.index(Cc)]
        t = f"{n} nəfər, o cümlədən Anar, Bəhruz və Cavid, təsadüfi qaydada bir cərgədə düzülür. Anarın Bəhruzdan, Bəhruzun isə Caviddən solda durması ehtimalını tapın (yan-yana olmaları vacib deyil)."
        how = "Üç nəfərin qarşılıqlı düzülüşü 3! = 6 cür, onlardan biri əlverişlidir."
    ans = F(len(good), len(perms))
    exp = {"adj": F(2, n), "between": F(2 * (n - 2), n * (n - 1)), "order3": F(1, 6)}.get(kind)
    if exp is not None:
        assert exp == ans
    return dict(t=t, a=ans, d=[1 - ans, F(1, n), F(2, n - 1) if kind != "adj" else F(1, n - 1), ans * 2, F(1, n * (n - 1))],
                e=f"{how} P = {show(ans)}.", chk=F(len(good), math.factorial(n)), diff=H)


def prob_shooters(r, g):
    ps = [F(r.randint(1, 9), 10) for _ in range(3)]
    kind = r.choice(["one", "atleast2", "two"]) if g != 9 else r.choice(["one", "atleast1"])
    outs = list(product([0, 1], repeat=3))
    def pr(o):
        v = F(1)
        for hit, p in zip(o, ps):
            v *= p if hit else 1 - p
        return v
    cond = {"one": lambda o: sum(o) == 1, "atleast2": lambda o: sum(o) >= 2, "two": lambda o: sum(o) == 2, "atleast1": lambda o: sum(o) >= 1}[kind]
    chk = sum(pr(o) for o in outs if cond(o))
    p1, p2, p3 = ps
    q1, q2, q3 = 1 - p1, 1 - p2, 1 - p3
    if kind == "one":
        ans = p1 * q2 * q3 + q1 * p2 * q3 + q1 * q2 * p3
        w = "yalnız birinin hədəfi vurması"
        how = "p₁q₂q₃ + q₁p₂q₃ + q₁q₂p₃"
    elif kind == "atleast1":
        ans = 1 - q1 * q2 * q3
        w = "ən azı birinin hədəfi vurması"
        how = "1 − q₁q₂q₃"
    elif kind == "two":
        ans = p1 * p2 * q3 + p1 * q2 * p3 + q1 * p2 * p3
        w = "düz ikisinin hədəfi vurması"
        how = "p₁p₂q₃ + p₁q₂p₃ + q₁p₂p₃"
    else:
        ans = p1 * p2 * q3 + p1 * q2 * p3 + q1 * p2 * p3 + p1 * p2 * p3
        w = "ən azı ikisinin hədəfi vurması"
        how = "p₁p₂q₃ + p₁q₂p₃ + q₁p₂p₃ + p₁p₂p₃"
    return dict(t=f"Üç atıcı hədəfə bir-birindən asılı olmadan bir dəfə atəş açır. Hədəfi vurma ehtimalları uyğun olaraq {dec(p1)}; {dec(p2)}; {dec(p3)}-dir. Atıcılardan {w} ehtimalını tapın.".replace(f"{dec(p3)}-dir", f"{dec(p3)}"),
                a=Num(dec(ans), ans) if ans.denominator in (10, 100, 1000, 2, 4, 5, 20, 25, 50, 125, 200, 250, 500) else ans,
                d=[Num(dec(x), x) for x in (p1 + p2 + p3 if p1 + p2 + p3 < 1 else 1 - ans, p1 * p2 * p3, 1 - ans, ans + F(1, 100), ans - F(1, 100), ans + F(2, 100), p1 * q2 * q3)],
                e=f"q = 1 − p: q₁ = {dec(q1)}, q₂ = {dec(q2)}, q₃ = {dec(q3)}. P = {how} = {dec(ans)}.", chk=chk, diff=H, open=False)


def prob_divis(r, g):
    while True:
        N = r.choice([60, 90, 100, 120, 150, 180, 200, 240, 300])
        a, b, c = r.sample([2, 3, 4, 5, 6, 7, 9, 10], 3)
        if len({a, b, c}) == 3:
            break
    good = [x for x in range(1, N + 1) if (x % a == 0 or x % b == 0) and x % c != 0]
    ans = F(len(good), N)
    L = lambda *xs: math.lcm(*xs)
    cnt = N // a + N // b - N // L(a, b) - (N // L(a, c) + N // L(b, c) - N // L(a, b, c))
    assert cnt == len(good)
    return dict(t=f"1-dən {N}-ə qədər natural ədədlərdən biri təsadüfi seçilir. Onun {a}-ə və ya {b}-ə bölünməsi, lakin {c}-ə bölünməməsi ehtimalını tapın.".replace(f"{N}-ə", dat(N)).replace(f"{a}-ə", dat(a)).replace(f"{b}-ə", dat(b)).replace(f"{c}-ə", dat(c)),
                a=ans, d=[F(N // a + N // b, N), F(N // a + N // b - N // L(a, b), N), F(N // a + N // b - N // c, N), ans + F(1, N), ans - F(1, N)],
                e=f"Daxiletmə–xaricetmə: {a} və ya {b}-yə bölünənlər {N // a + N // b - N // L(a, b)}, onlardan {c}-yə də bölünənlər {N // L(a, c) + N // L(b, c) - N // L(a, b, c)}. Fərq {cnt}. P = {show(ans)}.".replace(f"{b}-yə", dat(b)).replace(f"{c}-yə", dat(c)),
                chk=F(len(good), N), diff=H)


def prob_committee(r, g):
    while True:
        m, w = r.randint(3, 9), r.randint(3, 9)
        k = r.randint(3, 5)
        if k <= m + w - 2 and m + w <= 16:
            break
    kind = r.choice(["atleast2", "more_g", "both"])
    ppl = ["o"] * m + ["q"] * w
    combs = list(combinations(range(m + w), k))
    girls = lambda cmb: sum(1 for i in cmb if ppl[i] == "q")
    if kind == "atleast2":
        good = [c_ for c_ in combs if girls(c_) >= 2]
        ans = 1 - F(C(m, k) + w * C(m, k - 1), C(m + w, k))
        wq = "komissiyada ən azı 2 qızın olması"
        how = f"Tamamlayıcı: 0 qız — C({m}, {k}) = {C(m, k)}, 1 qız — {w}·C({m}, {k - 1}) = {w * C(m, k - 1)}. P = 1 − ({C(m, k)} + {w * C(m, k - 1)})/{C(m + w, k)}"
    elif kind == "more_g":
        good = [c_ for c_ in combs if girls(c_) > k - girls(c_)]
        ans = F(sum(C(w, j) * C(m, k - j) for j in range(k + 1) if j > k - j), C(m + w, k))
        wq = "komissiyada qızların oğlanlardan çox olması"
        how = "Σ C(" + str(w) + ", j)·C(" + str(m) + ", " + str(k) + " − j), j > " + str(k) + " − j, bölünsün C(" + str(m + w) + ", " + str(k) + ")"
    else:
        good = [c_ for c_ in combs if 0 < girls(c_) < k]
        ans = 1 - F(C(m, k) + C(w, k), C(m + w, k))
        wq = "komissiyada həm oğlan, həm də qızın olması"
        how = f"Tamamlayıcı: hamısı oğlan ({C(m, k)}) və ya hamısı qız ({C(w, k)}). P = 1 − {C(m, k) + C(w, k)}/{C(m + w, k)}"
    chk = F(len(good), len(combs))
    return dict(t=f"Sinifdə {m} oğlan və {w} qız var. Təsadüfi olaraq {k} nəfərlik komissiya seçilir. {wq[0].upper() + wq[1:]} ehtimalını tapın.",
                a=ans, d=[1 - ans, ans + F(1, C(m + w, k)), F(w, m + w), ans - F(1, C(m + w, k)), F(C(w, 2), C(m + w, k))],
                e=f"{how} = {show(ans)}.", chk=chk, diff=H)


def prob_seq_draw(r, g):
    while True:
        a, b = r.randint(2, 9), r.randint(2, 9)
        if a + b <= 14:
            break
    kind = r.choice(["second", "diff", "same3"])
    n = a + b
    balls = ["q"] * a + ["a"] * b
    if kind == "second":
        pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
        good = [p for p in pairs if balls[p[1]] == "q"]
        ans = F(a, n)
        t = f"Qutuda {a} qırmızı və {b} ağ şar var. Qaytarmadan ardıcıl iki şar götürülür. İkinci şarın qırmızı olması ehtimalını tapın."
        how = f"Tam ehtimal: {a}/{n}·{a - 1}/{n - 1} + {b}/{n}·{a}/{n - 1} = {show(ans)} (birinci şar haqqında məlumat olmadıqda ikinci şar da {a}/{n} ehtimalla qırmızıdır)."
        d = [F(a - 1, n - 1), F(a, n - 1), F(a * (a - 1), n * (n - 1)), F(b, n), F(a + 1, n)]
    elif kind == "diff":
        pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
        good = [p for p in pairs if balls[p[0]] != balls[p[1]]]
        ans = F(2 * a * b, n * (n - 1))
        t = f"Qutuda {a} qırmızı və {b} ağ şar var. Qaytarmadan ardıcıl iki şar götürülür. Şarların müxtəlif rəngdə olması ehtimalını tapın."
        how = f"P = {a}/{n}·{b}/{n - 1} + {b}/{n}·{a}/{n - 1} = {show(ans)}."
        d = [F(a * b, n * (n - 1)), F(2 * a * b, n * n), 1 - ans, F(a * b, C(n, 2) * 2), ans + F(1, n * (n - 1))]
    else:
        pairs = [(i, j, k) for i in range(n) for j in range(n) for k in range(n) if len({i, j, k}) == 3]
        good = [p for p in pairs if balls[p[0]] == balls[p[1]] == balls[p[2]]]
        ans = F(a * (a - 1) * (a - 2) + b * (b - 1) * (b - 2), n * (n - 1) * (n - 2))
        t = f"Qutuda {a} qırmızı və {b} ağ şar var. Qaytarmadan ardıcıl üç şar götürülür. Üç şarın eyni rəngdə olması ehtimalını tapın."
        how = f"P = ({a}·{a - 1}·{a - 2} + {b}·{b - 1}·{b - 2})/({n}·{n - 1}·{n - 2}) = {show(ans)}."
        d = [F(a ** 3 + b ** 3, n ** 3), 1 - ans, F(a * (a - 1) * (a - 2), n * (n - 1) * (n - 2)), ans * 2, ans + F(1, n)]
    return dict(t=t, a=ans, d=d, e=how, chk=F(len(good), len(pairs)), diff=H)


def prob_cond(r, g):
    kind = r.choice(["six_given_sum", "sum_given_diff", "double_given"])
    outs = list(product(range(1, 7), repeat=2))
    if kind == "six_given_sum":
        s = r.randint(7, 10)
        B = [o for o in outs if sum(o) >= s]
        A = [o for o in B if 6 in o]
        t = f"İki zər atılıb və xalların cəminin {s}-dən kiçik olmadığı məlumdur. Zərlərdən ən azı birində 6 düşməsi ehtimalını tapın.".replace(f"{s}-dən", abl(s))
        how = f"Cəmi ≥ {s} olan hallar: {len(B)}, onlardan 6 olanlar: {len(A)}."
    elif kind == "sum_given_diff":
        dd = r.randint(1, 3)
        s = r.randint(5, 9)
        B = [o for o in outs if abs(o[0] - o[1]) >= dd]
        A = [o for o in B if sum(o) <= s]
        t = f"İki zər atılıb və xalların fərqinin modulunun ən azı {dd} olduğu məlumdur. Xalların cəminin {s}-dən böyük olmaması ehtimalını tapın.".replace(f"{s}-dən", abl(s))
        how = f"|a − b| ≥ {dd}: {len(B)} hal, onlardan cəmi ≤ {s}: {len(A)}."
    else:
        s = r.choice([4, 6, 8, 10])
        B = [o for o in outs if sum(o) == s]
        A = [o for o in B if o[0] == o[1]]
        t = f"İki zər atılıb və xalların cəminin {s} olduğu məlumdur. Hər iki zərdə eyni xalın düşməsi ehtimalını tapın."
        how = f"Cəmi {s}: {len(B)} hal, onlardan cüt (a = b): {len(A)}."
    ans = F(len(A), len(B))
    chk = F(len(A), 36) / F(len(B), 36)
    return dict(t=t, a=ans, d=[F(len(A), 36), F(len(B), 36), 1 - ans, F(len(A) + 1, len(B)), F(len(A), len(B) + 1)],
                e=f"Şərti ehtimal: P(A|B) = P(AB)/P(B). {how} P = {show(ans)}.", chk=chk, diff=H)


def prob_binom(r, g):
    n = r.randint(4, 8)
    p = r.choice([F(1, 4), F(1, 5), F(1, 3), F(1, 2), F(2, 3)])
    k = r.randint(1, min(3, n - 1))
    kind = r.choice(["atleast", "exact"])
    chk = F(0)
    for seq in product([0, 1], repeat=n):
        h = sum(seq)
        if (h >= k if kind == "atleast" else h == k):
            chk += p ** h * (1 - p) ** (n - h)
    if kind == "atleast":
        ans = 1 - sum(C(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k))
        w = f"ən azı {k} sualı düzgün cavablandırması"
        how = f"P(X ≥ {k}) = 1 − Σ C({n}, j)·p^j·q^({n} − j), j = 0…{k - 1}"
        d = [1 - (1 - p) ** n, C(n, k) * p ** k * (1 - p) ** (n - k), p ** k, 1 - ans, ans + p ** n]
    else:
        ans = C(n, k) * p ** k * (1 - p) ** (n - k)
        w = f"düz {k} sualı düzgün cavablandırması"
        how = f"Bernulli düsturu: C({n}, {k})·p^{k}·q^{n - k}"
        d = [p ** k * (1 - p) ** (n - k), C(n, k) * p ** k, F(k, n), ans * 2, C(n, k - 1) * p ** k * (1 - p) ** (n - k)]
    nopt = {F(1, 4): 4, F(1, 5): 5, F(1, 3): 3, F(1, 2): 2}.get(p)
    if nopt:
        setup = f"Testdə {n} sual var, hər sualın {nopt} variantından biri düzgündür. Şagird bütün sualların cavabını təsadüfi seçir."
    else:
        setup = f"Basketbolçu topu səbətə {show(p)} ehtimalla salır. O, {n} atış edir (atışlar asılı deyil)."
        w = w.replace("sualı düzgün cavablandırması", "dəfə topu səbətə salması")
    return dict(t=f"{setup} Onun {w} ehtimalını tapın.", a=ans, d=d, e=f"p = {show(p)}, q = {show(1 - p)}. {how} = {show(ans)}.", chk=chk, diff=H)


def prob_total(r, g):
    while True:
        r1, w1, r2, w2 = r.randint(1, 8), r.randint(1, 8), r.randint(1, 8), r.randint(1, 8)
        t_ = r.randint(1, 5)
        if F(r1, r1 + w1) != F(r2, r2 + w2):
            break
    bayes = g == 11 and r.random() < 0.7
    # müstəqil: bütün (zər, şar) cütlərini çəkiləri ilə sadala
    num = den = F(0)
    for die in range(1, 7):
        urn = (r1, w1) if die <= t_ else (r2, w2)
        tot = sum(urn)
        for ball in range(tot):
            pr = F(1, 6) * F(1, tot)
            if ball < urn[0]:
                den += pr
                if die <= t_:
                    num += pr
    P1 = F(t_, 6)
    pr_red = P1 * F(r1, r1 + w1) + (1 - P1) * F(r2, r2 + w2)
    setup = (f"Birinci qutuda {r1} qırmızı və {w1} ağ, ikinci qutuda {r2} qırmızı və {w2} ağ şar var. Zər atılır: "
             f"{t_}-dən böyük olmayan xal düşərsə birinci qutudan, əks halda ikinci qutudan bir şar götürülür.".replace(f"{t_}-dən", abl(t_)))
    if not bayes:
        ans = pr_red
        return dict(t=f"{setup} Götürülən şarın qırmızı olması ehtimalını tapın.", a=ans,
                    d=[F(r1 + r2, r1 + w1 + r2 + w2), (F(r1, r1 + w1) + F(r2, r2 + w2)) / 2, P1 * F(r1, r1 + w1), 1 - ans, ans + F(1, 12)],
                    e=f"Tam ehtimal düsturu: {show(P1)}·{show(F(r1, r1 + w1))} + {show(1 - P1)}·{show(F(r2, r2 + w2))} = {show(ans)}.",
                    chk=den, diff=H)
    ans = P1 * F(r1, r1 + w1) / pr_red
    return dict(t=f"{setup} Götürülən şar qırmızı çıxıb. Onun birinci qutudan götürülməsi ehtimalını tapın.", a=ans,
                d=[P1 * F(r1, r1 + w1), F(r1, r1 + r2), P1, 1 - ans, pr_red],
                e=f"P(qırmızı) = {show(P1)}·{show(F(r1, r1 + w1))} + {show(1 - P1)}·{show(F(r2, r2 + w2))} = {show(pr_red)}. "
                  f"Bayes: P(I | qırmızı) = ({show(P1 * F(r1, r1 + w1))}) : ({show(pr_red)}) = {show(ans)}.", chk=num / den, diff=H)


def prob_digits(r, g):
    while True:
        digs = sorted(r.sample(range(0, 10), r.randint(5, 6)))
        k = 3
        div = r.choice([3, 4, 5, 6, 9, 25 if 0 in digs else 4])
        nums = [int("".join(map(str, p))) for p in permutations(digs, k) if p[0] != 0]
        good = [x for x in nums if x % div == 0]
        if 0 < len(good) < len(nums):
            break
    ans = F(len(good), len(nums))
    # müstəqil: bütün 3 rəqəmli ədədləri yoxla
    allx = [x for x in range(100, 1000) if len(set(str(x))) == 3 and all(int(c) in digs for c in str(x))]
    chk = F(sum(1 for x in allx if x % div == 0), len(allx))
    return dict(t=f"{', '.join(map(str, digs))} rəqəmlərindən rəqəmləri təkrarlanmayan üçrəqəmli ədəd təsadüfi düzəldilir. Ədədin {div}-ə bölünməsi ehtimalını tapın.".replace(f"{div}-ə", dat(div)),
                a=ans, d=[F(1, div), F(len(good), len(digs) ** 3), 1 - ans, F(len(good) + 1, len(nums)), F(len(good), len(nums) + len(digs))],
                e=f"Bütün ədədlər: {len(nums)} (birinci rəqəm 0 ola bilməz). {div}-ə bölünənlər: {len(good)}. P = {show(ans)}.".replace(f"{div}-ə", dat(div)),
                chk=chk, diff=H)


def prob_hyper_E(r, g):
    while True:
        a, b = r.randint(2, 7), r.randint(2, 8)
        k = r.randint(2, 4)
        if k < a + b and a + b <= 14:
            break
    n = a + b
    kind = r.choice(["E", "D", "E2"])
    balls = [1] * a + [0] * b
    combs = list(combinations(range(n), k))
    xs = [sum(balls[i] for i in c_) for c_ in combs]
    EX = F(sum(xs), len(xs))
    EX2 = F(sum(x * x for x in xs), len(xs))
    if kind == "E":
        ans, chk = F(k * a, n), EX
        w = "X-in riyazi gözləməsini"
        how = f"Hər şarın seçilmə ehtimalı {k}/{n}, M(X) = {a}·{k}/{n} = {show(ans)}."
        d = [F(k * b, n), F(a, n), F(k * a, n - 1), ans + F(1, n), F(k, 2)]
    elif kind == "D":
        ans = F(k * a * b * (n - k), n * n * (n - 1))
        chk = EX2 - EX ** 2
        w = "X-in dispersiyasını"
        how = f"Paylanma: P(X = j) = C({a}, j)·C({b}, {k} − j)/C({n}, {k}). M(X) = {show(EX)}, M(X²) = {show(EX2)}, D(X) = M(X²) − M(X)² = {show(ans)}."
        d = [F(k * a * b, n * n), EX2, EX, F(k * a * b * (n - k), n * n * n), ans * 2]
    else:
        ans, chk = EX2, EX2
        ans = F(k * a * b * (n - k), n * n * (n - 1)) + F(k * a, n) ** 2
        w = "X² təsadüfi kəmiyyətinin riyazi gözləməsini"
        how = f"M(X) = {show(EX)}, D(X) = {show(EX2 - EX ** 2)}, M(X²) = D(X) + M(X)² = {show(ans)}."
        d = [EX ** 2, EX, EX2 - EX ** 2, ans + 1, ans * 2]
    return dict(t=f"Qutuda {a} qırmızı və {b} ağ şar var. Eyni anda {k} şar götürülür. X — götürülən qırmızı şarların sayıdır. {w} tapın.",
                a=ans, d=d, e=how, chk=chk, diff=H)


def prob_table(r, g):
    while True:
        xs = sorted(r.sample(range(-5, 12), 4))
        den = r.choice([10, 12, 20, 8, 6])
        ps = [F(r.randint(1, den - 3), den) for _ in range(3)]
        p4 = 1 - sum(ps)
        if p4 > 0:
            break
    ps.append(p4)
    EX = sum(x * p for x, p in zip(xs, ps))
    DX = sum(x * x * p for x, p in zip(xs, ps)) - EX ** 2
    # müstəqil: ortaq məxrəclə "əhali" siyahısı və statistics.pvariance
    L = math.lcm(*[p.denominator for p in ps])
    pop = [x for x, p in zip(xs, ps) for _ in range(int(p * L))]
    kind = r.choice(["D", "find_x"])
    if kind == "D":
        ans, chk = DX, statistics.pvariance(pop)
        tbl = "; ".join(f"P(X = {neg(str(x))}) = {show(p)}" for x, p in zip(xs[:3], ps[:3])) + f"; X = {neg(str(xs[3]))} qiymətini alma ehtimalı məlum deyil"
        t = f"X diskret təsadüfi kəmiyyəti yalnız {', '.join(neg(str(x)) for x in xs)} qiymətlərini alır: {tbl}. D(X)-i tapın."
        how = f"P(X = {neg(str(xs[3]))}) = 1 − {show(sum(ps[:3]))} = {show(p4)}. M(X) = {show(EX)}, M(X²) = {show(EX + DX - EX + EX ** 2)}. D(X) = {show(DX)}."
        d = [sum(x * x * p for x, p in zip(xs, ps)), EX ** 2, DX + EX, DX * 2, sum(x * x * p for x, p in zip(xs[:3], ps[:3])) - EX ** 2]
    else:
        # x₄ naməlum, M(X) verilir
        ans = xs[3]
        tbl = "; ".join(f"P(X = {neg(str(x))}) = {show(p)}" for x, p in zip(xs[:3], ps[:3])) + f"; P(X = a) = {show(p4)}"
        t = f"X təsadüfi kəmiyyətinin paylanması: {tbl}. M(X) = {show(EX)} olarsa, a-nı tapın."
        sols = [z for z in range(-50, 51) if sum(x * p for x, p in zip(xs[:3], ps[:3])) + z * p4 == EX]
        chk = sols[0] if len(sols) == 1 else 999
        how = f"{show(sum(x * p for x, p in zip(xs[:3], ps[:3])))} + {show(p4)}·a = {show(EX)} ⇒ a = {ans}."
        d = [ans + 1, ans - 1, EX, ans + 2, -ans if ans else 3]
    return dict(t=t, a=ans, d=d, e=how, chk=chk, diff=H)


def prob_game(r, g):
    faces = 6
    cost = r.randint(1, 5)
    kind = r.choice(["double", "sum"])
    outs = list(product(range(1, faces + 1), repeat=2))
    if kind == "double":
        win = r.randint(5, 20)
        bonus = r.randint(2, 8)
        def gain(o):
            if o[0] == o[1]:
                return win - cost
            if sum(o) >= 10:
                return bonus - cost
            return -cost
        t = (f"Oyunda iştirak {cost} manatdır. İki zər atılır: eyni xal düşərsə oyunçu {win} manat, əks halda cəm 10 və ya daha çox olarsa {bonus} manat alır, "
             f"qalan hallarda heç nə almır. Oyunçunun xalis qazancının riyazi gözləməsini tapın (manatla).")
        nd = 6
        n10 = sum(1 for o in outs if o[0] != o[1] and sum(o) >= 10)
        ans = F(nd * win + n10 * bonus, 36) - cost
        how = f"P(cüt) = 6/36, P(cüt deyil, cəm ≥ 10) = {n10}/36. M = 6/36·{win} + {n10}/36·{bonus} − {cost} = {show(ans)}."
    else:
        s = r.randint(7, 11)
        win = r.randint(4, 20)
        def gain(o):
            return (win if sum(o) >= s else 0) - cost
        cnt = sum(1 for o in outs if sum(o) >= s)
        t = f"Oyunda iştirak {cost} manatdır. İki zər atılır: xalların cəmi {s} və ya daha çox olarsa oyunçu {win} manat alır. Oyunçunun xalis qazancının riyazi gözləməsini tapın (manatla)."
        ans = F(cnt * win, 36) - cost
        how = f"P(cəm ≥ {s}) = {cnt}/36. M = {cnt}/36·{win} − {cost} = {show(ans)}."
    chk = sum(F(gain(o), 36) for o in outs)
    return dict(t=t, a=ans, d=[ans + cost, -ans, ans - 1, ans + 1, ans + F(cost, 2)], e=how, chk=chk, diff=H)


def prob_Emax(r, g):
    faces = r.choice([4, 6, 8])
    kind = r.choice(["max", "absdiff", "min"])
    outs = list(product(range(1, faces + 1), repeat=2))
    f = {"max": max, "min": min, "absdiff": lambda a, b: abs(a - b)}[kind]
    vals = [f(*o) if kind != "absdiff" else abs(o[0] - o[1]) for o in outs]
    chk = F(sum(vals), len(vals))
    n = faces
    if kind == "max":
        ans = sum(F(k * (2 * k - 1), n * n) for k in range(1, n + 1))
        w, how = "ən böyüyünün", f"P(max = k) = (2k − 1)/{n * n}. M = Σ k(2k − 1)/{n * n} = {show(ans)}."
    elif kind == "min":
        ans = sum(F(k * (2 * (n - k) + 1), n * n) for k in range(1, n + 1))
        w, how = "ən kiçiyinin", f"P(min = k) = (2({n} − k) + 1)/{n * n}. M = {show(ans)}."
    else:
        ans = sum(F(2 * (n - k) * k, n * n) for k in range(1, n))
        w, how = "fərqinin modulunun", f"P(|a − b| = k) = 2({n} − k)/{n * n} (k ≥ 1). M = Σ k·2({n} − k)/{n * n} = {show(ans)}."
    name = {4: "tetraedr şəkilli (1–4)", 6: "adi (1–6)", 8: "səkkizüzlü (1–8)"}[faces]
    return dict(t=f"İki {name} zər atılır. Düşən xallardan {w} riyazi gözləməsini tapın.".replace("xallardan fərqinin", "xalların fərqinin"),
                a=ans, d=[F(n + 1, 2), ans + F(1, 2), ans - F(1, 2), F(n, 2), ans + F(1, n)], e=how, chk=chk, diff=H)


def prob_letters(r, g):
    words = [("AABBC", "A, A, B, B, C"), ("AABBCD", "A, A, B, B, C, D"), ("AAABB", "A, A, A, B, B"), ("AABBCC", "A, A, B, B, C, C"),
             ("AAABBC", "A, A, A, B, B, C"), ("AABCD", "A, A, B, C, D"), ("AAABC", "A, A, A, B, C"), ("AABBBC", "A, A, B, B, B, C")]
    w, shown = r.choice(words)
    kind = r.choice(["noadj", "Aends", "Afirst_together"])
    perms = list(permutations(w))  # kartlar fərqlənir (n! bərabər ehtimallı hal)
    if kind == "noadj":
        good = [p for p in perms if all(p[i] != p[i + 1] for i in range(len(p) - 1))]
        q = "heç bir eyni hərfin yan-yana düşməməsi"
    elif kind == "Aends":
        good = [p for p in perms if p[0] == "A" and p[-1] == "A"]
        q = "cərgənin hər iki kənarında A hərfinin olması"
    else:
        good = [p for p in perms if "".join(p).find("A" * w.count("A")) != -1]
        q = "bütün A hərflərinin yan-yana düşməsi"
    ans = F(len(good), len(perms))
    distinct = set(perms)
    chk = F(sum(1 for p in distinct if (p in set(good))), len(distinct))
    return dict(t=f"Üzərində {shown} hərfləri yazılmış {len(w)} kart təsadüfi qaydada bir cərgədə düzülür. {q[0].upper() + q[1:]} ehtimalını tapın.",
                a=ans, d=[1 - ans, F(len(good), len(perms) // 2) if len(good) * 2 <= len(perms) else ans / 2, ans * 2, ans + F(1, len(w)), F(1, len(w))],
                e=f"Bərabər ehtimallı fərqli düzülüşlər: {len(w)}!/(təkrarların faktorialları) = {len(distinct)}. Əlverişli: {sum(1 for p in distinct if p in set(good))}. P = {show(ans)}.",
                chk=chk, diff=H)


TOPICS = {
    "stat-avg": {9: [avg_new, avg_groups, avg_median_x, avg_freq, avg_pairwise],
                 10: [avg_variance, avg_transform, avg_median_x, avg_groups, avg_freq, avg_new]},
    "stat-prob": {9: [prob_urn_exact, prob_dice, prob_row, prob_shooters, prob_divis, prob_committee, prob_seq_draw],
                  10: [prob_cond, prob_binom, prob_total, prob_digits, prob_urn_exact, prob_committee, prob_row, prob_shooters],
                  11: [prob_total, prob_hyper_E, prob_table, prob_game, prob_Emax, prob_letters, prob_binom, prob_cond, prob_digits]},
}
