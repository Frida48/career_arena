"""İngilis dili sual çərçivəsi: boşluqlu bəndlər (Gap) və onlardan qurulan çoxtələbli suallar.

Gap: frame — «___» olan cümlə; ok — düzgün doldurma; bad — YALNIZ qrammatik/leksik baxımdan şübhəsiz səhv olan
doldurmalar (kontekstə görə düzgün sayıla biləcək variantlar distraktor kimi götürülmür); why — qısa qayda.
Hər sualın variantlarında hər boşluq yenidən yoxlanır: variant düzgündürsə, bütün boşluqlar ok ilə doldurulub.
"""
import re
from itertools import product as iproduct

ZERO = "—"


class Gap:
    __slots__ = ("frame", "ok", "bad", "why", "lvl")

    def __init__(self, frame, ok, bad, why, lvl=1):
        assert "___" in frame and frame.count("___") == 1, frame
        bad = [b for b in dict.fromkeys(bad) if b != ok]
        assert bad, frame
        self.frame, self.ok, self.bad, self.why, self.lvl = frame, ok, bad, why, lvl

    def fill(self, w):
        if w == ZERO:
            s = self.frame.replace(" ___ ", " ").replace("___ ", "").replace(" ___", "")
        else:
            s = self.frame.replace("___", w)
        return s[0].upper() + s[1:] if s else s

    def sent(self, w):
        """Tam cümlə variantı üçün: mötərizədəki ipucları (feilin əsas forması və s.) silinir"""
        return re.sub(r" \([^()]*\)", "", self.fill(w))


def _pool(items, g):
    lv = {9: (1, 2), 10: (1, 2, 3), 11: (2, 3)}[g]
    return [x for x in items if x.lvl in lv]


def multi_gap(items, note=""):
    def tpl(r, g):
        pool = _pool(items, g)
        k = 3 if g == 11 else 2
        frames = set()
        chosen = []
        for it in r.sample(pool, len(pool)):
            if it.frame in frames:
                continue
            chosen.append(it)
            frames.add(it.frame)
            if len(chosen) == k:
                break
        if len(chosen) < k:
            return None
        right = tuple(it.ok for it in chosen)
        cands = []
        for combo in iproduct(*[[it.ok] + it.bad for it in chosen]):
            if combo != right:
                cands.append(combo)
        r.shuffle(cands)
        cands.sort(key=lambda c: sum(a != b for a, b in zip(c, right)))  # bir boşluğu səhv olanlar əvvəl
        rend = lambda c: " / ".join(c)
        picked, seen = [], {rend(right)}
        for c in cands:
            if rend(c) not in seen:
                picked.append(c)
                seen.add(rend(c))
            if len(picked) == 4:
                break
        if len(picked) < 4:
            return None
        opts_c = picked + [right]
        r.shuffle(opts_c)
        stem = " ".join(f"({i + 1}) {it.frame}" for i, it in enumerate(chosen))
        ok = [all(a == it.ok for a, it in zip(c, chosen)) for c in opts_c]
        return dict(t=f"Choose the option that correctly completes all the gaps{note}: {stem}",
                    opts=[rend(c) for c in opts_c], ok=ok, diff="medium" if all(it.lvl == 1 for it in chosen) else "hard",
                    e=" ".join(f"({i + 1}) {it.ok} — {it.why}" for i, it in enumerate(chosen)))
    tpl.__name__ = "multi_gap"
    return tpl


def correct_sentence(items, ask="Which sentence is grammatically correct?"):
    """Bir düzgün cümlə + başqa bəndlərdən 4 səhv cümlə"""
    def tpl(r, g):
        pool = _pool(items, g)
        right = r.choice(pool)
        others = [x for x in pool if x.frame != right.frame]
        r.shuffle(others)
        picked, seen = [], {right.sent(right.ok)}
        for it in others:
            s = it.sent(r.choice(it.bad))
            if s not in seen:
                picked.append((it, s))
                seen.add(s)
            if len(picked) == 4:
                break
        if len(picked) < 4:
            return None
        items_ = picked + [(right, right.sent(right.ok))]
        r.shuffle(items_)
        opts = [s for _, s in items_]
        ok = [s == it.sent(it.ok) for it, s in items_]
        return dict(t=ask, opts=opts, ok=ok, diff="medium" if right.lvl == 1 else "hard",
                    e=f"Correct: «{right.sent(right.ok)}» — {right.why}. The other sentences each contain an error.")
    tpl.__name__ = "correct_sentence"
    return tpl


def correct_pair(items, ask="In which option are BOTH sentences grammatically correct?"):
    """İki cümləlik variantlar: yalnız birində hər iki cümlə düzgündür (11-ci sinif üçün)"""
    def tpl(r, g):
        pool = _pool(items, g)
        a, b = r.sample(pool, 2)
        if a.frame == b.frame:
            return None
        cand = []
        for wa in [a.ok] + a.bad:
            for wb in [b.ok] + b.bad:
                cand.append((wa, wb))
        right = (a.ok, b.ok)
        wrong = [c for c in cand if c != right]
        r.shuffle(wrong)
        wrong.sort(key=lambda c: (c[0] != a.ok) + (c[1] != b.ok))
        rend = lambda c: f"{a.sent(c[0])} {b.sent(c[1])}"
        picked, seen = [], {rend(right)}
        for c in wrong:
            if rend(c) not in seen:
                picked.append(c)
                seen.add(rend(c))
            if len(picked) == 4:
                break
        if len(picked) < 4:
            # əlavə səhv cütləri başqa bəndlərdən
            return None
        opts_c = picked + [right]
        r.shuffle(opts_c)
        return dict(t=ask, opts=[rend(c) for c in opts_c],
                    ok=[c == right for c in opts_c], diff="hard", e=f"{a.ok} — {a.why}; {b.ok} — {b.why}.")
    tpl.__name__ = "correct_pair"
    return tpl


def topic(items, note=""):
    t = [multi_gap(items, note), correct_sentence(items)]
    return {9: t, 10: t, 11: t + [correct_pair(items)]}
