"""Azərbaycan dili · Sintaksis (Cümlənin üzvləri, Mürəkkəb cümlələr) və Durğu işarələri.

Mürəkkəb cümlə korpusu: (mətn, növ, alt növ, bağlayıcı vasitə, budaq cümlənin yeri, sadə cümlələrin sayı)
  növ: sadə | tabesiz | tabeli
  alt növ: tabesiz üçün bağlayıcılı/bağlayıcısız; tabeli üçün budaq cümlənin növü; sadə üçün çaşdırıcı səbəb
"""
from azbuild import near_miss, nconds, dlevel
from az_corpus import CORPUS
from az_pos import ROLE_NAME, POS_NAME, POS_INSTR, _links

SD, TS, TB = "sadə", "tabesiz", "tabeli"
CX = {
    9: [
        ("Yağış dayandı, günəş çıxdı.", TS, "bağlayıcısız", None, None, 2),
        ("Hava soyudu, amma biz gəzintiyə çıxdıq.", TS, "bağlayıcılı", "amma", None, 2),
        ("Mən dərsimi hazırladım, qardaşım isə rəsm çəkdi.", TS, "bağlayıcılı", "isə", None, 2),
        ("Qar yağırdı, külək əsirdi, yollar buz bağlamışdı.", TS, "bağlayıcısız", None, None, 3),
        ("Ya sən gəl, ya da mən gəlim.", TS, "bağlayıcılı", "ya", None, 2),
        ("Həm atam gəldi, həm də anam zəng etdi.", TS, "bağlayıcılı", "həm", None, 2),
        ("Uşaqlar həyətdə oynayırdı, nənələri isə onlara baxırdı.", TS, "bağlayıcılı", "isə", None, 2),
        ("Bilirəm ki, sən düz deyirsən.", TB, "tamamlıq", "ki", "sonra", 2),
        ("Müəllim dedi ki, sabah imtahan olacaq.", TB, "tamamlıq", "ki", "sonra", 2),
        ("Əgər yağış yağsa, gəzintiyə çıxmayacağıq.", TB, "şərt", "əgər", "əvvəl", 2),
        ("Çalışsan, uğur qazanarsan.", TB, "şərt", "-sa", "əvvəl", 2),
        ("Dərsə gecikdim, çünki avtobus gəlmədi.", TB, "səbəb", "çünki", "sonra", 2),
        ("Erkən yatdım ki, səhər tez durum.", TB, "məqsəd", "ki", "sonra", 2),
        ("Harada bulaq var, orada həyat var.", TB, "yer", "harada", "əvvəl", 2),
        ("Hərçənd yorğun idi, o, işini bitirdi.", TB, "güzəşt", "hərçənd", "əvvəl", 2),
        ("Yağış yağsa da, biz yola çıxdıq.", TB, "güzəşt", "-sa da", "əvvəl", 2),
        ("Elə ki yaz gəldi, quşlar geri qayıtdı.", TB, "zaman", "elə ki", "əvvəl", 2),
        ("Kim çalışsa, o, qalib gələr.", TB, "mübtəda", "kim", "əvvəl", 2),
        ("Aydındır ki, bu iş asan deyil.", TB, "mübtəda", "ki", "sonra", 2),
        ("Məqsədim budur ki, həkim olum.", TB, "xəbər", "ki", "sonra", 2),
        ("Elə bir kitab oxudum ki, onu heç unutmaram.", TB, "təyin", "ki", "sonra", 2),
        ("Nə qədər çox oxusan, o qədər çox bilərsən.", TB, "kəmiyyət", "nə qədər", "əvvəl", 2),
        ("O, evə gəldi və dərslərini hazırladı.", SD, "həmcins xəbərlər", "və", None, 1),
        ("Zəng çalınanda şagirdlər sinfə daxil oldular.", SD, "feili bağlama tərkibi", None, None, 1),
        ("Atam işdən qayıdıb nahar etdi.", SD, "feili bağlama", None, None, 1),
        ("Bağçada qızılgüllər, lalələr və nərgizlər açmışdı.", SD, "həmcins mübtədalar", "və", None, 1),
    ],
    10: [
        ("Hava qaraldı, ulduzlar göründü, kənd sakitləşdi.", TS, "bağlayıcısız", None, None, 3),
        ("Biz stansiyaya çatdıq, lakin qatar artıq getmişdi.", TS, "bağlayıcılı", "lakin", None, 2),
        ("Qonaqlar gəldi və süfrə açıldı.", TS, "bağlayıcılı", "və", None, 2),
        ("Nə o gəldi, nə də mən getdim.", TS, "bağlayıcılı", "nə", None, 2),
        ("Səhər oldu, amma günəş görünmədi, göy buludlu idi.", TS, "bağlayıcılı", "amma", None, 3),
        ("Onu da bilirəm ki, siz bu işə çox əmək sərf etmisiniz.", TB, "tamamlıq", "ki", "sonra", 2),
        ("Müəllim soruşdu ki, tapşırığı kim yerinə yetirib.", TB, "tamamlıq", "ki", "sonra", 2),
        ("İstəyirəm ki, hamı xoşbəxt olsun.", TB, "tamamlıq", "ki", "sonra", 2),
        ("Hamıya məlumdur ki, Bakı Xəzərin sahilində yerləşir.", TB, "mübtəda", "ki", "sonra", 2),
        ("Kim ki vətənini sevir, o, onu qorumağa hazırdır.", TB, "mübtəda", "kim ki", "əvvəl", 2),
        ("Arzum odur ki, universitetə qəbul olum.", TB, "xəbər", "ki", "sonra", 2),
        ("Elə bir yer seçdik ki, oradan bütün şəhər görünürdü.", TB, "təyin", "ki", "sonra", 2),
        ("Hara getsən, orada dost tapacaqsan.", TB, "yer", "hara", "əvvəl", 2),
        ("Nə vaxt ki qar yağdı, uşaqlar həyətə çıxdılar.", TB, "zaman", "nə vaxt ki", "əvvəl", 2),
        ("Əgər sən gəlməsən, mən də getməyəcəyəm.", TB, "şərt", "əgər", "əvvəl", 2),
        ("Hava yaxşı olsa, ekskursiyaya gedəcəyik.", TB, "şərt", "-sa", "əvvəl", 2),
        ("Tez yola düşdük ki, qatara çataq.", TB, "məqsəd", "ki", "sonra", 2),
        ("Ona görə gecikdim ki, yolda tıxac var idi.", TB, "səbəb", "ki", "sonra", 2),
        ("Uşaq ağlayırdı, çünki oyuncağı sınmışdı.", TB, "səbəb", "çünki", "sonra", 2),
        ("Baxmayaraq ki, hava soyuq idi, biz dənizə getdik.", TB, "güzəşt", "baxmayaraq ki", "əvvəl", 2),
        ("Sən nə qədər çalışsan, bir o qədər uğur qazanarsan.", TB, "kəmiyyət", "nə qədər", "əvvəl", 2),
        ("Dağa qalxdıqca hava soyuyurdu.", SD, "feili bağlama", None, None, 1),
        ("Şagirdlər həm oxuyur, həm də işləyirlər.", SD, "həmcins xəbərlər", "həm", None, 1),
        ("Kitabı oxuyub bitirəndən sonra onu kitabxanaya qaytardım.", SD, "feili bağlama tərkibi", None, None, 1),
        ("Anam, atam və bacım bayramı nənəmgildə qeyd etdilər.", SD, "həmcins mübtədalar", "və", None, 1),
    ],
    11: [
        ("Səhər tezdən yola düşən səyyahlar dağın ətəyinə çatanda günəş artıq yüksəlmişdi, lakin hava hələ də sərin idi.",
         TS, "bağlayıcılı", "lakin", None, 2),
        ("Gün batdı, şəhərin işıqları yandı, küçələrdə gəzintiyə çıxanların sayı artdı.", TS, "bağlayıcısız", None, None, 3),
        ("Ya qatar vaxtında gələcək, ya da biz sabaha qədər gözləməli olacağıq.", TS, "bağlayıcılı", "ya", None, 2),
        ("Qonaqlar gəldi, süfrə açıldı və hamı bayramı təbrik etdi.", TS, "bağlayıcılı", "və", None, 3),
        ("Dəniz sakitləşmişdi, balıqçılar isə qayıqlarını suya salmağa hazırlaşırdılar.", TS, "bağlayıcılı", "isə", None, 2),
        ("Ata-babalarımızdan qalan adət-ənənələri qorumalıyıq ki, gələcək nəsillər də onları tanısın.", TB, "məqsəd", "ki", "sonra", 2),
        ("Səhər çox erkən oyandım ki, paytaxta gedən ilk qatara çatım.", TB, "məqsəd", "ki", "sonra", 2),
        ("Əgər vaxtında tədbir görülməsə, sahildəki qədim tikililər tamamilə dağılacaq.", TB, "şərt", "əgər", "əvvəl", 2),
        ("Hamıya aydın idi ki, uzun illər boyu davam edən mübahisə bu dəfə sülhlə başa çatacaq.", TB, "mübtəda", "ki", "sonra", 2),
        ("Məlumdur ki, Azərbaycan zəngin təbii sərvətlərə malikdir.", TB, "mübtəda", "ki", "sonra", 2),
        ("Kim ki elmə dəyər verir, o, heç vaxt geri qalmır.", TB, "mübtəda", "kim ki", "əvvəl", 2),
        ("Hərçənd səfər çətin və uzun idi, yolçular heç bir şikayət etmədən mənzil başına çatdılar.", TB, "güzəşt", "hərçənd", "əvvəl", 2),
        ("Baxmayaraq ki, sınaq çətin keçdi, tələbələrin hamısı yüksək nəticə göstərdi.", TB, "güzəşt", "baxmayaraq ki", "əvvəl", 2),
        ("Alim elə bir kəşf etdi ki, onun adı bütün dünyada tanındı.", TB, "təyin", "ki", "sonra", 2),
        ("Harada ki zəhmət var, orada bərəkət də var.", TB, "yer", "harada ki", "əvvəl", 2),
        ("Gənc rəssamın arzusu bu idi ki, əsərləri beynəlxalq sərgidə nümayiş etdirilsin.", TB, "xəbər", "ki", "sonra", 2),
        ("Kitabxanaya gələn oxucuların sayı artmışdı, çünki yeni nəşrlər gətirilmişdi.", TB, "səbəb", "çünki", "sonra", 2),
        ("Sən nə qədər səbirli olsan, işlərin bir o qədər yaxşı gedəcək.", TB, "kəmiyyət", "nə qədər", "əvvəl", 2),
        ("Biz istəyirik ki, ana dilimiz bütün sahələrdə daha geniş işlənsin.", TB, "tamamlıq", "ki", "sonra", 2),
        ("Elə ki imtahanlar başa çatdı, tələbələr doğma kəndlərinə yola düşdülər.", TB, "zaman", "elə ki", "əvvəl", 2),
        ("Tələbələr mühazirəni diqqətlə dinləyir, qeydlər aparır, sonra suallar verirdilər.", SD, "həmcins xəbərlər", None, None, 1),
        ("Qatar stansiyaya çatan kimi sərnişinlər vaqonlardan düşüb şəhərə tərəf getdilər.", SD, "feili bağlama tərkibi", None, None, 1),
        ("Gördüklərini danışmaq istəyən uşaq həyəcandan sözlərini çaşdırırdı.", SD, "feili sifət tərkibi", None, None, 1),
        ("Həm müəllimlər, həm də şagirdlər yeni məktəb binasının açılışına toplaşmışdılar.", SD, "həmcins mübtədalar", "həm", None, 1),
    ],
}


class CS:
    def __init__(self, text, typ, sub, conn, pos, n):
        self.text, self.typ, self.sub, self.conn, self.pos, self.n = text, typ, sub, conn, pos, n


def _cx(g):
    return [CS(*x) for x in CX[g]]


TB_KINDS = ["mübtəda", "xəbər", "tamamlıq", "təyin", "zaman", "yer", "şərt", "səbəb", "məqsəd", "güzəşt", "kəmiyyət"]


def _cx_conds(x):
    """Cümlənin doğru xüsusiyyətləri — şərt kataloqu"""
    C = []
    if x.typ == SD:
        C.append(("typ", "cümlə sadədir", lambda y: y.typ == SD))
    if x.typ == TS:
        C.append(("typ", "cümlə tabesiz mürəkkəbdir", lambda y: y.typ == TS))
        C.append(("sub", f"tabesiz mürəkkəb cümlənin komponentləri {'bağlayıcı ilə' if x.sub == 'bağlayıcılı' else 'bağlayıcısız (intonasiya ilə)'} əlaqələnib",
                  lambda y, s=x.sub: y.typ == TS and y.sub == s))
    if x.typ == TB:
        C.append(("typ", "cümlə tabeli mürəkkəbdir", lambda y: y.typ == TB))
        C.append(("sub", f"budaq cümlə {x.sub} budaq cümləsidir", lambda y, s=x.sub: y.typ == TB and y.sub == s))
        C.append(("pos", f"budaq cümlə baş cümlədən {x.pos} gəlir",
                  lambda y, p=x.pos: y.typ == TB and y.pos == p))
        if x.conn in ("ki", "çünki", "əgər", "hərçənd"):
            C.append(("conn", f"budaq cümlə «{x.conn}» bağlayıcısı ilə bağlanıb", lambda y, c=x.conn: y.typ == TB and y.conn == c))
        if x.conn in ("-sa", "-sa da"):
            C.append(("conn", "budaq cümlə bağlayıcısız, xəbərin şəkilçisi vasitəsilə bağlanıb", lambda y: y.typ == TB and y.conn in ("-sa", "-sa da")))
    C.append(("n", f"cümlə {x.n} sadə cümlədən ibarətdir" if x.n > 1 else "cümlədə bir xəbər mərkəzi var", lambda y, n=x.n: y.n == n))
    return C


def cx_multi(r, g):
    pool = _cx(g)
    tgt = r.choice([x for x in pool if x.typ != SD or g != 9])
    k = nconds(r, g)
    cs = _cx_conds(tgt)
    r.shuffle(cs)
    chosen, keys = [], set()
    # ən informativ şərt (növ/alt növ) mütləq olsun
    pref = [c for c in cs if c[0] in ("sub", "conn")] or [c for c in cs if c[0] == "typ"]
    if pref:
        chosen.append(pref[0])
        keys.add(pref[0][0])
    for c in cs:
        if len(chosen) >= k:
            break
        if c[0] in keys:
            continue
        chosen.append(c)
        keys.add(c[0])
    res = near_miss(r, pool, [c[2] for c in chosen], lambda x: x.text)
    if not res:
        return None
    opts, ok, ans = res
    desc = {SD: f"sadə cümlədir ({ans.sub})", TS: f"tabesiz mürəkkəb cümlədir ({ans.sub}, {ans.n} komponent)",
            TB: f"tabeli mürəkkəb cümlədir: budaq cümlə — {ans.sub}, baş cümlədən {ans.pos}"}[ans.typ]
    return dict(t=f"Hansı variantda {', '.join(c[1] for c in chosen[:-1])}{' və ' if len(chosen) > 1 else ''}{chosen[-1][1]}?",
                opts=opts, ok=ok, diff=dlevel(len(chosen)), e=f"«{ans.text}» — {desc}.")


def _cx_desc(x):
    if x.typ == SD:
        return "sadə cümlə"
    if x.typ == TS:
        return f"tabesiz mürəkkəb cümlə; {x.sub}; {x.n} komponent"
    return f"tabeli mürəkkəb cümlə; {x.sub} budaq cümləsi; budaq baş cümlədən {x.pos}"


def cx_desc(r, g):
    pool = _cx(g)
    x = r.choice([y for y in pool if y.typ != SD])
    true = _cx_desc(x)
    alts = set()
    if x.typ == TB:
        near = {"tamamlıq": ["mübtəda", "xəbər"], "mübtəda": ["tamamlıq", "xəbər"], "xəbər": ["mübtəda", "təyin"],
                "təyin": ["tamamlıq", "xəbər"], "zaman": ["şərt", "səbəb"], "şərt": ["zaman", "güzəşt"], "səbəb": ["məqsəd", "zaman"],
                "məqsəd": ["səbəb", "tamamlıq"], "güzəşt": ["şərt", "səbəb"], "yer": ["zaman", "şərt"], "kəmiyyət": ["şərt", "zaman"]}[x.sub]
        other_pos = "sonra" if x.pos == "əvvəl" else "əvvəl"
        for s in near:
            alts.add(f"tabeli mürəkkəb cümlə; {s} budaq cümləsi; budaq baş cümlədən {x.pos}")
            alts.add(f"tabeli mürəkkəb cümlə; {s} budaq cümləsi; budaq baş cümlədən {other_pos}")
        alts.add(f"tabeli mürəkkəb cümlə; {x.sub} budaq cümləsi; budaq baş cümlədən {other_pos}")
        alts.add(f"tabesiz mürəkkəb cümlə; bağlayıcılı; {x.n} komponent")
    else:
        other = "bağlayıcısız" if x.sub == "bağlayıcılı" else "bağlayıcılı"
        alts.add(f"tabesiz mürəkkəb cümlə; {other}; {x.n} komponent")
        alts.add(f"tabesiz mürəkkəb cümlə; {x.sub}; {x.n + 1 if x.n == 2 else 2} komponent")
        alts.add(f"tabesiz mürəkkəb cümlə; {other}; {x.n + 1 if x.n == 2 else 2} komponent")
        alts.add("sadə cümlə")
        alts.add(f"tabeli mürəkkəb cümlə; tamamlıq budaq cümləsi; budaq baş cümlədən sonra")
        alts.add(f"tabeli mürəkkəb cümlə; zaman budaq cümləsi; budaq baş cümlədən əvvəl")
    alts.discard(true)
    alts = sorted(alts)
    r.shuffle(alts)
    if len(alts) < 4:
        return None
    opts = alts[:4] + [true]
    r.shuffle(opts)
    ok = [o == _cx_desc(x) for o in opts]
    return dict(t=f"«{x.text}» cümləsinin təhlili hansı variantda düzgün verilib?", opts=opts, ok=ok, diff="hard",
                e=f"Düzgün təhlil: {true}.")


# ======================= Cümlənin üzvləri =======================

POS_COP = {"İ": "isimlə ifadə olunub", "S": "sifətlə ifadə olunub", "Say": "sayla ifadə olunub", "Ə": "əvəzliklə ifadə olunub",
           "F": "feillə ifadə olunub", "FS": "feili sifətlə ifadə olunub", "FB": "feili bağlama ilə ifadə olunub",
           "Məs": "məsdərlə ifadə olunub", "Z": "zərflə ifadə olunub"}
HEADS = {"FS", "FB", "Məs"}


def _runs(s):
    """Ardıcıl eyni vəzifəli sözlər (üzv deyil olanlar ayırır)"""
    out = []
    for t in s.toks:
        if t.role in ("-", "?"):
            out.append(None)
            continue
        if out and out[-1] and out[-1][0] == t.role:
            out[-1][1].append(t)
        else:
            out.append([t.role, [t]])
    return [m for m in out if m]


def _clear(run):
    """Run bir üzvdürmü: tək söz, «söz + qoşma» və ya sonu feili sifət/bağlama/məsdər olan tərkib (+ qoşma)"""
    ts = run[1]
    if len(ts) == 1:
        return True
    body = ts[:-1] if ts[-1].pos == "Q" else ts
    if len(body) == 1:
        return True
    return body[-1].pos in HEADS and not any(t.pos in HEADS or t.pos == "Q" for t in body[:-1])


def clear_sent(s):
    return not s.doubt and all(_clear(r_) for r_ in _runs(s))


def _members(s):
    return _runs(s)


def _mem_conds():
    C = []
    for r_, nm in ROLE_NAME.items():
        if r_ != "X":
            C.append((f"has-{r_}", f"{nm} var", lambda s, r_=r_: r_ in s.roles()))
            C.append((f"has-{r_}", f"{nm} yoxdur", lambda s, r_=r_: r_ not in s.roles()))
    for p in ("İ", "Ə", "Məs", "Say"):
        C.append(("M-pos", f"mübtəda {POS_INSTR[p]} ifadə olunub", lambda s, p=p: p in s.role_pos("M")))
    C.append(("X-pos", "xəbər feillə ifadə olunub", lambda s: "F" in s.role_pos("X")))
    C.append(("X-pos", "xəbər ismi xəbərdir (isim və ya sifətlə ifadə olunub)", lambda s: s.role_pos("X") & {"İ", "S"} != set()))
    C.append(("Zr-FB", "zərflik feili bağlama və ya onun tərkibi ilə ifadə olunub", lambda s: any(t.pos == "FB" and t.role == "Zr" for t in s.toks)))
    C.append(("Zr-Q", "zərflik qoşmalı birləşmə ilə ifadə olunub", lambda s: any(t.pos == "Q" and t.role == "Zr" for t in s.toks)))
    C.append(("Zr-Z", "zərflik zərflə ifadə olunub", lambda s: any(t.pos == "Z" and t.role == "Zr" for t in s.toks)))
    C.append(("Ty-FS", "təyin feili sifət və ya onun tərkibi ilə ifadə olunub", lambda s: any(t.pos == "FS" and t.role == "Ty" for t in s.toks)))
    C.append(("Ty-Ə", "təyin əvəzliklə ifadə olunub", lambda s: any(t.pos == "Ə" and t.role == "Ty" for t in s.toks)))
    C.append(("Ty-Say", "təyin sayla ifadə olunub", lambda s: any(t.pos == "Say" and t.role == "Ty" for t in s.toks)))
    C.append(("Ty-y", "təyin yiyəlik halında olan isimlə ifadə olunub", lambda s: any(t.pos == "İ" and t.case == "y" and t.role == "Ty" for t in s.toks)))
    C.append(("Tvs-Məs", "vasitəsiz tamamlıq məsdər və ya onun tərkibi ilə ifadə olunub", lambda s: any(t.pos == "Məs" and t.role == "Tvs" for t in s.toks)))
    C.append(("Tvs-a", "vasitəsiz tamamlıq adlıq halda (qeyri-müəyyən) işlənib", lambda s: any(t.pos == "İ" and t.case == "a" and t.role == "Tvs" for t in s.toks)))
    C.append(("Tvl-Ə", "vasitəli tamamlıq əvəzliklə ifadə olunub", lambda s: any(t.pos == "Ə" and t.role == "Tvl" for t in s.toks)))
    for r_ in ("M", "Tvs", "X", "Zr"):
        C.append((f"homo-{r_}", f"həmcins {ROLE_NAME[r_]}lar var".replace("xəbərlar", "xəbərlər").replace("zərfliklar", "zərfliklər"),
                  lambda s, r_=r_: _links(s, r_)))
    C.append(("mur", "müraciət var", lambda s: any(t.pos == "İ" and t.role == "-" for t in s.toks)))
    C.append(("mur", "ara söz (modal söz) var", lambda s: s.n("Mod") > 0))
    return C


def mem_multi(r, g):
    pool = [s for s in CORPUS[g] if not s.doubt]
    k = nconds(r, g) + (1 if g == 11 else 0)
    tgt = r.choice(pool)
    cs = [c for c in _mem_conds() if c[2](tgt)]
    r.shuffle(cs)
    # «yoxdur» tipli şərtlər birdən çox olmasın; ən azı bir ifadə vasitəsi şərti olsun
    expr = [c for c in cs if "ifadə olunub" in c[1] or c[0].startswith("homo")]
    if not expr:
        return None
    chosen, keys = [expr[0]], {expr[0][0]}
    negs = 0
    for c in cs:
        if len(chosen) >= k:
            break
        if c[0] in keys or (c[0].startswith("has-") and c[0].replace("has-", "") in {x[0].split("-")[0] for x in chosen}):
            continue
        if "yoxdur" in c[1]:
            if negs:
                continue
            negs += 1
        chosen.append(c)
        keys.add(c[0])
    if len(chosen) < k:
        return None
    res = near_miss(r, pool, [c[2] for c in chosen], lambda s: s.text)
    if not res:
        return None
    opts, ok, ans = res
    mem = "; ".join(f"{ROLE_NAME[m[0]]} — {' '.join(t.w for t in m[1])}" for m in _members(ans))
    return dict(t=f"Hansı cümlədə {', '.join(c[1] for c in chosen[:-1])} və {chosen[-1][1]}?", opts=opts, ok=ok,
                diff=dlevel(len(chosen)), e=f"«{ans.text}»: {mem}.")


def mem_mark(r, g):
    """Variantlar: cümlədə dırnağa alınmış söz; şərt — onun üzv vəzifəsi və nitq hissəsi."""
    pool = [s for s in CORPUS[g] if clear_sent(s)]
    items = []
    for s in pool:
        for i, t in enumerate(s.toks):
            if t.role in ROLE_NAME and t.pos != "Q" and sum(1 for z in s.toks if z.w.lower() == t.w.lower()) == 1:
                items.append((s, i))
    s, i = r.choice(items)
    t = s.toks[i]
    conds = [lambda it, rr=t.role: it[0].toks[it[1]].role == rr]
    txt = [f"{ROLE_NAME[t.role]} vəzifəsindədir"]
    if g != 9:
        conds.append(lambda it, p=t.pos: it[0].toks[it[1]].pos == p)
        txt.append(POS_COP[t.pos])
    if g == 11:
        in_phrase = len([m for m in _members(s) if any(z is t for z in m[1])][0][1]) > 1
        conds.append(lambda it, f=in_phrase: (len([m for m in _members(it[0]) if any(z is it[0].toks[it[1]] for z in m[1])][0][1]) > 1) == f)
        txt.append("söz birləşməsinin (tərkibin) tərkib hissəsidir" if in_phrase else "üzvü təkbaşına ifadə edir")

    def rend(it):
        ss, j = it
        out = []
        for jj, z in enumerate(ss.toks):
            out.append(z.w)
        # orijinal mətndə sözü dırnağa al
        w = ss.toks[j].w
        idx = ss.text.find(w)
        if idx < 0:
            idx = ss.text.lower().find(w.lower())
        return ss.text[:idx] + "«" + ss.text[idx: idx + len(w)] + "»" + ss.text[idx + len(w):]

    res = near_miss(r, items, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    at = ans[0].toks[ans[1]]
    return dict(t=f"Hansı cümlədə dırnaq içindəki söz {_join2(txt)}?", opts=opts, ok=ok, diff=dlevel(len(conds) + 1),
                e=f"«{at.w}» — {ROLE_NAME[at.role]}, {POS_NAME[at.pos]}. (Tərkibin daxilindəki sözlər tərkibin bütövlükdə daşıdığı üzvün tərkibinə daxildir.)")


def _join2(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " və " + xs[-1]


def mem_analysis(r, g):
    pool = [s for s in CORPUS[g] if clear_sent(s) and len(_members(s)) >= 3]
    s = r.choice(pool)
    mem = _members(s)
    show = mem if g != 9 else mem[:4]

    def rend(ms):
        return "; ".join(f"{' '.join(t.w for t in m[1])} — {ROLE_NAME[m[0]]}" for m in ms)

    true = rend(show)
    swaps = {"Zr": ["Tvl", "Ty"], "Tvl": ["Zr", "Tvs"], "Tvs": ["Tvl", "M"], "M": ["Tvs", "Ty"], "Ty": ["Zr", "M"], "X": ["M", "Ty"]}
    alts = set()
    for i, m in enumerate(show):
        for alt in swaps[m[0]]:
            ms = [list(x) for x in show]
            ms[i] = [alt, m[1]]
            alts.add(rend(ms))
    for i in range(len(show)):
        for j in range(i + 1, len(show)):
            if show[i][0] != show[j][0]:
                ms = [list(x) for x in show]
                ms[i], ms[j] = [show[j][0], show[i][1]], [show[i][0], show[j][1]]
                alts.add(rend(ms))
    alts.discard(true)
    alts = sorted(alts)
    r.shuffle(alts)
    if len(alts) < 4:
        return None
    opts = alts[:4] + [true]
    r.shuffle(opts)
    ok = [o == rend(_members(s) if g != 9 else _members(s)[:4]) for o in opts]
    return dict(t=f"«{s.text}» cümləsinin üzvlərinə görə təhlili hansı variantda düzgün verilib?", opts=opts, ok=ok, diff="hard",
                e=f"Düzgün: {true}. Tərkiblər və qoşmalı birləşmələr bütövlükdə bir üzv sayılır.")


# ======================= Durğu işarələri =======================
import re as _re


class PV:
    """Durğu işarəli cümlə variantı"""
    def __init__(self, base, text, correct, feats, err=None):
        self.base, self.text, self.correct, self.feats, self.err = base, text, correct, feats, err


def _simple_feats(s):
    f = set()
    if s.n("Mod"):
        f.add("ara söz")
    if any(t.pos == "İ" and t.role == "-" for t in s.toks):
        f.add("müraciət")
    if s.n("N"):
        f.add("nida")
    if any(_links(s, r_) for r_ in ("M", "Tvs", "X", "Ty", "Zr", "Tvl")):
        f.add("həmcins üzvlər")
    if s.text.startswith("O, ") or ", O, " in s.text or s.text.startswith("Bu, "):
        f.add("əvəzlik-mübtəda")
    if s.text.endswith("?"):
        f.add("sual")
    return f


def _cx_feats(x):
    f = set()
    if x.typ == TS:
        f.add("tabesiz")
    if x.typ == TB:
        f.add("tabeli")
    if x.typ == SD and x.conn is None:
        f.add("sadə")
    if " ki," in x.text or x.text.startswith("Elə ki") or " ki " in x.text:
        f.add("ki")
    return f


def _errors(text, feats):
    out = []
    # vergülü sil (korpusdakı bütün vergüllər məcburidir)
    for m in _re.finditer(",", text):
        out.append((text[: m.start()] + text[m.end():], "vergül buraxılıb"))
    # «ki,» → «, ki»
    for m in _re.finditer(r" ki,", text):
        bad = text[: m.start()] + ", ki" + text[m.end():]
        out.append((bad, "vergül «ki» bağlayıcısından əvvəl qoyulub"))
    # «, çünki» → «çünki,»
    for m in _re.finditer(r", çünki ", text):
        bad = text[: m.start()] + " çünki, " + text[m.end():]
        out.append((bad, "vergül «çünki»dən sonra qoyulub"))
    if text.endswith("?"):
        out.append((text[:-1] + ".", "sual cümləsinin sonunda nöqtə qoyulub"))
    # «və» bağlayıcısından əvvəl artıq vergül (həmcins üzvlər iki olduqda)
    for m in _re.finditer(r"(\w) və ", text):
        bad = text[: m.start() + 1] + ", və " + text[m.end():]
        out.append((bad, "«və» bağlayıcısından əvvəl artıq vergül"))
    singles = list(out)
    # ikiqat səhv: iki vergül birlikdə buraxılıb və s.
    for i in range(len(singles)):
        for j in range(i + 1, len(singles)):
            a, wa = singles[i]
            if wa == "vergül buraxılıb" and singles[j][1] == "vergül buraxılıb":
                commas = [m.start() for m in _re.finditer(",", text)]
                if len(commas) >= 2:
                    k1, k2 = commas[0], commas[-1]
                    bad = text[:k1] + text[k1 + 1:k2] + text[k2 + 1:]
                    out.append((bad, "iki vergül buraxılıb"))
    return out


from functools import lru_cache


@lru_cache(maxsize=None)
def _punct_pool(g):
    pool = []
    for s in CORPUS[g]:
        f = _simple_feats(s)
        pool.append(PV(s.text, s.text, True, f))
        for bad, why in _errors(s.text, f):
            pool.append(PV(s.text, bad, False, f, why))
        # isimlə ifadə olunmuş mübtədadan sonra artıq vergül (səhv: müraciətə bənzəyir)
        t0 = s.toks[0]
        if t0.pos == "İ" and t0.role == "M" and len(s.toks) > 1 and s.text.startswith(t0.w + " "):
            pool.append(PV(s.text, t0.w + ", " + s.text[len(t0.w) + 1:], False, f, "mübtəda ilə cümlənin qalan hissəsi arasında artıq vergül"))
        # təyin ilə isim arasına vergül (səhv)
        for i in range(len(s.toks) - 1):
            a, b = s.toks[i], s.toks[i + 1]
            if a.pos == "S" and a.role == "Ty" and b.pos == "İ" and not _links(s, "Ty"):
                bad = s.text.replace(f"{a.w} {b.w}", f"{a.w}, {b.w}", 1)
                if bad != s.text:
                    pool.append(PV(s.text, bad, False, f, "təyinlə isim arasında artıq vergül"))
    for x in _cx(g):
        f = _cx_feats(x)
        pool.append(PV(x.text, x.text, True, f))
        for bad, why in _errors(x.text, f):
            pool.append(PV(x.text, bad, False, f, why))
        w0 = x.text.split()[0]
        if x.typ != TB and w0[-1].isalpha() and w0 not in ("Ya", "Həm", "Nə", "O,", "Əgər"):
            pool.append(PV(x.text, w0 + ", " + x.text[len(w0) + 1:], False, f, "birinci sözdən sonra artıq vergül"))
    # təkrarları sil, düzgün mətnlə üst-üstə düşən «səhv» variant olmasın
    good_texts = {p.text for p in pool if p.correct}
    seen, out = set(), []
    for p in pool:
        if (not p.correct and p.text in good_texts) or (p.text, p.correct) in seen:
            continue
        seen.add((p.text, p.correct))
        out.append(p)
    return out


FEAT_TXT = {"ara söz": "ara söz (modal söz) var", "müraciət": "müraciət var", "nida": "nida işlənib",
            "həmcins üzvlər": "həmcins üzvlər var", "əvəzlik-mübtəda": "mübtəda «o» və ya «bu» əvəzliyi ilə ifadə olunub",
            "sual": "cümlə sual cümləsidir", "tabesiz": "cümlə tabesiz mürəkkəb cümlədir", "tabeli": "cümlə tabeli mürəkkəb cümlədir",
            "ki": "«ki» bağlayıcısı işlənib", "sadə": "cümlə sadədir"}


def punct_multi(r, g):
    pool = _punct_pool(g)
    k = {9: 1, 10: r.choice([1, 2]), 11: 2}[g]
    tgt = r.choice([p for p in pool if p.correct and p.feats])
    fs = sorted(tgt.feats)
    r.shuffle(fs)
    fs = fs[:k]
    if len(fs) < k:
        return None
    conds = [lambda p: p.correct] + [lambda p, f=f: f in p.feats for f in fs]
    res = near_miss(r, pool, conds, lambda p: p.text)
    if not res:
        return None
    opts, ok, ans = res
    # eyni cümlənin iki düzgün variantı ola bilməz: yoxla
    return dict(t=f"Hansı cümlədə durğu işarələri düzgün qoyulub, həm də {_join2([FEAT_TXT[f] for f in fs])}?",
                opts=opts, ok=ok, diff=dlevel(k + 1),
                e=f"Düzgün: «{ans.text}». Digər variantlarda ya durğu səhvi var, ya da şərt ödənmir.")


_BASES, _CAND = {}, {}


def punct_find(r, g):
    """Beş müxtəlif cümlə: yalnız birində durğu işarələri düzgündür (səhvlər müxtəlif növlüdür)."""
    pool = _punct_pool(g)
    right = r.choice([p for p in pool if p.correct and "," in p.text])
    wrong = [p for p in pool if not p.correct and p.base != right.base]
    # düzgün cümlə ilə ortaq xüsusiyyəti olan cümlələrin səhv variantları üstünlük alır
    r.shuffle(wrong)
    wrong.sort(key=lambda p: -len(p.feats & right.feats))
    pick, bases, errs = [], {right.base}, set()
    for p in wrong:
        if p.base in bases or (p.err in errs and len(errs) < 3):
            continue
        pick.append(p)
        bases.add(p.base)
        errs.add(p.err)
        if len(pick) == 4:
            break
    if len(pick) < 4:
        return None
    items = pick + [right]
    r.shuffle(items)
    return dict(t="Hansı cümlədə durğu işarələri düzgün qoyulub?", opts=[p.text for p in items], ok=[p.correct for p in items],
                diff="hard", e=f"Düzgün: «{right.text}». Digər cümlələrdə: " + "; ".join(sorted({p.err for p in pick})) + ".")


SYNT_TOPICS = {
    "aze-member": {9: [mem_multi, mem_mark, mem_analysis], 10: [mem_multi, mem_mark, mem_analysis], 11: [mem_multi, mem_mark, mem_analysis]},
    "aze-complex": {9: [cx_multi, cx_desc], 10: [cx_multi, cx_desc], 11: [cx_multi, cx_desc]},
    "aze-punct": {9: [punct_multi, punct_find], 10: [punct_multi, punct_find], 11: [punct_multi, punct_find]},
}
