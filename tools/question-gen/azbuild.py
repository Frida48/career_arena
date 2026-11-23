"""Azərbaycan dili sual bankının qurucusu: mövzu × sinif üçün 90 sual → 3 quiz × 30 sual.

Hər şablon fn(r, g) -> dict(t, opts, ok, e) və ya None (yenidən cəhd):
    t    — sualın şərti
    opts — 5 variant (mətn)
    ok   — hər variant üçün şərtin YENİDƏN hesablanmış nəticəsi (True/False)
    e    — izah
    diff — "medium" | "hard" (yalnız 10-cu sinifdə nəzərə alınır; 9 və 11-də hamısı "hard")
Qurucu yoxlayır: düz 5 variant, hamısı fərqli və boş deyil, şərti DÜZ BİR variant ödəyir.
Bu şərtlər pozularsa, sual bazaya düşmür (şablon xətası kimi dayandırılır).
"""
import random

QUIZZES, PER_QUIZ = 3, 30
TOTAL = QUIZZES * PER_QUIZ


def near_miss(r, pool, conds, render, need=4):
    """Bütün şərtləri ödəyən bir element + şərtlərin çoxunu ödəyən, amma hamısını ödəməyən 4 element.
    conds: [fn(item) -> bool]. Qaytarır (opts, ok, correct_item) və ya None."""
    good = [x for x in pool if all(c(x) for c in conds)]
    if not good:
        return None
    ans = r.choice(good)
    bad = [x for x in pool if not all(c(x) for c in conds)]
    r.shuffle(bad)
    bad.sort(key=lambda x: -sum(bool(c(x)) for c in conds))
    picked, seen = [], {render(ans)}
    for x in bad:
        s = render(x)
        if s in seen:
            continue
        picked.append(x)
        seen.add(s)
        if len(picked) == need:
            break
    if len(picked) < need:
        return None
    items = picked + [ans]
    r.shuffle(items)
    opts = [render(x) for x in items]
    ok = [all(c(x) for c in conds) for x in items]
    return opts, ok, ans


def check(q, where):
    o, ok = q["opts"], q["ok"]
    if len(o) != 5:
        raise AssertionError(f"{where}: 5 variant olmalıdır: {o}")
    if len(set(o)) != 5:
        raise AssertionError(f"{where}: eyni variantlar var: {o}")
    if any(not str(x).strip() for x in o):
        raise AssertionError(f"{where}: boş variant: {o}")
    if sum(bool(x) for x in ok) != 1:
        raise AssertionError(f"{where}: şərti {sum(bool(x) for x in ok)} variant ödəyir (1 olmalıdır)\n{q['t']}\n{o}\n{ok}")
    if not q.get("e"):
        raise AssertionError(f"{where}: izah yoxdur")


def build(grade, topic_id, templates, seed, used):
    r = random.Random(f"{seed}-{grade}-{topic_id}")
    made, per, i, guard = [], {}, 0, 0
    cap = -(-TOTAL // len(templates)) + 3
    while len(made) < TOTAL:
        guard += 1
        if guard > TOTAL * 4000:
            raise RuntimeError(f"{grade}/{topic_id}: unikal sual çatmır ({len(made)}); şablonlar: {per}")
        k = i % len(templates)
        i += 1
        if per.get(k, 0) >= cap:
            if all(per.get(j, 0) >= cap for j in range(len(templates))):
                cap += 1
            continue
        q = templates[k](r, grade)
        if q is None:
            continue
        check(q, f"{grade}/{topic_id}/{templates[k].__name__}")
        key = (q["t"], tuple(sorted(q["opts"])))
        if key in used or q["t"] in {m["t"] for m in made if m["_tpl"] == templates[k].__name__ and sorted(m["opts"]) == sorted(q["opts"])}:
            continue
        used.add(key)
        q["_tpl"] = templates[k].__name__
        per[k] = per.get(k, 0) + 1
        made.append(q)

    order = sorted(range(TOTAL), key=lambda k: (made[k]["_tpl"], r.random()))
    buckets = [[] for _ in range(QUIZZES)]
    for pos, k in enumerate(order):
        buckets[pos % QUIZZES].append(made[k])
    quizzes = []
    for qi, bucket in enumerate(buckets, 1):
        r.shuffle(bucket)
        out = []
        for n, q in enumerate(bucket, 1):
            # 9 və 11-ci sinif: hamısı çətin; 10-cu sinif: şablonun verdiyi (orta/çətin)
            diff = q.get("diff", "hard") if grade == 10 else "hard"
            item = {"id": f"g{grade}-{topic_id}-q{qi}-{n:02d}", "difficulty": diff}
            if q.get("passage"):
                item["passage"] = q["passage"]
            item.update({"text": q["t"], "type": "single", "options": q["opts"], "correctIndex": q["ok"].index(True),
                         "explanation": q["e"]})
            out.append(item)
        quizzes.append(out)
    return quizzes


def nconds(r, g):
    """Sinif səviyyəsinə görə şərtlərin sayı: 9 → 2, 10 → 2–3, 11 → 3–4"""
    return {9: 2, 10: r.choice([2, 3]), 11: r.choice([3, 4])}[g]


def dlevel(k):
    return "medium" if k <= 2 else "hard"
