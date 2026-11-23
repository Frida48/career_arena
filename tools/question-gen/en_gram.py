"""İngilis dili · Grammar: 10 mövzu. Bəndlər (Gap) qaydalarla qurulur və ya əl ilə seçilib.
Səviyyə (lvl): 1 — əsas, 2 — çətin, 3 — çox çətin. 9-cu sinif: 1–2, 10-cu: 1–3, 11-ci: 2–3."""
from en_core import Gap, ZERO, topic

# ---------------- feil cədvəli ----------------
V = {v[0]: v for v in [
    ("write", "wrote", "written", "writing", "writes"), ("cook", "cooked", "cooked", "cooking", "cooks"),
    ("clean", "cleaned", "cleaned", "cleaning", "cleans"), ("watch", "watched", "watched", "watching", "watches"),
    ("paint", "painted", "painted", "painting", "paints"), ("repair", "repaired", "repaired", "repairing", "repairs"),
    ("buy", "bought", "bought", "buying", "buys"), ("finish", "finished", "finished", "finishing", "finishes"),
    ("send", "sent", "sent", "sending", "sends"), ("wash", "washed", "washed", "washing", "washes"),
    ("plant", "planted", "planted", "planting", "plants"), ("translate", "translated", "translated", "translating", "translates"),
    ("design", "designed", "designed", "designing", "designs"), ("read", "read", "read", "reading", "reads"),
    ("visit", "visited", "visited", "visiting", "visits"), ("build", "built", "built", "building", "builds"),
    ("teach", "taught", "taught", "teaching", "teaches"), ("sell", "sold", "sold", "selling", "sells"),
    ("make", "made", "made", "making", "makes"), ("take", "took", "taken", "taking", "takes"),
    ("study", "studied", "studied", "studying", "studies"), ("pass", "passed", "passed", "passing", "passes"),
    ("leave", "left", "left", "leaving", "leaves"), ("catch", "caught", "caught", "catching", "catches"),
    ("have", "had", "had", "having", "has"), ("save", "saved", "saved", "saving", "saves"),
    ("win", "won", "won", "winning", "wins"), ("lose", "lost", "lost", "losing", "loses"),
    ("practise", "practised", "practised", "practising", "practises"), ("feed", "fed", "fed", "feeding", "feeds"),
    ("steal", "stole", "stolen", "stealing", "steals"), ("choose", "chose", "chosen", "choosing", "chooses"),
    ("grow", "grew", "grown", "growing", "grows"), ("publish", "published", "published", "publishing", "publishes"),
    ("deliver", "delivered", "delivered", "delivering", "delivers"), ("sign", "signed", "signed", "signing", "signs"),
    ("check", "checked", "checked", "checking", "checks"), ("invite", "invited", "invited", "inviting", "invites"),
]}
SUBJ = [("I", "1", "I"), ("She", "3", "she"), ("He", "3", "he"), ("We", "p", "we"), ("They", "p", "they"),
        ("My brother", "3", "he"), ("The students", "p", "they"), ("Our neighbours", "p", "they")]
OBJ = [("write", "a long letter"), ("cook", "dinner"), ("clean", "the kitchen"), ("watch", "a documentary"),
       ("paint", "the fence"), ("repair", "the old bike"), ("buy", "a new laptop"), ("finish", "the project"),
       ("wash", "the dishes"), ("plant", "trees in the garden"), ("translate", "the article"), ("design", "a poster"),
       ("read", "the report"), ("visit", "the museum"), ("teach", "the younger kids"), ("study", "for the exam")]


def _be(p, past=False):
    return ("were" if p == "p" else "was") if past else {"1": "am", "3": "is", "p": "are"}[p]


def _have(p):
    return "has" if p == "3" else "have"


def form(v, t, p):
    b, pa, pp, ing, s3 = V[v]
    return {
        "ps": s3 if p == "3" else b, "pc": f"{_be(p)} {ing}", "past": pa, "pastc": f"{_be(p, True)} {ing}",
        "pp": f"{_have(p)} {pp}", "ppc": f"{_have(p)} been {ing}", "pastp": f"had {pp}", "fut": f"will {b}",
        "futc": f"will be {ing}", "futp": f"will have {pp}",
    }[t]


TENSE_FRAMES = [  # (çərçivə, düzgün zaman, səhv zamanlar, qayda, səviyyə)
    ("Look! {S} ___ ({v}) {o} right now.", "pc", ["ps", "pp", "past"], "Present Continuous: «right now», «Look!»", 1),
    ("{S} ___ ({v}) {o} two days ago.", "past", ["pp", "ps", "fut"], "Past Simple: «ago» ilə", 1),
    ("Every Sunday {s0} ___ ({v}) {o}; it is a family tradition.", "ps", ["pastc", "pastp", "futp"], "Present Simple: müntəzəm adət (Every Sunday … it is a tradition)", 1),
    ("{S} ___ ({v}) {o} three times since January.", "pp", ["past", "ps", "pc"], "Present Perfect: «since» + təkrar sayı", 2),
    ("{S} ___ ({v}) {o} when the lights suddenly went out.", "pastc", ["pc", "pp", "futc", "ps"], "Past Continuous: kəsilən proses", 2),
    ("By the time we arrived, {s} had already ___ ({v}) {o}.", "PP", ["PAST_BARE", "ING"], "Past Perfect: had + V3", 2),
    ("By the time we arrived, {s} ___ ({v}) {o}.", "pastp", ["pp", "futp", "ps"], "Past Perfect: «by the time» + keçmiş", 3),
    ("By next July, {s} ___ ({v}) {o}.", "futp", ["pp", "pastp", "past"], "Future Perfect: «by next July»", 3),
    ("This time tomorrow, {s} ___ ({v}) {o}.", "futc", ["pastc", "ppc", "past", "pastp"], "Future Continuous: «this time tomorrow»", 3),
    ("{S} ___ ({v}) {o} for two hours, and {s} still hasn't finished.", "ppc", ["pastc", "pc", "past"], "Present Perfect Continuous: davam edən proses", 3),
]


def _tense_items():
    out = []
    for fr, ok, bads, why, lvl in TENSE_FRAMES:
        for S, p, s in SUBJ:
            for v, o in OBJ:
                if "still hasn't" in fr and p != "3":
                    continue  # «hasn't» III şəxs təki tələb edir
                if fr.startswith("By the time we arrived") and S == "We":
                    continue
                txt = fr.replace("{S}", S).replace("{s}", s if S != "I" else "I").replace("{v}", v).replace("{o}", o)
                txt = txt.replace("{s0}", S if S == "I" else S[0].lower() + S[1:])
                if ok == "PP":
                    if V[v][0] == V[v][2]:
                        continue  # read/read/read: səhv forma düzgünlə üst-üstə düşür
                    out.append(Gap(txt, V[v][2], [V[v][1] if V[v][1] != V[v][2] else V[v][0], V[v][3]], why, lvl))
                    continue
                out.append(Gap(txt, form(v, ok, p), [form(v, b, p) for b in bads], why, lvl))
    # zaman budaq cümləsində gələcək əvəzinə Present Simple
    for v, o in OBJ:
        out.append(Gap(f"I will call you as soon as I ___ ({v}) {o}.", V[v][0], [f"will {V[v][0]}", f"would {V[v][0]}", f"to {V[v][0]}"],
                       "Zaman budaq cümləsində (as soon as, when) gələcək Present Simple ilə ifadə olunur", 2))
    return out


TENSES = _tense_items()

# ---------------- Conditionals ----------------
COND = [("you", "study", "harder", "pass", "the exam"), ("we", "leave", "now", "catch", "the train"),
        ("she", "practise", "every day", "win", "the competition"), ("they", "save", "enough money", "buy", "a new house"),
        ("he", "check", "the figures", "find", "the mistake"), ("I", "have", "more time", "visit", "my grandparents")]
FINDV = {"find": ("find", "found", "found"), "visit": ("visit", "visited", "visited"), "pass": ("pass", "passed", "passed"),
         "catch": ("catch", "caught", "caught"), "win": ("win", "won", "won"), "buy": ("buy", "bought", "bought")}


def _s3(v, s):
    return V[v][4] if s in ("she", "he") else V[v][0]


def _cond_items():
    out = []
    for s, v1, o1, v2, o2 in COND:
        b2, pa2, pp2 = FINDV[v2]
        S = s[0].upper() + s[1:] if s != "I" else "I"
        # I tip — şərt hissəsində boşluq
        out.append(Gap(f"If {s} ___ ({v1}) {o1}, {s} will {b2} {o2}.", _s3(v1, s), [f"will {V[v1][0]}", V[v1][1] if V[v1][1] != _s3(v1, s) else f"had {V[v1][2]}", f"had {V[v1][2]}"],
                       "I tip şərt: If + Present Simple, will + V1", 1))
        out.append(Gap(f"Unless {s} ___ ({v1}) {o1}, {s} won't {b2} {o2}.", _s3(v1, s),
                       [f"will {V[v1][0]}", f"won't {V[v1][0]}", f"would {V[v1][0]}"],
                       "Unless = if not; zaman/şərt hissəsində Present Simple", 2))
        # II tip
        out.append(Gap(f"If {s} ___ ({v1}) {o1}, {s} would {b2} {o2}.", V[v1][1],
                       [_s3(v1, s), f"will {V[v1][0]}", f"{_have(('3' if s in ('she', 'he') else 'p'))} {V[v1][2]}"],
                       "II tip şərt: If + Past Simple, would + V1", 2))
        # III tip
        out.append(Gap(f"If {s} had {V[v1][2]} {o1}, {s} ___ ({b2}) {o2}.", f"would have {pp2}",
                       [f"will {b2}", f"had {pp2}", f"will have {pp2}"], "III tip şərt: If + Past Perfect, would have + V3", 2))
        out.append(Gap(f"If {s} ___ ({v1}) {o1}, {s} would have {pp2} {o2}.", f"had {V[v1][2]}",
                       [f"would have {V[v1][2]}", f"have {V[v1][2]}", f"will have {V[v1][2]}"], "III tip şərt: şərt hissəsində Past Perfect", 3))
    zero = [("If you heat ice, it ___.", "melts", ["will melted", "is melt", "melting"]),
            ("If water reaches 100°C, it ___.", "boils", ["boil", "is boil", "boiling"]),
            ("If you mix red and blue, you ___ purple.", "get", ["gets", "getting", "got to"]),
            ("If plants don't get water, they ___.", "die", ["dies", "dying", "are die"])]
    out += [Gap(f, a, b, "Sıfır tip şərt: ümumi həqiqət, hər iki hissədə Present Simple", 1) for f, a, b in zero]
    wish = [("I wish I ___ the answer to this question. (know)", "knew", ["know", "will know", "knowing"], "wish + Past Simple: indiki vəziyyətə təəssüf", 2),
            ("She wishes she ___ to the party last night. (go)", "had gone", ["went", "goes", "has gone"], "wish + Past Perfect: keçmişə təəssüf", 3),
            ("I wish it ___ raining. It has been raining for days. (stop)", "would stop", ["stops", "stopped to", "will stop"], "wish + would: başqasının hərəkətinin dəyişməsini arzu", 3),
            ("If only I ___ more carefully yesterday! (drive)", "had driven", ["drove", "have driven", "drive"], "If only + Past Perfect: keçmişə təəssüf", 3),
            ("I wish I ___ taller. (be)", "were", ["am", "will be", "being"], "wish + were (bütün şəxslərdə)", 2)]
    out += [Gap(*w) for w in wish]
    mixed = [("If she had studied medicine, she ___ a doctor now. (be)", "would be", ["will be", "had been", "is"], "Qarışıq şərt: keçmiş şərt, indiki nəticə", 3),
             ("If I ___ afraid of flying, I would have visited you last summer. (not be)", "weren't", ["wasn't been", "am not", "won't be"], "Qarışıq şərt: indiki şərt (were), keçmiş nəticə", 3),
             ("If he had taken the medicine, he ___ ill now. (not feel)", "wouldn't feel", ["won't feel", "doesn't feel", "hadn't felt"], "Qarışıq şərt: keçmiş şərt → indiki nəticə", 3),
             ("Had I known about the meeting, I ___ it. (attend)", "would have attended", ["will attend", "had attended", "attended"], "İnversiya: Had I known = If I had known", 3),
             ("Should you need any help, ___ me. (call)", "call", ["calling", "to call", "called"], "İnversiya: Should you need = If you need; əmr", 3)]
    out += [Gap(*m) for m in mixed]
    return out


CONDS = _cond_items()

# ---------------- Passive ----------------
POBJ = [("bridge", "s", "build"), ("houses", "p", "paint"), ("letters", "p", "send"), ("report", "s", "publish"), ("article", "s", "translate"),
        ("posters", "p", "design"), ("bikes", "p", "repair"), ("parcel", "s", "deliver"), ("contract", "s", "sign"), ("cars", "p", "sell")]


def _passive_items():
    out = []
    for n, num, v in POBJ:
        b, pa, pp, ing, s3 = V[v]
        be, was, has = ("is", "was", "has") if num == "s" else ("are", "were", "have")
        N = f"The {n}"
        out.append(Gap(f"{N} ___ ({v}) in 2015.", f"{was} {pp}", [pp, f"{has} been {pp}", f"{be} {pp}", f"{was} {ing}"], "Past Simple Passive: was/were + V3", 1))
        out.append(Gap(f"{N} ___ ({v}) since 2010.", f"{has} been {pp}", [f"{was} {pp}", f"{be} {pp}", f"{has} {pp}"], "Present Perfect Passive: has/have been + V3", 2))
        out.append(Gap(f"{N} ___ ({v}) at the moment.", f"{be} being {pp}", [f"{be} {ing}", f"{has} been {ing}", f"{was} being {pp}"], "Present Continuous Passive: is/are being + V3", 2))
        out.append(Gap(f"{N} must ___ ({v}) before Friday.", f"be {pp}", [f"been {pp}", pp, f"being {pp}"], "Modal + be + V3", 1))
        out.append(Gap(f"{N} ___ ({v}) by the end of next week.", f"will have been {pp}", [f"{has} been {pp}", f"had been {pp}", f"will have {pp}"],
                       "Future Perfect Passive: will have been + V3", 3))
        out.append(Gap(f"{N} ___ ({v}) when the storm started.", f"{was} being {pp}", [f"{be} being {pp}", f"{was} {ing}", f"{has} been {pp}"],
                       "Past Continuous Passive: was/were being + V3", 3))
    extra = [("He is said ___ the best player in the team.", "to be", ["being", "be", "that is"], "be said + to-infinitive", 3),
             ("The thief is believed ___ the country last week.", "to have left", ["to leave", "leaving", "to be left"], "Keçmişə aid: be believed + to have + V3", 3),
             ("I had my car ___ yesterday. (repair)", "repaired", ["repair", "repairing", "to repair"], "Causative: have + obyekt + V3", 3),
             ("She got her hair ___ last week. (cut)", "cut", ["to cut", "cutting", "cuts"], "Causative: get + obyekt + V3", 2),
             ("The windows need ___. (clean)", "cleaning", ["to clean", "cleaned", "clean"], "need + -ing (məchul məna)", 3),
             ("This problem can't ___ easily. (solve)", "be solved", ["solved", "been solved", "be solving"], "Modal + be + V3", 2)]
    out += [Gap(*e) for e in extra]
    return out


PASSIVE = _passive_items()

# ---------------- Articles ----------------
ART = [
    ("She is ___ honest person.", "an", ["a"], "«honest» saitlə tələffüz olunur (h oxunmur) → an", 1),
    ("He works at ___ university in Baku.", "a", ["an"], "«university» [ju] səsi ilə başlayır → a", 1),
    ("We waited for ___ hour.", "an", ["a"], "«hour»da h oxunmur → an", 1),
    ("I bought ___ one-way ticket.", "a", ["an"], "«one» [w] səsi ilə başlayır → a", 2),
    ("It was ___ unusual decision.", "an", ["a"], "«unusual» sait səsi ilə başlayır → an", 1),
    ("She has ___ MBA from a famous school.", "an", ["a"], "«MBA» [em] səsi ilə başlayır → an", 3),
    ("Germany is ___ European country.", "a", ["an"], "«European» [ju] səsi ilə başlayır → a", 2),
    ("They play ___ football every Saturday.", ZERO, ["the", "a"], "İdman növləri ilə artikl işlənmir", 1),
    ("___ Nile is the longest river in Africa.", "The", [ZERO, "A"], "Çay adları ilə the", 1),
    ("___ Mount Everest is the highest mountain in the world.", ZERO, ["The", "A"], "Tək dağ adları ilə artikl işlənmir", 2),
    ("We sailed across ___ Pacific Ocean.", "the", [ZERO, "a"], "Okean adları ilə the", 1),
    ("She lives in ___ United Kingdom.", "the", [ZERO, "a"], "«Kingdom, States, Republic» olan ölkə adları ilə the", 2),
    ("My cousin lives in ___ Azerbaijan.", ZERO, ["the", "an"], "Əksər ölkə adları ilə artikl işlənmir", 1),
    ("We went there by ___ bus.", ZERO, ["a", "an"], "by + nəqliyyat vasitəsi: artikl yoxdur", 1),
    ("___ sun rises in the east.", "The", ["A", ZERO], "Yeganə obyektlər: the sun, the moon", 1),
    ("I visit my grandparents twice ___ month.", "a", ["the", ZERO], "twice a month — «hər» mənasında a", 2),
    ("We have ___ breakfast at seven.", ZERO, ["a", "an"], "Yemək adları ilə (breakfast, lunch) artikl işlənmir", 1),
    ("This is ___ most interesting book I have ever read.", "the", [ZERO, "an"], "Üstünlük dərəcəsi ilə the", 1),
    ("He speaks ___ English fluently.", ZERO, ["the", "an"], "Dil adları ilə artikl işlənmir", 1),
    ("___ English language has many irregular verbs.", "The", [ZERO, "An"], "«the English language» — language sözü ilə the", 2),
    ("___ rich should help the poor.", "The", [ZERO, "A"], "the + sifət = sosial qrup (the rich, the poor)", 2),
    ("He was born in ___ 1990s.", "the", [ZERO, "a"], "Onilliklər: in the 1990s", 2),
    ("She goes to ___ bed at ten o'clock.", ZERO, ["a", "an"], "go to bed — sabit ifadə, artiklsiz", 1),
    ("___ Caspian Sea is the largest lake in the world.", "The", [ZERO, "A"], "Dəniz adları ilə the", 2),
    ("___ Lake Baikal is very deep.", ZERO, ["The", "A"], "«Lake + ad» formasında artikl işlənmir", 3),
    ("___ history is my favourite subject.", ZERO, ["The", "A"], "Fənn adları ümumi mənada artiklsiz", 2),
    ("I'd like ___ glass of water, please.", "a", ["an", ZERO], "Saylan tək isimlə ilk dəfə: a", 1),
    ("What ___ beautiful day it is!", "a", ["the", ZERO], "What a + saylan tək isim (nida)", 2),
    ("What ___ lovely weather we are having!", ZERO, ["a", "the"], "What + saylanmayan isim (weather) — artiklsiz", 3),
    ("She is ___ only person who knows the truth.", "the", ["an", "a"], "«only» ilə the", 2),
    ("He became ___ engineer after graduating.", "an", ["a", ZERO], "Peşə bildirəndə: an engineer", 1),
    ("___ Netherlands is famous for its tulips.", "The", [ZERO, "A"], "Cəm formalı ölkə adları ilə the", 2),
    ("They climbed ___ Alps last summer.", "the", [ZERO, "an"], "Dağ silsilələri ilə the", 2),
    ("He has ___ unique talent for music.", "a", ["an"], "«unique» [ju] səsi ilə başlayır → a", 3),
    ("It's ___ honour to meet you.", "an", ["a", ZERO], "«honour»da h oxunmur → an", 3),
    ("He was elected ___ president of the club.", ZERO, ["a", "an"], "Yeganə vəzifə «elect» ilə — artiklsiz", 3),
]
ARTICLES = [Gap(*a) for a in ART]

# ---------------- Quantifiers ----------------
QNT = [
    ("There isn't ___ milk left in the fridge.", "much", ["many", "a few", "few"], "much + saylanmayan isim (inkarda)", 1),
    ("How ___ students are there in your class?", "many", ["much", "little", "a little"], "many + saylan cəm isim", 1),
    ("I have ___ money, so I can buy you a coffee.", "a little", ["a few", "few", "many"], "a little + saylanmayan (müsbət məna: bir az var)", 2),
    ("She has ___ friends, so she often feels lonely.", "few", ["little", "a little", "much"], "few + saylan (mənfi məna: az, demək olar ki, yox)", 2),
    ("We have ___ time; we must hurry.", "little", ["few", "a few", "many"], "little + saylanmayan (mənfi məna)", 2),
    ("___ student in the class received a certificate.", "Each", ["All", "Both", "Many"], "each/every + saylan tək isim", 1),
    ("___ of my parents are doctors.", "Both", ["Every", "Much"], "both of + cəm, cəm feil (are)", 2),
    ("___ of the two answers is correct, so try again.", "Neither", ["Both", "All"], "neither of (ikisindən heç biri) + tək feil (is)", 3),
    ("You can take ___ road; both lead to the city centre.", "either", ["both", "all"], "either + tək isim: ikisindən hər hansı biri", 2),
    ("___ of the students passed the test; it was too difficult.", "None", ["Nobody", "No", "Any"], "none of + cəm (üç və daha çox): heç biri", 3),
    ("There are ___ apples in the basket.", "some", ["any", "much", "a little"], "Təsdiq cümləsində some", 1),
    ("Are there ___ questions?", "any", ["much", "a little", "a few of"], "Sual cümləsində any", 1),
    ("He spends ___ deal of time reading.", "a great", ["a large", "a lot", "many"], "a great deal of + saylanmayan", 3),
    ("___ number of tourists has increased this year.", "The", ["A", ZERO, "Many"], "the number of + tək feil (has)", 3),
    ("___ number of tourists have complained about the hotel.", "A", ["The", ZERO, "Much"], "a number of (bir neçə) + cəm feil (have)", 3),
    ("I don't have ___ information about this topic.", "much", ["many", "a few", "few"], "information saylanmayandır → much", 2),
    ("She gave me ___ useful advice.", "some", ["an", "a few", "many"], "advice saylanmayandır → some advice", 2),
    ("___ child needs love and attention.", "Every", ["All", "Both", "Several"], "every + tək isim", 1),
    ("___ the children enjoyed the trip.", "All", ["Every", "Each", "Either"], "all (of) the + cəm", 2),
    ("There were ___ people at the concert that we couldn't find a seat.", "so many", ["so much", "such many", "too much"], "so many + saylan cəm", 3),
    ("It was ___ a long journey that we were exhausted.", "such", ["so", "too", "very"], "such + (a) + sifət + isim", 2),
    ("We bought ___ furniture for the new flat.", "some", ["a few", "many", "several"], "furniture saylanmayandır → some", 2),
    ("___ of the cakes is mine; take the other one.", "One", ["Both", "All", "Some"], "one of + cəm isim + tək feil", 2),
    ("He hardly has ___ free time these days.", "any", ["some", "many", "no"], "hardly (inkar mənalı) + any", 3),
    ("I've got ___ homework to do tonight.", "a lot of", ["many", "a few", "several"], "homework saylanmayandır → a lot of / much", 2),
    ("Only ___ students came to the lecture, so it was cancelled.", "a few", ["a little", "much", "little"], "only a few + saylan cəm", 2),
    ("There's hardly ___ sugar left.", "any", ["some", "many", "few"], "hardly any — demək olar ki, heç", 3),
    ("___ luggage do you have?", "How much", ["How many", "How few", "How a lot"], "luggage saylanmayandır → how much", 2),
    ("Plenty ___ volunteers came to help.", "of", ["much", "many", ZERO], "plenty of + isim", 3),
    ("We had ___ problems with the new software.", "several", ["much", "a little", "a great deal"], "several + saylan cəm", 2),
]
QUANT = [Gap(*q) for q in QNT]

# ---------------- Nouns ----------------
PLURAL = [("child", "children", ["childs", "childrens"]), ("mouse", "mice", ["mouses", "mices"]), ("tooth", "teeth", ["tooths", "teeths"]),
          ("woman", "women", ["womans", "womens"]), ("knife", "knives", ["knifes", "knive"]), ("potato", "potatoes", ["potatos", "potatoe"]),
          ("criterion", "criteria", ["criterions", "criterias"]), ("phenomenon", "phenomena", ["phenomenons", "phenomenas"]),
          ("analysis", "analyses", ["analysises", "analysis"]), ("crisis", "crises", ["crisises", "crisis"]), ("sheep", "sheep", ["sheeps", "sheepes"]),
          ("foot", "feet", ["foots", "feets"]), ("city", "cities", ["citys", "cityes"]), ("roof", "roofs", ["roofes", "roofies"]),
          ("hero", "heroes", ["heros", "heroies"]), ("leaf", "leaves", ["leafs", "leavs"]), 
          ("passer-by", "passers-by", ["passer-bys", "passers-bys"]), ("mother-in-law", "mothers-in-law", ["mother-in-laws", "mothers-in-laws"]),
          ("goose", "geese", ["gooses", "geeses"])]


def _noun_items():
    out = []
    for i, (sg, pl, bad) in enumerate(PLURAL):
        lvl = 3 if sg in ("criterion", "phenomenon", "analysis", "crisis", "passer-by", "mother-in-law") else (1 if i < 8 else 2)
        fr = (f"The report mentions three ___ ({sg})." if sg in ("criterion", "phenomenon", "analysis", "crisis")
              else f"There were three ___ ({sg}) in the picture.")
        out.append(Gap(fr, pl, bad, f"{sg} → {pl}", lvl))
    cur = [
        ("Can you give me some ___ about the course?", "information", ["informations", "an information", "information's"], "information saylanmayandır, cəmi yoxdur", 1),
        ("The ___ on TV was very bad today.", "news", ["new", "newses", "news'"], "news tək sayılır (the news was)", 2),
        ("The news ___ shocking.", "was", ["were", "are", "have been"], "news + tək feil", 2),
        ("Mathematics ___ my favourite subject.", "is", ["are", "were", "have been"], "Mathematics, physics, economics + tək feil", 2),
        ("The police ___ looking for the missing boy.", "are", ["is", "was", "has"], "police həmişə cəm feillə", 3),
        ("My jeans ___ too tight.", "are", ["is", "was", "has"], "jeans, trousers, scissors — cəm isim", 2),
        ("He gave me a useful piece of ___.", "advice", ["advices", "advise", "an advice"], "a piece of advice — advice saylanmayan", 2),
        ("We need new ___ for the office.", "furniture", ["furnitures", "a furniture", "furniture's"], "furniture saylanmayandır", 2),
        ("She has a ten-___-old son.", "year", ["years", "year's", "yearly"], "Mürəkkəb sifətdə isim tək olur: a ten-year-old", 3),
        ("It was a three-___ journey.", "hour", ["hours", "hour's", "hourly"], "a three-hour journey — tək forma", 3),
        ("This is the ___ room. (girls — bir neçə qız)", "girls'", ["girl's", "girls's", "girls"], "Cəm -s ilə bitəndə yiyəlik: girls'", 3),
        ("These are the ___ toys. (children)", "children's", ["childrens'", "childrens", "children'"], "Qeyri-adi cəmdə yiyəlik: children's", 2),
        ("My ___ car is very old. (parents)", "parents'", ["parent's's", "parents", "parentses'"], "Cəm -s ilə: parents'", 2),
        ("The ___ are grazing in the field. (cattle)", "cattle", ["cattles", "cattle's", "cattlees"], "cattle həmişə cəm, -s qəbul etmir", 3),
        ("I bought two ___ of bread.", "loaves", ["loafs", "loaf", "loaves'"], "loaf → loaves", 2),
        ("Our ___ was lost at the airport.", "luggage", ["luggages", "a luggage", "luggage's"], "luggage saylanmayandır", 2),
        ("The scissors ___ on the table.", "are", ["is", "was", "has been"], "scissors cəm feillə", 2),
        ("Each of the ___ has a different colour. (box)", "boxes", ["boxs", "box", "boxies"], "-x ilə bitən: boxes", 1),
        ("There are many ___ on the farm. (fish)", "fish", ["fishs", "fishes'", "fishies"], "fish (eyni növ) cəmdə dəyişmir", 2),
        ("Scientists have discovered two new ___ of birds. (species)", "species", ["specie", "specieses", "species'"], "species tək və cəmdə eynidir", 3),
    ]
    out += [Gap(*c) for c in cur]
    return out


NOUNS = _noun_items()

# ---------------- Adjectives ----------------
COMP = [  # (sifət, müqayisə, üstünlük, səhv müq., səhv üst., müqayisə cümləsi, üstünlük cümləsi)
    ("good", "better", "best", ["gooder", "more better"], ["goodest", "most best"], "This plan is ___ (good) than the first one.", "It is the ___ (good) plan we have."),
    ("bad", "worse", "worst", ["badder", "more worse"], ["baddest", "worstest"], "The weather today is ___ (bad) than yesterday.", "It was the ___ (bad) storm in ten years."),
    ("big", "bigger", "biggest", ["biger", "more big"], ["bigest", "most big"], "Their new flat is ___ (big) than the old one.", "It is the ___ (big) flat in the building."),
    ("happy", "happier", "happiest", ["happyer", "more happier"], ["happyest", "most happiest"], "My sister looks ___ (happy) than before.", "She is the ___ (happy) girl in the class."),
    ("careful", "more careful", "most careful", ["carefuler", "more carefuller"], ["carefulest", "most carefullest"], "Leyla is ___ (careful) than her brother.", "He is the ___ (careful) driver I know."),
    ("difficult", "more difficult", "most difficult", ["difficulter", "more difficulter"], ["difficultest", "most difficultest"], "This test is ___ (difficult) than the last one.", "It was the ___ (difficult) question in the exam."),
    ("thin", "thinner", "thinnest", ["thiner", "more thin"], ["thinest", "most thin"], "This book is ___ (thin) than that one.", "It is the ___ (thin) book on the shelf."),
    ("busy", "busier", "busiest", ["busyer", "more busier"], ["busyest", "most busier"], "This street is ___ (busy) than ours.", "It is the ___ (busy) street in the city."),
    ("modern", "more modern", "most modern", ["moderner", "more moderner"], ["modernest", "most modernest"], "Their office is ___ (modern) than ours.", "It is the ___ (modern) office in the area."),
    ("dry", "drier", "driest", ["dryier", "more drier"], ["dryest", "most driest"], "This summer was ___ (dry) than last summer.", "It was the ___ (dry) month of the year."),
]


def _adj_items():
    out = []
    for i, (a, c, s_, bc, bs, f1, f2) in enumerate(COMP):
        out.append(Gap(f1, c, bc + [s_], f"Müqayisə dərəcəsi: {a} → {c}", 1 if i < 5 else 2))
        out.append(Gap(f2, s_, bs + [c], f"Üstünlük dərəcəsi: {a} → the {s_}", 1 if i < 5 else 2))
        out.append(Gap(f1.replace(" ___", " much ___", 1), c, [f"very {c}", f"more {s_}" if not s_.startswith("most") else f"more {a}er", s_],
                       "much/far + müqayisə dərəcəsi (very işlənmir)", 3))
    cur = [
        ("She bought a ___ dress.", "beautiful long red silk", ["long beautiful red silk", "red beautiful long silk", "beautiful silk long red"],
         "Sifət sırası: rəy – ölçü – rəng – material", 3),
        ("They live in a ___ house.", "lovely old stone", ["old lovely stone", "stone lovely old", "lovely stone old"], "Sifət sırası: rəy – yaş – material", 2),
        ("He has a ___ car.", "small black Japanese", ["black small Japanese", "Japanese small black", "small Japanese black"], "Sifət sırası: ölçü – rəng – mənşə", 2),
        ("I found a ___ table at the market.", "round wooden dining", ["wooden round dining", "dining round wooden", "round dining wooden"], "Sifət sırası: forma – material – təyinat", 3),
        ("The film was so ___ that I fell asleep.", "boring", ["bored", "bore", "boringly"], "-ing: səbəb olan şey (film darıxdırıcıdır)", 1),
        ("I was ___ because the lesson was too long.", "bored", ["boring", "bore", "boredly"], "-ed: insanın hissi", 1),
        ("We were ___ by the news.", "shocked", ["shocking", "shock", "shockingly"], "-ed: hiss (be shocked by)", 2),
        ("He isn't old ___ to drive.", "enough", ["too", "so", "very"], "sifət + enough", 1),
        ("The box was ___ heavy for me to carry.", "too", ["enough", "so much", "very much"], "too + sifət + for + to-infinitive", 1),
        ("Your English is getting ___.", "better and better", ["more and more good", "best and best", "gooder and gooder"], "Artan dəyişiklik: comparative and comparative", 2),
        ("The more you read, the ___ you know.", "more", ["most", "much", "many"], "the + comparative ..., the + comparative", 2),
        ("This bag is not as expensive ___ that one.", "as", ["than", "like", "so"], "as ... as müqayisəsi", 1),
            ("It was the ___ film I have ever seen.", "worst", ["baddest", "worse", "most bad"], "bad → the worst", 1),
        ("For ___ information, please contact our office.", "further", ["farther", "farer", "furthest"], "further = əlavə (məlumat)", 3),
        ("My ___ brother is a pilot.", "elder", ["older than", "eldest than", "more old"], "elder — ailə üzvləri üçün atributiv", 3),
        ("She felt ___ after the long walk.", "tired", ["tiring", "tire", "tiredly"], "feel + sifət (-ed: hiss)", 1),
        ("It is getting ___ to find a cheap flat in the city.", "harder", ["more hard", "hardest", "most hard"], "hard → harder", 2),
    ]
    out += [Gap(*c) for c in cur]
    return out


ADJS = _adj_items()

# ---------------- Pronouns ----------------
PRN = [
    ("She made the cake ___.", "herself", ["himself", "her", "itself"], "Qayıdış əvəzliyi: she → herself", 1),
    ("The children enjoyed ___ at the party.", "themselves", ["theirselves", "themself", "themselfs"], "they → themselves", 1),
    ("This book is not yours; it's ___.", "mine", ["my", "me", "myself"], "Müstəqil yiyəlik əvəzliyi: mine", 1),
    ("Is this umbrella ___ or hers?", "yours", ["your", "you", "yourself"], "Müstəqil forma: yours", 1),
    ("The woman ___ car was stolen called the police.", "whose", ["who", "which", "whom"], "whose — yiyəlik bildirən nisbi əvəzlik", 2),
    ("The man ___ I spoke to was very helpful.", "whom", ["whose", "which", "what"], "whom — obyekt kimi şəxs (formal)", 3),
    ("This is the house ___ I was born in.", "which", ["who", "whose", "whom"], "Əşya üçün which", 1),
    ("The two friends looked at ___ and smiled.", "each other", ["theirselves", "each others", "itself"], "Qarşılıqlı: each other", 2),
    ("Between you and ___, I don't trust him.", "me", ["I", "my", "mine"], "Önlükdən sonra obyekt forması: me", 2),
    ("Neither of the girls brought ___ book.", "her", ["their own's", "hers", "herself"], "neither (tək) + her", 3),
    ("I don't like these shoes. Can I see the black ___?", "ones", ["it", "them"], "Cəm isim əvəzinə ones", 2),
    ("___ is raining heavily outside.", "It", ["There", "This", "That's"], "Hava ilə it", 1),
    ("___ are three books on the table.", "There", ["It", "Their", "This"], "Varlıq bildirmə: there are", 1),
    ("He hurt ___ while playing football.", "himself", ["hisself", "his", "he"], "Qayıdış əvəzliyi: he → himself", 1),
    ("We did the project by ___.", "ourselves", ["ourself", "we", "ours"], "by ourselves — öz-özümüzə", 2),
    ("A friend of ___ is coming to visit.", "mine", ["me", "my", "I"], "a friend of mine — müstəqil forma", 2),
    ("___ of them knew the answer, so the teacher explained it again.", "None", ["Nobody", "Nothing", "No"], "none of them — heç biri", 3),
    ("Everybody has done ___ homework.", "their", ["there", "they're", "theirs"], "everybody ilə their (cinsdən asılı olmayan forma)", 3),
    ("The company changed ___ logo last year.", "its", ["it's", "their's", "it"], "its — yiyəlik; it's = it is", 2),
    ("This is the place ___ we first met.", "where", ["which", "who", "whose"], "Yer bildirən nisbi zərf: where", 2),
    ("___ did you give the keys to?", "Who", ["Whose", "What's", "How"], "Sual: Who … to?", 2),
    ("The girl ___ is sitting next to me is my cousin.", "who", ["which", "whose", "whom"], "Şəxs mübtəda: who", 1),
    ("I have two brothers, both of ___ are engineers.", "whom", ["who", "them", "which"], "Önlükdən sonra şəxs üçün whom (both of whom)", 3),
    ("She bought a laptop, ___ was very expensive.", "which", ["that", "what", "who"], "Ayırıcı nisbi cümlədə that işlənmir → which", 3),
    ("___ you need is a good night's sleep.", "What", ["That", "Which", "Who"], "What = the thing that", 3),
    ("They blamed ___ for the mistake.", "themselves", ["theirselves", "themself", "their"], "Qayıdış: they → themselves", 2),
]
PRONOUNS = [Gap(*p) for p in PRN]

# ---------------- Numerals ----------------
NUM = [
    ("The stadium holds two ___ people.", "thousand", ["thousands", "thousand of", "thousands of"], "Dəqiq saydan sonra thousand tək qalır", 1),
    ("___ people watched the match online.", "Millions of", ["Million of", "Millions", "Million"], "Qeyri-müəyyən çoxluq: millions of", 2),
    ("We live on the ___ floor.", "twenty-first", ["twenty-oneth", "twentieth-first", "twenty-one"], "21 → twenty-first", 1),
    ("Her birthday is on the ___ of May.", "third", ["three", "threeth", "thirdth"], "Tarix: the third of May", 1),
    ("___ of the students are girls. (2/3)", "Two thirds", ["Two third", "Second thirds", "Two threes"], "Kəsr: two thirds (surət >1 olanda məxrəc cəm)", 2),
    ("The flight takes ___ hours.", "one and a half", ["one and half", "one half and", "a one and half"], "1,5: one and a half hours", 2),
    ("I need a ___ eggs for this cake.", "dozen", ["dozen of", "dozens", "dozens of"], "a dozen eggs (of olmadan)", 2),
    ("___ birds flew over the lake.", "Hundreds of", ["Hundred of", "Hundreds", "A hundreds of"], "Qeyri-müəyyən: hundreds of", 2),
    ("Please open your books at ___.", "page 25", ["the page 25", "25 page", "the 25 page"], "page + rəqəm, artiklsiz", 2),
    ("He came ___ in the race.", "second", ["two", "the two", "secondly"], "Sıra sayı: came second", 1),
    ("The ___ World War ended in 1945.", "Second", ["Two", "Twice", "Secondly"], "the Second World War", 2),
    ("Prices rose by 2.5 per cent — that is, two ___ five per cent.", "point", ["comma", "dot and", "and"], "Onluq kəsr: two point five", 3),
    ("It was a ___ walk.", "five-mile", ["five-miles", "five miles'", "fifth-mile"], "Mürəkkəb sifət: a five-mile walk", 3),
    ("This is the ___ time I have told you!", "hundredth", ["hundred", "hundreds", "hundredeth"], "100-cü: hundredth", 2),
    ("The ___ century began in 2001.", "twenty-first", ["twenty-one", "twentieth-one", "twenty-oneth"], "XXI əsr: the twenty-first century", 2),
    ("Three ___ of the cake were eaten. (3/4)", "quarters", ["quarter", "fourth", "four"], "three quarters", 2),
    ("The population is about seven ___. (7 000 000)", "million", ["millions", "million of", "millions of"], "seven million — rəqəmdən sonra tək", 1),
    ("She won ___ prize in the competition.", "first", ["the one", "one", "firstly"], "won first prize — artiklsiz sabit ifadə", 3),
    ("Can you count from one to ___? (12)", "twelve", ["twelfth", "twelveth", "twelfe"], "Miqdar sayı: twelve", 1),
    ("King Charles ___ became king in 2022. (III)", "the Third", ["Three", "the Three", "third the"], "Hökmdar adlarında sıra sayı: Charles the Third", 3),
    ("I've told you ___ times not to do that!", "dozens of", ["dozen", "a dozens", "dozens"], "Qeyri-müəyyən: dozens of times", 3),
    ("The meeting is on ___ floor.", "the ninth", ["ninth the", "the nineth", "nine"], "9 → ninth (e düşür)", 2),
    ("Water freezes at zero degrees ___.", "Celsius", ["Celsiuses", "of Celsius", "Celsius's"], "Temperatur: zero degrees Celsius", 3),
    ("Half ___ the class was absent.", "of", ["from", "in", "by"], "half of the class", 3),
]
NUMERALS = [Gap(*n) for n in NUM]

# ---------------- Adverbs ----------------
ADV = [
    ("She drives very ___.", "carefully", ["careful", "carefuly", "carefullly"], "Feili izah edən zərf: carefully", 1),
    ("He speaks English ___.", "well", ["good", "goodly", "nice"], "good (sifət) → well (zərf)", 1),
    ("He works ___ every day.", "hard", ["hardly", "hardy", "harder than"], "hard — zərf də olur; hardly = demək olar ki, yox", 2),
    ("I can ___ hear you; please speak louder.", "hardly", ["hard", "hardy", "hardily"], "hardly = demək olar ki, yox", 2),
    ("Have you seen any good films ___?", "lately", ["late", "latest", "lateness"], "lately = son vaxtlar", 2),
    ("He arrived ___ for the meeting.", "late", ["lately", "lates", "latish"], "late — zərf (gec)", 2),
    ("The car was moving very ___.", "fast", ["fastly", "fasted", "fastful"], "fast — zərf də fast", 1),
    ("She ___ late for school.", "is never", ["never is", "is ever", "never"], "Tezlik zərfi «be» feilindən sonra gəlir", 1),
    ("They ___ to the gym on Mondays.", "usually go", ["go usually", "usually goes", "goes usually"], "Tezlik zərfi əsas feildən əvvəl", 1),
    ("Have you finished your homework ___?", "yet", ["still", "since", "ever"], "Sualda yet (cümlənin sonunda)", 1),
    ("I have ___ finished; I can help you now.", "already", ["yet", "still", "ever"], "Təsdiqdə already (have ilə V3 arasında)", 1),
    ("She ___ lives with her parents.", "still", ["yet", "ever"], "still — hələ də (davam edən vəziyyət)", 2),
    ("He ran ___ than anyone else.", "faster", ["more fast", "fastlier", "more faster"], "fast → faster", 2),
    ("She answered the question ___ than I did.", "more confidently", ["confidentlier", "more confident", "most confidently"], "-ly zərfləri: more + zərf", 2),
    ("He ___ ever goes to the cinema.", "hardly", ["hard", "almost", "nearly"], "hardly ever = demək olar ki, heç vaxt", 3),
    ("The soup smells ___.", "delicious", ["deliciously", "delicious-ly", "more deliciously"], "Duyğu feilləri (smell, taste) + sifət", 3),
    ("She looked at me ___.", "angrily", ["angrilly", "angryly", "angerly"], "look at (hərəkət) + zərf", 3),
    ("He was ___ tired that he fell asleep at once.", "so", ["such", "too", "enough"], "so + sifət + that", 2),
    ("You are not working ___ to pass the exam.", "hard enough", ["enough hard", "hardly enough", "too hard"], "zərf + enough", 2),
    ("___ had I arrived when the phone rang.", "Hardly", ["Hard", "Already", "Lately"], "İnversiya: Hardly had I …", 3),
    ("Never ___ such a beautiful sunset.", "have I seen", ["I have seen", "I saw", "seen I have"], "Inkar zərfi əvvəldə → inversiya", 3),
    ("She sings ___ of all the students.", "the most beautifully", ["the most beautiful", "beautifullest", "more beautifully"], "Zərfin üstünlük dərəcəsi: the most + -ly", 3),
    ("We arrived ___ on time; the doors were closing.", "just", ["yet", "still", "lately"], "just — tam, ancaq", 3),
    ("He did ___ in the test.", "badly", ["bad", "badily", "worsely"], "bad (sifət) → badly (zərf)", 1),
    ("The children played ___ in the garden.", "happily", ["happy", "happyly", "happilly"], "happy → happily (y → i)", 1),
    ("She can ___ speak three languages.", "fluently", ["fluent", "fluentlly", "fluency"], "fluent → fluently", 2),
    ("I'll be there ___. Wait for me!", "soon", ["soonly", "soonest", "sooner than"], "soon — zaman zərfi", 2),
]
ADVERBS = [Gap(*a) for a in ADV]

GRAM_TOPICS = {
    "eng-tense": topic(TENSES),
    "eng-cond": topic(CONDS),
    "eng-passive": topic(PASSIVE),
    "eng-article": topic(ARTICLES, " (— = no article)"),
    "eng-quant": topic(QUANT, " (— = nothing)"),
    "eng-noun": topic(NOUNS),
    "eng-adj": topic(ADJS),
    "eng-pron": topic(PRONOUNS),
    "eng-num": topic(NUMERALS),
    "eng-adv": topic(ADVERBS),
}
