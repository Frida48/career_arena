"""Riyaziyyat · Həndəsə: geo-basic, geo-poly, geo-circle, geo-trig.

Hər cavab koordinatlarla qurulmuş fiqurda ölçülərək (chk) yoxlanır. Çertyojlar həmin koordinatlardan çəkilir.
"""
import math
from fractions import Fraction as F

import numpy as np

from mx import Num, M, H, show, neg, par, is_sq, surd, lin_surd, pi_mul, deg, simp_root
from svg import Fig, tri_from_sides, labeled_polygon, centroid

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


# ---------------- köməkçilər ----------------

def rt(x):
    """√x (x rasional) → F və ya Num"""
    x = F(x)
    if x < 0:
        return None
    n, d = x.numerator, x.denominator
    if is_sq(n) and is_sq(d):
        return F(math.isqrt(n), math.isqrt(d))
    return surd(F(1, d), n * d)


def mulrt(k, x):
    """k·√x"""
    v = rt(x)
    if v is None:
        return None
    if isinstance(v, F):
        return k * v
    return surd(F(k) * F(1, F(x).denominator), F(x).numerator * F(x).denominator)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def ang(v, a, b):
    """v təpəsində a-v-b bucağı, dərəcə"""
    ux, uy = a[0] - v[0], a[1] - v[1]
    wx, wy = b[0] - v[0], b[1] - v[1]
    c = (ux * wx + uy * wy) / (math.hypot(ux, uy) * math.hypot(wx, wy))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def inter(p1, p2, p3, p4):
    """p1p2 və p3p4 düz xətlərinin kəsişməsi"""
    A = np.array([[p2[0] - p1[0], p3[0] - p4[0]], [p2[1] - p1[1], p3[1] - p4[1]]], float)
    b = np.array([p3[0] - p1[0], p3[1] - p1[1]], float)
    t, _ = np.linalg.solve(A, b)
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def circ3(a, b, c):
    """üç nöqtədən keçən çevrə: mərkəz, radius"""
    A = np.array([[2 * (b[0] - a[0]), 2 * (b[1] - a[1])], [2 * (c[0] - a[0]), 2 * (c[1] - a[1])]], float)
    rhs = np.array([b[0] ** 2 - a[0] ** 2 + b[1] ** 2 - a[1] ** 2, c[0] ** 2 - a[0] ** 2 + c[1] ** 2 - a[1] ** 2], float)
    o = np.linalg.solve(A, rhs)
    return (o[0], o[1]), dist((o[0], o[1]), a)


def shoelace(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def foot(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / (ax * ax + ay * ay)
    return (a[0] + t * ax, a[1] + t * ay)


def tri_ok(a, b, c):
    return a + b > c and a + c > b and b + c > a


def heronian(maxs=30):
    out = []
    for a in range(3, maxs + 1):
        for b in range(a, maxs + 1):
            for c in range(b, min(a + b, maxs + 1)):
                s16 = (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)
                if s16 > 0 and is_sq(s16) and math.isqrt(s16) % 4 == 0:
                    out.append((a, b, c, math.isqrt(s16) // 4))
    return out


HERON = heronian()


def sides_fig(names, P, labels):
    fig = labeled_polygon(names, P)
    g = centroid(P)
    for (i, j), t in labels.items():
        fig.side(P[i], P[j], t, inside=g)
    return fig


# ======================= geo-basic =======================

def tri_altitude(r, g):
    while True:
        p, q = r.randint(1, 16), r.randint(1, 16)
        if p != q and not is_sq(p * q) or (g == 9 and p != q):
            break
    c = p + q
    h = math.sqrt(p * q)
    A, B, Hh, C = (0.0, 0.0), (float(c), 0.0), (float(p), 0.0), (float(p), h)
    fig = Fig().poly([A, B, C]).seg(C, Hh, dash=True).right(Hh, B, C).right(C, A, B)
    gc = centroid([A, B, C])
    for nm, pt in (("A", A), ("B", B), ("C", C)):
        fig.label(pt, nm, away=gc)
    fig.label(Hh, "H", away=C)
    fig.side(A, Hh, str(p), inside=C)
    fig.side(Hh, B, str(q), inside=C)
    kind = r.choice(["leg", "h", "area"] if g != 11 else ["leg2"])
    if kind == "leg":
        a = rt(p * c)
        chk = dist(A, C)
        t = f"ABC düzbucaqlı üçbucağında (∠C = 90°) CH hündürlüyü hipotenuzu AH = {p} və HB = {q} parçalarına bölür. AC katetini tapın."
        e = f"AC² = AH·AB = {p}·{c} = {p * c} ⇒ AC = {show(a)}."
        d = [rt(q * c), rt(p * q), rt(p * p + q * q), rt(c * c - p * p), rt(2 * p * c)]
    elif kind == "h":
        a = rt(p * q)
        chk = h
        t = f"ABC düzbucaqlı üçbucağında (∠C = 90°) CH hündürlüyü hipotenuzu AH = {p} və HB = {q} parçalarına bölür. CH hündürlüyünü tapın."
        e = f"CH² = AH·HB = {p}·{q} = {p * q} ⇒ CH = {show(a)}."
        d = [rt(p * c), rt(q * c), rt(F(p + q, 2) ** 2), rt(p * p + q * q), rt(2 * p * q)]
    elif kind == "area":
        a = mulrt(F(c, 2), p * q)
        chk = shoelace([A, B, C])
        t = f"ABC düzbucaqlı üçbucağında (∠C = 90°) CH hündürlüyü hipotenuzu AH = {p} və HB = {q} parçalarına bölür. Üçbucağın sahəsini tapın."
        e = f"CH = √(AH·HB) = {show(rt(p * q))}. S = AB·CH/2 = {c}·{show(rt(p * q))}/2 = {show(a)}."
        d = [mulrt(c, p * q), mulrt(F(p, 2), p * q), mulrt(F(c, 4), p * q), mulrt(F(c, 2), p * c), mulrt(F(q, 2), p * q)]
    else:  # 11: AC və AH verilir, BC tapılır
        ac2 = p * c
        a = rt(q * c)
        chk = dist(B, C)
        fig = Fig().poly([A, B, C]).seg(C, Hh, dash=True).right(Hh, B, C).right(C, A, B)
        for nm, pt in (("A", A), ("B", B), ("C", C)):
            fig.label(pt, nm, away=gc)
        fig.label(Hh, "H", away=C)
        fig.side(A, Hh, str(p), inside=C)
        fig.side(A, C, show(rt(ac2)), inside=B)
        t = f"ABC düzbucaqlı üçbucağında (∠C = 90°) CH hündürlükdür. AC = {show(rt(ac2))} və AH = {p} olarsa, BC katetini tapın."
        e = f"AC² = AH·AB ⇒ AB = {ac2}/{p} = {c}. HB = {c} − {p} = {q}. BC² = HB·AB = {q}·{c} ⇒ BC = {show(a)}."
        d = [rt(p * q), rt(c * c + ac2), rt(ac2 - p * p), rt(p * c), rt(q * q + p * p)]
    return dict(t=t, a=a, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def tri_bisector(r, g):
    while True:
        a, b, c = r.randint(4, 20), r.randint(4, 20), r.randint(4, 20)
        if tri_ok(a, b, c) and b != c and len({a, b, c}) == 3:
            break
    A, B, C = tri_from_sides(a, b, c)
    # müstəqil: bucağın tənböləninin istiqaməti ilə BC-nin kəsişməsi
    ub = ((B[0] - A[0]) / c, (B[1] - A[1]) / c)
    uc = ((C[0] - A[0]) / b, (C[1] - A[1]) / b)
    Dp = inter(A, (A[0] + ub[0] + uc[0], A[1] + ub[1] + uc[1]), B, C)
    fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(c), (2, 0): str(b), (1, 2): str(a)}).seg(A, Dp, dash=True)
    fig.label(Dp, "D", away=A)
    kind = "bd" if g == 9 else r.choice(["ad", "bd"]) if g == 10 else "ad"
    if kind == "bd":
        ans = F(a * c, b + c)
        chk = dist(B, Dp)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, BC = {a}. AD — A bucağının tənbölənidir (D ∈ BC). BD parçasını tapın."
        e = f"Tənbölən xassəsi: BD : DC = AB : AC = {c} : {b}. BD = {a}·{c}/({c} + {b}) = {show(ans)}."
        d = [F(a * b, b + c), F(a, 2), F(a * c, b), F(c * c, b + c), ans + 1]
    else:
        ans = rt(F(b * c * ((b + c) ** 2 - a * a), (b + c) ** 2))
        chk = dist(A, Dp)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, BC = {a}. A bucağının tənbölənini (AD) tapın."
        e = (f"BD = {show(F(a * c, b + c))}, DC = {show(F(a * b, b + c))}. AD² = AB·AC − BD·DC = {b * c} − {show(F(a * a * b * c, (b + c) ** 2))} "
             f"= {show(F(b * c * ((b + c) ** 2 - a * a), (b + c) ** 2))} ⇒ AD = {show(ans)}.")
        d = [rt(F(b * c, 1)), rt(F(b * c * ((b + c) ** 2 - a * a), (b + c) ** 2) + 1), rt(F(2 * b * b + 2 * c * c - a * a, 4)),
             rt(b * c - F(a * a, 4)), rt(F(b * c * ((b + c) ** 2 + a * a), (b + c) ** 2))]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def tri_median(r, g):
    while True:
        a, b, c = r.randint(3, 18), r.randint(3, 18), r.randint(3, 18)
        if tri_ok(a, b, c) and len({a, b, c}) == 3:
            break
    A, B, C = tri_from_sides(a, b, c)
    Mp = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    m2 = F(2 * b * b + 2 * c * c - a * a, 4)
    if g == 11:
        # mediana verilir, üçüncü tərəf tapılır
        ans = rt(a * a)
        ans = F(a)
        chk = dist(B, C)
        fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(c), (2, 0): str(b)}).seg(A, Mp, dash=True)
        fig.label(Mp, "M", away=A)
        fig.side(A, Mp, show(rt(m2)), inside=B)
        t = f"ABC üçbucağında AB = {c}, AC = {b} və AM medianı {show(rt(m2))}-ə bərabərdir. BC tərəfini tapın.".replace(f"{show(rt(m2))}-ə bərabərdir", f"= {show(rt(m2))}").replace("medianı =", "medianı")
        t = f"ABC üçbucağında AB = {c}, AC = {b}, AM medianı isə {show(rt(m2))}. BC tərəfini tapın."
        e = f"4AM² = 2AB² + 2AC² − BC² ⇒ BC² = {2 * c * c} + {2 * b * b} − {show(4 * m2)} = {a * a}, BC = {a}."
        d = [rt(2 * b * b + 2 * c * c - m2), rt(b * b + c * c), rt(F(b * b + c * c, 2)), F(a + 1), F(a - 1), rt(2 * b * b + 2 * c * c - 2 * m2)]
    else:
        ans = rt(m2)
        chk = dist(A, Mp)
        fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(c), (2, 0): str(b), (1, 2): str(a)}).seg(A, Mp, dash=True)
        fig.label(Mp, "M", away=A)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, BC = {a}. A təpəsindən çəkilmiş AM medianını tapın."
        e = f"m² = (2AB² + 2AC² − BC²)/4 = ({2 * c * c} + {2 * b * b} − {a * a})/4 = {show(m2)} ⇒ AM = {show(ans)}."
        d = [rt(F(2 * b * b + 2 * c * c + a * a, 4)), rt(F(b * b + c * c, 2)), rt(F(2 * b * b + 2 * c * c - a * a, 2)), rt(m2 + 1), rt(b * c)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M if g == 10 else H)


def _tri_angles(Aa, Bb):
    """bucaqlarla üçbucaq: A=(0,0), B=(1,0)"""
    A, B = (0.0, 0.0), (1.0, 0.0)
    ta, tb = math.radians(Aa), math.radians(Bb)
    C = inter(A, (math.cos(ta), math.sin(ta)), B, (1 - math.cos(tb), math.sin(tb)))
    return A, B, C


def tri_angle_chase(r, g):
    while True:
        Aa, Bb = r.randint(20, 110), r.randint(20, 110)
        Cc = 180 - Aa - Bb
        if Cc >= 20 and Aa != Bb and Aa % 2 == 0 and Bb % 2 == 0:
            break
    A, B, C = _tri_angles(Aa, Bb)
    a, b, c = dist(B, C), dist(A, C), dist(A, B)
    kind = r.choice(["incenter", "alt_bis"] if g != 11 else ["alt_bis", "ext"])
    if kind == "incenter":
        I = ((a * A[0] + b * B[0] + c * C[0]) / (a + b + c), (a * A[1] + b * B[1] + c * C[1]) / (a + b + c))
        ans = F(90) + F(Cc, 2)
        chk = ang(I, A, B)
        fig = labeled_polygon(["A", "B", "C"], [A, B, C]).seg(A, I, dash=True).seg(B, I, dash=True).dot(I)
        fig.label(I, "O", away=C)
        t = f"ABC üçbucağında ∠A = {Aa}°, ∠B = {Bb}°. A və B bucaqlarının tənbölənləri O nöqtəsində kəsişir. ∠AOB-ni tapın."
        e = f"∠C = 180° − {Aa}° − {Bb}° = {Cc}°. ∠AOB = 180° − (∠A + ∠B)/2 = 90° + ∠C/2 = {show(ans)}°."
        d = [F(Aa + Bb, 2), F(180 - Cc), F(90) + F(Aa, 2), 180 - F(Cc, 2), ans + 10]
    elif kind == "alt_bis":
        Hh = foot(C, A, B)
        L = inter(C, (C[0] + (A[0] - C[0]) / b + (B[0] - C[0]) / a, C[1] + (A[1] - C[1]) / b + (B[1] - C[1]) / a), A, B)
        ans = F(abs(Aa - Bb), 2)
        chk = ang(C, Hh, L)
        fig = labeled_polygon(["A", "B", "C"], [A, B, C]).seg(C, Hh, dash=True).seg(C, L, dash=True).right(Hh, B, C)
        fig.label(Hh, "H", away=C)
        fig.label(L, "L", away=C)
        t = f"ABC üçbucağında ∠A = {Aa}°, ∠B = {Bb}°. CH hündürlüyü ilə CL tənböləni arasındakı bucağı tapın."
        e = (f"∠C = {Cc}°, ∠ACL = {show(F(Cc, 2))}°. ∠ACH = 90° − ∠A = {90 - Aa}°. "
             f"Aradakı bucaq |{show(F(Cc, 2))}° − ({90 - Aa}°)| = |∠A − ∠B|/2 = {show(ans)}°.")
        d = [F(abs(Aa - Bb)), F(Cc, 2), F(Aa + Bb, 4), ans + 5, abs(ans - 5)]
    else:
        # A-nın xarici bucağının tənböləni ilə B-nin daxili tənböləni kəsişir: ∠ = C/2
        ext_dir = (-(B[0] - A[0]) / c + (C[0] - A[0]) / b, -(B[1] - A[1]) / c + (C[1] - A[1]) / b)
        bis_b = ((A[0] - B[0]) / c + (C[0] - B[0]) / a, (A[1] - B[1]) / c + (C[1] - B[1]) / a)
        K = inter(A, (A[0] + ext_dir[0], A[1] + ext_dir[1]), B, (B[0] + bis_b[0], B[1] + bis_b[1]))
        ans = F(Cc, 2)
        chk = ang(K, A, B)
        fig = labeled_polygon(["A", "B", "C"], [A, B, C]).seg(B, K, dash=True).seg(A, K, dash=True)
        fig.label(K, "K", away=B)
        t = (f"ABC üçbucağında ∠A = {Aa}°, ∠B = {Bb}°. B bucağının tənböləni ilə A təpəsindəki xarici bucağın tənböləni K nöqtəsində kəsişir. "
             f"∠AKB-ni tapın.")
        e = (f"∠C = {Cc}°. ABK üçbucağında ∠KBA = {show(F(Bb, 2))}°, ∠KAB = ∠A + (180° − ∠A)/2 = {show(Aa + F(180 - Aa, 2))}°. "
             f"∠AKB = 180° − {show(F(Bb, 2))}° − {show(Aa + F(180 - Aa, 2))}° = ∠C/2 = {show(ans)}°.")
        d = [F(Cc), F(90) - F(Cc, 2), F(90) + F(Cc, 2), F(Aa, 2), ans + 10]
    return dict(t=t, a=Num(show(ans) + "°", ans), d=[Num(show(x) + "°", x) for x in d], e=e, chk=chk, img=fig.render(), diff=M)


def tri_iso_angle(r, g):
    al = r.choice(range(8, 58, 2))
    base = F(180 - al, 2)
    ans = base - al
    # koordinatlar: B(−1,0), C(1,0), A(0, h)
    hgt = math.tan(math.radians(float(base)))
    A, B, C = (0.0, hgt), (-1.0, 0.0), (1.0, 0.0)
    # D ∈ AC, BD = BC = 2 (D ≠ C)
    # BD = 2 çevrəsi ilə AC düz xəttinin kəsişməsi: C + t(A − C), |P − B|² = 4
    ux, uy = A[0] - C[0], A[1] - C[1]
    wx, wy = C[0] - B[0], C[1] - B[1]
    qa, qb, qc = ux * ux + uy * uy, 2 * (ux * wx + uy * wy), wx * wx + wy * wy - 4
    ts = [(-qb + sg_ * math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa) for sg_ in (1, -1)]
    tt = [t for t in ts if 1e-9 < t <= 1 + 1e-12]
    Dp = (C[0] + tt[0] * ux, C[1] + tt[0] * uy)
    best = (0.0, Dp)
    chk = ang(B, A, Dp)
    fig = labeled_polygon(["A", "B", "C"], [A, B, C]).seg(B, Dp, dash=True)
    fig.label(Dp, "D", away=B)
    return dict(t=f"ABC bərabəryanlı üçbucağında AB = AC və ∠A = {al}°. AC tərəfi üzərində D nöqtəsi elə götürülüb ki, BD = BC. ∠ABD-ni tapın.",
                a=Num(show(ans) + "°", ans), d=[Num(show(x) + "°", x) for x in (base, F(al), 180 - 2 * base, base - F(al, 2), ans + 6)],
                e=f"∠B = ∠C = (180° − {al}°)/2 = {show(base)}°. BDC bərabəryanlıdır: ∠BDC = ∠C, ∠DBC = 180° − 2·{show(base)}° = {al}°. "
                  f"∠ABD = {show(base)}° − {al}° = {show(ans)}°.", chk=chk if abs(best[0]) < 1e-3 else 999, img=fig.render(), diff=H)


def tri_heron(r, g):
    a, b, c, S = r.choice([t for t in HERON if t[2] <= 30])
    sides = [a, b, c]
    r.shuffle(sides)
    BC, CA, AB = sides
    A, B, C = tri_from_sides(BC, CA, AB)
    kind = r.choice(["h", "r"] if g == 9 else ["h", "r", "R"] if g == 10 else ["R", "r", "hR"])
    fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(AB), (2, 0): str(CA), (1, 2): str(BC)})
    p = F(a + b + c, 2)
    head = f"Üçbucağın tərəfləri AB = {AB}, AC = {CA}, BC = {BC}-dir.".replace(f"BC = {BC}-dir", f"BC = {BC}")
    head = f"ABC üçbucağında AB = {AB}, AC = {CA}, BC = {BC}."
    heron = f"p = {show(p)}, S = √(p(p − a)(p − b)(p − c)) = {S}."
    if kind == "h":
        big = max(sides)
        ans = F(2 * S, big)
        name = {BC: "BC", CA: "AC", AB: "AB"}[big]
        opp = {"BC": A, "AC": B, "AB": C}[name]
        ends = {"BC": (B, C), "AC": (A, C), "AB": (A, B)}[name]
        chk = dist(opp, foot(opp, *ends))
        fig.seg(opp, foot(opp, *ends), dash=True)
        t = f"{head} Ən böyük tərəfə endirilmiş hündürlüyü tapın."
        e = f"{heron} h = 2S/{big} = {show(ans)}."
        d = [F(S, big), F(2 * S, min(sides)), F(2 * S, sorted(sides)[1]), ans + 1, F(4 * S, big)]
    elif kind == "r":
        ans = S / p
        I = ((BC * A[0] + CA * B[0] + AB * C[0]) / (a + b + c), (BC * A[1] + CA * B[1] + AB * C[1]) / (a + b + c))
        chk = dist(I, foot(I, A, B))
        fig.circle(I, chk)
        t = f"{head} Üçbucağa daxil çəkilmiş çevrənin radiusunu tapın."
        e = f"{heron} r = S/p = {S}/{show(p)} = {show(ans)}."
        d = [S / (2 * p), 2 * S / p, F(a * b * c, 4 * S), ans + 1, F(S, a + b + c) * 3]
    elif kind == "R":
        ans = F(a * b * c, 4 * S)
        O, Rr = circ3(A, B, C)
        chk = Rr
        fig.circle(O, Rr)
        t = f"{head} Üçbucağa xaricdən çəkilmiş çevrənin radiusunu tapın."
        e = f"{heron} R = abc/(4S) = {a * b * c}/{4 * S} = {show(ans)}."
        d = [F(a * b * c, 2 * S), S / p, F(max(sides), 2), ans + 1, F(a * b * c, 4 * S + 4)]
    else:
        R_ = F(a * b * c, 4 * S)
        r_ = S / p
        ans = R_ * r_
        O, Rr = circ3(A, B, C)
        I = ((BC * A[0] + CA * B[0] + AB * C[0]) / (a + b + c), (BC * A[1] + CA * B[1] + AB * C[1]) / (a + b + c))
        chk = Rr * dist(I, foot(I, A, B))
        t = f"{head} Daxilə və xaricə çəkilmiş çevrələrin radiuslarının hasilini (r·R) tapın."
        e = f"{heron} r = S/p = {show(r_)}, R = abc/(4S) = {show(R_)}. r·R = {show(ans)}."
        d = [R_ + r_, F(a * b * c, 4 * (a + b + c)) * 2, R_ * r_ * 2, ans + 1, F(a * b * c, 2 * (a + b + c)) + 1]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def tri_cos120_median(r, g):
    ang_ = r.choice([60, 120])
    while True:
        b, c = r.randint(2, 12), r.randint(2, 12)
        if b != c:
            break
    cosA = F(1, 2) if ang_ == 60 else F(-1, 2)
    a2 = b * b + c * c - 2 * b * c * cosA
    m2 = F(2 * b * b + 2 * c * c - a2, 4)
    ans = rt(m2)
    A = (0.0, 0.0)
    B = (float(c), 0.0)
    C = (b * math.cos(math.radians(ang_)), b * math.sin(math.radians(ang_)))
    Mp = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(c), (2, 0): str(b)}).seg(A, Mp, dash=True).arc(A, B, C, f"{ang_}°")
    fig.label(Mp, "M", away=A)
    return dict(t=f"ABC üçbucağında AB = {c}, AC = {b}, ∠A = {ang_}°. AM medianını tapın.", a=ans,
                d=[rt(a2), rt(F(a2, 4)), rt(F(b * b + c * c, 2)), rt(F(2 * b * b + 2 * c * c + a2, 4)), rt(m2 + b * c)],
                e=f"Əvvəlcə BC² = {b}² + {c}² − 2·{b}·{c}·cos {ang_}° = {show(a2)}. "
                  f"Sonra AM² = (2AB² + 2AC² − BC²)/4 = ({2 * c * c} + {2 * b * b} − {show(a2)})/4 = {show(m2)} ⇒ AM = {show(ans)}.",
                chk=dist(A, Mp), img=fig.render(), diff=H)


# ======================= geo-poly =======================

def poly_diagonals(r, g):
    n = r.choice([n for n in range(5, 37) if 360 % n == 0 or g != 9])
    kind = "angle" if (360 % n == 0 and r.random() < 0.6) else "sum"
    if kind == "angle":
        angv = F(180 * (n - 2), n)
        t = f"Düzgün çoxbucaqlının daxili bucağı {show(angv)}°-dir. Onun neçə diaqonalı var?".replace(f"{show(angv)}°-dir", f"{show(angv)}°")
        t = f"Düzgün çoxbucaqlının hər daxili bucağı {show(angv)}° olarsa, onun neçə diaqonalı var?"
        found = [m for m in range(3, 400) if F(180 * (m - 2), m) == angv]
        e = f"Xarici bucaq 180° − {show(angv)}° = {show(180 - angv)}°, n = 360 : {show(180 - angv)} = {n}. Diaqonallar: n(n − 3)/2 = {n * (n - 3) // 2}."
    else:
        tot = 180 * (n - 2)
        t = f"Qabarıq çoxbucaqlının daxili bucaqlarının cəmi {tot}° olarsa, onun neçə diaqonalı var?"
        found = [m for m in range(3, 400) if 180 * (m - 2) == tot]
        e = f"180°(n − 2) = {tot}° ⇒ n = {n}. Diaqonallar: n(n − 3)/2 = {n * (n - 3) // 2}."
    ans = n * (n - 3) // 2
    m = found[0]
    return dict(t=t, a=ans, d=[n * (n - 3), n * (n - 2) // 2, (n - 3), (n + 1) * (n - 2) // 2, (n - 1) * (n - 4) // 2],
                e=e, chk=m * (m - 3) // 2, diff=M)


def poly_rhombus(r, g):
    a0, b0, c0 = r.choice(TRIPLES[:5])
    k = r.randint(1, 3)
    p, q, s = a0 * k, b0 * k, c0 * k  # yarımdiaqonallar və tərəf
    d1, d2 = 2 * p, 2 * q
    P = [(0.0, float(q)), (float(p), 0.0), (0.0, float(-q)), (float(-p), 0.0)]
    fig = labeled_polygon(["A", "B", "C", "D"], P).seg(P[0], P[2], dash=True).seg(P[1], P[3], dash=True)
    kind = r.choice(["h", "r"] if g != 11 else ["h_from_side", "r"])
    if kind == "h":
        ans = F(d1 * d2, 2 * s)
        chk = dist(P[0], foot(P[0], P[2], P[3]))
        t = f"Rombun diaqonalları {d1} və {d2}-dir. Rombun hündürlüyünü tapın.".replace(f"{d2}-dir", f"{d2}")
        t = f"Rombun diaqonalları {d1} və {d2} olarsa, onun hündürlüyünü tapın."
        e = f"Tərəf: √({p}² + {q}²) = {s}. S = d₁d₂/2 = {d1 * d2 // 2}. h = S/a = {d1 * d2 // 2}/{s} = {show(ans)}."
        d = [F(d1 * d2, 4 * s), F(d1 * d2, s), F(d1 + d2, 2), ans + 1, F(p * q, s * 2)]
    elif kind == "r":
        ans = F(p * q, s)
        chk = dist((0.0, 0.0), foot((0.0, 0.0), P[0], P[1]))
        fig.circle((0.0, 0.0), chk)
        t = f"Rombun diaqonalları {d1} və {d2} olarsa, ona daxil çəkilmiş çevrənin radiusunu tapın."
        e = f"Tərəf {s}. Radius hündürlüyün yarısıdır: r = (d₁d₂/2)/(2a) = {d1 * d2 // 2}/{2 * s} = {show(ans)}."
        d = [F(d1 * d2, 2 * s), F(p * q, 2 * s), F(s, 2), ans + 1, F(p + q, 2)]
    else:
        # tərəf və bir diaqonal verilir
        ans = F(d1 * d2, 2 * s)
        chk = dist(P[0], foot(P[0], P[2], P[3]))
        t = f"Rombun tərəfi {s}, diaqonallarından biri {d1} olarsa, rombun hündürlüyünü tapın."
        e = f"İkinci yarımdiaqonal √({s}² − {p}²) = {q}, d₂ = {d2}. S = {d1}·{d2}/2 = {d1 * d2 // 2}. h = S/a = {show(ans)}."
        d = [F(d1 * d2, 4 * s), F(d1 * d2, s), F(d1 * s, 2 * s + 1), ans + 1, F(q * 2, 1)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M)


def poly_trapezoid(r, g):
    while True:
        b = r.randint(2, 14)
        a = b + 2 * r.randint(1, 8)
        c = r.randint(F(a - b, 2).numerator + 1, 20)
        x = F(a - b, 2)
        if c > x:
            break
    h2 = c * c - x * x
    A, B, C, D = (0.0, 0.0), (float(a), 0.0), (float(a - x), math.sqrt(h2)), (float(x), math.sqrt(h2))
    fig = sides_fig(["A", "B", "C", "D"], [A, B, C, D], {(0, 1): str(a), (2, 3): str(b), (1, 2): str(c), (3, 0): str(c)})
    kind = r.choice(["diag", "area"] if g != 11 else ["diag", "area", "mid"])
    if kind == "diag":
        ans = rt(h2 + (a - x) ** 2)
        chk = dist(A, C)
        fig.seg(A, C, dash=True)
        t = f"Bərabəryanlı trapesiyanın oturacaqları {a} və {b}, yan tərəfi {c} olarsa, onun diaqonalını tapın."
        e = f"Hündürlük: h² = {c}² − (({a} − {b})/2)² = {show(h2)}. Diaqonalın proyeksiyası ({a} + {b})/2 = {show(F(a + b, 2))}. d = √({show(h2)} + {show(F(a + b, 2) ** 2)}) = {show(ans)}."
        d = [rt(h2 + a * a), rt(c * c + b * b), rt(h2 + x * x), rt(a * b + c * c + 1), rt(h2 + F(a, 1) ** 2 - 1)]
    elif kind == "area":
        ans = mulrt(F(a + b, 2), h2)
        chk = shoelace([A, B, C, D])
        t = f"Bərabəryanlı trapesiyanın oturacaqları {a} və {b}, yan tərəfi {c} olarsa, onun sahəsini tapın."
        e = f"h = √({c}² − {show(x)}²) = {show(rt(h2))}. S = ({a} + {b})/2 · h = {show(ans)}."
        d = [mulrt(a + b, h2), mulrt(F(a + b, 2), c * c), F(a + b, 2) * c, mulrt(F(a + b, 4), h2), mulrt(F(a + b, 2), h2 + 1)]
    else:
        # diaqonalların kəsişmə nöqtəsindən böyük oturacağa qədər məsafə
        ans = mulrt(F(a, a + b), h2)
        O = inter(A, C, B, D)
        chk = O[1]
        fig.seg(A, C, dash=True).seg(B, D, dash=True).dot(O)
        fig.label(O, "O", away=A)
        t = f"Bərabəryanlı trapesiyanın oturacaqları AB = {a}, CD = {b}, yan tərəfi {c}. Diaqonallar O nöqtəsində kəsişir. O nöqtəsindən AB-yə qədər məsafəni tapın."
        e = f"h = {show(rt(h2))}. AOB ~ COD, oxşarlıq əmsalı {a} : {b}, deməli O hündürlüyü {a} : {b} nisbətində bölür: {a}/({a} + {b})·h = {show(ans)}."
        d = [mulrt(F(b, a + b), h2), mulrt(F(1, 2), h2), mulrt(F(a, b), h2), mulrt(F(a, a + b), h2 + 1), mulrt(F(2 * a, a + b), h2)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def poly_parallelogram(r, g):
    angd = r.choice([60, 120, 45, 135, 30, 150]) if g != 9 else r.choice([60, 120])
    a, b = r.randint(2, 14), r.randint(2, 14)
    if a == b:
        b += 1
    cos_v = {60: F(1, 2), 120: F(-1, 2)}.get(angd)
    A = (0.0, 0.0)
    B = (float(a), 0.0)
    D = (b * math.cos(math.radians(angd)), b * math.sin(math.radians(angd)))
    C = (B[0] + D[0], B[1] + D[1])
    fig = sides_fig(["A", "B", "C", "D"], [A, B, C, D], {(0, 1): str(a), (3, 0): str(b)}).arc(A, B, D, f"{angd}°")
    if angd in (60, 120):
        kind = r.choice(["long", "short"])
        dl2 = a * a + b * b + a * b
        ds2 = a * a + b * b - a * b
        big_at_A = angd == 120  # A-dakı bucaq korsa, BD uzun diaqonaldır
        if kind == "long":
            ans = rt(dl2)
            chk = max(dist(A, C), dist(B, D))
            w = "böyük"
        else:
            ans = rt(ds2)
            chk = min(dist(A, C), dist(B, D))
            w = "kiçik"
        fig.seg(A, C, dash=True).seg(B, D, dash=True)
        t = f"Paraleloqramın tərəfləri {a} və {b}, aralarındakı bucaq {angd}° olarsa, onun {w} diaqonalını tapın."
        e = (f"Kosinuslar teoremi: d² = {a}² + {b}² ∓ 2·{a}·{b}·cos 60°. Böyük diaqonal √{dl2}, kiçik diaqonal √{ds2}. Cavab: {show(ans)}.")
        d = [rt(ds2 if kind == "long" else dl2), rt(a * a + b * b), rt(2 * (a * a + b * b)), rt((dl2 if kind == "long" else ds2) + a * b), F(a + b)]
    else:
        s_ = {45: (F(1, 2), 2), 135: (F(1, 2), 2), 30: (F(1, 2), 1), 150: (F(1, 2), 1)}[angd]
        ans = surd(a * b * s_[0], s_[1]) if s_[1] != 1 else F(a * b, 2)
        chk = shoelace([A, B, C, D])
        t = f"Paraleloqramın tərəfləri {a} və {b}, aralarındakı bucaq {angd}° olarsa, onun sahəsini tapın."
        e = f"S = a·b·sin {angd}° = {a}·{b}·{'√2/2' if s_[1] == 2 else '1/2'} = {show(ans)}."
        d = [F(a * b), surd(a * b, 2) if s_[1] == 2 else F(a * b, 4), surd(F(a * b, 2), 3), F(a * b, 2) if s_[1] == 2 else surd(F(a * b, 2), 2),
             surd(F(a * b, 4), 2)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M)


def poly_rect_bisector(r, g):
    m, n = r.randint(1, 6), r.randint(1, 6)
    k = r.randint(1, 5)
    x, y = m * k, n * k  # BK = AB = x, KC = y
    P_ = 2 * (x + x + y)
    A, B, C, D = (0.0, 0.0), (0.0, float(x)), (float(x + y), float(x)), (float(x + y), 0.0)
    K = inter(A, (1.0, 1.0), B, C)
    fig = labeled_polygon(["A", "B", "C", "D"], [A, B, C, D]).seg(A, K, dash=True)
    fig.label(K, "K", away=A)
    kind = r.choice(["area", "perim"])
    if kind == "area":
        ans = x * (x + y)
        chk = shoelace([A, B, C, D])
        t = f"ABCD düzbucaqlısında A bucağının tənböləni BC tərəfini K nöqtəsində BK : KC = {m} : {n} nisbətində bölür. Düzbucaqlının perimetri {P_} olarsa, sahəsini tapın."
        e = f"∠BAK = 45° ⇒ AB = BK = {m}t, BC = {m + n}t. Perimetr 2({2 * m + n}t) = {P_} ⇒ t = {k}. S = {x}·{x + y} = {ans}."
        d = [x * x, (x + y) * (x + y), ans + x, ans - x, x * (x + y) // 2 if (x * (x + y)) % 2 == 0 else ans + 2 * k]
    else:
        ans = P_
        chk = 2 * (dist(A, B) + dist(B, C))
        t = f"ABCD düzbucaqlısında A bucağının tənböləni BC tərəfini K nöqtəsində kəsir. BK = {x}, KC = {y} olarsa, düzbucaqlının perimetrini tapın."
        e = f"∠BAK = ∠AKB = 45°, ABK bərabəryanlıdır: AB = BK = {x}. BC = {x + y}. P = 2({x} + {x + y}) = {ans}."
        d = [2 * (x + y), 2 * (2 * y + x), ans + 2 * x, ans - 2 * y if ans - 2 * y > 0 else ans + 4, 2 * (x + y) + x]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M)


def poly_hexagon(r, g):
    a = r.randint(2, 14)
    P = [(a * math.cos(math.radians(60 * i)), a * math.sin(math.radians(60 * i))) for i in range(6)]
    fig = labeled_polygon(["A", "B", "C", "D", "E", "F"], P)
    kind = r.choice(["short", "area", "tri"])
    if kind == "short":
        ans = surd(a, 3)
        chk = dist(P[0], P[2])
        fig.seg(P[0], P[2], dash=True)
        t = f"Düzgün ABCDEF altıbucaqlısının tərəfi {a}. AC diaqonalını tapın."
        e = f"∠ABC = 120°: AC² = {a}² + {a}² − 2·{a}·{a}·cos 120° = 3·{a * a} ⇒ AC = {show(ans)}."
        d = [F(2 * a), surd(a, 2), surd(2 * a, 3), surd(F(a, 2), 3), F(a)]
    elif kind == "area":
        ans = surd(F(3 * a * a, 2), 3)
        chk = shoelace(P)
        t = f"Düzgün altıbucaqlının tərəfi {a} olarsa, onun sahəsini tapın."
        e = f"6 bərabərtərəfli üçbucaq: S = 6·{a}²√3/4 = {show(ans)}."
        d = [surd(F(3 * a * a, 4), 3), surd(3 * a * a, 3), surd(F(a * a, 4), 3), F(6 * a * a), surd(F(3 * a * a, 2), 2)]
    else:
        ans = surd(F(3 * a * a, 4), 3)
        chk = shoelace([P[0], P[2], P[4]])
        fig.poly([P[0], P[2], P[4]])
        t = f"Düzgün ABCDEF altıbucaqlısının tərəfi {a}. ACE üçbucağının sahəsini tapın."
        e = f"ACE bərabərtərəflidir, tərəfi AC = {a}√3. S = (√3/4)·3·{a * a} = {show(ans)}. (Altıbucaqlının sahəsinin yarısı.)"
        d = [surd(F(3 * a * a, 2), 3), surd(F(a * a, 4), 3), surd(F(3 * a * a, 8), 3), surd(F(a * a, 2), 3), F(3 * a * a, 2)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M)


def poly_trap_perp(r, g):
    while True:
        a, b = r.randint(4, 24), r.randint(2, 20)
        if a > b and (a + b) % 2 == 0:
            break
    h = F(a + b, 2)
    x = F(a - b, 2)
    A, B, C, D = (0.0, 0.0), (float(a), 0.0), (float(a - x), float(h)), (float(x), float(h))
    # yoxla: diaqonallar perpendikulyardır
    v1 = (C[0] - A[0], C[1] - A[1])
    v2 = (D[0] - B[0], D[1] - B[1])
    assert abs(v1[0] * v2[0] + v1[1] * v2[1]) < 1e-9
    kind = r.choice(["area", "leg"])
    fig = sides_fig(["A", "B", "C", "D"], [A, B, C, D], {(0, 1): str(a), (2, 3): str(b)}).seg(A, C, dash=True).seg(B, D, dash=True)
    O = inter(A, C, B, D)
    fig.right(O, C, D)
    if kind == "area":
        ans = h * h
        chk = shoelace([A, B, C, D])
        t = f"Bərabəryanlı trapesiyanın diaqonalları perpendikulyardır, oturacaqları {a} və {b}-dir. Trapesiyanın sahəsini tapın.".replace(f"{b}-dir", f"{b}")
        t = f"Bərabəryanlı trapesiyanın diaqonalları perpendikulyardır. Oturacaqları {a} və {b} olarsa, trapesiyanın sahəsini tapın."
        e = f"Diaqonallar kəsişmə nöqtəsində 45° bucaq altında oturacaqlara düşür, ona görə h = ({a} + {b})/2 = {show(h)}. S = ({a} + {b})/2 · h = {show(ans)}."
        d = [F(a * b), F((a + b) ** 2, 2), F(a * a + b * b, 2), ans + h, F(a + b, 2) * F(a - b, 2)]
    else:
        ans = rt(h * h + x * x)
        chk = dist(B, C)
        t = f"Bərabəryanlı trapesiyanın diaqonalları perpendikulyardır. Oturacaqları {a} və {b} olarsa, yan tərəfini tapın."
        e = f"h = ({a} + {b})/2 = {show(h)}, yan tərəfin proyeksiyası ({a} − {b})/2 = {show(x)}. c = √({show(h * h)} + {show(x * x)}) = {show(ans)}."
        d = [rt(F(a * a + b * b, 2)), rt(h * h), rt(F(a * b)), rt(h * h - x * x), rt(h * h + x * x + 2)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def poly_trap_scalene(r, g):
    """Bərabəryanlı olmayan trapesiya: oturacaqlar və yan tərəflər verilir — hündürlük (Heron üçbucağı ilə)"""
    t3 = r.choice([t for t in HERON if t[2] <= 25])
    s1, s2, base_diff, S3 = t3
    sides = [s1, s2, base_diff]
    r.shuffle(sides)
    c, dd, w = sides  # yan tərəflər c, dd, oturacaqların fərqi w
    b = r.randint(2, 12)
    a = b + w
    h = F(2 * S3, w)
    # koordinatlar: D(?,h), C(?,h); A(0,0), B(a,0). AD = dd, BC = c
    xd = math.sqrt(dd * dd - float(h) ** 2)
    xc = math.sqrt(c * c - float(h) ** 2)
    sols = []
    for sd in (1, -1):
        for sc in (1, -1):
            Dp = (sd * xd, float(h))
            Cp = (a - sc * xc, float(h))
            if abs((Cp[0] - Dp[0]) - b) < 1e-9:
                sols.append((Dp, Cp))
    if not sols:
        return poly_trap_scalene(r, g)
    Dp, Cp = sols[0]
    A, B = (0.0, 0.0), (float(a), 0.0)
    fig = sides_fig(["A", "B", "C", "D"], [A, B, Cp, Dp], {(0, 1): str(a), (2, 3): str(b), (1, 2): str(c), (3, 0): str(dd)})
    kind = r.choice(["h", "area"])
    if kind == "h":
        ans = h
        chk = Dp[1]
        t = f"Trapesiyanın oturacaqları {a} və {b}, yan tərəfləri {dd} və {c} olarsa, onun hündürlüyünü tapın."
        e = (f"C təpəsindən AD-yə paralel düz xətt çəkin: tərəfləri {dd}, {c} və {a} − {b} = {w} olan üçbucaq alınır. "
             f"Heron düsturu: S = {S3}. h = 2S/{w} = {show(h)}.")
        d = [F(S3, w), F(2 * S3, a), F(2 * S3, b + w + 1), h + 1, F(dd + c, 2)]
    else:
        ans = F(a + b, 2) * h
        chk = shoelace([A, B, Cp, Dp])
        t = f"Trapesiyanın oturacaqları {a} və {b}, yan tərəfləri {dd} və {c} olarsa, onun sahəsini tapın."
        e = (f"Yan tərəflər və oturacaqların fərqi ({w}) üçbucaq əmələ gətirir, onun sahəsi Heron düsturu ilə {S3}, hündürlüyü 2·{S3}/{w} = {show(h)}. "
             f"S = ({a} + {b})/2 · {show(h)} = {show(ans)}.")
        d = [(a + b) * h, F(a + b, 2) * F(S3, w), F(a + b, 2) * min(c, dd), ans + h, F(a + b, 2) * (h + 1)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


# ======================= geo-circle =======================

def circ_chords(r, g):
    R = r.choice([5, 10, 13, 15, 17, 25, 20, 26])
    halves = [(x, math.isqrt(R * R - x * x)) for x in range(1, R) if is_sq(R * R - x * x)]
    if len(halves) < 2 and g != 9:
        return circ_chords(r, g)
    if g == 9:
        h, dd = r.choice(halves)
        ans = dd
        chk = math.sqrt(R * R - h * h)
        fig = Fig().circle((0, 0), R).seg((-h, dd), (h, dd)).seg((0, 0), (0, dd), dash=True).seg((0, 0), (h, dd)).dot((0, 0))
        fig.label((0, 0), "O", away=(0, dd))
        t = f"Radiusu {R} olan çevrədə uzunluğu {2 * h} olan vətər çəkilib. Çevrənin mərkəzindən vətərə qədər məsafəni tapın."
        e = f"Mərkəzdən vətərə perpendikulyar vətəri yarıya bölür: d = √({R}² − {h}²) = {dd}."
        d_ = [R - h, math.isqrt(R * R + h * h) if is_sq(R * R + h * h) else R + h, 2 * h - R if 2 * h > R else R - 1, dd + 1, dd - 1]
        return dict(t=t, a=ans, d=d_, e=e, chk=chk, img=fig.render(), diff=M)
    (h1, d1), (h2, d2) = r.sample(halves, 2)
    same = r.choice([True, False])
    ans = abs(d1 - d2) if same else d1 + d2
    y1, y2 = d1, (d2 if same else -d2)
    chk = abs(y1 - y2)
    # müstəqil: vətərin uclarının çevrə üzərində olması
    assert abs(math.hypot(h1, y1) - R) < 1e-9 and abs(math.hypot(h2, y2) - R) < 1e-9
    fig = Fig().circle((0, 0), R).seg((-h1, y1), (h1, y1)).seg((-h2, y2), (h2, y2)).dot((0, 0))
    fig.label((0, 0), "O", away=(R, 0))
    t = (f"Radiusu {R} olan çevrədə uzunluqları {2 * h1} və {2 * h2} olan paralel vətərlər çəkilib. Vətərlər mərkəzin "
         f"{'eyni tərəfində' if same else 'müxtəlif tərəflərində'} yerləşir. Vətərlər arasındakı məsafəni tapın.")
    e = f"Mərkəzdən məsafələr: √({R}² − {h1}²) = {d1} və √({R}² − {h2}²) = {d2}. {'Fərq' if same else 'Cəm'}: {ans}."
    d_ = [d1 + d2 if same else abs(d1 - d2), abs(h1 - h2), h1 + h2, ans + 1, ans + 2]
    return dict(t=t, a=ans, d=d_, e=e, chk=chk, img=fig.render(), diff=H)


def circ_power(r, g):
    while True:
        ae, eb, ce = r.randint(2, 15), r.randint(2, 15), r.randint(2, 15)
        ed = F(ae * eb, ce)
        if ed.denominator <= 3 and ce != ae:
            break
    th = math.radians(r.randint(35, 145))
    E = (0.0, 0.0)
    A, B = (-float(ae), 0.0), (float(eb), 0.0)
    C = (ce * math.cos(th), ce * math.sin(th))
    Dp = (-float(ed) * math.cos(th), -float(ed) * math.sin(th))
    O, Rr = circ3(A, B, C)
    assert abs(dist(O, Dp) - Rr) < 1e-7  # D həqiqətən çevrə üzərindədir
    fig = Fig().circle(O, Rr).seg(A, B).seg(C, Dp).dot(E)
    for nm, p in (("A", A), ("B", B), ("C", C), ("D", Dp)):
        fig.label(p, nm, away=O)
    fig.label(E, "E", away=(0.0, -1.0 if math.sin(th) > 0 else 1.0))
    ask = r.choice(["ed", "cd"])
    if ask == "ed":
        ans = ed
        chk = dist(E, Dp)
        t = f"Çevrənin AB və CD vətərləri E nöqtəsində kəsişir. AE = {ae}, EB = {eb}, CE = {ce} olarsa, ED-ni tapın."
        e = f"AE·EB = CE·ED ⇒ ED = {ae}·{eb}/{ce} = {show(ed)}."
        dd = [F(ae * ce, eb), F(eb * ce, ae), F(ae + eb - ce), ed + 1, F(ae * eb, ce + 1)]
    else:
        ans = ce + ed
        chk = dist(C, Dp)
        t = f"Çevrənin AB və CD vətərləri E nöqtəsində kəsişir. AE = {ae}, EB = {eb}, CE = {ce} olarsa, CD vətərini tapın."
        e = f"AE·EB = CE·ED ⇒ ED = {show(ed)}. CD = {ce} + {show(ed)} = {show(ans)}."
        dd = [ed, F(ae + eb), ce + F(ae * ce, eb), ans + 1, ans - 1]
    return dict(t=t, a=ans, d=dd, e=e, chk=chk, img=fig.render(), diff=M)


def circ_tangent(r, g):
    while True:
        pa = r.randint(1, 12)
        pb = pa + r.randint(2, 25)
        if is_sq(pa * pb) or g == 11:
            break
    ans = rt(pa * pb)
    # müstəqil: çevrə qur — vətər AB x oxunda, mərkəz (mid, k)
    k = r.uniform(0.5, 6)
    P = (0.0, 0.0)
    A, B = (float(pa), 0.0), (float(pb), 0.0)
    O = ((pa + pb) / 2, k)
    Rr = dist(O, A)
    chk = math.sqrt(dist(P, O) ** 2 - Rr ** 2)
    tlen = chk
    # toxunma nöqtəsi
    ang_ = math.atan2(O[1], O[0]) + math.asin(Rr / dist(P, O))
    T = (tlen * math.cos(ang_), tlen * math.sin(ang_))
    fig = Fig().circle(O, Rr).seg(P, B).seg(P, T).dot(P)
    for nm, p in (("P", P), ("A", A), ("B", B), ("T", T)):
        fig.label(p, nm, away=O if nm != "P" else B)
    if g == 11:
        t = f"Çevrədən kənardakı P nöqtəsindən PT toxunanı və çevrəni A və B nöqtələrində kəsən kəsən çəkilib (A nöqtəsi P ilə B arasındadır). PA = {pa}, AB = {pb - pa} olarsa, PT-ni tapın."
        e = f"PB = PA + AB = {pb}. Toxunan-kəsən teoremi: PT² = PA·PB = {pa}·{pb} = {pa * pb} ⇒ PT = {show(ans)}."
        d = [rt(pa * (pb - pa)), rt(pb * (pb - pa)), rt(pa * pa + (pb - pa) ** 2), rt(pa * pb + pa), rt(F(pa + pb, 2) ** 2)]
    else:
        t = f"Çevrədən kənardakı P nöqtəsindən PT toxunanı və çevrəni A və B nöqtələrində kəsən kəsən çəkilib (A nöqtəsi P ilə B arasındadır). PA = {pa}, PB = {pb} olarsa, PT-ni tapın."
        e = f"PT² = PA·PB = {pa}·{pb} = {pa * pb} ⇒ PT = {show(ans)}."
        d = [rt(pa * (pb - pa)), F(pa + pb, 2), rt(pb * pb - pa * pa), rt(pa * pb + 1), rt(pa * pb - 1)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M if g == 9 else H)


def circ_arcs(r, g):
    while True:
        x, y, z = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)
        if len({x, y, z}) == 3 and 360 % (x + y + z) == 0 and (360 * max(x, y, z) // (x + y + z)) % 2 == 0:
            break
    s = x + y + z
    arcs = [F(360 * v, s) for v in (x, y, z)]
    # ən böyük bucaq ən böyük qövsə söykənir: yarısı
    ans = max(arcs) / 2
    th = [0.0, float(arcs[0]), float(arcs[0] + arcs[1])]
    Pp = [(math.cos(math.radians(t)), math.sin(math.radians(t))) for t in th]
    # qövs AB = x, BC = y, CA = z; bucaq C qövs AB-yə söykənir
    angs = [ang(Pp[2], Pp[0], Pp[1]), ang(Pp[0], Pp[1], Pp[2]), ang(Pp[1], Pp[2], Pp[0])]
    chk = max(angs)
    fig = Fig().circle((0, 0), 1).poly(Pp)
    for nm, p in zip("ABC", Pp):
        fig.label(p, nm, away=(0, 0))
    return dict(t=f"Çevrəyə daxil çəkilmiş ABC üçbucağının təpələri çevrəni uzunluqları {x} : {y} : {z} nisbətində olan qövslərə bölür. Üçbucağın ən böyük bucağını tapın.",
                a=Num(show(ans) + "°", ans), d=[Num(show(v) + "°", v) for v in (max(arcs), min(arcs) / 2, sorted(arcs)[1] / 2, ans + 10, F(180) - ans, ans - 10)],
                e=f"Qövslər: {', '.join(show(v) + '°' for v in arcs)}. Daxili bucaq söykəndiyi qövsün yarısına bərabərdir: {show(max(arcs))}°/2 = {show(ans)}°.",
                chk=chk, img=fig.render(), diff=M)


def circ_right_tri(r, g):
    a0, b0, c0 = r.choice(TRIPLES)
    k = r.randint(1, 3)
    a, b, c = a0 * k, b0 * k, c0 * k
    rr = F(a + b - c, 2)
    RR = F(c, 2)
    S = F(a * b, 2)
    rr_chk = float(S / (F(a + b + c, 2)))
    kind = r.choice(["sum", "dist"] if g != 9 else ["sum", "ratio"])
    if kind == "sum":
        ans = rr + RR
        chk = rr_chk + c / 2
        t = f"Düzbucaqlı üçbucağın katetləri {a} və {b}-dir. Daxili və xarici çəkilmiş çevrələrin radiuslarının cəmini tapın.".replace(f"{b}-dir", f"{b}")
        t = f"Düzbucaqlı üçbucağın katetləri {a} və {b} olarsa, ona daxil və xaricdən çəkilmiş çevrələrin radiuslarının cəmini tapın."
        e = f"Hipotenuz {c}. r = (a + b − c)/2 = {show(rr)}, R = c/2 = {show(RR)}. Cəm: {show(ans)} (= (a + b)/2)."
        d = [F(c) + rr, F(a + b), rr + F(c), F(a + b + c, 2), ans + 1]
    elif kind == "ratio":
        ans = RR / rr
        chk = (c / 2) / rr_chk
        t = f"Düzbucaqlı üçbucağın katetləri {a} və {b} olarsa, xarici çəkilmiş çevrənin radiusunun daxili çəkilmiş çevrənin radiusuna nisbətini tapın."
        e = f"c = {c}, R = {show(RR)}, r = (a + b − c)/2 = {show(rr)}. R : r = {show(ans)}."
        d = [rr / RR, F(c, a + b - c) * 2, F(c, a + b), ans + 1, F(c, a)]
    else:
        # mərkəzlər arasındakı məsafə: d² = R² − 2Rr (Eyler)
        d2 = RR * RR - 2 * RR * rr
        ans = rt(d2)
        A, B, C = (0.0, 0.0), (float(a), 0.0), (0.0, float(b))
        I = (float(rr), float(rr))
        O = (a / 2, b / 2)
        chk = dist(I, O)
        t = f"Düzbucaqlı üçbucağın katetləri {a} və {b} olarsa, daxili və xarici çəkilmiş çevrələrin mərkəzləri arasındakı məsafəni tapın."
        e = f"r = {show(rr)}, R = {show(RR)}. Eyler düsturu: d² = R² − 2Rr = {show(RR * RR)} − {show(2 * RR * rr)} = {show(d2)} ⇒ d = {show(ans)}."
        d = [RR - rr, rt(RR * RR - RR * rr), rt(RR * RR + 2 * RR * rr), rt(RR * RR - rr * rr), rt(d2 + 1)]
    A, B, C = (0.0, 0.0), (float(a), 0.0), (0.0, float(b))
    fig = labeled_polygon(["C", "A", "B"], [A, B, C]).right(A, B, C).circle((float(rr), float(rr)), float(rr)).circle((a / 2, b / 2), c / 2)
    fig.side(A, B, str(a), inside=C)
    fig.side(A, C, str(b), inside=B)
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M if kind == "sum" else H)


def circ_sector(r, g):
    R = r.randint(2, 15)
    th = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270, 300])
    kind = r.choice(["seg", "ring"]) if g != 9 else r.choice(["arc_area", "ring"])
    if kind == "arc_area":
        L = F(R * th, 180)
        ans = pi_mul(F(R * R * th, 360))
        chk = math.pi * R * R * th / 360
        t = f"Dairəvi sektorun qövsünün uzunluğu {pi_mul(L).s}, radiusu {R} olarsa, sektorun sahəsini tapın."
        e = f"Qövs: πRα/180 = {pi_mul(L).s} ⇒ α = {th}°. S = πR²α/360 = {ans.s}. (və ya S = L·R/2)"
        d = [pi_mul(F(R * R * th, 180)), pi_mul(F(R * th, 360)), pi_mul(L * R), pi_mul(F(R * R * th, 720)), pi_mul(F(R * R * th, 360) + 1)]
    elif kind == "ring":
        R2 = R + r.randint(1, 8)
        ch = 2 * math.sqrt(R2 * R2 - R * R)
        ch2 = 4 * (R2 * R2 - R * R)
        ans = pi_mul(R2 * R2 - R * R)
        chk = math.pi * (ch / 2) ** 2
        t = f"İki konsentrik çevrədən böyüyünün vətəri kiçiyinə toxunur. Vətərin uzunluğu {show(rt(ch2))} olarsa, çevrələr arasındakı halqanın sahəsini tapın."
        e = f"Vətərin yarısı ℓ/2, R² − r² = (ℓ/2)² = {R2 * R2 - R * R}. Halqanın sahəsi π(R² − r²) = {ans.s}."
        d = [pi_mul(4 * (R2 * R2 - R * R)), pi_mul(2 * (R2 * R2 - R * R)), pi_mul(F(R2 * R2 - R * R, 2)), pi_mul(R2 * R2 - R * R + 1), pi_mul(R2 * R2)]
    else:
        # seqmentin sahəsi: sektor − üçbucaq (60°, 90°, 120°)
        th = r.choice([60, 90, 120])
        sec = F(R * R * th, 360)
        tri = {60: (F(R * R, 4), 3), 90: (F(R * R, 2), 1), 120: (F(R * R, 4), 3)}[th]
        tri_v = float(tri[0]) * math.sqrt(tri[1])
        ans = Num(f"{pi_mul(sec).s} − {show(tri[0]) if tri[1] == 1 else surd(tri[0], 3).s}", math.pi * float(sec) - tri_v)
        # müstəqil: ədədi inteqral (seqment = vətərlə qövs arasındakı oblast)
        n = 20000
        half = math.radians(th) / 2
        chk = 0.0
        x0 = R * math.cos(half)
        for i in range(n):
            x = x0 + (R - x0) * (i + 0.5) / n
            chk += 2 * math.sqrt(max(R * R - x * x, 0)) * (R - x0) / n
        tris = show(tri[0]) if tri[1] == 1 else surd(tri[0], 3).s
        t = f"Radiusu {R} olan çevrədə {th}°-li qövsə söykənən vətər çəkilib. Vətərlə bu qövs arasındakı seqmentin sahəsini tapın."
        e = f"Seqment = sektor − üçbucaq: πR²·{th}/360 − ½R²·sin {th}° = {pi_mul(sec).s} − {tris}."
        d = [Num(f"{pi_mul(sec).s} + {tris}", math.pi * float(sec) + tri_v), pi_mul(sec), Num(f"{pi_mul(2 * sec).s} − {tris}", 2 * math.pi * float(sec) - tri_v),
             Num(f"{pi_mul(sec).s} − {show(2 * tri[0]) if tri[1] == 1 else surd(2 * tri[0], 3).s}", math.pi * float(sec) - 2 * tri_v),
             Num(f"{pi_mul(R * R - sec).s} − {tris}", math.pi * (R * R - float(sec)) - tri_v)]
        return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=H, open=False)
    return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=M if g == 9 else H)


def circ_trap_in(r, g):
    while True:
        a, b = r.randint(3, 30), r.randint(2, 20)
        if a > b and is_sq(a * b) and (a + b) % 2 == 0:
            break
    rr = F(math.isqrt(a * b), 2)
    c = F(a + b, 2)
    h = 2 * rr
    x = F(a - b, 2)
    A, B, C, D = (0.0, 0.0), (float(a), 0.0), (float(a - x), float(h)), (float(x), float(h))
    assert abs(math.hypot(float(x), float(h)) - float(c)) < 1e-9
    fig = sides_fig(["A", "B", "C", "D"], [A, B, C, D], {(0, 1): str(a), (2, 3): str(b)}).circle((a / 2, float(rr)), float(rr))
    kind = r.choice(["r", "area", "leg"])
    if kind == "r":
        ans, chk = rr, float(h) / 2
        t = f"Bərabəryanlı trapesiyaya çevrə daxil çəkilib. Trapesiyanın oturacaqları {a} və {b} olarsa, çevrənin radiusunu tapın."
        e = f"Toxunanlar xassəsi: 2c = {a} + {b} ⇒ c = {show(c)}. h = √(c² − (({a} − {b})/2)²) = √{a * b} = {show(h)}, r = h/2 = {show(rr)}."
        d = [F(a + b, 4), h, F(a - b, 2), rr + 1, F(a + b, 2)]
    elif kind == "area":
        ans, chk = F(a + b, 2) * h, shoelace([A, B, C, D])
        t = f"Bərabəryanlı trapesiyaya çevrə daxil çəkilib. Trapesiyanın oturacaqları {a} və {b} olarsa, onun sahəsini tapın."
        e = f"c = ({a} + {b})/2 = {show(c)}, h = √(ab) = {show(h)}. S = ({a} + {b})/2·{show(h)} = {show(ans)}."
        d = [F(a + b, 2) * rr, F(a + b, 2) * c, F(a * b), ans + h, F(a + b) * h]
    else:
        ans, chk = c, dist(B, C)
        t = f"Bərabəryanlı trapesiyaya radiusu {show(rr)} olan çevrə daxil çəkilib, kiçik oturacağı {b}-dir. Yan tərəfini tapın.".replace(f"{b}-dir", f"{b}")
        t = f"Bərabəryanlı trapesiyaya radiusu {show(rr)} olan çevrə daxil çəkilib. Kiçik oturacaq {b} olarsa, trapesiyanın yan tərəfini tapın."
        e = f"h = 2r = {show(h)}. h² = ab ⇒ a = {show(h * h)}/{b} = {a}. c = (a + b)/2 = {show(c)}."
        d = [F(a), h, F(a - b, 2), c + 1, rt(h * h + b * b)]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=H)


def circ_common_chord(r, g):
    while True:
        hh = r.choice([12, 24, 4, 8, 15, 20, 6, 3, 5, 9])
        opts = [(math.isqrt(R * R - hh * hh), R) for R in range(hh + 1, 60) if is_sq(R * R - hh * hh)]
        if len(opts) >= 2:
            break
    (d1, R1), (d2, R2) = r.sample(opts, 2)
    same_side = False
    D = d1 + d2
    O1, O2 = (0.0, 0.0), (float(D), 0.0)
    # müstəqil: iki çevrənin kəsişmə nöqtələri
    x = (D * D + R1 * R1 - R2 * R2) / (2 * D)
    y = math.sqrt(R1 * R1 - x * x)
    chk = 2 * y
    fig = Fig().circle(O1, R1).circle(O2, R2).seg((x, y), (x, -y)).seg(O1, O2, dash=True).dot(O1).dot(O2)
    fig.label(O1, "O₁", away=O2)
    fig.label(O2, "O₂", away=O1)
    return dict(t=f"Radiusları {R1} və {R2} olan iki çevrə kəsişir, mərkəzləri arasındakı məsafə {D}-dir. Ortaq vətərin uzunluğunu tapın.".replace(f"məsafə {D}-dir", f"məsafə {_cop(D)}"),
                a=2 * hh, d=[hh, 2 * hh + 2, 2 * hh - 2, abs(R1 - R2) + D // 2, R1 + R2 - D if R1 + R2 - D != 2 * hh else 2 * hh + 4],
                e=f"Ortaq vətər O₁O₂-yə perpendikulyardır və onu yarıya bölür. Yarım vətər h: √({R1}² − h²) + √({R2}² − h²) = {D}. "
                  f"h = {hh} yoxlanır: √{R1 * R1 - hh * hh} + √{R2 * R2 - hh * hh} = {d1} + {d2} = {D}. Vətər 2h = {2 * hh}.",
                chk=chk, img=fig.render(), diff=H)


def _cop(n):
    from mx import az_cop
    return az_cop(n)


# ======================= geo-trig =======================

def trig_quadrant(r, g):
    a0, b0, c0 = r.choice(TRIPLES)
    which = r.choice(["sin", "cos"])
    quad = r.choice([2, 3, 4] if g != 9 else [2])
    # α bucağını qur
    s_abs, c_abs = F(a0, c0), F(b0, c0)
    if which == "cos":
        s_abs, c_abs = c_abs, s_abs
    sgn_s = {1: 1, 2: 1, 3: -1, 4: -1}[quad]
    sgn_c = {1: 1, 2: -1, 3: -1, 4: 1}[quad]
    s, c = sgn_s * s_abs, sgn_c * c_abs
    alpha = math.atan2(float(s), float(c))
    given = f"sin α = {show(s)}" if which == "sin" else f"cos α = {show(c)}"
    rng = {2: "π/2 < α < π", 3: "π < α < 3π/2", 4: "3π/2 < α < 2π"}[quad]
    kinds = {9: ["tg", "ctg_plus"], 10: ["sin2", "cos2", "tg"], 11: ["sin2", "cos2", "tg_half", "tg2"]}[g]
    kind = r.choice(kinds)
    if kind == "tg":
        ans, chk, w = s / c, math.tan(alpha), "tg α"
        d = [c / s, -s / c, s_abs / c_abs, -c / s]
    elif kind == "ctg_plus":
        ans, chk, w = s / c + c / s, math.tan(alpha) + 1 / math.tan(alpha), "tg α + ctg α"
        d = [-(s / c + c / s), s / c - c / s, c / s - s / c, 1 / (s * c) + 1]
    elif kind == "sin2":
        ans, chk, w = 2 * s * c, math.sin(2 * alpha), "sin 2α"
        d = [-2 * s * c, s * c, c * c - s * s, 2 * s_abs * c_abs + 0 if 2 * s * c < 0 else -s * c]
    elif kind == "cos2":
        ans, chk, w = c * c - s * s, math.cos(2 * alpha), "cos 2α"
        d = [s * s - c * c, 2 * s * c, 1 - s * s, 2 * c * c]
    elif kind == "tg2":
        tg = s / c
        ans, chk, w = 2 * tg / (1 - tg * tg), math.tan(2 * alpha), "tg 2α"
        d = [-ans, 2 * tg, tg / (1 - tg * tg), 2 * tg / (1 + tg * tg)]
    else:
        ans, chk, w = s / (1 + c), math.tan(alpha / 2), "tg (α/2)"
        d = [-ans, (1 + c) / s, s / (1 - c), (1 - c) / s * -1]
    return dict(t=f"{given} və {rng} olarsa, {w} ifadəsinin qiymətini tapın.", a=ans, d=d,
                e=f"{'cos' if which == 'sin' else 'sin'} α = {'−' if (sgn_c if which == 'sin' else sgn_s) < 0 else ''}√(1 − {show((s_abs if which == 'sin' else c_abs) ** 2)}) "
                  f"= {show(c if which == 'sin' else s)} (rüb işarəsinə görə). {w} = {show(ans)}.", chk=chk, diff=M if kind == "tg" else H)


def trig_tan_expr(r, g):
    while True:
        k = F(r.randint(-7, 7), r.randint(1, 4))
        a, b, c, d = r.randint(1, 5), r.randint(-5, 5), r.randint(1, 5), r.randint(-5, 5)
        den = c * k - d
        if k != 0 and den != 0 and b != 0 and d != 0:
            break
    kind = r.choice(["lin", "sq"]) if g != 9 else "lin"
    al = math.atan(float(k))
    if kind == "lin":
        ans = (a * k + b) / den
        chk = (a * math.sin(al) + b * math.cos(al)) / (c * math.sin(al) - d * math.cos(al))
        t = f"tg α = {show(k)} olarsa, ({a if a > 1 else ''}sin α {'+' if b > 0 else '−'} {abs(b) if abs(b) > 1 else ''}cos α) / ({c if c > 1 else ''}sin α {'+' if -d > 0 else '−'} {abs(d) if abs(d) > 1 else ''}cos α) ifadəsinin qiymətini tapın."
        e = f"Surəti və məxrəci cos α-ya bölün: ({a}·tg α + {par(b)})/({c}·tg α − {par(d)}) = ({show(a * k)} + {par(b)})/({show(c * k)} − {par(d)}) = {show(ans)}."
        dd = [(a * k - b) / den, (a + b * k) / (c - d * k) if c - d * k else ans + 1, (a * k + b) / (c * k + d) if c * k + d else ans + 2, -ans, 1 / ans if ans else ans + 3]
    else:
        ans = (a * k * k + b) / (1 + k * k)
        chk = a * math.sin(al) ** 2 + b * math.cos(al) ** 2
        t = f"tg α = {show(k)} olarsa, {a if a > 1 else ''}sin²α {'+' if b > 0 else '−'} {abs(b) if abs(b) > 1 else ''}cos²α ifadəsinin qiymətini tapın."
        e = f"Bölün sin²α + cos²α = 1-ə, sonra cos²α-ya: ({a}·tg²α + {par(b)})/(tg²α + 1) = ({show(a * k * k)} + {par(b)})/{show(1 + k * k)} = {show(ans)}."
        dd = [a * k * k + b, (a * k * k + b) / (k * k), (a + b * k * k) / (1 + k * k), -ans, ans + 1]
    return dict(t=t, a=ans, d=dd, e=e, chk=chk, diff=M)


def trig_sum_t(r, g):
    while True:
        t_ = F(r.randint(-13, 13), r.choice([2, 3, 4, 5, 7]))
        if 0 < abs(t_) < F(7, 5) and t_ * t_ != 1:
            break
    kind = r.choice(["prod", "cube"] if g == 10 else ["cube", "four", "diff2"])
    al = math.asin(float(t_) / math.sqrt(2)) - math.pi / 4
    s, c = math.sin(al), math.cos(al)
    p = (t_ * t_ - 1) / 2
    if kind == "prod":
        ans, chk, w = p, s * c, "sin α · cos α"
        how = f"(sin α + cos α)² = 1 + 2sin α cos α ⇒ sin α cos α = ({show(t_ * t_)} − 1)/2 = {show(p)}"
        d = [t_ * t_ - 1, (t_ * t_ + 1) / 2, (1 - t_ * t_) / 2, t_ / 2]
    elif kind == "cube":
        ans, chk, w = t_ * (1 - p), s ** 3 + c ** 3, "sin³α + cos³α"
        how = f"sin α cos α = {show(p)}; sin³α + cos³α = (sin α + cos α)(1 − sin α cos α) = {show(t_)}·{show(1 - p)} = {show(ans)}"
        d = [t_ ** 3, t_ * (1 + p), t_ ** 3 - 3 * p, t_ * (1 - 2 * p)]
    elif kind == "four":
        ans, chk, w = 1 - 2 * p * p, s ** 4 + c ** 4, "sin⁴α + cos⁴α"
        how = f"sin α cos α = {show(p)}; sin⁴α + cos⁴α = 1 − 2(sin α cos α)² = {show(ans)}"
        d = [1 - p * p, 1 + 2 * p * p, 1 - 2 * p, (1 - 2 * p) ** 2]
    else:
        ans, chk, w = 2 - t_ * t_, (s - c) ** 2, "(sin α − cos α)²"
        how = f"(sin α − cos α)² + (sin α + cos α)² = 2 ⇒ (sin α − cos α)² = 2 − {show(t_ * t_)} = {show(ans)}"
        d = [1 - t_ * t_, t_ * t_ - 1, 2 + t_ * t_, 1 - 2 * p * 0 - p]
    return dict(t=f"sin α + cos α = {show(t_)} olarsa, {w} ifadəsinin qiymətini tapın.", a=ans, d=d, e=how + ".", chk=chk, diff=H)


def trig_cos_law(r, g):
    angd = r.choice([60, 120])
    kind = "a" if g == 9 else r.choice(["a", "R"]) if g == 10 else r.choice(["R", "h"])
    cosA = F(1, 2) if angd == 60 else F(-1, 2)
    while True:
        b, c = r.randint(2, 20 if kind != "a" else 15), r.randint(2, 20 if kind != "a" else 15)
        if b != c and (kind == "a" or is_sq(int(b * b + c * c - 2 * b * c * cosA))):
            break
    a2 = b * b + c * c - 2 * b * c * cosA
    A = (0.0, 0.0)
    B = (float(c), 0.0)
    C = (b * math.cos(math.radians(angd)), b * math.sin(math.radians(angd)))
    fig = sides_fig(["A", "B", "C"], [A, B, C], {(0, 1): str(c), (2, 0): str(b)}).arc(A, B, C, f"{angd}°")
    if kind == "a":
        ans = rt(a2)
        chk = dist(B, C)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, ∠A = {angd}°. BC tərəfini tapın."
        e = f"BC² = {b}² + {c}² − 2·{b}·{c}·cos {angd}° = {show(a2)} ⇒ BC = {show(ans)}."
        alt = b * b + c * c + 2 * b * c * cosA
        d = [rt(alt), rt(b * b + c * c), rt(a2 + b * c), F(abs(b - c) + 1) if a2 != (abs(b - c) + 1) ** 2 else F(b + c), rt(a2 - 1)]
    elif kind == "R":
        # R = a / (2 sin A) = a/√3
        ans = rt(F(a2, 3))
        O, Rr = circ3(A, B, C)
        chk = Rr
        fig.circle(O, Rr)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, ∠A = {angd}°. Üçbucağa xaricdən çəkilmiş çevrənin radiusunu tapın."
        e = f"BC² = {show(a2)} (kosinuslar teoremi). Sinuslar teoremi: 2R = BC/sin {angd}° ⇒ R = √{show(a2)}/√3 = {show(ans)}."
        d = [rt(F(a2, 2)), rt(F(a2 * 4, 3)), rt(a2), rt(F(a2, 3) + 1), rt(F(a2, 12))]
    else:
        # BC-yə endirilmiş hündürlük: h = 2S/a = b c sin A / a
        S2 = F(b * b * c * c * 3, 4)  # S² = (½ b c sin A)², sin² = 3/4 → S² = b²c²·3/16 ⇒ (2S)² = b²c²·3/4
        ans = rt(S2 / a2)
        Hh = foot(A, B, C)
        chk = dist(A, Hh)
        fig.seg(A, Hh, dash=True)
        t = f"ABC üçbucağında AB = {c}, AC = {b}, ∠A = {angd}°. A təpəsindən BC-yə endirilmiş hündürlüyü tapın."
        e = f"BC² = {show(a2)}. S = ½·{b}·{c}·sin {angd}° = {b * c}√3/4. h = 2S/BC = {b * c}√3/(2√{show(a2)}) ⇒ h = {show(ans)}."
        d = [rt(S2 / (4 * a2)), rt(F(b * c * 3, 4)), rt(S2 / a2 + 1), rt(S2 / (b * b + c * c)), rt(F(3 * b * c, 4))]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, img=fig.render(), diff=M if kind == "a" else H)


def trig_sine_law(r, g):
    Aa, Bb = r.choice([(30, 45), (45, 30), (30, 60), (60, 45), (45, 60), (30, 120), (120, 30), (135, 30), (30, 135), (60, 60), (45, 45)])
    a = r.randint(2, 14)
    sins = {30: (F(1, 2), 1), 45: (F(1, 2), 2), 60: (F(1, 2), 3), 120: (F(1, 2), 3), 135: (F(1, 2), 2), 90: (F(1), 1)}
    sq = {1: 1, 2: 2, 3: 3}
    if Bb in sins and Aa in sins:
        ka, ma = sins[Aa]
        kb, mb = sins[Bb]
        # b = a sinB / sinA = a (kb√mb)/(ka√ma) = a (kb/ka) √(mb/ma)
        ans = mulrt(a * kb / ka, F(mb, ma))
        chk_ans = a * math.sin(math.radians(Bb)) / math.sin(math.radians(Aa))
    else:
        return trig_sine_law(r, g)
    Cc = 180 - Aa - Bb
    Ap, Bp, Cp = _tri_angles(Aa, Bb)
    scale = a / dist(Bp, Cp)
    chk = dist(Ap, Cp) * scale
    assert abs(chk - chk_ans) < 1e-9
    P = [Ap, Bp, Cp]
    fig = labeled_polygon(["A", "B", "C"], P).arc(Ap, Bp, Cp, f"{Aa}°").arc(Bp, Cp, Ap, f"{Bb}°")
    fig.side(Bp, Cp, str(a), inside=Ap)
    return dict(t=f"ABC üçbucağında BC = {a}, ∠A = {Aa}°, ∠B = {Bb}°. AC tərəfini tapın.", a=ans,
                d=[mulrt(a * ka / kb, F(ma, mb)), mulrt(a, F(mb, 1)), mulrt(F(a, 2), F(mb * ma, 1)), mulrt(a * kb / ka, F(mb * ma, 1)) if mb != ma else F(2 * a), F(a)],
                e=f"Sinuslar teoremi: AC/sin B = BC/sin A ⇒ AC = {a}·sin {Bb}°/sin {Aa}° = {show(ans)}.",
                chk=chk, img=fig.render(), diff=M)


def _roots_on(fn, lo, hi, n=120000):
    """[lo; hi] parçasında f(x) = 0 köklərini ədədi tapır (sadə köklər + toxunma nöqtələri)"""
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    ys = [fn(x) for x in xs]
    roots = []
    for i in range(n):
        if ys[i] == 0:
            roots.append(xs[i])
        elif ys[i] * ys[i + 1] < 0:
            a, b = xs[i], xs[i + 1]
            for _ in range(80):
                m = (a + b) / 2
                if fn(a) * fn(m) <= 0:
                    b = m
                else:
                    a = m
            roots.append((a + b) / 2)
    if ys[n] == 0 or abs(ys[n]) < 1e-12:
        roots.append(xs[n])
    if abs(ys[0]) < 1e-12 and xs[0] not in roots:
        roots.append(xs[0])
    # toxunma: |f| lokal minimumu, işarə dəyişmir
    for i in range(1, n):
        if abs(ys[i]) <= abs(ys[i - 1]) and abs(ys[i]) <= abs(ys[i + 1]) and abs(ys[i]) < 1e-6 and ys[i - 1] * ys[i + 1] > 0:
            a, b = xs[i - 1], xs[i + 1]
            for _ in range(100):
                m1, m2 = a + (b - a) / 3, b - (b - a) / 3
                if abs(fn(m1)) < abs(fn(m2)):
                    b = m2
                else:
                    a = m1
            roots.append((a + b) / 2)
    out = []
    for x in sorted(roots):
        if not out or abs(x - out[-1]) > 1e-5:
            out.append(x)
    return out


# sin/cos qiymətləri və [0; 2π]-dəki həllər (π vahidi ilə)
SOL_SIN = {F(1): [F(1, 2)], F(-1): [F(3, 2)], F(0): [F(0), F(1), F(2)], F(1, 2): [F(1, 6), F(5, 6)], F(-1, 2): [F(7, 6), F(11, 6)]}
SOL_COS = {F(1): [F(0), F(2)], F(-1): [F(1)], F(0): [F(1, 2), F(3, 2)], F(1, 2): [F(1, 3), F(5, 3)], F(-1, 2): [F(2, 3), F(4, 3)]}


def trig_eq(r, g):
    fn_name = r.choice(["sin", "cos"])
    table = SOL_SIN if fn_name == "sin" else SOL_COS
    vals = list(table.keys()) + [F(2), F(-2), F(3, 2), F(-3, 2)]
    while True:
        s1, s2 = r.sample(vals, 2)
        if s1 in table or s2 in table:
            # 2t² − 2(s1+s2)t + 2s1s2 = 0 tam əmsallı olsun
            B, C = -2 * (s1 + s2), 2 * s1 * s2
            if B.denominator == 1 and C.denominator == 1:
                break
    sols = sorted(set((table.get(s1, []) + table.get(s2, []))))
    ask = r.choice(["count", "sum"])
    f = (lambda x: 2 * math.sin(x) ** 2 + float(B) * math.sin(x) + float(C)) if fn_name == "sin" else \
        (lambda x: 2 * math.cos(x) ** 2 + float(B) * math.cos(x) + float(C))
    found = _roots_on(f, 0.0, 2 * math.pi)
    eq = f"2{fn_name}²x {'+' if B > 0 else '−'} {abs(B) if abs(B) != 1 else ''}{fn_name} x {'+' if C >= 0 else '−'} {abs(C)} = 0".replace(" + 0 = 0", " = 0").replace(" − 0 = 0", " = 0")
    if B == 0:
        eq = f"2{fn_name}²x {'+' if C >= 0 else '−'} {abs(C)} = 0"
    lst = ", ".join(pi_mul(x).s for x in sols)
    e = (f"t = {fn_name} x: 2t² {'+' if B > 0 else '−'} {abs(B)}t {'+' if C >= 0 else '−'} {abs(C)} = 0 ⇒ t = {show(s1)} və ya t = {show(s2)} "
         f"(|t| ≤ 1 olanlar qalır). [0; 2π] parçasında həllər: {lst}.")
    if ask == "count":
        ans = len(sols)
        return dict(t=f"{eq} tənliyinin [0; 2π] parçasında neçə kökü var?", a=ans, d=[ans + 1, ans - 1, ans + 2, ans * 2, ans + 3],
                    e=e + f" Cəmi {ans} kök.", chk=len(found), open=False, diff=H)
    tot = sum(sols)
    return dict(t=f"{eq} tənliyinin [0; 2π] parçasındakı köklərinin cəmini tapın.", a=pi_mul(tot),
                d=[pi_mul(tot + 1), pi_mul(tot - F(1, 2)) if tot > F(1, 2) else pi_mul(tot + 2), pi_mul(tot + F(1, 2)), pi_mul(2 * tot), pi_mul(tot + 2)],
                e=e + f" Cəm: {pi_mul(tot).s}.", chk=sum(found), diff=H)


def trig_reduce(r, g):
    a0, b0, c0 = r.choice(TRIPLES[:5])
    s = F(a0, c0)
    c = -F(b0, c0) if r.random() < 0.5 else F(b0, c0)
    quad = "π/2 < α < π" if c < 0 else "0 < α < π/2"
    al = math.atan2(float(s), float(c))
    exprs = [
        ("sin(π − α) + cos(3π/2 + α)", 2 * s, math.sin(math.pi - al) + math.cos(1.5 * math.pi + al), "sin α + sin α"),
        ("cos(π + α) − sin(π/2 − α)", -2 * c, math.cos(math.pi + al) - math.sin(math.pi / 2 - al), "−cos α − cos α"),
        ("sin(3π/2 − α) · tg(π + α)", -s, math.sin(1.5 * math.pi - al) * math.tan(math.pi + al), "(−cos α)·tg α = −sin α"),
        ("cos(π/2 + α) · ctg(3π/2 − α)", -s * s / c, math.cos(math.pi / 2 + al) / math.tan(1.5 * math.pi - al), "(−sin α)·tg α"),
        ("tg(π − α) + ctg(π/2 + α)", -2 * s / c, math.tan(math.pi - al) + 1 / math.tan(math.pi / 2 + al), "−tg α − tg α"),
    ]
    txt, ans, chk, how = r.choice(exprs)
    return dict(t=f"sin α = {show(s)} və {quad} olarsa, {txt} ifadəsinin qiymətini tapın.", a=ans,
                d=[-ans, ans / 2 if ans else F(1), 2 * ans if ans else F(2), ans + s, ans - c],
                e=f"cos α = {show(c)}. Çevirmə düsturları: {txt} = {how} = {show(ans)}.", chk=chk, diff=M)


def trig_maxmin(r, g):
    a0, b0, c0 = r.choice(TRIPLES[:5])
    k = r.randint(1, 2)
    a, b = a0 * k * r.choice([1, -1]), b0 * k * r.choice([1, -1])
    c = r.randint(-10, 10)
    R = c0 * k
    kind = r.choice(["prod", "count"])
    xs = [2 * math.pi * i / 200000 for i in range(200001)]
    vals = [a * math.sin(x) + b * math.cos(x) + c for x in xs]
    mx_, mn_ = max(vals), min(vals)
    from mx import lead, sg
    fx = f"{lead(a, 'sin x')}{sg(b, 'cos x')}{sg(c)}"
    if kind == "prod":
        ans = (c + R) * (c - R)
        chk = mx_ * mn_
        t = f"f(x) = {fx} funksiyasının ən böyük və ən kiçik qiymətlərinin hasilini tapın."
        e = f"a sin x + b cos x ifadəsinin qiymətləri [−√(a² + b²); √(a² + b²)] = [−{R}; {R}]. f-in max = {c + R}, min = {c - R}. Hasil: {ans}."
        d = [c * c + R * R, (c + abs(a) + abs(b)) * (c - abs(a) - abs(b)), -R * R, ans + 1, (c + R) * (c - R + 1)]
    else:
        ans = sum(1 for y in range(-200, 201) if c - R <= y <= c + R)
        chk = math.floor(mx_ + 1e-6) - math.ceil(mn_ - 1e-6) + 1
        t = f"f(x) = {fx} funksiyası neçə tam qiymət alır?"
        e = f"√({abs(a)}² + {abs(b)}²) = {R}, deməli f-in qiymətlər çoxluğu [{neg(str(c - R))}; {c + R}]. Tam qiymətlər: {ans}."
        d = [2 * R, ans + 1, 2 * (abs(a) + abs(b)) + 1, ans - 2, ans + 2]
    return dict(t=t, a=ans, d=d, e=e, chk=chk, diff=H)


TOPICS = {
    "geo-basic": {9: [tri_altitude, tri_bisector, tri_angle_chase, tri_iso_angle, tri_heron],
                  10: [tri_median, tri_bisector, tri_heron, tri_angle_chase, tri_altitude, tri_iso_angle],
                  11: [tri_altitude, tri_median, tri_heron, tri_angle_chase, tri_cos120_median, tri_bisector]},
    "geo-poly": {9: [poly_diagonals, poly_rhombus, poly_trapezoid, poly_rect_bisector, poly_parallelogram],
                 10: [poly_parallelogram, poly_hexagon, poly_trapezoid, poly_rhombus, poly_rect_bisector, poly_diagonals],
                 11: [poly_trap_perp, poly_trap_scalene, poly_trapezoid, poly_rhombus, poly_parallelogram, poly_hexagon]},
    "geo-circle": {9: [circ_chords, circ_power, circ_tangent, circ_arcs, circ_right_tri, circ_sector],
                   10: [circ_chords, circ_trap_in, circ_right_tri, circ_power, circ_sector, circ_arcs],
                   11: [circ_common_chord, circ_trap_in, circ_tangent, circ_right_tri, circ_chords, circ_sector]},
    "geo-trig": {9: [trig_quadrant, trig_tan_expr, trig_cos_law, trig_sine_law],
                 10: [trig_quadrant, trig_sum_t, trig_reduce, trig_cos_law, trig_sine_law, trig_tan_expr],
                 11: [trig_eq, trig_quadrant, trig_sum_t, trig_maxmin, trig_cos_law]},
}
