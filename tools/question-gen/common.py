"""Ortaq köməkçilər: sual qurulması, formatlama, distraktorlar."""
import json
import random
from fractions import Fraction as F
from pathlib import Path

LETTERS = "ABCDE"
OUT = Path(__file__).resolve().parents[2] / "src" / "data" / "questions"


def fr(x):
    """Fraction/int -> 'a/b' və ya tam ədəd mətni."""
    if isinstance(x, str):
        return x
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def dec(x):
    """Onluq kəsri vergüllə yaz (Azərbaycan qaydası)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.4f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _fallback(a):
    """Rəqəm cavab üçün əlavə yanlış variantlar."""
    if isinstance(a, str):
        return []
    a = F(a)
    out = [a + 1, a - 1, a + 2, a - 2, 2 * a, -a, a + 3, a * 3, a + 5, a - 4]
    return out


def make_options(rng, answer, distractors, fmt=fr):
    seen = []
    ans = fmt(answer)
    for d in list(distractors) + _fallback(answer):
        s = fmt(d)
        if s != ans and s not in seen:
            seen.append(s)
        if len(seen) == 4:
            break
    if len(seen) < 4:
        raise ValueError(f"Kifayət qədər distraktor yoxdur: {answer} {distractors}")
    opts = seen + [ans]
    rng.shuffle(opts)
    return opts, opts.index(ans)


def build_section(grade, subject, section_id, section_title, templates, seed, count=30,
                  open_every=6):
    """templates: rng -> dict(t, a, d, e, topic, diff[, open][, fmt])
    Şablonlar növbə ilə işlədilir; eyni mətnli suallar atılır.
    open_every: hər N-ci sual açıq (kodlaşdırıla bilən) cavablı olur (yalnız rəqəm cavablarda)."""
    rng = random.Random(seed)
    qs, texts = [], set()
    i, guard = 0, 0
    while len(qs) < count:
        guard += 1
        if guard > count * 60:
            raise RuntimeError(f"{section_id}: unikal sual çatmır ({len(qs)})")
        tpl = templates[i % len(templates)]
        i += 1
        q = tpl(rng)
        if q["t"] in texts:
            continue
        texts.add(q["t"])
        n = len(qs) + 1
        item = {
            "id": f"g{grade}-{subject}-{section_id}-{n:03d}",
            "grade": grade,
            "subject": subject,
            "sectionId": section_id,
            "sectionTitle": section_title,
            "topic": q["topic"],
            "difficulty": q["diff"],
            "text": q["t"],
        }
        fmt = q.get("fmt", fr)
        want_open = q.get("open") or (open_every and n % open_every == 0
                                      and not isinstance(q["a"], str) and q.get("allow_open", True))
        if want_open:
            item["type"] = "open"
            item["answer"] = fmt(q["a"])
        else:
            opts, ci = make_options(rng, q["a"], q.get("d", []), fmt)
            item["type"] = "single"
            item["options"] = opts
            item["correctIndex"] = ci
        item["explanation"] = q["e"]
        qs.append(item)
    return qs


def handwritten(grade, subject, section_id, section_title, items, seed):
    """Əl ilə yazılmış suallar: (topic, diff, text, correct, [4 yanlış], izah)."""
    rng = random.Random(seed)
    qs = []
    for n, it in enumerate(items, 1):
        topic, diff, text, correct, wrong, expl = it[:6]
        passage = it[6] if len(it) > 6 else None
        assert len(wrong) == 4, (section_id, n, text)
        assert correct not in wrong, (section_id, n, text)
        assert len(set(wrong)) == 4, (section_id, n, text)
        opts = list(wrong) + [correct]
        rng.shuffle(opts)
        q = {
            "id": f"g{grade}-{subject}-{section_id}-{n:03d}",
            "grade": grade,
            "subject": subject,
            "sectionId": section_id,
            "sectionTitle": section_title,
            "topic": topic,
            "difficulty": diff,
        }
        if passage:
            q["passage"] = passage
        q.update({
            "text": text,
            "type": "single",
            "options": opts,
            "correctIndex": opts.index(correct),
            "explanation": expl,
        })
        qs.append(q)
    return qs


def save(grade, subject, sections):
    """sections: [(section_id, title, [questions], description)]"""
    OUT.mkdir(exist_ok=True)
    data = {
        "grade": grade,
        "subject": subject,
        "sections": [{"id": sec[0], "title": sec[1], "description": sec[3] if len(sec) > 3 else "",
                      "questions": sec[2]} for sec in sections],
    }
    path = OUT / f"grade{grade}-{subject}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path.name, sum(len(s[2]) for s in sections), "sual")
