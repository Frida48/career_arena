"""İngilis dili: 7 mövzu × 3 sinif × 60 sual (orta-çətin).
Qrammatika sualları feil cədvəlindən qaydalarla qurulur; söz yaradıcılığı və frazal feillər bankdandır;
Main idea və Inference — orijinal mətnlər (en_passages.py)."""
from quiz import build_topic, build_fixed, save_grade, pick
from en_passages import PASSAGES

M, H = "medium", "hard"

# base, past, past participle, -ing, 3sg
V = {v[0]: v for v in [
    ("write", "wrote", "written", "writing", "writes"), ("go", "went", "gone", "going", "goes"),
    ("eat", "ate", "eaten", "eating", "eats"), ("see", "saw", "seen", "seeing", "sees"), ("take", "took", "taken", "taking", "takes"),
    ("make", "made", "made", "making", "makes"), ("buy", "bought", "bought", "buying", "buys"),
    ("finish", "finished", "finished", "finishing", "finishes"), ("visit", "visited", "visited", "visiting", "visits"),
    ("study", "studied", "studied", "studying", "studies"), ("play", "played", "played", "playing", "plays"),
    ("watch", "watched", "watched", "watching", "watches"), ("clean", "cleaned", "cleaned", "cleaning", "cleans"),
    ("cook", "cooked", "cooked", "cooking", "cooks"), ("swim", "swam", "swum", "swimming", "swims"),
    ("drive", "drove", "driven", "driving", "drives"), ("give", "gave", "given", "giving", "gives"),
    ("speak", "spoke", "spoken", "speaking", "speaks"), ("build", "built", "built", "building", "builds"),
    ("break", "broke", "broken", "breaking", "breaks"), ("send", "sent", "sent", "sending", "sends"),
    ("lose", "lost", "lost", "losing", "loses"), ("win", "won", "won", "winning", "wins"), ("paint", "painted", "painted", "painting", "paints"),
    ("repair", "repaired", "repaired", "repairing", "repairs"), ("plant", "planted", "planted", "planting", "plants"),
    ("open", "opened", "opened", "opening", "opens"), ("wash", "washed", "washed", "washing", "washes"),
    ("teach", "taught", "taught", "teaching", "teaches"), ("catch", "caught", "caught", "catching", "catches"),
    ("find", "found", "found", "finding", "finds"), ("sell", "sold", "sold", "selling", "sells"), ("tell", "told", "told", "telling", "tells"),
    ("bring", "brought", "brought", "bringing", "brings"), ("sing", "sang", "sung", "singing", "sings"),
    ("drink", "drank", "drunk", "drinking", "drinks"), ("leave", "left", "left", "leaving", "leaves"), ("have", "had", "had", "having", "has"),
    ("know", "knew", "known", "knowing", "knows"), ("save", "saved", "saved", "saving", "saves"),
    ("practise", "practised", "practised", "practising", "practises"), ("wake", "woke", "woken", "waking", "wakes"),
    ("call", "called", "called", "calling", "calls"), ("check", "checked", "checked", "checking", "checks"),
    ("get", "got", "got", "getting", "gets"), ("pass", "passed", "passed", "passing", "passes"), ("help", "helped", "helped", "helping", "helps"),
    ("arrive", "arrived", "arrived", "arriving", "arrives"), ("stay", "stayed", "stayed", "staying", "stays"),
    ("travel", "travelled", "travelled", "travelling", "travels"), ("sign", "signed", "signed", "signing", "signs"),
    ("translate", "translated", "translated", "translating", "translates"), ("deliver", "delivered", "delivered", "delivering", "delivers"),
    ("invite", "invited", "invited", "inviting", "invites"), ("design", "designed", "designed", "designing", "designs"),
    ("publish", "published", "published", "publishing", "publishes"), ("steal", "stole", "stolen", "stealing", "steals"),
    ("forget", "forgot", "forgotten", "forgetting", "forgets"), ("choose", "chose", "chosen", "choosing", "chooses"),
    ("grow", "grew", "grown", "growing", "grows"), ("feed", "fed", "fed", "feeding", "feeds"), ("be", "was", "been", "being", "is")]}

SUBJ = [("I", "1"), ("She", "3"), ("My brother", "3"), ("We", "p"), ("They", "p"), ("The students", "p"), ("He", "3"), ("My parents", "p")]
OBJ = [("write", "a letter"), ("cook", "dinner"), ("clean", "the kitchen"), ("watch", "a documentary"), ("play", "chess"),
       ("visit", "my grandparents"), ("paint", "the fence"), ("repair", "the old bike"), ("buy", "a new laptop"), ("finish", "the project"),
       ("send", "an email to the manager"), ("wash", "the dishes"), ("plant", "trees in the garden"), ("teach", "the younger kids"),
       ("speak", "to the head teacher"), ("swim", "in the lake"), ("travel", "to Ganja"), ("sing", "in the school choir"),
       ("translate", "the article"), ("feed", "the cat"), ("design", "a poster"), ("study", "for the exam")]


def _be(p, past=False):
    if past:
        return "were" if p == "p" else "was"
    return {"1": "am", "3": "is", "p": "are"}[p]


def _have(p, past=False):
    return "had" if past else ("has" if p == "3" else "have")


def conj(verb, tense, p):
    b, pa, pp, ing, s3 = V[verb]
    return {
        "present simple": s3 if p == "3" else b,
        "present continuous": f"{_be(p)} {ing}",
        "past simple": pa,
        "past continuous": f"{_be(p, True)} {ing}",
        "present perfect": f"{_have(p)} {pp}",
        "present perfect continuous": f"{_have(p)} been {ing}",
        "past perfect": f"had {pp}",
        "future perfect": f"will have {pp}",
        "future continuous": f"will be {ing}",
        "future simple": f"will {b}",
    }[tense]


TENSE_FRAMES = [
    ("{S} ___ {O} every weekend.", "present simple", M), ("{S} usually ___ {O} on Sundays.", "present simple", M),
    ("Look! {S} ___ {O} right now.", "present continuous", M), ("{S} ___ {O} at the moment, so please don't disturb.", "present continuous", M),
    ("{S} ___ {O} yesterday.", "past simple", M), ("{S} ___ {O} two days ago.", "past simple", M),
    ("{S} ___ {O} when the lights suddenly went out.", "past continuous", H), ("At 8 o'clock last night, {s} ___ {O}.", "past continuous", H),
    ("{S} ___ {O} three times this month.", "present perfect", M), ("{S} ___ {O} since the beginning of the year.", "present perfect", H),
    ("By the time we arrived, {s} ___ already ___ {O}.", "past perfect*", H), ("By the time the guests came, {s} ___ {O}.", "past perfect", H),
    ("By next June, {s} ___ {O}.", "future perfect", H), ("This time tomorrow, {s} ___ {O}.", "future continuous", H),
    ("{S} ___ {O} for two hours, and {p} still {neg} finished.", "present perfect continuous", H),
]
ALL_TENSES = ["present simple", "present continuous", "past simple", "past continuous", "present perfect",
              "present perfect continuous", "past perfect", "future perfect", "future continuous", "future simple"]


def _subj_lower(s):
    return s if s == "I" else s[0].lower() + s[1:]


def _pron(subj, p):
    return {"I": "I", "She": "she", "He": "he", "We": "we", "They": "they"}.get(subj, "he" if p == "3" else "they")


def eng_tense(r, g):
    frame, tense, diff = r.choice([f for f in TENSE_FRAMES if not f[1].endswith("*")])
    subj, p = r.choice(SUBJ)
    verb, obj = r.choice(OBJ)
    pron = _pron(subj, p)
    neg = "hasn't" if p == "3" else "haven't"
    text = frame.format(S=subj, s=_subj_lower(subj), O=obj, p=pron, neg=neg) + f" ({verb})"
    ans = conj(verb, tense, p)
    others = [conj(verb, t, p) for t in ALL_TENSES if t != tense]
    return dict(t=text, a=ans, d=pick(r, others, 4, exclude={ans}),
                e=f"Zaman göstəricisinə görə {tense.title()} lazımdır: {ans}.", diff=diff)


def eng_tense_name(r, g):
    frame, tense, diff = r.choice([f for f in TENSE_FRAMES if not f[1].endswith("*")])
    subj, p = r.choice(SUBJ)
    verb, obj = r.choice(OBJ)
    pron = _pron(subj, p)
    neg = "hasn't" if p == "3" else "haven't"
    filled = frame.replace("___", conj(verb, tense, p)).format(S=subj, s=_subj_lower(subj), O=obj, p=pron, neg=neg)
    return dict(t=f"Which tense is used in this sentence? «{filled}»", a=tense.title(),
                d=[t.title() for t in pick(r, ALL_TENSES, 4, exclude={tense})], e=f"«{conj(verb, tense, p)}» — {tense.title()}.", diff=H)


# ---------- Conditionals ----------
# (if feili, if obyekti, nəticə feili, nəticə obyekti)
COND = [("study", "harder", "pass", "the exam"), ("leave", "now", "catch", "the train"), ("have", "more money", "buy", "a new car"),
        ("know", "her number", "call", "her"), ("save", "enough money", "travel", "around the world"),
        ("practise", "every day", "play", "much better"), ("take", "a taxi", "arrive", "on time"), ("wake", "up early", "see", "the sunrise"),
        ("have", "more free time", "help", "you with the project"), ("bring", "an umbrella", "stay", "dry"),
        ("find", "the keys", "open", "the door"), ("get", "the tickets", "go", "to the concert"), ("check", "the map", "find", "the hotel"),
        ("win", "the competition", "get", "a scholarship"), ("study", "medicine", "help", "sick people")]
UNLESS = [("hurry", "", "miss", "the bus"), ("study", "harder", "fail", "the exam"), ("water", "the plants", "die", ""),
          ("wear", "a coat", "catch", "a cold"), ("book", "a table", "find", "no free seats")]
V.update({x[0]: x for x in [("hurry", "hurried", "hurried", "hurrying", "hurries"), ("miss", "missed", "missed", "missing", "misses"),
                             ("fail", "failed", "failed", "failing", "fails"), ("water", "watered", "watered", "watering", "waters"),
                             ("die", "died", "died", "dying", "dies"), ("wear", "wore", "worn", "wearing", "wears"),
                             ("book", "booked", "booked", "booking", "books")]})
ZERO = [("If you heat ice, it ___.", "melts", ["melted", "will melted", "would melt", "is melt"]),
        ("If you mix blue and yellow, you ___ green.", "get", ["got", "would get", "had got", "getting"]),
        ("Water ___ if you heat it to 100 degrees.", "boils", ["boiled", "would boil", "has boil", "boiling"]),
        ("If people don't drink water, they ___ thirsty.", "get", ["got", "would have got", "gets", "had got"]),
        ("Plants ___ if they don't get enough light.", "die", ["died", "would have died", "dies", "had died"]),
        ("If you press this button, the machine ___.", "starts", ["started", "would have started", "start", "had started"])]
CSUBJ = [("you", "p"), ("she", "3"), ("we", "p"), ("they", "p"), ("I", "1"), ("he", "3")]


def _vp(verb, form, p, obj):
    b, pa, pp, ing, s3 = V[verb]
    w = {"base": b, "s": s3 if p == "3" else b, "past": pa, "pp": pp}[form]
    if verb == "be" and form == "past":
        w = "were"
    return (w + (" " + obj if obj else "")).strip()


def eng_cond(r, g):
    t = r.choice([1, 2, 3] if g > 9 else [1, 1, 2, 3])
    (v1, o1, v2, o2) = r.choice(COND)
    (s1, p1) = r.choice(CSUBJ)
    s2, p2 = s1, p1
    b2 = V[v2][0]
    pp2 = V[v2][2]
    forms = {"will": f"will {b2}", "would": f"would {b2}", "would have": f"would have {pp2}", "had": f"had {pp2}", "present": V[v2][4] if p2 == "3" else b2}
    if t == 1:
        cl = f"If {s1} {_vp(v1, 's', p1, o1)}, {s2} ___ {o2}."
        ans, why = forms["will"], "Real şərt (First Conditional): If + Present Simple, will + V1."
    elif t == 2:
        cl = f"If {s1} {_vp(v1, 'past', p1, o1)}, {s2} ___ {o2}."
        ans, why = forms["would"], "Qeyri-real indiki şərt (Second Conditional): If + Past Simple, would + V1."
    else:
        cl = f"If {s1} had {_vp(v1, 'pp', p1, o1)}, {s2} ___ {o2}."
        ans, why = forms["would have"], "Keçmişə aid qeyri-real şərt (Third Conditional): If + Past Perfect, would have + V3."
    cl = cl[0].upper() + cl[1:]
    return dict(t=cl.replace(" .", ".") + f" ({b2})", a=ans, d=[v for k, v in forms.items() if v != ans],
                e=why, diff=M if t == 1 else H)


def eng_cond_if(r, g):
    t = r.choice([2, 3])
    (v1, o1, v2, o2) = r.choice(COND)
    (s1, p1) = r.choice(CSUBJ)
    b1, pa1, pp1 = V[v1][0], V[v1][1], V[v1][2]
    if t == 2:
        cl = f"If {s1} ___ {o1}, {s1} would {V[v2][0]} {o2}. ({b1})"
        ans = pa1
        why = "Second Conditional: if-hissədə Past Simple."
    else:
        cl = f"If {s1} ___ {o1}, {s1} would have {V[v2][2]} {o2}. ({b1})"
        ans = f"had {pp1}"
        why = "Third Conditional: if-hissədə Past Perfect."
    opts = {pa1, f"had {pp1}", f"would {b1}", V[v1][4] if p1 == "3" else b1, f"will {b1}", f"have {pp1}"} - {ans}
    return dict(t=cl.replace("  ", " ").replace(" ,", ","), a=ans, d=list(opts), e=why, diff=H)


def eng_unless(r, g):
    (v1, o1, v2, o2) = r.choice(UNLESS)
    (s1, p1) = r.choice(CSUBJ)
    subj2 = s1 if o2 or v2 != "die" else "they"
    cl = f"Unless {s1} {_vp(v1, 's', p1, o1)}, {subj2 if v2 != 'die' else 'the plants'} ___ {o2}".strip() + f". ({V[v2][0]})"
    cl = cl.replace(" .", ".")
    b2, pp2 = V[v2][0], V[v2][2]
    ans = f"will {b2}"
    return dict(t=cl[0].upper() + cl[1:], a=ans, d=[f"would {b2}", f"would have {pp2}", f"had {pp2}", V[v2][4] if v2 != "die" else "died"],
                e="Unless = if not. Real şərt olduğu üçün nəticə hissəsində will + V1 işlənir.", diff=H)


def eng_zero(r, g):
    t, a, d = r.choice(ZERO)
    return dict(t=t, a=a, d=d, e="Ümumi həqiqət (Zero Conditional): If + Present Simple, Present Simple.", diff=M)


WISH = [("I wish I ___ the answer to this question. (know)", "knew", ["know", "had known", "would know", "have known"], "İndiki vəziyyətə arzu: wish + Past Simple."),
        ("I wish I ___ harder for last week's test. (study)", "had studied", ["studied", "would study", "have studied", "study"], "Keçmişə peşmanlıq: wish + Past Perfect."),
        ("She wishes she ___ taller. (be)", "were", ["is", "had been", "would be", "be"], "İndiki vəziyyətə arzu: wish + were."),
        ("I wish you ___ making so much noise. It's annoying! (stop)", "would stop", ["stopped", "had stopped", "stop", "will stop"], "Başqasının hərəkətindən narazılıq: wish + would."),
        ("We wish we ___ that expensive phone yesterday. (not / buy)", "hadn't bought", ["didn't buy", "wouldn't buy", "don't buy", "haven't bought"], "Keçmişə peşmanlıq: wish + Past Perfect."),
        ("I wish I ___ a car. Then I could drive to work. (have)", "had", ["have", "had had", "would have", "will have"], "İndiki vəziyyətə arzu: wish + Past Simple."),
        ("If only I ___ to his advice last year! (listen)", "had listened", ["listened", "would listen", "listen", "have listened"], "If only + Past Perfect — keçmişə peşmanlıq."),
        ("He wishes he ___ speak French fluently. (can)", "could", ["can", "could have", "will", "has could"], "Bacarığa dair arzu: wish + could.")]
MIXED = [("If she had studied medicine, she ___ a doctor now. (be)", "would be", ["would have been", "will be", "had been", "is"]),
         ("If I hadn't missed the bus this morning, I ___ late for work now. (not / be)", "wouldn't be", ["won't be", "wouldn't have been", "hadn't been", "am not"]),
         ("If they had taken the job in London, they ___ in England now. (live)", "would live", ["would have lived", "will live", "had lived", "lived"]),
         ("If he weren't so shy, he ___ to her at the party yesterday. (speak)", "would have spoken", ["would speak", "will speak", "had spoken", "spoke"]),
         ("If I had learned to drive, I ___ a car now. (have)", "would have", ["would have had", "will have", "had", "have"]),
         ("Had I known about the problem, I ___ you. (help)", "would have helped", ["would help", "will help", "had helped", "helped"]),
         ("Were I in your position, I ___ the offer. (accept)", "would accept", ["will accept", "accepted", "would have accept", "had accepted"]),
         ("Should you need any help, ___ me immediately. (call)", "call", ["called", "would call", "calling", "to call"]),
         ("Had they left earlier, they ___ the train. (not / miss)", "wouldn't have missed", ["wouldn't miss", "didn't miss", "hadn't missed", "won't miss"])]


def eng_wish(r, g):
    t, a, d, e = r.choice(WISH)
    return dict(t=t, a=a, d=d, e=e, diff=H)


def eng_mixed(r, g):
    t, a, d = r.choice(MIXED)
    return dict(t=t, a=a, d=d, e="Qarışıq/inversiyalı şərt: keçmiş şərt + indiki nəticə (would + V1) və ya Had/Were/Should ilə başlayan şərt cümləsi.", diff=H)


# ---------- Passive voice ----------
PASS_OBJ = [("The letter", "s", ["write", "send", "translate"]), ("These houses", "p", ["build", "paint", "design"]),
            ("The bridge", "s", ["build", "repair", "paint"]), ("The windows", "p", ["clean", "open", "break", "wash"]),
            ("A new hospital", "s", ["build", "open", "design"]), ("The tickets", "p", ["sell", "buy", "deliver"]),
            ("The car", "s", ["repair", "wash", "sell"]), ("The documents", "p", ["sign", "send", "translate"]),
            ("This song", "s", ["sing", "write"]), ("The keys", "p", ["find", "lose", "steal"]), ("Many trees", "p", ["plant", "grow"]),
            ("The article", "s", ["publish", "write", "translate"]), ("The guests", "p", ["invite"]), ("The parcels", "p", ["deliver", "send"])]
PASS_FRAMES = [("{O} ___ yesterday.", "past"), ("{O} ___ in 2015.", "past"), ("{O} ___ every year.", "present"),
               ("{O} ___ regularly.", "present"), ("{O} ___ already.", "pres_perf"), ("{O} just ___.", None),
               ("{O} ___ next month.", "future"), ("{O} ___ tomorrow.", "future"), ("{O} ___ right now.", "pres_cont"),
               ("{O} ___ at the moment.", "pres_cont"), ("{O} ___ by the time we arrived.", "past_perf"),
               ("{O} ___ when we visited the town.", "past_cont")]


def _pass(verb, kind, n):
    pp = V[verb][2]
    sg = n == "s"
    return {"past": f"{'was' if sg else 'were'} {pp}", "present": f"{'is' if sg else 'are'} {pp}",
            "pres_perf": f"{'has' if sg else 'have'} been {pp}", "future": f"will be {pp}",
            "pres_cont": f"{'is' if sg else 'are'} being {pp}", "past_perf": f"had been {pp}",
            "past_cont": f"{'was' if sg else 'were'} being {pp}"}[kind]


PASS_NAMES = {"past": "Past Simple Passive", "present": "Present Simple Passive", "pres_perf": "Present Perfect Passive",
              "future": "Future Simple Passive", "pres_cont": "Present Continuous Passive", "past_perf": "Past Perfect Passive",
              "past_cont": "Past Continuous Passive"}


def eng_passive(r, g):
    obj, n, verbs = r.choice(PASS_OBJ)
    verb = r.choice(verbs)
    frame, kind = r.choice([f for f in PASS_FRAMES if f[1]])
    ans = _pass(verb, kind, n)
    wrong = [_pass(verb, k, n) for k in PASS_NAMES if k != kind]
    wrong += [V[verb][1], f"{'has' if n == 's' else 'have'} {V[verb][2]}", f"{'is' if n == 's' else 'are'} {V[verb][0]}"]
    return dict(t=frame.format(O=obj) + f" ({verb})", a=ans, d=pick(r, wrong, 4, exclude={ans}),
                e=f"Obyekt işi özü görmür — məchul növ lazımdır. Zaman göstəricisinə görə {PASS_NAMES[kind]}: {ans}.",
                diff=M if kind in ("past", "present", "future") else H)


ACTIVE = [("They", "build", "this school", "in 1990", "past"), ("Someone", "steal", "my bike", "last night", "past"),
          ("The company", "sell", "these phones", "all over the world", "present"), ("People", "speak", "English", "in many countries", "present"),
          ("They", "repair", "the road", "next week", "future"), ("The workers", "paint", "the walls", "at the moment", "pres_cont"),
          ("Somebody", "clean", "the classrooms", "every day", "present"), ("They", "translate", "the book", "into ten languages", "pres_perf"),
          ("The police", "catch", "the thief", "yesterday", "past"), ("Our teacher", "check", "the tests", "already", "pres_perf"),
          ("They", "deliver", "the parcel", "tomorrow", "future"), ("The children", "plant", "these trees", "last spring", "past")]


def eng_transform(r, g):
    subj, verb, obj, tail, kind = r.choice(ACTIVE)
    plural = obj.split()[0] in ("these", "the") and obj.endswith("s") and not obj.endswith("ss")
    n = "p" if plural else "s"
    act_verb = {"past": V[verb][1], "present": V[verb][4] if subj in ("The company", "Somebody", "Our teacher") else V[verb][0],
                "future": f"will {V[verb][0]}", "pres_cont": f"are {V[verb][3]}",
                "pres_perf": f"{'has' if subj in ('Our teacher',) else 'have'} {V[verb][2]}"}[kind]
    if kind == "pres_perf" and tail == "already":
        active = f"{subj} {act_verb.split()[0]} already {act_verb.split()[1]} {obj}."
    else:
        active = f"{subj} {act_verb} {obj} {tail}."
    O = obj[0].upper() + obj[1:]
    good = f"{O} {_pass(verb, kind, n)} {tail}." if tail != "already" else f"{O} {'has' if n == 's' else 'have'} already been {V[verb][2]}."
    wrong_kinds = [k for k in ["past", "present", "pres_perf", "future"] if k != kind][:3]
    bad = [f"{O} {_pass(verb, k, n)} {tail}." for k in wrong_kinds]
    bad.append(f"{O} {'was' if n == 's' else 'were'} {V[verb][0]} {tail}." if kind == "past" else f"{O} {V[verb][1]} {tail}.")
    bad = [b.replace(" already.", " already.") for b in bad]
    return dict(t=f"Choose the correct passive form of the sentence: «{active}»", a=good, d=bad,
                e=f"Məchul növdə zaman saxlanılır: {PASS_NAMES[kind]} — {good}", diff=H)


REPORTING = [("It is said that he is the best player in the team.", "He is said to be the best player in the team.",
              ["He is said being the best player in the team.", "He said to be the best player in the team.", "He is said that be the best player in the team.", "He is saying to be the best player in the team."]),
             ("People believe that the castle was built in the 12th century.", "The castle is believed to have been built in the 12th century.",
              ["The castle is believed to be built in the 12th century.", "The castle believed to have been built in the 12th century.", "The castle is believed that was built in the 12th century.", "The castle was believing to have been built in the 12th century."]),
             ("They say that the new museum will open next year.", "The new museum is said to open next year.",
              ["The new museum is said opening next year.", "The new museum says to open next year.", "The new museum is said that opens next year.", "The new museum said to be opened next year."]),
             ("I had my hair cut yesterday. This means:", "Someone cut my hair for me.",
              ["I cut my own hair.", "I wanted to cut my hair.", "My hair was too long to cut.", "I will cut my hair."]),
             ("We are having our house painted. This means:", "Someone is painting our house for us.",
              ["We are painting our house ourselves.", "Our house painted us.", "We painted our house last year.", "We don't want to paint the house."])]


def eng_reporting(r, g):
    q, a, d = r.choice(REPORTING)
    t = q if q.endswith("means:") else f"Choose the sentence closest in meaning: «{q}»"
    return dict(t=t, a=a, d=d, e="Passive reporting / causative (have something done) quruluşu.", diff=H)


# ---------- Word formation ----------
FAM = {
    "SUCCEED": ["success", "successful", "successfully", "succeed", "unsuccessful"], "DECIDE": ["decide", "decision", "decisive", "decisively", "indecisive"],
    "CREATE": ["create", "creation", "creative", "creatively", "creativity"], "BEAUTY": ["beauty", "beautiful", "beautifully", "beautify", "beauties"],
    "CARE": ["care", "careful", "carefully", "careless", "carelessly"], "DANGER": ["danger", "dangerous", "dangerously", "endanger", "dangers"],
    "EDUCATE": ["educate", "education", "educational", "educated", "uneducated"], "EMPLOY": ["employ", "employer", "employee", "employment", "unemployment"],
    "FRIEND": ["friend", "friendly", "friendship", "unfriendly", "friendliness"], "HAPPY": ["happy", "happiness", "happily", "unhappy", "unhappily"],
    "HEALTH": ["health", "healthy", "healthily", "unhealthy", "healthier"], "HONEST": ["honest", "honesty", "honestly", "dishonest", "dishonesty"],
    "IMPORTANT": ["important", "importance", "importantly", "unimportant", "import"], "INFORM": ["inform", "information", "informative", "informal", "informed"],
    "INVENT": ["invent", "invention", "inventor", "inventive", "inventing"], "KNOW": ["know", "knowledge", "knowledgeable", "known", "unknown"],
    "NATURE": ["nature", "natural", "naturally", "unnatural", "naturalist"], "PATIENT": ["patient", "patience", "patiently", "impatient", "impatience"],
    "POSSIBLE": ["possible", "possibility", "possibly", "impossible", "impossibility"], "POLLUTE": ["pollute", "pollution", "polluted", "polluter", "pollutant"],
    "PROTECT": ["protect", "protection", "protective", "protector", "unprotected"],
    "RESPONSIBLE": ["responsible", "responsibility", "responsibly", "irresponsible", "response"],
    "SCIENCE": ["science", "scientist", "scientific", "scientifically", "sciences"], "ACHIEVE": ["achieve", "achievement", "achievable", "achiever", "unachievable"],
    "ARGUE": ["argue", "argument", "arguable", "arguably", "argumentative"], "COMFORT": ["comfort", "comfortable", "comfortably", "uncomfortable", "discomfort"],
    "COMPETE": ["compete", "competition", "competitive", "competitor", "competitively"], "DIFFER": ["differ", "different", "difference", "differently", "indifferent"],
    "DEPEND": ["depend", "dependent", "independent", "independence", "dependable"],
    "ENVIRONMENT": ["environment", "environmental", "environmentally", "environmentalist", "environments"],
    "EXPLAIN": ["explain", "explanation", "explanatory", "unexplained", "explaining"], "IMAGINE": ["imagine", "imagination", "imaginative", "imaginary", "unimaginable"],
    "POWER": ["power", "powerful", "powerfully", "powerless", "empower"], "PREDICT": ["predict", "prediction", "predictable", "unpredictable", "predictably"],
    "RELY": ["rely", "reliable", "reliability", "unreliable", "reliance"], "VARY": ["vary", "variety", "various", "variation", "variable"],
    "WIDE": ["wide", "width", "widely", "widen", "widened"], "STRONG": ["strong", "strength", "strongly", "strengthen", "stronger"],
    "DEEP": ["deep", "depth", "deeply", "deepen", "deeper"], "LONG": ["long", "length", "lengthen", "longer", "lengthy"],
    "ACT": ["act", "action", "active", "actively", "activity"], "APPEAR": ["appear", "appearance", "disappear", "disappearance", "apparent"],
    "AGREE": ["agree", "agreement", "agreeable", "disagree", "disagreement"], "BELIEVE": ["believe", "belief", "believable", "unbelievable", "believer"],
    "COURAGE": ["courage", "courageous", "courageously", "encourage", "discourage"], "DESTROY": ["destroy", "destruction", "destructive", "destroyer", "destroyed"],
    "FAME": ["fame", "famous", "famously", "infamous", "famed"], "GROW": ["grow", "growth", "grown", "grower", "growing"],
    "HELP": ["help", "helpful", "helpless", "helper", "unhelpful"], "LUCK": ["luck", "lucky", "luckily", "unlucky", "unluckily"],
    "OBSERVE": ["observe", "observation", "observant", "observer", "observatory"], "PERFORM": ["perform", "performance", "performer", "performing", "performed"],
    "PRODUCE": ["produce", "product", "production", "productive", "productivity"], "SATISFY": ["satisfy", "satisfaction", "satisfied", "satisfying", "dissatisfied"],
    "SURPRISE": ["surprise", "surprised", "surprising", "surprisingly", "surprises"], "TRADITION": ["tradition", "traditional", "traditionally", "traditions", "untraditional"],
    "USE": ["use", "useful", "useless", "usefully", "user"],
}
WF = [("Her ___ in the exam made her parents proud.", "SUCCEED", "success"), ("The concert was a great ___; all the tickets were sold.", "SUCCEED", "success"),
      ("He ___ passed all his exams on the first try.", "SUCCEED", "successfully"), ("It was a difficult ___, but I chose to study abroad.", "DECIDE", "decision"),
      ("Our art teacher is very ___ and always has original ideas.", "CREATE", "creative"), ("She sings ___; everyone loves her voice.", "BEAUTY", "beautifully"),
      ("Please be ___ when you cross the street.", "CARE", "careful"), ("He made a ___ mistake because he didn't check his work.", "CARE", "careless"),
      ("Swimming in this river is very ___ because of the strong current.", "DANGER", "dangerous"),
      ("A good ___ opens many doors in life.", "EDUCATE", "education"), ("The museum offers ___ programmes for schoolchildren.", "EDUCATE", "educational"),
      ("The factory has more than 500 ___.", "EMPLOY", "employees"), ("The government wants to reduce ___ among young people.", "EMPLOY", "unemployment"),
      ("Their ___ began when they were at primary school.", "FRIEND", "friendship"), ("Money cannot buy ___.", "HAPPY", "happiness"),
      ("The children were playing ___ in the garden.", "HAPPY", "happily"), ("Eating too much fast food is ___.", "HEALTH", "unhealthy"),
      ("I appreciate your ___; thank you for telling the truth.", "HONEST", "honesty"), ("It is ___ to cheat in exams.", "HONEST", "dishonest"),
      ("Nobody understood the ___ of the discovery at that time.", "IMPORTANT", "importance"), ("The guide gave us a lot of useful ___.", "INFORM", "information"),
      ("The lecture was very ___; I learned a lot.", "INFORM", "informative"), ("The telephone is one of the most important ___ in history.", "INVENT", "inventions"),
      ("Thomas Edison was a famous American ___.", "INVENT", "inventor"), ("Reading books increases your ___.", "KNOW", "knowledge"),
      ("The painter is ___ only to a small group of experts.", "KNOW", "known"), ("This juice contains only ___ ingredients.", "NATURE", "natural"),
      ("Teaching small children requires a lot of ___.", "PATIENT", "patience"), ("He waited ___ for his turn.", "PATIENT", "patiently"),
      ("Don't be so ___! The bus will come soon.", "PATIENT", "impatient"), ("Is there any ___ of rain tomorrow?", "POSSIBLE", "possibility"),
      ("It is ___ to finish this work in one day; it's too much.", "POSSIBLE", "impossible"), ("Air ___ is a serious problem in big cities.", "POLLUTE", "pollution"),
      ("Wild animals need ___ from hunters.", "PROTECT", "protection"), ("Keeping the classroom clean is everyone's ___.", "RESPONSIBLE", "responsibility"),
      ("It was ___ of him to leave the children alone.", "RESPONSIBLE", "irresponsible"), ("Marie Curie was a brilliant ___.", "SCIENCE", "scientist"),
      ("There is no ___ evidence for this claim.", "SCIENCE", "scientific"), ("Winning the olympiad was her greatest ___.", "ACHIEVE", "achievement"),
      ("They had an ___ about who should pay the bill.", "ARGUE", "argument"), ("This chair is very ___; I could sit in it all day.", "COMFORT", "comfortable"),
      ("I felt ___ in the new shoes because they were too small.", "COMFORT", "uncomfortable"), ("There were 40 teams in the ___.", "COMPETE", "competition"),
      ("The job market is very ___ these days.", "COMPETE", "competitive"), ("Can you see any ___ between these two pictures?", "DIFFER", "difference"),
      ("Azerbaijan gained its ___ in 1991.", "DEPEND", "independence"), ("Teenagers want to be more ___ from their parents.", "DEPEND", "independent"),
      ("Plastic waste causes serious ___ problems.", "ENVIRONMENT", "environmental"), ("The teacher's ___ was clear and simple.", "EXPLAIN", "explanation"),
      ("Children have a wonderful ___.", "IMAGINE", "imagination"), ("Dragons are ___ creatures; they don't exist.", "IMAGINE", "imaginary"),
      ("This is the most ___ computer in our office.", "POWER", "powerful"), ("The weather in the mountains is very ___; it can change in minutes.", "PREDICT", "unpredictable"),
      ("My old car is not very ___; it often breaks down.", "RELY", "reliable"), ("The shop sells a wide ___ of fruit.", "VARY", "variety"),
      ("English is ___ spoken around the world.", "WIDE", "widely"), ("The ___ of the river here is about 50 metres.", "WIDE", "width"),
      ("Swimming will improve your ___.", "STRONG", "strength"), ("The ___ of the lake is about ten metres.", "DEEP", "depth"),
      ("They decided to ___ the runway for bigger planes.", "LONG", "lengthen"), ("Doctors say we should be physically ___ every day.", "ACT", "active"),
      ("The sudden ___ of the plane from the radar worried everyone.", "APPEAR", "disappearance"),
      ("The two countries signed an ___ on trade.", "AGREE", "agreement"), ("It is ___ that he ran 20 km without water!", "BELIEVE", "unbelievable"),
      ("The firefighter received a medal for his ___ actions.", "COURAGE", "courageous"), ("Teachers should ___ students to ask questions.", "COURAGE", "encourage"),
      ("The earthquake caused terrible ___.", "DESTROY", "destruction"), ("Baku is ___ for its old city and modern towers.", "FAME", "famous"),
      ("The country has seen strong economic ___.", "GROW", "growth"), ("The staff at the hotel were very ___.", "HELP", "helpful"),
      ("___, nobody was hurt in the accident.", "LUCK", "Luckily"), ("Her ___ in the play was excellent.", "PERFORM", "performance"),
      ("The meeting was very ___; we solved many problems.", "PRODUCE", "productive"), ("Customer ___ is our main goal.", "SATISFY", "satisfaction"),
      ("___, the shy boy won the speech competition.", "SURPRISE", "Surprisingly"), ("Plov is a ___ Azerbaijani dish.", "TRADITION", "traditional"),
      ("This old map is completely ___ because all the roads have changed.", "USE", "useless")]


def eng_wordform(r, g):
    s, root, ans = r.choice(WF)
    fam = FAM[root]
    cap = ans[0].isupper()
    opts = [w[0].upper() + w[1:] if cap else w for w in fam if w.lower() != ans.lower()]
    if len(opts) < 4:
        opts.append((root.lower() + "ness") if not cap else root.capitalize() + "ness")
    return dict(t=f"{s} ({root})", a=ans, d=opts[:4], e=f"Cümlədə bu yerə «{ans}» forması uyğun gəlir.", diff=M if len(ans) < 9 else H)


# ---------- Phrasal verbs ----------
PH = {"look": ("looked", "looking", "looks", "looked"), "take": ("took", "taking", "takes", "taken"), "give": ("gave", "giving", "gives", "given"),
      "put": ("put", "putting", "puts", "put"), "turn": ("turned", "turning", "turns", "turned"), "run": ("ran", "running", "runs", "run"),
      "get": ("got", "getting", "gets", "got"), "come": ("came", "coming", "comes", "come"), "go": ("went", "going", "goes", "gone"),
      "break": ("broke", "breaking", "breaks", "broken"), "bring": ("brought", "bringing", "brings", "brought"),
      "carry": ("carried", "carrying", "carries", "carried"), "set": ("set", "setting", "sets", "set"), "call": ("called", "calling", "calls", "called"),
      "find": ("found", "finding", "finds", "found"), "fill": ("filled", "filling", "fills", "filled"), "pick": ("picked", "picking", "picks", "picked"),
      "make": ("made", "making", "makes", "made"), "point": ("pointed", "pointing", "points", "pointed"), "work": ("worked", "working", "works", "worked"),
      "hand": ("handed", "handing", "hands", "handed"), "hold": ("held", "holding", "holds", "held"), "keep": ("kept", "keeping", "keeps", "kept"),
      "show": ("showed", "showing", "shows", "shown"), "wake": ("woke", "waking", "wakes", "woken"), "grow": ("grew", "growing", "grows", "grown"),
      "fall": ("fell", "falling", "falls", "fallen"), "cut": ("cut", "cutting", "cuts", "cut"), "drop": ("dropped", "dropping", "drops", "dropped"),
      "catch": ("caught", "catching", "catches", "caught"), "count": ("counted", "counting", "counts", "counted")}
# (frazal feil, məna, cümlə, forma, qrup)
PHRASAL = [("look after", "take care of", "Can you ___ my little brother this evening?", "base", 1),
           ("look for", "try to find", "I've been ___ my keys all morning.", "ing", 2),
           ("look up", "find information in a dictionary or online", "You can ___ the word in a dictionary.", "base", 3),
           ("look forward to", "wait for something with pleasure", "We are ___ the summer holidays.", "ing", 4),
           ("look into", "investigate", "The police are ___ the case.", "ing", 5),
           ("take off", "leave the ground (a plane)", "The plane ___ at 7 a.m.", "past", 6),
           ("take after", "look or behave like an older relative", "She ___ her mother — they have the same smile.", "s", 7),
           ("take up", "start a new hobby", "He ___ chess last year, and now he plays every day.", "past", 8),
           ("give up", "stop doing something", "My father ___ smoking five years ago, and he feels much healthier now.", "past", 9),
           ("put off", "postpone", "They ___ the meeting until Friday.", "past", 10),
           ("put on", "dress in (clothes)", "It's cold outside, so ___ your coat.", "base", 11),
           ("put up with", "tolerate", "I can't ___ this noise any longer.", "base", 12),
           ("turn off", "stop a machine or light", "Don't forget to ___ the lights when you leave.", "base", 13),
           ("turn down", "refuse an offer", "She ___ the job offer because the salary was low.", "past", 14),
           ("run out of", "have no more of something", "We have ___ milk, so I'll buy some.", "pp", 15),
           ("get up", "get out of bed", "I usually ___ at seven.", "base", 16),
           ("get on with", "have a good relationship with", "Do you ___ your neighbours?", "base", 17),
           ("come across", "find by chance", "I ___ an old photo while I was cleaning the attic.", "past", 18),
           ("come up with", "think of an idea", "She ___ a brilliant idea for the project.", "past", 19),
           ("go on", "continue", "Please ___ with your story — I'm listening.", "base", 20),
           ("carry on", "continue", "Despite the rain, the players ___ playing.", "past", 20),
           ("break down", "stop working (a machine)", "Our car ___ on the way to Sheki.", "past", 21),
           ("bring up", "raise a child", "She was ___ by her grandparents.", "pp", 22),
           ("set off", "start a journey", "We ___ early in the morning to avoid traffic.", "past", 23),
           ("call off", "cancel", "The match was ___ because of the heavy rain.", "pp", 24),
           ("find out", "discover information", "I ___ the truth only yesterday.", "past", 25),
           ("fill in", "complete a form", "Please ___ this form and sign it.", "base", 26),
           ("pick up", "collect someone by car", "Can you ___ the children from school today?", "base", 27),
           ("make up", "invent a story or excuse", "He ___ an excuse for being late.", "past", 28),
           ("point out", "draw attention to", "The teacher ___ a mistake in my essay.", "past", 29),
           ("work out", "find the answer to a problem", "Can you ___ the answer to this puzzle?", "base", 30),
           ("hand in", "give work to a teacher", "You must ___ your homework by Friday.", "base", 31),
           ("hold on", "wait a short time", "Could you ___ a minute, please?", "base", 32),
           ("keep up with", "stay at the same level as", "He walks so fast that I can't ___ him.", "base", 33),
           ("show off", "try to impress people", "He's always ___ his new phone.", "ing", 34),
           ("wake up", "stop sleeping", "I ___ at six o'clock this morning.", "past", 35),
           ("grow up", "become an adult", "My mother ___ in a small village near Quba.", "past", 36),
           ("fall out with", "argue and stop being friends", "She ___ her best friend last week, and now they don't speak to each other.", "past", 37),
           ("get over", "recover from an illness or problem", "It took him two weeks to ___ the flu.", "base", 38),
           ("turn up", "arrive or appear", "Only five people ___ at the meeting.", "past", 39),
           ("cut down on", "reduce the amount of", "You should ___ sugar if you want to be healthy.", "base", 40),
           ("run into", "meet someone by chance", "I ___ my old teacher at the supermarket.", "past", 18),
           ("set up", "start a company or organisation", "They ___ a small business in 2020.", "past", 41),
           ("break into", "enter a building illegally", "Someone ___ our neighbour's house last night.", "past", 42),
           ("go off", "start ringing (an alarm)", "My alarm ___ at 6 a.m.", "past", 43),
           ("give in", "stop resisting and agree", "After hours of arguing, he finally ___.", "past", 44),
           ("take over", "take control of", "A bigger company ___ the firm last year.", "past", 45),
           ("drop out", "leave school or university early", "He ___ of university in his second year.", "past", 46),
           ("catch up with", "reach someone who is ahead", "Go ahead — I'll ___ you later.", "base", 47),
           ("count on", "rely on", "You can always ___ me if you need help.", "base", 48)]


# Bir cümləyə hər ikisi uyğun gələ bilən feillər eyni qrupa salınır ki, variantlarda birlikdə çıxmasınlar
_MERGE = {31: 26, 14: 13, 39: 13, 17: 1, 27: 1, 7: 1, 22: 1, 30: 25, 3: 25, 29: 25, 35: 16, 24: 10, 37: 18, 45: 41, 28: 19, 47: 33, 40: 9, 44: 9, 23: 6}
PHRASAL = [(a, b, c, d, _MERGE.get(e, e)) for a, b, c, d, e in PHRASAL]


def _inflect(ph, f):
    head, *rest = ph.split()
    pa, ing, s, pp = PH[head]
    h = {"base": head, "past": pa, "ing": ing, "s": s, "pp": pp}[f]
    return " ".join([h] + rest)


def ph_fill(r, g):
    ph, mean, sent, f, grp = r.choice(PHRASAL)
    head = ph.split()[0]
    same_head = [p for p in PHRASAL if p[0].split()[0] == head and p[4] != grp]
    others = [p for p in PHRASAL if p[4] != grp and p not in same_head]
    choice = (same_head + pick(r, others, 4))[:4] if len(same_head) >= 2 else same_head + pick(r, others, 4 - len(same_head))
    return dict(t=sent, a=_inflect(ph, f), d=[_inflect(p[0], f) for p in choice],
                e=f"«{ph}» — {mean}.", diff=M if same_head else H)


def ph_meaning(r, g):
    ph, mean, sent, f, grp = r.choice(PHRASAL)
    bad = pick(r, [p[1] for p in PHRASAL if p[4] != grp], 4)
    return dict(t=f"What does the phrasal verb «{ph}» mean?", a=mean, d=bad, e=f"«{ph}» — {mean}.", diff=M)


def ph_which(r, g):
    ph, mean, sent, f, grp = r.choice(PHRASAL)
    bad = pick(r, [p[0] for p in PHRASAL if p[4] != grp], 4)
    return dict(t=f"Which phrasal verb means «{mean}»?", a=ph, d=bad, e=f"«{ph}» — {mean}.", diff=H)


def ph_context(r, g):
    ph, mean, sent, f, grp = r.choice(PHRASAL)
    filled = sent.replace("___", _inflect(ph, f))
    bad = pick(r, [p[1] for p in PHRASAL if p[4] != grp], 4)
    return dict(t=f"In the sentence «{filled}», the phrasal verb means ___.", a=mean, d=bad, e=f"«{ph}» — {mean}.", diff=H)


# ---------- Main idea / Inference (mətnlər) ----------
def _from_passages(kind):
    def tpl(r, g):
        items = [(p["text"], q) for p in PASSAGES if p["g"] == g for q in p[kind]]
        i = tpl.idx.get(g, 0)
        tpl.idx[g] = i + 1
        text, (q, a, d) = items[i % len(items)]
        return dict(t=q, a=a, d=d, passage=text,
                    e="Cavab mətndəki məlumata əsaslanır." if kind == "main" else "Cavab mətndə birbaşa deyilmir, amma verilmiş faktlardan məntiqi olaraq çıxır.",
                    diff=M if g == 9 else H)
    tpl.idx = {}
    return tpl


TOPICS = {
    "eng-tense": [eng_tense, eng_tense, eng_tense_name],
    "eng-cond": [eng_cond, eng_cond_if, eng_unless, eng_zero, eng_wish, eng_mixed],
    "eng-passive": [eng_passive, eng_passive, eng_transform, eng_reporting],
    "eng-word": [eng_wordform],
    "eng-phrasal": [ph_fill, ph_meaning, ph_which, ph_context],
}


def reading_quizzes(g):
    """Reading bölməsi mövzulara bölünmür: hər sinif üçün 3 quiz, hər quiz bir mətn və ona aid 10 sual."""
    quizzes = []
    for p in [x for x in PASSAGES if x["g"] == g]:
        text = f"{p['title']}\n\n{p['text']}"
        quizzes.append([dict(t=q, a=a, d=d, passage=text, diff=M if (g == 9 and k < 6) else H,
                             e="Cavab mətndəki məlumata əsaslanır.")
                        for k, (q, a, d) in enumerate(p["qs"])])
    return quizzes

if __name__ == "__main__":
    for g in (9, 10, 11):
        topics = {tid: build_topic(g, "en", tid, tpls, seed=9000) for tid, tpls in TOPICS.items()}
        topics["eng-reading"] = build_fixed(g, "eng-reading", reading_quizzes(g), seed=9000)
        save_grade(g, "en", topics)
