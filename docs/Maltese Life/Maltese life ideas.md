---
type: "list"
date: "2026-11-15"
status: "open"
---
# Maltese life: ideas for the add-on mod

**Ideas only. Nothing here is built or decided.** Written 2026-11-15 after the owner's request:

> what more could the mod have? this should really work in tandem with the Malta in Minecraft world. we're talking a true maltese experience. but go even beyond this. what makes malta? its also the people, the interactions, the life, the animals, the existence, the leisure activities. it all holisitically makes us who we are. thats what this mod should capture

This list builds on `Content mod list.md` (animals, plants, crops, 40 dishes, the nature log). It doesn't repeat that list. It adds the rest of Maltese life: people, village, faith and festa, language, sounds, seasons, work, leisure, the sea, history and humour.

## How to read it

- Every idea works in **layer 2**: it happens while you play, on top of the finished vanilla world. Nothing needs to be placed at generation. Take the mod out and the world is untouched. Ideas that need generation are in the "Layer 3 (later)" list at the end.
- Towns aren't built yet, so no idea depends on a building being there. Ideas use **the place** (real coordinates, the biome), **the date and time**, or **what the player builds**.
- **Art cost** is marked on each idea:
  - **none**: text, chat, titles, sounds from vanilla, particles, vanilla items and blocks.
  - **low**: a recoloured vanilla texture, a villager with a different outfit, a simple item icon, a simple recorded or made sound.
  - **medium**: a new simple model or several new textures.
  - **high**: a detailed new model or animation.
- Maltese words I'm not sure of are marked †.
- No brand names, no real living people, no real band club or party names.

## The four things everything else stands on

These aren't ideas to play with. They're the base that makes the other ideas cheap.

| Base | What it is | Art |
|---|---|---|
| **A. The parish table** | One data table of the 68 localities (54 in Malta, 14 in Gozo): centre coordinates, patron saint, festa date, what the place is known for, the meaning of its name, its motto. The world is 1:1, so the mod always knows which parish you're standing in. | none |
| **B. The Maltese calendar** | The mod knows the date: month, weekday, season, the moving feasts (Carnival, Good Friday, Easter). Either the real date of your PC, or a faster in-game year (question 1 at the end). | none |
| **C. People from villagers** | Every person is a vanilla villager or wandering trader with a different outfit, a Maltese name, a job, a daily routine and things to say. No new models. | low |
| **D. Build it and they come** | People appear at the parish centre, and also around things **you** build from vanilla blocks: a chair by a door, a counter with a sign, a boat at a quay. Like vanilla job blocks. So life grows where the player builds, and the world file never needs anything. | none |

---

## 1. People you meet

All use base C (reskinned villagers) unless marked.

### 1. The nanna on the doorstep *(art: low)*
- **You get:** an old woman on a chair by a door at sunset. She greets you, asks who you are, tells you the village news and gives you something to eat.
- **How:** place a chair (a stair block) next to a door in a town biome. In the evening a nanna may sit there. Talk to her daily: gossip (hints about nearby things), a food gift, and your standing in that parish goes up.
- **Where/when:** any town, evenings, most in summer.
- **Why Maltese:** the chair on the għatba (doorstep) in the cool of the evening is the picture of village life.

### 2. "Ta' min int?" *(art: none)*
- **You get:** the first time you meet someone in a new village they ask "Int ta' min?" (whose are you?). Your answer is your family nickname (idea 31) and your home parish.
- **How:** a chat line with a reply. If they "know your people" (you have standing in a nearby parish) prices are better and they talk more.
- **Where/when:** everywhere, first meeting.
- **Why Maltese:** in Malta you aren't asked what you do. You're asked whose you are.

### 3. The pastizzi seller (tal-pastizzi) *(art: low)*
- **You get:** a seller behind a counter from before sunrise. Cheap, hot pastizzi and tea in a glass. A small queue of villagers early in the morning.
- **How:** a villager job. Job block: a smoker with a sign. Sells for a few copper or iron nuggets, cheapest food in the game. Fresh ones (first hour) feed more.
- **Where/when:** town biomes, busiest 5 to 9 in the morning and after a night out.
- **Why Maltese:** the pastizzerija is where everyone meets, rich or poor.

### 4. The farmer (il-bidwi) *(art: low)*
- **You get:** a farmer in the fields at dawn who knows what to sow this month and when rain is coming.
- **How:** appears in `ghelieqi_fields`. Trades seeds for the right season, buys your crops, gives weather sayings that are true in game (idea 60).
- **Where/when:** field biomes, early morning and late afternoon; gone at midday in summer.
- **Why Maltese:** small family fields, rubble walls, a girna for shade and a farmer who has worked the same strip all his life.

### 5. The fisherman (is-sajjied) *(art: low)*
- **You get:** a fisherman mending nets on the quay, who tells you what's running and takes you out.
- **How:** appears near boats at the coast. Sells bait and traps, buys fish, tells the season (lampuki from 15 August). Can take you on a trip (idea 49).
- **Where/when:** Marsaxlokk, Mġarr (Gozo), Marsalforn, St Paul's Bay, Wied iż-Żurrieq, Xlendi.
- **Why Maltese:** the luzzu, the nets on the quay and the Sunday fish market.

### 6. The parish priest (il-kappillan) *(art: low)*
- **You get:** a kind figure near the church spot who knows the feast days, blesses your house after Easter and thanks you for helping with the festa.
- **How:** appears near the parish centre. Gives calendar information and small tasks (bring candles, flowers, help with the festa). See idea 24 for the house blessing.
- **Where/when:** every parish.
- **Why Maltese:** the kappillan is at the centre of village life. Kept warm and respectful, never a joke.

### 7. The man on the ridge (il-kaċċatur) *(art: low)*
- **You get:** an old countryman with his Kelb tal-Fenek at dawn. He knows the birds, the winds and the land better than anyone.
- **How:** he tells you which birds are passing today and where (helps the nature log), reads the wind, and sells rabbit and wild herbs. He never asks you to kill anything, and the mod gives no reward for killing (the owner's rule).
- **Where/when:** garrigue and cliff biomes, dawn, most in spring and autumn.
- **Why Maltese:** a real part of the countryside. A sensitive subject, so he's shown as a man who knows nature. Question 5 at the end asks if he should be in at all.

### 8. The birdwatcher *(art: low)*
- **You get:** someone with a notebook at Għadira, Is-Simar, Buskett or the cliffs who shares sightings.
- **How:** trades nature-log hints for your own sightings. Rings birds with you (the ringing idea already in the list).
- **Where/when:** `ghadira_wetland`, Buskett in September (birds of prey), Ta' Ċenċ cliffs.
- **Why Maltese:** the other side of the same countryside, and the real ringing station at Għadira.

### 9. The tourist *(art: low)*
- **You get:** sunburnt visitors in summer who are lost, ask the way, and pay you to guide them.
- **How:** a tourist asks for a real place ("Where is the Blue Grotto?"). Walk them there (they follow) for a reward. They stand in the sun at midday, take the wrong bus and say place names wrong.
- **Where/when:** summer; Valletta, Mdina, Sliema, Buġibba, Comino's Blue Lagoon, Marsaxlokk on Sunday.
- **Why Maltese:** every Maltese has given directions to a tourist holding a map upside down. It also teaches the player the island.

### 10. The band club members (il-bandisti) *(art: low)*
- **You get:** men and women with instruments who practise in the evening and march at the festa.
- **How:** villagers with a note-block sound each (brass, drum, clarinet). Near a festa they gather and rehearse; on the day they march (idea 18).
- **Where/when:** every parish, evenings in the weeks before its festa.
- **Why Maltese:** the każin tal-banda is the village's second home.

### 11. The hawkers with a horn *(art: low)*
- **You get:** sellers who come down the street and announce themselves with a sound: the bread man (tal-ħobż) at dawn, the vegetable man (tal-ħaxix) mid-morning, the fish man (tal-ħut), the gas man with his horn, the ice-cream van's tune in summer.
- **How:** wandering-trader style visits on fixed days of the week. You hear the horn or call first, then you have a few minutes to come out and buy. Each has his own sound.
- **Where/when:** town biomes and wherever a player has a house; ice cream only in summer and at beaches.
- **Why Maltese:** you know who's in the street without looking. Art is low: a recoloured trader and five short sounds.

### 12. The baker (il-furnar) *(art: low)*
- **You get:** a wood oven that works all night, bread at dawn, and the Sunday dish service (idea 68).
- **How:** a villager job at a furnace or smoker with a sign. Sells Maltese bread and ftira; best bread before sunrise.
- **Where/when:** every town; Qormi is the bread town (more bakers, better bread).
- **Why Maltese:** Qormi's old name is Casal Fornaro, the village of bakers.

### 13. The boatman (il-barklor) *(art: low)*
- **You get:** a man with a dgħajsa who rows you across the harbour and tells you what every fort is.
- **How:** see idea 52. He names each landmark as you pass it.
- **Where/when:** the Grand Harbour: Valletta, Birgu, Isla, Bormla, Kalkara.
- **Why Maltese:** the dgħajsa tal-pass has carried people across that harbour for centuries.

### 14. The cat lady and the street cats *(art: none)*
- **You get:** cats in every street and harbour, and someone who feeds them each evening.
- **How:** vanilla cats spawn in colonies in town biomes and at fishing quays. Put out fish at the same spot each day and a colony forms. A colony keeps rats and mice away from your food stores (same "worth more alive" rule). The cat lady NPC gives you a small thank-you when you feed them.
- **Where/when:** all towns; the quays at Marsaxlokk and St Julian's; Sliema's seafront gardens.
- **Why Maltese:** the cats of Malta are part of every street.

### 15. More faces, one line each *(art: low each)*
- **The sacristan:** rings the bells; lets you ring them (idea 37).
- **The salt family at Xwejni:** see idea 43.
- **The lace maker in Gozo:** see idea 44.
- **The stonemason (il-bennej):** buys and dresses stone; teaches the rubble wall (idea 41).
- **The bus driver:** see idea 51.
- **The kiosk owner:** see idea 69.
- **The lifeguard:** tells you the sea state and the jellyfish (idea 47).
- **The old men on the bench:** two or three villagers who sit in the square and argue about football and the festa all day. Pure colour, and a source of rumours.
- **The festa enthusiast (id-dilettant):** lives for the fireworks and the street decorations, and recruits you (ideas 17 to 21).

---

## 2. Village life and how people treat you

### 16. Parish standing *(art: none)*
- **You get:** each village slowly gets to know you. At first you're a stranger; later you're greeted by name, given food, told secrets and asked to carry the statue.
- **How:** one number per parish (base A). It goes up when you greet people, buy locally, help the festa, feed the cats, bring fish. It gives better prices, more gossip and festa jobs. It never goes negative: no punishment system.
- **Where/when:** all 68 parishes.
- **Why Maltese:** belonging to your village is the heart of it.

### 17. Two band clubs *(art: none)*
- **You get:** in some villages there are two clubs, each sure its feast, its band and its fireworks are the best. You can be friendly with both, or pick a side.
- **How:** in villages that really have two, the mod has two made-up clubs with a colour each (for example "the Blues" and "the Reds", no real names). Helping one makes its members warmer and the other side tease you. Teasing only: jokes in chat, never anything hostile.
- **Where/when:** the villages that really have two clubs or two feasts.
- **Why Maltese:** the pika (friendly rivalry) is what drives the fireworks, the decorations and the pride.

### 18. The greeting *(art: none)*
- **You get:** people greet you by time of day: "Bonġu", "Il-wara nofsinhar it-tajjeb", "Bonswa", "Il-lejl it-tajjeb". You can greet back.
- **How:** a "greet" key or a sneak-and-look. Greeting first raises parish standing a little. Older people expect it; ignoring a nanna gets a "Mela dan?".
- **Where/when:** everywhere.
- **Why Maltese:** you greet everyone you pass in a village street.

### 19. Gossip travels *(art: none)*
- **You get:** what you do in one village is known in the next before you get there. "Mela int dak li qabad il-lampuka l-kbira?" (so you're the one who caught the big lampuka?)
- **How:** notable things you do (a big catch, a house built, a fall off Dingli cliffs, losing at boċċi) become lines that NPCs in nearby parishes say for a few days.
- **Where/when:** everywhere; fastest in Gozo.
- **Why Maltese:** on a small island everyone knows everything by the evening.

### 20. The square and the church steps (il-pjazza u z-zuntier) *(art: none)*
- **You get:** a daily rhythm at the centre of each village: women after morning Mass, old men at midday, children after school, everyone on a summer night.
- **How:** villagers gather near the parish centre point at set hours (base C routines). If the player has built a square or benches there, they use them.
- **Where/when:** every parish centre.
- **Why Maltese:** the pjazza is the village's living room.

### 21. The evening walk (il-passiġġata) *(art: none)*
- **You get:** on summer evenings whole families walk slowly up and down the seafront, eating ice cream and nuts and stopping every ten steps to talk.
- **How:** groups of villagers walk a line along the coast between two points and back. Walking with them gives a small "good company" effect.
- **Where/when:** summer evenings; the Sliema front, Buġibba, Marsaskala, Birżebbuġa, Marsalforn, Xlendi.
- **Why Maltese:** nobody stays inside on a summer night.

### 22. Il-quċċija: your start in life *(art: none)*
- **You get:** when you first join, a tray of objects is put in front of you. The one you pick "tells your future" and gives a small lifelong perk.
- **How:** a simple screen with vanilla items: an egg (plenty: a little less hunger), a coin (trade: slightly better prices), a rosary-like bead string (calm: better festa rewards), a pen or book (learning: Maltese words stick faster), a fishing hook, a hoe, a trowel, a musical note. One choice, kept forever.
- **Where/when:** once, at first login.
- **Why Maltese:** the real custom on a child's first birthday.

### 23. Godparents and name days *(art: none)*
- **You get:** an NPC in your home parish becomes your parrinu or parrina (godparent). They give a gift on your name day and at Christmas and Easter (a figolla).
- **How:** choose a home parish; on its patron's feast and on set dates a gift arrives. In multiplayer a player can be godparent to a new player and gift them.
- **Where/when:** home parish; feast days.
- **Why Maltese:** godparents and name days matter as much as birthdays.

### 24. The house blessing (it-tberik tad-djar) *(art: none)*
- **You get:** in the weeks after Easter the priest visits your home and blesses it. Clean the house first.
- **How:** if you have a bed and a door in a parish, he knocks one day after Easter. The house gets a gentle effect for the season (fewer hostile mobs spawn near it, for example).
- **Where/when:** the weeks after Easter.
- **Why Maltese:** a real yearly custom, with the spring cleaning before it.

### 25. Your street niche (in-niċċa) *(art: none or low)*
- **You get:** a small corner shrine with a lamp on your house, as on real street corners. Neighbours leave flowers.
- **How:** a pattern built by the player from vanilla blocks (a wall niche, a lantern, a flower pot) is recognised by the mod. Lit every evening, it raises parish standing and keeps the corner free of mobs. A statue item would be low art; without one the lamp and flowers are enough.
- **Where/when:** anywhere the player builds.
- **Why Maltese:** niches and their red lamps are on thousands of Maltese corners.

### 26. House names *(art: none)*
- **You get:** your house gets a name on a sign by the door, and people use it. "Dar il-Paċi", "Ave Maria", "God Bless Australia" for a returned emigrant.
- **How:** a sign next to a door names the house. NPCs refer to you by it. The mod offers real-style names, including the emigrant ones.
- **Where/when:** any player house.
- **Why Maltese:** named houses and the emigrant story (Australia, Canada, England) are everywhere.

### 27. The garage *(art: none)*
- **You get:** a ground-floor room with a wide door becomes a family gathering place in summer: chairs out front, a table, cards, home-made wine.
- **How:** a room with a big door at street level (the mod checks the shape) attracts neighbours on summer evenings. They bring food. Light humour only.
- **Where/when:** summer evenings, towns.
- **Why Maltese:** the garage that never held a car.

---

## 3. Faith, festa and the year's feasts

Tone for the whole section: joyful and respectful. The player can always just watch. Religious parts never give combat power or anything that reads as a game "spell".

### 28. The village festa week *(art: low)*
- **You get:** every parish has its week. The streets fill, bells ring, petards go off at 8 in the morning, the band marches, the statue comes out on the last evening, and it ends with fireworks.
- **How:** driven by the parish table and the calendar. In festa week that parish gets: more people, stalls (idea 33), bell peals, petard sounds, band marches, a procession on the Sunday, night fireworks. Players can help in each part (ideas 29 to 34) or just enjoy it. The title on entering reads "Il-festa t-tajba!".
- **Where/when:** from late spring to September, a different village almost every weekend. Fixed points: St Paul's Shipwreck in Valletta on 10 February; Santa Marija on 15 August in seven places at once (Mosta, Attard, Għaxaq, Gudja, Mqabba, Qrendi, Victoria); Il-Vitorja on 8 September (Naxxar, Senglea, Mellieħa, Xagħra).
- **Why Maltese:** the festa is the high point of every village's year.

### 29. Decorating the streets (l-armar) *(art: none to low)*
- **You get:** in the days before the festa you help hang banners and lights along the main street.
- **How:** the dilettant gives you banners (vanilla banners in the club's colours), lanterns and chains to place. The more the street is dressed, the better the festa (more visitors, more stalls). Decorations placed by this job are removed again after the feast, so the world is left as it was.
- **Where/when:** the week before each festa.
- **Why Maltese:** the pavaljuni, bandalori and festuni take volunteers the whole winter to make.

### 30. Fireworks, air and ground *(art: low)*
- **You get:** Maltese fireworks, which are different from anything vanilla has: the daytime petards that are all bang and smoke, the long colour-changing shells at night, the ground fireworks (ġiggifogu) of spinning wheels on poles in the square, and the deafening finale (the kaxxa infernali).
- **How:** new firework star recipes give Maltese patterns (vanilla particle system). A "wheel" is a block on a fence post that spins sparks (particles; low art). Petards are sound and a puff of smoke. Villages compete: the mod scores each festa's show, and players who helped get the credit. Crafting is done at the crafting table, with no "factory" building and no accident mechanic, out of respect for real tragedies.
- **Where/when:** every festa; the Grand Harbour fireworks festival in late April; Lija on 6 August; Mqabba and Qrendi on 15 August.
- **Why Maltese:** Malta's fireworks makers are volunteers and among the best in the world.

### 31. The band march *(art: low)*
- **You get:** a brass band walking the streets playing a march, with a crowd around it, confetti from above and people singing along.
- **How:** bandist villagers walk a route playing a short loop (note-block style sounds or a simple recorded march written for the mod, never a real club's march). Confetti is particles. Walk with the march for a "briju" (high spirits) effect. The Sunday morning march (marċ ta' filgħodu) is the loud, wild one.
- **Where/when:** festa week.
- **Why Maltese:** the march is the sound of summer.

### 32. Carrying the statue *(art: low to medium)*
- **You get:** the statue comes out of the church to applause and bells, carried on shoulders, slowly, with the band behind.
- **How:** low-art version: an armour stand on a platform carried by a group of villagers, moving along a route. Players with high standing can be one of the carriers (reffiegħa): you walk in step for the route (a slow, simple rhythm task) and earn the village's thanks. In multiplayer, several players carry together.
- **Where/when:** the last evening of each festa; Good Friday (idea 36).
- **Why Maltese:** being a reffiegħ is an honour passed down in families.

### 33. Festa stalls *(art: low)*
- **You get:** stalls of nougat (qubbajt), hot mqaret, ice cream and toys along the street.
- **How:** festa-only traders who sell sweets you can't get otherwise. The nougat seller follows the festa from village to village all summer, so you meet the same face.
- **Where/when:** festa week, near the parish centre.
- **Why Maltese:** the white nougat stall with its lights and brass scales is at every festa.

### 34. Il-ġostra: the greasy pole *(art: low)*
- **You get:** a long greased pole sticking out over the sea, flags at the end. Run up it, grab a flag, fall in the water.
- **How:** a player-built or event-spawned slanted beam over water at festa time. A slippery surface (ice-like physics): the faster you run the further you get. Three flags, three prizes. Everyone falls in. Removed after the feast.
- **Where/when:** St Julian's (San Ġiljan) at its feast in late August; Msida.
- **Why Maltese:** a game from the Knights' time, still played.

### 35. Carnival (il-Karnival) *(art: low)*
- **You get:** five days of colour before Lent: costumes, dancing, loud floats, sweets. In Gozo, the strange one: Nadur's carnival, at night, with odd masks and no rules.
- **How:** players get mask and costume items (recoloured carved pumpkin and leather armour: low art). Villagers wear bright colours. In Nadur after dark the villagers wear silent, odd masks and nobody says who they are. Sweets: prinjolata and perlini, only now. Floats are a layer 3 or high-art thing; a low-art float is a decorated boat or minecart parade.
- **Where/when:** the five days before Ash Wednesday (February or early March); Valletta and Floriana by day, Nadur by night.
- **Why Maltese:** carnival since the Knights; Nadur's is like nothing else.

### 36. Lent, Holy Week and Easter *(art: low)*
- **You get:** the year's quiet turn. Lent: no festa noise, Lent biscuits (kwareżimal) and the Apostles' ring bread (qagħaq tal-appostli). Maundy Thursday: the seven visits (is-seba' visti), walking to seven churches. Good Friday: the bells go silent and a wooden clapper (iċ-ċuqlajta) sounds instead; slow processions with statues and hooded walkers. Easter Sunday: the bells explode back, the statue of the Risen Christ is **run** up the street, children hold up their figolla.
- **How:** calendar-driven. Bell sounds are replaced by a wooden rattle for two days. The seven visits is a walking task between seven parish centres (a lovely reason to walk the 1:1 island) with a quiet reward. The Easter run is a short sprint event with the carriers. Godparents give a figolla.
- **Where/when:** Good Friday processions: Valletta, Żebbuġ, Qormi, Mosta, Żejtun, Xagħra and others; the Easter morning run: Birgu, Bormla, Isla.
- **Why Maltese:** the most deeply felt days of the year. Shown plainly and with respect.

### 37. The bells *(art: low: sounds)*
- **You get:** bells you can read like a clock: the quarters and hours, the Ave Maria at dawn, noon and sunset, the Pater Noster in the morning, the slow toll for a death (il-mota), the wild peal of a festa. And a second, painted clock face on the church that shows the wrong time.
- **How:** sounds played from each parish centre by hour and calendar, heard further on a still day. With the sacristan's leave you ring them yourself (a small rhythm game). The "wrong clock" is a line the nanna tells you: one clock is painted wrong to confuse the devil.
- **Where/when:** every parish, all day.
- **Why Maltese:** you always know the time, the day and the news from the bells.

### 38. The Christmas crib (il-presepju) *(art: low)*
- **You get:** build your own crib at home, grow the white ġulbiena for it, and collect the little clay figures (pasturi) one by one.
- **How:** sow vetch seeds on a block **in a dark room** in late November; in the dark it grows long and white (a recoloured grass texture). Pasturi are small items found, traded or given through December (a shepherd, the sleeping one, the amazed one, the bagpiper). A crib with ġulbiena and figures brings visiting neighbours and a Christmas gift. On Christmas Eve a child villager gives the sermon (il-priedka tat-tifel) and there's a small procession with the Baby Jesus.
- **Where/when:** December; every parish.
- **Why Maltese:** the presepju, the ġulbiena on the windowsill and the boy's sermon at midnight Mass.

### 39. L-Imnarja at Buskett *(art: low)*
- **You get:** a night in the woods with lanterns, rabbit stew, wine, folk singing till dawn and a farm show; the next afternoon, bareback horse and donkey races up the hill at Rabat for a brocade banner (il-palju).
- **How:** on 28 June at night, people, stalls, għana singers (idea 55) and a "best crop" show gather in Buskett (the world already has `verdala_grove`): bring your best vegetables, honey, wine or animals for a prize. On 29 June a short horse race on a straight course at Saqqajja; the prize is a banner for your house.
- **Where/when:** 28 and 29 June; Buskett and Rabat.
- **Why Maltese:** the oldest country feast in Malta. Old marriage contracts promised the bride a yearly trip to it.

### 40. The small feasts of the year *(art: none to low)*
One line each, all calendar-driven:
- **San Girgor** (first Wednesday after Easter): walk from Żejtun to Marsaxlokk with the procession; by tradition the first swim and first ice cream of the year.
- **Il-Vitorja, 8 September:** the regatta (idea 50) and three feasts on one day.
- **All Souls, November:** bone-shaped almond sweets (għadam tal-mejtin); candles at night.
- **San Martin, 11 November:** children get a cloth bag (il-borża ta' San Martin) of walnuts, hazelnuts, almonds, chestnuts, a tangerine, dried figs and a sweet bun. A fair at Baħrija.
- **The Immaculate Conception, 8 December:** Bormla's feast, the one winter festa with the full works.
- **Christmas to Epiphany:** honey rings, the crib, carols.
- **Candlemas, 2 February (il-Kandlora):** the weather on this day "tells" the rest of winter (a real saying, made true in game).
- **St Joseph, 19 March:** Rabat's feast; fried sweet fritters (zeppoli).
- **The national days:** 31 March (Freedom Day, with a regatta), 7 June, 21 September (Independence), 13 December (Republic). Flags on houses, a band, fireworks over the harbour. No politics in the text.

---

## 4. Language

### 41. Place names that speak *(art: none)*
- **You get:** when you walk into a place, its name appears with what it means: "Marsaxlokk: the harbour of the south-east wind", "Mdina: the walled city", "Għajn Tuffieħa: the spring of the apple tree", "Wied il-Għasel: the valley of honey", "Xagħra: the open rocky plain".
- **How:** a title on entering, from a table of names and coordinates. It covers parishes, bays, valleys, headlands and hills, hundreds of names. Could be the very first thing built: it's all data.
- **Where/when:** everywhere.
- **Why Maltese:** the names are the oldest Maltese we have, and they describe the land the world already shows.

### 42. Kelma kelma: learning Maltese by living it *(art: none)*
- **You get:** people speak Maltese mixed with English. Words you've heard often turn from Maltese to "known" in a word book, with the meaning and how to say it (the ħ, għ, ż, ċ sounds explained).
- **How:** NPC lines are written half in Maltese. Each time you meet a word in a real situation (buying bread: ħobż; the sea: baħar) it counts. After a few times it's "learnt" in the book. Learnt words unlock more Maltese in the speech, so the island sounds more Maltese the longer you live there. An advancement for 50, 200, 500 words.
- **Where/when:** always.
- **Why Maltese:** the language is the single most Maltese thing there is, and no other game teaches it.

### 43. The Maltese mix *(art: none)*
- **You get:** real speech: "Mela", "Uwejja", "Ajma", "Isa!", "Ta", "Kollox sew?", "Insomma", "Prosit", "Saħħa", "Grazzi ħafna", "Ħi" between friends; English sentences that end in "ta" or "hux"; "I'll come now" meaning in an hour.
- **How:** a bank of short lines by situation and age: nanniet speak mostly Maltese, young people mix, shopkeepers call you "qalbi" (my heart) or "ħanini". A setting chooses how much Maltese (question 3).
- **Where/when:** always.
- **Why Maltese:** the way we really talk.

### 44. Your laqam (nickname) *(art: none)*
- **You get:** the village gives you a nickname from what you do, and it sticks. Fish a lot: "Tal-Ħut". Always on the cliffs: "Tar-Rdum". Keep falling in the sea: something worse.
- **How:** the mod watches your habits for the first weeks, then people start using a laqam "Ta' …". It appears under your name and NPCs use it. In multiplayer a family (team) shares one. You can't choose it, which is the point; but a setting lets you reroll.
- **Where/when:** your home parish first, then it spreads.
- **Why Maltese:** everyone has a family laqam, and nobody chose theirs.

### 45. Sayings that are true *(art: none)*
- **You get:** proverbs said at the right moment: "Il-baħar żaqqu ratba u rasu iebsa" (the sea has a soft belly and a hard head) when you go out in a storm; "Qatra qatra timtela l-ġarra" (drop by drop the jar fills) when you save up; "Min jistenna jithenna" (who waits is rewarded) at the bus stop.
- **How:** a table of sayings linked to events. Each one heard goes into a "sayings" page of the word book.
- **Where/when:** always.
- **Why Maltese:** the nanna has one for everything.

### 46. Counting and bargaining in Maltese *(art: none)*
- **You get:** prices said in Maltese numbers (wieħed, tnejn, tlieta…), weights in the old measures (a ratal, a qatta of greens, a wiżna), money talk in "liri" by old people.
- **How:** trade screens show the Maltese under the number. Old sellers still say prices in liri and convert, grumbling.
- **Where/when:** all trades.
- **Why Maltese:** the old measures are still used at the vegetable van.

---

## 5. Sound

All sounds can be vanilla sounds, re-pitched vanilla sounds, or short simple recordings made for the mod. No real band or broadcast recordings.

### 47. The soundscape by place and hour *(art: low: sounds)*
- **You get:** close your eyes and know where and when you are.
- **How:** layered ambient sounds chosen by biome, hour, season and wind:
  - **summer midday in the country:** cicadas (il-werżieq), loud, stopping when you come near the tree;
  - **summer night:** crickets, a gecko's chirp on a wall, a far-off festa;
  - **cliffs at night, February to October:** the wailing of shearwaters coming in from the sea (ties to the nature log);
  - **village morning:** bells, a rooster, a radio through a window, a hawker's horn;
  - **Sunday morning:** għana from a radio, pots, church bells;
  - **harbour:** ropes on masts, a ferry horn, gulls, engines of fishing boats at dawn;
  - **valley after rain:** running water and frogs;
  - **a match night:** a whole street shouting at once through open windows.
- **Where/when:** everywhere.
- **Why Maltese:** Malta is a loud, particular place. The sound may do more than any model.

### 48. The noon gun *(art: none)*
- **You get:** a cannon fired at 12:00 and 16:00 that you hear across the Grand Harbour.
- **How:** an explosion sound and smoke at the saluting battery's coordinates below the Upper Barrakka. If you're there at the right moment, an advancement.
- **Where/when:** Valletta, daily.
- **Why Maltese:** people still set their watches by it.

### 49. Folk singing (l-għana) *(art: low: sounds)*
- **You get:** two singers trading sharp, funny rhymed verses over guitars, each trying to outdo the other, while the bar listens.
- **How:** two NPC singers take turns with four-line verses from a bank (written in Maltese, with a translation), over a simple guitar loop. The verses can be about **you**: your laqam, your last big catch, your fall. That's the spirtu pront (quick wit) style. Old instruments appear at feasts: the żaqq (bagpipe), the tanbur (frame drum), the żafżafa (friction drum).
- **Where/when:** village bars on weekend evenings; Imnarja night at Buskett; strongest in Żejtun, Għaxaq, Żurrieq and Qormi.
- **Why Maltese:** the island's own folk music, improvised and teasing.

---

## 6. Seasons, weather and the feel of the year

### 50. The colour of the land *(art: none)*
- **You get:** Malta green and full of flowers from November to April, then gold, then dry brown by August, and green again within days of the first rain.
- **How:** the mod tints grass and leaf colours by season on the player's screen only. The world's blocks don't change, so it stays layer 2.
- **Where/when:** all land biomes.
- **Why Maltese:** the island has two faces, and visitors only ever see the brown one.

### 51. The winds by name *(art: none)*
- **You get:** the wind has a name and a character, and people talk about it: Grigal (north-east, the storm wind that wrecks harbours), Xlokk (south-east, hot, sticky, hazy, brings red dust), Majjistral (north-west, the clear cool wind), Tramuntana (north), Lvant, Nofsinhar, Lbiċ, Punent.
- **How:** each day has a wind and a strength shown on a simple compass item. It decides which coast is calm (swim and fish on the sheltered side: a real Maltese habit), boat speed, kite flying, and how far bells carry. A Xlokk day gives haze (fog distance), slow tempers (NPC lines) and "blood rain" that leaves red dust. A Grigal throws waves (particles, sound) at north-east coasts and keeps boats in.
- **Where/when:** everywhere; Grigal mostly autumn and winter, Xlokk spring and autumn.
- **Why Maltese:** every Maltese picks their beach by the wind.

### 52. Summer heat and the siesta *(art: none)*
- **You get:** in July and August, the middle of the day is hard. Villages go silent, shutters close, the streets empty, and everything wakes again at five.
- **How:** from about 1 to 4 on summer afternoons NPCs go indoors and shops shut. In the sun you tire faster (hunger drains a little quicker) unless you're in shade, in the sea, wearing a straw hat or have had a drink. Resting indoors at this time gives a rested bonus for the long evening. Gentle, never deadly.
- **Where/when:** June to September, midday.
- **Why Maltese:** the island runs on two shifts in summer.

### 53. The first rain (l-ewwel xita) *(art: none)*
- **You get:** after months of drought, the first real storm of September or October. People come to their doors. The land smells. Snails come out everywhere, the valleys run, frogs call.
- **How:** a marked event once a year. Snails (bebbux) can be gathered for a day or two on walls and fennel stalks (food idea already in the list). Valley biomes get running-water sound and particles. NPCs comment for days.
- **Where/when:** September or October.
- **Why Maltese:** the day the summer breaks is felt by everyone.

### 54. The wall calendar *(art: low)*
- **You get:** the church calendar that hangs in every Maltese kitchen: today's saint, the moon, the feasts this week, what's in season, the wind.
- **How:** an item you hang or hold. One screen: date in Maltese (Jannar, Frar… it-Tnejn, it-Tlieta…), the nearest festa and how far it is, what fish and crops are in, tonight's moon. It's the mod's main "what's on" page.
- **Where/when:** always.
- **Why Maltese:** every house has one by the kitchen door.

### 55. What the year gives, month by month *(art: none)*
A foraging and work calendar, tied to real seasons (uses the plants and crops already listed):
- **December to March:** wild asparagus (spraġġ) and wild greens; narcissus in the valleys; oranges; almond blossom in February.
- **Spring:** broad beans (the first ful, eaten raw in the field); artichokes; strawberries at Mġarr (a strawberry day in April); capers in bud.
- **June:** wheat harvest and threshing; thyme in flower on the garrigue and the best honey of the year.
- **July and August:** tomatoes, and making kunserva and sun-dried tomatoes on the roof; figs; prickly pears; carob pods; salt.
- **15 August on:** lampuki.
- **September:** the grape harvest and wine pressing; pomegranates; birds of prey over Buskett.
- **October and November:** olives and the oil press (an olive oil day at Żejtun in late September); the first rain and snails; a bread night at Qormi.
- **Why Maltese:** people still measure the year by what's ripe.

---

## 7. Work and crafts

### 56. Salt pans *(art: none to low)*
- **You get:** make sea salt the old way: fill shallow rock pans with sea water, let the sun dry them over a summer week, sweep the salt into heaps, bag it.
- **How:** in the world's `salina_saltworks` biome (and on any flat coastal rock the player cuts pans into), a water source in a one-block-deep pan slowly turns to a salt layer in sun (a recoloured snow layer). Rain or a Grigal ruins it. No salt in winter. The Xwejni family buys and teaches.
- **Where/when:** Xwejni near Marsalforn, Salina, Delimara, Marsaskala; May to September.
- **Why Maltese:** the Xwejni pans have been worked by the same families for generations.

### 57. Gozo lace (il-bizzilla) *(art: low)*
- **You get:** women at their doors in Gozo making lace on a long pillow with dozens of bobbins, fingers flying. You can learn.
- **How:** a pattern mini-game: repeat a short sequence that gets longer (like a memory game) to make lace pieces. Lace is a trade good and a decoration (a white glass-pane-like pattern block: low art). Taught by the lace maker; only in Gozo.
- **Where/when:** Gozo: Xagħra, Għarb, Sannat, Victoria; on doorsteps in daylight.
- **Why Maltese:** Gozo lace is known everywhere.

### 58. Stone: the quarry and the mason *(art: none)*
- **You get:** cut the soft golden stone (il-franka) in neat blocks, let it weather hard, and build with it as Maltese builders do.
- **How:** the world's stone already has the right vanilla blocks. The mod adds the craft: a mason who buys clean-cut blocks, teaches patterns (corner stones, a stone arch, a flat roof on stone slabs, a well head), and judges your building. Freshly cut stone is pale and darkens to honey over game weeks (a tint or a swap to a darker vanilla block the player placed).
- **Where/when:** Mqabba, Qrendi, Siġġiewi for the franka; Gozo for its own.
- **Why Maltese:** the whole country is built from one stone.

### 59. Rubble walls and the girna *(art: none)*
- **You get:** build a dry-stone wall (ħajt tas-sejjieħ) by hand, and a corbelled stone hut (girna) for shade in your field.
- **How:** stones picked from tilled fields (a drop when you hoe in field biomes) stack into a wall block by block with no mortar item. A finished wall around a field holds the soil: crops inside grow better and rain doesn't wash them out. A round hut of the right shape is recognised as a girna and gives shade and tool storage.
- **Where/when:** field biomes; giren are most common around Mellieħa and the north-west.
- **Why Maltese:** the walls are what makes a Maltese landscape. The world has them; this lets players make their own.

### 60. Luzzu fishing *(art: low to medium)*
- **You get:** a painted boat with eyes on the bow, and the fishing year: lampuki under floating palm fronds in autumn, octopus pots, traps for bogue, lamp fishing on dark summer nights, swordfish and tuna far out in early summer.
- **Update 2026-11-17:** the owner chose a real luzzu model, not a recolour; see [[Luzzu]].
- **How:** a recoloured vanilla boat in luzzu colours (yellow, red, green, blue) with the eye of Osiris painted on (low art; a new boat model would be medium). Kannizzati: place rafts of palm fronds on the open sea from 15 August; fish gather in their shade over days; come back and net around them. The eyes give a small luck bonus. Lamp fishing: a lantern on the boat on moonless nights draws fish and squid.
- **Where/when:** Marsaxlokk, Mġarr, Marsalforn, St Paul's Bay; by season.
- **Why Maltese:** the lampuki season and the luzzu are the Maltese sea.

### 61. The Sunday fish market *(art: none)*
- **You get:** every Sunday morning the quay at Marsaxlokk is one long market. Sell your week's catch at the best price, and buy what you didn't catch.
- **How:** many traders at the quay coordinates on Sunday mornings only. Prices move with what was caught that week.
- **Where/when:** Marsaxlokk, Sunday morning.
- **Why Maltese:** the best-known market on the island.

### 62. Bees and honey by flower *(art: none)*
- **You get:** honey that tastes of where and when it was made: spring wildflower, thyme in June (the famous one), carob and eucalyptus in autumn.
- **How:** vanilla bees and hives. The honey's type depends on the season and the biome around the hive. Thyme honey needs a hive on the garrigue in June. Old-style hives are clay jars laid in a stone wall (a decorated pot in a wall: no art).
- **Where/when:** Mellieħa (the old Roman bee houses at Xemxija), the garrigue.
- **Why Maltese:** Malta's old name, Melite, is tied to honey.

### 63. Smaller crafts, one line each *(art: low each)*
- **Reed work (xogħol tal-qasab):** cut reed (the world's valleys have it as vanilla blocks) into fish traps, baskets, blinds and windbreaks.
- **Filigree (filugranu):** twist gold or silver nuggets into a Maltese cross and other pieces; a gift item that raises standing.
- **Blown glass:** coloured glass vases from a furnace, in sea colours.
- **The Maltese clock (l-arloġġ tal-lira):** a gilded wall clock with one hand; a craft with many steps, a prestige piece.
- **Hand-painted lettering (it-tberfil):** signs in the flowing style of the old buses and carts (a font, no model).
- **The windmill and the animal-turned well wheel (il-mitħna, is-sienja):** grind your wheat at a miller NPC; a donkey walking in a circle lifts water for your field (vanilla animal on a lead: none).
- **Cheeselets on the roof:** ġbejniet dry in a mesh box in the wind; taste depends on days dried (fresh, dried, peppered).

---

## 8. The sea and the shore

### 64. The swimming season *(art: none)*
- **You get:** the sea has a temperature. Nobody swims before the first hot days, the whole island is in the water in August, and the brave swim on New Year's Day.
- **How:** sea temperature follows the calendar. Cold water tires you; summer water cools and restores you after the heat (idea 52). The first swim of your year is marked. NPCs swim off the rocks from ladders (a ladder on a rocky shore attracts swimmers).
- **Where/when:** all coasts; June to October.
- **Why Maltese:** summer is lived in the sea.

### 65. Reading the sea *(art: none to low)*
- **You get:** before you jump in, you look: which way is the wind, are there jellyfish, is there a swell.
- **How:** a lifeguard NPC or a flag item at beaches shows the state from the wind (idea 51). Jellyfish (in the creature list) drift in with certain winds; a sting hurts a little. Sea urchins on rocky bottoms sting bare feet: enter by the ladder. Vinegar or a fresh-water rinse cures it.
- **Where/when:** all beaches and rocky shores, summer.
- **Why Maltese:** "Hemm il-brim?" (are there jellyfish?) is the first question at any bay.

### 66. A day at the beach *(art: none)*
- **You get:** the full kit: umbrella, cool box, ftira and bread with oil, watermelon in the sea to keep it cold, a barbecue on the sand at night with everyone you know.
- **How:** placing a campfire and a few seats on a beach on a summer evening draws family NPCs with food; eating together gives the shared-meal bonus (idea 67). A melon left in shallow water becomes "chilled" and restores more.
- **Where/when:** Għadira, Golden Bay, Ġnejna, Ramla l-Ħamra, Pretty Bay, Armier; summer nights.
- **Why Maltese:** the beach barbecue is the summer social event.

### 67. Snorkelling and diving *(art: low)*
- **You get:** a mask to see clearly underwater, and real dive sites to log: the Blue Hole and Inland Sea at Dwejra, the Santa Marija caves at Comino, the reefs at Ċirkewwa, Għar Lapsi, Wied iż-Żurrieq.
- **How:** a mask item (a recoloured helmet) clears underwater vision and lets you log sea life for the nature log. A dive log lists the real sites by coordinates and stamps each one when you reach its depth. The world's measured sea caves are already there.
- **Where/when:** all year for divers; the named sites.
- **Why Maltese:** some of the best diving in the Mediterranean is here, and the world has those caves at 1:1.

### 68. Boat trips *(art: none)*
- **You get:** pay a boatman at Wied iż-Żurrieq and he takes you through the Blue Grotto caves in the morning light, naming each cave. Or a trip round Comino, or under the cliffs at Ta' Ċenċ.
- **How:** an NPC boatman steers a vanilla boat along a fixed path while you sit; he talks. Only on calm mornings (the wind decides).
- **Where/when:** Wied iż-Żurrieq (mornings, when the light is right), Mġarr, Ċirkewwa, Xlendi, Dwejra's Inland Sea tunnel.
- **Why Maltese:** the boat trip everybody has taken, in the measured caves the project already built.

### 69. The regatta *(art: low)*
- **You get:** rowing races in the Grand Harbour under the bastions, crowds on the walls, harbour towns against each other for a shield.
- **How:** a rowing race on a fixed course (a timed boat race with a rhythm for the oars). Seven harbour districts compete; you row for the one where you have standing. NPC crowds cheer from above.
- **Where/when:** 31 March and 8 September; the Grand Harbour.
- **Why Maltese:** rowed since the Knights; the harbour towns live for it.

### 70. Water polo and the summer pitch *(art: none)*
- **You get:** a roped-off patch of sea with two goals, a ball, and a crowd on the rocks.
- **How:** a simple ball game in the water between two goals (the player marks the pitch with ropes or buoys). NPC teams play on summer evenings.
- **Where/when:** summer; sea-side pitches at Sliema, St Julian's, Marsaskala, Birżebbuġa, Marsaxlokk.
- **Why Maltese:** the summer sport, played in the sea itself.

---

## 9. Leisure and games

### 71. Boċċi *(art: low)*
- **You get:** the Maltese game of bowls on a sandy pitch, with old men who take it very seriously and comment on every throw.
- **How:** a throwing game on a strip of sand the player lays (the mod recognises a pitch of the right size). Throw to land nearest the small jack; round bowls and the Maltese cylinder-shaped ones behave differently. Play against NPCs; beating the village champion is gossip for a week.
- **Where/when:** every village has a pitch beside a club bar.
- **Why Maltese:** the Maltese form of the game is its own.

### 72. The fenkata *(art: none)*
- **You get:** a long, loud rabbit meal with a big group: spaghetti with the rabbit sauce first, then the rabbit, then nuts and a lot of talk.
- **How:** a shared meal for several players or NPCs at one long table: the dishes from the food list eaten in the right order give a strong, long bonus to everyone at the table. More people, better bonus.
- **Where/when:** Mġarr and Baħrija are the fenkata villages; any long table.
- **Why Maltese:** the national meal, and never eaten alone.

### 73. Horses: Marsa, the roads at dawn and the sea *(art: low)*
- **You get:** trotting races at the Marsa track on Sundays; men exercising trotters on country roads at first light; horses led into the sea to swim on summer mornings.
- **How:** a trotting race is a horse race where breaking into a gallop loses time: hold a steady pace. A light two-wheel cart (the sulky) is the one piece of new art (low to medium; a minecart recolour is the low version). NPC horses swim at dawn at a few bays. No betting.
- **Where/when:** Marsa on Sundays; Xagħra and Victoria street races at feasts; Imnarja at Rabat.
- **Why Maltese:** horse racing is a deep passion, in the villages as much as at the track.

### 74. Football and the two tribes *(art: none)*
- **You get:** a village pitch and a ball; and every two years the island splits in two, for Italy or for England, with flags on balconies and car horns after a win.
- **How:** a simple ball you kick, goals from any frame. During the real tournament weeks, NPCs hang one of two flag colours and tease the other side; a "win" night fills the streets with horns and flags.
- **Where/when:** village pitches; summer tournament weeks.
- **Why Maltese:** the horn parade for someone else's team is pure Malta.

### 75. Kites, picnics and a day in the country *(art: low)*
- **You get:** a kite (tajra) on a windy headland; a picnic under the carob trees; a walk along the cliffs to watch the sun set over Filfla.
- **How:** a kite item that flies with the day's wind (a banner on a lead: low art). A picnic: a blanket (carpet) and food shared outdoors in the green months gives a rested bonus. Sunset from Dingli Cliffs, the Citadel walls, Dwejra or Golden Bay is logged in a "sunsets" page.
- **Where/when:** Buskett, Mtaħleb, Dingli, Selmun, Ta' Ċenċ; November to May for picnics.
- **Why Maltese:** the Sunday outing to the country when it's green.

### 76. The children's games *(art: none)*
- **You get:** games children play in the street: marbles, hopscotch (passju), hide and seek (noli), and in Għarb a nine-pin game found nowhere else (il-brilli).
- **How:** small games with child villagers using vanilla items. Brilli: knock down nine wooden pins with a ball in the street at Għarb.
- **Where/when:** squares and quiet streets; brilli only at Għarb, Gozo.
- **Why Maltese:** street games, and one that survives in a single village.

### 77. Racing pigeons *(art: none to low)*
- **You get:** a loft on your roof, birds that know their home, and race days when everyone watches the sky.
- **How:** a recoloured parrot or the mod's pigeon. Birds released far away fly home to your loft; time is your score. Races from Gozo first, then "from Sicily" (released by an NPC at the coast). Birds are bred and cared for, never harmed.
- **Where/when:** rooftops everywhere; the south is keenest.
- **Why Maltese:** rooftop lofts are part of the skyline.

### 78. Cards, tombla and the nanna's numbers *(art: low)*
- **You get:** a card game in the bar (bixkla), a parish bingo night (tombla), and a nanna who turns your dreams into numbers.
- **How:** bixkla as a simple card screen against NPCs for pride only. Tombla at the parish hall: free cards, the caller's rhymes in Maltese, prizes are a hamper of food. When you sleep, the nanna tells you next morning what your dream "means" as a number: a joke only. Nothing is bought, staked or paid out in any form.
- **Where/when:** village bars; winter evenings.
- **Why Maltese:** tombla nights raise money for the festa. Kept cosmetic.

---

## 10. Food as a social thing

(The dishes are already in the list. These are about **how** we eat.)

### 79. The shared table *(art: none)*
- **You get:** food eaten with others is worth more than food eaten alone.
- **How:** the same dish gives a longer, better effect when two or more people (players or NPCs) eat at one table. Someone says "L-ikla t-tajba". Guests always get offered more ("Ħu ftit ieħor!") and refusing twice is the polite way to say yes.
- **Where/when:** always.
- **Why Maltese:** nobody leaves a Maltese house hungry.

### 80. Sunday lunch and the baker's oven *(art: none)*
- **You get:** on Sunday morning you carry your dish of meat and potatoes to the village baker, leave it with your name, go to the square, and collect it hot at noon.
- **How:** give a raw oven dish (baked rice, timpana, potatoes and meat) to the baker; get it back later, better than your own furnace makes. Sunday lunch at home with family NPCs or friends gives the week's best food bonus.
- **Where/when:** Sundays, every village.
- **Why Maltese:** within living memory the whole street's lunch cooked in one oven.

### 81. The kiosk and the tea in a glass *(art: none)*
- **You get:** a small kiosk by the sea or the bus stop: tea in a glass, a hot pastizz, a bench, and people who have all the time in the world.
- **How:** a counter and a sign built by the player becomes a kiosk with an owner. Sitting there for a minute gives rumours and a rested effect.
- **Where/when:** seafronts, squares, bus stops.
- **Why Maltese:** the kiosk is the island's meeting point.

### 82. Bread, properly *(art: none)*
- **You get:** bread that's best in its first hours: crusty at dawn, fine at noon, hard by tomorrow, and never thrown away.
- **How:** Maltese bread has a freshness timer. Stale bread becomes bread pudding, soup thickener or fish bait. A dropped piece of bread: old people pick it up and kiss it (a line of text).
- **Where/when:** always.
- **Why Maltese:** the respect for bread.

---

## 11. Getting around

### 83. The bus (tal-linja) *(art: none, or medium with a bus)*
- **You get:** wait at the stop, wonder if it's coming, squeeze on, ring the bell, get off in another town.
- **How:** bus stops are just points from the parish table (and signs players place). A driver NPC arrives; pay a small fare; the ride is a short fade with engine and horn sounds; you arrive at the chosen parish. Real quirks: almost every route goes through Valletta; it's sometimes late or full in summer. The old buses' hand-painted names and sayings appear as text ("the driver's bus is called …"). A visible bus you ride in is the medium-art version.
- **Where/when:** all of Malta and Gozo; fewer at night.
- **Why Maltese:** the old buses are loved and missed. It's also the fast travel a 1:1 island needs.

### 84. The Gozo ferry *(art: none)*
- **You get:** the crossing: the queue, the horn, Comino sliding past, the Citadel on the skyline as you come in to Mġarr.
- **How:** an NPC at Ċirkewwa and at Mġarr. Either an instant fade or, better, a real 25-minute-style crossing shortened to a few minutes on a moving platform or boat while you stand at the rail. One true detail: you only pay on the way back from Gozo. Cancelled in a strong Grigal.
- **Where/when:** Ċirkewwa and Mġarr, every 45 minutes.
- **Why Maltese:** "crossing over" is a feeling every Maltese and Gozitan knows.

### 85. The dgħajsa and the harbour ferry *(art: low)*
- **You get:** a painted water taxi across the Grand Harbour for a coin, the boatman standing to row.
- **How:** a recoloured vanilla boat with an NPC rower on short fixed routes: Valletta to the Three Cities, Valletta to Sliema.
- **Where/when:** the two harbours.
- **Why Maltese:** the harbour's own boat.

### 86. The karozzin *(art: none to medium)*
- **You get:** a slow horse-cab ride with a driver who tells you about every building.
- **How:** low version: you ride a horse led by the driver along a route while he talks. A carriage model is medium art.
- **Where/when:** Valletta, Mdina, Sliema front.
- **Why Maltese:** in use since the 1850s.

---

## 12. History you live in

### 87. The tower signal chain *(art: none)*
- **You get:** light a fire on a coastal watchtower's spot at night, and the next tower along the coast answers, then the next, all the way to Valletta.
- **How:** the mod knows the towers' coordinates. A fire lit by a player at one makes a beacon light (particles or a light beam) appear at the next ones in turn. Relighting the whole chain from Gozo to the Grand Harbour is an advancement. Works on bare terrain, with no tower building needed.
- **Where/when:** the Knights' coastal towers, all round the islands, at night.
- **Why Maltese:** this is how the Knights' towers really warned Valletta of corsairs.

### 88. Sunrise at Mnajdra *(art: none)*
- **You get:** stand at the temple's doorway spot at dawn on the equinox and the first light runs straight down the passage. At the solstices it strikes the edges of the inner slabs.
- **How:** on 20 March, 21 June, 22 September and 21 December, at sunrise, at Mnajdra's coordinates, a beam of light particles and a quiet title. An advancement for each of the four.
- **Where/when:** Mnajdra, Qrendi; four mornings a year.
- **Why Maltese:** a 5,000-year-old calendar that still works.

### 89. The stories of places *(art: none)*
- **You get:** at the right spot a nanna or a found book tells the place's legend, and sometimes the game plays along:
  - **Il-Maqluba, Qrendi:** the village that sank for its sins, leaving only the chapel.
  - **Ġgantija, Xagħra:** the giantess who carried the stones on her head, eating broad beans.
  - **Fungus Rock, Dwejra:** the plant the Knights guarded with their lives.
  - **Calypso's cave, above Ramla:** the nymph who kept Ulysses seven years.
  - **San Dimitri, Għarb:** the saint who rode out of his painting to save a widow's son; the light under the sea.
  - **Wied Speranza, Mosta:** the girl hidden from raiders by a spider's web.
  - **Għar Ħasan:** the cave of the last Saracen.
  - **St Paul's Bay:** the shipwreck, and why Maltese snakes have no venom.
- **How:** a "stories" book that fills in as you visit each place. Small plays-along are effects only: a light under the sea off San Dimitri at night; a web across a cave mouth at Wied Speranza.
- **Where/when:** each legend's real place.
- **Why Maltese:** every corner of the island has a story our grandparents told.

### 90. The bogeymen *(art: none)*
- **You get:** what Maltese children were warned about: **il-Belliegħa**, who lives in wells and pulls down children who lean over; **il-Gawgaw**, who walks on Christmas Eve night; **il-Ħares**, the house spirit who leaves you gifts as long as you never tell anyone.
- **How:** lean over a deep well too long: a sound and a tug. Il-Ħares: now and then a small gift appears in an old house you live in; if you mention it in chat, the gifts stop. A light, spooky touch; optional.
- **Where/when:** wells; old houses; Christmas Eve.
- **Why Maltese:** our own folklore, not vanilla's zombies.

### 91. The siren and the shelter *(art: none)*
- **You get:** on certain days an air-raid siren sounds as a memory. Players can dig a shelter into the rock as families did, and a nannu tells what it was like.
- **How:** a commemorative event with sound only: no bombs, no damage. Stories from an old NPC: the shelters, the hunger and the Victory Kitchens, the convoy that came in on Santa Marija. On 15 April the George Cross is remembered with a small ceremony and a medal item for players who heard the stories. On 9 April at Mosta, the story of the bomb that fell through the dome and didn't explode.
- **Where/when:** 15 April; 15 August in the Grand Harbour (the convoy); Mosta.
- **Why Maltese:** the war is still family memory. Done as remembrance, not as a game of war.

### 92. The Knights and the Great Siege as a walk *(art: none)*
- **You get:** a trail through the real places of 1565, told day by day: St Elmo, Birgu, Senglea, Mdina, the relief landing at Mellieħa.
- **How:** a book of stations with coordinates. At each, the story of what happened there and a stamp. Finishing on 8 September joins Il-Vitorja.
- **Where/when:** the harbour, Mdina, the north.
- **Why Maltese:** the story every Maltese child learns.

### 93. The cart ruts and other mysteries *(art: none)*
- **You get:** a "mysteries" page: the cart ruts nobody can explain, the temples older than the pyramids, the underground temple.
- **How:** logged by visiting the coordinates; each gives the competing explanations and lets the player pick the one they believe.
- **Where/when:** Misraħ Għar il-Kbir near Dingli, Ħaġar Qim, Ġgantija, Ta' Ħaġrat, Skorba.
- **Why Maltese:** we live on top of things nobody fully understands.

---

## 13. Identity and humour

### 94. The passport of the 68 *(art: none)*
- **You get:** a book with a page per locality, stamped when you've been there, eaten there and been greeted there. Each page has the name's meaning, the motto, the patron and what the village is known for.
- **How:** from the parish table. A reason to walk the whole 1:1 island.
- **Where/when:** all 68.
- **Why Maltese:** we're 68 villages before we're one country.

### 95. Malta and Gozo *(art: none)*
- **You get:** gentle teasing both ways. Gozitans are careful with money and proud; the Maltese are loud and always in a hurry. Life on Gozo runs slower: NPCs walk slower, shops open later, people talk longer.
- **How:** different line banks and routines by island. A Gozitan home parish gets you a "one of ours" welcome in Gozo and friendly suspicion in Malta.
- **Where/when:** crossing the channel.
- **Why Maltese:** the oldest friendly rivalry we have.

### 96. Small truths *(art: none)*
A bank of little moments that make a Maltese player laugh:
- Two NPCs "arguing" loudly are only saying hello.
- "Mela" works as an answer to everything.
- Ask the way and you get landmarks, not street names: "turn at the niche, after tal-pastizzi".
- Everyone knows a cousin who can fix it.
- "Issa naraw" (we'll see) means no.
- The moment it rains, everyone complains about the rain; the moment it stops, about the heat.
- A nanna who thinks you're too thin, always.
- **Why Maltese:** we recognise ourselves and laugh.

### 97. The emigrant's return *(art: none)*
- **You get:** now and then an NPC comes back from Australia, Canada or England after forty years, with a changed accent, looking for the house he was born in.
- **How:** a rare visitor who asks you to walk him to a place in his old village and tells you what it was like. A quiet, touching task.
- **Where/when:** summer, festa time.
- **Why Maltese:** nearly every family has someone who left.

---

## The first version: 15 ideas with the most feeling for the least work

Almost all are text, data and sound.

| # | Idea | Why first | Art |
|---|---|---|---|
| 1 | **Place names that speak** (41) | Pure data. Makes the whole 1:1 world feel named and known from the first minute. | none |
| 2 | **The parish table and parish standing** (base A, 16) | Everything else hangs on it. | none |
| 3 | **The bells** (37) | One set of sounds brings every village to life. | low |
| 4 | **The soundscape** (47): cicadas, crickets, shearwaters, harbour | Huge feeling, no models. | low |
| 5 | **The Maltese mix and greetings** (18, 43) | People sound Maltese at once. | none |
| 6 | **Kelma kelma word book** (42) | Unique: a game that teaches Maltese. | none |
| 7 | **The nanna on the doorstep and "Ta' min int?"** (1, 2) | The warmest single picture of village life. | low |
| 8 | **The wall calendar** (54, base B) | The page that shows what's on and in season. | low |
| 9 | **The village festa, simple form** (28, 30, 31): bells, petards, a band march, night fireworks | The heart of the year. Start with sound, crowds and fireworks; the statue and decorating come later. | low |
| 10 | **The winds by name** (51) | Changes where you swim and fish every day; all text and rules. | none |
| 11 | **The colour of the land and the first rain** (50, 53) | The green and brown island with no new art. | none |
| 12 | **The pastizzi seller, baker and hawkers with horns** (3, 11, 12) | Daily life and food as a social thing. | low |
| 13 | **Your laqam** (44) | Funny, personal, and all text. | none |
| 14 | **The tower signal chain and sunrise at Mnajdra** (87, 88) | Two "wow" moments from coordinates and particles only. | none |
| 15 | **The shared table and the fenkata** (72, 79) | Makes the 40 dishes already listed social. | none |

Good next wave: the bus and Gozo ferry (83, 84), salt pans (56), luzzu and kannizzati (60), the Christmas crib (38), Holy Week and Easter (36), boċċi (71), the stories of places (89), the passport of the 68 (94).

---

## Layer 3 (later): ideas that need generation or built towns

Not for this mod. Kept so they aren't lost.

- Real parish churches, squares and band club buildings for the festa to happen in and around.
- Street niches, wells, bus stops, kiosks and boċċi pitches already standing in the villages.
- Luzzi and dgħajjes moored in the harbours from the start.
- Carnival floats and a true karozzin and old bus as models on real streets.
- Fixed street decorations and statue pedestals in festa streets.
- War shelters, the wartime airfields and the Victoria Lines as built places to explore.
- Wrecks at the real dive sites (the mod can use vanilla shipwrecks for now).
- The temples, towers and forts as buildings, so the signal chain and the sunrise happen in real stone.
- Giren, farmhouses, windmills and threshing floors placed across the countryside.
- Salt pans cut in the rock at every real site (the world has the Xwejni biome; the others would need generation).
- Fishing villages' boathouses and slipways; the Marsa race track; village football pitches.

---

## Questions for the owner

1. **The calendar:** should the mod follow the **real date** (festa in Mosta on the real 15 August, lampuki from the real August), or a **faster in-game year** so players see every season in a few weeks of play? Or real dates with an option?
2. **Faith and festa:** how present should religion be? Suggested: festa, bells, processions and feasts shown warmly and plainly, the player free to join or only watch. Is that the right tone, and is anything off limits (the statue, the priest, Good Friday)?
3. **Language:** how much Maltese should people speak: mostly English with Maltese words, a true half-and-half mix, or a setting from "tourist" to "Malti"?
4. **Band club rivalry:** made-up clubs with colours only (suggested), or leave rivalry out?
5. **The man on the ridge (idea 7):** keep him as a countryman who knows birds and weather, with no hunting in play, or leave him out and keep only the birdwatcher?
6. **The war (idea 91):** is a remembrance-only version (siren, stories, the George Cross day, no bombing) right, or should the war stay out?
7. **Single player or shared:** will most people play alone, or on a server together? It changes how much the festa, the regatta and the fenkata should lean on other players.
8. **Where to start:** does the first-version shortlist feel right, or is there one thing (the festa in full, the bus, the luzzu) you'd want before anything else?
