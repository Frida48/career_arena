"""Quiz çərçivəsi: hər sinif × mövzu üçün 60 sual → 3 quiz × 20 sual.

Şablon funksiyası: fn(r, g) -> dict(
    t=mətn, a=düzgün cavab, d=[yanlış variantlar], e=izah, diff="medium"|"hard",
    fmt=formatlayıcı (ixtiyari), open=True (açıq sual, ixtiyari), passage=oxu mətni (ixtiyari))
r — random.Random, g — sinif (9, 10, 11).
"""
import json
import random
from pathlib import Path

from common import make_options, fr

OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "questions"
QUIZZES, PER_QUIZ = 3, 20
TOTAL = QUIZZES * PER_QUIZ


def build_topic(grade, subject, topic_id, templates, seed, open_every=0):
    """Şablonlardan 60 unikal sual yaradır və 3 quizə bölür (hər quizdə çətinlik qarışıq)."""
    r = random.Random(f"{seed}-{grade}-{topic_id}")
    made, keys = [], set()
    i = guard = 0
    while len(made) < TOTAL:
        guard += 1
        if guard > TOTAL * 400:
            raise RuntimeError(f"{grade}/{topic_id}: unikal sual çatmır ({len(made)})")
        tpl = templates[i % len(templates)]
        i += 1
        q = tpl(r, grade)
        fmt = q.get("fmt", fr)
        key = (q["t"], q.get("passage"), fmt(q["a"]))
        if key in keys:
            continue
        keys.add(key)
        made.append(q)

    # Çətinliyə görə növbələşdirərək 3 quizə payla
    order = sorted(range(TOTAL), key=lambda k: (made[k]["diff"] != "hard", r.random()))
    buckets = [[] for _ in range(QUIZZES)]
    for pos, k in enumerate(order):
        buckets[pos % QUIZZES].append(made[k])

    quizzes = []
    for qi, bucket in enumerate(buckets, 1):
        # Oxu mətni olan suallar ardıcıl qalsın
        r.shuffle(bucket)
        bucket.sort(key=lambda q: (q.get("passage") or ""))
        out = []
        for n, q in enumerate(bucket, 1):
            fmt = q.get("fmt", fr)
            item = {
                "id": f"g{grade}-{topic_id}-q{qi}-{n:02d}",
                "difficulty": q["diff"],
            }
            if q.get("passage"):
                item["passage"] = q["passage"]
            item["text"] = q["t"]
            is_open = q.get("open") or (open_every and n % open_every == 0
                                        and not isinstance(q["a"], str) and q.get("allow_open", True))
            if is_open:
                item["type"] = "open"
                item["answer"] = fmt(q["a"])
            else:
                opts, ci = make_options(r, q["a"], q.get("d", []), fmt)
                item["type"] = "single"
                item["options"] = opts
                item["correctIndex"] = ci
            item["explanation"] = q["e"]
            out.append(item)
        quizzes.append(out)
    return quizzes


def build_fixed(grade, topic_id, quizzes, seed):
    """Hazır quizlər (məs. Reading: hər quiz bir mətn + suallar). quizzes: [[dict(t,a,d,e,diff[,passage])]]"""
    r = random.Random(f"{seed}-{grade}-{topic_id}")
    out = []
    for qi, items in enumerate(quizzes, 1):
        qs = []
        for n, q in enumerate(items, 1):
            opts, ci = make_options(r, q["a"], q["d"], q.get("fmt", fr))
            item = {"id": f"g{grade}-{topic_id}-q{qi}-{n:02d}", "difficulty": q["diff"]}
            if q.get("passage"):
                item["passage"] = q["passage"]
            item.update({"text": q["t"], "type": "single", "options": opts, "correctIndex": ci, "explanation": q["e"]})
            qs.append(item)
        out.append(qs)
    return out


def save_grade(grade, subject, topics):
    """topics: {topic_id: [quiz1, quiz2, quiz3]}"""
    OUT.mkdir(parents=True, exist_ok=True)
    data = {"grade": grade, "subject": subject,
            "topics": [{"topicId": tid, "quizzes": qz} for tid, qz in topics.items()]}
    path = OUT / f"grade{grade}-{subject}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(q) for qz in topics.values() for q in qz)
    print(f"{path.name}: {len(topics)} mövzu, {n} sual")


def pick(r, pool, k, exclude=()):
    """pool-dan exclude-da olmayan k fərqli element"""
    cand = [x for x in dict.fromkeys(pool) if x not in exclude]
    return r.sample(cand, k)
