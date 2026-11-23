"""İsim (mənsubiyyət + hal) və feil (zaman, şəxs, inkar, əmr şəkli) formaları — qaydalarla.
Yalnız yoxlanmış, qaydaya tabe olan köklər işlənir (istisna kökləri yoxdur)."""
from az_morph import h2, h4, soften, ends_vowel, add_vowel_suffix, VOWELS, BACK

# ---------------- İsim ----------------
PERS = ["I şəxs tək", "II şəxs tək", "III şəxs tək", "I şəxs cəm", "II şəxs cəm"]
PRON_GEN = {"I şəxs tək": "mənim", "II şəxs tək": "sənin", "III şəxs tək": "onun", "I şəxs cəm": "bizim", "II şəxs cəm": "sizin"}
CASES = ["adlıq", "yiyəlik", "yönlük", "təsirlik", "yerlik", "çıxışlıq"]


def poss(n, p):
    if ends_vowel(n):
        return {"I şəxs tək": n + "m", "II şəxs tək": n + "n", "III şəxs tək": n + "s" + h4(n),
                "I şəxs cəm": n + "m" + h4(n) + "z", "II şəxs cəm": n + "n" + h4(n) + "z"}[p]
    b = soften(n) + h4(n)
    return {"I şəxs tək": b + "m", "II şəxs tək": b + "n", "III şəxs tək": b,
            "I şəxs cəm": b + "m" + h4(n) + "z", "II şəxs cəm": b + "n" + h4(n) + "z"}[p]


def poss_case(n, p, c):
    w = poss(n, p)
    if c == "adlıq":
        return w
    if p == "III şəxs tək":  # sait + n bufer
        return {"yiyəlik": w + "n" + h4(w) + "n", "yönlük": w + "n" + h2(w, "a", "ə"), "təsirlik": w + "n" + h4(w),
                "yerlik": w + "nd" + h2(w, "a", "ə"), "çıxışlıq": w + "nd" + h2(w, "an", "ən")}[c]
    return {"yiyəlik": w + h4(w) + "n", "yönlük": w + h2(w, "a", "ə"), "təsirlik": w + h4(w),
            "yerlik": w + "d" + h2(w, "a", "ə"), "çıxışlıq": w + "d" + h2(w, "an", "ən")}[c]


# ---------------- Feil ----------------
VPERS = ["I şəxs tək", "II şəxs tək", "III şəxs tək", "I şəxs cəm", "II şəxs cəm", "III şəxs cəm"]
PRON = {"I şəxs tək": "Mən", "II şəxs tək": "Sən", "III şəxs tək": "O,", "I şəxs cəm": "Biz", "II şəxs cəm": "Siz",
        "III şəxs cəm": "Onlar"}
TENSES = ["şühudi keçmiş zaman", "indiki zaman", "qəti gələcək zaman"]


def _iq(x):
    """I şəxs cəm: -q/-k (şühudi keçmiş)"""
    return "q" if [c for c in x if c in VOWELS][-1] in BACK else "k"


def conj(stem, tense, p, neg=False, vstem=None):
    vs = vstem or stem
    if tense == "şühudi keçmiş zaman":
        base = stem + (h2(stem, "ma", "mə") if neg else "")
        x = base + "d" + h4(base)
        return {"I şəxs tək": x + "m", "II şəxs tək": x + "n", "III şəxs tək": x, "I şəxs cəm": x + _iq(x),
                "II şəxs cəm": x + "n" + h4(x) + "z", "III şəxs cəm": x + h2(x, "lar", "lər")}[p]
    if tense == "indiki zaman":
        x = stem + "m" + h4(stem) + "r" if neg else add_vowel_suffix(vs, h4(stem) + "r")
        return {"I şəxs tək": x + h2(x, "am", "əm"), "II şəxs tək": x + h2(x, "san", "sən"), "III şəxs tək": x,
                "I şəxs cəm": x + h4(x) + _iq(x), "II şəxs cəm": x + "s" + h4(x) + "n" + h4(x) + "z",
                "III şəxs cəm": x + h2(x, "lar", "lər")}[p]
    if tense == "qəti gələcək zaman":
        x = (stem + h2(stem, "ma", "mə") + "y" + h2(stem, "acaq", "əcək")) if neg else add_vowel_suffix(vs, h2(stem, "acaq", "əcək"))
        return {"I şəxs tək": soften(x) + h2(x, "am", "əm"), "II şəxs tək": x + h2(x, "san", "sən"), "III şəxs tək": x,
                "I şəxs cəm": soften(x) + h2(x, "ıq", "ik"), "II şəxs cəm": x + h2(x, "sınız", "siniz"),
                "III şəxs cəm": x + h2(x, "lar", "lər")}[p]
    raise ValueError(tense)


# (kök, saitdən əvvəlki kök, tamamlıq) — yalnız qaydaya tabe köklər
VERBS = [("yaz", None, "məktubu"), ("oxu", None, "kitabı"), ("al", None, "bileti"), ("gör", None, "tamaşanı"),
         ("iç", None, "çayı"), ("sev", None, "bu mahnını"), ("tap", None, "açarı"), ("bil", None, "cavabı"),
         ("dinlə", None, "musiqini"), ("aç", None, "qapını"), ("bağla", None, "pəncərəni"), ("çək", None, "şəkli"),
         ("sat", None, "maşını"), ("tik", None, "evi"), ("qur", None, "çadırı"), ("yığ", None, "almaları"),
         ("sil", None, "lövhəni"), ("götür", None, "çantanı"), ("öyrən", None, "şeiri"), ("unut", None, "tapşırığı")]
NOUNS = ["kitab", "dəftər", "məktub", "məqalə", "hekayə", "lüğət", "layihə", "rəsm", "çanta", "şeir"]


if __name__ == "__main__":
    for n in ("kitab", "məqalə", "çanta", "lüğət"):
        for p in PERS:
            print(n, p, [poss_case(n, p, c) for c in CASES])
    for v, vs, _ in [("yaz", None, 0), ("oxu", None, 0), ("gör", None, 0), ("dinlə", None, 0), ("çək", None, 0)]:
        for t in TENSES:
            print(v, t, [conj(v, t, p, False, vs) for p in VPERS], [conj(v, t, p, True, vs) for p in VPERS])
