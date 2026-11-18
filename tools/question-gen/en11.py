"""11-ci sinif ingilis dili: 3 bölmə × 30 orijinal sual (B1+/B2 səviyyəsi)."""
from common import handwritten, save

GRAMMAR = [
    ("Third Conditional", "medium", "If I had known about the meeting, I ___ it.", "would have attended",
     ["would attend", "had attended", "will attend", "attended"], "Keçmişə aid qeyri-real şərt: would have + V3."),
    ("Mixed Conditionals", "hard", "If she ___ harder last year, she would be at university now.", "had studied",
     ["studied", "has studied", "would study", "studies"], "Qarışıq şərt: keçmiş şərt (Past Perfect) → indiki nəticə."),
    ("Wishes", "medium", "I wish I ___ that rude comment yesterday.", "hadn't made",
     ["didn't make", "haven't made", "wouldn't make", "don't make"], "Keçmişə peşmanlıq: wish + Past Perfect."),
    ("Inversion", "hard", "Not only ___ the exam, but she also got the highest score.", "did she pass",
     ["she passed", "she did pass", "passed she", "has she passed"], "«Not only» cümlənin əvvəlində gəldikdə inversiya olur."),
    ("Inversion", "hard", "Hardly ___ home when it started to rain.", "had we got",
     ["we had got", "did we get", "we got", "have we got"], "Hardly … when quruluşunda Past Perfect ilə inversiya."),
    ("Future Perfect Passive", "hard", "The report ___ by the time the manager arrives.", "will have been finished",
     ["will finish", "is finished", "has finished", "will be finishing"], "Gələcəkdə müəyyən andan əvvəl bitəcək iş, məchul növ."),
    ("Passive Reporting", "medium", "She is said ___ fluent in five languages.", "to be",
     ["being", "be", "to being", "that she is"], "Be said + to + V1."),
    ("Gerund / Infinitive", "medium", "He denied ___ the window.", "breaking",
     ["to break", "break", "broke", "to have broke"], "«Deny»dən sonra -ing."),
    ("Gerund / Infinitive", "hard", "I remember ___ him at the party last year.", "meeting",
     ["to meet", "meet", "met", "to have meet"], "Remember + -ing — keçmişdə olanı xatırlamaq."),
    ("Gerund / Infinitive", "hard", "Remember ___ the door when you leave.", "to lock",
     ["locking", "lock", "locked", "to locking"], "Remember + to — gələcəkdə ediləcək işi unutmamaq."),
    ("Unreal Past", "hard", "It's high time we ___ home.", "went",
     ["go", "will go", "have gone", "going"], "«It's high time» + Past Simple (indiki mənada)."),
    ("Unreal Past", "hard", "I'd rather you ___ smoke here.", "didn't",
     ["don't", "won't", "not", "haven't"], "Would rather + başqa şəxs + Past Simple."),
    ("Relative Clauses", "medium", "The man ___ car was stolen called the police.", "whose",
     ["who", "which", "whom", "that"], "Sahiblik bildirir — whose."),
    ("Reported Questions", "medium", "She asked me where ___.", "I had been",
     ["had I been", "I have been", "was I", "have I been"], "Vasitəli sualda söz sırası nəqli cümlədəki kimidir, zaman geri çəkilir."),
    ("Reported Commands", "medium", "He told me ___ late again.", "not to be",
     ["don't be", "not be", "to not being", "no to be"], "Vasitəli inkar əmr: told + obyekt + not to + V1."),
    ("Linking Words", "medium", "___ it was raining, they continued the match.", "Even though",
     ["Despite", "In spite", "However", "Because of"], "Even though + cümlə; despite + isim."),
    ("Linking Words", "medium", "___ the bad weather, the flight left on time.", "Despite",
     ["Although", "Even though", "However", "Whereas"], "Despite + isim (birləşmə)."),
    ("Inverted Conditionals", "hard", "Had I known, I ___ you.", "would have told",
     ["will tell", "had told", "would tell", "told"], "Had I known = If I had known → would have + V3."),
    ("Future Perfect", "medium", "By next June, I ___ here for ten years.", "will have worked",
     ["will work", "am working", "have worked", "work"], "Gələcəkdəki bir ana qədər tamamlanmış müddət."),
    ("Modals (Past)", "hard", "You ___ have bought milk; there's plenty in the fridge.", "needn't",
     ["mustn't", "can't", "couldn't", "wouldn't"], "Needn't have + V3 — lazım olmayan iş görülüb."),
    ("Modals (Past)", "hard", "She ___ have taken the bus — she always walks.", "can't",
     ["must", "should", "needn't", "would"], "Can't have + V3 — keçmişə dair inamlı inkar ehtimal."),
    ("Passive Voice", "medium", "The problem ___ at the moment.", "is being discussed",
     ["is discussing", "discusses", "has discussed", "is discussed being"], "Present Continuous Passive: is being + V3."),
    ("Be used to", "medium", "I'm not used to ___ in such a big city.", "living",
     ["live", "lived", "to live", "be living"], "Be used to + -ing."),
    ("Inversion", "hard", "Scarcely had the show begun ___ the lights went out.", "when",
     ["than", "then", "that", "as"], "Scarcely … when."),
    ("Inversion", "hard", "No sooner had I sat down ___ the phone rang.", "than",
     ["when", "then", "that", "as"], "No sooner … than."),
    ("Suggest", "medium", "She suggested ___ to the museum.", "going",
     ["to go", "we to go", "go", "went"], "Suggest + -ing (və ya suggest that we go)."),
    ("Inverted Conditionals", "hard", "Were I in your position, I ___ the offer.", "would accept",
     ["will accept", "accepted", "had accepted", "accept"], "Were I = If I were → would + V1."),
    ("Gerund", "medium", "There's no point ___ about it now.", "worrying",
     ["to worry", "worry", "worried", "of worry"], "There's no point (in) + -ing."),
    ("Comparatives", "easy", "The more you read, ___ your vocabulary will be.", "the richer",
     ["richer", "the richest", "more rich", "most rich"], "The more …, the + müqayisə dərəcəsi."),
    ("Relative Clauses", "hard", "He's the person ___ I spoke on the phone.", "to whom",
     ["whom", "who", "which", "to which"], "Rəsmi üslubda önlük «whom»dan əvvəl gəlir: to whom."),
]

VOCAB = [
    ("Idioms", "easy", "«A piece of cake» means ___.", "very easy",
     ["very sweet", "very small", "very expensive", "very boring"], "A piece of cake — çox asan iş."),
    ("Idioms", "medium", "«To break the ice» means ___.", "to start a friendly conversation",
     ["to damage something", "to feel very cold", "to end a relationship", "to win a game"], "Break the ice — tanışlıqda gərginliyi aradan qaldırmaq."),
    ("Idioms", "medium", "«Once in a blue moon» means ___.", "very rarely",
     ["every month", "at night", "very quickly", "always"], "Once in a blue moon — çox nadir hallarda."),
    ("Idioms", "medium", "«To hit the books» means ___.", "to study hard",
     ["to throw books", "to buy books", "to write a book", "to stop reading"], "Hit the books — ciddi oxumaq."),
    ("Word Choice", "medium", "She was ___ by the beauty of the landscape.", "overwhelmed",
     ["overworked", "overdone", "overcharged", "overslept"], "Overwhelmed — heyran qalmış, sarsılmış."),
    ("Phrasal Verbs", "medium", "The company decided to ___ 50 new employees.", "take on",
     ["take off", "take after", "take in", "take over"], "Take on — işə götürmək."),
    ("Phrasal Verbs", "medium", "I need to ___ my French before the trip.", "brush up on",
     ["brush off", "brush away", "brush down", "brush aside"], "Brush up on — biliyi təzələmək."),
    ("Phrasal Verbs", "easy", "The plane ___ at 6 a.m.", "took off",
     ["took on", "took over", "took up", "took out"], "Take off — (təyyarə) havaya qalxmaq."),
    ("Phrasal Verbs", "medium", "We must ___ a solution to this problem.", "come up with",
     ["come across", "come down with", "come round", "come into"], "Come up with — (fikir, həll) tapmaq."),
    ("Phrasal Verbs", "medium", "He ___ with flu last week.", "came down",
     ["came up", "came across", "came over", "came into"], "Come down with — xəstələnmək."),
    ("Word Formation", "easy", "The ___ of the new medicine has saved many lives. (DISCOVER)", "discovery",
     ["discover", "discoverer", "discovered", "discovering"], "Artikldan sonra isim: discovery."),
    ("Word Formation", "medium", "Her ___ to help others is admirable. (WILLING)", "willingness",
     ["willing", "willingly", "unwilling", "will"], "Willingness — hazır olma, istək."),
    ("Word Formation", "medium", "The results were ___; nobody expected them. (PREDICT)", "unpredictable",
     ["predictable", "prediction", "predicted", "predicting"], "Heç kim gözləmirdi — inkar sifət: unpredictable."),
    ("Word Formation", "hard", "His explanation was completely ___. I didn't understand anything. (COMPREHEND)", "incomprehensible",
     ["comprehensive", "comprehension", "comprehensible", "comprehending"], "Incomprehensible — anlaşılmaz."),
    ("Word Formation", "easy", "The city is famous for its ___ architecture. (IMPRESS)", "impressive",
     ["impression", "impressed", "impress", "impressively"], "İsimdən əvvəl sifət: impressive."),
    ("Collocations", "easy", "Sometimes you have to ___ a risk to succeed.", "take",
     ["make", "do", "give", "get"], "Sabit birləşmə: take a risk."),
    ("Collocations", "medium", "It's too early to ___ a conclusion.", "draw",
     ["pull", "give", "do", "put"], "Sabit birləşmə: draw a conclusion."),
    ("Collocations", "easy", "The match was cancelled because of heavy ___.", "rain",
     ["sun", "sky", "heat", "light"], "Sabit birləşmə: heavy rain."),
    ("Synonyms", "medium", "Choose the synonym of «obsolete».", "outdated",
     ["modern", "essential", "popular", "complicated"], "Obsolete — köhnəlmiş."),
    ("Synonyms", "easy", "Choose the synonym of «diligent».", "hard-working",
     ["lazy", "clever", "careless", "talkative"], "Diligent — çalışqan."),
    ("Antonyms", "medium", "Choose the antonym of «scarce».", "plentiful",
     ["rare", "limited", "expensive", "tiny"], "Scarce (az, qıt) — plentiful (bol)."),
    ("Meaning", "medium", "«Reluctant» means ___.", "unwilling",
     ["eager", "angry", "happy", "tired"], "Reluctant — istəksiz."),
    ("Meaning", "medium", "The verb «to enhance» is closest in meaning to ___.", "to improve",
     ["to reduce", "to destroy", "to hide", "to measure"], "Enhance — yaxşılaşdırmaq, artırmaq."),
    ("Confusing Words", "hard", "The government plans to ___ taxes on sugary drinks.", "impose",
     ["impress", "import", "implore", "imply"], "Impose a tax — vergi tətbiq etmək."),
    ("Confusing Words", "medium", "The medicine had a strong ___ on him.", "effect",
     ["affect", "effort", "effective", "affection"], "Effect (isim) — təsir; affect — feildir."),
    ("Confusing Words", "medium", "The ___ of the event is to raise money for charity.", "purpose",
     ["propose", "porpoise", "suppose", "purchase"], "Purpose — məqsəd."),
    ("Word Choice", "medium", "She has a ___ for languages; she learns them very easily.", "gift",
     ["present", "price", "prize", "prise"], "Have a gift for something — nəyəsə qabiliyyəti olmaq."),
    ("Dependent Prepositions", "medium", "He was accused ___ stealing the money.", "of",
     ["for", "with", "about", "on"], "Accuse somebody of something."),
    ("Dependent Prepositions", "easy", "The success of the project depends ___ teamwork.", "on",
     ["of", "from", "in", "at"], "Depend on."),
    ("Word Choice", "medium", "Despite the difficulties, they ___ to finish the project on time.", "managed",
     ["succeeded", "achieved", "reached", "won"], "Manage to do something; «succeed» isə «in + -ing» ilə işlənir."),
]

R1 = ("When companies first sent their staff home to work, many managers expected productivity to fall. In many cases the "
      "opposite happened. Without long commutes, employees had more time and energy, and some reported finishing tasks "
      "faster in a quiet home environment. Yet remote work has a less visible cost. Younger workers, in particular, say "
      "they learn less because they cannot simply watch and ask experienced colleagues. Casual conversations by the coffee "
      "machine, which often produce new ideas, have largely disappeared. As a result, a growing number of firms now ask "
      "employees to come to the office two or three days a week, hoping to keep the benefits of both worlds.")
R2 = ("On a summer afternoon, the centre of a large city can be several degrees hotter than the countryside around it. This "
      "effect is known as an urban heat island. Concrete, asphalt and dark roofs absorb sunlight during the day and release "
      "the heat slowly at night, so cities cool down far less than rural areas. Cars, air conditioners and factories add "
      "even more heat. The consequences are serious: higher energy bills, poorer air quality and greater health risks for "
      "elderly people. Fortunately, there are solutions. Planting trees, creating parks and painting roofs in light colours "
      "can noticeably reduce temperatures, while green roofs covered with plants also help to absorb rainwater.")
R3 = ("Kamran had practised the violin piece for months, but as he waited behind the curtain, his hands were shaking. He "
      "could hear the audience whispering and imagined every possible mistake. His teacher noticed his face and quietly "
      "told him to breathe slowly and to focus on the first four notes only — not on the whole performance. When Kamran "
      "stepped onto the stage, he followed her advice. The first notes sounded weak, but gradually his confidence returned. "
      "He made one small mistake in the middle, yet he kept playing. When he finished, the hall burst into applause. "
      "Later he admitted that the mistake had taught him something: a performance does not need to be perfect to move people.")
R4 = ("For more than a thousand years, the network of trade routes known as the Silk Road connected China with the "
      "Mediterranean. Merchants carried silk, spices, paper and porcelain westwards, while glassware, wool and precious "
      "metals travelled east. Few traders crossed the entire route; instead, goods passed from hand to hand through many "
      "cities. Along the way, caravanserais — roadside inns with rooms for travellers and space for their animals — offered "
      "shelter and safety. However, the Silk Road was not only about goods. Religions, languages, scientific knowledge and "
      "even recipes spread along it, which is why historians often describe it as one of the first great channels of "
      "cultural exchange.")
R5 = ("Every day, millions of people share news stories online without checking whether they are true. False information "
      "often spreads faster than accurate reports because it is designed to provoke strong emotions such as fear or anger. "
      "Experts recommend a few simple habits. First, check who published the story and whether the source is known for "
      "reliable reporting. Second, look for the same news on other trusted websites. Third, pay attention to the date: old "
      "stories are sometimes shared as if they were new. Finally, be suspicious of headlines that seem too shocking to be "
      "true. Taking thirty seconds to think before sharing can stop a false story from reaching thousands of people.")
R6 = ("It is commonly believed that children learn foreign languages more easily than adults. In some ways this is true: "
      "young children often develop a more natural accent. However, research suggests that adults have important "
      "advantages too. They can understand grammar rules more quickly, use learning strategies consciously and connect "
      "new words to knowledge they already have. The main obstacles for adult learners are often not biological but "
      "practical: lack of time, fear of making mistakes and fewer chances to practise. Teachers therefore advise adults "
      "to set small, regular goals, to accept errors as part of learning and to find real situations in which to use the language.")

READING = [
    ("Reading", "medium", "What did many managers expect when staff started working from home?", "a fall in productivity",
     ["higher salaries", "more office space", "longer commutes", "more meetings"], "Birinci cümləyə baxın.", R1),
    ("Reading", "medium", "Why did some employees finish tasks faster at home?", "They had more time and a quieter environment.",
     ["They worked at night.", "Their managers helped them more.", "They had better computers.", "They worked fewer hours."],
     "Uzun yol olmadığı üçün vaxt və enerji artdı.", R1),
    ("Reading", "hard", "What is the «less visible cost» of remote work?", "Younger workers learn less from experienced colleagues.",
     ["Electricity bills increase.", "Offices become empty.", "Employees work too slowly.", "Managers lose their jobs."],
     "Gənc işçilər təcrübəli həmkarlarını izləyib soruşa bilmir.", R1),
    ("Reading", "medium", "According to the text, what often produced new ideas?", "casual conversations in the office",
     ["formal meetings", "online training", "long commutes", "working alone"], "«Casual conversations by the coffee machine…»", R1),
    ("Reading", "hard", "Why do many firms now ask staff to come in two or three days a week?", "to combine the advantages of both ways of working",
     ["to save money on rent", "to punish lazy workers", "to stop remote work completely", "because employees asked for it"],
     "«…hoping to keep the benefits of both worlds.»", R1),
    ("Reading", "easy", "What is an urban heat island?", "a city area that is hotter than the countryside around it",
     ["an island in a hot sea", "a park in the city centre", "a type of air conditioner", "a cold area in a city"],
     "Birinci iki cümləyə baxın.", R2),
    ("Reading", "medium", "Why do cities cool down less at night?", "Buildings and roads release stored heat slowly.",
     ["There is more wind in cities.", "People switch off their lights.", "There is no sun in the evening.", "Rivers keep cities warm."],
     "Beton və asfalt günün istiliyini gecə yavaş-yavaş buraxır.", R2),
    ("Reading", "medium", "Which consequence is mentioned in the text?", "higher energy bills",
     ["more tourists", "cheaper housing", "colder winters", "less traffic"], "Nəticələr sırasına baxın.", R2),
    ("Reading", "medium", "Which solution is NOT mentioned?", "building taller buildings",
     ["planting trees", "creating parks", "painting roofs in light colours", "green roofs"], "Mətndə hündür binalar həll kimi göstərilmir.", R2),
    ("Reading", "hard", "What is the tone of the last part of the text?", "hopeful",
     ["angry", "humorous", "sad", "indifferent"], "«Fortunately, there are solutions.»", R2),
    ("Reading", "easy", "How did Kamran feel before the performance?", "very nervous",
     ["bored", "relaxed", "angry", "sleepy"], "Əlləri titrəyirdi.", R3),
    ("Reading", "medium", "What did his teacher advise him to do?", "breathe slowly and focus on the first few notes",
     ["practise the whole piece again", "play faster than usual", "look at the audience", "cancel the performance"],
     "Müəllim nəfəs almağı və ilk dörd nota fikir verməyi məsləhət gördü.", R3),
    ("Reading", "medium", "What happened in the middle of the performance?", "He made a small mistake but continued.",
     ["He stopped and left the stage.", "A string broke.", "The audience laughed.", "His teacher joined him."],
     "«He made one small mistake… yet he kept playing.»", R3),
    ("Reading", "hard", "The phrase «burst into applause» suggests that the audience ___.", "suddenly started clapping loudly",
     ["left the hall quickly", "remained silent", "started to sing", "complained about the mistake"], "Burst into — qəfildən başlamaq.", R3),
    ("Reading", "hard", "What lesson did Kamran learn?", "A performance can move people even if it isn't perfect.",
     ["Mistakes always ruin a performance.", "He should stop playing the violin.", "Teachers are always right.", "Audiences never notice mistakes."],
     "Son cümləyə baxın.", R3),
    ("Reading", "easy", "What did the Silk Road connect?", "China and the Mediterranean",
     ["Europe and America", "Africa and Australia", "India and Japan", "Russia and Canada"], "Birinci cümləyə baxın.", R4),
    ("Reading", "medium", "Which goods travelled west?", "silk, spices, paper and porcelain",
     ["glassware and wool", "precious metals only", "cars and machines", "coffee and tea only"], "İkinci cümləyə baxın.", R4),
    ("Reading", "hard", "What does the text say about most traders?", "Few of them travelled the whole route.",
     ["They all crossed the entire route.", "They never left China.", "They travelled only by sea.", "They avoided cities."],
     "«Few traders crossed the entire route…»", R4),
    ("Reading", "medium", "What were caravanserais?", "roadside inns for travellers and their animals",
     ["markets for silk", "large ships", "schools for merchants", "religious buildings"], "Mətndə tərifi verilib.", R4),
    ("Reading", "hard", "Why do historians call the Silk Road a channel of cultural exchange?", "Ideas, religions and knowledge also spread along it.",
     ["It was built by many countries together.", "Only cultural objects were sold there.", "It connected all continents.", "It still exists today."],
     "Mallarla yanaşı din, dil, elm və reseptlər də yayılırdı.", R4),
    ("Reading", "medium", "Why does false information often spread quickly?", "It is designed to provoke strong emotions.",
     ["It is always very long.", "It comes from official sources.", "It is written by experts.", "It is easy to check."],
     "«…designed to provoke strong emotions such as fear or anger.»", R5),
    ("Reading", "easy", "What is the first habit experts recommend?", "checking who published the story",
     ["sharing it immediately", "reading only headlines", "asking friends to share it", "ignoring the date"], "«First, check who published the story…»", R5),
    ("Reading", "medium", "Why should readers pay attention to the date?", "Old stories are sometimes shared as new.",
     ["New stories are always false.", "Dates are often missing.", "Websites change dates every day.", "Old news is more reliable."],
     "Üçüncü vərdişə baxın.", R5),
    ("Reading", "medium", "The word «suspicious» in the text is closest in meaning to ___.", "doubtful",
     ["excited", "certain", "grateful", "careless"], "Be suspicious of — şübhə ilə yanaşmaq.", R5),
    ("Reading", "hard", "What is the main message of the text?", "A short pause to check can stop false news from spreading.",
     ["The internet should be banned.", "All news online is false.", "Only experts can recognize fake news.", "Headlines are always true."],
     "Son cümləyə baxın.", R5),
    ("Reading", "easy", "In what way do children have an advantage, according to the text?", "They often develop a more natural accent.",
     ["They understand grammar rules faster.", "They have more time.", "They use strategies consciously.", "They never make mistakes."],
     "İkinci cümləyə baxın.", R6),
    ("Reading", "medium", "Which advantage of adults is mentioned?", "They can connect new words to existing knowledge.",
     ["They have a better accent.", "They have more free time.", "They are never afraid of mistakes.", "They learn without practice."],
     "Böyüklərin üstünlükləri sadalanır.", R6),
    ("Reading", "hard", "According to the text, what are the main obstacles for adult learners?", "practical problems such as lack of time",
     ["biological limits of the brain", "bad teachers", "expensive books", "difficult accents"], "«…not biological but practical…»", R6),
    ("Reading", "medium", "What do teachers advise adults to do?", "set small, regular goals",
     ["study only grammar", "avoid speaking until they are perfect", "learn only one word a week", "stop if they make errors"],
     "Son cümləyə baxın.", R6),
    ("Reading", "hard", "What is the writer's main purpose?", "to challenge a common belief about language learning",
     ["to advertise a language school", "to prove that children cannot learn languages", "to describe a teacher's life", "to compare two languages"],
     "Mətn ümumi yayılmış fikri tənqidi şəkildə nəzərdən keçirir.", R6),
]

if __name__ == "__main__":
    save(11, "en", [
        ("grammar", "Grammar", handwritten(11, "en", "grammar", "Grammar", GRAMMAR, 11201),
         "Mixed və inverted conditionals, inversion, wishes, perfect modals, reported speech və passive."),
        ("vocabulary", "Vocabulary", handwritten(11, "en", "vocabulary", "Vocabulary", VOCAB, 11202),
         "Idioms, phrasal verbs, collocations, word formation və dependent prepositions."),
        ("reading", "Reading", handwritten(11, "en", "reading", "Reading", READING, 11203),
         "Altı orijinal mətn üzrə əsas fikir, nəticə çıxarma, müəllifin mövqeyi və söz mənası."),
    ])
