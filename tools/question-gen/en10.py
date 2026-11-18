"""10-cu sinif ingilis dili: 3 bölmə × 30 orijinal sual (B1 səviyyəsi)."""
from common import handwritten, save

GRAMMAR = [
    ("Second Conditional", "medium", "If I ___ more time, I would learn Japanese.", "had",
     ["have", "will have", "would have", "having"], "Qeyri-real indiki şərt: If + Past Simple, would + V1."),
    ("Present Perfect", "easy", "She ___ in this company since 2019.", "has worked",
     ["works", "worked", "is working", "work"], "«Since» ilə keçmişdən indiyə qədər davam edən iş — Present Perfect."),
    ("Past Perfect", "medium", "By the time we arrived, the film ___.", "had already started",
     ["already started", "has already started", "was already starting", "already starts"],
     "Keçmişdəki bir anlıq hərəkətdən əvvəl bitmiş iş — Past Perfect."),
    ("Passive Voice", "medium", "The new bridge ___ next year.", "will be built",
     ["will build", "is building", "builds", "built"], "Gələcək zamanda məchul növ: will be + V3."),
    ("Reported Speech", "medium", "He said that he ___ tired.", "was", ["is", "be", "were being", "has"],
     "Vasitəli nitqdə Present Simple → Past Simple."),
    ("Gerund / Infinitive", "medium", "I'm looking forward to ___ you.", "seeing", ["see", "saw", "to see", "seen"],
     "«Look forward to» birləşməsindən sonra -ing gəlir (to burada önlükdür)."),
    ("Modals", "medium", "You'd better ___ a doctor.", "see", ["to see", "seeing", "saw", "seen"],
     "«Had better»dən sonra to-suz V1 gəlir."),
    ("Relative Clauses", "easy", "This is the house ___ I was born.", "where", ["which", "who", "whose", "what"],
     "Yer bildirən isimdən sonra «where»."),
    ("Wishes", "medium", "I wish I ___ how to swim.", "knew", ["know", "have known", "will know", "knowing"],
     "İndiki vəziyyətə dair arzu: wish + Past Simple."),
    ("Modals of Deduction", "medium", "She ___ be at home — her car is outside.", "must",
     ["can't", "mustn't", "needn't", "shouldn't"], "Güclü məntiqi ehtimal — must."),
    ("Modals of Deduction", "medium", "He ___ be at work; it's Sunday and the office is closed.", "can't",
     ["must", "should", "has to", "will"], "Mümkün olmadığına əminlik — can't."),
    ("Comparatives", "medium", "The more you practise, ___ you become.", "the better",
     ["better", "the best", "more better", "the more good"], "The + müqayisə dərəcəsi …, the + müqayisə dərəcəsi."),
    ("Be used to / Used to", "hard", "I'm used to ___ up early.", "getting", ["get", "got", "to get", "gets"],
     "«Be used to» (öyrəşmək) + -ing."),
    ("Be used to / Used to", "medium", "I used to ___ football when I was a child.", "play",
     ["playing", "played", "plays", "be playing"], "Keçmiş vərdiş: used to + V1."),
    ("Causative / Let / Make", "easy", "Let me ___ your bag.", "carry", ["to carry", "carrying", "carried", "carries"],
     "«Let»dən sonra to-suz V1."),
    ("Causative / Let / Make", "medium", "They made us ___ the room.", "clean", ["to clean", "cleaning", "cleaned", "cleans"],
     "Məlum növdə «make somebody do» — to-suz V1."),
    ("Relative Clauses", "medium", "The book, ___ was written in 1950, is still popular.", "which",
     ["that", "who", "what", "whose"], "Vergüllə ayrılan (non-defining) budaq cümlədə əşya üçün «which» işlənir, «that» yox."),
    ("Quantifiers", "medium", "I have two brothers, and ___ of them live in Baku.", "both",
     ["all", "each", "either", "every"], "İki nəfər haqqında, cəm feillə — both."),
    ("Quantifiers", "medium", "We have ___ bread left. Let's buy some.", "little", ["few", "a few", "many", "a lot"],
     "Sayılmayan isim, «az, demək olar ki, yoxdur» mənası — little."),
    ("Quantifiers", "medium", "There were ___ people at the party, so it wasn't boring.", "a few",
     ["a little", "little", "much", "any"], "Sayılan isim, müsbət məna — a few."),
    ("Reported Questions", "medium", "He asked me ___ I could help him.", "if", ["that", "what", "unless", "which"],
     "Hə/yox sualı vasitəli nitqdə if/whether ilə verilir."),
    ("Superlatives", "easy", "It's the ___ film I have ever seen.", "most exciting",
     ["more exciting", "excitingest", "exciting", "much exciting"], "Üstünlük dərəcəsi: the most + uzun sifət."),
    ("Present Perfect Continuous", "easy", "She has been studying English ___ she was ten.", "since",
     ["for", "during", "ago", "until"], "Başlanğıc nöqtəsi — since."),
    ("First Conditional", "medium", "Unless you hurry, you ___ the bus.", "will miss",
     ["miss", "would miss", "missed", "are missing"], "Unless = if not; real şərt: will + V1."),
    ("Past Continuous", "medium", "I ___ dinner when my phone rang.", "was cooking",
     ["am cooking", "have cooked", "cook", "had been cook"], "Kəsilən uzun keçmiş hərəkət — Past Continuous."),
    ("Subject–Verb Agreement", "hard", "Neither of my parents ___ coffee.", "drinks",
     ["drink", "are drinking", "drinking", "have drink"], "Rəsmi qrammatikada «neither of» təkdə feillə işlənir."),
    ("Gerund / Infinitive", "easy", "Would you mind ___ the window?", "opening",
     ["to open", "open", "opened", "opens"], "«Mind»dan sonra -ing."),
    ("Time Clauses", "medium", "I'll call you as soon as I ___ home.", "get",
     ["will get", "got", "am getting", "would get"], "Zaman budaq cümləsində gələcək mənada Present Simple işlənir."),
    ("Too / Enough", "easy", "She is too young ___ alone.", "to travel",
     ["travelling", "travel", "for travel", "traveled"], "Too + sifət + to + V1."),
    ("Question Tags", "medium", "You're coming tomorrow, ___?", "aren't you",
     ["don't you", "won't you", "are you", "isn't it"], "Müsbət cümlə + inkar «tag»: You're … , aren't you?"),
]

VOCAB = [
    ("Phrasal Verbs", "easy", "The teacher asked us to ___ our mobile phones during the exam.", "switch off",
     ["switch on", "take up", "give in", "look up"], "Switch off — söndürmək."),
    ("Phrasal Verbs", "medium", "I can't ___ the noise any longer.", "put up with",
     ["put off", "put on", "put away", "put out"], "Put up with — dözmək."),
    ("Phrasal Verbs", "medium", "The meeting has been ___ until next week.", "put off",
     ["put up", "put on", "put down", "put in"], "Put off — təxirə salmaq."),
    ("Phrasal Verbs", "medium", "She ___ her grandmother — they have the same eyes.", "takes after",
     ["takes off", "takes over", "takes up", "takes in"], "Take after — (ailə üzvünə) oxşamaq."),
    ("Phrasal Verbs", "medium", "We ran ___ milk, so I went to the shop.", "out of",
     ["away from", "into", "over", "through"], "Run out of — qurtarmaq, tükənmək."),
    ("Synonyms", "easy", "Choose the synonym of «reliable».", "dependable",
     ["careless", "cheerful", "generous", "curious"], "Reliable = dependable (etibarlı)."),
    ("Antonyms", "medium", "Choose the antonym of «generous».", "mean",
     ["kind", "rich", "friendly", "polite"], "Generous (səxavətli) — mean (xəsis)."),
    ("Collocations", "easy", "We are making good ___ with our project.", "progress",
     ["homework", "housework", "exercise", "research"], "Sabit birləşmə: make progress."),
    ("Collocations", "easy", "Don't worry about the result. Just ___ your best.", "do",
     ["make", "take", "put", "get"], "Sabit birləşmə: do your best."),
    ("Collocations", "medium", "It's important to ___ a balanced diet.", "follow",
     ["do", "make", "win", "spend"], "Follow a diet — pəhrizə əməl etmək."),
    ("Word Formation", "easy", "Smoking is ___ to your health. (HARM)", "harmful",
     ["harmless", "harm", "harmed", "harmfully"], "Harmful — zərərli."),
    ("Word Formation", "medium", "She showed great ___ during the competition. (CONFIDENT)", "confidence",
     ["confident", "confidently", "confide", "confidential"], "Sifətdən sonra isim lazımdır: confidence (özünəinam)."),
    ("Word Formation", "easy", "Thank you for your ___. (KIND)", "kindness",
     ["kind", "kindly", "unkind", "kinder"], "Your + isim: kindness."),
    ("Word Formation", "medium", "I ___ with you. I think you're wrong. (AGREE)", "disagree",
     ["agree", "agreement", "agreeable", "disagreement"], "Məna inkardır və feil lazımdır: disagree."),
    ("Word Formation", "medium", "The film was ___; I couldn't stop laughing. (HUMOUR)", "humorous",
     ["humour", "humourless", "humorously", "humorist"], "Humorous — gülməli, yumorlu."),
    ("Word Formation", "medium", "An ___ person hates waiting. (PATIENT)", "impatient",
     ["patient", "patience", "unpatient", "patiently"], "Patient sözünün inkarı im- ilə düzəlir: impatient."),
    ("People", "easy", "A ___ is a person who travels to a place for pleasure.", "tourist",
     ["guide", "pilot", "resident", "driver"], "Tourist — turist."),
    ("Confusing Words", "medium", "The doctor wrote me a ___ for some medicine.", "prescription",
     ["recipe", "receipt", "description", "subscription"], "Prescription — resept (həkim)."),
    ("Confusing Words", "medium", "Please keep the ___ in case you want to return the shirt.", "receipt",
     ["recipe", "prescription", "review", "menu"], "Receipt — qəbz, çek."),
    ("Confusing Words", "medium", "My mum gave me a ___ for chocolate cake.", "recipe",
     ["receipt", "prescription", "menu", "review"], "Recipe — yemək resepti."),
    ("Meaning", "medium", "«Ambitious» means ___.", "having a strong wish to succeed",
     ["being very shy", "feeling sleepy", "easily angry", "not interested"], "Ambitious — iddialı, məqsədyönlü."),
    ("Meaning", "easy", "«Fragile» means ___.", "easily broken",
     ["very heavy", "very expensive", "quite old", "brightly coloured"], "Fragile — kövrək, asan sınan."),
    ("Meaning", "medium", "«To postpone» means ___.", "to delay",
     ["to cancel", "to start", "to finish", "to repeat"], "Postpone — təxirə salmaq (ləğv etmək deyil)."),
    ("Synonyms", "easy", "Which word is closest in meaning to «essential»?", "necessary",
     ["optional", "extra", "unusual", "boring"], "Essential — vacib, zəruri."),
    ("Antonyms", "easy", "The opposite of «increase» is ___.", "decrease",
     ["rise", "grow", "expand", "raise"], "Increase (artmaq) — decrease (azalmaq)."),
    ("Collocations", "easy", "I'd like to ___ a table for two at 7 p.m.", "book",
     ["order", "take", "buy", "do"], "Book a table — stol sifariş etmək (rezerv)."),
    ("Collocations", "easy", "Could you ___ me a favour?", "do", ["make", "give", "take", "have"],
     "Sabit birləşmə: do somebody a favour."),
    ("Collocations", "medium", "She ___ a speech at the conference.", "gave", ["did", "said", "told", "spoke"],
     "Sabit birləşmə: give a speech."),
    ("Collocations", "medium", "He has ___ a cold, so he's staying at home.", "caught",
     ["taken", "made", "kept", "held"], "Catch a cold — soyuqlamaq."),
    ("So / Such", "medium", "The bus was ___ crowded that we couldn't get on.", "so",
     ["such", "too", "very", "enough"], "So + sifət + that."),
]

R1 = ("Last summer Aysel got her first part-time job at a small café near her school. At first she found it difficult. "
      "She had to remember dozens of orders, and once she dropped a whole tray of glasses in front of the customers. "
      "She wanted to quit after the first week, but the owner, Mr Kamal, told her that everyone makes mistakes at the "
      "beginning. He taught her to write orders down and to carry fewer things at once. By the end of the summer, "
      "Aysel was one of the fastest waiters in the café. She says the job taught her more about responsibility than "
      "any lesson at school, and she used the money she earned to buy a laptop for her studies.")
R2 = ("Every year millions of tonnes of plastic end up in the world's oceans. Most of it comes from land: bottles, bags "
      "and packaging are carried by rivers or blown by the wind into the sea. Plastic does not disappear; instead, it "
      "slowly breaks into tiny pieces called microplastics. Sea animals often mistake these pieces for food. Turtles, for "
      "example, sometimes eat plastic bags because they look like jellyfish. Some countries have banned single-use bags, "
      "and many beaches are now cleaned by volunteers. However, scientists say that the most effective solution is to "
      "produce and use less plastic in the first place.")
R3 = ("When Elvin was helping his grandfather clean the attic, he found an old wooden box. Inside there was a map of their "
      "village, drawn by hand more than sixty years ago. On the map, a small cross was marked next to the old mill. "
      "Elvin was sure it was hidden treasure. The next morning he and his sister walked to the mill with a shovel. After "
      "an hour of digging, they found a metal tin. There was no gold inside — only a letter and a black-and-white photo of "
      "a young man. The young man was their grandfather. In the letter, he had written about his dreams for the future. "
      "That evening the whole family read the letter together, and grandfather laughed until he cried.")
R4 = ("Every Thursday afternoon a group of teenagers meets at the local community centre to teach older people how to use "
      "smartphones. The idea came from Leyla, a sixteen-year-old student, after her grandmother asked her for help with "
      "video calls for the tenth time. Now about fifteen pensioners come to each session. They learn how to send messages, "
      "take photos and pay bills online. The volunteers say patience is the most important skill. 'We explain the same "
      "thing many times, and that's fine,' says Leyla. The older learners, in return, share stories about their lives. "
      "Several of them have become good friends with the students.")
R5 = ("Honeybees are famous for making honey, but their most important job is pollination. When a bee visits a flower to "
      "collect nectar, tiny grains of pollen stick to its body. As it flies from flower to flower, it carries this pollen "
      "with it, which helps plants produce fruit and seeds. Many of the fruits and vegetables we eat depend on this "
      "process. Unfortunately, bee populations have fallen in many parts of the world. Scientists believe the main reasons "
      "are the use of certain pesticides, the loss of wild flowers and disease. Planting flowers in gardens and on "
      "balconies is one simple way that ordinary people can help bees.")
R6 = ("Since the pandemic, online learning has become a normal part of education. Supporters say it gives students "
      "freedom: they can watch lessons again, study at their own speed and learn from teachers in other cities or even "
      "other countries. Critics, however, point out that not every family has a fast internet connection or a quiet place "
      "to study. They also argue that students miss the social side of school — talking to friends, working in teams and "
      "asking questions face to face. Many experts now believe that the best approach is a mix of both: online materials "
      "for practice and classroom time for discussion and cooperation.")

READING = [
    ("Reading", "easy", "Where did Aysel work last summer?", "at a café near her school",
     ["at a supermarket", "in a library", "at her father's office", "in a computer shop"], "Birinci cümləyə baxın.", R1),
    ("Reading", "medium", "Why did Aysel want to quit after the first week?", "She found the job difficult and made mistakes.",
     ["She was paid too little.", "The owner was unkind.", "She was bored.", "She had too much homework."],
     "Çətinliklər və səhvlər (sınan stəkanlar) təsvir olunur.", R1),
    ("Reading", "medium", "What advice did Mr Kamal give her?", "to write orders down and carry fewer things",
     ["to work only in the mornings", "to find a different job", "to smile more at customers", "to buy a laptop"],
     "«He taught her to write orders down and to carry fewer things at once.»", R1),
    ("Reading", "hard", "What does the text suggest about Aysel by the end of the summer?", "She had become confident and skilled.",
     ["She still hated the job.", "She was dismissed.", "She opened her own café.", "She stopped going to school."],
     "O, kafenin ən sürətli ofisiantlarından biri olmuşdu.", R1),
    ("Reading", "easy", "What did Aysel buy with her money?", "a laptop", ["a phone", "a bicycle", "new clothes", "a tray"],
     "Son cümləyə baxın.", R1),
    ("Reading", "easy", "Where does most ocean plastic come from?", "from land",
     ["from ships", "from fishing nets only", "from the sky", "from sea animals"], "«Most of it comes from land…»", R2),
    ("Reading", "medium", "What are microplastics?", "tiny pieces of broken plastic",
     ["a type of jellyfish", "new plastic bottles", "plastic bags", "special fishing nets"], "Plastik kiçik hissəciklərə parçalanır.", R2),
    ("Reading", "medium", "Why do turtles sometimes eat plastic bags?", "The bags look like jellyfish.",
     ["They are very hungry.", "The bags taste sweet.", "They use them to build nests.", "They cannot see well."],
     "«…because they look like jellyfish.»", R2),
    ("Reading", "medium", "According to scientists, what is the best solution?", "producing and using less plastic",
     ["cleaning more beaches", "banning all fishing", "building more rivers", "feeding turtles"], "Son cümləyə baxın.", R2),
    ("Reading", "hard", "The word «effective» in the text is closest in meaning to ___.", "successful in producing a result",
     ["very expensive", "very fast", "difficult to understand", "easy to forget"], "Effective — səmərəli.", R2),
    ("Reading", "easy", "Where did Elvin find the box?", "in the attic", ["near the mill", "in the garden", "at school", "in a shop"],
     "Birinci cümləyə baxın.", R3),
    ("Reading", "medium", "What did Elvin think the cross on the map meant?", "hidden treasure",
     ["a grave", "a new house", "a dangerous place", "a well"], "«Elvin was sure it was hidden treasure.»", R3),
    ("Reading", "medium", "What was inside the metal tin?", "a letter and an old photo",
     ["gold coins", "a new map", "a key", "nothing"], "«…only a letter and a black-and-white photo…»", R3),
    ("Reading", "hard", "Who was the young man in the photo?", "their grandfather",
     ["their father", "the mill owner", "a famous actor", "a stranger"], "«The young man was their grandfather.»", R3),
    ("Reading", "hard", "How did grandfather feel when the family read the letter?", "He was amused and moved.",
     ["He was angry.", "He was bored.", "He was frightened.", "He was confused."], "«…laughed until he cried.»", R3),
    ("Reading", "easy", "When do the sessions take place?", "on Thursday afternoons",
     ["every morning", "at weekends", "on Monday evenings", "once a month"], "Birinci cümləyə baxın.", R4),
    ("Reading", "medium", "How did the idea start?", "Leyla's grandmother often asked her for help.",
     ["A teacher suggested it.", "The community centre paid students.", "Leyla saw it on TV.", "A phone company started it."],
     "Nənəsi video zənglər üçün dəfələrlə kömək istəmişdi.", R4),
    ("Reading", "easy", "About how many pensioners come to each session?", "fifteen",
     ["five", "ten", "twenty", "fifty"], "«…about fifteen pensioners come to each session.»", R4),
    ("Reading", "medium", "According to the volunteers, what is the most important skill?", "patience",
     ["speed", "technical knowledge", "strictness", "good English"], "«…patience is the most important skill.»", R4),
    ("Reading", "hard", "What do the older learners give the students in return?", "stories about their lives",
     ["money", "new phones", "lessons in maths", "food"], "«…share stories about their lives.»", R4),
    ("Reading", "easy", "What is the bees' most important job, according to the text?", "pollination",
     ["making honey", "building hives", "eating flowers", "producing wax"], "Birinci cümləyə baxın.", R5),
    ("Reading", "medium", "How does pollen travel between flowers?", "It sticks to bees' bodies.",
     ["The wind always carries it.", "Gardeners move it by hand.", "It falls into the soil.", "Bees eat it and grow it."],
     "«…tiny grains of pollen stick to its body.»", R5),
    ("Reading", "medium", "Which is NOT given as a reason for the fall in bee numbers?", "cold winters",
     ["certain pesticides", "loss of wild flowers", "disease", "use of chemicals on farms"],
     "Mətndə soyuq qışlar səbəb kimi göstərilmir.", R5),
    ("Reading", "medium", "How can ordinary people help bees?", "by planting flowers",
     ["by eating more honey", "by keeping bees at school", "by using more pesticides", "by cutting grass often"],
     "Son cümləyə baxın.", R5),
    ("Reading", "hard", "What is the main purpose of the text?", "to explain why bees matter and why they are in danger",
     ["to teach how to make honey", "to describe different types of flowers", "to sell pesticides", "to compare bees and wasps"],
     "Mətn arıların rolunu və təhlükələri izah edir.", R5),
    ("Reading", "easy", "What is one advantage of online learning mentioned in the text?", "Students can study at their own speed.",
     ["It is always free.", "It needs no internet.", "Teachers work less.", "Exams are easier."], "Tərəfdarların fikirlərinə baxın.", R6),
    ("Reading", "medium", "What problem do critics point out?", "Not every family has a good internet connection.",
     ["Online lessons are too short.", "Teachers cannot use computers.", "Students learn too fast.", "Books are too expensive."],
     "«…not every family has a fast internet connection…»", R6),
    ("Reading", "medium", "What do students miss in online learning, according to critics?", "the social side of school",
     ["homework", "school uniforms", "exams", "textbooks"], "«…students miss the social side of school…»", R6),
    ("Reading", "hard", "What approach do many experts now recommend?", "a mix of online and classroom learning",
     ["only online learning", "only classroom learning", "learning without teachers", "learning only at weekends"],
     "Son cümləyə baxın.", R6),
    ("Reading", "hard", "What is the writer's attitude in the text?", "balanced, showing both sides",
     ["strongly against online learning", "strongly in favour of online learning", "angry with teachers", "not interested in education"],
     "Müəllif hər iki tərəfin arqumentlərini verir.", R6),
]

if __name__ == "__main__":
    save(10, "en", [
        ("grammar", "Grammar", handwritten(10, "en", "grammar", "Grammar", GRAMMAR, 10201),
         "Conditionals, perfect tenses, passive, reported speech, modals of deduction, gerund və infinitive."),
        ("vocabulary", "Vocabulary", handwritten(10, "en", "vocabulary", "Vocabulary", VOCAB, 10202),
         "Phrasal verbs, collocations, word formation və tez qarışdırılan sözlər."),
        ("reading", "Reading", handwritten(10, "en", "reading", "Reading", READING, 10203),
         "Altı orijinal mətn üzrə detal, əsas fikir, söz mənası və nəticə çıxarma sualları."),
    ])
