#import "@preview/starter-journal-article:0.4.0": article, author-meta

#show: article.with(
  title: "Balatro-KI",
  authors: (
    "Jul Lang": author-meta(
      "",
      email: "jullanggit@proton.me",
    ),
    "Dan Lut": author-meta(
      "",
      cofirst: true,
      email: "zadowcloud.0@gmail.com"
    ),
  ),
  affiliations: (
    "": ""
  ),
)
#set heading(numbering: "1.")
#set text(
  size: 10.95pt //Are we like making it as close as possible XD, absolutely :D (mabe like 2 digits tbh) (seems good ) hell yeah nailed it CINEMAAAAAAAAA
)

= Thema
== Einleitung
Balatro ist ein pokerinspiriertes Roguelike-Strategiespiel des Indie-Entwicklers LocalThunk. Trotz seines limitierten Budgets wurde es innerhalb von kürzester Zeit ein Überraschungshit auf Steam. Auch wir entwickelten schnell eine Leidenschaft, und haben mittlerweile beide je um die 250 Stunden in das Spiel investiert. Als sich also bei diesem Projekt die Möglichkeit bot uns mehr damit zu beschäftigen, mussten wir diese Gelegenheit nutzen. So entstand die Idee, eine KI zu entwickeln, die das Spiel eigenständig spielen (und hoffentlich meistern) kann.
== Fragestellung
Eine natürliche Option für die Fragestellung wäre, ob wir es schaffen, eine KI zu trainieren, die das Spiel schlägt, was bei Balatro heisst, den "Ante" (ein Zusammenschluss aus drei etwas unterschiedlichen Runden) 8 zu schlagen, auch wenn danach noch ohne Einschränkungen weiterspielen kann. Andererseits gibt es auch einige andere Werte, die man in Balatro versuchen könnte zu maximieren, zum Beispiel das Geld, den Score, oder die Anzahl gewonnene Runden. Wir haben uns für letzteres entschieden, da es weniger "alles oder nichts" ist als die erste Option, aber dennoch den zentralen Aspekt des Spieles verfolgt, im Gegensatz zu Geld und Score, die eher ein Mittel zum Zweck sind. Somit lautet unsere zentrale Fragestellung: *"Ist es möglich eine Balatro KI zu programmieren? Wie viele Runden schafft sie innerhalb von dieser limitierten Zeit?"* \
Nichtsdestotrotz sind wir natürlich auch sehr interessiert an den Taktiken der KI, welche Wechselwirkungen entdeckt werden und welche Aspekte des Spiels die KI meistern wird.

= Planungsphase
== Deep Reinforcement Learning: Geschichte
Historisch hatte die KI-Trainingsmethode "Deep Reinforcement Learning" grosse Erfolge im Bereich der Spiel-KIs, so konnte z.B. die KI AlphaGo von DeepMind im Jahre 2016 erstmals den Go Weltmeister schlagen! @deepmind-alphago \
Auch wenn Deep-RL zwischenzeitlich etwas in den Hintergrund rückte, hat es momentan eine kleine Renaissance und blüht nach grossem Erfolg in LLMs wie Deepseek R1 @deepseek wieder auf. \
== Typus der KI
Da es sich bei Balatro dank seiner vielfältigen Interaktionen zwischen Spielkarten, Modifikationen, Jokers usw. um ein ähnlich komplexes Spiel wie Go handelt, scheint uns die Trainingsmethode die dieses meisterte eine gute Wahl, spezifisch eine *Online Deep Reinforcement Learning KI*  @huggingface-deeprl-offline-online, da es keinen Datensatz von Spielen gibt, den die KI imitieren könnte um "offline" zu trainieren. \
Es beginnt damit, dass der Agent den Spielzustand erhält indem er sich befindet. Daraufhin wählt der Agent eine Handlung, z.B. eine Pokerhand spielen, welche sich auf die Umgebung, das Spiel, auswirkt und deren Zustand verändert. Hat die Handlung nach manuell gewählten Kriterien einen guten Effekt auf den Spielzustand, so erhält die KI eine Belohnung. Dieser Prozess wiederholt sich kontinuierlich und durch Trial & Error lernt die KI welche Handlungen vorteilhaft sind und passt sein Verhalten an @wikipedia-reinforcement-learning @studyflix-reinforcement-learning. \
== Zeitplan
Wir entschieden uns bis zum 11. so gut wie möglich die Umgebung funktionsfähig zu machen und bis zum 18. die eigentliche KI fertigzustellen. (Steht noch etwas ausführlicher im Zwischenbericht)

= Erfahrungen
== Umgebung
=== Suche
Nach einer ersten Suche stossen wir auf einen Balatro Mod @balatrobot-github, welcher als Umgebung geeignet sein könnte: Er stellt eine API für Handlungen und Spielzustand zur Verfügung. Da Lua, die Programmiersprache von Balatro und dessen Mods, nicht für seine KI-Fähigkeiten bekannt ist, entschieden wir uns, diese API von Rust aus zu konsumieren und dort das Burn framework @burn-dev zu verwenden um die KI zu trainieren. Leider stellte sich heraus das der Mod essenzielle Informationen, wie zum Beispiel Kartenmodifikationen, nicht liefert.
Daraufhin haben wir versucht, diese direkt aus dem internen Spielzustand zu extrahieren @balatro-bot-github, was aber selbst nach vielen Stunden Analyse desselben und Debugging immernoch häufig aus unerklärlichen Gründen einfror. Zudem hatte der Mod einige Bugs bei denen er ebenfalls einfror und keine Handlungen mehr annahm. \
In Anbetracht der verhältnismässig kurzen Deadline haben wir uns schweren Herzens entschieden diesen Ansatz hinter uns zu lassen und auf eine andere Umgebung umzuschwenken: Eine Kopie von Balatro in Python @python-balatro, welche einen weitaus sinnvoller strukturierteren, und besser dokumentierten internen Spielzustand hat, und die mit vergleichsweise wenig arbeit eine gute Umgebung bieten konnte. Vereinfachend kommt dazu, dass Python der Industrie-Standard für KI ist und es somit viel Tutorials und Dokumentation für die Entwicklung verschiedener KI-Modelle hat. Als Framework haben wir uns für PyTorch @pytorch-org entschieden, da es als anfängerfreundlicher als die grosse Alternative, TensorFlow @tensorflow-org, beschrieben wird @freecodecamp-pytorch-vs-tensorflow.
=== Implementation @python-balatro-ai
Um die Umgebung tatsächlich funktionstüchtig zu machen, implementierten wir zuerst einige Standardfunktionen, welche uns erlauben, die Umgebung zu initialisieren, neuzustarten und Aktionen auszuführen. Dies war für den Anfang genug, doch im Verlauf des Trainings wurde uns klar, dass die Menge an möglichen Aktionen der KI schlichtweg zu gross, und die Menge der legalen Aktionen zu klein waren: Wenn sich die KI in einer Runde befand waren lediglich #{2*(calc.binom(8,5) + calc.binom(8,4) + calc.binom(8,3) + calc.binom(8,2) + calc.binom(8,2) + calc.binom(8,0))} der $2^43$ möglichen Aktionen legal. Aufgrund dieser unmöglichen Wahrscheinlichkeit, sahen wir uns gezwungen, manuell legale Aktionen zu erzwingen. Auch wenn wir uns aus Zeitgründen nicht schafften, tatsächlich alle illegalen Aktionen zu verbieten, gelang es uns genug von diesen auszuschliessen, um der KI eine reale Chance zu geben, das Spiel zu meistern. Die letzte Verantwortung der Umgebung war es, die gespielten Aktionen aufzunehmen, damit wir sie zu einem späteren Zeitpunkt analysieren können.

== Architektur
Im Bereich der Spiel-KIs hat es eine riesige Auswahl an erfolgreichen Architekturen, wie zum Beispiel Deep-Q-Networks @mnih2013playingatarideepreinforcement @Mnih2015 mit seinen Erweiterungen wie Double-DQN @vanhasselt2015deepreinforcementlearningdouble, Dueling-DQN @wang2016duelingnetworkarchitecturesdeep und Rainbow @hessel2017rainbowcombiningimprovementsdeep, eine andere Option wären die Actor-Critic Architekturen, welche die die Advantage-Actor-Critic Familie @mnih2016asynchronousmethodsdeepreinforcement und die Algorithmen der Proximal Policy Optimization @schulman2017proximalpolicyoptimizationalgorithms beinhalten. Wir haben uns für letztere entschieden, da sie als sehr leistungsstark gelten, und ihre kontrollierten Updates der Policy für ein stabileres Training sorgen.

= Ergebnisse
Nach etwa 22'000 Instanzen und ungefähr einem Tag Training, erreichte die KI den Boss von Ante 4, also fast die Hälfte des Spieles! Es war sehr unterhaltsam der KI dabei zuzusehen, wie sie kleine Dinge über das Spiel herausfand. Recht schnell merkte sie bereits, dass die Karten links grösseren Werten entsprechen und folglich ein klein wenig mehr Punkte geben. Auch scheint sie simple Pokerhände wie Pair oder Three of a Kind zu verstehen. Das Verständnis von den tatsächlichen Jokern lässt momentan noch sehr viel zu wünschen übrig, kein Wunder, es gibt 150 davon! Noch schlimmer sind natürlich jegliche Booster Packs, die KI bleibt dort oftmals stecken, da sie nicht weiss, was sie mit Param 2 anstellen sollte. Es wäre sicher noch sehr interessant zu sehen, wie sich die KI mit weiterem Training und Verbesserungen entwickelt.

== Schlussfolgerung
Die Frage, ob es denn möglich sei, eine Balatro KI zu coden, lässt sich also mit einem klaren Ja beantworten. Wir mussten auf einen Python Port zurückgreifen, da das tatsächliche Spiel uns zu viele Kopfschmerzen bereitete, jedoch bleibt das Konzept des Spieles ja dasselbe. Unsere KI schaffte es, wie erwähnt, bis zu Ante 4 was hier der Runde 11 entsprach und einer erforderten Punktzahl von 20'000.

= Reflexion
== Planung
Wie korrekt von Herr Forny vorhergesagt, war unsere Planung zu knapp bemessen. Die eigentliche KI funktionierte zwar bereits ungefähr am 20, also etwa 2 Tage später als vorhergesagt, jedoch waren eigentlich alle der Aktionen der KI illegal. Daher mussten wir uns für eine relativ lange Zeit damit beschäftigen so gut wie möglich illegale Aktionen nicht zur Verfügung zu stellen, bei einem Spiel wie Balatro wird das jedoch sehr schnell sehr komplex. Auch tauchten einige Anomalien auf, die wir nicht mehr beheben konnten, es ist aber dennoch sehr interessant über diese zu sprechen!
== Anomalien
Statt von Bestrafungen abzuschrecken wies unsere KI manchmal auch auf ein etwas... masochistisches Verhalten auf, sie machte nämlich oftmals weiter mit derselben illegalen Handlung, obwohl sie jederzeit durch eine andere Handlung weitermachen könnte. In einer Instanz erreichte die Gesamtbelohnung ungefähr -9'000, das sind ungefähr 1'800 illegale Handlungen!! Das passierte nahezu bei jeder Instanz bei welcher ein Planet Pack geöffnet wurde, da hier das Param 2 leer sein muss. Interessanterweise fand die KI sogar einen Bug in der Python Version! Mit einem bestimmten Blind Skip Tag, sind alle Rerolls im Shop permanent gratis. Wir werden dies vermutlich dem Entwickler noch melden.
== Lieblingsversuch
Wir fanden überraschenderweise einen Lieblingsversuch, auch hier blieb die KI stecken, dieses Mal im Shop, da sie bereits 5 von 5 Jokern hatte und somit keine neuen erwerben konnte. Das ging so weit, dass sie schliesslich einen Grossteil ihrer Joker verkaufte um etwas neues zu kaufen. Da war jedoch der Joker "Credit Card" dabei, welcher der KI erlaubte bis zu 20 Dollar im Minus zu sein. Nach dem Fiasko war die KI schliesslich verschuldet, konnte nichts neues kaufen und ihr blieb weniger als zuvor. In der nächsten Runde starb sie einen poetischen Tod. \ \
#set text(
  style: "oblique"
)
"The day a blind man sees. The first thing he throws away is the stick that has helped him all his life."
#set text(
  style: "normal"
)
#figure(
  image("stuff/best_run.png", width: 100%),
  caption: [
    Der finale Spielzustand des besten Runs der KI
  ],
)
#figure(
  image("stuff/stuck_celestial_pack.png", width: 100%),
  caption: [
    Der Spielzustand des Planet-Pack Param 2 Problems
  ],
)
#figure(
    grid(
      columns: 3,
      gutter: 2pt, // optional
      image("stuff/full_jokers.png", width: 100%),
      image("stuff/4.png", width: 100%),
      image("stuff/2.png", width: 100%),
      image("stuff/0.png", width: 100%),
      image("stuff/select.png", width: 100%),
      image("stuff/loss.png", width: 100%),
    ),
    caption: [
    Der Spielverlauf unseres Lieblingsversuches
  ],

)
#bibliography("sources.bib")
