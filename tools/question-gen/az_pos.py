"""Azərbaycan dili · Əsas və köməkçi nitq hissələri (11 mövzu).

Mənbə: az_corpus.py (işarələnmiş cümlələr) + az_forms.py (qaydalarla qurulan isim və feil formaları).
Hər sual çoxşərtlidir; şərtlər hər variantda işarələrə görə yenidən yoxlanır (azbuild.near_miss + check).
"""
from azbuild import near_miss, nconds, dlevel
from az_corpus import CORPUS
from az_forms import PERS, PRON_GEN, CASES, poss_case, VPERS, PRON, TENSES, conj, VERBS, NOUNS

CASE_NAME = {"a": "adlıq", "y": "yiyəlik", "yö": "yönlük", "t": "təsirlik", "yer": "yerlik", "ç": "çıxışlıq"}
ROLE_NAME = {"M": "mübtəda", "X": "xəbər", "Tvs": "vasitəsiz tamamlıq", "Tvl": "vasitəli tamamlıq", "Ty": "təyin", "Zr": "zərflik"}
SUB_NAME = {
    "Say": {"mq": "miqdar sayı", "sr": "sıra sayı", "kəsr": "kəsr sayı", "tx": "təxmini say"},
    "Ə": {"şəxs": "şəxs əvəzliyi", "işarə": "işarə əvəzliyi", "sual": "sual əvəzliyi", "təyini": "təyini əvəzlik",
          "qayıdış": "qayıdış əvəzliyi", "qm": "qeyri-müəyyən əvəzlik", "inkar": "inkar əvəzliyi"},
    "Z": {"tərz": "tərzi-hərəkət zərfi", "zaman": "zaman zərfi", "yer": "yer zərfi", "kəm": "kəmiyyət zərfi", "məqsəd": "məqsəd zərfi"},
}
POS_NAME = {"İ": "isim", "S": "sifət", "Say": "say", "Ə": "əvəzlik", "F": "feil", "FS": "feili sifət", "FB": "feili bağlama",
            "Məs": "məsdər", "Z": "zərf", "Q": "qoşma", "B": "bağlayıcı", "Əd": "ədat", "Mod": "modal söz", "N": "nida"}
POS_INSTR = {"İ": "isimlə", "S": "sifətlə", "Say": "sayla", "Ə": "əvəzliklə", "F": "feillə", "Məs": "məsdərlə", "FS": "feili sifətlə"}
MOD_MEAN = {"əlbəttə": "təsdiq", "şübhəsiz": "təsdiq", "doğrudan da": "təsdiq", "sözsüz": "təsdiq",
            "yəqin": "ehtimal", "bəlkə": "ehtimal", "ehtimal ki": "ehtimal", "görünür": "ehtimal",
            "təəssüf ki": "təəssüf", "xoşbəxtlikdən": "sevinc", "deməli": "nəticə", "bir sözlə": "nəticə", "məncə": "fikir sahibi"}
MOD_MEAN_TXT = {"təsdiq": "təsdiq, qətiyyət", "ehtimal": "ehtimal, şübhə", "təəssüf": "təəssüf", "sevinc": "sevinc",
                "nəticə": "nəticə, yekun", "fikir sahibi": "fikrin kimə məxsus olduğunu"}
NIDA_CALL = {"ay", "ey"}  # çağırış (xitab) nidaları; qalanları hiss-həyəcan nidalarıdır


class Cond:
    def __init__(self, key, text, fn, role=False):
        self.key, self.text, self.fn, self.role = key, text, fn, role


def _n(p, word):
    return f"{p} {word}" if p else word


def _cnt_text(k, what):
    return f"{k} {what} işlənib" if k else f"{what} işlənməyib"


# ---------------- ümumi şərtlər ----------------

def general_conds(s):
    out = []
    for r_, nm in ROLE_NAME.items():
        if r_ in ("M", "Tvs", "Tvl", "Zr", "Ty"):
            out.append(Cond("role-" + r_, f"{nm} var", lambda x, r_=r_: r_ in x.roles(), True))
            out.append(Cond("role-" + r_, f"{nm} yoxdur", lambda x, r_=r_: r_ not in x.roles(), True))
    for p, ins in (("Ə", "əvəzliklə"), ("İ", "isimlə")):
        out.append(Cond("M-pos", f"mübtəda {ins} ifadə olunub", lambda x, p=p: p in x.role_pos("M"), True))
    out.append(Cond("X-pos", "xəbər feillə ifadə olunub", lambda x: "F" in x.role_pos("X"), True))
    out.append(Cond("Nmur2", "müraciət yoxdur", lambda x: not any(t.pos == "İ" and t.role == "-" for t in x.toks)))
    out.append(Cond("X-pos", "xəbər feillə ifadə olunmayıb", lambda x: "X" in x.roles() and "F" not in x.role_pos("X"), True))
    for p in ("Mod", "N", "Q", "B", "Əd", "Say", "FS", "FB", "Məs", "Z", "S"):
        out.append(Cond("has-" + p, f"{POS_NAME[p]} var", lambda x, p=p: x.n(p) > 0))
        out.append(Cond("has-" + p, f"{POS_NAME[p]} yoxdur", lambda x, p=p: x.n(p) == 0))
    out.append(Cond("end", "cümlə sual cümləsidir", lambda x: x.text.endswith("?")))
    out.append(Cond("end", "cümlə nida cümləsidir", lambda x: x.text.endswith("!")))
    out.append(Cond("Nmur", "müraciət var", lambda x: any(t.pos == "İ" and t.role == "-" for t in x.toks)))
    return out


# ---------------- mövzuya xas şərtlər ----------------

def focus_conds(topic):
    C = []
    if topic == "isim":
        for k in range(1, 6):
            C.append(Cond("cnt", f"{k} isim işlənib", lambda x, k=k: x.n("İ") == k))
        for c, nm in CASE_NAME.items():
            if c == "a":
                continue
            C.append(Cond("case-" + c, f"{nm} halında isim var", lambda x, c=c: x.n("İ", case=c) > 0))
            C.append(Cond("case-" + c, f"{nm} halında isim yoxdur", lambda x, c=c: x.n("İ", case=c) == 0))
        for r_ in ("Zr", "Ty", "Tvl", "Tvs", "X"):
            C.append(Cond("role-İ-" + r_, f"isim {ROLE_NAME[r_]} vəzifəsində işlənib",
                          lambda x, r_=r_: any(t.pos == "İ" and t.role == r_ for t in x.toks), True))
        C.append(Cond("mur-İ", "isim müraciət kimi işlənib", lambda x: any(t.pos == "İ" and t.role == "-" for t in x.toks)))
    elif topic == "sifət":
        for k in range(0, 4):
            C.append(Cond("cnt", _cnt_text(k, "sifət"), lambda x, k=k: x.n("S") == k))
        C.append(Cond("role-S-X", "sifət xəbər vəzifəsində işlənib", lambda x: any(t.pos == "S" and t.role == "X" for t in x.toks), True))
        C.append(Cond("role-S-Ty", "sifət təyin vəzifəsində işlənib", lambda x: any(t.pos == "S" and t.role == "Ty" for t in x.toks), True))
        C.append(Cond("homo-S", "həmcins sifətlər işlənib", lambda x: _homo(x, "S")))
        C.append(Cond("S-in-M", "sifət mübtədanı izah edir", lambda x: _attr_of(x, "S", "M"), True))
        C.append(Cond("S-in-Tvs", "sifət vasitəsiz tamamlığı izah edir", lambda x: _attr_of(x, "S", "Tvs"), True))
    elif topic == "say":
        for sub, nm in SUB_NAME["Say"].items():
            C.append(Cond("sub-" + sub, f"{nm} var", lambda x, sub=sub: x.n("Say", sub) > 0))
            C.append(Cond("sub-" + sub, f"{nm} yoxdur", lambda x, sub=sub: x.n("Say", sub) == 0))
        for k in range(0, 3):
            C.append(Cond("cnt", _cnt_text(k, "say"), lambda x, k=k: x.n("Say") == k))
        C.append(Cond("role-Say", "say mübtəda vəzifəsində işlənib", lambda x: any(t.pos == "Say" and t.role == "M" for t in x.toks), True))
        C.append(Cond("role-Say", "say təyin vəzifəsində işlənib", lambda x: any(t.pos == "Say" and t.role == "Ty" for t in x.toks), True))
    elif topic == "əvəzlik":
        for sub, nm in SUB_NAME["Ə"].items():
            C.append(Cond("sub-" + sub, f"{nm} var", lambda x, sub=sub: x.n("Ə", sub) > 0))
            C.append(Cond("sub-" + sub, f"{nm} yoxdur", lambda x, sub=sub: x.n("Ə", sub) == 0))
        for r_ in ("M", "Ty", "Tvs", "Tvl", "Zr"):
            C.append(Cond("role-Ə-" + r_, f"əvəzlik {ROLE_NAME[r_]} vəzifəsində işlənib",
                          lambda x, r_=r_: any(t.pos == "Ə" and t.role == r_ for t in x.toks), True))
        for c in ("yö", "t", "ç", "y"):
            C.append(Cond("case-Ə-" + c, f"{CASE_NAME[c]} halında əvəzlik var", lambda x, c=c: x.n("Ə", case=c) > 0))
        for k in range(1, 4):
            C.append(Cond("cnt", f"{k} əvəzlik işlənib", lambda x, k=k: x.n("Ə") == k))
    elif topic == "feil":
        for k in range(1, 3):
            C.append(Cond("cnt", f"feilin təsriflənən formalarından {k} işlənib", lambda x, k=k: x.n("F") == k))
        for p in ("FS", "FB", "Məs"):
            C.append(Cond("has-" + p, f"{POS_NAME[p]} var", lambda x, p=p: x.n(p) > 0))
            C.append(Cond("has-" + p, f"{POS_NAME[p]} yoxdur", lambda x, p=p: x.n(p) == 0))
        C.append(Cond("Məs-role", "məsdər mübtəda vəzifəsindədir", lambda x: any(t.pos == "Məs" and t.role == "M" for t in x.toks), True))
        C.append(Cond("Məs-role", "məsdər tamamlıq vəzifəsindədir", lambda x: any(t.pos == "Məs" and t.role in ("Tvs", "Tvl") for t in x.toks), True))
        C.append(Cond("Məs-role", "məsdər zərflik vəzifəsindədir", lambda x: any(t.pos == "Məs" and t.role == "Zr" for t in x.toks), True))
        C.append(Cond("X-pos", "xəbər feillə ifadə olunmayıb", lambda x: "X" in x.roles() and "F" not in x.role_pos("X"), True))
        C.append(Cond("neg", "inkarda olan feil var", lambda x: any(t.pos == "F" and _neg(t.w) for t in x.toks)))
    elif topic == "zərf":
        for sub, nm in SUB_NAME["Z"].items():
            C.append(Cond("sub-" + sub, f"{nm} var", lambda x, sub=sub: x.n("Z", sub) > 0))
            C.append(Cond("sub-" + sub, f"{nm} yoxdur", lambda x, sub=sub: x.n("Z", sub) == 0))
        for k in range(0, 3):
            C.append(Cond("cnt", _cnt_text(k, "zərf"), lambda x, k=k: x.n("Z") == k))
        C.append(Cond("Z-in", "zərf feili sifət tərkibinin daxilindədir", lambda x: any(t.pos == "Z" and t.role == "Ty" for t in x.toks), True))
        C.append(Cond("Z-Zr", "zərf müstəqil zərflik vəzifəsindədir", lambda x: any(t.pos == "Z" and t.role == "Zr" for t in x.toks), True))
    elif topic == "qoşma":
        C.append(Cond("has", "qoşma var", lambda x: x.n("Q") > 0))
        for c in ("yö", "ç"):
            C.append(Cond("has", f"{CASE_NAME[c]} halını idarə edən qoşma var", lambda x, c=c: x.n("Q", case=c) > 0))
            C.append(Cond("case-" + c, f"{CASE_NAME[c]} halını idarə edən qoşma yoxdur", lambda x, c=c: x.n("Q", case=c) == 0))
        C.append(Cond("has", "adlıq və ya yiyəlik halını idarə edən qoşma var", lambda x: x.n("Q", case="a") + x.n("Q", case="y") > 0))
        C.append(Cond("Q-role", "qoşma zərfliyin tərkibindədir", lambda x: any(t.pos == "Q" and t.role == "Zr" for t in x.toks), True))
        C.append(Cond("Q-role", "qoşma vasitəli tamamlığın tərkibindədir", lambda x: any(t.pos == "Q" and t.role == "Tvl" for t in x.toks), True))
        C.append(Cond("ilə", "«ilə» qoşma kimi işlənib", lambda x: any(t.pos == "Q" and t.w.lower() == "ilə" for t in x.toks)))
        C.append(Cond("ilə", "«ilə» bağlayıcı kimi işlənib", lambda x: any(t.pos == "B" and t.w.lower() == "ilə" for t in x.toks)))
        C.append(Cond("kimi", "«kimi» qoşması yönlük halını idarə edir", lambda x: any(t.pos == "Q" and t.w.lower() == "kimi" and t.case == "yö" for t in x.toks)))
    elif topic == "bağlayıcı":
        C.append(Cond("has", "bağlayıcı var", lambda x: x.n("B") > 0))
        C.append(Cond("pair", "qoşa (təkrarlanan) bağlayıcı işlənib", lambda x: x.n("B") >= 2))
        C.append(Cond("pair", "bağlayıcı bir dəfə işlənib", lambda x: x.n("B") == 1))
        PL = {"M": "mübtədaları", "Tvs": "vasitəsiz tamamlıqları", "X": "xəbərləri", "Ty": "təyinləri", "Zr": "zərflikləri",
              "Tvl": "vasitəli tamamlıqları"}
        for r_ in ("M", "Tvs", "X", "Ty", "Zr", "Tvl"):
            C.append(Cond("has", f"bağlayıcı həmcins {PL[r_]} bağlayır", lambda x, r_=r_: _links(x, r_), True))
        C.append(Cond("ilə", "«ilə» bağlayıcı kimi işlənib", lambda x: any(t.pos == "B" and t.w.lower() == "ilə" for t in x.toks)))
        C.append(Cond("ilə", "«ilə» qoşma kimi işlənib", lambda x: any(t.pos == "Q" and t.w.lower() == "ilə" for t in x.toks)))
        for w in ("və", "həm", "ya", "nə"):
            C.append(Cond("word", f"«{w}» bağlayıcısı var", lambda x, w=w: any(t.pos == "B" and t.w.lower() == w for t in x.toks)))
    elif topic == "ədat":
        C.append(Cond("has", "ədat var", lambda x: x.n("Əd") > 0))
        C.append(Cond("has", "ədat yoxdur", lambda x: x.n("Əd") == 0))
        for w in ("hətta", "məhz", "axı", "qoy", "yalnız", "ancaq", "bəs", "ən", "lap"):
            C.append(Cond("w-" + w, f"«{w}» ədatı işlənib", lambda x, w=w: any(t.pos == "Əd" and t.w.lower() == w for t in x.toks)))
        C.append(Cond("two", "iki ədat işlənib", lambda x: x.n("Əd") == 2))
    elif topic == "modal":
        C.append(Cond("has", "modal söz var", lambda x: x.n("Mod") > 0))
        C.append(Cond("has", "modal söz yoxdur", lambda x: x.n("Mod") == 0))
        for m, txt in MOD_MEAN_TXT.items():
            C.append(Cond("mean-" + m, f"modal söz {txt} bildirir", lambda x, m=m: any(t.pos == "Mod" and MOD_MEAN.get(t.w.lower()) == m for t in x.toks)))
        C.append(Cond("modpos", "modal söz cümlənin əvvəlindədir", lambda x: x.toks[0].pos == "Mod"))
    elif topic == "nida":
        C.append(Cond("has", "nida var", lambda x: x.n("N") > 0))
        C.append(Cond("has", "nida yoxdur", lambda x: x.n("N") == 0))
        C.append(Cond("has", "çağırış (xitab) nidası işlənib", lambda x: any(t.pos == "N" and t.w.lower() in NIDA_CALL for t in x.toks)))
        C.append(Cond("has", "hiss-həyəcan nidası işlənib", lambda x: any(t.pos == "N" and t.w.lower() not in NIDA_CALL for t in x.toks)))
        C.append(Cond("has", "nida müraciətlə birlikdə işlənib", lambda x: x.n("N") > 0 and any(t.pos == "İ" and t.role == "-" for t in x.toks)))
        C.append(Cond("has", "nida müraciətsiz işlənib", lambda x: x.n("N") > 0 and not any(t.pos == "İ" and t.role == "-" for t in x.toks)))
    return C


def _negative(text):
    return "yoxdur" in text or "işlənməyib" in text or "olunmayıb" in text


def _neg(w):
    w = w.lower()
    return any(s in w for s in ("madı", "mədi", "madı", "mır", "mir", "mur", "mür", "mayacaq", "məyəcək", "mamış", "məmiş",
                                "masın", "məsin", "mamıs", "məmis", "mayacağ", "məyəcəy"))


def _homo(x, pos):
    t = x.toks
    for i in range(len(t) - 2):
        if t[i].pos == pos and t[i + 2].pos == pos and t[i + 1].pos == "B":
            return True
    for i in range(len(t) - 1):
        if t[i].pos == pos and t[i + 1].pos == pos and t[i].role == t[i + 1].role and x.text.find(t[i].w + ",") >= 0:
            return True
    return False


def _attr_of(x, pos, role):
    """pos təyin kimi bilavasitə role üzvünün əvvəlində gəlir (aradakı təyinlər nəzərə alınır)"""
    t = x.toks
    for i, k in enumerate(t):
        if k.pos == pos and k.role == "Ty":
            j = i + 1
            while j < len(t) and t[j].role == "Ty":
                j += 1
            if j < len(t) and t[j].role == role and t[j].pos in ("İ", "Ə", "Say"):
                return True
    return False


def _links(x, role):
    t = x.toks
    for i, k in enumerate(t):
        if k.pos == "B":
            prev = [z for z in t[:i] if z.role not in ("-",)]
            nxt = [z for z in t[i + 1:] if z.role not in ("-",) and (role == "Ty" or z.role != "Ty")]
            if prev and nxt and prev[-1].role == role and nxt[0].role == role:
                # həmcins: əvvəl və sonra eyni üzv
                if role != "Ty" or (prev[-1].pos == nxt[0].pos):
                    return True
    return False


TOPIC_POS = {"isim": "İ", "sifət": "S", "say": "Say", "əvəzlik": "Ə", "feil": "F", "zərf": "Z", "qoşma": "Q",
             "bağlayıcı": "B", "ədat": "Əd", "modal": "Mod", "nida": "N"}


def _join(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " və " + xs[-1]


def make_multi(topic):
    def tpl(r, g):
        k = nconds(r, g)
        pool = CORPUS[g]
        focus = focus_conds(topic)
        gen = general_conds(None)
        tgt = r.choice(pool)
        fts = [c for c in focus if c.fn(tgt) and not (c.role and tgt.doubt)]
        pos_f = [c for c in fts if not _negative(c.text)]
        if not pos_f:
            return None
        r.shuffle(fts)
        first = r.choice(pos_f)
        fts = [first] + [c for c in fts if c is not first]
        chosen = [fts[0]]
        # 11-ci sinifdə iki mövzu şərti, qalanları ümumi
        nf = 2 if g == 11 and len(fts) > 1 else 1
        for c in fts[1:]:
            if len(chosen) >= nf:
                break
            if c.key not in {x.key for x in chosen}:
                chosen.append(c)
        gts = [c for c in gen if c.fn(tgt) and not (c.role and tgt.doubt)]
        r.shuffle(gts)
        for c in gts:
            if len(chosen) >= k:
                break
            if c.key in {x.key for x in chosen}:
                continue
            # mövzu şərti ilə məntiqi təkrar olmasın
            if any(c.text.split()[0] == x.text.split()[0] for x in chosen):
                continue
            chosen.append(c)
        if len(chosen) < k:
            return None
        use_role = any(c.role for c in chosen)
        P = [x for x in pool if not (use_role and x.doubt)]
        res = near_miss(r, P, [c.fn for c in chosen], lambda x: x.text)
        if not res:
            return None
        opts, ok, ans = res
        return dict(t=f"Hansı cümlədə {_join([c.text for c in chosen])}?", opts=opts, ok=ok, diff=dlevel(k),
                    e=_explain(ans, topic) + " Digər cümlələr şərtlərdən ən azı birini ödəmir.")
    tpl.__name__ = f"multi_{topic}"
    return tpl


def _explain(s, topic):
    p = TOPIC_POS[topic]
    parts = []
    for t in s.toks:
        if t.pos == p or (topic == "feil" and t.pos in ("F", "FS", "FB", "Məs")):
            lab = POS_NAME[t.pos]
            if t.sub and t.pos in SUB_NAME:
                lab = SUB_NAME[t.pos][t.sub]
            if t.case:
                lab += f", {CASE_NAME[t.case]} hal" + (" (idarə edir)" if t.pos == "Q" else "")
            if t.role in ROLE_NAME:
                lab += f", {ROLE_NAME[t.role]}"
            parts.append(f"«{t.w}» — {lab}")
    return f"«{s.text}»: " + ("; ".join(parts) if parts else f"{POS_NAME[p]} yoxdur") + "."


def make_count(topic):
    """Cümlə verilir; variantlar sayların kombinasiyasıdır."""
    p = TOPIC_POS[topic]

    def feats(s, g):
        out = [(POS_NAME[p] if topic != "feil" else "feilin təsriflənən forması", s.n(p))]
        if topic == "isim":
            out.append(("yönlük, yerlik və çıxışlıq halında isim", sum(s.n("İ", case=c) for c in ("yö", "yer", "ç"))))
            out.append(("əvəzlik", s.n("Ə")))
        elif topic == "feil":
            out.append(("feilin təsriflənməyən forması", s.n("FS") + s.n("FB") + s.n("Məs")))
            out.append(("isim", s.n("İ")))
        elif topic == "əvəzlik":
            out.append(("isim", s.n("İ")))
            out.append(("şəxs əvəzliyi", s.n("Ə", "şəxs")))
        elif topic in ("sifət", "say", "zərf"):
            out.append(("isim", s.n("İ")))
            out.append(("əvəzlik", s.n("Ə")))
        else:
            out.append(("isim", s.n("İ")))
            out.append(("köməkçi nitq hissəsi (qoşma, bağlayıcı, ədat)", s.n("Q") + s.n("B") + s.n("Əd")))
        return out[:2] if g == 9 else out

    def tpl(r, g):
        pool = [s for s in CORPUS[g] if s.n(p) > 0 and len(s.toks) >= 5 and s.n("B") <= 1]
        if not pool:
            return None
        s = r.choice(pool)
        fs = feats(s, g)
        true = tuple(v for _, v in fs)
        rend = lambda vals: "; ".join(f"{nm} — {v}" for (nm, _), v in zip(fs, vals))
        cands = set()
        for i in range(len(true)):
            for d in (-1, 1, 2):
                v = list(true)
                v[i] += d
                if v[i] >= 0:
                    cands.add(tuple(v))
        for i in range(len(true)):
            for j in range(i + 1, len(true)):
                v = list(true)
                v[i] += 1
                v[j] -= 1
                if min(v) >= 0:
                    cands.add(tuple(v))
        cands.discard(true)
        cands = sorted(cands)
        r.shuffle(cands)
        if len(cands) < 4:
            return None
        items = cands[:4] + [true]
        r.shuffle(items)
        opts = [rend(v) for v in items]
        ok = [v == tuple(val for _, val in feats(s, g)) for v in items]
        return dict(t=f"«{s.text}» cümləsindəki nitq hissələrinin sayı hansı variantda düzgün göstərilib?",
                    opts=opts, ok=ok, diff="hard", e=_explain(s, topic) + f" Düzgün: {rend(true)}.")
    tpl.__name__ = f"count_{topic}"
    return tpl


# ---------------- İsim: mənsubiyyət + hal (qaydalarla) ----------------
NOUN_FRAMES = {
    "adlıq": "{G} {N} masanın üstündə qalıb.",
    "yiyəlik": "{G} {N} cildi köhnəlib.",
    "yönlük": "Müəllim {G} {N} yüksək qiymət verdi.",
    "təsirlik": "Dostum {G} {N} maraqla nəzərdən keçirdi.",
    "yerlik": "{G} {N} bir neçə səhv tapdıq.",
    "çıxışlıq": "Tələbələr {G} {N} çox şey öyrəndilər.",
}


def noun_gen(r, g):
    n = r.choice(NOUNS)
    k = 2 if g != 11 else 3
    items = [(p, c) for p in PERS for c in CASES]
    tp, tc = r.choice(items)
    conds = [lambda it, tp=tp: it[0] == tp, lambda it, tc=tc: it[1] == tc]
    txt = [f"mənsubiyyətin {tp}ində işlənib", f"{tc} halındadır"]
    if k == 3:
        # eyni yazılışlı forma (II və III şəxs) ilə çaşdırma: əlavə şərt — sözdə n bufer samiti var
        has_buf = lambda it: it[0] == "III şəxs tək" and it[1] != "adlıq"
        want = has_buf((tp, tc))
        conds.append(lambda it, w=want: has_buf(it) == w)
        txt.append("hal şəkilçisindən əvvəl bitişdirici n samiti var" if want else "bitişdirici n samiti yoxdur")
    cap = lambda s_: s_[0].upper() + s_[1:]
    rend = lambda it: cap(NOUN_FRAMES[it[1]].format(G=PRON_GEN[it[0]], N=poss_case(n, it[0], it[1])))
    res = near_miss(r, items, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    return dict(t=f"Hansı cümlədə «{n}» ismi {_join(txt)}?", opts=opts, ok=ok, diff=dlevel(k),
                e=f"«{poss_case(n, ans[0], ans[1])}» — {ans[0]} mənsubiyyət, {ans[1]} hal ({PRON_GEN[ans[0]]} {n}). "
                  "II və III şəxsin təkində bəzi formalar eyni yazılır (kitabına), şəxsi əvəzlik müəyyən edir.")


# ---------------- Feil: zaman, şəxs, inkar (qaydalarla) ----------------

def verb_gen(r, g):
    stem, vs, obj = r.choice(VERBS)
    items = [(t, p, neg) for t in TENSES for p in VPERS for neg in (False, True)]
    tt, tp, tn = r.choice(items)
    conds = [lambda it, tt=tt: it[0] == tt, lambda it, tp=tp: it[1] == tp]
    txt = [f"feil {tt}dadır", f"{tp}dədir"]
    if g != 9:
        conds.append(lambda it, tn=tn: it[2] == tn)
        txt.append("inkar formasındadır" if tn else "təsdiq formasındadır")
    rend = lambda it: f"{PRON[it[1]]} {obj} {conj(stem, it[0], it[1], it[2], vs)}."
    res = near_miss(r, items, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    return dict(t=f"Hansı cümlədə {_join(txt)}?".replace("feil ", "xəbər vəzifəsindəki feil ", 1), opts=opts, ok=ok, diff=dlevel(len(conds)),
                e=f"«{conj(stem, ans[0], ans[1], ans[2], vs)}» — {ans[0]}, {ans[1]}, {'inkar' if ans[2] else 'təsdiq'} forması.")


TOPIC_IDS = {"isim": "aze-isim", "sifət": "aze-sifet", "say": "aze-say", "əvəzlik": "aze-evez", "feil": "aze-feil",
             "zərf": "aze-zerf", "qoşma": "aze-qosma", "bağlayıcı": "aze-bag", "ədat": "aze-edat", "modal": "aze-modal",
             "nida": "aze-nida"}

POS_TOPICS = {}
for _tp, _tid in TOPIC_IDS.items():
    tpls = [make_multi(_tp), make_count(_tp)]
    if _tp == "isim":
        tpls.append(noun_gen)
    if _tp == "feil":
        tpls.append(verb_gen)
    POS_TOPICS[_tid] = {9: tpls, 10: tpls, 11: tpls}
