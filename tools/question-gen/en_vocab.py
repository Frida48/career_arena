"""İngilis dili · Vocabulary: söz yaradıcılığı, frazal feillər, önlüklər və önlüklü ifadələr.
Distraktorlar yalnız şübhəsiz səhv olanlardır: yanlış nitq hissəsi, olmayan söz forması, yanlış önlük,
frazal feilin yanlış quruluşu (önlüyün düşməsi, əvəzliyin yanlış yeri, feildən sonra yanlış forma)."""
from en_core import Gap, multi_gap, correct_sentence, correct_pair

# ---------------- Word formation ----------------
# (cümlə, düzgün, səhvlər — hamısı yanlış nitq hissəsi və ya olmayan söz, səviyyə)
WF = [
    ("Her ___ in the final exam made her parents proud. (SUCCEED)", "success", ["successful", "successfully", "succeed"], 1),
    ("He ___ passed all his exams on the first try. (SUCCEED)", "successfully", ["successful", "success", "successly"], 1),
    ("It was a difficult ___, but I chose to study abroad. (DECIDE)", "decision", ["decisive", "decide", "decisively"], 1),
    ("Our art teacher is very ___ and always has original ideas. (CREATE)", "creative", ["creation", "creatively", "creativity"], 1),
    ("Swimming in this river is ___ because of the strong current. (DANGER)", "dangerous", ["danger", "dangerously", "endanger"], 1),
    ("The museum offers ___ programmes for schoolchildren. (EDUCATE)", "educational", ["education", "educate", "educationally"], 1),
    ("The government wants to reduce ___ among young people. (EMPLOY)", "unemployment", ["unemployed", "unemploy", "unemployable"], 2),
    ("I appreciate your ___; thank you for telling the truth. (HONEST)", "honesty", ["honest", "honestly", "dishonest"], 1),
    ("Teaching small children requires a lot of ___. (PATIENT)", "patience", ["patient", "patiently", "impatient"], 1),
    ("Keeping the classroom clean is everyone's ___. (RESPONSIBLE)", "responsibility", ["responsible", "responsibly", "irresponsible"], 2),
    ("There is no ___ evidence for this claim. (SCIENCE)", "scientific", ["scientist", "scientifically", "sciences"], 1),
    ("The job market is extremely ___ these days. (COMPETE)", "competitive", ["competition", "competitively", "competitor"], 2),
    ("Azerbaijan restored its ___ in 1991. (DEPEND)", "independence", ["independent", "independently", "dependent"], 2),
    ("Dragons are ___ creatures; they don't exist. (IMAGINE)", "imaginary", ["imagination", "imagine", "imaginatively"], 2),
    ("The weather in the mountains is highly ___; it can change in minutes. (PREDICT)", "unpredictable", ["unpredictably", "prediction", "predict"], 2),
    ("The shop sells a wide ___ of fruit. (VARY)", "variety", ["various", "vary", "variously"], 2),
    ("English is ___ spoken around the world. (WIDE)", "widely", ["wide", "width", "widen"], 1),
    ("The ___ of the lake is about ten metres. (DEEP)", "depth", ["deep", "deeply", "deepen"], 1),
    ("They decided to ___ the runway for bigger planes. (LONG)", "lengthen", ["length", "lengthy", "lengthily"], 2),
    ("The sudden ___ of the plane from the radar worried everyone. (APPEAR)", "disappearance", ["disappear", "disappeared", "disappearment"], 2),
    ("It is ___ that he ran 20 km without water! (BELIEVE)", "unbelievable", ["unbelief", "unbelievably", "disbelieve"], 2),
    ("Teachers should ___ students to ask questions. (COURAGE)", "encourage", ["courageous", "encouragement", "courageously"], 2),
    ("The earthquake caused terrible ___. (DESTROY)", "destruction", ["destructive", "destroy", "destructively"], 2),
    ("Customer ___ is our main goal. (SATISFY)", "satisfaction", ["satisfied", "satisfy", "satisfactory"], 2),
    ("___, the shy boy won the speech competition. (SURPRISE)", "Surprisingly", ["Surprising", "Surprisement", "Surprise"], 2),
    ("The meeting was very ___; we solved many problems. (PRODUCE)", "productive", ["production", "productivity", "productively"], 2),
    ("The new law has had a ___ effect on small businesses. (BENEFIT)", "beneficial", ["benefitful", "beneficially", "beneficiary"], 3),
    ("His ___ to admit the mistake surprised everyone. (REFUSE)", "refusal", ["refuse", "refusing to", "refusable"], 3),
    ("The results of the experiment were ___ with the theory. (CONSIST)", "consistent", ["consistency", "consistently", "consist"], 3),
    ("The damage to the coral reef may be ___. (REVERSE)", "irreversible", ["unreversible", "irreversibly", "reversal"], 3),
    ("The rise in prices was ___; nobody had ever seen anything like it. (PRECEDENT)", "unprecedented", ["inprecedented", "unprecedentedly", "precedence"], 3),
    ("A simple ___ of the instructions led to the accident. (INTERPRET)", "misinterpretation", ["misinterpret", "disinterpretation", "misinterpreted"], 3),
    ("The ___ of the old factory took three years. (DEMOLISH)", "demolition", ["demolish", "demolishion", "demolished"], 3),
    ("Her ___ to detail makes her an excellent editor. (ATTEND)", "attention", ["attentive", "attend", "attentively"], 2),
    ("The team showed great ___ under pressure. (RESILIENT)", "resilience", ["resilient", "resiliently", "resilientness"], 3),
    ("The minister's speech was deliberately ___, so nobody knew his real position. (AMBIGUITY)", "ambiguous", ["ambiguity", "ambiguously", "unambiguity"], 3),
    ("The decision was made ___, without a single objection. (UNANIMOUS)", "unanimously", ["unanimity", "unanimousness", "unanimousely"], 3),
    ("We need to ___ our efforts if we want to finish on time. (INTENSE)", "intensify", ["intensive", "intensity", "intensely"], 3),
    ("The documents were ___ and must be checked again. (ACCURATE)", "inaccurate", ["unaccurate", "inaccuracy", "inaccurately"], 2),
    ("This problem is ___; we have to accept it and move on. (AVOID)", "unavoidable", ["inavoidable", "unavoidably", "avoidance"], 3),
    ("He is a man of great ___; he never breaks a promise. (RELY)", "reliability", ["reliable", "reliably", "unreliable"], 2),
    ("The ___ of the bridge was delayed by bad weather. (CONSTRUCT)", "construction", ["constructive", "construct", "constructively"], 1),
    ("The audience listened ___ to every word. (ATTENTION)", "attentively", ["attentive", "attention", "attend"], 2),
    ("They live in a ___ area with very few shops. (RESIDENT)", "residential", ["residentially", "reside", "residentional"], 3),
    ("The film's ending was completely ___. (EXPECT)", "unexpected", ["unexpectedly", "expectation", "inexpected"], 2),
    ("Sleep ___ can cause serious health problems. (DEPRIVE)", "deprivation", ["deprive", "deprived", "deprivement"], 3),
    ("His ___ behaviour annoyed the other passengers. (CONSIDER)", "inconsiderate", ["inconsiderately", "unconsiderate", "inconsideration"], 3),
]


def _wf():
    out = []
    for f, ok, bad, lvl in WF:
        out.append(Gap(f, ok, bad, f"«{ok}» — boşluğun tələb etdiyi nitq hissəsi/forma", lvl))
    return out


WORDF = _wf()

# ---------------- Phrasal verbs ----------------
# Distraktorlar: frazal feilin quruluşunun pozulması (önlüyün düşməsi/dəyişməsi, əvəzliyin yeri, sonrakı forma)
PHR = [
    ("We are looking forward ___ you next week.", "to seeing", ["to see", "seeing", "for seeing"], "look forward to + V-ing", 1),
    ("I can't put up ___ this noise any longer.", "with", ["to", "on", "for"], "put up with — dözmək", 1),
    ("We have run out ___ milk, so I'll buy some.", "of", ["from", "with", "off"], "run out of — qurtarmaq", 1),
    ("My father gave up ___ five years ago.", "smoking", ["to smoke", "smoke", "for smoking"], "give up + V-ing — tərgitmək", 1),
    ("The light is too bright. Could you turn ___, please?", "it off", ["off it", "it out off", "off to it"], "Ayrılan frazal feildə əvəzlik ortada: turn it off", 2),
    ("These are your shoes. Put ___ before you go out.", "them on", ["on them", "them in on", "on to them"], "Əvəzlik: put them on", 2),
    ("Here is the form. Please fill ___ and sign it.", "it in", ["in it", "it on in", "in to it"], "Əvəzlik: fill it in", 2),
    ("She takes ___ her mother; they have the same smile.", "after", ["off", "up", "over"], "take after — oxşamaq", 1),
    ("The plane took ___ at 7 a.m. and landed two hours later.", "off", ["after", "up", "over"], "take off — havaya qalxmaq", 1),
    ("He took ___ chess last year, and now he plays every day.", "up", ["after", "off", "over"], "take up — yeni məşğuliyyətə başlamaq", 2),
    ("A bigger company took ___ the firm last year and changed its name.", "over", ["after", "off", "up to"], "take over — nəzarəti ələ keçirmək", 2),
    ("The match was called ___ because of the heavy rain.", "off", ["out", "up", "after"], "call off — ləğv etmək", 2),
    ("She came up ___ a brilliant idea for the project.", "with", ["to", "for", "on"], "come up with — fikir tapmaq", 1),
    ("Do you get on ___ your new neighbours?", "with", ["to", "for", "at"], "get on with — yola getmək", 2),
    ("It took him two weeks to get ___ the flu.", "over", ["off", "out", "up"], "get over — sağalmaq", 2),
    ("He walks so fast that I can't keep up ___ him.", "with", ["to", "on", "for"], "keep up with — ayaqlaşmaq", 2),
    ("You should cut down ___ sugar if you want to be healthy.", "on", ["of", "with", "from"], "cut down on — azaltmaq", 2),
    ("She fell out ___ her best friend, and now they don't speak.", "with", ["to", "of", "from"], "fall out with — küsmək", 3),
    ("He dropped out ___ university in his second year.", "of", ["to", "off", "with"], "drop out of — oxumağı yarımçıq atmaq", 3),
    ("Go ahead — I'll catch up ___ you later.", "with", ["for", "on", "at"], "catch up with — çatmaq", 2),
    ("The police are looking ___ the case; they want to know what happened.", "into", ["up to", "down on", "forward"], "look into — araşdırmaq", 2),
    ("She was brought ___ by her grandparents in a small village.", "up", ["off", "out", "over"], "bring up — böyütmək", 2),
    ("They set ___ a small business in 2020, and now it has ten employees.", "up", ["off", "out to", "over"], "set up — qurmaq (şirkət)", 2),
    ("We set ___ early in the morning to avoid the traffic.", "off", ["on", "over", "after"], "set off — yola düşmək", 2),
    ("Our car broke ___ on the way to Sheki, so we called a mechanic.", "down", ["into", "up with", "over"], "break down — xarab olmaq", 1),
    ("Someone broke ___ our neighbour's house last night and stole a TV.", "into", ["out", "off", "down to"], "break into — oğurluq üçün girmək", 2),
    ("Only five people turned ___ at the meeting.", "up", ["down", "off", "over"], "turn up — gəlmək, görünmək", 2),
    ("She turned ___ the job offer because the salary was too low.", "down", ["up", "off", "over"], "turn down — rədd etmək", 2),
    ("I ran ___ my old teacher at the supermarket yesterday.", "into", ["out of", "up with", "off"], "run into — təsadüfən rastlaşmaq", 2),
    ("The teacher pointed ___ a mistake in my essay.", "out", ["up", "off", "over"], "point out — diqqət çəkmək", 2),
    ("After hours of arguing, he finally gave ___ and agreed.", "in", ["up to", "out of", "off"], "give in — təslim olmaq", 3),
    ("You can always count ___ me if you need help.", "on", ["at", "with", "for"], "count on — güvənmək", 2),
    ("I'm not used to ___ up so early.", "getting", ["get", "got", "be getting"], "be used to + V-ing", 3),
    ("He has always looked down ___ people who earn less than him.", "on", ["with", "to", "after"], "look down on — xor baxmaq", 3),
    ("We need to come ___ with a solution before Friday.", "up", ["over", "off", "after"], "come up with — tapmaq", 2),
    ("The meeting has been put ___ until next Monday.", "off", ["out", "up with", "over to"], "put off — təxirə salmaq", 2),
    ("I came ___ an interesting article while I was reading the news.", "across", ["over to", "out of", "up to"], "come across — təsadüfən tapmaq", 2),
    ("The children were told to hand ___ their homework by Friday.", "in", ["off", "over to", "up"], "hand in — təhvil vermək", 2),
    ("My alarm went ___ at 6 a.m., but I didn't hear it.", "off", ["up", "over", "after"], "go off — zəng çalmaq (zəngli saat)", 2),
    ("He made ___ an excuse for being late, but nobody believed him.", "up", ["off", "over", "out of"], "make up — uydurmaq", 2),
    ("The detectives finally worked ___ how the thief had escaped.", "out", ["up", "off", "over"], "work out — anlamaq, həll etmək", 3),
    ("I'll look ___ the word in the dictionary.", "up", ["after", "forward", "into to"], "look up — axtarıb tapmaq (lüğətdə)", 1),
    ("Who will look ___ the dog while we are on holiday?", "after", ["up", "forward", "into to"], "look after — qayğısına qalmaq", 1),
    ("The government has decided to do away ___ the old tax.", "with", ["to", "from", "of"], "do away with — ləğv etmək", 3),
    ("The company had to lay ___ fifty workers because of the crisis.", "off", ["up", "over", "out to"], "lay off — işdən çıxarmaq", 3),
    ("Don't let the bad result put you ___; keep trying.", "off", ["up with", "over", "out of"], "put somebody off — həvəsdən salmaq", 3),
    ("The rumour turned ___ to be completely false.", "out", ["up", "off", "down"], "turn out — məlum olmaq", 3),
    ("She stood ___ for her friend when the others laughed at him.", "up", ["out", "off", "over"], "stand up for — müdafiə etmək", 3),
    ("I don't feel ___ going out tonight; I'm too tired.", "like", ["as", "to", "for"], "feel like + V-ing — istəmək", 2),
    ("They have been trying to figure ___ the meaning of the old map.", "out", ["up", "over", "off"], "figure out — başa düşmək", 3),
]
PHRASAL = [Gap(*p) for p in PHR]

# ---------------- Prepositions and prepositional phrases ----------------
PREP = [
    ("She is very interested ___ ancient history.", "in", ["on", "at", "about"], "interested in", 1),
    ("He is good ___ solving difficult puzzles.", "at", ["on", "about", "of"], "good at + V-ing", 1),
    ("I'm afraid ___ spiders.", "of", ["from", "about", "for"], "afraid of", 1),
    ("The result depends ___ the weather.", "on", ["of", "from", "at"], "depend on", 1),
    ("Who is responsible ___ this mess?", "for", ["of", "about", "to"], "responsible for", 1),
    ("She insisted ___ paying for dinner.", "on", ["to", "for", "at"], "insist on + V-ing", 2),
    ("They accused him ___ stealing the money.", "of", ["for", "with", "about"], "accuse somebody of", 2),
    ("The rain prevented us ___ going out.", "from", ["of", "to", "for"], "prevent somebody from + V-ing", 2),
    ("I broke the vase by accident, not ___ purpose.", "on", ["by", "for", "with"], "on purpose — qəsdən", 2),
    ("Sorry, I took your umbrella ___ mistake.", "by", ["on", "with", "in"], "by mistake — səhvən", 2),
    ("You have to book the tickets ___ advance.", "in", ["on", "by", "at"], "in advance — əvvəlcədən", 2),
    ("The lift is ___ of order, so we have to use the stairs.", "out", ["off", "under", "without"], "out of order — xarab", 2),
    ("Mr Aliyev is ___ charge of the sales department.", "in", ["on", "at", "under"], "in charge of — məsul", 2),
    ("I'm writing ___ behalf of my company.", "on", ["at", "for", "by"], "on behalf of — adından", 3),
    ("___ spite of the rain, they went for a walk.", "In", ["Despite of", "On", "By"], "in spite of (despite of yanlışdır)", 2),
    ("He arrived ___ time for the start of the lesson.", "in", ["at", "by", "with"], "in time — vaxtında (gecikmədən)", 3),
    ("I'll meet you ___ the weekend.", "at", ["in", "to", "of"], "at the weekend (BrE)", 2),
    ("She was born ___ 5 May 2008.", "on", ["in", "at", "by"], "Tarix ilə on", 1),
    ("The shop opens ___ 9 o'clock.", "at", ["on", "in", "by the"], "Saat ilə at", 1),
    ("We moved to Baku ___ 2015.", "in", ["on", "at", "by the"], "İl ilə in", 1),
    ("He has lived here ___ 2010.", "since", ["for", "during", "at"], "since + başlanğıc nöqtəsi", 1),
    ("I have known her ___ ten years.", "for", ["since", "during", "from"], "for + müddət", 1),
    ("She is married ___ a doctor.", "to", ["with", "on", "for"], "married to", 2),
    ("Are you aware ___ the risks?", "of", ["about", "on", "for"], "aware of", 2),
    ("He apologised ___ being late.", "for", ["of", "about", "on"], "apologise for", 2),
    ("This book is different ___ the one I read last year.", "from", ["of", "with", "on"], "different from", 2),
    ("She congratulated me ___ passing the exam.", "on", ["about", "with", "of"], "congratulate somebody on", 3),
    ("He succeeded ___ finding a new job.", "in", ["to", "on", "at"], "succeed in + V-ing", 2),
    ("The town is famous ___ its mineral water.", "for", ["of", "with", "by"], "famous for", 1),
    ("I'm not keen ___ horror films.", "on", ["of", "at", "with"], "keen on", 2),
    ("This medicine is not suitable ___ children under 12.", "for", ["of", "with", "at"], "suitable for", 2),
    ("He is capable ___ doing much better work.", "of", ["to", "for", "in"], "capable of + V-ing", 3),
    ("She has no intention ___ resigning.", "of", ["to", "for", "on"], "intention of + V-ing", 3),
    ("There has been a sharp rise ___ the price of fuel.", "in", ["with", "on", "at"], "a rise in (price)", 3),
    ("The demand ___ electric cars is growing fast.", "for", ["of", "on", "to"], "demand for", 3),
    ("He was ___ the impression that the meeting had been cancelled.", "under", ["in", "on", "with"], "under the impression — belə təsəvvür etmək", 3),
    ("The new rules will come ___ effect next month.", "into", ["in", "to", "on"], "come into effect — qüvvəyə minmək", 3),
    ("___ the whole, the trip was a success.", "On", ["In", "At", "By"], "on the whole — ümumilikdə", 3),
    ("The plan is still ___ discussion.", "under", ["in", "on", "at"], "under discussion — müzakirədə", 3),
    ("I know the poem ___ heart.", "by", ["in", "with", "from"], "by heart — əzbər", 2),
    ("The two brothers look alike, but they differ ___ character.", "in", ["on", "at", "with"], "differ in", 3),
    ("She objected ___ being treated like a child.", "to", ["against", "on", "for"], "object to + V-ing", 3),
    ("He was ___ a hurry and forgot his keys.", "in", ["on", "at", "with"], "in a hurry", 1),
    ("The children were ___ danger, so the police acted quickly.", "in", ["on", "at", "under the"], "in danger", 1),
    ("The building is ___ construction and will open next year.", "under", ["in", "on", "at"], "under construction", 2),
    ("___ my opinion, the film was too long.", "In", ["On", "By", "For"], "in my opinion", 1),
    ("He did it ___ his own, without any help.", "on", ["by", "in", "for"], "on his own — təkbaşına", 2),
    ("She is jealous ___ her sister's success.", "of", ["on", "about", "for"], "jealous of", 2),
    ("This road leads ___ the city centre.", "to", ["at", "in", "for"], "lead to", 1),
    ("The decision was taken ___ the expense of the workers.", "at", ["on", "by", "for"], "at the expense of — hesabına", 3),
]
PREPS = [Gap(*p) for p in PREP]


def topic_v(items, note, ask):
    t = [multi_gap(items, note), correct_sentence(items, ask)]
    return {9: t, 10: t, 11: t + [correct_pair(items, "In which option are BOTH sentences correct?")]}


VOCAB_TOPICS = {
    "eng-word": topic_v(WORDF, "", "In which sentence is the word form correct?"),
    "eng-phrasal": topic_v(PHRASAL, "", "Which sentence is correct?"),
    "eng-prep": topic_v(PREPS, "", "In which sentence is the preposition used correctly?"),
}
