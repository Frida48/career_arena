"""9-cu sinif ingilis dili: 3 bölmə × 30 orijinal sual."""
from common import handwritten, save

GRAMMAR = [
    ("Present Simple", "easy", "She ___ to school every day.", "goes", ["go", "is going", "gone", "going"],
     "Hər gün təkrarlanan iş — Present Simple; he/she/it ilə -s/-es artırılır."),
    ("Present Continuous", "easy", "Look! The children ___ in the garden.", "are playing",
     ["play", "plays", "played", "have played"], "«Look!» indi baş verən hərəkəti göstərir — Present Continuous."),
    ("Past Simple", "easy", "I ___ my homework yesterday evening.", "did", ["do", "have done", "am doing", "does"],
     "«Yesterday» keçmişdə bitmiş iş — Past Simple."),
    ("Past Continuous", "medium", "While I ___ TV, the phone rang.", "was watching",
     ["watched", "am watching", "watch", "have watched"], "Uzun davam edən keçmiş hərəkəti qısa hərəkət kəsir — Past Continuous."),
    ("Present Perfect", "easy", "I have lived here ___ 2015.", "since", ["for", "from", "ago", "during"],
     "Konkret başlanğıc nöqtəsi ilə «since» işlənir."),
    ("Present Perfect", "medium", "They ___ to London.", "have never been",
     ["never have been", "has never been", "never were been", "are never been"],
     "They + have + never + V3: have never been."),
    ("First Conditional", "medium", "If it rains tomorrow, we ___ at home.", "will stay",
     ["stay", "stayed", "would stay", "staying"], "Real şərt: If + Present Simple, will + V1."),
    ("Comparatives", "easy", "This book is ___ than that one.", "more interesting",
     ["interestinger", "most interesting", "more interestinger", "the more interesting"],
     "Uzun sifətlərdə müqayisə dərəcəsi «more» ilə düzəlir."),
    ("Superlatives", "easy", "Mount Everest is ___ mountain in the world.", "the highest",
     ["higher", "the higher", "highest", "the most high"], "Üstünlük dərəcəsi: the + -est."),
    ("Quantifiers", "easy", "There isn't ___ milk in the fridge.", "any", ["some", "many", "a", "few"],
     "İnkar cümlədə sayılmayan isimlə «any» işlənir."),
    ("Quantifiers", "easy", "How ___ apples do you need?", "many", ["much", "any", "lot", "more of"],
     "Sayılan isimlərlə «how many»."),
    ("Articles", "easy", "She is ___ honest girl.", "an", ["a", "the", "– (artikl lazım deyil)", "some"],
     "«Honest» sözündə h oxunmur, söz sait səslə başlayır — an."),
    ("Modals", "medium", "You ___ wear a uniform at school. It's a rule.", "must",
     ["can", "may", "might", "could"], "Qayda, məcburiyyət — must."),
    ("Passive Voice", "medium", "The letter ___ yesterday.", "was sent", ["sent", "is sent", "has sent", "sends"],
     "Keçmiş zamanda məchul növ: was/were + V3."),
    ("Passive Voice", "medium", "English ___ in many countries.", "is spoken",
     ["speaks", "spoke", "is speaking", "has spoke"], "İndiki zamanda məchul növ: is/are + V3."),
    ("Prepositions", "easy", "I'm interested ___ history.", "in", ["on", "at", "for", "of"],
     "Sabit birləşmə: interested in."),
    ("Prepositions", "medium", "We arrived ___ Baku at 6 p.m.", "in", ["to", "at the", "into", "on"],
     "Şəhər və ölkə adları ilə: arrive in."),
    ("Gerund / Infinitive", "medium", "He enjoys ___ football.", "playing", ["to play", "play", "played", "plays"],
     "«Enjoy» feilindən sonra -ing forması gəlir."),
    ("Gerund / Infinitive", "medium", "I want ___ a doctor.", "to become", ["becoming", "become", "became", "becomes"],
     "«Want» feilindən sonra to + V1 gəlir."),
    ("Prepositions", "easy", "My sister is good ___ maths.", "at", ["in", "on", "for", "with"], "Sabit birləşmə: good at."),
    ("Relative Clauses", "medium", "This is the boy ___ won the prize.", "who", ["which", "what", "whose", "where"],
     "İnsanlara aid budaq cümlədə «who» işlənir."),
    ("Future Forms", "medium", "I ___ to the cinema tomorrow; I've already bought tickets.", "am going",
     ["go", "went", "have gone", "was going"], "Əvvəlcədən planlaşdırılmış iş üçün Present Continuous işlənir."),
    ("Reported Speech", "hard", "She asked me where I ___.", "lived", ["live", "do live", "living", "am living"],
     "Vasitəli sualda zaman bir pillə geri çəkilir, söz sırası nəqli cümlədəki kimi olur."),
    ("Linking Words", "easy", "We didn't go out ___ it was raining.", "because", ["so", "but", "although", "or"],
     "Səbəb bildirir — because."),
    ("Linking Words", "medium", "___ she was tired, she finished her work.", "Although",
     ["Because", "So", "Despite", "But"], "Qarşılaşdırma: although + cümlə. «Despite»dən sonra isim gəlir."),
    ("Subject–Verb Agreement", "hard", "Neither Ali nor his friends ___ at home.", "were",
     ["was", "is", "has been", "be"], "Neither…nor quruluşunda feil özünə yaxın mübtədaya (friends) uyğunlaşır."),
    ("Present Perfect", "easy", "He has just ___ his breakfast.", "finished",
     ["finish", "finishing", "finishes", "to finish"], "Have/has + V3."),
    ("Indirect Questions", "hard", "Could you tell me what time ___?", "it is",
     ["is it", "it does", "does it be", "it be"], "Dolayı sualda söz sırası nəqli cümlədəki kimidir: it is."),
    ("Present Perfect Continuous", "medium", "I've been waiting for you ___ two hours.", "for",
     ["since", "during", "ago", "from"], "Müddət bildirəndə «for» işlənir."),
    ("Past Continuous", "medium", "At 8 o'clock last night, I ___ dinner.", "was having",
     ["have", "am having", "will have", "have had"], "Keçmişdə konkret anda davam edən hərəkət — Past Continuous."),
]

VOCAB = [
    ("Synonyms", "easy", "Choose the synonym of «huge».", "enormous", ["tiny", "narrow", "weak", "quiet"],
     "Huge = enormous (çox böyük)."),
    ("Antonyms", "easy", "Choose the antonym of «ancient».", "modern", ["old", "historic", "antique", "aged"],
     "Ancient (qədim) — modern (müasir)."),
    ("Collocations", "easy", "I need to ___ a decision.", "make", ["do", "say", "tell", "get"], "Sabit birləşmə: make a decision."),
    ("Collocations", "easy", "Please ___ attention to the board.", "pay", ["do", "make", "take", "put"],
     "Sabit birləşmə: pay attention."),
    ("Collocations", "easy", "She ___ the bus to work every morning.", "takes", ["does", "makes", "brings", "walks"],
     "Nəqliyyatdan istifadə: take the bus."),
    ("Phrasal Verbs", "easy", "Please ___ your shoes before entering the room.", "take off",
     ["take on", "turn off", "look after", "give up"], "Take off — (paltarı, ayaqqabını) çıxarmaq."),
    ("Phrasal Verbs", "easy", "Can you ___ my cat while I'm away?", "look after",
     ["look for", "look up", "look at", "look out"], "Look after — qayğısına qalmaq."),
    ("Phrasal Verbs", "medium", "I'm ___ my keys. Have you seen them?", "looking for",
     ["looking after", "looking up", "looking forward", "looking at"], "Look for — axtarmaq."),
    ("Verbs", "medium", "We ___ a lot of money on our holiday.", "spent", ["paid", "bought", "cost", "lent"],
     "Spend money on something — nəyəsə pul xərcləmək."),
    ("Word Formation", "easy", "He is a very ___ person. He always helps others. (HELP)", "helpful",
     ["helpless", "helping", "helper", "helped"], "Helpful — köməksevər (sifət)."),
    ("Word Formation", "medium", "The ___ of the city is about two million. (POPULATE)", "population",
     ["populate", "popular", "populous", "populating"], "Artikldan sonra isim lazımdır: population (əhali)."),
    ("Word Formation", "easy", "She answered the question ___. (CORRECT)", "correctly",
     ["correct", "correction", "corrected", "correctness"], "Feili təsvir edən söz zərf olmalıdır: correctly."),
    ("-ed / -ing Adjectives", "medium", "It was a ___ film; I fell asleep.", "boring",
     ["bored", "bore", "boredom", "bores"], "Əşyanın xüsusiyyəti -ing ilə ifadə olunur: boring film."),
    ("-ed / -ing Adjectives", "medium", "I was very ___ when I heard the news.", "surprised",
     ["surprising", "surprise", "surprisingly", "surprises"], "İnsanın hissi -ed ilə ifadə olunur: I was surprised."),
    ("Word Groups", "easy", "Which word does not belong to the group: apple, banana, carrot, orange, grape?", "carrot",
     ["apple", "banana", "orange", "grape"], "Carrot tərəvəzdir, digərləri meyvədir."),
    ("Jobs", "easy", "A person who designs buildings is called an ___.", "architect",
     ["engineer", "electrician", "mechanic", "pilot"], "Architect — memar."),
    ("Places", "easy", "A place where you can borrow books is a ___.", "library",
     ["bookshop", "bakery", "museum", "pharmacy"], "Library — kitabxana; bookshop-da kitab satılır."),
    ("Antonyms", "easy", "The opposite of «cheap» is ___.", "expensive", ["free", "poor", "low", "easy"],
     "Cheap (ucuz) — expensive (bahalı)."),
    ("Meaning", "easy", "«Exhausted» means ___.", "very tired", ["very happy", "very hungry", "very angry", "very bored"],
     "Exhausted — çox yorğun."),
    ("Meaning", "medium", "«Purchase» means ___.", "buy", ["sell", "borrow", "lend", "rent"], "Purchase — satın almaq."),
    ("Meaning", "medium", "Which word means «to say that you are sorry»?", "apologize",
     ["complain", "promise", "refuse", "admit"], "Apologize — üzr istəmək."),
    ("Adjectives", "easy", "The weather was so ___ that we stayed inside.", "awful",
     ["pleasant", "sunny", "warm", "lovely"], "Evdə qalmağın səbəbi pis havadır: awful."),
    ("Say / Tell", "medium", "My grandfather ___ a lot of interesting stories.", "tells",
     ["says", "speaks", "talks", "chats"], "Sabit birləşmə: tell a story."),
    ("Borrow / Lend", "medium", "Can I ___ your pen for a minute?", "borrow", ["lend", "rent", "owe", "give"],
     "Borrow — (kiminsə əşyasını) müvəqqəti götürmək."),
    ("Verbs", "easy", "He ___ the exam because he didn't study.", "failed", ["passed", "won", "lost", "succeeded"],
     "Oxumadığı üçün imtahandan kəsildi: failed."),
    ("Environment", "easy", "We should ___ energy by turning off the lights.", "save",
     ["spend", "waste", "keep up", "break"], "Save energy — enerjiyə qənaət etmək."),
    ("Irregular Plurals", "easy", "The plural of «child» is ___.", "children",
     ["childs", "childes", "childrens", "childer"], "Child — children (qeyri-qaydalı cəm)."),
    ("Adverbs of Frequency", "easy", "«Rarely» means ___.", "not often", ["always", "usually", "often", "every day"],
     "Rarely — nadir hallarda."),
    ("Adjectives + Prepositions", "medium", "She screams when she sees spiders. She is ___ of them.", "afraid",
     ["fond", "proud", "tired", "jealous"], "Be afraid of — qorxmaq."),
    ("Parts of Speech", "easy", "Which word is a noun?", "happiness", ["happy", "happily", "happen", "unhappy"],
     "-ness şəkilçisi isim düzəldir."),
]

P1 = ("Nigar lives on the ninth floor of a tall building in Baku, so she has no garden. Two years ago she decided "
      "to grow vegetables on her balcony. She started with tomatoes and herbs in old plastic boxes. At first, most of "
      "the plants died because they got too much sun in the afternoon. Nigar read about the problem and moved the boxes "
      "to the shady side of the balcony. She also began to water them early in the morning instead of in the evening. "
      "Now her balcony is full of green leaves, and her family eats fresh salad almost every day. Last spring Nigar "
      "showed her neighbours how to start their own balcony gardens.")
P2 = ("Every Saturday a big blue bus stops in the centre of a small village near Shamakhi. It is not an ordinary bus — "
      "it is a library on wheels. Inside, there are shelves with about two thousand books, two computers and a small "
      "table for children. The village has no library of its own, so the bus is very popular. People can borrow up to "
      "three books for two weeks. The driver, Mr Rauf, is also the librarian. He says that the most popular books are "
      "adventure stories for teenagers and cookery books for adults. In winter, when the roads are icy, the bus "
      "sometimes cannot come, and the villagers say they really miss it.")
P3 = ("The robotics club at School No. 47 meets twice a week after lessons. This year twelve students are preparing "
      "for a national competition in which robots must find their way through a maze. The team's first robot was fast "
      "but kept hitting the walls. The students then added two extra sensors, which made the robot slower but much more "
      "accurate. Their teacher, Ms Leyla, does not write any code for them. She only asks questions and helps them test "
      "their ideas. 'When the robot fails, we learn the most,' says Murad, the youngest member of the team. The "
      "competition will take place in March, and the club is now looking for a sponsor to pay for new parts.")
P4 = ("Camels are well suited to life in the desert. Contrary to a popular belief, a camel's hump does not hold water. "
      "It stores fat, which the animal can use for energy when there is little food. Camels can go for many days without "
      "drinking, and when they finally find water, they can drink a very large amount in a few minutes. Their long "
      "eyelashes and the ability to close their noses protect them from sand during storms. Wide, soft feet help them "
      "walk on hot sand without sinking. Because of these features, people in desert regions have used camels for "
      "transport for thousands of years.")
P5 = ("Scientists say that teenagers need between eight and ten hours of sleep every night, but many get much less. "
      "One reason is that the body clock changes during the teenage years, so young people naturally feel sleepy later "
      "in the evening. Another reason is the use of phones and tablets in bed. The light from screens tells the brain "
      "that it is still daytime. Lack of sleep can make it harder to concentrate, remember new information and control "
      "emotions. Doctors advise teenagers to go to bed at the same time every day, to keep their phones out of the "
      "bedroom and to avoid drinks with caffeine in the evening.")
P6 = ("The Palace of the Shaki Khans is one of the most famous historical buildings in Azerbaijan. It was built in the "
      "18th century as a summer residence for the rulers of Shaki. The palace is not very large, but it is famous for "
      "its colourful wall paintings and its shebeke windows. Shebeke is a traditional art in which small pieces of "
      "coloured glass are fitted into a wooden frame without nails or glue. When sunlight passes through the windows, "
      "the rooms fill with red, blue and green light. Today the palace is a museum, and tourists from many countries "
      "visit it every year.")

READING = [
    ("Reading", "easy", "Why did Nigar start growing vegetables on her balcony?", "She had no garden.",
     ["Vegetables were expensive.", "Her teacher asked her to.", "Her neighbours had balcony gardens.", "She wanted to sell them."],
     "Mətndə deyilir: doqquzuncu mərtəbədə yaşadığı üçün bağı yoxdur.", P1),
    ("Reading", "medium", "Why did most of the plants die at first?", "They got too much afternoon sun.",
     ["They did not get enough water.", "The boxes were too small.", "It was too cold on the balcony.", "Insects ate them."],
     "«…because they got too much sun in the afternoon.»", P1),
    ("Reading", "medium", "What did Nigar change about watering?", "She watered the plants early in the morning.",
     ["She watered them twice a day.", "She stopped watering them.", "She used rainwater only.", "She watered them in the evening."],
     "«…water them early in the morning instead of in the evening.»", P1),
    ("Reading", "easy", "The word «shady» in the text is closest in meaning to ___.", "out of direct sunlight",
     ["very windy", "very wet", "full of plants", "near the street"], "Shady — kölgəli, birbaşa günəş düşməyən.", P1),
    ("Reading", "medium", "What did Nigar do last spring?", "She taught her neighbours to start balcony gardens.",
     ["She moved to a house with a garden.", "She sold salad to her neighbours.", "She bought new plastic boxes.", "She started growing tomatoes."],
     "Son cümləyə baxın.", P1),
    ("Reading", "easy", "What is special about the blue bus?", "It is a library.",
     ["It is a school.", "It is a shop.", "It is a hospital.", "It is a restaurant."], "«…it is a library on wheels.»", P2),
    ("Reading", "easy", "How many books can a person borrow at one time?", "three", ["two", "four", "five", "ten"],
     "«People can borrow up to three books…»", P2),
    ("Reading", "medium", "Who is Mr Rauf?", "the driver and the librarian",
     ["the head of the village", "a teacher", "a writer of cookery books", "a computer engineer"],
     "«The driver, Mr Rauf, is also the librarian.»", P2),
    ("Reading", "medium", "Which books are most popular with adults?", "cookery books",
     ["adventure stories", "history books", "computer books", "children's books"], "Böyüklər arasında yemək kitabları populyardır.", P2),
    ("Reading", "medium", "Why does the bus sometimes not come in winter?", "The roads are icy.",
     ["The driver is on holiday.", "There are no readers.", "The bus is too cold.", "The books are returned."],
     "«…when the roads are icy, the bus sometimes cannot come…»", P2),
    ("Reading", "easy", "What must the robots do in the competition?", "find their way through a maze",
     ["play football", "carry heavy boxes", "draw pictures", "answer questions"], "«…robots must find their way through a maze.»", P3),
    ("Reading", "medium", "What was the problem with the first robot?", "It kept hitting the walls.",
     ["It was too slow.", "It was too heavy.", "It had no sensors.", "It was too expensive."], "«…was fast but kept hitting the walls.»", P3),
    ("Reading", "medium", "What happened after the students added two sensors?", "The robot became slower but more accurate.",
     ["The robot became faster.", "The robot stopped working.", "The robot broke the walls.", "Nothing changed."],
     "«…made the robot slower but much more accurate.»", P3),
    ("Reading", "hard", "How does Ms Leyla help the team?", "She asks questions and helps them test ideas.",
     ["She writes the code for them.", "She builds the robot herself.", "She pays for new parts.", "She chooses the team members."],
     "«She only asks questions and helps them test their ideas.»", P3),
    ("Reading", "medium", "What is the club looking for now?", "a sponsor", ["a new teacher", "new members", "a bigger room", "a maze"],
     "Son cümlə: «…looking for a sponsor to pay for new parts.»", P3),
    ("Reading", "easy", "What does a camel's hump store?", "fat", ["water", "sand", "milk", "air"],
     "«It stores fat…»", P4),
    ("Reading", "medium", "What popular belief does the text say is wrong?", "that the hump holds water",
     ["that camels live in deserts", "that camels have long eyelashes", "that camels can carry people", "that camels have wide feet"],
     "«Contrary to a popular belief, a camel's hump does not hold water.»", P4),
    ("Reading", "medium", "What helps camels during sandstorms?", "long eyelashes and noses they can close",
     ["their humps", "their wide feet", "their thick tails", "their short legs"], "Kirpiklər və burnu bağlaya bilməsi.", P4),
    ("Reading", "medium", "Why don't camels sink in hot sand?", "Their feet are wide and soft.",
     ["They walk very fast.", "They are very light.", "They walk only at night.", "Their legs are short."], "«Wide, soft feet help them…»", P4),
    ("Reading", "hard", "What is the main idea of the text?", "Camels have features that help them live in the desert.",
     ["Camels are dangerous animals.", "Deserts are very hot.", "Camels need a lot of water every day.", "People no longer use camels."],
     "Mətn dəvənin səhra həyatına uyğunlaşmasından bəhs edir.", P4),
    ("Reading", "easy", "How many hours of sleep do teenagers need?", "8–10 hours",
     ["5–6 hours", "6–7 hours", "11–12 hours", "about 4 hours"], "«…between eight and ten hours…»", P5),
    ("Reading", "medium", "Why do teenagers feel sleepy later in the evening?", "Their body clock changes.",
     ["They drink too much water.", "They do too much sport.", "Their schools start late.", "They eat too much."],
     "«…the body clock changes during the teenage years…»", P5),
    ("Reading", "medium", "How does screen light affect the brain?", "It makes the brain think it is still day.",
     ["It helps the brain relax.", "It improves memory.", "It makes people hungry.", "It has no effect."],
     "«The light from screens tells the brain that it is still daytime.»", P5),
    ("Reading", "medium", "According to the text, lack of sleep can make it harder to ___.", "control emotions",
     ["see clearly", "run fast", "eat properly", "speak foreign languages"],
     "«…harder to concentrate, remember new information and control emotions.»", P5),
    ("Reading", "medium", "Which piece of advice is given in the text?", "Keep phones out of the bedroom.",
     ["Sleep only at weekends.", "Drink coffee before bed.", "Use a tablet to fall asleep.", "Go to bed at different times."],
     "Həkimlər telefonu yataq otağından kənarda saxlamağı məsləhət görür.", P5),
    ("Reading", "easy", "When was the palace built?", "in the 18th century",
     ["in the 16th century", "in the 19th century", "in the 20th century", "two years ago"], "«It was built in the 18th century…»", P6),
    ("Reading", "medium", "What was the palace used for originally?", "a summer residence for the rulers",
     ["a school", "a museum", "a hotel for tourists", "a glass factory"], "«…as a summer residence for the rulers of Shaki.»", P6),
    ("Reading", "medium", "What is shebeke?", "an art of fitting coloured glass into wooden frames",
     ["a type of wall painting", "a kind of carpet", "a traditional dance", "a building material made of stone"],
     "Mətndə şəbəkənin tərifi verilir.", P6),
    ("Reading", "hard", "What is NOT used to make shebeke?", "nails", ["wood", "coloured glass", "small pieces of glass", "a wooden frame"],
     "«…without nails or glue.»", P6),
    ("Reading", "easy", "What is the palace today?", "a museum", ["a school", "a hotel", "a library", "a home for the rulers"],
     "«Today the palace is a museum…»", P6),
]

if __name__ == "__main__":
    save(9, "en", [
        ("grammar", "Grammar", handwritten(9, "en", "grammar", "Grammar", GRAMMAR, 9201)),
        ("vocabulary", "Vocabulary", handwritten(9, "en", "vocabulary", "Vocabulary", VOCAB, 9202)),
        ("reading", "Reading", handwritten(9, "en", "reading", "Reading", READING, 9203)),
    ])
