"""Riyaziyyat sual bankının qurucusu.

Hər şablon fn(r, g) -> dict:
    t    — mətn
    a    — düzgün cavab (int / Fraction / Num)
    d    — yanlış variantlar (oxşar, tipik səhvlərdən)
    e    — izah
    chk  — MÜSTƏQİL üsulla hesablanmış cavab (sadalama, koordinat, ədədi yoxlama). a ilə üst-üstə düşməsə — dayanır
    diff — "medium" | "hard" (yalnız 10-cu sinifdə nəzərə alınır; 9 və 11-də hamısı "hard")
    img  — SVG (ixtiyari)
    open — False: açıq suala çevirmə

Sətir cavablı suallar (məs. sıralama) Num(mətn, kod) ilə verilir: düzgün variantın kodu chk ilə yoxlanır.
"""
import random
from fractions import Fraction as F

from mx import Num, options, check, show, H

QUIZZES, PER_QUIZ = 3, 20
TOTAL = QUIZZES * PER_QUIZ
OPEN_EVERY = 7


def _openable(a):
    if isinstance(a, Num):
        return False
    return isinstance(a, (int, F)) and abs(F(a).denominator) <= 99


def build(grade, topic_id, templates, seed, used):
    """60 unikal sual → 3 quiz. used — bütün siniflər üzrə istifadə olunmuş mətnlər (siniflər fərqli olsun)."""
    r = random.Random(f"{seed}-{grade}-{topic_id}")
    made, i, guard = [], 0, 0
    per_tpl = {}
    cap = -(-TOTAL // len(templates)) + 2  # bir şablon quizi doldurmasın
    while len(made) < TOTAL:
        guard += 1
        if guard > TOTAL * 3000:
            raise RuntimeError(f"{grade}/{topic_id}: unikal sual çatmır ({len(made)})")
        k = i % len(templates)
        tpl = templates[k]
        i += 1
        if per_tpl.get(k, 0) >= cap:
            if all(per_tpl.get(j, 0) >= cap for j in range(len(templates))):
                cap += 1
            continue
        q = tpl(r, grade)
        where = f"{grade}/{topic_id}/{tpl.__name__}"
        check(q, where)
        if q["t"] in used:
            continue
        # variantlar burada qurulur ki, distraktor çatmazsa xəta dərhal çıxsın
        q["_opts"] = options(r, q["a"], q.get("d", []))
        used.add(q["t"])
        q["_tpl"] = tpl.__name__
        per_tpl[k] = per_tpl.get(k, 0) + 1
        made.append(q)

    if grade == 10:
        for q in made:
            q["diff"] = q.get("diff", H)
    else:
        for q in made:
            q["diff"] = H

    # Şablonlar quizlərə bərabər paylansın
    order = sorted(range(TOTAL), key=lambda k: (made[k]["_tpl"], r.random()))
    buckets = [[] for _ in range(QUIZZES)]
    for pos, k in enumerate(order):
        buckets[pos % QUIZZES].append(made[k])

    quizzes = []
    for qi, bucket in enumerate(buckets, 1):
        r.shuffle(bucket)
        out = []
        for n, q in enumerate(bucket, 1):
            item = {"id": f"g{grade}-{topic_id}-q{qi}-{n:02d}", "difficulty": q["diff"], "text": q["t"]}
            if q.get("img"):
                item["image"] = q["img"]
            if n % OPEN_EVERY == 0 and q.get("open", True) and _openable(q["a"]):
                item["type"] = "open"
                item["answer"] = show(q["a"])
            else:
                opts, ci = q["_opts"]
                item["type"] = "single"
                item["options"] = opts
                item["correctIndex"] = ci
            item["explanation"] = q["e"]
            out.append(item)
        quizzes.append(out)
    return quizzes
