"""Azərbaycan dili · Leksika: Sinonim, antonim və omonim; Frazeoloji birləşmələr.

Bütün suallar cümlə daxilindədir: variantlar cümlələrdir. Hər cümlə əl ilə işarələnib:
  rel — [("syn"|"ant", söz1, söz2, nitq hissəsi), ("hom", söz1, söz2, nitq hissəsi1, nitq hissəsi2)]
Frazeologizm cümlələri: idioms — [(birləşmə, məna qrupu)], literal — frazeologizmə oxşayan, amma həqiqi mənalı birləşmə.
"""
from azbuild import near_miss, nconds, dlevel

S, A, HM = "syn", "ant", "hom"

LEX = {
    9: [
        ("Qoca bağban ahıl qonşusu ilə söhbət edirdi.", [(S, "qoca", "ahıl", "sifət")]),
        ("Uzun yolu qısa vaxtda qət etdik.", [(A, "uzun", "qısa", "sifət")]),
        ("Atı tövləyə apar, topu da bura at.", [(HM, "at", "at", "isim", "feil")]),
        ("Çay kənarında oturub isti çay içdik.", [(HM, "çay", "çay", "isim", "isim")]),
        ("Cəsur əsgərlər igid komandirlərinin ardınca irəlilədi.", [(S, "cəsur", "igid", "sifət")]),
        ("Gecənin sükutu gündüzün səs-küyünü unutdurdu.", [(A, "gecə", "gündüz", "isim")]),
        ("Bu gülü sənə verirəm, bir az gül.", [(HM, "gül", "gül", "isim", "feil")]),
        ("Uşaqların sevinci və fərəhi hamıya yoluxdu.", [(S, "sevinc", "fərəh", "isim")]),
        ("Dost da, düşmən də onun cəsarətini etiraf etdi.", [(A, "dost", "düşmən", "isim")]),
        ("Qız saçını daradı, sonra quşlara dən saçdı.", [(HM, "saç", "saç", "isim", "feil")]),
        ("Yaz gəldi, dəftərinə bu şeiri yaz.", [(HM, "yaz", "yaz", "isim", "feil")]),
        ("Yeni dərslikləri köhnə kitabların yanına qoydu.", [(A, "yeni", "köhnə", "sifət")]),
        ("Bu gözəl şəhərin qəşəng küçələri var.", [(S, "gözəl", "qəşəng", "sifət")]),
        ("Ağır çantanı yüngül səbətlə dəyişdi.", [(A, "ağır", "yüngül", "sifət")]),
        ("Vətən torpağı, ana yurd hər kəs üçün əzizdir.", [(S, "vətən", "yurd", "isim")]),
        ("Sevinclə kədər bir-birini əvəz edirdi.", [(A, "sevinc", "kədər", "isim")]),
        ("Tut ağacından tut dər, səbəti möhkəm tut.", [(HM, "tut", "tut", "isim", "feil")]),
        ("Gənc müəllim cavan həmkarına kömək etdi.", [(S, "gənc", "cavan", "sifət")]),
        ("Ocağın yanında oturma, yanarsan.", [(HM, "yan", "yan", "isim", "feil")]),
        ("Kasıb ailələr də, varlı ailələr də bu bayramı sevinclə qarşılayır.", [(A, "kasıb", "varlı", "sifət")]),
        ("Tənbəl qardaşı ilə çalışqan bacısı tamamilə fərqli idi.", [(A, "tənbəl", "çalışqan", "sifət")]),
        ("Uşaq gülə-gülə qapını açdı və həyətə qaçdı.", []),
        ("Dolu yağanda vedrə su ilə dolu idi.", [(HM, "dolu", "dolu", "isim", "sifət")]),
        ("İsti yay günlərində soyuq su içməyi xoşlayırıq.", [(A, "isti", "soyuq", "sifət")]),
        ("Kədər və qəm onun ürəyini sıxırdı.", [(S, "kədər", "qəm", "isim")]),
        ("Qardaşım yavaş, asta addımlarla otağa girdi.", [(S, "yavaş", "asta", "sifət")]),
        ("Kitabxanada oxucular sakit oturub kitab oxuyurdular.", []),
        ("Səhərdən axşama qədər bağda işlədik.", [(A, "səhər", "axşam", "isim")]),
    ],
    10: [
        ("Ahıl kişi dedi ki, qoca çinar kəndin tarixini yaxşı xatırlayır.", [(S, "ahıl", "qoca", "sifət")]),
        ("Varlı tacir kasıb qonşusuna həmişə əl tuturdu.", [(A, "varlı", "kasıb", "sifət")]),
        ("Futbolçu qolunu zədələsə də, oyunun sonunda qol vurdu.", [(HM, "qol", "qol", "isim", "isim")]),
        ("Aşpaz aş bişirdi, biz isə həmin gün dağı aşdıq.", [(HM, "aş", "aş", "isim", "feil")]),
        ("Hündür binaların yanında alçaq evlər kiçik görünürdü.", [(A, "hündür", "alçaq", "sifət")]),
        ("Şagirdin xətası müəllimin diqqətindən yayınmadı, o, səhvini dərhal düzəltdi.", [(S, "xəta", "səhv", "isim")]),
        ("Yaralı əsgər sağ qaldı, amma sağ əli zədələnmişdi.", [(HM, "sağ", "sağ", "sifət", "sifət")]),
        ("Dərin dərədən dayaz çaya qədər hər yeri gəzdik.", [(A, "dərin", "dayaz", "sifət")]),
        ("Yolun sonunda yorğun səyyahı dinc və sakit bir kənd qarşıladı.", [(S, "dinc", "sakit", "sifət")]),
        ("İmtahanda yüksək bal toplayan nəvəsinə nənəsi bal göndərdi.", [(HM, "bal", "bal", "isim", "isim")]),
        ("Bağda oynayan uşaq ayaqqabısının bağını bağladı.", [(HM, "bağ", "bağ", "isim", "isim")]),
        ("Gəlmək asandır, getmək çətin.", [(A, "gəlmək", "getmək", "feil"), (A, "asan", "çətin", "sifət")]),
        ("Təzə paltarını geyindi, əski paltarlarını isə kasıblara payladı.", [(S, "təzə", "əski", "sifət")]),
        ("Uca dağların hündür zirvələri qarla örtülmüşdü.", [(S, "uca", "hündür", "sifət")]),
        ("Məqsədi aydın idi, niyyəti isə təmiz.", [(S, "məqsəd", "niyyət", "isim")]),
        ("İşıqla qaranlığın sərhədində bir kölgə tərpəndi.", [(A, "işıq", "qaranlıq", "isim")]),
        ("Qapını açan uşaq pəncərəni bağlamağı unutdu.", [(A, "açmaq", "bağlamaq", "feil")]),
        ("Bu tanınmış alim dünyada məşhur kitabların müəllifidir.", [(S, "tanınmış", "məşhur", "sifət")]),
        ("Qalib komanda məğlub rəqibini təbrik etdi.", [(A, "qalib", "məğlub", "sifət")]),
        ("Kitabı aldı, dəftəri isə dostuna verdi.", [(A, "almaq", "vermək", "feil")]),
        ("Yağışlı havada uşaqlar evdə qaldılar.", []),
        ("Qorxu və vahimə bütün kəndi bürümüşdü.", [(S, "qorxu", "vahimə", "isim")]),
        ("Qış soyuğunu yayın istisi ilə müqayisə etmək olmaz.", [(A, "qış", "yay", "isim")]),
        ("Köhnə dostunu görən kimi ağladı, sonra güldü.", [(A, "ağlamaq", "gülmək", "feil")]),
        ("Dolu yağdı, səbət isə almalarla dolu qaldı.", [(HM, "dolu", "dolu", "isim", "sifət")]),
        ("Kitabın ilk səhifəsi ilə son səhifəsi arasında böyük fərq vardı.", [(A, "ilk", "son", "sifət")]),
        ("Uşaq anasının əlindən tutub yavaş-yavaş yeriyirdi.", []),
        ("Zəhmətkeş kəndlilər çalışqan gənclərə nümunə idilər.", [(S, "zəhmətkeş", "çalışqan", "sifət")]),
    ],
    11: [
        ("Qorxaq döyüşçü çətin anda geri çəkildi, cəsur döyüşçü isə irəli atıldı.", [(A, "qorxaq", "cəsur", "sifət"), (A, "geri", "irəli", "zərf")]),
        ("Ocağın yanında oturan qoca qəfildən ayağa qalxdı: «Ehtiyatlı ol, yanarsan!»", [(HM, "yan", "yan", "isim", "feil")]),
        ("Ahıl müəllim cavan tələbələrinə gənclik illərindən danışırdı.", [(A, "ahıl", "cavan", "sifət")]),
        ("Atı yəhərləyən çoban kəndiri uzağa at deyə oğluna səsləndi.", [(HM, "at", "at", "isim", "feil")]),
        ("Hirsini, qəzəbini boğmağı bacaran insan hamının hörmətini qazanır.", [(S, "hirs", "qəzəb", "isim")]),
        ("Kasıb, yoxsul ailədə böyüsə də, əliaçıq və comərd idi.", [(S, "kasıb", "yoxsul", "sifət"), (S, "əliaçıq", "comərd", "sifət")]),
        ("Şirin xatirələr acı həqiqətlərin yanında daha qiymətli görünürdü.", [(A, "şirin", "acı", "sifət")]),
        ("Qolundan yaralanan hücumçu yenə də qol vurmağa can atırdı.", [(HM, "qol", "qol", "isim", "isim")]),
        ("Saçlarına dən düşmüş ana nəvələrinə şirniyyat saçırdı.", [(HM, "saç", "saç", "isim", "feil")]),
        ("Fikirləri, düşüncələri onu səhərə qədər yatmağa qoymadı.", [(S, "fikir", "düşüncə", "isim")]),
        ("Uzaq kəndlərdən gələn qonaqlar yaxın qohumlarımızın evində qaldılar.", [(A, "uzaq", "yaxın", "sifət")]),
        ("Sülh, barış arzusu xalqları birləşdirir, müharibə isə ayırır.", [(S, "sülh", "barış", "isim"), (A, "sülh", "müharibə", "isim")]),
        ("Çay qırağında dincələn səyyahlar dəmlənmiş çayın ətrini duydular.", [(HM, "çay", "çay", "isim", "isim")]),
        ("Ağıllı adam zəkalı həmsöhbət tapanda dərdini də unudur.", [(S, "ağıllı", "zəkalı", "sifət")]),
        ("Təmiz niyyətlə başlanan iş çirkli hiylələrə uduzmaz.", [(A, "təmiz", "çirkli", "sifət")]),
        ("İmtahandan yüksək bal alan tələbə bal arılarından bəhs edən məqalə yazdı.", [(HM, "bal", "bal", "isim", "isim")]),
        ("Vəfalı dost sədaqətli olduğu kimi, xain də satqın olur.", [(S, "vəfalı", "sədaqətli", "sifət"), (S, "xain", "satqın", "sifət")]),
        ("Böyük qardaş kiçik bacısına həmişə qayğı göstərirdi.", [(A, "böyük", "kiçik", "sifət")]),
        ("Tut ağaclarının altında oturan qızlar «Əlimdən möhkəm tut» deyib güldülər.", [(HM, "tut", "tut", "isim", "feil")]),
        ("Gülümsəyən qız əlindəki gülü müəlliminə uzatdı.", []),
        ("Dərin fikrə dalan alim dayaz mülahizələri dərhal rədd edirdi.", [(A, "dərin", "dayaz", "sifət")]),
        ("Məşhur, şöhrətli sənətkar sadəliyi ilə hamını heyran qoyurdu.", [(S, "məşhur", "şöhrətli", "sifət")]),
        ("Qələbəni qazanmaq çətin, itirmək isə çox asan oldu.", [(A, "qazanmaq", "itirmək", "feil"), (A, "çətin", "asan", "sifət")]),
        ("Yaz gələndə nənəm deyərdi: «Bu sevinci dəftərinə yaz».", [(HM, "yaz", "yaz", "isim", "feil")]),
        ("Kəndin sakit, dinc həyatı şəhərin səs-küyündən çox fərqlənirdi.", [(S, "sakit", "dinc", "sifət")]),
        ("Səhərin sərinliyi axşamın bürküsünü unutdurdu.", [(A, "səhər", "axşam", "isim")]),
        ("Uşaq kitabı ehtiyatla rəfə qoydu və otaqdan çıxdı.", []),
        ("Dağ başını duman aldı, dərələri isə qalın kölgə bürüdü.", []),
    ],
}
POS_GEN = {"sifət": "sifətlə", "isim": "isimlə", "feil": "feillə", "zərf": "zərflə"}
REL_NAME = {S: "sinonim", A: "antonim", HM: "omonim"}


class LS:
    def __init__(self, text, rels):
        self.text, self.rels = text, rels

    def has(self, t):
        return any(x[0] == t for x in self.rels)

    def pos(self, t):
        return {x[3] for x in self.rels if x[0] == t and t != HM}

    def hom_mixed(self):
        return any(x[0] == HM and x[3] != x[4] for x in self.rels)

    def n(self, t):
        return sum(1 for x in self.rels if x[0] == t)


def _pool(g):
    return [LS(t, rel) for t, rel in LEX[g]]


def lex_presence(r, g):
    k = nconds(r, g)
    pool = _pool(g)
    catalog = []
    for t in (S, A, HM):
        catalog.append((f"{REL_NAME[t]} işlənib", lambda x, t=t: x.has(t)))
        catalog.append((f"{REL_NAME[t]} işlənməyib", lambda x, t=t: not x.has(t)))
    for t in (S, A):
        for p in ("sifət", "isim", "feil"):
            catalog.append((f"{REL_NAME[t]}lər {POS_GEN[p]} ifadə olunub", lambda x, t=t, p=p: x.has(t) and p in x.pos(t)))
    catalog.append(("omonimlər müxtəlif nitq hissələrinə aiddir", lambda x: x.hom_mixed()))
    catalog.append(("omonimlər eyni nitq hissəsinə aiddir", lambda x: x.has(HM) and not x.hom_mixed()))
    catalog.append(("iki leksik cüt (sinonim, antonim və ya omonim) var", lambda x: len(x.rels) == 2))
    tgt = r.choice([x for x in pool if x.rels])
    true = [c for c in catalog if c[1](tgt)]
    r.shuffle(true)
    chosen = []
    for c in true:
        # məntiqi təkrar olmasın: «X işlənib» + «X sifətlə» → ikincisi kifayətdir
        if any(c[0].split()[0] == d[0].split()[0] for d in chosen):
            continue
        chosen.append(c)
        if len(chosen) == k:
            break
    if len(chosen) < k:
        return None
    res = near_miss(r, pool, [c[1] for c in chosen], lambda x: x.text)
    if not res:
        return None
    opts, ok, ans = res
    det = "; ".join(f"{x[1]} – {x[2]} ({REL_NAME[x[0]]})" for x in ans.rels)
    return dict(t=f"Hansı cümlədə {', '.join(c[0] for c in chosen[:-1])}{' və ' if len(chosen) > 1 else ''}{chosen[-1][0]}?",
                opts=opts, ok=ok, diff=dlevel(k), e=f"Cümlədə: {det}. Digər cümlələr şərtlərdən ən azı birini ödəmir.")


def lex_label(r, g):
    """Variant: cümlə + göstərilmiş cüt və onun növü. Şərt: həm cüt, həm də növ düzgündür (və əlavə şərt)."""
    pool = [x for x in _pool(g) if x.rels]
    items = []
    for x in pool:
        for rel in x.rels:
            for lab in (S, A, HM):
                items.append((x, rel, lab))
    extra = None
    if g != 9:
        extra = r.choice([("antonim", lambda it: it[2] == A), ("sinonim", lambda it: it[2] == S), ("omonim", lambda it: it[2] == HM)])
    conds = [lambda it: it[1][0] == it[2]]
    if extra:
        conds.append(extra[1])
    if g == 11:
        p = r.choice(["sifət", "isim", "feil"])
        conds.append(lambda it, p=p: it[1][3] == p)
    rend = lambda it: f"{it[0].text} ({it[1][1]} – {it[1][2]}: {REL_NAME[it[2]]})"
    res = near_miss(r, items, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    t = "Hansı variantda cümlədəki leksik cüt və onun növü düzgün göstərilib"
    if extra:
        t += f", həm də bu cüt {extra[0]}dir"
    if g == 11:
        t += f" və {'birinci sözü ' if ans[1][0] == HM else ''}{p} ilə ifadə olunub".replace("sifət ilə", "sifətlə").replace("isim ilə", "isimlə").replace("feil ilə", "feillə")
    return dict(t=t + "?", opts=opts, ok=ok, diff=dlevel(len(conds) + 1),
                e=f"«{ans[1][1]}» və «{ans[1][2]}» — {REL_NAME[ans[1][0]]}. Digər variantlarda ya cütün növü səhv göstərilib, ya da şərt ödənmir.")


# ======================= Frazeoloji birləşmələr =======================
GROUPS = {
    "yorğun": "çox yorulmaq", "qorx": "çox qorxmaq", "sevin": "çox sevinmək", "sus": "susmaq, danışmamaq",
    "aldat": "aldatmaq", "eşitmə": "eşitməzliyə vurmaq", "tənbəl": "heç bir iş görməmək", "hirs": "çox hirslənmək",
    "kef": "kefi pozulmaq", "gözlə": "intizarla gözləmək", "qocal": "qocalmaq", "vəfat": "vəfat etmək",
    "utan": "çox utanmaq", "anla": "başa düşmək, anlamaq", "zəhmət": "çox zəhmət çəkmək", "vəd": "vəd etmək",
    "etiraf": "etiraf etmək", "dinlə": "diqqətlə dinləmək", "kömək": "kömək etmək", "ümid": "ümidini kəsmək",
    "heyrət": "heyrətlənmək", "fikir": "çox fikirləşmək", "ruh": "ruhlandırmaq", "imza": "imzalamaq",
    "görmə": "görməzlikdən gəlmək", "birləş": "birləşib birgə çalışmaq",
}
ID = {  # cümlə: (frazeologizmlər [(birləşmə, qrup)], həqiqi mənalı oxşar birləşmə varmı)
    9: [
        ("Bütün günü bağda işləyən babam axşam əldən düşmüşdü.", [("əldən düşmək", "yorğun")], False),
        ("Qəfil səsdən hamının ürəyi ağzına gəldi.", [("ürəyi ağzına gəlmək", "qorx")], False),
        ("Hədiyyəni görəndə qızın ağzı qulağına çatdı.", [("ağzı qulağına çatmaq", "sevin")], False),
        ("Müəllim soruşanda o, ağzına su aldı.", [("ağzına su almaq", "sus")], False),
        ("Susayan uşaq ağzına bir qurtum su aldı.", [], True),
        ("Tənbəl qardaşım evdə əlini ağdan qaraya vurmur.", [("əlini ağdan qaraya vurmamaq", "tənbəl")], False),
        ("Anam dəfələrlə tapşırdı, amma o, sözləri qulaqardına vurdu.", [("qulaqardına vurmaq", "eşitmə")], False),
        ("Nənəmin gözü nəvəsinin yolunda qalmışdı.", [("gözü yolda qalmaq", "gözlə")], False),
        ("Uşaq səhvini boynuna aldı.", [("boynuna almaq", "etiraf")], False),
        ("Şagirdlər müəllimin hekayəsinə qulaq kəsilmişdilər.", [("qulaq kəsilmək", "dinlə")], False),
        ("Dostum sabah gələcəyinə söz verdi.", [("söz vermək", "vəd")], False),
        ("Məsələni həll etmək üçün xeyli baş sındırdım.", [("baş sındırmaq", "fikir")], False),
        ("Babam bizə həmişə ürək-dirək verirdi.", [("ürək-dirək vermək", "ruh")], False),
        ("Direktor əmrə qol çəkdi.", [("qol çəkmək", "imza")], False),
        ("Uşaq anasının qolundan tutub çəkdi.", [], True),
        ("Yolda gördüyü mənzərədən ağzı açıla qaldı.", [("ağzı açıla qalmaq", "heyrət")], False),
        ("Komandamız uduzanda hamımızın qanı qaraldı.", [("qanı qaralmaq", "kef")], False),
        ("Yalan danışdığını biləndə utandı, sanki yerə girdi.", [("yerə girmək", "utan")], False),
        ("Kəndlilər çörək üçün alın təri tökürdülər.", [("alın təri tökmək", "zəhmət")], False),
        ("Həkim xəstənin qulağını diqqətlə yoxladı.", [], True),
        ("Babamın saçına dən düşsə də, hələ gümrah idi.", [("saçına dən düşmək", "qocal")], False),
        ("Qonşumuz darda qalanlara həmişə əl tutur.", [("əl tutmaq", "kömək")], False),
        ("Dərsdən sonra uşaqlar parkda oynadılar.", [], False),
        ("Səhər tezdən işə başlayan fəhlələr günortaya qədər ayaqdan düşdülər.", [("ayaqdan düşmək", "yorğun")], False),
        ("Bu çətin mövzudan heç cür başım çıxmır.", [("başı çıxmaq", "anla")], False),
        ("İtirilmiş itin tapılacağından əlimizi üzmüşdük.", [("əlini üzmək", "ümid")], False),
    ],
    10: [
        ("Qaranlıq meşədə canavar səsi eşidəndə ödüm ağzıma gəldi.", [("ödü ağzına gəlmək", "qorx")], False),
        ("İmtahan nəticəsini eşidən tələbənin sevincdən ağzı qulağına çatdı.", [("ağzı qulağına çatmaq", "sevin")], False),
        ("Yarışdan qayıdan idmançılar əldən düşmüş, ayaqdan düşmüşdülər.", [("əldən düşmək", "yorğun"), ("ayaqdan düşmək", "yorğun")], False),
        ("Fırıldaqçı sadəlövh alıcının başına papaq qoydu.", [("başına papaq qoymaq", "aldat")], False),
        ("Satıcı müştərinin başını tovlayıb ona köhnə mal satdı.", [("başını tovlamaq", "aldat")], False),
        ("Ədalətsizliyi görən hakimin gözü qızdı.", [("gözü qızmaq", "hirs")], False),
        ("Xəbəri eşidən rəis od püskürürdü.", [("od püskürmək", "hirs")], False),
        ("Ağsaqqal ömrünün son günlərində dünyasını dəyişdi.", [("dünyasını dəyişmək", "vəfat")], False),
        ("Bu iş üçün o, dəridən-qabıqdan çıxdı, alın təri tökdü.", [("dəridən-qabıqdan çıxmaq", "zəhmət"), ("alın təri tökmək", "zəhmət")], False),
        ("Rəhbər bəzi nöqsanlara göz yumurdu.", [("göz yummaq", "görmə")], False),
        ("Qız gözlərini yumub bir az dincəldi.", [], True),
        ("Atası çağıranda oğlan dilini dişləyib susdu.", [("dilini dişləmək", "sus")], False),
        ("Uşaq dişini ağrıdan dodağını dişlədi.", [], True),
        ("Yaşlı ana illərlə oğlunun yolunu gözlədi, gözü yolda qaldı.", [("gözü yolda qalmaq", "gözlə")], False),
        ("Sınaqdan keçə bilməyən şagirdin qanı qaraldı.", [("qanı qaralmaq", "kef")], False),
        ("Çalışqan gənclər əl-ələ verib kəndi abadlaşdırdılar.", [("əl-ələ vermək", "birləş")], False),
        ("Usta öz şagirdinə həmişə əl uzadırdı.", [("əl uzatmaq", "kömək")], False),
        ("Möcüzəli mənzərəni görən turistlər barmaqlarını dişlədilər.", [("barmağını dişləmək", "heyrət")], False),
        ("Şahid bütün günahları boynuna aldı.", [("boynuna almaq", "etiraf")], False),
        ("Tapşırığın mənasını ağlım kəsmədi.", [("ağlı kəsmək", "anla")], False),
        ("Müəllimin tənqidindən sonra uşaq yerə girdi.", [("yerə girmək", "utan")], False),
        ("Nənəmin beli bükülsə də, bağda işləməyə davam edirdi.", [("beli bükülmək", "qocal")], False),
        ("Barmağını belə tərpətməyən oğlan hamıdan çox tərif gözləyirdi.", [("barmağını belə tərpətməmək", "tənbəl")], False),
        ("Bağban budağı kəsmək üçün əlini uzatdı.", [], True),
        ("Səyahətdən qayıdan bacım hər şeyi bir-bir danışdı.", [], False),
        ("Komandamızın qələbəsindən sevinən azarkeşlər yerə-göyə sığmırdılar.", [("yerə-göyə sığmamaq", "sevin")], False),
    ],
    11: [
        ("Səhər tezdən işə başlayan bənna günortaya qədər əldən düşsə də, iş yarımçıq qalmasın deyə alın təri tökməkdə davam etdi.",
         [("əldən düşmək", "yorğun"), ("alın təri tökmək", "zəhmət")], False),
        ("Qəfildən açılan qapının cırıltısından hamının ürəyi ağzına gəldi, yalnız ağsaqqal dinməz-söyləməz oturmuşdu.",
         [("ürəyi ağzına gəlmək", "qorx")], False),
        ("Rəqiblərinin başına papaq qoymaq istəyən tacir sonda özü aldandı.", [("başına papaq qoymaq", "aldat")], False),
        ("Müdirin tapşırıqlarını qulaqardına vuran işçi sonda gördüyü işdən utanıb yerə girdi.",
         [("qulaqardına vurmaq", "eşitmə"), ("yerə girmək", "utan")], False),
        ("Övladının imtahandan kəsildiyini eşidən atanın qanı qaraldı, gözü qızdı.", [("qanı qaralmaq", "kef"), ("gözü qızmaq", "hirs")], False),
        ("Babamın ömrünün son illərində beli bükülsə də, saçına dən düşsə də, bağda çalışmağı tərk etmədi.",
         [("beli bükülmək", "qocal"), ("saçına dən düşmək", "qocal")], False),
        ("Arzusuna çatacağından əlini üzən gənc yenidən çalışmağa başlayanda müəllimi ona ürək-dirək verdi.",
         [("əlini üzmək", "ümid"), ("ürək-dirək vermək", "ruh")], False),
        ("Sirr açılanda hamının ağzı açıla qaldı, cinayətkar isə günahını boynuna almalı oldu.",
         [("ağzı açıla qalmaq", "heyrət"), ("boynuna almaq", "etiraf")], False),
        ("Dəniz kənarında ağzına su alıb oynayan uşaqlar bir-birinin üzünə su püskürürdülər.", [], True),
        ("Danışıqlar zamanı nümayəndə ağzına su aldı, çünki ona söz verilməmişdi.", [("ağzına su almaq", "sus")], False),
        ("Ehtiyac içində yaşayan ailəyə qonşular hər zaman əl tutur, əl uzadırdılar.", [("əl tutmaq", "kömək"), ("əl uzatmaq", "kömək")], False),
        ("Usta ağır daşı qaldırmaq üçün əlini uzatdı, amma gücü çatmadı.", [], True),
        ("Komandanın kapitanı müqaviləyə qol çəkəndə azarkeşlər sevincdən yerə-göyə sığmırdılar.",
         [("qol çəkmək", "imza"), ("yerə-göyə sığmamaq", "sevin")], False),
        ("Məsələnin həllindən başı çıxmayan şagird saatlarla baş sındırdı.", [("başı çıxmaq", "anla"), ("baş sındırmaq", "fikir")], False),
        ("Tənbəl gənc evdə əlini ağdan qaraya vurmur, barmağını belə tərpətmirdi.",
         [("əlini ağdan qaraya vurmamaq", "tənbəl"), ("barmağını belə tərpətməmək", "tənbəl")], False),
        ("Rəssamın əsərinə tamaşa edənlər heyrətdən barmaqlarını dişlədilər.", [("barmağını dişləmək", "heyrət")], False),
        ("Qorxudan ödü ağzına gələn ovçu tüfəngini yerə atıb qaçdı.", [("ödü ağzına gəlmək", "qorx")], False),
        ("Müəllimin hər sözünə qulaq kəsilən tələbələr mühazirədən sonra ona çoxlu sual verdilər.", [("qulaq kəsilmək", "dinlə")], False),
        ("Xalqın sevimli şairi dünyasını dəyişsə də, onun şeirləri yaşayır.", [("dünyasını dəyişmək", "vəfat")], False),
        ("Qonaqları görən uşaq qapını açıb onları içəri dəvət etdi.", [], False),
        ("Ana illərlə oğlunun yolunu gözlədi, gözü yolda qaldı, lakin ümidini itirmədi.", [("gözü yolda qalmaq", "gözlə")], False),
        ("Sənədləri diqqətlə oxuyan hüquqşünas nöqsanlara göz yummadı.", [("göz yummaq", "görmə")], False),
        ("Yorulan uşaq gözlərini yumub dərhal yuxuya getdi.", [], True),
        ("Rəis od püskürsə də, işçilər ona söz verdikləri işi vaxtında bitirdilər.", [("od püskürmək", "hirs"), ("söz vermək", "vəd")], False),
        ("Hiyləgər qonşu sadəlövh kəndlinin başını tovlayıb torpağını ucuz qiymətə aldı.", [("başını tovlamaq", "aldat")], False),
        ("Kitabın mətləbini ağlı kəsməyən oxucu onu bir daha oxumağa qərar verdi.", [("ağlı kəsmək", "anla")], False),
    ],
}


class IS:
    def __init__(self, text, idioms, literal):
        self.text, self.idioms, self.literal = text, idioms, literal
        self.groups = [g for _, g in idioms]


def _ipool(g):
    return [IS(*x) for x in ID[g]]


def id_meaning(r, g):
    pool = _ipool(g)
    tgt = r.choice([x for x in pool if x.idioms])
    grp = r.choice(tgt.groups)
    conds = [lambda x, grp=grp: grp in x.groups]
    txt = f"«{GROUPS[grp]}» mənasında frazeoloji birləşmə işlənib"
    if g != 9:
        k = len(tgt.idioms)
        if k == 2:
            conds.append(lambda x: len(x.idioms) == 2)
            txt += ", cümlədə daha bir frazeologizm var"
        else:
            conds.append(lambda x: len(x.idioms) == 1)
            txt += " və cümlədə başqa frazeologizm yoxdur"
    if g == 11:
        other = [gg for gg in tgt.groups if gg != grp]
        if other:
            conds.append(lambda x, o=other[0]: o in x.groups)
            txt += f" (ikincisi «{GROUPS[other[0]]}» mənasındadır)"
    res = near_miss(r, pool, conds, lambda x: x.text)
    if not res:
        return None
    opts, ok, ans = res
    return dict(t=f"Hansı cümlədə {txt}?", opts=opts, ok=ok, diff=dlevel(len(conds) + 1),
                e="Cümlədəki frazeologizmlər: " + "; ".join(f"«{i}» — {GROUPS[gg]}" for i, gg in ans.idioms) + ".")


def id_literal(r, g):
    pool = _ipool(g)
    kind = r.choice(["literal", "syn_pair", "none"])
    if kind == "literal":
        conds = [lambda x: not x.idioms, lambda x: x.literal]
        txt = "frazeologizm işlənməyib, lakin frazeologizmin tərkibindəki sözlər həqiqi mənada işlənib"
    elif kind == "syn_pair":
        conds = [lambda x: len(x.idioms) == 2, lambda x: len(set(x.groups)) == 1]
        txt = "iki frazeologizm işlənib və onlar mənaca bir-birinə yaxındır (sinonimdir)"
    else:
        conds = [lambda x: len(x.idioms) == 2, lambda x: len(set(x.groups)) == 2]
        txt = "iki frazeologizm işlənib və onlar müxtəlif mənalıdır"
    res = near_miss(r, pool, conds, lambda x: x.text)
    if not res:
        return None
    opts, ok, ans = res
    det = "; ".join(f"«{i}» — {GROUPS[gg]}" for i, gg in ans.idioms) or "frazeologizm yoxdur, sözlər həqiqi mənadadır"
    return dict(t=f"Hansı cümlədə {txt}?", opts=opts, ok=ok, diff="hard", e=f"Düzgün cümlədə: {det}.")


def id_label(r, g):
    """Cümlə + göstərilmiş məna. Şərt: göstərilən frazeologizm cümlədə var və mənası düzgündür."""
    pool = [x for x in _ipool(g) if x.idioms]
    items = []
    for x in pool:
        for idm, grp in x.idioms:
            for lab in r.sample(list(GROUPS), 3) + [grp]:
                items.append((x, idm, lab))
    conds = [lambda it: dict((i, gg) for i, gg in it[0].idioms)[it[1]] == it[2]]
    if g == 11:
        conds.append(lambda it: len(it[0].idioms) == 2)
    rend = lambda it: f"{it[0].text} («{it[1]}» — {GROUPS[it[2]]})"
    res = near_miss(r, items, conds, rend)
    if not res:
        return None
    opts, ok, ans = res
    t = "Hansı variantda cümlədəki frazeoloji birləşmənin mənası düzgün izah olunub"
    if g == 11:
        t += " və həmin cümlədə iki frazeologizm işlənib"
    return dict(t=t + "?", opts=opts, ok=ok, diff=dlevel(len(conds) + 1), e=f"«{ans[1]}» — {GROUPS[ans[2]]}.")


LEX_TOPICS = {
    "aze-syn": {9: [lex_presence, lex_label], 10: [lex_presence, lex_label], 11: [lex_presence, lex_label]},
    "aze-idiom": {9: [id_meaning, id_literal, id_label], 10: [id_meaning, id_literal, id_label], 11: [id_meaning, id_literal, id_label]},
}
