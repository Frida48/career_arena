"""Reading: hər sinif üçün 3 orijinal mətn, hər mətnə 10 sual (1 mətn = 1 quiz).
Sual: (sual, düzgün cavab, [4 yanlış cavab])"""

PASSAGES = [
    # ======================= 9-cu sinif =======================
    {"g": 9, "title": "The Jam Stall", "text": (
        "Every Saturday, fifteen-year-old Lala helps her aunt Nargiz at a small stall in the town market. Her aunt makes jam "
        "from the fruit that grows in her garden: cherries in June, apricots in July and quinces in the autumn. At first, Lala "
        "only carried boxes and put the jars on the table. She was too shy to speak to customers, and when someone asked her a "
        "question, she always looked at her aunt for help.\n\n"
        "One morning, Aunt Nargiz had to leave the stall for an hour to take a phone call. Lala was alone. An old man stopped "
        "and asked which jam was best for his grandchildren. Lala's heart was beating fast, but she remembered what her aunt "
        "usually said. She explained that the apricot jam was the sweetest and offered him a small spoon to taste it. The man "
        "smiled and bought three jars.\n\n"
        "When her aunt came back, Lala proudly showed her the money. 'You see,' said Aunt Nargiz, 'you knew everything — you "
        "just needed to believe it.' Since that day, Lala has talked to customers herself. She has even started writing small "
        "labels for the jars that tell the story of each fruit. Her aunt says that sales have gone up since the labels appeared."),
     "qs": [
         ("Where does Lala help her aunt?", "at a stall in the town market", ["in a fruit garden", "in a jam factory", "at a school fair", "in a supermarket"]),
         ("Which fruit does Aunt Nargiz use in the autumn?", "quinces", ["cherries", "apricots", "apples", "strawberries"]),
         ("What did Lala do at first?", "She carried boxes and put jars on the table.", ["She sold most of the jam.", "She made the jam herself.", "She wrote labels for the jars.", "She took phone calls for her aunt."]),
         ("Why did Lala always look at her aunt when customers asked questions?", "She was too shy to answer.", ["She didn't know any prices.", "She couldn't hear them well.", "Her aunt didn't allow her to speak.", "She didn't understand their language."]),
         ("Why was Lala alone at the stall one morning?", "Her aunt had to take a phone call.", ["Her aunt was ill.", "Her aunt went to buy fruit.", "Her aunt went home early.", "Her aunt was talking to another seller."]),
         ("Which jam did Lala say was the sweetest?", "apricot", ["cherry", "quince", "strawberry", "fig"]),
         ("The phrase «her heart was beating fast» shows that Lala was ___.", "nervous", ["bored", "angry", "tired", "hungry"]),
         ("What did Aunt Nargiz mean when she said «you just needed to believe it»?", "Lala needed more confidence, not more knowledge.", ["Lala should believe the customers.", "Lala had told the man a lie.", "Lala needed to learn more about jam.", "Lala should not work alone again."]),
         ("What has happened since the labels appeared?", "The stall has sold more jam.", ["Lala's aunt has stopped making jam.", "The labels have been removed.", "Customers have complained.", "Prices have gone down."]),
         ("What is the main idea of the text?", "A shy girl gains confidence by helping at her aunt's stall.", ["How to make apricot jam at home.", "Why markets are better than supermarkets.", "An old man who loves his grandchildren.", "The history of the town market."]),
     ]},
    {"g": 9, "title": "Why Do Cats Purr?", "text": (
        "Anyone who has lived with a cat knows the soft, low sound it makes when it is relaxed: purring. For a long time, "
        "people believed that cats purr only when they are happy. Today we know that the truth is more complicated.\n\n"
        "Scientists explain that purring is produced by the muscles in a cat's throat. These muscles move very quickly and make "
        "the air vibrate as the cat breathes in and out. That is why a cat can purr for a long time without stopping.\n\n"
        "Cats do purr when they are comfortable, for example when they are lying on a warm sofa or being stroked. However, "
        "they also purr when they are frightened, hungry or even hurt. Mother cats purr to their kittens, and kittens begin to "
        "purr when they are only a few days old. This helps the kittens find their mother, because they cannot see well at "
        "that age.\n\n"
        "Some researchers think that purring may also help cats relax and feel better when they are in pain. This idea has not "
        "been fully proven yet, and scientists are still studying it. One thing is certain: a purring cat is trying to "
        "communicate something, and a careful owner can learn to understand what it means."),
     "qs": [
         ("What did people believe about purring for a long time?", "Cats purr only when they are happy.", ["Cats purr only when they are hungry.", "Only kittens can purr.", "Purring is a sign of illness.", "Cats purr to scare other animals."]),
         ("How is purring produced?", "by fast-moving muscles in the throat", ["by the cat's heart", "by the cat's teeth", "by the cat's stomach", "by the cat's tail"]),
         ("Why can a cat purr for a long time without stopping?", "It purrs both when breathing in and out.", ["It does not need to breathe.", "It purrs only when sleeping.", "It stores air in its body.", "It purrs very quietly."]),
         ("Which situation is NOT mentioned as a time when cats purr?", "when they are playing with a ball", ["when they are frightened", "when they are hurt", "when they are being stroked", "when they are hungry"]),
         ("Why is purring useful for very young kittens?", "It helps them find their mother.", ["It keeps them warm.", "It helps them see better.", "It makes them grow faster.", "It teaches them to hunt."]),
         ("The word «comfortable» in the text is closest in meaning to ___.", "relaxed and pleasant", ["afraid", "hungry", "busy", "noisy"]),
         ("What does the text say about the idea that purring helps cats in pain?", "It has not been fully proven yet.", ["It is completely false.", "It was proven a long time ago.", "Only owners believe it.", "It is true only for kittens."]),
         ("According to the text, what can a careful owner do?", "learn to understand what the purring means", ["stop a cat from purring", "teach a cat to purr louder", "make a cat purr all the time", "hear purring from far away"]),
         ("What can we infer from the text?", "A purring cat is not always happy.", ["Cats never purr when they are alone.", "Only old cats purr.", "Purring is dangerous for cats.", "Kittens learn to purr at school age."]),
         ("What is the best title for the text?", "Purring: More Than a Happy Sound", ["How to Feed Your Cat", "Cats and Dogs as Pets", "The Life of Wild Cats", "Why Cats Like Warm Sofas"]),
     ]},
    {"g": 9, "title": "Bobik Comes Home", "text": (
        "On a rainy evening in November, the Aliyev family's dog, Bobik, ran out of the garden gate and disappeared. "
        "Ten-year-old Murad had forgotten to close the gate after coming home from football practice. He felt terrible. The "
        "whole family went out with torches and called Bobik's name until midnight, but there was no sign of him.\n\n"
        "The next morning, Murad's sister Aysu suggested making posters. Together they printed twenty posters with Bobik's "
        "photo and their phone number and put them up around the neighbourhood. Murad also wrote a message in a local "
        "online group. For two days nothing happened, and Murad began to lose hope.\n\n"
        "On the third day, the phone rang. A woman who worked at a bakery three streets away said that a brown dog had been "
        "sleeping by the warm oven door every night. When the family arrived, Bobik jumped up and almost knocked Murad over. "
        "The baker laughed and said that Bobik had chosen the warmest place in town.\n\n"
        "That evening, Murad fixed a small bell to the garden gate. 'Now I will always hear it,' he said. His father smiled and "
        "told him that everyone makes mistakes, but the important thing is to learn from them."),
     "qs": [
         ("Why did Bobik get out of the garden?", "Murad forgot to close the gate.", ["The fence was broken.", "Aysu opened the gate.", "He jumped over the wall.", "A neighbour let him out."]),
         ("How did Murad feel when Bobik disappeared?", "He felt guilty and upset.", ["He felt relieved.", "He did not care.", "He was angry with his sister.", "He was excited."]),
         ("Whose idea was it to make posters?", "Aysu's", ["Murad's", "their father's", "the baker's", "a neighbour's"]),
         ("How many posters did they put up?", "twenty", ["ten", "two", "three", "thirty"]),
         ("Who found Bobik?", "a woman who worked at a bakery", ["a police officer", "Murad's football coach", "a vet", "a woman from the online group"]),
         ("Why was Bobik sleeping near the bakery?", "It was warm next to the oven.", ["He liked the smell of bread.", "The baker fed him every day.", "He was afraid to go home.", "He was locked inside."]),
         ("The phrase «almost knocked Murad over» shows that Bobik was ___.", "very happy to see Murad", ["angry with Murad", "too tired to move", "afraid of Murad", "hurt and weak"]),
         ("Why did Murad put a bell on the gate?", "to hear when the gate opens", ["to call Bobik for dinner", "to decorate the garden", "to scare away other dogs", "because his father asked him to"]),
         ("What lesson does Murad's father want him to learn?", "Learn from your mistakes.", ["Never keep a dog.", "Always ask for help from neighbours.", "Don't go out in the rain.", "Bakeries are good for dogs."]),
         ("What is the main idea of the story?", "A boy loses his dog by mistake and finds it again with his family's help.", ["How to make posters on a computer.", "Why dogs like bakeries.", "A football match on a rainy day.", "How a baker opened a new shop."]),
     ]},
    # ======================= 10-cu sinif =======================
    {"g": 10, "title": "A Beach Worth Saving", "text": (
        "When our school announced a volunteer clean-up of a beach on the Caspian coast, only a few students signed up. Most "
        "of us thought it would be a boring way to spend a Sunday. I went mainly because my best friend, Rashad, had promised "
        "to bring his camera.\n\n"
        "What we found surprised everyone. In just three hours, thirty volunteers collected more than two hundred bags of "
        "rubbish. Plastic bottles were the most common item, but we also found fishing nets, shoes, a broken chair and "
        "thousands of tiny pieces of plastic mixed with the sand. A biologist from a local environmental group explained that "
        "these small pieces are especially dangerous, because birds and fish often mistake them for food.\n\n"
        "Rashad's photos turned out to be the most powerful part of the day. He posted a 'before and after' picture of the "
        "beach, and within a week it had been shared hundreds of times. People we had never met wrote to ask when the next "
        "clean-up would take place.\n\n"
        "The next event attracted almost a hundred volunteers, including several families with small children. Looking back, "
        "I realise that the beach did not change because of one Sunday. It changed because people saw what was possible and "
        "decided to act. Cleaning the beach is useful, but the real goal, the biologist reminded us, is to stop the rubbish "
        "from getting there in the first place."),
     "qs": [
         ("Why did the writer go to the clean-up?", "because his friend was going to bring a camera", ["because his teacher made him go", "because he loved the beach", "because he wanted to meet a biologist", "because he needed points for school"]),
         ("What did most students think about the clean-up at first?", "It would be boring.", ["It would be dangerous.", "It would be too difficult.", "It would be well paid.", "It would be fun."]),
         ("What was the most common item found on the beach?", "plastic bottles", ["fishing nets", "shoes", "broken chairs", "paper bags"]),
         ("Why are tiny pieces of plastic especially dangerous?", "Birds and fish think they are food.", ["They are sharp and cut people.", "They make the water too warm.", "They are impossible to see.", "They attract insects."]),
         ("What made Rashad's photos so powerful?", "They showed the difference before and after the clean-up.", ["They were taken by a professional.", "They were printed in a newspaper.", "They showed rare birds.", "They won a competition."]),
         ("The word «attracted» in the text is closest in meaning to ___.", "brought in", ["sent away", "frightened", "counted", "paid"]),
         ("How many volunteers came to the next event?", "almost a hundred", ["thirty", "two hundred", "a few", "several thousand"]),
         ("According to the writer, why did the beach really change?", "People saw what was possible and decided to act.", ["The government cleaned it.", "The weather became better.", "The rubbish disappeared naturally.", "A company paid for the clean-up."]),
         ("What does the biologist believe is the real goal?", "stopping rubbish from reaching the beach", ["organising a clean-up every Sunday", "taking more photos", "closing the beach to visitors", "studying birds and fish"]),
         ("What can we infer about the writer's attitude by the end of the text?", "He now sees the value of taking action together.", ["He still thinks the clean-up was a waste of time.", "He is angry with the people who came.", "He wants to become a photographer.", "He is no longer friends with Rashad."]),
     ]},
    {"g": 10, "title": "How Habits Work", "text": (
        "Why is it so easy to check your phone and so hard to start your homework? According to some researchers, the answer "
        "lies in the way habits are formed. They describe every habit as a loop made of three parts: a cue, a routine and a "
        "reward.\n\n"
        "The cue is the signal that starts the behaviour — for example, the sound of a notification. The routine is the "
        "behaviour itself: picking up the phone and scrolling. The reward is the pleasant feeling that follows, such as seeing "
        "a funny message. When this loop is repeated many times, the brain begins to connect the cue with the reward, and the "
        "routine becomes almost automatic.\n\n"
        "The good news is that the same loop can be used to build useful habits. Experts suggest keeping the cue simple and "
        "visible: if you want to read more, leave a book on your pillow. They also recommend starting with a very small "
        "routine, such as reading just two pages, so that it does not feel like hard work. Finally, giving yourself a small "
        "reward, like ticking a box on a calendar, helps the brain remember that the behaviour is worth repeating.\n\n"
        "Breaking a bad habit is usually harder than starting a new one. Instead of simply trying to stop, it often works better "
        "to keep the same cue and reward but change the routine. A student who snacks when bored, for instance, might go for a "
        "short walk instead."),
     "qs": [
         ("According to the text, how many parts does a habit loop have?", "three", ["two", "four", "five", "one"]),
         ("In the phone example, what is the cue?", "the sound of a notification", ["picking up the phone", "scrolling", "seeing a funny message", "doing homework"]),
         ("What happens when the loop is repeated many times?", "The routine becomes almost automatic.", ["The reward disappears.", "The cue becomes louder.", "The brain forgets the behaviour.", "The habit becomes harder."]),
         ("Why do experts suggest leaving a book on your pillow?", "to make the cue simple and visible", ["to make the bed more comfortable", "to reward yourself", "to read before sleeping only", "to stop using your phone"]),
         ("Why should you start with a very small routine?", "so that it does not feel like hard work", ["because big routines are dangerous", "so that you can finish faster", "because experts don't like reading", "so that you forget the cue"]),
         ("What example of a reward is given?", "ticking a box on a calendar", ["buying a new phone", "reading two pages", "going for a walk", "eating a snack"]),
         ("The word «automatic» in the text is closest in meaning to ___.", "done without thinking", ["done very slowly", "done with a machine", "done only once", "done by others"]),
         ("According to the text, what often works better than simply trying to stop a bad habit?", "keeping the cue and reward but changing the routine", ["removing all rewards", "ignoring the cue", "starting several new habits at once", "asking someone to punish you"]),
         ("What can we infer about the student who goes for a walk instead of snacking?", "Boredom is still the cue, but the routine has changed.", ["The student is no longer ever bored.", "The student has stopped eating.", "Walking is the cue for snacking.", "The student has no habits at all."]),
         ("What is the main purpose of the text?", "to explain how habits form and how to change them", ["to warn people never to use phones", "to describe a scientific experiment", "to sell a book about reading", "to compare good and bad students"]),
     ]},
    {"g": 10, "title": "A Letter from Abroad", "text": (
        "Dear Leyla,\n\n"
        "It has been almost three months since I arrived in Germany for my exchange year, and I finally have time to write a "
        "proper letter. The first weeks were much harder than I expected. I had studied German for two years, but on my first "
        "day at school I understood almost nothing. Everyone spoke so fast! I went home and cried, and I seriously thought "
        "about coming back.\n\n"
        "My host family helped me more than I can say. Every evening at dinner, my host mother asked me to describe my day in "
        "German, and she never laughed at my mistakes. My host brother, Jonas, introduced me to his friends and took me to "
        "his football club, even though I am a terrible player.\n\n"
        "Now things are different. Last week I gave a short presentation about Azerbaijan in my geography class. I showed "
        "photos of Baku and the mountains of Quba, and my classmates asked so many questions that the teacher had to stop us. "
        "I have also learned to cook a German potato salad, although I still prefer our plov.\n\n"
        "The most important thing I have learned is that feeling lost is normal at the beginning. If you decide to apply for "
        "the exchange programme next year, don't let the first difficult weeks scare you. Write back soon and tell me "
        "everything about school!\n\n"
        "With love,\nSabina"),
     "qs": [
         ("Why is Sabina in Germany?", "She is on an exchange year.", ["She moved there with her family.", "She is on holiday.", "She works there.", "She is visiting a sick relative."]),
         ("How long has Sabina been in Germany?", "almost three months", ["two years", "one week", "a whole year", "three days"]),
         ("What was the problem on Sabina's first day at school?", "She understood almost nothing.", ["She got lost on the way.", "She forgot her books.", "Nobody talked to her.", "She was late."]),
         ("How did Sabina's host mother help her?", "She asked Sabina to describe her day in German every evening.", ["She gave her extra German lessons at school.", "She translated everything into English.", "She took her to the football club.", "She cooked plov for her."]),
         ("What does Sabina say about her football skills?", "She is a terrible player.", ["She is the best in the club.", "She has never played.", "She plays better than Jonas.", "She wants to become a professional."]),
         ("What happened during Sabina's presentation?", "Her classmates asked a lot of questions.", ["Nobody listened to her.", "She forgot her photos.", "The teacher criticised her German.", "She cried in front of the class."]),
         ("Which dish does Sabina still prefer?", "plov", ["German potato salad", "pizza", "dolma", "kebab"]),
         ("The phrase «feeling lost» in the text means ___.", "feeling confused and not at home", ["not knowing the way in a city", "losing your bag", "feeling sick", "being late for school"]),
         ("What can we infer about Leyla?", "She may apply for the exchange programme next year.", ["She lives in Germany.", "She is Sabina's teacher.", "She has already studied abroad.", "She doesn't like writing letters."]),
         ("What is the main message of Sabina's letter?", "The beginning is hard, but it gets better, so don't give up.", ["Germany is a boring country.", "Learning German is impossible.", "Exchange programmes are too expensive.", "Host families are always strict."]),
     ]},
    # ======================= 11-ci sinif =======================
    {"g": 11, "title": "Farms That Grow Upwards", "text": (
        "As cities grow and farmland becomes scarcer, some engineers and farmers are looking up rather than out. Vertical "
        "farms grow crops indoors, in stacked layers that can rise many metres high. Instead of sunlight, the plants receive "
        "light from LED lamps, and instead of soil, their roots often sit in water that contains carefully measured "
        "nutrients.\n\n"
        "Supporters point to several advantages. Because the environment is fully controlled, crops can be harvested all year "
        "round regardless of the weather. Water is recycled within the system, so these farms typically use far less of it "
        "than traditional fields. Since insects are kept out, pesticides are rarely needed. And when a farm is built inside a "
        "city, vegetables can reach shops within hours rather than days, which reduces transport costs and keeps the food "
        "fresher.\n\n"
        "Critics, however, are less enthusiastic. Lighting and climate control consume enormous amounts of electricity, and "
        "unless that energy comes from renewable sources, the environmental benefits may be smaller than they first appear. "
        "Building costs are also high, which is why most vertical farms focus on fast-growing, valuable crops such as lettuce "
        "and herbs. Staple foods like wheat or rice, which need a lot of space and time, are still far more practical to grow "
        "in open fields.\n\n"
        "For now, then, vertical farming seems unlikely to replace traditional agriculture. A more realistic role may be to "
        "complement it, supplying cities with fresh greens while conventional farms continue to feed the world."),
     "qs": [
         ("What replaces sunlight in a vertical farm?", "LED lamps", ["mirrors", "solar panels", "candles", "glass roofs"]),
         ("Where do plant roots often sit in vertical farms?", "in water with nutrients", ["in sand", "in normal garden soil", "in the air without anything", "in plastic bags of earth"]),
         ("Why can vertical farms harvest crops all year round?", "The environment is fully controlled.", ["They use special seeds.", "They are built in hot countries.", "They grow only one plant.", "Workers stay there day and night."]),
         ("Why are pesticides rarely needed?", "Insects are kept out.", ["The plants are poisonous.", "LED light kills insects.", "Water washes insects away.", "The crops grow too fast."]),
         ("Which advantage is linked to building farms inside cities?", "Food reaches shops faster and stays fresher.", ["Land is cheaper inside cities.", "City air helps plants grow.", "More workers live in cities.", "Cities have more sunlight."]),
         ("The word «scarcer» in the first paragraph is closest in meaning to ___.", "less available", ["more expensive", "more fertile", "larger", "cleaner"]),
         ("According to critics, when might the environmental benefits be smaller than they appear?", "when the electricity does not come from renewable sources", ["when the farms are built outside cities", "when too much water is recycled", "when crops grow too quickly", "when lettuce is replaced by herbs"]),
         ("Why do most vertical farms grow lettuce and herbs?", "They are fast-growing and valuable.", ["They need more space than wheat.", "They are the cheapest crops to buy.", "They cannot be grown in fields.", "They need no light."]),
         ("The word «complement» in the last paragraph means ___.", "add to and improve something", ["completely replace something", "say something nice about", "compete against", "make something smaller"]),
         ("What is the writer's overall view of vertical farming?", "It is useful but will not replace traditional farming.", ["It will soon feed the whole world.", "It is completely useless.", "It is too dangerous to continue.", "It should replace all open-field farms."]),
     ]},
    {"g": 11, "title": "In Defence of Boredom", "text": (
        "We live in an age in which boredom has become almost impossible. The moment we have to wait — for a bus, in a queue, "
        "for a kettle to boil — most of us reach for our phones. It seems harmless: why sit doing nothing when there are "
        "messages to read and videos to watch? Yet a growing number of psychologists suggest that by eliminating boredom, we "
        "may be losing something valuable.\n\n"
        "Boredom, they argue, is not simply an unpleasant emptiness. It is a signal that our current situation is not "
        "satisfying us, and it pushes us to look for something more meaningful. When the mind has nothing external to focus "
        "on, it begins to wander, connecting memories, ideas and plans in unexpected ways. Many people report that their best "
        "ideas arrive in the shower or on a long walk — precisely the moments when they are not being entertained.\n\n"
        "This does not mean that every dull moment leads to brilliance. Chronic boredom, especially when people feel trapped "
        "in situations they cannot change, is linked to frustration and low mood. The difference seems to lie in how we "
        "respond. Boredom that we escape from instantly teaches us nothing; boredom that we tolerate for a while can become "
        "the starting point for curiosity and creativity.\n\n"
        "Perhaps, then, the next time you are waiting for a bus, it is worth leaving the phone in your pocket. You may simply "
        "be bored for ten minutes — or you may have your next good idea."),
     "qs": [
         ("According to the writer, what do most people do the moment they have to wait?", "reach for their phones", ["start a conversation", "read a book", "close their eyes", "leave the queue"]),
         ("How do some psychologists describe boredom?", "as a signal that the current situation is not satisfying", ["as a dangerous illness", "as a complete waste of time", "as a sign of low intelligence", "as something only children feel"]),
         ("What happens when the mind has nothing external to focus on?", "It begins to wander and connect ideas.", ["It stops working completely.", "It falls asleep.", "It becomes angry.", "It forgets memories."]),
         ("Why does the writer mention the shower and long walks?", "to show that good ideas often come when we are not entertained", ["to recommend healthy habits", "to explain why people get bored", "to describe the writer's daily routine", "to compare two types of exercise"]),
         ("What is chronic boredom linked to?", "frustration and low mood", ["better creativity", "physical strength", "higher grades", "more free time"]),
         ("The word «tolerate» in the third paragraph is closest in meaning to ___.", "accept and put up with", ["avoid completely", "enjoy very much", "fight against", "forget quickly"]),
         ("According to the text, what makes the difference between useful and useless boredom?", "how we respond to it", ["how long we sleep", "where we live", "how old we are", "what phone we use"]),
         ("What can be inferred about boredom we escape from instantly?", "It is unlikely to lead to new ideas.", ["It is the most creative kind.", "It makes us healthier.", "It lasts longer than other boredom.", "It only happens at work."]),
         ("What is the writer's purpose in the final paragraph?", "to encourage readers to accept short periods of boredom", ["to tell readers to throw away their phones", "to explain how buses work", "to warn that boredom is dangerous", "to describe a scientific study"]),
         ("Which statement would the writer most likely agree with?", "Constant entertainment can stop us from thinking deeply.", ["Boredom should be avoided at all costs.", "Phones make people more creative.", "Every bored person becomes a genius.", "Psychologists have no interest in boredom."]),
     ]},
    {"g": 11, "title": "The Last Keeper", "text": (
        "For thirty-two years, Ilyas had climbed the hundred and twelve steps of the lighthouse every evening to light the lamp. "
        "He knew every crack in the stone walls and every change in the sound of the sea. Ships passing the dangerous rocks "
        "below had never seen him, but many of their sailors owed him their lives.\n\n"
        "The letter arrived on a grey morning in March. The lighthouse was to be automated: a computer in a city office would "
        "now control the lamp, and a keeper would no longer be needed. Ilyas read the letter twice, folded it carefully and "
        "placed it under the clock on the kitchen table, where it stayed for a week.\n\n"
        "On his last evening, he climbed the steps more slowly than usual. At the top, he did not light the lamp; it lit "
        "itself at exactly the programmed minute. For a moment he felt useless, like an old tool left on a shelf. Then he "
        "noticed a small fishing boat struggling against the wind near the rocks. Out of habit, he picked up the radio and "
        "guided the fisherman to the safe channel, calmly, step by step, as he had done a hundred times before.\n\n"
        "When the boat was safe, the fisherman's voice came through the radio: 'Thank you, whoever you are.' Ilyas smiled. "
        "Machines, he thought, could light a lamp. But they could not hear fear in a man's voice. He went down the steps for "
        "the last time, feeling, for the first time in weeks, that his work had mattered."),
     "qs": [
         ("How long had Ilyas worked at the lighthouse?", "thirty-two years", ["a hundred and twelve years", "twelve years", "one year", "twenty years"]),
         ("What did Ilyas do every evening?", "He climbed the steps to light the lamp.", ["He repaired the stone walls.", "He went fishing.", "He wrote letters to sailors.", "He visited the city office."]),
         ("What did the letter say?", "The lighthouse would be controlled by a computer.", ["The lighthouse would be closed and destroyed.", "Ilyas would get a new assistant.", "Ilyas had won an award.", "A storm was coming."]),
         ("What does Ilyas's reaction to the letter — leaving it under the clock for a week — suggest?", "He found the news difficult to accept.", ["He did not read it.", "He was happy about the change.", "He planned to reply quickly.", "He did not understand it."]),
         ("Why did Ilyas not light the lamp on his last evening?", "It was lit automatically.", ["He forgot to do it.", "The lamp was broken.", "He was too tired.", "There was no electricity."]),
         ("The comparison «like an old tool left on a shelf» shows that Ilyas felt ___.", "no longer needed", ["very proud", "physically ill", "excited about the future", "angry with the fisherman"]),
         ("What did Ilyas do when he saw the fishing boat?", "He guided the fisherman to safety by radio.", ["He called the city office.", "He switched off the lamp.", "He ran down to the shore.", "He ignored it."]),
         ("The phrase «out of habit» means that Ilyas acted ___.", "automatically, because he had done it many times", ["unwillingly, because he was ordered to", "for money", "by mistake", "after a long discussion"]),
         ("What point does the writer make through Ilyas's thought about machines?", "Human understanding cannot be fully replaced by technology.", ["Machines are better than people.", "Lighthouses are no longer necessary.", "Fishermen should use computers.", "Technology is always dangerous."]),
         ("How has Ilyas's feeling changed by the end of the story?", "He feels that his work had real value.", ["He feels more useless than ever.", "He decides to stay at the lighthouse.", "He is angry with the fisherman.", "He wants to work with computers."]),
     ]},
]
