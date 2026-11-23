"""İngilis dili sual bankı: 9, 10, 11-ci siniflər.

Grammar (10 mövzu) və Vocabulary (3 mövzu): hər mövzuya 90 sual (3 quiz × 30).
- Suallar çoxtələblidir: bir neçə boşluğu birlikdə doldurmaq (9–10: 2 boşluq, 11: 3 boşluq), düzgün cümləni seçmək,
  11-ci sinifdə isə «hər iki cümləsi düzgün olan variant».
- Variantlar oxşardır: əksər səhv variantlarda yalnız bir boşluq səhvdir.
- Distraktorlar yalnız şübhəsiz səhv formalardır; hər variant bəndlərin qaydasına görə yenidən yoxlanır.
Reading: hər sinif üçün 10 mətn × 8 sual (1 mətn = 1 quiz).

İşə salmaq:  python3 q_en.py
"""
from azbuild import build
from quiz import build_fixed, save_grade
from en_gram import GRAM_TOPICS
from en_vocab import VOCAB_TOPICS
from en_passages import PASSAGES
from en_read9 import R9
from en_read10 import R10
from en_read11 import R11

SEED = 2027
ORDER = ["eng-tense", "eng-cond", "eng-passive", "eng-article", "eng-quant", "eng-noun", "eng-adj", "eng-pron",
         "eng-num", "eng-adv", "eng-word", "eng-phrasal", "eng-prep"]
ALL = {**GRAM_TOPICS, **VOCAB_TOPICS}

# Köhnə mətnlərdən 8 sual saxlanır (ən sadə fakt sualları çıxarılır)
DROP = {"The Jam Stall": (0, 1), "Why Do Cats Purr?": (0, 1), "Bobik Comes Home": (2, 3), "A Beach Worth Saving": (2, 6),
        "How Habits Work": (0, 5), "A Letter from Abroad": (0, 1), "Farms That Grow Upwards": (0, 1),
        "In Defence of Boredom": (0, 4), "The Last Keeper": (0, 1)}
NEW = {9: R9, 10: R10, 11: R11}


def passages(g):
    old = [dict(title=p["title"], text=p["text"], qs=[q for i, q in enumerate(p["qs"]) if i not in DROP[p["title"]]])
           for p in PASSAGES if p["g"] == g]
    out = old + NEW[g]
    assert len(out) == 10, (g, len(out))
    for p in out:
        assert len(p["qs"]) == 8, (g, p["title"], len(p["qs"]))
    return out


def reading_quizzes(g):
    quizzes = []
    for p in passages(g):
        text = f"{p['title']}\n\n{p['text']}"
        quizzes.append([dict(t=q, a=a, d=d, passage=text, diff="medium" if (g == 10 and k < 3) else "hard",
                             e=f"Cavab mətnə əsaslanır: «{a}».")
                        for k, (q, a, d) in enumerate(p["qs"])])
    return quizzes


def main():
    used = set()
    for g in (9, 10, 11):
        topics = {tid: build(g, tid, ALL[tid][g], SEED, used) for tid in ORDER}
        topics["eng-reading"] = build_fixed(g, "eng-reading", reading_quizzes(g), seed=SEED)
        save_grade(g, "en", topics)


if __name__ == "__main__":
    main()
