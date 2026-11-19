"""Azərbaycan dili: 8 mövzu × 3 sinif × 60 sual (orta-çətin).
Suallar söz/cümlə banklarından qurulur; fonetik və morfoloji cavablar qaydalarla hesablanır."""
from az_morph import (BACK, FRONT, ROUND, VOICED, VOICELESS, vowels, consonants, syllables, case, possessive, form,
                      tense_1sg, mood, negative_past, passive_past, RECIPROCAL, CAUSATIVE, REFLEXIVE, ordinal, h4,
                      add_vowel_suffix, ends_vowel, soften)
from quiz import build_topic, save_grade, pick

M, H = "medium", "hard"

# ======================= Səs və hərf =======================
WORDS = """qardaş bacı torpaq ağac quzu qonaq yarpaq qaranlıq uşaq dəniz ürək çiçək gözəl dəftər ölkə köynək böyük kiçik
gecə səhər bulud yağış balıq ayaq qulaq dodaq barmaq ərik üzüm şəkər düymə gümüş sünbül qarışqa yumurta oyuncaq oxucu
yazıçı sevinc ümid örtük dəyirman qayıq otaq qapı pəncərə divar kitab məktub telefon kompüter insan kino radio teatr
müəllim tələbə kağız qələm dünya xəstə həkim ailə mədəniyyət ədəbiyyat qanun şagird dəqiqə zaman hava xalça maşın
avtobus metro səyahət kitabxana təşəkkür cəmiyyət ayaqqabı saqqal səkkiz doqquz yeddi əlli kassa müəllif imtahan
təbiət istirahət vətən xəbər tarix coğrafiya musiqi bayram çörək dovşan qartal bülbül göyərçin quyruq buludlu gündüz
axşam günəş ulduz yuxu nağıl tapmaca dostluq sərçə yumşaq qırmızı yaşıl sarı bənövşə lalə qızılgül ərzaq sükut
səadət cəsarət ədalət iştirak təhsil şəhər kənd meşə çay göl bağ bostan şaftalı armud gilas alça portağal limon
universitet akademiya müvəffəqiyyət konstitusiya biologiya olimpiada laboratoriya televizor ekskursiya riyaziyyat""".split()


def _harmonic(w):
    v = vowels(w)
    return all(c in BACK for c in v) or all(c in FRONT for c in v)


def snd_syllables(r, g):
    n = r.choice([3, 4] if g == 9 else [3, 4, 5])
    good = [w for w in WORDS if syllables(w) == n]
    bad = [w for w in WORDS if syllables(w) != n]
    w = r.choice(good)
    return dict(t=f"Hansı söz {n} hecalıdır?", a=w, d=pick(r, bad, 4),
                e=f"Heca sayı sait sayına bərabərdir: «{w}» sözündə {n} sait var ({', '.join(vowels(w))}).", diff=M)


def snd_harmony(r, g):
    good = [w for w in WORDS if not _harmonic(w)]
    bad = [w for w in WORDS if _harmonic(w) and syllables(w) >= 2]
    w = r.choice(good)
    return dict(t="Hansı söz ahəng qanununa (qalın-incəlik ahənginə) tabe deyil?", a=w, d=pick(r, bad, 4),
                e=f"«{w}» sözündə həm qalın, həm incə sait var: {', '.join(vowels(w))}. Bu, adətən alınma sözlər üçün xarakterikdir.", diff=M)


def snd_back_front(r, g):
    want = r.choice(["qalın", "incə"])
    group = BACK if want == "qalın" else FRONT
    good = [w for w in WORDS if all(c in group for c in vowels(w)) and syllables(w) >= 2]
    bad = [w for w in WORDS if any(c not in group for c in vowels(w))]
    w = r.choice(good)
    return dict(t=f"Hansı sözdə yalnız {want} saitlər var?", a=w, d=pick(r, bad, 4),
                e=f"Qalın saitlər: a, ı, o, u; incə saitlər: e, ə, i, ö, ü. «{w}»: {', '.join(vowels(w))}.", diff=M)


def snd_round(r, g):
    k = r.choice([0, 2])
    good = [w for w in WORDS if sum(c in ROUND for c in vowels(w)) == k and syllables(w) >= 2]
    bad = [w for w in WORDS if sum(c in ROUND for c in vowels(w)) != k]
    w = r.choice(good)
    txt = "dodaqlanan sait yoxdur" if k == 0 else "iki dodaqlanan sait var"
    return dict(t=f"Hansı sözdə {txt}?", a=w, d=pick(r, bad, 4),
                e=f"Dodaqlanan saitlər: o, ö, u, ü. «{w}» sözündə onların sayı {k}.", diff=M if k == 0 else H)


def snd_voiced(r, g):
    good = [w for w in WORDS if consonants(w) and all(c in VOICED for c in consonants(w)) and len(consonants(w)) >= 2]
    bad = [w for w in WORDS if any(c in VOICELESS for c in consonants(w))]
    w = r.choice(good)
    return dict(t="Hansı sözdə bütün samitlər cingiltilidir?", a=w, d=pick(r, bad, 4),
                e=f"«{w}» sözünün samitləri ({', '.join(consonants(w))}) cingiltilidir. Kar samitlər: ç, f, h, k, p, s, ş, t, x.", diff=H)


def snd_count(r, g):
    w = r.choice([x for x in WORDS if len(x) >= 6])
    kind = r.choice(["samit", "sait", "kar samit", "cingiltili samit"])
    if kind == "samit":
        n = len(consonants(w))
    elif kind == "sait":
        n = len(vowels(w))
    elif kind == "kar samit":
        n = sum(c in VOICELESS for c in consonants(w))
    else:
        n = sum(c in VOICED for c in consonants(w))
    return dict(t=f"«{w}» sözündə neçə {kind} var?", a=n, d=[x for x in range(0, 9) if x != n][:6] if n > 2 else [n + 1, n + 2, n + 3, n + 4],
                e=f"«{w}»: saitlər — {', '.join(vowels(w))}; samitlər — {', '.join(consonants(w))}. Cavab: {n}.", diff=M if kind in ("samit", "sait") else H)


def snd_double(r, g):
    def dbl(w):
        return any(w[i] == w[i + 1] and w[i] not in "aıoueəiöü" for i in range(len(w) - 1))
    good = [w for w in WORDS if dbl(w)]
    bad = [w for w in WORDS if not dbl(w) and len(w) >= 5]
    w = r.choice(good)
    return dict(t="Hansı sözdə qoşa samit var?", a=w, d=pick(r, bad, 4), e=f"«{w}» sözündə yanaşı iki eyni samit yazılır.", diff=M)


def snd_equal(r, g):
    good = [w for w in WORDS if len(vowels(w)) == len(consonants(w)) and len(w) >= 4]
    bad = [w for w in WORDS if len(vowels(w)) != len(consonants(w)) and len(w) >= 4]
    w = r.choice(good)
    return dict(t="Hansı sözdə saitlərin sayı samitlərin sayına bərabərdir?", a=w, d=pick(r, bad, 4),
                e=f"«{w}»: {len(vowels(w))} sait, {len(consonants(w))} samit.", diff=H)


# ======================= Orfoqrafiya =======================
ORTHO = """müəllim müəssisə təəssüf mədəniyyət ədəbiyyat inşaat müvəffəqiyyət təşəkkür ehtiyac mühüm şeir qiraət əhəmiyyət
müxtəlif istiqamət mütəxəssis elan saat bəzən kompüter redaktor cəmiyyət səhiyyə tələbə müəllif təəccüb mətbəə camaat
şöbə ailə şair müraciət müalicə təbiət səadət cəsarət ədalət səfər müsabiqə iştirak istirahət təhsil imtahan
şəhadətnamə attestat akademiya universitet fakültə laboratoriya ekskursiya kitabxana müzakirə mühazirə məsuliyyət
şəxsiyyət xüsusiyyət keyfiyyət kəmiyyət vəziyyət fəaliyyət ehtiram ehtiyat əhali əhval sənaye sənət qəzet jurnal
məqalə hekayə dastan nağıl tapmaca dərslik lüğət ensiklopediya coğrafiya kimya fizika riyaziyyat biologiya həndəsə
ehtimal statistika alqoritm proqram internet televizor avtomobil təyyarə sürücü mühəndis memar əczaçı xəstəxana
poliklinika temperatur termometr kilometr santimetr perimetr diametr trapesiya paraleloqram üçbucaq dəqiqə saniyə
həftə çərşənbə cümə şənbə sentyabr oktyabr noyabr dekabr müstəqillik respublika prezident parlament konstitusiya
vətəndaş hüquq vəzifə mükafat olimpiada idman şahmat gimnastika məşqçi komanda stadion qələbə məğlubiyyət rəqib
tamaşaçı aktyor rejissor musiqi bəstəkar müğənni opera balet muzey sərgi rəssam heykəltəraş memarlıq ayaqqabı
saqqal səkkiz doqquz əlli kassa ədəb qəhrəman mərhəmət səxavət hörmət mehriban""".split()
ORTHO_SET = set(ORTHO)

_SWAP = {"ə": "e", "e": "ə", "ı": "i", "i": "ı", "ü": "u", "u": "ü", "ö": "o", "o": "ö", "k": "q", "q": "k", "h": "x", "x": "h"}


def misspell(r, w, n=4):
    """Sözün n müxtəlif yanlış yazılışı (bank sözləri ilə üst-üstə düşmür)"""
    out, tries = set(), 0
    while len(out) < n and tries < 400:
        tries += 1
        i = r.randrange(len(w))
        rule = r.randrange(5)
        c = w[i]
        if rule == 0 and c in _SWAP:
            x = w[:i] + _SWAP[c] + w[i + 1:]
        elif rule == 1 and c not in "aıoueəiöü" and 0 < i < len(w) - 1 and w[i - 1] != c and w[i + 1] != c:
            x = w[:i] + c + w[i:]
        elif rule == 2 and i < len(w) - 1 and w[i] == w[i + 1]:
            x = w[:i] + w[i + 1:]
        elif rule == 3 and i < len(w) - 1 and w[i] in "aıoueəiöü" and w[i + 1] in "aıoueəiöü":
            x = w[:i + 1] + r.choice(["y", ""]) + w[i + 1:] if r.random() < 0.5 else w[:i] + w[i + 1:]
        elif rule == 4 and i == len(w) - 1 and c in "bdgc":
            x = w[:i] + {"b": "p", "d": "t", "g": "k", "c": "ç"}[c]
        else:
            continue
        if x != w and x not in ORTHO_SET and len(x) > 2:
            out.add(x)
    return list(out)


def ort_correct(r, g):
    w = r.choice(ORTHO)
    bad = misspell(r, w)
    if len(bad) < 4:
        return ort_correct(r, g)
    return dict(t="Hansı sözün yazılışı düzgündür?", a=w, d=bad, e=f"Düzgün yazılış: {w}.", diff=M)


def ort_wrong(r, g):
    w = r.choice(ORTHO)
    bad = misspell(r, w, 1)
    if not bad:
        return ort_wrong(r, g)
    return dict(t="Hansı söz səhv yazılıb?", a=bad[0], d=pick(r, ORTHO, 4, exclude={w}),
                e=f"Düzgün yazılış: {w}. Digər sözlər düzgün yazılıb.", diff=M)


def ort_rows(r, g):
    rows = []
    for _ in range(5):
        ws = r.sample(ORTHO, 3)
        rows.append(ws)
    good = ", ".join(rows[0])
    bad = []
    for ws in rows[1:]:
        k = r.randrange(3)
        m_ = misspell(r, ws[k], 1)
        if not m_:
            return ort_rows(r, g)
        ws = ws[:k] + m_ + ws[k + 1:]
        bad.append(", ".join(ws))
    return dict(t="Hansı sırada bütün sözlər düzgün yazılıb?", a=good, d=bad, e=f"Düzgün sıra: {good}. Digər sıralarda bir söz səhv yazılıb.", diff=H)


def _wrong_ordinal(n):
    right = ordinal(n).split("-")[1]
    return [f"{n}-{s}" for s in ["cı", "ci", "cu", "cü"] if s != right]


def ort_ordinal(r, g):
    nums = r.sample(list(range(2, 100)) + [100, 200, 1000, 2000, 2025, 2030, 1918, 1991], 5)
    good = ordinal(nums[0])
    bad = [r.choice(_wrong_ordinal(n)) for n in nums[1:]]
    return dict(t="Hansı sıra sayı rəqəmlə düzgün yazılıb?", a=good, d=bad,
                e=f"Sıra şəkilçisi sayın oxunuşundakı son saitə uyğunlaşır: {good}. Məs.: 3-cü, 6-cı, 9-cu, 20-ci.", diff=H)


DEFIS = ["ata-ana", "ev-eşik", "qab-qacaq", "səs-küy", "az-çox", "gec-tez", "tez-tez", "yavaş-yavaş", "el-oba", "toy-düyün",
         "çör-çöp", "pal-paltar", "ora-bura", "ara-sıra", "gecə-gündüz", "qohum-əqraba", "dost-tanış", "qız-gəlin", "böyük-kiçik"]
BITISIK = ["ayaqqabı", "ağsaqqal", "qayınata", "qayınana", "açıqgöz", "xoşbəxt", "bədbəxt", "yeraltı", "sualtı", "günəbaxan",
           "qızılgül", "dəvəquşu", "ağcaqanad", "istiqanlı", "əliaçıq", "həmyerli", "həmkar", "yarımada", "ikimərtəbəli",
           "beşillik", "üçbucaq", "dördbucaq", "çoxbucaqlı", "yerkökü"]


def _split_compound(w):
    """bitişik mürəkkəb sözü səhvən defislə yazılmış formaya sal"""
    for k in range(3, len(w) - 2):
        if w[k - 1] not in "aıoueəiöü" or w[k] not in "aıoueəiöü":
            if 3 <= k <= len(w) - 3:
                return w[:k] + "-" + w[k:]
    return w[:3] + "-" + w[3:]


_SPLITS = {"ayaqqabı": "ayaq-qabı", "ağsaqqal": "ağ-saqqal", "qayınata": "qayın-ata", "qayınana": "qayın-ana",
           "açıqgöz": "açıq-göz", "xoşbəxt": "xoş-bəxt", "bədbəxt": "bəd-bəxt", "yeraltı": "yer-altı", "sualtı": "su-altı",
           "günəbaxan": "günə-baxan", "qızılgül": "qızıl-gül", "dəvəquşu": "dəvə-quşu", "ağcaqanad": "ağca-qanad",
           "istiqanlı": "isti-qanlı", "əliaçıq": "əli-açıq", "həmyerli": "həm-yerli", "həmkar": "həm-kar",
           "yarımada": "yarım-ada", "ikimərtəbəli": "iki-mərtəbəli", "beşillik": "beş-illik", "üçbucaq": "üç-bucaq",
           "dördbucaq": "dörd-bucaq", "çoxbucaqlı": "çox-bucaqlı", "yerkökü": "yer-kökü"}


def ort_hyphen(r, g):
    if r.random() < 0.5:
        good = r.choice(DEFIS)
        bad = [x.replace("-", "") for x in pick(r, DEFIS, 2, exclude={good})] + [_SPLITS[x] for x in pick(r, BITISIK, 2)]
        rule = "Qoşa sözlər defislə yazılır"
    else:
        good = r.choice(BITISIK)
        bad = [_SPLITS[x] for x in pick(r, BITISIK, 2, exclude={good})] + [x.replace("-", "") for x in pick(r, DEFIS, 2)]
        rule = "Mürəkkəb sözlər bitişik yazılır"
    return dict(t="Hansı söz düzgün yazılıb?", a=good, d=bad, e=f"{rule}: {good}.", diff=H)


CAPITALS = [("Xəzər dənizi", ["xəzər dənizi", "Xəzər Dənizi", "XƏZƏR dənizi"]),
            ("Kür çayı", ["kür çayı", "Kür Çayı", "kür Çayı"]),
            ("Azərbaycan Respublikası", ["azərbaycan Respublikası", "Azərbaycan respublikası", "azərbaycan respublikası"]),
            ("Novruz bayramı", ["novruz bayramı", "Novruz Bayramı", "novruz Bayramı"]),
            ("Milli Məclis", ["milli məclis", "Milli məclis", "milli Məclis"]),
            ("Bakı Dövlət Universiteti", ["Bakı dövlət universiteti", "bakı Dövlət Universiteti", "Bakı Dövlət universiteti"]),
            ("Qafqaz dağları", ["qafqaz dağları", "Qafqaz Dağları", "qafqaz Dağları"]),
            ("Şuşa şəhəri", ["şuşa şəhəri", "Şuşa Şəhəri", "şuşa Şəhəri"]),
            ("Qız qalası", ["qız qalası", "Qız Qalası", "qız Qalası"]),
            ("Atlantik okeanı", ["atlantik okeanı", "Atlantik Okeanı", "atlantik Okeanı"]),
            ("Birləşmiş Millətlər Təşkilatı", ["Birləşmiş millətlər təşkilatı", "birləşmiş Millətlər Təşkilatı", "Birləşmiş Millətlər təşkilatı"])]


def ort_capital(r, g):
    good, wrongs = r.choice(CAPITALS)
    other = r.choice([c for c in CAPITALS if c[0] != good])
    return dict(t="Hansı ad düzgün yazılıb?", a=good, d=wrongs + [r.choice(other[1])],
                e=f"Xüsusi adın özü böyük hərflə yazılır; rəsmi adlarda hər söz böyük hərflə başlayır: {good}.", diff=M)


# ======================= Sinonim və antonim =======================
SYN = [["böyük", "iri", "yekə"], ["kiçik", "balaca", "xırda"], ["gözəl", "qəşəng", "göyçək"], ["ağıllı", "zəkalı", "dərrakəli"],
       ["cəsur", "igid", "qorxmaz"], ["sevinc", "fərəh", "şadlıq"], ["kədər", "qəm", "qüssə"], ["vətən", "yurd", "diyar"],
       ["dost", "yoldaş", "rəfiq"], ["üz", "sifət", "çöhrə"], ["cəld", "çevik", "zirək"], ["yavaş", "asta"], ["qoca", "yaşlı", "ahıl"],
       ["cavan", "gənc"], ["çalışqan", "zəhmətkeş"], ["tənbəl", "ərincək"], ["xəsis", "simic"], ["səxavətli", "əliaçıq", "comərd"],
       ["arzu", "istək", "dilək"], ["qorxu", "vahimə", "xof"], ["hörmət", "ehtiram"], ["səbr", "dözüm", "təmkin"],
       ["sakit", "dinc", "aram"], ["bərk", "möhkəm"], ["zəif", "gücsüz", "taqətsiz"], ["güclü", "qüvvətli", "qüdrətli"],
       ["varlı", "dövlətli", "zəngin"], ["kasıb", "yoxsul"], ["məşhur", "tanınmış", "şöhrətli"], ["gizli", "xəlvəti"],
       ["şən", "şad", "şux"], ["qəzəb", "hirs", "acıq"], ["vaxt", "zaman", "çağ"], ["məqsəd", "niyyət", "məram"],
       ["fikir", "düşüncə"], ["söz", "kəlmə"], ["hekayə", "əhvalat"], ["səhv", "xəta", "yanlışlıq"], ["döyüş", "vuruşma", "müharibə"],
       ["sülh", "barış"], ["təmiz", "pak"], ["çirkli", "kirli"], ["yeni", "təzə"], ["köhnə", "əski"], ["uca", "hündür", "yüksək"],
       ["qaçmaq", "yüyürmək"], ["danışmaq", "söyləmək"], ["vəfalı", "sədaqətli"], ["xain", "satqın"], ["doğru", "düz"]]
ANT = [("böyük", "kiçik"), ("uzun", "qısa"), ("isti", "soyuq"), ("ağ", "qara"), ("gecə", "gündüz"), ("səhər", "axşam"),
       ("gəlmək", "getmək"), ("açmaq", "bağlamaq"), ("yaxşı", "pis"), ("dost", "düşmən"), ("şirin", "acı"), ("varlı", "kasıb"),
       ("yeni", "köhnə"), ("gənc", "qoca"), ("sevinc", "kədər"), ("ağır", "yüngül"), ("doğru", "yalan"), ("cəsur", "qorxaq"),
       ("çalışqan", "tənbəl"), ("səxavətli", "xəsis"), ("yuxarı", "aşağı"), ("içəri", "bayır"), ("ön", "arxa"), ("güclü", "zəif"),
       ("təmiz", "çirkli"), ("sağ", "sol"), ("qalın", "nazik"), ("dərin", "dayaz"), ("enli", "dar"), ("tez", "gec"),
       ("ucuz", "baha"), ("quru", "yaş"), ("bərk", "yumşaq"), ("alçaq", "hündür"), ("yaxın", "uzaq"), ("az", "çox"), ("ilk", "son"),
       ("giriş", "çıxış"), ("qış", "yay"), ("qalib", "məğlub"), ("sülh", "müharibə"), ("dolu", "boş"), ("qazanmaq", "itirmək"),
       ("almaq", "vermək"), ("gülmək", "ağlamaq"), ("başlamaq", "bitirmək"), ("həyat", "ölüm"), ("işıq", "qaranlıq"),
       ("xeyir", "şər"), ("kök", "arıq"), ("düz", "əyri"), ("iti", "küt"), ("şad", "qəmgin"), ("ağıllı", "ağılsız")]


def _syn_of(w):
    return {x for c in SYN if w in c for x in c}


def _ant_of(w):
    out = set()
    for a, b in ANT:
        if a == w:
            out.add(b)
        if b == w:
            out.add(a)
    return out


def _related(w):
    rel = set(_syn_of(w)) | {w}
    for x in list(rel):
        rel |= _ant_of(x)
        for y in _ant_of(x):
            rel |= _syn_of(y)
    return rel


ALL_LEX = sorted({x for c in SYN for x in c} | {x for p in ANT for x in p})


def syn_word(r, g):
    c = r.choice(SYN)
    w, s = r.sample(c, 2)
    return dict(t=f"«{w}» sözünün sinonimi hansıdır?", a=s, d=pick(r, ALL_LEX, 4, exclude=_related(w)),
                e=f"«{w}» və «{s}» mənaca yaxın sözlərdir (sinonim).", diff=M)


def ant_word(r, g):
    a, b = r.choice(ANT)
    if r.random() < 0.5:
        a, b = b, a
    return dict(t=f"«{a}» sözünün antonimi hansıdır?", a=b, d=pick(r, ALL_LEX, 4, exclude=_related(a) | _related(b)),
                e=f"«{a}» və «{b}» əks mənalı sözlərdir (antonim).", diff=M)


def syn_pair(r, g):
    c = r.choice(SYN)
    x, y = r.sample(c, 2)
    bad = [f"{a} – {b}" for a, b in r.sample(ANT, 3)]
    u, v = r.sample([w for w in ALL_LEX if w not in _related(x)], 2)
    if v in _related(u):
        return syn_pair(r, g)
    bad.append(f"{u} – {v}")
    return dict(t="Hansı cüt sinonimdir?", a=f"{x} – {y}", d=bad, e=f"«{x}» və «{y}» mənaca yaxındır; digər cütlər antonim və ya əlaqəsizdir.", diff=M)


def ant_pair(r, g):
    a, b = r.choice(ANT)
    bad = [" – ".join(r.sample(c, 2)) for c in r.sample(SYN, 3)]
    u, v = r.sample(ALL_LEX, 2)
    if v in _related(u):
        return ant_pair(r, g)
    bad.append(f"{u} – {v}")
    return dict(t="Hansı cüt antonimdir?", a=f"{a} – {b}", d=bad, e=f"«{a}» və «{b}» əks mənalıdır.", diff=M)


def syn_row(r, g):
    c = r.choice([c for c in SYN if len(c) == 3])
    good = ", ".join(c)
    bad = []
    for c2 in r.sample([x for x in SYN if len(x) >= 2 and x is not c], 4):
        a, b = c2[0], c2[1]
        intruder = r.choice(list(_ant_of(a)) or [w for w in ALL_LEX if w not in _related(a)])
        bad.append(", ".join([a, b, intruder]))
    return dict(t="Hansı sırada yalnız sinonimlər verilib?", a=good, d=bad, e=f"{good} — eyni mənaya yaxın sözlərdir. Digər sıralarda bir söz mənaca uyğun gəlmir.", diff=H)


def ant_row(r, g):
    p1, p2 = r.sample(ANT, 2)
    good = f"{p1[0]} – {p1[1]}, {p2[0]} – {p2[1]}"
    bad = []
    for _ in range(4):
        a, b = r.choice(ANT)
        c = r.choice(SYN)
        x, y = r.sample(c, 2)
        bad.append(f"{a} – {b}, {x} – {y}" if r.random() < 0.5 else f"{x} – {y}, {a} – {b}")
    return dict(t="Hansı sırada yalnız antonim cütlər verilib?", a=good, d=bad, e=f"Hər iki cüt əks mənalıdır; digər sıralarda bir cüt sinonimdir.", diff=H)


# ======================= Frazeoloji birləşmələr =======================
# (ifadə, məna, qrup) — eyni qrupdan olanlar mənaca yaxındır
IDIOMS = [("ağzı qulağına çatmaq", "çox sevinmək", 1), ("baş sındırmaq", "çox fikirləşmək", 2), ("göz qoymaq", "izləmək, nəzarət etmək", 3),
          ("göz-qulaq olmaq", "diqqətlə nəzarət etmək", 3), ("əl çəkmək", "imtina etmək", 4), ("ağzına su almaq", "susmaq", 5),
          ("dilə tutmaq", "şirin sözlə razı salmaq", 6), ("gözdən düşmək", "hörmətini itirmək", 7), ("gözündən düşmək", "hörmətini, sevgisini itirmək", 7),
          ("qulaqardına vurmaq", "eşitməzliyə vurmaq", 8), ("ürəyi yanmaq", "kiməsə acımaq", 9), ("ürəyi ağzına gəlmək", "çox qorxmaq", 10),
          ("əlini-ayağını itirmək", "çaşıb qalmaq", 11), ("başını itirmək", "özünü itirmək, çaşmaq", 11), ("burnunu soxmaq", "başqasının işinə qarışmaq", 12),
          ("gözü su içməmək", "inanmamaq", 13), ("ürəyinə dammaq", "əvvəlcədən hiss etmək", 14), ("əl-ələ vermək", "birləşib birgə çalışmaq", 15),
          ("göz yummaq", "görməzlikdən gəlmək", 16), ("ağzından qaçırmaq", "sirri bilmədən demək", 17), ("gözünün odunu almaq", "bərk qorxutmaq", 18),
          ("əli açıq", "səxavətli", 19), ("əli əyri", "oğru", 20), ("gözü tox", "tamahsız", 21), ("gözü ac", "tamahkar", 22),
          ("ürək-dirək vermək", "ruhlandırmaq", 23), ("ürəyi sıxılmaq", "darıxmaq", 24), ("göz dikmək", "tamah salmaq", 25),
          ("gözü yolda qalmaq", "intizarla gözləmək", 26), ("yerə soxmaq", "çox utandırmaq", 27), ("yerlə yeksan etmək", "tamamilə dağıtmaq", 28),
          ("cana gəlmək", "təngə gəlmək, bezmək", 29), ("canını dişinə tutmaq", "dözmək, səbr etmək", 30), ("dişini dişinə sıxmaq", "dözmək", 30),
          ("ayaqdan düşmək", "çox yorulmaq", 31), ("əldən düşmək", "taqətdən düşmək, çox yorulmaq", 31), ("boynuna almaq", "etiraf etmək", 32),
          ("boyun qaçırmaq", "yayınmaq", 33), ("ağzı açıla qalmaq", "heyrətlənmək", 34), ("kefi kök olmaq", "əhvalı yaxşı olmaq", 35),
          ("qanı qaralmaq", "kefi pozulmaq", 36), ("dili topuq vurmaq", "çaşıb düzgün danışa bilməmək", 37), ("sözü keçmək", "nüfuzu olmaq", 38),
          ("sözündən dönmək", "vədinə əməl etməmək", 39), ("söz vermək", "vəd etmək", 40), ("qol çəkmək", "imzalamaq", 41),
          ("ayağını yorğanına görə uzatmaq", "imkanına uyğun hərəkət etmək", 42), ("iki ayağını bir başmağa dirəmək", "inad etmək", 43),
          ("qulaq asmaq", "dinləmək", 44), ("göz yaşı tökmək", "ağlamaq", 45), ("dil açmaq", "danışmağa başlamaq", 46),
          ("dilə gəlmək", "danışmağa başlamaq", 46), ("əlindən gəlmək", "bacarmaq", 47), ("ağ yalan", "açıq-aşkar yalan", 48),
          ("başa salmaq", "izah etmək", 49), ("başa düşmək", "anlamaq", 50), ("üz döndərmək", "əlaqəni kəsmək", 51),
          ("ürəyindən keçmək", "arzulamaq, fikirləşmək", 52), ("nəfəsini dərmək", "dincəlmək", 53), ("başı qarışmaq", "məşğul olmaq", 54),
          ("ayaq açmaq", "yeriməyə başlamaq", 55), ("əlini üzmək", "ümidini kəsmək", 56), ("ağzının dadını bilmək", "zövqlü olmaq", 57),
          ("ürək qızdırmaq", "isinişmək, bağlanmaq", 58), ("baş əymək", "hörmətlə tabe olmaq", 59), ("gözü qızmaq", "hirslənmək", 60),
          ("ayağı yer tutmaq", "yerləşmək, möhkəmlənmək", 61), ("boğazdan yuxarı danışmaq", "səmimiyyətsiz danışmaq", 62)]
FREE = ["yeni kitab", "isti çay", "uzun yol", "qırmızı alma", "böyük ev", "məktub yazmaq", "çay içmək", "dərs oxumaq",
        "qapını açmaq", "pəncərəni bağlamaq", "çörək almaq", "parka getmək", "maraqlı film", "soyuq su", "yaşıl yarpaq"]
IDIOM_SENT = [("Bu xəbəri eşidəndə onun ağzı qulağına çatdı.", "ağzı qulağına çatmaq"),
              ("Müəllim tapşırığı yenidən başa saldı.", "başa salmaq"),
              ("Məsələnin həlli üzərində saatlarla baş sındırdıq.", "baş sındırmaq"),
              ("Anası onun ad gününü gözü yolda gözləyirdi.", "gözü yolda qalmaq"),
              ("Uşaq səhvini boynuna aldı.", "boynuna almaq"),
              ("Bütün gün işlədiyi üçün axşam ayaqdan düşmüşdü.", "ayaqdan düşmək"),
              ("Müsabiqəni uduzanda onun qanı qaraldı.", "qanı qaralmaq"),
              ("Kənd sakinləri əl-ələ verib körpünü təmir etdilər.", "əl-ələ vermək"),
              ("O, verdiyi sözdən heç vaxt dönməz.", "sözündən dönmək"),
              ("Direktor sənədə qol çəkdi.", "qol çəkmək"),
              ("Qəfil səsdən hamının ürəyi ağzına gəldi.", "ürəyi ağzına gəlmək"),
              ("Uşaq bir yaşında ayaq açdı.", "ayaq açmaq"),
              ("Xəbəri eşidib ağzı açıla qaldı.", "ağzı açıla qalmaq"),
              ("Mən sənin sözlərinə qulaq asıram.", "qulaq asmaq"),
              ("O, sirri təsadüfən ağzından qaçırdı.", "ağzından qaçırmaq"),
              ("Babam bizə həmişə ürək-dirək verirdi.", "ürək-dirək vermək"),
              ("Qardaşım hər işə burnunu soxur.", "burnunu soxmaq"),
              ("İmtahan vaxtı əlimi-ayağımı itirdim.", "əlini-ayağını itirmək")]
LITERAL = ["Uşaq qapını açıb həyətə çıxdı.", "Anam bazardan təzə meyvə aldı.", "Biz axşam parkda gəzdik.",
           "Qardaşım hər səhər idmanla məşğul olur.", "Müəllim lövhəyə yeni mövzunu yazdı.", "Pişik pəncərənin qarşısında yatmışdı.",
           "Atam maşını qarajın qarşısında saxladı.", "Bağda gözəl güllər açmışdı.", "Şagirdlər sinfə daxil oldular.",
           "Nənəm bizə dadlı plov bişirdi.", "Qatar vağzala vaxtında çatdı.", "Dənizdə böyük gəmi görünürdü.",
           "Qız əlini suya saldı.", "Oğlan başını qaldırıb səmaya baxdı.", "O, ayağını yerə qoyub dayandı."]


def idiom_meaning(r, g):
    i, m_, grp = r.choice(IDIOMS)
    bad = pick(r, [x[1] for x in IDIOMS if x[2] != grp], 4)
    return dict(t=f"«{i}» frazeoloji birləşməsinin mənası nədir?", a=m_, d=bad, e=f"«{i}» — {m_}.", diff=M)


def idiom_find(r, g):
    i, m_, grp = r.choice(IDIOMS)
    bad = pick(r, [x[0] for x in IDIOMS if x[2] != grp], 4)
    return dict(t=f"Hansı frazeoloji birləşmə «{m_}» mənasını bildirir?", a=i, d=bad, e=f"«{i}» — {m_}.", diff=M)


def idiom_not(r, g):
    f = r.choice(FREE)
    return dict(t="Hansı birləşmə frazeoloji birləşmə deyil?", a=f, d=pick(r, [x[0] for x in IDIOMS], 4),
                e=f"«{f}» sərbəst söz birləşməsidir: sözlər həqiqi mənasında işlənib.", diff=M)


def idiom_close(r, g):
    groups = {}
    for i, m_, grp in IDIOMS:
        groups.setdefault(grp, []).append(i)
    pairs = [v for v in groups.values() if len(v) >= 2]
    a, b = r.sample(r.choice(pairs), 2)
    bad = []
    while len(bad) < 4:
        x, y = r.sample(IDIOMS, 2)
        if x[2] != y[2]:
            bad.append(f"{x[0]} – {y[0]}")
    return dict(t="Hansı frazeoloji birləşmələr mənaca yaxındır?", a=f"{a} – {b}", d=bad,
                e=f"Hər ikisi eyni mənanı bildirir: {dict((x[0], x[1]) for x in IDIOMS)[a]}.", diff=H)


def idiom_sentence(r, g):
    s, i = r.choice(IDIOM_SENT)
    return dict(t="Hansı cümlədə frazeoloji birləşmə işlənib?", a=s, d=pick(r, LITERAL, 4),
                e=f"Cümlədə «{i}» frazeologizmi işlənib; digər cümlələrdə sözlər həqiqi mənadadır.", diff=H)


def idiom_in_sentence(r, g):
    s, i = r.choice(IDIOM_SENT)
    m_ = next(x[1] for x in IDIOMS if x[0] == i)
    grp = next(x[2] for x in IDIOMS if x[0] == i)
    return dict(t=f"«{s}» cümləsindəki frazeoloji birləşmənin mənası hansıdır?", a=m_, d=pick(r, [x[1] for x in IDIOMS if x[2] != grp], 4),
                e=f"«{i}» — {m_}.", diff=H)


# ======================= İsim və sifət =======================
NOUNS = ["kitab", "məktəb", "dəniz", "şəhər", "qapı", "bağ", "ev", "çiçək", "qonaq", "göl", "meşə", "dağ", "otaq", "bazar",
         "stadion", "muzey", "kənd", "kitabxana", "universitet", "küçə", "park", "dəftər", "qələm", "pəncərə", "bulud"]
CASES = ["adlıq", "yiyəlik", "yönlük", "təsirlik", "yerlik", "çıxışlıq"]
CASE_FRAME = {
    "yönlük": "Biz {w} getdik.",
    "yerlik": "Uşaqlar {w} idilər.",
    "çıxışlıq": "O, {w} qayıtdı.",
    "təsirlik": "Mən {w} gördüm.",
}


def noun_case(r, g):
    c = r.choice(["yönlük", "yerlik", "çıxışlıq", "təsirlik", "yiyəlik"])
    n = r.choice(NOUNS)
    w = case(n, c)
    if c == "yiyəlik":
        owner = r.choice([("qapısı", "qapı"), ("rəngi", "rəng"), ("adı", "ad"), ("divarı", "divar"), ("havası", "hava")])
        phrase = f"{w} {owner[0]}"
        return dict(t=f"«{phrase}» birləşməsində «{w}» sözü hansı haldadır?", a=c, d=[x for x in CASES if x != c][:5],
                    e=f"«{w}» — kimin? nəyin? sualına cavab verir, -{w[len(n):]} yiyəlik hal şəkilçisidir.", diff=M)
    sent = CASE_FRAME[c].format(w=w)
    q = {"yönlük": "hara? kimə? nəyə?", "yerlik": "harada? kimdə? nədə?", "çıxışlıq": "haradan? kimdən? nədən?", "təsirlik": "kimi? nəyi? haranı?"}[c]
    return dict(t=f"«{sent}» cümləsində «{w}» sözü hansı haldadır?", a=c, d=[x for x in CASES if x != c],
                e=f"«{w}» {q} sualına cavab verir — {c} hal.", diff=M)


PERSONS = ["I şəxs tək", "II şəxs tək", "III şəxs tək", "I şəxs cəm", "II şəxs cəm", "III şəxs cəm"]


def noun_possessive(r, g):
    n = r.choice([x for x in NOUNS if not x.endswith("a") or x == "kitabxana"])
    p = r.choice(["I şəxs tək", "I şəxs cəm", "II şəxs cəm"])
    w = possessive(n, p)
    return dict(t=f"«{w}» sözündəki mənsubiyyət şəkilçisi hansı şəxsi bildirir?", a=p, d=[x for x in PERSONS if x != p],
                e=f"{n} + {w[len(soften(n)) if not ends_vowel(n) else len(n):]} — {p}: {'mənim' if p == 'I şəxs tək' else 'bizim' if p == 'I şəxs cəm' else 'sizin'} {n}.", diff=M)


ABSTRACT = ["sevgi", "ümid", "cəsarət", "ədalət", "sevinc", "qorxu", "dostluq", "fikir", "arzu", "həyat", "zəka", "vicdan", "azadlıq", "kədər", "səbr"]
CONCRETE = ["masa", "daş", "ağac", "qələm", "kitab", "ev", "qapı", "maşın", "dəftər", "alma", "pəncərə", "divar", "çanta", "stul", "lampa"]
COLLECTIVE = ["xalq", "ordu", "sürü", "qoşun", "camaat", "dəstə", "komanda", "izdiham", "heyət", "ailə"]
DERIVED_NOUN = ["dəmirçi", "balıqçı", "gözəllik", "yazıçı", "çörəkçi", "dostluq", "ovçu", "bilik", "əkin", "qələmdan", "oyunçu", "gülüş", "qaçış", "döyüş", "duzluq"]
SIMPLE_NOUN = ["ev", "daş", "dağ", "su", "göz", "kitab", "qələm", "ağac", "at", "quş", "yol", "qapı", "divar", "kənd", "gül"]
COMPOUND_NOUN = ["ayaqqabı", "qayınata", "dəvəquşu", "qızılgül", "günəbaxan", "ağsaqqal", "yerkökü", "ağcaqanad"]


def noun_kind(r, g):
    k = r.choice(["abstract", "collective", "derived", "compound"])
    if k == "abstract":
        return dict(t="Hansı isim mücərrəd isimdir?", a=r.choice(ABSTRACT), d=pick(r, CONCRETE, 4),
                    e="Mücərrəd isimlər hiss üzvləri ilə qavranılmayan anlayışları bildirir.", diff=M)
    if k == "collective":
        return dict(t="Hansı isim topluluq bildirir?", a=r.choice(COLLECTIVE), d=pick(r, CONCRETE + SIMPLE_NOUN, 4),
                    e="Topluluq bildirən isimlər təkdə olsa da çoxluq anlayışı ifadə edir.", diff=M)
    if k == "derived":
        return dict(t="Hansı isim düzəltmədir?", a=r.choice(DERIVED_NOUN), d=pick(r, SIMPLE_NOUN + COMPOUND_NOUN, 4),
                    e="Düzəltmə isim kök + sözdüzəldici şəkilçidən ibarətdir (-çı, -lıq, -ış, -ik və s.).", diff=H)
    return dict(t="Hansı isim mürəkkəbdir?", a=r.choice(COMPOUND_NOUN), d=pick(r, SIMPLE_NOUN + DERIVED_NOUN, 4),
                e="Mürəkkəb isim iki və daha çox kökdən ibarətdir.", diff=H)


ADJ_SIMPLE = ["ağ", "qara", "gözəl", "uzun", "böyük", "yaxşı", "şirin", "isti", "yaşıl", "qırmızı", "sarı", "kiçik", "təmiz"]
ADJ_DERIVED = ["dadlı", "ağıllı", "duzlu", "gülməli", "ürəkli", "savadlı", "işıqlı", "dözümlü", "qorxulu", "maraqlı", "evsiz", "susuz", "dağlıq"]
ADJ_COMPOUND = ["açıqgöz", "qaragöz", "istiqanlı", "əliaçıq", "ikimərtəbəli", "beşillik", "uzunboylu", "qarasaçlı", "enlikürək"]
DEGREES = {"çoxaltma dərəcəsi": ["ağappaq", "qapqara", "yamyaşıl", "göm-göy", "sapsarı", "qıpqırmızı", "dümdüz", "tərtəmiz", "bomboş", "yupyumru"],
           "azaltma dərəcəsi": ["ağımtıl", "qaramtıl", "göyümtül", "sarımtıl", "yaşılımtıl", "qırmızımtıl", "uzunsov", "turşməzə"],
           "adi dərəcə": ["ağ", "qara", "göy", "sarı", "yaşıl", "qırmızı", "uzun", "boş"],
           "üstünlük dərəcəsi": ["ən gözəl", "ən böyük", "ən uzun", "ən yaxşı", "ən çətin", "ən hündür"]}


def adj_kind(r, g):
    k = r.choice(["derived", "compound", "simple"])
    if k == "derived":
        return dict(t="Hansı sifət düzəltmədir?", a=r.choice(ADJ_DERIVED), d=pick(r, ADJ_SIMPLE + ADJ_COMPOUND, 4),
                    e="Düzəltmə sifət kök + sözdüzəldici şəkilçidən ibarətdir (-lı, -lu, -sız, -malı və s.).", diff=M)
    if k == "compound":
        return dict(t="Hansı sifət mürəkkəbdir?", a=r.choice(ADJ_COMPOUND), d=pick(r, ADJ_SIMPLE + ADJ_DERIVED, 4),
                    e="Mürəkkəb sifət iki kökdən yaranır.", diff=H)
    return dict(t="Hansı sifət sadədir?", a=r.choice(ADJ_SIMPLE), d=pick(r, ADJ_DERIVED + ADJ_COMPOUND, 4),
                e="Sadə sifət yalnız kökdən ibarətdir.", diff=M)


def adj_degree(r, g):
    d_ = r.choice(list(DEGREES))
    w = r.choice(DEGREES[d_])
    if r.random() < 0.5:
        others = [x for k, v in DEGREES.items() if k != d_ for x in v]
        return dict(t=f"Hansı sifət {d_}ndədir?".replace("dərəcəsindədir", "dərəcəsindədir").replace("adi dərəcəndədir", "adi dərəcədədir"),
                    a=w, d=pick(r, others, 4), e=f"«{w}» — {d_}.", diff=M)
    return dict(t=f"«{w}» sifəti hansı dərəcədədir?", a=d_, d=[x for x in DEGREES if x != d_] + ["isimləşmiş sifət"],
                e=f"«{w}» — {d_}.", diff=M)


SUBST = ["Yaxşılar həmişə xatırlanır.", "Böyüklərə hörmət et.", "Gənclər meydana toplaşdı.", "Qocalar bağda oturmuşdu.",
         "Ağıllılar səbirli olur.", "Tənbəllər uğur qazanmır.", "Cəsurlar qorxmur.", "Xəstələrə qayğı göstərin."]
ATTR = ["Yaxşı insan həmişə xatırlanır.", "Böyük qardaşıma hörmət edirəm.", "Gənc müəllim dərsə başladı.", "Qoca kişi bağda oturmuşdu.",
        "Ağıllı uşaq sualı tez cavablandırdı.", "Tənbəl pişik bütün gün yatdı.", "Cəsur əsgər irəli atıldı.", "Xəstə uşaq evdə qaldı."]


def adj_subst(r, g):
    s = r.choice(SUBST)
    return dict(t="Hansı cümlədə sifət isimləşib?", a=s, d=pick(r, ATTR, 4),
                e="İsimləşmiş sifət isim kimi işlənir və isim şəkilçiləri qəbul edir (yaxşılar, böyüklərə).", diff=H)


# ======================= Feil və təsriflənməyən formalar =======================
VERBS = [("yaz", None, True), ("oxu", None, True), ("al", None, True), ("ver", None, True), ("aç", None, True), ("tik", None, True),
         ("sev", None, True), ("tap", None, True), ("sat", None, True), ("sil", None, True), ("qoru", None, True), ("öyrən", None, True),
         ("yığ", None, True), ("qur", None, True), ("gör", None, True), ("bil", None, True),
         ("gəl", None, False), ("get", "ged", False), ("qaç", None, False), ("dur", None, False), ("gül", None, False), ("yat", None, False),
         ("uç", None, False), ("qalx", None, False), ("düş", None, False), ("otur", None, False), ("yaşa", None, False), ("çalış", None, False),
         ("gəz", None, False), ("ağla", None, False), ("qorx", None, False), ("sevin", None, False)]
SIFAT = ["feili sifət -an", "feili sifət -mış", "feili sifət -acaq", "feili sifət -dığı"]
BAGLAMA = ["feili bağlama -araq", "feili bağlama -ıb", "feili bağlama -anda", "feili bağlama -madan", "feili bağlama -dıqca", "feili bağlama -ınca"]
TENSES = ["şühudi keçmiş zaman", "nəqli keçmiş zaman", "indiki zaman", "qəti gələcək zaman", "qeyri-qəti gələcək zaman"]
MOODS = ["əmr şəkli", "şərt şəkli", "arzu şəkli", "lazım şəkli"]


def _v(r):
    return r.choice(VERBS)


def _other_forms(r, exclude_kind, n=4):
    out = set()
    while len(out) < n:
        s, vs, _ = _v(r)
        k = r.choice(["məsdər", "tense", "mood"] + [x for x in (["sifat"] if exclude_kind != "sifat" else [])] + (["baglama"] if exclude_kind != "baglama" else []))
        if k == "məsdər" and exclude_kind != "məsdər":
            out.add(form(s, "məsdər", vs))
        elif k == "tense":
            out.add(tense_1sg(s, r.choice(TENSES), vs))
        elif k == "mood":
            out.add(mood(s, r.choice(MOODS), vs))
        elif k == "sifat":
            out.add(form(s, r.choice(SIFAT), vs))
        elif k == "baglama":
            out.add(form(s, r.choice(BAGLAMA), vs))
    return list(out)


def verb_baglama(r, g):
    s, vs, _ = _v(r)
    kind = r.choice(BAGLAMA)
    w = form(s, kind, vs)
    return dict(t="Hansı söz feili bağlamadır?", a=w, d=_other_forms(r, "baglama"),
                e=f"«{w}» — {kind.split()[-1]} şəkilçili feili bağlama: işin tərzini, zamanını və ya səbəbini bildirir.", diff=M)


def verb_sifat(r, g):
    s, vs, _ = _v(r)
    kind = r.choice(SIFAT)
    w = form(s, kind, vs)
    return dict(t="Hansı söz feili sifətdir?", a=w, d=_other_forms(r, "sifat"),
                e=f"«{w}» — {kind.split()[-1]} şəkilçili feili sifət: əşyanın əlamətini hərəkətə görə bildirir.", diff=M)


def verb_kind(r, g):
    s, vs, _ = _v(r)
    k = r.choice(["məsdər", "feili sifət", "feili bağlama"])
    if k == "məsdər":
        w = form(s, "məsdər", vs)
    elif k == "feili sifət":
        w = form(s, r.choice(SIFAT), vs)
    else:
        w = form(s, r.choice(BAGLAMA), vs)
    return dict(t=f"«{w}» sözü feilin hansı formasıdır?", a=k, d=[x for x in ["məsdər", "feili sifət", "feili bağlama", "təsriflənən feil (zaman forması)", "isim"] if x != k],
                e=f"«{w}» — {k}.", diff=M)


def verb_tense(r, g):
    s, vs, _ = _v(r)
    t = r.choice(TENSES)
    w = tense_1sg(s, t, vs)
    return dict(t=f"«{w}» feili hansı zamandadır?", a=t, d=[x for x in TENSES if x != t] + ["arzu şəkli"],
                e=f"«{w}» — {t} (I şəxs tək).", diff=M)


def verb_mood(r, g):
    s, vs, _ = _v(r)
    m_ = r.choice(MOODS)
    w = mood(s, m_, vs)
    return dict(t=f"«{w}» feili hansı şəkildədir?", a=m_, d=[x for x in MOODS if x != m_] + ["xəbər şəkli", "vacib şəkli"],
                e=f"«{w}» — {m_}.", diff=H)


def verb_voice(r, g):
    kind = r.choice(["məchul", "qarşılıq-birgəlik", "icbar", "qayıdış"])
    trans = [v for v in VERBS if v[2]]
    passive = [passive_past(s, vs) for s, vs, _ in trans]
    pools = {"məchul": passive, "qarşılıq-birgəlik": RECIPROCAL, "icbar": CAUSATIVE, "qayıdış": REFLEXIVE}
    w = r.choice(pools[kind])
    others = [x for k, v in pools.items() if k != kind for x in v]
    return dict(t=f"Hansı feil {kind} növündədir?", a=w, d=pick(r, others, 4),
                e={"məchul": f"«{w}» — məchul növ (-ıl/-ın/-n): işi görən göstərilmir.",
                   "qarşılıq-birgəlik": f"«{w}» — qarşılıq-birgəlik növ (-ış): iş birgə və ya qarşılıqlı görülür.",
                   "icbar": f"«{w}» — icbar növ (-dır/-t): iş başqasına gördürülür.",
                   "qayıdış": f"«{w}» — qayıdış növ: iş subyektin özünə qayıdır."}[kind], diff=H)


def verb_trans(r, g):
    want = r.choice([True, False])
    good = [s for s, vs, t in VERBS if t == want]
    bad = [s for s, vs, t in VERBS if t != want]
    s = r.choice(good)
    vs = dict((v[0], v[1]) for v in VERBS)
    return dict(t=f"Hansı feil {'təsirlidir' if want else 'təsirsizdir'}?", a=form(s, "məsdər", vs[s]),
                d=[form(x, "məsdər", vs[x]) for x in pick(r, bad, 4)],
                e="Təsirli feillər kimi? nəyi? sualına cavab verən obyekt tələb edir; təsirsiz feillər tələb etmir.", diff=M)


def verb_negative(r, g):
    s, vs, _ = _v(r)
    good = negative_past(s)
    traps = [form(s, "məsdər", vs), mood(s, "lazım şəkli", vs), tense_1sg(s, "şühudi keçmiş zaman", vs), form(s, "feili sifət -mış", vs)]
    return dict(t="Hansı feil inkar formasındadır?", a=good, d=traps,
                e=f"«{good}» sözündə -ma/-mə inkar şəkilçisidir. «{form(s, 'məsdər', vs)}» və «{mood(s, 'lazım şəkli', vs)}» sözlərindəki «ma/mə» isə başqa şəkilçinin hissəsidir.",
                diff=H)


# ======================= Cümlənin üzvləri =======================
MUB, XEB, VZT, VLT, TEY = "mübtəda", "xəbər", "vasitəsiz tamamlıq", "vasitəli tamamlıq", "təyin"
ZZ, YZ, TZ, SZ, MZ, KZ = "zaman zərfliyi", "yer zərfliyi", "tərzi-hərəkət zərfliyi", "səbəb zərfliyi", "məqsəd zərfliyi", "kəmiyyət zərfliyi"
MEMBERS = [MUB, XEB, VZT, VLT, TEY, ZZ, YZ, TZ, SZ, MZ, KZ]
SENTS = [
    ("Uşaqlar səhər tezdən parka getdilər.", [("uşaqlar", MUB), ("səhər tezdən", ZZ), ("parka", YZ), ("getdilər", XEB)]),
    ("Ana qızına gözəl bir paltar tikdi.", [("ana", MUB), ("qızına", VLT), ("gözəl", TEY), ("paltar", VZT), ("tikdi", XEB)]),
    ("Müəllim yeni mövzunu şagirdlərə aydın izah etdi.", [("müəllim", MUB), ("yeni", TEY), ("mövzunu", VZT), ("şagirdlərə", VLT), ("aydın", TZ), ("izah etdi", XEB)]),
    ("Qardaşım kitabxanadan maraqlı bir roman gətirdi.", [("qardaşım", MUB), ("kitabxanadan", YZ), ("maraqlı", TEY), ("roman", VZT), ("gətirdi", XEB)]),
    ("Güclü küləkdən ağaclar yerə əyilirdi.", [("güclü", TEY), ("küləkdən", SZ), ("ağaclar", MUB), ("yerə", YZ), ("əyilirdi", XEB)]),
    ("Biz bu filmə iki dəfə baxmışıq.", [("biz", MUB), ("bu", TEY), ("filmə", VLT), ("iki dəfə", KZ), ("baxmışıq", XEB)]),
    ("Nənəm hər axşam bizə nağıl danışırdı.", [("nənəm", MUB), ("hər axşam", ZZ), ("bizə", VLT), ("nağıl", VZT), ("danışırdı", XEB)]),
    ("Tələbələr imtahana hazırlaşmaq üçün kitabxanada qaldılar.", [("tələbələr", MUB), ("imtahana hazırlaşmaq üçün", MZ), ("kitabxanada", YZ), ("qaldılar", XEB)]),
    ("Yağışdan sonra hava sərinləşdi.", [("yağışdan sonra", ZZ), ("hava", MUB), ("sərinləşdi", XEB)]),
    ("Atam bu gün işdən gec qayıtdı.", [("atam", MUB), ("bu gün", ZZ), ("işdən", YZ), ("gec", ZZ), ("qayıtdı", XEB)]),
    ("Bağban bağdakı ağacları diqqətlə budayırdı.", [("bağban", MUB), ("bağdakı", TEY), ("ağacları", VZT), ("diqqətlə", TZ), ("budayırdı", XEB)]),
    ("Kənddə yeni məktəb tikildi.", [("kənddə", YZ), ("yeni", TEY), ("məktəb", MUB), ("tikildi", XEB)]),
    ("Mən dostumdan bir neçə kitab aldım.", [("mən", MUB), ("dostumdan", VLT), ("bir neçə", TEY), ("kitab", VZT), ("aldım", XEB)]),
    ("Şagirdlər müəllimin sualına cavab verdilər.", [("şagirdlər", MUB), ("müəllimin", TEY), ("sualına", VLT), ("cavab verdilər", XEB)]),
    ("Gecə yarısı güclü yağış başladı.", [("gecə yarısı", ZZ), ("güclü", TEY), ("yağış", MUB), ("başladı", XEB)]),
    ("O, sevincindən ağladı.", [("o", MUB), ("sevincindən", SZ), ("ağladı", XEB)]),
    ("Turistlər qədim qalaya maraqla baxırdılar.", [("turistlər", MUB), ("qədim", TEY), ("qalaya", VLT), ("maraqla", TZ), ("baxırdılar", XEB)]),
    ("Dənizdən sərin bir meh əsdi.", [("dənizdən", YZ), ("sərin", TEY), ("meh", MUB), ("əsdi", XEB)]),
    ("Bacım məktəbdə ingilis dilini öyrənir.", [("bacım", MUB), ("məktəbdə", YZ), ("ingilis dilini", VZT), ("öyrənir", XEB)]),
    ("Biz yayda üç dəfə dənizə getdik.", [("biz", MUB), ("yayda", ZZ), ("üç dəfə", KZ), ("dənizə", YZ), ("getdik", XEB)]),
    ("Yorğunluqdan onun gözləri yumulurdu.", [("yorğunluqdan", SZ), ("onun", TEY), ("gözləri", MUB), ("yumulurdu", XEB)]),
    ("Rəssam gözəl bir mənzərə çəkdi.", [("rəssam", MUB), ("gözəl", TEY), ("mənzərə", VZT), ("çəkdi", XEB)]),
    ("Uşaq qorxa-qorxa qapını açdı.", [("uşaq", MUB), ("qorxa-qorxa", TZ), ("qapını", VZT), ("açdı", XEB)]),
    ("Dostlarım məni ad günümdə təbrik etdilər.", [("dostlarım", MUB), ("məni", VZT), ("ad günümdə", ZZ), ("təbrik etdilər", XEB)]),
    ("Oxumaq insanın dünyagörüşünü genişləndirir.", [("oxumaq", MUB), ("insanın", TEY), ("dünyagörüşünü", VZT), ("genişləndirir", XEB)]),
    ("Ağıllılar həmişə düşünərək danışır.", [("ağıllılar", MUB), ("həmişə", ZZ), ("düşünərək", TZ), ("danışır", XEB)]),
    ("Səhər-səhər quşların səsi eşidilirdi.", [("səhər-səhər", ZZ), ("quşların", TEY), ("səsi", MUB), ("eşidilirdi", XEB)]),
    ("Atam mənə yeni velosiped aldı.", [("atam", MUB), ("mənə", VLT), ("yeni", TEY), ("velosiped", VZT), ("aldı", XEB)]),
    ("Zəng çalınan kimi şagirdlər həyətə çıxdılar.", [("zəng çalınan kimi", ZZ), ("şagirdlər", MUB), ("həyətə", YZ), ("çıxdılar", XEB)]),
    ("Qızım rəqs dərnəyinə həftədə iki dəfə gedir.", [("qızım", MUB), ("rəqs dərnəyinə", YZ), ("həftədə iki dəfə", KZ), ("gedir", XEB)]),
    ("Həkim xəstəni diqqətlə müayinə etdi.", [("həkim", MUB), ("xəstəni", VZT), ("diqqətlə", TZ), ("müayinə etdi", XEB)]),
    ("Soyuqdan əllərim donmuşdu.", [("soyuqdan", SZ), ("əllərim", MUB), ("donmuşdu", XEB)]),
    ("Mən sənə bir sirr deyəcəyəm.", [("mən", MUB), ("sənə", VLT), ("sirr", VZT), ("deyəcəyəm", XEB)]),
    ("Pəncərədən gözəl bir mənzərə görünürdü.", [("pəncərədən", YZ), ("gözəl", TEY), ("mənzərə", MUB), ("görünürdü", XEB)]),
    ("Biz istirahət etmək üçün dağlara getdik.", [("biz", MUB), ("istirahət etmək üçün", MZ), ("dağlara", YZ), ("getdik", XEB)]),
    ("Qardaşım səhv etdiyinə görə üzr istədi.", [("qardaşım", MUB), ("səhv etdiyinə görə", SZ), ("üzr istədi", XEB)]),
    ("Nənəm bizim üçün dadlı mürəbbə bişirdi.", [("nənəm", MUB), ("bizim üçün", VLT), ("dadlı", TEY), ("mürəbbə", VZT), ("bişirdi", XEB)]),
    ("Səbinə məktubu diqqətlə oxudu.", [("Səbinə", MUB), ("məktubu", VZT), ("diqqətlə", TZ), ("oxudu", XEB)]),
    ("Şəhərimizdə bu il üç yeni park salındı.", [("şəhərimizdə", YZ), ("bu il", ZZ), ("üç", TEY), ("yeni", TEY), ("park", MUB), ("salındı", XEB)]),
    ("Yolçular yorğunluqdan ağacın kölgəsində dincəldilər.", [("yolçular", MUB), ("yorğunluqdan", SZ), ("ağacın", TEY), ("kölgəsində", YZ), ("dincəldilər", XEB)]),
]


def mem_which(r, g):
    s, parts = r.choice(SENTS)
    ph, m_ = r.choice(parts)
    return dict(t=f"«{s}» cümləsində «{ph}» hansı cümlə üzvüdür?", a=m_, d=pick(r, MEMBERS, 4, exclude={m_}),
                e=f"«{ph}» — {m_}.", diff=M if m_ in (MUB, XEB, TEY) else H)


def mem_find(r, g):
    s, parts = r.choice([x for x in SENTS if len(x[1]) >= 5])
    labels = [m_ for _, m_ in parts]
    uniq = [m_ for m_ in labels if labels.count(m_) == 1]
    m_ = r.choice(uniq)
    ph = next(p for p, l in parts if l == m_)
    return dict(t=f"«{s}» cümləsində {m_} hansıdır?", a=ph, d=[p for p, l in parts if l != m_][:4],
                e=f"{m_[0].upper() + m_[1:]} — «{ph}».", diff=M if m_ in (MUB, XEB) else H)


def mem_has(r, g):
    m_ = r.choice([SZ, MZ, KZ, VLT, TZ, ZZ])
    good = [s for s, p in SENTS if any(l == m_ for _, l in p)]
    bad = [s for s, p in SENTS if all(l != m_ for _, l in p)]
    s = r.choice(good)
    ph = next(p for p, l in dict(SENTS)[s] if l == m_)
    return dict(t=f"Hansı cümlədə {m_} var?", a=s, d=pick(r, bad, 4), e=f"Cümlədə «{ph}» {m_}dir.".replace(f"{m_}dir", f"{m_}dir"), diff=H)


def mem_count(r, g):
    s, parts = r.choice(SENTS)
    m_ = r.choice([TEY, VZT, VLT])
    n = sum(1 for _, l in parts if l == m_)
    return dict(t=f"«{s}» cümləsində neçə {m_} var?", a=n, d=[x for x in [0, 1, 2, 3, 4] if x != n],
                e=f"{m_[0].upper() + m_[1:]}: {', '.join(p for p, l in parts if l == m_) or 'yoxdur'}.", diff=H)


# ======================= Mürəkkəb cümlələr =======================
TABELI = [("Kim çalışsa, o qazanar.", "mübtəda", "əvvəl"), ("Kim yaxşılıq edərsə, o hörmət qazanar.", "mübtəda", "əvvəl"),
          ("Hər kəs bilir ki, zəhmət insanı ucaldır.", "tamamlıq", "sonra"), ("Mən bilirəm ki, sən imtahandan uğurla keçəcəksən.", "tamamlıq", "sonra"),
          ("Müəllim dedi ki, sabah ekskursiyaya gedəcəyik.", "tamamlıq", "sonra"), ("Kim çox oxuyarsa, ona hamı hörmət edər.", "tamamlıq", "əvvəl"),
          ("Arzum budur ki, həkim olum.", "xəbər", "sonra"), ("Məqsədimiz budur ki, hamı savadlı olsun.", "xəbər", "sonra"),
          ("Elə bir kitab oxudum ki, onu heç vaxt unutmaram.", "təyin", "sonra"), ("Elə bir yerə gəldik ki, orada heç kim yaşamırdı.", "təyin", "sonra"),
          ("Nə vaxt ki bahar gəldi, ağaclar çiçəklədi.", "zaman", "əvvəl"), ("Nə zaman ki zəng çalındı, şagirdlər sinfə qayıtdılar.", "zaman", "əvvəl"),
          ("Harada ki birlik var, orada qələbə var.", "yer", "əvvəl"), ("Hara getsən, orada dost tapacaqsan.", "yer", "əvvəl"),
          ("Biz evdə qaldıq, çünki bərk yağış yağırdı.", "səbəb", "sonra"), ("O, dərsə gecikdi, çünki avtobus gəlmədi.", "səbəb", "sonra"),
          ("Ona görə tez yatdım ki, səhər erkən durmalıydım.", "səbəb", "sonra"), ("Erkən durdum ki, qatara çatım.", "məqsəd", "sonra"),
          ("Kitabxanaya getdim ki, lazımi ədəbiyyatı tapım.", "məqsəd", "sonra"), ("Əgər yağış yağsa, gəzintiyə getməyəcəyik.", "şərt", "əvvəl"),
          ("Əgər vaxtım olsa, sənə zəng edərəm.", "şərt", "əvvəl"), ("Çalışsan, qazanarsan.", "şərt", "əvvəl"),
          ("Hərçənd hava soyuq idi, biz gəzintiyə çıxdıq.", "güzəşt", "əvvəl"), ("Baxmayaraq ki, yorğun idi, o, işini bitirdi.", "güzəşt", "əvvəl"),
          ("Nə qədər çalışsa da, tapşırığı həll edə bilmədi.", "güzəşt", "əvvəl")]
TABESIZ = [("Günəş batdı, hava qaraldı.", 2, False), ("Bahar gəldi, çöllər yaşıllaşdı.", 2, False),
           ("Yağış yağırdı, külək əsirdi, ağaclar yırğalanırdı.", 3, False), ("Zəng çalındı, şagirdlər həyətə qaçdı.", 2, False),
           ("Qar yağdı, yollar ağardı, uşaqlar sevindi.", 3, False), ("Yağış dayandı, amma külək hələ də əsirdi.", 2, True),
           ("Biz gəldik, lakin onlar artıq getmişdilər.", 2, True), ("Gah yağış yağır, gah da günəş çıxır.", 2, True),
           ("Nə o zəng etdi, nə də mən məktub yazdım.", 2, True), ("Ya sən gəl, ya da mən gəlim.", 2, True),
           ("Hava qaraldı və ulduzlar göründü.", 2, True), ("Həm hava isti idi, həm də dəniz sakit idi.", 2, True),
           ("Külək əsdi, yarpaqlar töküldü, budaqlar sındı, yol bağlandı.", 4, False), ("Musiqi səsləndi, hamı rəqsə başladı.", 2, False)]
SADE = ["Günəş batanda hava qaraldı.", "Dərsdən sonra kitabxanaya getdim.", "Yağış yağdığı üçün evdə qaldıq.",
        "Səhər tezdən durub yola çıxdıq.", "Zəng çalınan kimi şagirdlər həyətə çıxdılar.", "Kitabı oxuyub rəfə qoydum.",
        "Uşaqlar gülə-gülə parka qaçdılar.", "İmtahana hazırlaşmaq üçün çox oxudum.", "Qış gələndə quşlar isti ölkələrə uçur.",
        "Bahar gəldiyi üçün çöllər yaşıllaşdı."]
BUDAQ = ["mübtəda", "xəbər", "tamamlıq", "təyin", "zaman", "yer", "səbəb", "məqsəd", "şərt", "güzəşt"]


def cx_tabeli(r, g):
    s, t, _ = r.choice(TABELI)
    d = [x[0] for x in r.sample(TABESIZ, 2)] + r.sample(SADE, 2)
    return dict(t="Hansı cümlə tabeli mürəkkəb cümlədir?", a=s, d=d, e=f"Burada {t} budaq cümləsi baş cümləyə tabe olub.", diff=M)


def cx_tabesiz(r, g):
    s, n, _ = r.choice(TABESIZ)
    d = [x[0] for x in r.sample(TABELI, 2)] + r.sample(SADE, 2)
    return dict(t="Hansı cümlə tabesiz mürəkkəb cümlədir?", a=s, d=d, e=f"Cümlə {n} bərabərhüquqlu komponentdən ibarətdir.", diff=M)


def cx_sade(r, g):
    s = r.choice(SADE)
    d = [x[0] for x in r.sample(TABELI, 2)] + [x[0] for x in r.sample(TABESIZ, 2)]
    return dict(t="Hansı cümlə sadə cümlədir?", a=s, d=d,
                e="Cümlədə bir qrammatik əsas var; feili sifət və ya feili bağlama tərkibi cümləni mürəkkəb etmir.", diff=H)


def cx_type(r, g):
    s, t, _ = r.choice(TABELI)
    return dict(t=f"«{s}» cümləsində budaq cümlənin növü hansıdır?", a=f"{t} budaq cümləsi",
                d=[f"{x} budaq cümləsi" for x in pick(r, BUDAQ, 4, exclude={t})], e=f"Budaq cümlə — {t} budaq cümləsi.", diff=H)


def cx_has_type(r, g):
    s, t, _ = r.choice(TABELI)
    d = [x[0] for x in r.sample([y for y in TABELI if y[1] != t], 4)]
    return dict(t=f"Hansı cümlədə {t} budaq cümləsi var?", a=s, d=d, e=f"«{s}» — {t} budaq cümləsi.", diff=H)


def cx_count(r, g):
    s, n, _ = r.choice(TABESIZ)
    return dict(t=f"«{s}» mürəkkəb cümləsi neçə komponentdən ibarətdir?", a=n, d=[x for x in [1, 2, 3, 4, 5] if x != n],
                e=f"Cümlədə {n} qrammatik əsas var.", diff=M)


def cx_conj(r, g):
    want = r.choice([True, False])
    s, n, _ = r.choice([x for x in TABESIZ if x[2] == want])
    others = [x[0] for x in TABESIZ if x[2] != want]
    d = pick(r, others, 3) + [r.choice(TABELI)[0]]
    return dict(t=f"Hansı cümlə {'bağlayıcılı' if want else 'bağlayıcısız'} tabesiz mürəkkəb cümlədir?", a=s, d=d,
                e=f"Komponentlər {'bağlayıcı ilə' if want else 'yalnız intonasiya ilə (bağlayıcısız)'} bağlanıb.", diff=H)


def cx_position(r, g):
    want = r.choice(["əvvəl", "sonra"])
    s, t, _ = r.choice([x for x in TABELI if x[2] == want])
    d = [x[0] for x in r.sample([y for y in TABELI if y[2] != want], 4)]
    return dict(t=f"Hansı cümlədə budaq cümlə baş cümlədən {'əvvəl' if want == 'əvvəl' else 'sonra'} gəlib?", a=s, d=d,
                e=f"«{s}» cümləsində budaq cümlə ({t}) baş cümlədən {want} gəlir.", diff=H)


TOPICS = {
    "aze-sound": [snd_syllables, snd_harmony, snd_back_front, snd_round, snd_voiced, snd_count, snd_double, snd_equal],
    "aze-orth": [ort_correct, ort_wrong, ort_rows, ort_ordinal, ort_hyphen, ort_capital],
    "aze-syn": [syn_word, ant_word, syn_pair, ant_pair, syn_row, ant_row],
    "aze-idiom": [idiom_meaning, idiom_find, idiom_not, idiom_close, idiom_sentence, idiom_in_sentence],
    "aze-noun": [noun_case, noun_possessive, noun_kind, adj_kind, adj_degree, adj_subst],
    "aze-verb": [verb_baglama, verb_sifat, verb_kind, verb_tense, verb_mood, verb_voice, verb_trans, verb_negative],
    "aze-member": [mem_which, mem_find, mem_has],
    "aze-complex": [cx_tabeli, cx_tabesiz, cx_sade, cx_type, cx_has_type, cx_count, cx_conj, cx_position],
}

if __name__ == "__main__":
    for g in (9, 10, 11):
        topics = {tid: build_topic(g, "az", tid, tpls, seed=8000) for tid, tpls in TOPICS.items()}
        save_grade(g, "az", topics)
