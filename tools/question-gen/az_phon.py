"""Azərbaycan dili · Fonetika: Səs və hərf (fonetik təhlil) və Orfoqrafiya (transkripsiyadan yazılış).

Fonetik təhlil yalnız «təhlükəsiz» sözlərdə aparılır: yazılışı ilə tələffüzü üst-üstə düşən sözlər
(sözün sonunda b, c, d, g, k, q, ğ yoxdur; yanaşı sait yoxdur; k/q samitdən əvvəl gəlmir; kar və cingiltili
küylü samitlər yanaşı deyil; nb yoxdur; ğ yoxdur; söz iki samitlə başlamır). Belə sözlərdə səs sayı = hərf sayı.
"""
from itertools import product as iproduct

from azbuild import near_miss, nconds, dlevel
from az_morph import VOWELS, BACK, FRONT, ROUND

OPEN_V = set("aoeəö")      # açıq (geniş) saitlər
CLOSED_V = set("ıuiü")     # qapalı (dar) saitlər
VOICED = set("bcdgğjlmnqrvyz")
VOICELESS = set("çfhkpsştx")
SONOR = set("lmnry")
OBSTR_VOICED = set("bcdgğjqvz")

WORDS = """ana ata bacı qardaş nənə baba əmi xala dayı ailə uşaqlar gəlin qonşu dost yoldaş müəllimə şagirdlər
alma armud heyva nar gilas alça şaftalı limon portağal üzüm ərik qarpız yemiş xiyar pomidor kartof soğan sarımsaq
pendir yağ şəkər bal duz çay su süt qatıq plov dolma kətə şorba
ev otaqlar qapı pəncərə divar masa stul çarpayı xalça pərdə lampa güzgü şkaf rəf divan kreslo
məktəbli sinif lövhə təbaşir dəftər qələm karandaş pozan xətkeş çanta kitablar lüğət xəritə
dəniz çay göl bulaq dərə təpə meşə çəmən tarla bostan bağlar çöl səhra ada sahil liman körpü yol küçə
günəş ay ulduz səma bulud yağış qar dolu duman şimşək ildırım külək tufan şəfəq axşam səhər gecə gündüz
inək qoyun keçi dovşan tülkü canavar ayı aslan pələng fil zürafə meymun dələ kirpi tısbağa ilan
qartal sərçə bülbül göyərçin qaranquş tutuquşu leylək durna qu
gül lalə nərgiz bənövşə qızılgül yasəmən çinar palıd şam söyüd qovaq ərik
sevinc ümid arzu sevgi həsrət kədər qorxu cəsarət səbir hörmət vətən torpaqlar
qırmızı yaşıl sarı mavi bənövşəyi narıncı qara boz ağ
gözəl şirin acı turş isti soyuq uzun qısa geniş dar dərin hündür alçaq yumşaq kövrək
qonaqlar oyunçu yazıçı rəssam müğənni həkim mühəndis sürücü fəhlə çoban əkinçi bağban dəmirçi dülgər
gəlmək getmək yazmaq oxumaq danışmaq gülmək ağlamaq qaçmaq üzmək yatmaq oyanmaq
dünya həyat zaman saniyə dəqiqə həftə ay il əsr tarix səyahət mənzərə
musiqi şeir nağıl hekayə roman dastan pyes tamaşa konsert sərgi muzey teatr kino
sərin işıq kölgə rəng səs nəfəs addım yuxu fikir xəyal sual cavablar
bayram toy hədiyyə qonaqlıq süfrə nahar şam
qızıl gümüş dəmir mis qalay daş qum gil kərpic şüşə kağız parça ipək yun
oyun top tor qapıçı hakim komanda yarış qələbə medal kubok
kənar orta sağ sol yuxarı aşağı irəli geri
nişan qalib məğlub tələbə alim sənətkar ustad şair ozan aşıq saz tar kaman
mehriban səmimi çalışqan tənbəl ağıllı savadlı cəsur igid qorxaq səxavətli
yumurta qarışqa arı milçək kəpənəklər
gəmi qatar təyyarə maşın avtobus velosiped
""".split()


def _cons(w):
    return [c for c in w if c not in VOWELS]


def safe(w):
    """yazılış = tələffüz (səs sayı hərf sayına bərabər)"""
    if not w.isalpha() or len(w) < 3:
        return False
    if w[-1] in "bcdgkqğ":
        return False
    if "ğ" in w or "nb" in w or w[0] not in VOWELS and w[1] not in VOWELS:
        return False
    for a, b in zip(w, w[1:]):
        if a in VOWELS and b in VOWELS:
            return False
        if a in "kq" and b not in VOWELS:
            return False
        if a not in VOWELS and b not in VOWELS:
            if (a in VOICELESS and b in OBSTR_VOICED) or (a in OBSTR_VOICED and b in VOICELESS):
                return False
    return True


SAFE = sorted({w for w in WORDS if safe(w)})


def syll(w):
    """Hecalara bölmə: V-CV, VC-CV, VCC-CV; sözün əvvəlindəki samit birinci hecaya, sonundakılar sonuncuya."""
    vpos = [i for i, c in enumerate(w) if c in VOWELS]
    cuts = []
    for a, b in zip(vpos, vpos[1:]):
        n = b - a - 1  # aradakı samitlərin sayı
        if n <= 1:
            cuts.append(a + 1)
        else:
            cuts.append(b - 1)  # son samit növbəti hecaya
    parts, prev = [], 0
    for c in cuts:
        parts.append(w[prev:c])
        prev = c
    parts.append(w[prev:])
    return parts


class Ph:
    def __init__(self, w):
        self.w = w
        v = [c for c in w if c in VOWELS]
        k = _cons(w)
        self.sy = syll(w)
        self.nsy = len(self.sy)
        self.open_s = sum(1 for s in self.sy if s[-1] in VOWELS)
        self.closed_s = self.nsy - self.open_s
        self.nv, self.nc = len(v), len(k)
        self.back = sum(c in BACK for c in v)
        self.front = sum(c in FRONT for c in v)
        self.round = sum(c in ROUND for c in v)
        self.openv = sum(c in OPEN_V for c in v)
        self.closedv = sum(c in CLOSED_V for c in v)
        self.voiced = sum(c in VOICED for c in k)
        self.voiceless = sum(c in VOICELESS for c in k)
        self.sonor = sum(c in SONOR for c in k)
        self.first_v = w[0] in VOWELS
        self.last_open = w[-1] in VOWELS


PH = {w: Ph(w) for w in SAFE}


def _cnt(k, noun):
    return f"{noun} yoxdur" if k == 0 else f"{k} {noun} var"


# Xüsusiyyət kataloqu: (ad, mətn(p), predikat qurucusu)
def _props(p):
    """Sözün təsvir oluna bilən xüsusiyyətləri: [(açar, mətn, fn)]"""
    out = [
        ("sy", f"{p.nsy} heca var", lambda q, n=p.nsy: q.nsy == n),
        ("open_s", _cnt(p.open_s, "açıq heca"), lambda q, n=p.open_s: q.open_s == n),
        ("closed_s", _cnt(p.closed_s, "qapalı heca"), lambda q, n=p.closed_s: q.closed_s == n),
        ("round", _cnt(p.round, "dodaqlanan sait"), lambda q, n=p.round: q.round == n),
        ("voiceless", _cnt(p.voiceless, "kar samit"), lambda q, n=p.voiceless: q.voiceless == n),
        ("voiced", _cnt(p.voiced, "cingiltili samit"), lambda q, n=p.voiced: q.voiced == n),
        ("sonor", _cnt(p.sonor, "sonor samit"), lambda q, n=p.sonor: q.sonor == n),
        ("openv", _cnt(p.openv, "açıq (geniş) sait"), lambda q, n=p.openv: q.openv == n),
        ("closedv", _cnt(p.closedv, "qapalı (dar) sait"), lambda q, n=p.closedv: q.closedv == n),
        ("len", f"{len(p.w)} səs var", lambda q, n=len(p.w): len(q.w) == n),
        ("first", "söz saitlə başlayır" if p.first_v else "söz samitlə başlayır", lambda q, f=p.first_v: q.first_v == f),
        ("last", "son heca açıqdır" if p.last_open else "son heca qapalıdır", lambda q, f=p.last_open: q.last_open == f),
    ]
    if p.back == 0:
        out.append(("harm", "bütün saitlər incədir", lambda q: q.back == 0))
    elif p.front == 0:
        out.append(("harm", "bütün saitlər qalındır", lambda q: q.front == 0))
    else:
        out.append(("harm", "həm qalın, həm də incə sait var", lambda q: q.back > 0 and q.front > 0))
    if p.voiced > p.voiceless:
        out.append(("vs", "cingiltili samitlər kar samitlərdən çoxdur", lambda q: q.voiced > q.voiceless))
    elif p.voiced < p.voiceless:
        out.append(("vs", "kar samitlər cingiltili samitlərdən çoxdur", lambda q: q.voiced < q.voiceless))
    else:
        out.append(("vs", "kar və cingiltili samitlərin sayı bərabərdir", lambda q: q.voiced == q.voiceless))
    return out


def _join(parts):
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " və " + parts[-1]


def ph_pick(r, g):
    k = nconds(r, g) + (1 if g == 11 else 0)
    w = r.choice(SAFE)
    props = _props(PH[w])
    r.shuffle(props)
    chosen, keys = [], set()
    for key, txt, fn in props:
        if key in keys or (key in ("open_s", "closed_s") and ("sy" in keys)):
            continue
        chosen.append((txt, fn))
        keys.add(key)
        if len(chosen) == k:
            break
    conds = [lambda x, f=fn: f(PH[x]) for _, fn in chosen]
    res = near_miss(r, SAFE, conds, lambda x: x)
    if not res:
        return None
    opts, ok, ans = res
    p = PH[ans]
    return dict(t=f"Hansı sözdə {_join([t for t, _ in chosen])}?", opts=opts, ok=ok, diff=dlevel(k),
                e=f"«{ans}»: hecalar — {'-'.join(p.sy)}; saitlər — {p.nv} ({p.back} qalın, {p.front} incə, {p.round} dodaqlanan); "
                  f"samitlər — {p.nc} ({p.voiced} cingiltili, {p.voiceless} kar, {p.sonor} sonor). Digər sözlər şərtlərdən ən azı birini ödəmir.")


def _desc(p, g):
    s = f"{p.nsy} heca ({p.open_s} açıq, {p.closed_s} qapalı); {p.nv} sait ({p.back} qalın, {p.front} incə)"
    if g == 11:
        s += f", {p.round} dodaqlanan"
    s += f"; {p.nc} samit ({p.voiced} cingiltili, {p.voiceless} kar)"
    if g != 9:
        s += f", {p.sonor} sonor"
    return s


class _Fake:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def ph_desc(r, g):
    w = r.choice([x for x in SAFE if len(x) >= 5])
    p = PH[w]
    true = _desc(p, g)
    variants = set()
    tries = 0
    base = dict(nsy=p.nsy, open_s=p.open_s, closed_s=p.closed_s, nv=p.nv, back=p.back, front=p.front, round=p.round,
                nc=p.nc, voiced=p.voiced, voiceless=p.voiceless, sonor=p.sonor)
    while len(variants) < 4 and tries < 300:
        tries += 1
        d = dict(base)
        m = r.choice(["os", "bf", "vv", "rnd", "son", "nv", "nc"])
        if m == "os" and d["nsy"] > 1:
            j = r.choice([1, -1])
            d["open_s"] += j
            d["closed_s"] -= j
        elif m == "bf":
            j = r.choice([1, -1])
            d["back"] += j
            d["front"] -= j
        elif m == "vv":
            j = r.choice([1, -1])
            d["voiced"] += j
            d["voiceless"] -= j
        elif m == "rnd" and g == 11:
            d["round"] += r.choice([1, -1])
        elif m == "son" and g != 9:
            d["sonor"] += r.choice([1, -1])
        elif m == "nv":
            d["nv"] += 1
            d["nsy"] += 1
            d["open_s"] += 1
            d["back" if r.random() < 0.5 else "front"] += 1
        elif m == "nc":
            d["nc"] += 1
            d["voiced" if r.random() < 0.5 else "voiceless"] += 1
        else:
            continue
        if any(v < 0 for v in d.values()) or d["sonor"] > d["voiced"] or d["round"] > d["nv"]:
            continue
        s = _desc(_Fake(**d), g)
        if s != true:
            variants.add(s)
    if len(variants) < 4:
        return None
    variants = sorted(variants)
    r.shuffle(variants)
    opts = variants[:4] + [true]
    r.shuffle(opts)
    ok = [o == _desc(p, g) for o in opts]
    return dict(t=f"«{w}» sözünün fonetik təhlili hansı variantda düzgün verilib?", opts=opts, ok=ok, diff="hard",
                e=f"«{w}» — hecalar: {'-'.join(p.sy)}. {true}.")


def ph_rows(r, g):
    k = 2 if g == 9 else 3
    w = r.choice(SAFE)
    props = [x for x in _props(PH[w]) if x[0] not in ("len",)]
    r.shuffle(props)
    chosen = props[:k - 1] if g != 9 else props[:1]
    chosen += [x for x in props[len(chosen):] if x[0] == "harm"][:1] or props[len(chosen):len(chosen) + 1]
    fns = [fn for _, _, fn in chosen]
    sat = lambda x: all(f(PH[x]) for f in fns)
    goodw = [x for x in SAFE if sat(x)]
    badw = [x for x in SAFE if not sat(x) and sum(f(PH[x]) for f in fns) >= len(fns) - 1]
    if len(goodw) < 3 + 4 * 2 or len(badw) < 4:
        return None
    rows = []
    gpool = r.sample(goodw, len(goodw))
    rows.append(sorted(gpool[:3]))
    idx = 3
    for _ in range(4):
        row = gpool[idx: idx + 2] + [r.choice(badw)]
        idx += 2
        rows.append(sorted(row))
    opts = [", ".join(x) for x in rows]
    if len(set(opts)) < 5:
        return None
    r.shuffle(opts)
    ok = [all(sat(x) for x in o.split(", ")) for o in opts]
    return dict(t=f"Hansı cərgədəki bütün sözlərdə {_join([t for _, t, _ in chosen])}?", opts=opts, ok=ok, diff=dlevel(len(chosen) + 1),
                e="Düzgün cərgədə hər üç söz şərtləri ödəyir; digər cərgələrdə bir söz şərtlərdən birinə uyğun gəlmir.")


def ph_syll(r, g):
    cands = [x for x in SAFE if PH[x].nsy >= 3 and any(len(s) >= 3 for s in PH[x].sy)]
    words = r.sample(cands, 5)
    tgt = words[0]
    rendered = []
    for i, w in enumerate(words):
        parts = PH[w].sy
        if i == 0:
            rendered.append((w, "-".join(parts)))
            continue
        # səhv bölmə: bir sərhəddi bir hərf sürüşdür
        s = "-".join(parts)
        pos = [j for j, c in enumerate(s) if c == "-"]
        j = r.choice(pos)
        shift = r.choice([-1, 1])
        t = s.replace("-", "")
        cut = [p - n for n, p in enumerate(pos)]
        cut[pos.index(j)] += shift
        if any(c <= 0 or c >= len(t) for c in cut) or len(set(cut)) != len(cut):
            return None
        out, prev = [], 0
        for c in sorted(cut):
            out.append(t[prev:c])
            prev = c
        out.append(t[prev:])
        if any(not any(ch in VOWELS for ch in seg) for seg in out):
            # saitsiz heca — açıq-aşkar səhv, çaşdırıcı deyil; başqa sürüşmə
            return None
        rendered.append((w, "-".join(out)))
    extra = ""
    if g != 9:
        k = PH[tgt].open_s
        extra = f" və həmin sözdə {k} açıq heca var"
    opts = [x[1] for x in rendered]
    if len(set(opts)) < 5:
        return None
    r.shuffle(opts)
    ok = [o.replace("-", "") in PH and "-".join(PH[o.replace("-", "")].sy) == o and
          (g == 9 or PH[o.replace("-", "")].open_s == PH[tgt].open_s) for o in opts]
    if sum(ok) != 1:
        return None
    return dict(t=f"Hansı sözün hecalara bölünməsi düzgündür{extra}?", opts=opts, ok=ok, diff="hard",
                e=f"Düzgün bölgü: {'-'.join(PH[tgt].sy)}. Saitlər arasındakı tək samit növbəti hecaya, iki samitdən ikincisi növbəti hecaya keçir.")


def ph_pair(r, g):
    """iki sözün müqayisəsi"""
    rel = r.choice(["sy_eq_round", "len_eq_vs", "sy_eq_harm"])
    pairs = [(a, b) for a in SAFE for b in SAFE if a < b]
    r.shuffle(pairs)
    pairs = pairs[:4000]
    if rel == "sy_eq_round":
        conds = [lambda p: PH[p[0]].nsy == PH[p[1]].nsy, lambda p: PH[p[0]].round > 0, lambda p: PH[p[1]].round == 0]
        txt = "hər iki sözdə hecaların sayı eynidir, birinci sözdə dodaqlanan sait var, ikincidə isə yoxdur"
    elif rel == "len_eq_vs":
        conds = [lambda p: len(p[0]) == len(p[1]), lambda p: PH[p[0]].voiceless > PH[p[1]].voiceless, lambda p: PH[p[0]].front == 0 and PH[p[1]].back == 0]
        txt = "sözlərdə səslərin sayı bərabərdir, birinci sözdə kar samitlər ikincidəkindən çoxdur, birinci sözün saitləri qalın, ikincininki incədir"
    else:
        conds = [lambda p: PH[p[0]].nsy == PH[p[1]].nsy, lambda p: PH[p[0]].open_s != PH[p[1]].open_s,
                 lambda p: (PH[p[0]].front == 0) != (PH[p[1]].front == 0)]
        txt = "heca sayı eynidir, açıq hecaların sayı fərqlidir, sözlərdən yalnız birində bütün saitlər qalındır"
    if g == 9:
        conds = conds[:2]
        txt = txt.rsplit(",", 1)[0]
    res = near_miss(r, pairs, conds, lambda p: f"{p[0]} – {p[1]}")
    if not res:
        return None
    opts, ok, ans = res
    return dict(t=f"Hansı cütdə {txt}?", opts=opts, ok=ok, diff=dlevel(len(conds)),
                e=f"«{ans[0]}»: {'-'.join(PH[ans[0]].sy)}; «{ans[1]}»: {'-'.join(PH[ans[1]].sy)}. Yalnız bu cüt bütün şərtləri ödəyir.")


# ======================= Orfoqrafiya: transkripsiyadan yazılış =======================
# (düzgün yazılış, tələffüz [transkripsiya], qayda)
PRON = [
    ("kitab", "kitap", "Sözün sonundakı b kar tələffüz olunur, amma b yazılır"),
    ("cavab", "cavap", "Sonda b yazılır"), ("hesab", "hesap", "Sonda b yazılır"), ("şərab", "şərap", "Sonda b yazılır"),
    ("məktəb", "məxtəp", "k samitdən əvvəl x kimi, sondakı b isə p kimi tələffüz olunur"),
    ("məktub", "məxtup", "k samitdən əvvəl x kimi, sondakı b isə p kimi tələffüz olunur"),
    ("kənd", "kənt", "Sonda d yazılır"), ("qənd", "qənt", "Sonda d yazılır"), ("əcdad", "əcdat", "Sonda d yazılır"),
    ("ağac", "ağaç", "Sonda c yazılır"), ("sevinc", "sevinç", "Sonda c yazılır"), ("qılınc", "qılınç", "Sonda c yazılır"),
    ("ayaq", "ayax", "Çoxhecalı sözün sonundakı q x kimi tələffüz olunur"), ("uşaq", "uşax", "Sonda q yazılır"),
    ("qonaq", "qonax", "Sonda q yazılır"), ("bıçaq", "bıçax", "Sonda q yazılır"), ("torpaq", "torpax", "Sonda q yazılır"),
    ("yarpaq", "yarpax", "Sonda q yazılır"), ("bayraq", "bayrax", "Sonda q yazılır"), ("oyuncaq", "oyuncax", "Sonda q yazılır"),
    ("qulaq", "qulax", "Sonda q yazılır"),
    ("çörək", "çörəy'", "Çoxhecalı sözün sonundakı k y' kimi tələffüz olunur, k yazılır"),
    ("ürək", "ürəy'", "Sonda k yazılır"), ("çiçək", "çiçəy'", "Sonda k yazılır"), ("kürək", "kürəy'", "Sonda k yazılır"),
    ("kəpənək", "kəpənəy'", "Sonda k yazılır"), ("köynək", "köynəy'", "Sonda k yazılır"),
    ("doqquz", "doxquz", "qq birləşməsində birinci q x kimi tələffüz olunur, qq yazılır"),
    ("saqqal", "saxqal", "qq yazılır"), ("toqqa", "toxqa", "qq yazılır"), ("ayaqqabı", "ayaxqabı", "qq yazılır"),
    ("ağsaqqal", "axsaxqal", "ğ kar samitdən əvvəl x kimi tələffüz olunur; ğ və qq yazılır"),
    ("bağça", "baxça", "ğ kar samitdən əvvəl x kimi tələffüz olunur, ğ yazılır"),
    ("sünbül", "sümbül", "n b-dən əvvəl m kimi tələffüz olunur, n yazılır"),
    ("şənbə", "şəmbə", "n b-dən əvvəl m kimi tələffüz olunur, n yazılır"),
    ("çərşənbə", "çərşəmbə", "n yazılır"), ("tənbəl", "təmbəl", "n yazılır"),
    ("uşaqlar", "uşaxlar", "q samitdən əvvəl x kimi tələffüz olunur, q yazılır"),
    ("yarpaqlar", "yarpaxlar", "q yazılır"), ("qonaqlıq", "qonaxlıx", "q yazılır"),
    ("qaçdı", "qaçtı", "Kar samitdən sonra d t kimi tələffüz olunur, d yazılır"),
    ("keçdi", "keçti", "Kar samitdən sonra d t kimi tələffüz olunur, d yazılır"),
    ("kəsdi", "kəsti", "d yazılır"),
]
PRON_D = {w: (tr, rule) for w, tr, rule in PRON}


def _wrongs(w, tr):
    """Düzgün yazılış ilə transkripsiyanın qarışığından yanlış yazılışlar"""
    t = tr.replace("'", "")
    out = set()
    if len(t) == len(w):
        diff = [i for i in range(len(w)) if w[i] != t[i]]
        for mask in iproduct([0, 1], repeat=len(diff)):
            if not any(mask):
                continue
            s = list(w)
            for m, i in zip(mask, diff):
                if m:
                    s[i] = t[i]
            out.add("".join(s))
    else:
        out.add(t)
    # əlavə hiperkorrekt / yarımçıq formalar
    if w.endswith("k"):
        out.add(w[:-1] + "y")
        out.add(w[:-1] + "q")
    if w.endswith("q"):
        out.add(w[:-1] + "ğ")
    if "qq" in w:
        out.add(w.replace("qq", "q"))
        out.add(w.replace("qq", "xq"))
    out.discard(w)
    return sorted(out)


# Cümlə çərçivələri: {A}, {B} yerinə sözlər (düzgün və ya səhv) qoyulur. Hər cümlədə iki transkripsiyalı söz var.
ORTH_FRAMES = {
    9: [("{A} pəncərənin qarşısında {B} oynayırdı.", "uşaq", "oyuncaqla"),
        ("Nənəm isti {A} və {B} süfrəyə qoydu.", "çörək", "qənd"),
        ("{A} yeni {B} oxudu.", "uşaqlar", "kitab"),
        ("Bağdakı {A} altında bir {B} görünürdü.", "ağacın", "kəpənək"),
        ("{A} {B} yolunu tanıyırdı.", "qonaq", "bağçanın"),
        ("Qardaşım {A} günü {B} gəlir.", "şənbə", "kəndə"),
        ("{A} {B} qəbul etdi.", "ağsaqqal", "qonaqları"),
        ("Yerə düşən {A} küləkdə {B} qarışdı.", "yarpaqlar", "torpağa"),
        ("Müəllim {A} sualın {B} yazdı.", "doqquz", "cavabını"),
        ("Atam {A} günü mənə {B} aldı.", "çərşənbə", "köynək"),
        ("Bu {A} uşaq {B} yazmağı sevmir.", "tənbəl", "məktub"),
        ("Sahədə {A} və {B} saralmışdı.", "sünbüllər", "yarpaqlar"),
        ("Babamın uzun {A} və köhnə {B} var idi.", "saqqalı", "bıçağı"),
        ("Bizim {A} hər il {B} keçirilir.", "kənddə", "qonaqlıq"),
        ("Pişik {A}, {B} isə onun arxasınca düşdü.", "qaçdı", "uşaqlar")],
    10: [("{A} yeni {B} geyib həyətə çıxdı.", "uşaq", "ayaqqabı"),
         ("Şagird {A} tapşırığın {B} tapdı.", "doqquz", "cavabını"),
         ("{A} günü {B} gəldi.", "çərşənbə", "qonaq"),
         ("Bu {A} oğlan heç vaxt {B} getmir.", "tənbəl", "məktəbə"),
         ("Şəhərin {A} qırmızı {B} dalğalanırdı.", "bağçasında", "bayraq"),
         ("O, {A} gələn sözləri {B} yazdı.", "ürəkdən", "məktubda"),
         ("{A} {B} nəvələrinə izah etdi.", "ağsaqqal", "hesabı"),
         ("Payızda {A} {B} örtmüşdü.", "yarpaqlar", "torpağı"),
         ("Qatar tuneldən {A}, bir saatdan sonra {B} çatdı.", "keçdi", "kəndə"),
         ("Bağban {A} günü {B} əkdi.", "şənbə", "çiçək"),
         ("Kəndli {A} {B} yığdı.", "torpaqdan", "sünbülləri"),
         ("{A} uzun {B} sığallayırdı.", "ağsaqqal", "saqqalını"),
         ("Nənə {A} ilə {B} kəsdi.", "bıçaq", "çörəyi"),
         ("{A} {B} atılıb-düşürdü.", "uşaqlar", "sevincdən"),
         ("Qız gülümsəyib {A} və {B} əlini yellədi.", "qaçdı", "qonağa")],
    11: [("{A} qayıdan {B} sevincini gizlədə bilmirdi.", "məktəbdən", "uşaqlar"),
         ("{A} sözlərini {B} yazan şair dərin fikrə daldı.", "ürəyinin", "məktubda"),
         ("{A} {B} günü gəlməyi vəd etdi.", "ağsaqqal", "çərşənbə"),
         ("{A} uşağın {B} heç kəs inanmadı.", "tənbəl", "cavabına"),
         ("Küləkdən {A} {B} kimi uçuşurdu.", "yarpaqlar", "kəpənək"),
         ("{A} süfrəsinə isti {B} qoyuldu.", "qonaqlıq", "çörək"),
         ("{A} əkilmiş {B} boy atmışdı.", "bağçada", "ağac"),
         ("Ayın {A} {B} imtahan keçiriləcək.", "doqquzunda", "məktəbdə"),
         ("Əsgər {A} qınından çıxarıb {B} öpdü.", "qılıncı", "bayrağı"),
         ("Uşaq {A} və {B} itirdi.", "qaçdı", "oyuncağını"),
         ("{A} {B} sanki quş qanad çaldı.", "sevincdən", "ürəyində"),
         ("Günəş altında {A} kimi {B} qızılı rəngə çalırdı.", "sünbül", "saqqalı"),
         ("Bu {A} {B} adı ilə tanınır.", "kənd", "əcdadlarımızın"),
         ("{A} axşamı {B} yoxlandı.", "şənbə", "hesablarımız"),
         ("{A} və {B} geyinib qonaqlığa getdi.", "köynəyini", "ayaqqabısını")],
}

# Çekim formalarının transkripsiyası (yalnız kökdəki dəyişiklik göstərilir; şəkilçi dəyişmir)
FORM_STEM = {
    "kəndə": "kənd", "kənddə": "kənd", "torpağa": "torpaq", "cavabını": "cavab", "məktəbə": "məktəb", "bağçasında": "bağça",
    "ürəkdən": "ürək", "məktubda": "məktub", "hesabı": "hesab", "torpağı": "torpaq", "torpaqdan": "torpaq",
    "saqqalını": "saqqal", "sevincdən": "sevinc", "qonağa": "qonaq", "məktəbdən": "məktəb",
    "ürəyinin": "ürək", "cavabına": "cavab", "bağçada": "bağça", "doqquzunda": "doqquz", "məktəbdə": "məktəb",
    "qılıncı": "qılınc", "oyuncaqla": "oyuncaq", "ağacın": "ağac", "bağçanın": "bağça", "qonaqları": "qonaq",
    "sünbüllər": "sünbül", "saqqalı": "saqqal", "bıçağı": "bıçaq", "sünbülləri": "sünbül", "çörəyi": "çörək", "bayrağı": "bayraq", "oyuncağını": "oyuncaq", "ürəyində": "ürək",
    "əcdadlarımızın": "əcdad", "hesablarımız": "hesab", "köynəyini": "köynək", "ayaqqabısını": "ayaqqabı",
}


def _forms(word):
    """(düzgün forma, [yanlış formalar], transkripsiya mətni)"""
    stem = FORM_STEM.get(word, word)
    if stem is None or stem not in PRON_D:
        return None
    tr, rule = PRON_D[stem]
    rest = word[len(stem):] if word.startswith(stem) else None
    if rest is None:
        # kök dəyişib (k→y, q→ğ): ürəyinin, bayrağı ...
        base = stem[:-1]
        if not word.startswith(base):
            return None
        tail = word[len(base):]
        wr = [x for x in {base + ("k" if stem.endswith("k") else "q") + tail[1:], base + ("x" if stem.endswith("q") else "y'") + tail[1:]}
              if x != word]
        wr = [x.replace("'", "") for x in wr]
        return word, sorted(set(wr) - {word}), f"[{tr}]", rule
    wr = [x + rest for x in _wrongs(stem, tr)]
    return word, wr, f"[{tr}]", rule


def orth_pron(r, g):
    frame, A, B = r.choice(ORTH_FRAMES[g])
    fa, fb = _forms(A), _forms(B)
    if not fa or not fb or not fa[1] or not fb[1]:
        return None
    combos = [(fa[0], fb[0])] + [(x, fb[0]) for x in fa[1]] + [(fa[0], y) for y in fb[1]] + [(x, y) for x in fa[1] for y in fb[1]]
    right = combos[0]
    wrong = combos[1:]
    # 11-ci sinifdə iki sözün hər ikisi səhv olan variantlara az yer ver — daha çaşdırıcı: bir hərf fərqi
    r.shuffle(wrong)
    wrong.sort(key=lambda c: (c[0] != fa[0]) + (c[1] != fb[0]))
    pick = wrong[:4]
    if len(pick) < 4:
        return None
    cap = lambda s: s[0].upper() + s[1:]
    rend = lambda c: cap(frame.format(A=c[0], B=c[1]))
    items = pick + [right]
    r.shuffle(items)
    opts = [rend(c) for c in items]
    if len(set(opts)) < 5:
        return None
    ok = [c[0] == fa[0] and c[1] == fb[0] for c in items]
    stem_a = FORM_STEM.get(A, A) or A
    stem_b = FORM_STEM.get(B, B) or B
    t = (f"Tələffüzü {fa[2]} və {fb[2]} olan sözlər hansı cümlədə düzgün yazılıb?" if g != 11 else
         f"Hansı cümlədə kökləri {fa[2]} və {fb[2]} kimi tələffüz olunan sözlərin hər ikisi orfoqrafiya qaydalarına uyğun yazılıb?")
    return dict(t=t, opts=opts, ok=ok, diff="hard",
                e=f"«{stem_a}» — {PRON_D[stem_a][1]}; «{stem_b}» — {PRON_D[stem_b][1]}. Düzgün: {rend(right)}")


# ---------- Morfoloji orfoqrafiya: samit əvəzlənməsi, sait düşümü, istisnalar ----------
# (söz, düzgün forma -ı/-i şəkilçisi ilə, səhv forma, növ)
MORPH = [
    ("çörək", "çörəyi", "çörəki", "k→y"), ("ürək", "ürəyi", "ürəki", "k→y"), ("çiçək", "çiçəyi", "çiçəki", "k→y"),
    ("inək", "inəyi", "inəki", "k→y"), ("köynək", "köynəyi", "köynəki", "k→y"), ("dirək", "dirəyi", "dirəki", "k→y"),
    ("ayaq", "ayağı", "ayaqı", "q→ğ"), ("uşaq", "uşağı", "uşaqı", "q→ğ"), ("bıçaq", "bıçağı", "bıçaqı", "q→ğ"),
    ("bayraq", "bayrağı", "bayraqı", "q→ğ"), ("yarpaq", "yarpağı", "yarpaqı", "q→ğ"), ("qulaq", "qulağı", "qulaqı", "q→ğ"),
    ("ağız", "ağzı", "ağızı", "sait düşümü"), ("burun", "burnu", "burunu", "sait düşümü"), ("oğul", "oğlu", "oğulu", "sait düşümü"),
    ("alın", "alnı", "alını", "sait düşümü"), ("sinif", "sinfi", "sinifi", "sait düşümü"), ("isim", "ismi", "isimi", "sait düşümü"),
    ("şəkil", "şəkli", "şəkili", "sait düşümü"), ("fikir", "fikri", "fikiri", "sait düşümü"), ("ömür", "ömrü", "ömürü", "sait düşümü"),
    ("qarın", "qarnı", "qarını", "sait düşümü"), ("könül", "könlü", "könülü", "sait düşümü"), ("boyun", "boynu", "boyunu", "sait düşümü"),
    ("tank", "tankı", "tanğı", "dəyişmir"), ("bank", "bankı", "banğı", "dəyişmir"), ("park", "parkı", "parğı", "dəyişmir"),
    ("hüquq", "hüququ", "hüquğu", "dəyişmir"), ("xalq", "xalqı", "xalğı", "dəyişmir"), ("fərq", "fərqi", "fərği", "dəyişmir"),
    ("nitq", "nitqi", "nitği", "dəyişmir"), ("ittifaq", "ittifaqı", "ittifağı", "dəyişmir"), ("şərq", "şərqi", "şərği", "dəyişmir"),
    ("şəhər", "şəhəri", "şəhri", "dəyişmir"), ("dəniz", "dənizi", "dənzi", "dəyişmir"), ("qəfəs", "qəfəsi", "qəfsi", "dəyişmir"),
]
MORPH_NAME = {"k→y": "k samiti y ilə əvəzlənən", "q→ğ": "q samiti ğ ilə əvəzlənən", "sait düşümü": "kökündə sait düşən",
              "dəyişmir": "kökü dəyişməyən"}
MORPH_FRAMES = ["Hamı {X} haqqında danışırdı.", "Onun {X} hamıdan fərqlənirdi.", "Müəllim {X} xüsusi qeyd etdi."]


def orth_morph(r, g):
    """Cümlələr: hər birində iki söz; biri səhv yazıla bilər. Şərt: səhv yoxdur + müəyyən hadisələr var."""
    k = 1 if g == 9 else 2
    kinds = r.sample(list(MORPH_NAME), k)
    entries = []
    for _ in range(14):
        a, b = r.sample(MORPH, 2)
        if a[0] == b[0]:
            continue
        for wa in (True, False):
            for wb in (True, False):
                entries.append((a, b, wa, wb))
    # cümlə: «{A} ilə {B} haqqında hekayə oxudum.» tipli neytral çərçivə
    frames = ["Kitabda {A} və {B} sözləri bir cümlədə işlənib.", "Lüğətdə «{A}» və «{B}» formaları verilib.",
              "Mətndə {A}, {B} kimi sözlər var idi."] if False else [
        "Şagird «{A}» və «{B}» sözlərini lövhəyə yazdı.", "Diktantda «{A}» və «{B}» sözləri işlənmişdi.",
        "Müəllim «{A}», «{B}» sözlərini misal gətirdi."]
    frame = r.choice(frames)

    def rend(e):
        a, b, wa, wb = e
        return frame.format(A=a[1] if wa else a[2], B=b[1] if wb else b[2])

    def no_err(e):
        return e[2] and e[3]

    conds = [no_err] + [lambda e, kd=kd: e[0][3] == kd or e[1][3] == kd for kd in kinds]
    if k == 2:
        conds.append(lambda e: e[0][3] != e[1][3])
    res = near_miss(r, entries, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    need = " və ".join(MORPH_NAME[kd] for kd in kinds)
    t = (f"Hansı cümlədə {need} söz var və cümlədə orfoqrafik səhv yoxdur?" if k == 1 else
         f"Hansı cümlədə həm {MORPH_NAME[kinds[0]]}, həm də {MORPH_NAME[kinds[1]]} söz düzgün yazılıb?")
    return dict(t=t, opts=opts, ok=ok, diff=dlevel(k + 1),
                e=f"{ans[0][0]} → {ans[0][1]} ({ans[0][3]}), {ans[1][0]} → {ans[1][1]} ({ans[1][3]}). "
                  "Çoxhecalı sözlərdə k/q saitlə başlayan şəkilçidən əvvəl y/ğ olur, alınma və birhecalı sözlər (tank, hüquq, xalq) istisnadır; "
                  "ağız, burun, oğul, sinif kimi sözlərdə ikinci hecanın saiti düşür.")


# ---------- Bitişik / ayrı / defislə yazılış (da/də, ki, -mı, qoşa sözlər, ən, heç) ----------
SEP = [  # (düzgün cümlə, səhv cümlə, qayda açarı)
    ("Mən də sizinlə gedəcəyəm.", "Məndə sizinlə gedəcəyəm.", "da"),
    ("Kitab evdə qalıb.", "Kitab ev də qalıb.", "da"),
    ("Sən də bu işdə iştirak et.", "Səndə bu işdə iştirak et.", "da"),
    ("Qardaşım da, bacım da gəldi.", "Qardaşımda, bacımda gəldi.", "da"),
    ("Dedi ki, sabah gələcək.", "Dediki, sabah gələcək.", "ki"),
    ("Masadakı kitab mənimdir.", "Masada ki kitab mənimdir.", "ki"),
    ("Bilirəm ki, sən haqlısan.", "Bilirəmki, sən haqlısan.", "ki"),
    ("Evdəki hamı yatmışdı.", "Evdə ki hamı yatmışdı.", "ki"),
    ("Sən bu kitabı oxudunmu?", "Sən bu kitabı oxudun mu?", "mı"),
    ("Onlar artıq gəldilərmi?", "Onlar artıq gəldilər mi?", "mı"),
    ("Yavaş-yavaş irəlilədik.", "Yavaş yavaş irəlilədik.", "qoşa"),
    ("Gülə-gülə danışırdı.", "Gülə gülə danışırdı.", "qoşa"),
    ("Ata-ana övladını qoruyar.", "Ataana övladını qoruyar.", "qoşa"),
    ("Ara-sıra bizə baş çəkir.", "Arasıra bizə baş çəkir.", "qoşa"),
    ("Bu, ən gözəl mənzərədir.", "Bu, əngözəl mənzərədir.", "ən"),
    ("Heç kim bu suala cavab vermədi.", "Heçkim bu suala cavab vermədi.", "heç"),
    ("Heç nə görmədim.", "Heçnə görmədim.", "heç"),
    ("Ayaqqabılarını təmizlədi.", "Ayaq qabılarını təmizlədi.", "bitişik"),
    ("Qızılgül bağçanı bəzəyirdi.", "Qızıl gül bağçanı bəzəyirdi.", "bitişik"),
    ("Ağsaqqal söz aldı.", "Ağ saqqal söz aldı.", "bitişik"),
    ("Günəbaxan günəşə tərəf dönür.", "Günə baxan günəşə tərəf dönür.", "bitişik"),
    ("Yarımada dənizə uzanır.", "Yarım ada dənizə uzanır.", "bitişik"),
]
SEP_NAME = {"da": "«da/də» bağlayıcısının və ya şəkilçisinin", "ki": "«ki» bağlayıcısının və ya -kı/-ki şəkilçisinin",
            "mı": "sual ədatının (-mı, -mi)", "qoşa": "qoşa sözün", "ən": "«ən» ədatının", "heç": "«heç» sözünün",
            "bitişik": "mürəkkəb sözün"}


def orth_sep(r, g):
    k = 4 if g == 11 else 3
    rows = r.sample(SEP, k)
    # variant: k cümlə ardıcıl; düzgün variantda hamısı düzgündür
    combos = list(iproduct([True, False], repeat=k))
    right = tuple([True] * k)
    wrong = [c for c in combos if c != right]
    r.shuffle(wrong)
    wrong.sort(key=lambda c: c.count(False))  # bir səhvli variantlar əvvəl — daha çaşdırıcı
    items = wrong[:4] + [right]
    if len(items) < 5:
        return None
    r.shuffle(items)
    rend = lambda c: " ".join(rows[i][0] if c[i] else rows[i][1] for i in range(k))
    opts = [rend(c) for c in items]
    ok = [all(c) for c in items]
    keys = list(dict.fromkeys(x[2] for x in rows))
    return dict(t=f"Hansı variantda bütün sözlər düzgün yazılıb ({', '.join(SEP_NAME[x] for x in keys)} yazılışına diqqət edin)?",
                opts=opts, ok=ok, diff=dlevel(k),
                e="Düzgün: " + " ".join(x[0] for x in rows) + " «da/də» bağlayıcısı, «ki» bağlayıcısı, «ən», «heç kim» ayrı; -mı ədatı, -dakı/-dəki, mürəkkəb sözlər bitişik; qoşa sözlər defislə yazılır.")


def orth_ordinal(r, g):
    from az_morph import ordinal
    years = [1918, 1991, 2003, 2010, 2016, 2020, 2023, 2026, 1828, 1937, 1945, 1969, 2005, 2014, 1996, 1990]
    nums = [3, 6, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 7, 16, 23, 27, 46, 57, 64, 79, 88]
    frames = ["{Y} ildə məktəbimizin {N} buraxılışı oldu.", "Biz {Y} ildə {N} yerə çıxdıq.", "Muzey {Y} ildə {N} dəfə sərgi açdı."]
    y, n = r.choice(years), r.choice(nums)
    fr = r.choice(frames)
    good_y, good_n = ordinal(y), ordinal(n)
    alt = lambda x: [f"{x}-{s}" for s in ("cı", "ci", "cu", "cü") if f"{x}-{s}" != ordinal(x)]
    combos = [(good_y, good_n)] + [(a, good_n) for a in alt(y)] + [(good_y, b) for b in alt(n)]
    r.shuffle(combos)
    combos = [c for c in combos if c != (good_y, good_n)][:4] + [(good_y, good_n)]
    r.shuffle(combos)
    opts = [fr.format(Y=a, N=b) for a, b in combos]
    ok = [a == good_y and b == good_n for a, b in combos]
    return dict(t="Hansı cümlədə sıra sayları rəqəmlə düzgün yazılıb?", opts=opts, ok=ok, diff="medium" if g == 10 else "hard",
                e=f"Şəkilçi sayın oxunuşundakı son saitə uyğunlaşır: {good_y}, {good_n}.")


PHON_TOPICS = {
    "aze-sound": {9: [ph_pick, ph_desc, ph_rows, ph_syll, ph_pair], 10: [ph_pick, ph_desc, ph_rows, ph_syll, ph_pair],
                  11: [ph_pick, ph_desc, ph_rows, ph_syll, ph_pair]},
    "aze-orth": {9: [orth_pron, orth_morph, orth_sep, orth_ordinal], 10: [orth_pron, orth_morph, orth_sep, orth_ordinal],
                 11: [orth_pron, orth_morph, orth_sep]},
}
