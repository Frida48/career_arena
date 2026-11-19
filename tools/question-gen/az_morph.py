"""Azərbaycan dili morfologiyası üçün köməkçilər: ahəng qanunu, şəkilçilər, söz analizləri."""
VOWELS = "aıoueəiöü"
BACK = "aıou"          # qalın
FRONT = "eəiöü"        # incə
ROUND = "oöuü"         # dodaqlanan
VOICED = set("bcdgğjlmnqrvyz")   # cingiltili samitlər (14)
VOICELESS = set("çfhkpsştx")       # kar samitlər (9)


def vowels(w):
    return [c for c in w.lower() if c in VOWELS]


def consonants(w):
    return [c for c in w.lower() if c.isalpha() and c not in VOWELS]


def syllables(w):
    return len(vowels(w))


def last_vowel(w):
    v = vowels(w)
    return v[-1] if v else "a"


def h2(w, back, front):
    """İkivariantlı şəkilçi: a/ə"""
    return back if last_vowel(w) in BACK else front


def h4(w):
    """Dördvariantlı sait: ı/i/u/ü"""
    v = last_vowel(w)
    return {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "ə": "i", "i": "i", "ö": "ü", "ü": "ü"}[v]


def ends_vowel(w):
    return w[-1] in VOWELS


def soften(w):
    """Saitlə başlayan şəkilçidən əvvəl son k → y, q → ğ (çoxhecalı sözlərdə)"""
    if syllables(w) > 1 and w.endswith("k"):
        return w[:-1] + "y"
    if syllables(w) > 1 and w.endswith("q"):
        return w[:-1] + "ğ"
    return w


def add_vowel_suffix(w, suf, buffer="y"):
    """Saitlə başlayan şəkilçi: sözdən sonra bufer samit və ya yumşalma"""
    if ends_vowel(w):
        return w + buffer + suf
    return soften(w) + suf


# ---------- İsim: hallar və mənsubiyyət ----------

def case(n, c):
    if c == "yiyəlik":
        return add_vowel_suffix(n, h4(n) + "n", "n")
    if c == "yönlük":
        return add_vowel_suffix(n, h2(n, "a", "ə"), "y")
    if c == "təsirlik":
        return add_vowel_suffix(n, h4(n), "n")
    if c == "yerlik":
        return n + h2(n, "da", "də")
    if c == "çıxışlıq":
        return n + h2(n, "dan", "dən")
    return n


def possessive(n, person):
    v = h4(n)
    if person == "I şəxs tək":
        return n + "m" if ends_vowel(n) else soften(n) + v + "m"
    if person == "I şəxs cəm":
        return n + "m" + v + "z" if ends_vowel(n) else soften(n) + v + "m" + v + "z"
    if person == "II şəxs cəm":
        return n + "n" + v + "z" if ends_vowel(n) else soften(n) + v + "n" + v + "z"
    raise ValueError(person)


# ---------- Feil formaları ----------
# stem: əsas; vstem: saitlə başlayan şəkilçidən əvvəlki variant (get → ged)

def _v(stem, vstem):
    return vstem or stem


def form(stem, kind, vstem=None):
    vs = _v(stem, vstem)
    a = h2(stem, "a", "ə")
    i = h4(stem)
    if kind == "məsdər":
        return stem + h2(stem, "maq", "mək")
    if kind == "feili sifət -an":
        return add_vowel_suffix(vs, a + "n")
    if kind == "feili sifət -mış":
        return stem + "m" + i + "ş"
    if kind == "feili sifət -acaq":
        return add_vowel_suffix(vs, a + "c" + a + h2(stem, "q", "k"))
    if kind == "feili sifət -dığı":
        return stem + "d" + i + h2(stem, "ğ", "y") + i
    if kind == "feili bağlama -araq":
        return add_vowel_suffix(vs, a + "r" + a + h2(stem, "q", "k"))
    if kind == "feili bağlama -ıb":
        return add_vowel_suffix(vs, i + "b")
    if kind == "feili bağlama -anda":
        return add_vowel_suffix(vs, a + "nd" + a)
    if kind == "feili bağlama -madan":
        return stem + h2(stem, "madan", "mədən")
    if kind == "feili bağlama -dıqca":
        return stem + "d" + i + h2(stem, "qca", "kcə")
    if kind == "feili bağlama -ınca":
        return add_vowel_suffix(vs, i + "nc" + a)
    raise ValueError(kind)


def tense_1sg(stem, tense, vstem=None):
    """I şəxs tək"""
    vs = _v(stem, vstem)
    a = h2(stem, "a", "ə")
    i = h4(stem)
    if tense == "şühudi keçmiş zaman":
        return stem + "d" + i + "m"
    if tense == "nəqli keçmiş zaman":
        return stem + "m" + i + "ş" + a + "m"
    if tense == "indiki zaman":
        base = add_vowel_suffix(vs, i + "r")
        return base + a + "m"
    if tense == "qəti gələcək zaman":
        return add_vowel_suffix(vs, a + "c" + a + h2(stem, "ğ", "y") + a + "m")
    if tense == "qeyri-qəti gələcək zaman":
        return add_vowel_suffix(vs, a + "r" + a + "m")
    raise ValueError(tense)


def mood(stem, m, vstem=None):
    vs = _v(stem, vstem)
    a = h2(stem, "a", "ə")
    i = h4(stem)
    if m == "əmr şəkli":
        return stem + "s" + i + "n"
    if m == "şərt şəkli":
        return stem + "s" + a + "m"
    i2 = h2(stem, "ı", "i")  # -a/-ə və -malı/-məli şəkilçisindən sonrakı sait ikivariantlıdır
    if m == "arzu şəkli":
        return add_vowel_suffix(vs, a + "yd" + i2 + "m")
    if m == "lazım şəkli":
        return stem + "m" + a + "l" + i2 + "y" + a + "m"
    raise ValueError(m)


def negative_past(stem):
    return stem + h2(stem, "ma", "mə") + "d" + h2(stem, "ı", "i")


def passive_past(stem, vstem=None):
    """Məchul növ, şühudi keçmiş: yazıldı, oxundu, alındı"""
    i = h4(stem)
    if ends_vowel(stem):
        p = stem + "n"
    elif stem.endswith("l"):
        p = _v(stem, vstem) + i + "n"
    else:
        p = _v(stem, vstem) + i + "l"
    return p + "d" + h4(p)


# Qarşılıq-birgəlik və icbar növləri qeyri-qaydalı ola bildiyi üçün yalnız yoxlanmış hazır formalar
RECIPROCAL = ["görüşdülər", "yazışdılar", "vuruşdular", "döyüşdülər", "salamlaşdılar", "qucaqlaşdılar",
              "barışdılar", "deyişdilər", "sözləşdilər", "atışdılar"]
CAUSATIVE = ["yazdırdı", "oxutdu", "aldırdı", "tikdirdi", "sildirdi", "satdırdı", "açdırdı", "qurdurdu",
             "tapdırdı", "yığdırdı", "işlətdi", "təmizlətdi", "dinlətdi", "ağlatdı", "güldürdü", "qaçırtdı"]
REFLEXIVE = ["yuyundu", "geyindi", "darandı", "bəzəndi", "isindi", "soyundu", "örtündü", "gizləndi"]


def ordinal(n):
    """5 → 5-ci, 3 → 3-cü, 6 → 6-cı, 10 → 10-cu"""
    from common import _last_word
    v, _ = _last_word(n)
    suf = {"a": "cı", "ı": "cı", "e": "ci", "ə": "ci", "i": "ci", "o": "cu", "u": "cu", "ö": "cü", "ü": "cü"}[v]
    return f"{n}-{suf}"
