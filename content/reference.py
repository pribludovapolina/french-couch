# -*- coding: utf-8 -*-
"""Справочник для вкладки «Теория»: времена, построение предложения, глаголы, предлоги, местоимения.

Собирается в public/data/reference.json скриптом build_reference.py.
Раздел «Из уроков» сюда не входит: его сайт собирает сам из теории всех дней плана.

Блоки раздела:
  p(text)                    — абзац
  h(text)                    — подзаголовок
  grid(head, rows, fr=[...]) — таблица; fr — номера столбцов с французским (их можно нажать и послушать)
  ex(pairs)                  — примеры [фр, рус] с озвучкой
  note(text)                 — важное замечание
  line(items)                — ось времени [подпись, фр, рус]
  verbs(list)                — карточки спряжения: V(...)
"""


def p(text): return {"t": "p", "text": text}
def h(text): return {"t": "h", "text": text}
def grid(head, rows, fr=()): return {"t": "grid", "head": head, "rows": rows, "fr": list(fr)}
def ex(*pairs): return {"t": "ex", "items": [list(x) for x in pairs]}
def note(text): return {"t": "note", "text": text}
def line(*items): return {"t": "line", "items": [list(x) for x in items]}
def verbs(*items): return {"t": "verbs", "items": list(items)}


def V(inf, ru, pres, pc, imp, fut, note=""):
    """pres — шесть форм présent с местоимениями: je, tu, il, nous, vous, ils."""
    assert len(pres) == 6, inf
    return {"inf": inf, "ru": ru, "pres": pres, "pc": pc, "imp": imp, "fut": fut, "note": note}


SECTIONS = []


def section(id, title, lead, *blocks):
    SECTIONS.append({"id": id, "title": title, "lead": lead, "blocks": list(blocks)})


# ---------------------------------------------------------------- времена
section(
    "tenses", "Времена",
    "Главная таблица: какое время когда нужно и как его собрать. В русском одно прошедшее время, во французском их несколько — подсказка в столбце «По-русски».",
    line(
        ["раньше прошлого", "j’avais parlé", "plus-que-parfait"],
        ["прошлое: событие", "j’ai parlé", "passé composé"],
        ["прошлое: фон, привычка", "je parlais", "imparfait"],
        ["только что", "je viens de parler", "passé récent"],
        ["сейчас, обычно", "je parle", "présent"],
        ["скоро, по плану", "je vais parler", "futur proche"],
        ["потом, когда-нибудь", "je parlerai", "futur simple"],
    ),
    grid(
        ["Время", "Когда нужно", "Как собрать", "Пример", "По-русски"],
        [
            ["présent", "Сейчас; обычно, регулярно; факт. С обстоятельством — и ближайшее будущее: Demain, je travaille.",
             "основа + окончание группы: -er → -e, -es, -e, -ons, -ez, -ent",
             "Je travaille à Moscou. — Я работаю в Москве.", "настоящее: работаю"],
            ["passé composé", "Законченное событие в прошлом: что произошло, один раз, по шагам, с датой.",
             "avoir или être в présent + participe passé: j’ai parlé, je suis allée",
             "J’ai visité Paris en 2019. — Я побывала в Париже в 2019-м.", "прошедшее, обычно совершенный вид: сделала, побывала"],
            ["imparfait", "Фон и описание в прошлом (какой была погода, где жила); привычка («бывало»); действие в процессе.",
             "основа формы nous в présent (nous parlons → parl-) + -ais, -ais, -ait, -ions, -iez, -aient. Исключение: être → ét-",
             "Quand j’étais petite, j’habitais à Kazan. — Когда я была маленькой, я жила в Казани.", "прошедшее, обычно несовершенный вид: делала, жила"],
            ["plus-que-parfait", "Действие, которое случилось раньше другого прошлого.",
             "avoir или être в imparfait + participe passé: j’avais parlé, j’étais partie",
             "Quand je suis arrivée, le film avait déjà commencé. — Когда я пришла, фильм уже начался.", "прошедшее + «уже», «до того»"],
            ["passé récent", "Только что, минуту назад.",
             "venir в présent + de + инфинитив",
             "Je viens de manger. — Я только что поела.", "«только что» + прошедшее"],
            ["être en train de", "Прямо сейчас, в процессе (подчеркнуть, что занята).",
             "être в présent + en train de + инфинитив",
             "Je suis en train de lire. — Я как раз читаю.", "«сейчас как раз»"],
            ["futur proche", "Скоро, уже решено, по плану. В разговоре — самое частое будущее.",
             "aller в présent + инфинитив",
             "Je vais partir demain. — Я завтра уезжаю (собираюсь уехать).", "«собираюсь», будущее"],
            ["futur simple", "Будущее дальше и в общем: прогноз, обещание, «однажды».",
             "инфинитив + -ai, -as, -a, -ons, -ez, -ont (у -re без e: prendre → prendr-). Есть неправильные основы: ser-, aur-, ir-, fer-…",
             "Un jour, je parlerai bien français. — Однажды я буду хорошо говорить по-французски.", "будущее: буду говорить, скажу"],
            ["conditionnel présent", "Вежливая просьба, желание, мечта, совет — всё, что с «бы».",
             "основа futur simple + окончания imparfait: -ais, -ais, -ait, -ions, -iez, -aient",
             "J’aimerais vivre à Lyon. — Я бы хотела жить в Лионе.", "«бы»: хотела бы, сделала бы"],
            ["impératif", "Просьба, совет, приказ, инструкция.",
             "формы tu, nous, vous из présent без местоимения; у глаголов на -er в форме tu нет -s",
             "Écoute ! Allons-y ! Parlez plus lentement, s’il vous plaît. — Послушай! Пошли! Говорите медленнее, пожалуйста.", "повелительное: слушай, пойдём"],
            ["subjonctif présent · позже, B1", "После il faut que, je veux que, pour que, bien que.",
             "основа формы ils в présent (ils partent → part-) + -e, -es, -e, -ions, -iez, -ent",
             "Il faut que tu viennes. — Нужно, чтобы ты пришла.", "«чтобы» + прошедшее"],
        ],
        fr=[0, 3],
    ),
    note("Как выбрать между passé composé и imparfait: представь фильм. Imparfait — декорации и то, что идёт фоном (il pleuvait, j’étais fatiguée). Passé composé — то, что случилось в кадре (soudain, le téléphone a sonné)."),

    h("Как выбрать время: вопрос → время"),
    grid(
        ["Что хочу сказать", "Время", "Пример"],
        [
            ["что делаю сейчас или обычно", "présent", "Le matin, je bois du thé."],
            ["что случилось (законченное событие)", "passé composé", "Hier, j’ai vu un bon film."],
            ["как было, что было фоном, что делала обычно раньше", "imparfait", "Avant, je faisais du sport tous les jours."],
            ["что случилось ещё раньше другого прошлого", "plus-que-parfait", "J’ai perdu le livre que tu m’avais donné."],
            ["что сделала только что", "venir de + инфинитив", "Elle vient de partir."],
            ["что собираюсь сделать", "aller + инфинитив", "Ce soir, je vais regarder une série."],
            ["что будет потом, прогноз, обещание", "futur simple", "Demain, il fera froid."],
            ["вежливо попросить, помечтать, «бы»", "conditionnel", "Je voudrais un café, s’il vous plaît."],
            ["попросить, дать инструкцию", "impératif", "Ferme la fenêtre, s’il te plaît."],
        ],
        fr=[1, 2],
    ),

    h("Passé composé или imparfait"),
    grid(
        ["", "imparfait — фон", "passé composé — событие"],
        [
            ["что это", "описание, состояние, чувства, погода, возраст, привычка, процесс", "одно действие, законченное; цепочка действий; результат"],
            ["слова-подсказки", "avant, autrefois, d’habitude, souvent, toujours, tous les jours, le lundi, quand j’étais petite, pendant que",
             "hier, un jour, soudain, tout à coup, d’abord, puis, ensuite, enfin, en 2019, deux fois, ce jour-là"],
            ["пример", "Il faisait beau. J’avais vingt ans. Nous habitions à Sotchi.", "Un jour, j’ai rencontré Marc. Nous sommes allés au café."],
            ["вместе", "Je lisais…", "…quand le téléphone a sonné."],
        ],
        fr=[1, 2],
    ),
    ex(["Il pleuvait quand je suis sortie.", "Шёл дождь, когда я вышла."],
       ["Quand j’étais petite, je passais l’été chez ma grand-mère.", "Когда я была маленькой, я проводила лето у бабушки."],
       ["Ce jour-là, il faisait froid, et j’ai pris un taxi.", "В тот день было холодно, и я взяла такси."]),

    h("Один глагол во всех временах: parler (говорить)"),
    grid(
        ["présent", "passé composé", "imparfait", "futur simple", "conditionnel"],
        [
            ["je parle", "j’ai parlé", "je parlais", "je parlerai", "je parlerais"],
            ["tu parles", "tu as parlé", "tu parlais", "tu parleras", "tu parlerais"],
            ["il / elle parle", "il a parlé", "il parlait", "il parlera", "il parlerait"],
            ["nous parlons", "nous avons parlé", "nous parlions", "nous parlerons", "nous parlerions"],
            ["vous parlez", "vous avez parlé", "vous parliez", "vous parlerez", "vous parleriez"],
            ["ils / elles parlent", "ils ont parlé", "ils parlaient", "ils parleront", "ils parleraient"],
        ],
        fr=[0, 1, 2, 3, 4],
    ),
    p("Составные времена того же глагола: je vais parler (futur proche), je viens de parler (passé récent), j’avais parlé (plus-que-parfait), je suis en train de parler."),

    h("Глагол с être: aller (идти, ехать)"),
    grid(
        ["présent", "passé composé", "imparfait", "futur simple", "conditionnel"],
        [
            ["je vais", "je suis allé(e)", "j’allais", "j’irai", "j’irais"],
            ["tu vas", "tu es allé(e)", "tu allais", "tu iras", "tu irais"],
            ["il / elle va", "il est allé / elle est allée", "il allait", "il ira", "il irait"],
            ["nous allons", "nous sommes allé(e)s", "nous allions", "nous irons", "nous irions"],
            ["vous allez", "vous êtes allé(e)(s)", "vous alliez", "vous irez", "vous iriez"],
            ["ils / elles vont", "ils sont allés / elles sont allées", "ils allaient", "ils iront", "ils iraient"],
        ],
        fr=[0, 1, 2, 3, 4],
    ),
    note("С être причастие согласуется с подлежащим, как прилагательное: она — allée, они — allés, они (женщины) — allées. С avoir не согласуется: elle a parlé."),

    h("Passé composé: avoir или être"),
    p("Почти все глаголы — с avoir. С être — около 15 глаголов движения и изменения состояния и все возвратные глаголы."),
    grid(
        ["с être", "перевод", "причастие"],
        [
            ["aller / venir", "идти / приходить", "allé / venu"],
            ["arriver / partir", "прибывать / уезжать", "arrivé / parti"],
            ["entrer / sortir", "входить / выходить", "entré / sorti"],
            ["monter / descendre", "подниматься / спускаться", "monté / descendu"],
            ["naître / mourir", "родиться / умереть", "né / mort"],
            ["rester / tomber", "оставаться / падать", "resté / tombé"],
            ["rentrer / retourner", "возвращаться (домой) / возвращаться", "rentré / retourné"],
            ["revenir / devenir", "вернуться / стать", "revenu / devenu"],
            ["passer (par)", "заходить, проезжать (через)", "passé"],
            ["se lever, se promener…", "все возвратные", "je me suis levée"],
        ],
        fr=[0, 2],
    ),
    note("Если у monter, descendre, sortir, rentrer, passer есть прямое дополнение, они берут avoir: J’ai sorti le chien. — Я вывела собаку."),

    h("Participe passé"),
    grid(
        ["правило", "пример"],
        [
            ["-er → -é", "parler → parlé, aller → allé"],
            ["-ir 2-й группы → -i", "finir → fini, choisir → choisi"],
            ["-re → -u (многие)", "attendre → attendu, répondre → répondu, vendre → vendu"],
        ],
        fr=[1],
    ),
    grid(
        ["неправильные причастия", "", ""],
        [
            ["être → été", "avoir → eu", "faire → fait"],
            ["prendre → pris", "mettre → mis", "dire → dit"],
            ["écrire → écrit", "voir → vu", "venir → venu"],
            ["pouvoir → pu", "vouloir → voulu", "devoir → dû"],
            ["savoir → su", "lire → lu", "boire → bu"],
            ["connaître → connu", "croire → cru", "vivre → vécu"],
            ["naître → né", "mourir → mort", "ouvrir → ouvert"],
            ["recevoir → reçu", "courir → couru", "tenir → tenu"],
            ["partir → parti", "sortir → sorti", "dormir → dormi"],
        ],
        fr=[0, 1, 2],
    ),

    h("Futur simple и conditionnel: неправильные основы"),
    p("Окончания у всех глаголов одинаковые. Меняется только основа — её и нужно запомнить."),
    grid(
        ["глагол", "основа", "futur", "conditionnel"],
        [
            ["être", "ser-", "je serai", "je serais"],
            ["avoir", "aur-", "j’aurai", "j’aurais"],
            ["aller", "ir-", "j’irai", "j’irais"],
            ["faire", "fer-", "je ferai", "je ferais"],
            ["venir", "viendr-", "je viendrai", "je viendrais"],
            ["pouvoir", "pourr-", "je pourrai", "je pourrais"],
            ["vouloir", "voudr-", "je voudrai", "je voudrais"],
            ["devoir", "devr-", "je devrai", "je devrais"],
            ["savoir", "saur-", "je saurai", "je saurais"],
            ["voir", "verr-", "je verrai", "je verrais"],
            ["envoyer", "enverr-", "j’enverrai", "j’enverrais"],
            ["falloir", "faudr-", "il faudra", "il faudrait"],
            ["tenir", "tiendr-", "je tiendrai", "je tiendrais"],
            ["recevoir", "recevr-", "je recevrai", "je recevrais"],
        ],
        fr=[0, 1, 2, 3],
    ),

    h("Предложения с si (если)"),
    grid(
        ["если…", "то…", "пример"],
        [
            ["si + présent", "présent, futur или impératif", "S’il fait beau demain, nous irons à la plage. — Если завтра будет хорошая погода, мы пойдём на пляж."],
            ["si + imparfait", "conditionnel", "Si j’avais le temps, je voyagerais. — Если бы у меня было время, я бы путешествовала."],
        ],
        fr=[0, 1, 2],
    ),
    note("После si никогда не ставится futur и conditionnel: не «si il fera», а s’il fait. И si + il сливается в s’il, а si + elle — нет."),

    h("Impératif"),
    grid(
        ["глагол", "tu", "nous", "vous"],
        [
            ["parler", "parle", "parlons", "parlez"],
            ["finir", "finis", "finissons", "finissez"],
            ["aller", "va (но vas-y)", "allons", "allez"],
            ["faire", "fais", "faisons", "faites"],
            ["être", "sois", "soyons", "soyez"],
            ["avoir", "aie", "ayons", "ayez"],
            ["savoir", "sache", "sachons", "sachez"],
        ],
        fr=[0, 1, 2, 3],
    ),
    p("С отрицанием: Ne parle pas ! С местоимением: в утверждении местоимение после глагола через дефис (Regarde-moi ! Prends-le !), в отрицании — перед глаголом (Ne le prends pas !)."),
)

# ---------------------------------------------------------------- построение предложения
section(
    "sentence", "Как строить предложение",
    "Порядок слов, отрицание, вопросы и место местоимений. Это скелет, на который надеваются времена.",
    h("Порядок слов"),
    grid(
        ["кто", "(ne)", "местоимение", "спрягаемый глагол", "(pas)", "остальное: причастие, инфинитив, что, где, когда"],
        [
            ["Je", "", "", "regarde", "", "un film ce soir."],
            ["Je", "ne", "le", "vois", "pas", "souvent."],
            ["Elle", "", "m’", "a", "", "donné un livre hier."],
            ["Nous", "n’", "y", "sommes", "pas", "allés l’été dernier."],
            ["Je", "ne", "", "vais", "pas", "lui écrire."],
        ],
        fr=[0, 1, 2, 3, 4, 5],
    ),
    p("Подлежащее во французском есть всегда: не «работаю», а je travaille. Для погоды и безличных фраз — il: Il pleut. Il faut partir."),

    h("Отрицание"),
    p("Ne и вторая часть обнимают спрягаемый глагол. В составных временах спрягается вспомогательный глагол, поэтому отрицание стоит вокруг него. Инфинитив остаётся снаружи."),
    grid(
        ["", "утверждение", "отрицание", "вопрос"],
        [
            ["présent", "Je parle.", "Je ne parle pas.", "Tu parles ? / Est-ce que tu parles ? / Parles-tu ?"],
            ["passé composé", "J’ai parlé.", "Je n’ai pas parlé.", "Tu as parlé ? / Est-ce que tu as parlé ? / As-tu parlé ?"],
            ["imparfait", "Je parlais.", "Je ne parlais pas.", "Tu parlais ? / Est-ce que tu parlais ?"],
            ["futur proche", "Je vais parler.", "Je ne vais pas parler.", "Tu vas parler ? / Vas-tu parler ?"],
            ["futur simple", "Je parlerai.", "Je ne parlerai pas.", "Tu parleras ? / Est-ce que tu parleras ?"],
            ["conditionnel", "Je parlerais.", "Je ne parlerais pas.", "Tu parlerais ? / Parlerais-tu ?"],
            ["возвратный", "Je me lève.", "Je ne me lève pas.", "Tu te lèves ? / Te lèves-tu ?"],
        ],
        fr=[1, 2, 3],
    ),
    grid(
        ["отрицание", "значение", "пример"],
        [
            ["ne … pas", "не", "Je ne travaille pas le dimanche."],
            ["ne … jamais", "никогда не", "Je ne suis jamais allée en Italie."],
            ["ne … plus", "больше не", "Il n’habite plus ici."],
            ["ne … rien", "ничего не", "Je n’ai rien compris."],
            ["ne … personne", "никого не (personne — после причастия)", "Je n’ai vu personne."],
            ["ne … pas encore", "ещё не", "Elle n’est pas encore arrivée."],
            ["ne … que", "только", "Je n’ai que dix euros."],
        ],
        fr=[0, 2],
    ),
    note("После отрицания un, une, des, du, de la превращаются в de (d’): J’ai une voiture → Je n’ai pas de voiture. Кроме глагола être: Ce n’est pas un problème. В разговоре ne часто проглатывают: Je sais pas."),

    h("Вопрос: три способа"),
    grid(
        ["способ", "где звучит", "пример"],
        [
            ["интонация", "разговор", "Tu viens ce soir ?"],
            ["est-ce que", "везде, нейтрально", "Est-ce que tu viens ce soir ?"],
            ["инверсия", "письмо, вежливо", "Viens-tu ce soir ?"],
        ],
        fr=[2],
    ),
    p("В инверсии между гласными вставляется -t-: Parle-t-il français ? A-t-elle fini ? Если подлежащее — существительное, его оставляют впереди и добавляют местоимение: Marie parle-t-elle anglais ?"),
    grid(
        ["слово", "значение", "пример"],
        [
            ["où", "где, куда", "Où est-ce que tu habites ? / Tu habites où ?"],
            ["d’où", "откуда", "D’où viens-tu ?"],
            ["quand", "когда", "Quand est-ce que tu pars ?"],
            ["comment", "как", "Comment tu t’appelles ?"],
            ["pourquoi — parce que", "почему — потому что", "Pourquoi tu ris ? Parce que c’est drôle."],
            ["combien (de)", "сколько", "Combien de frères as-tu ?"],
            ["qui", "кто", "Qui est-ce ?"],
            ["que / qu’est-ce que", "что", "Qu’est-ce que tu fais ? / Que fais-tu ?"],
            ["quoi", "что (в конце, разговорно)", "Tu fais quoi ?"],
            ["quel, quelle, quels, quelles", "какой", "Quelle heure est-il ? Quel âge as-tu ?"],
        ],
        fr=[0, 2],
    ),

    h("Где стоят местоимения"),
    grid(
        ["случай", "место", "пример"],
        [
            ["один глагол", "перед глаголом", "Je le vois. Je lui parle."],
            ["составное время", "перед вспомогательным", "Je l’ai vu. Je ne l’ai pas vu."],
            ["глагол + инфинитив", "перед инфинитивом", "Je vais le faire. Je veux lui écrire."],
            ["impératif, утверждение", "после глагола через дефис", "Fais-le ! Donne-moi ça !"],
            ["impératif, отрицание", "перед глаголом", "Ne le fais pas !"],
        ],
        fr=[2],
    ),
    note("Если le, la, les стоят перед avoir в passé composé, причастие согласуется с ними: Cette photo ? Je l’ai prise à Paris."),
)

# ---------------------------------------------------------------- глаголы
section(
    "verbs", "Глаголы",
    "Три группы глаголов, правильные окончания, капризы орфографии и спряжение главных неправильных глаголов.",
    h("Три группы"),
    grid(
        ["", "1-я группа: -er", "2-я группа: -ir (-issons)", "3-я группа: -re"],
        [
            ["пример", "parler — говорить", "finir — заканчивать", "attendre — ждать"],
            ["je", "je parle", "je finis", "j’attends"],
            ["tu", "tu parles", "tu finis", "tu attends"],
            ["il / elle", "il parle", "il finit", "il attend"],
            ["nous", "nous parlons", "nous finissons", "nous attendons"],
            ["vous", "vous parlez", "vous finissez", "vous attendez"],
            ["ils / elles", "ils parlent", "ils finissent", "ils attendent"],
            ["participe", "parlé", "fini", "attendu"],
            ["так же", "почти все на -er (кроме aller)", "choisir, réussir, grandir, réfléchir", "répondre, entendre, perdre, vendre, descendre"],
        ],
        fr=[1, 2, 3],
    ),
    note("Je parle, tu parles, il parle, ils parlent звучат одинаково: окончания -e, -es, -ent не читаются. Слышно только nous и vous."),

    h("Орфографические капризы -er"),
    grid(
        ["глагол", "что меняется", "формы"],
        [
            ["manger, voyager", "перед -o пишется -ge-", "nous mangeons, je mangeais"],
            ["commencer", "перед -o и -a пишется ç", "nous commençons, je commençais"],
            ["acheter, se lever", "e → è, когда окончание не слышно", "j’achète, nous achetons; je me lève"],
            ["appeler, s’appeler", "удвоение l", "je m’appelle, nous nous appelons"],
            ["préférer, répéter", "é → è в тех же формах", "je préfère, nous préférons"],
            ["payer, envoyer", "y → i", "je paie, j’envoie, nous envoyons"],
        ],
        fr=[0, 2],
    ),

    h("Возвратные глаголы"),
    grid(
        ["présent", "passé composé"],
        [
            ["je me lève", "je me suis levé(e)"],
            ["tu te lèves", "tu t’es levé(e)"],
            ["il / elle se lève", "il s’est levé / elle s’est levée"],
            ["nous nous levons", "nous nous sommes levé(e)s"],
            ["vous vous levez", "vous vous êtes levé(e)(s)"],
            ["ils / elles se lèvent", "ils se sont levés / elles se sont levées"],
        ],
        fr=[0, 1],
    ),
    p("Так же: se réveiller, s’habiller, se laver, se coucher, se promener, s’appeler, s’amuser, se reposer, se dépêcher. Отрицание: je ne me lève pas, je ne me suis pas levée."),

    h("Неправильные глаголы"),
    p("Présent целиком, а для остальных времён — форма je: по ней собираются все лица."),
    verbs(
        V("être", "быть", ["je suis", "tu es", "il est", "nous sommes", "vous êtes", "ils sont"], "j’ai été", "j’étais", "je serai"),
        V("avoir", "иметь", ["j’ai", "tu as", "il a", "nous avons", "vous avez", "ils ont"], "j’ai eu", "j’avais", "j’aurai"),
        V("aller", "идти, ехать", ["je vais", "tu vas", "il va", "nous allons", "vous allez", "ils vont"], "je suis allé(e)", "j’allais", "j’irai"),
        V("faire", "делать", ["je fais", "tu fais", "il fait", "nous faisons", "vous faites", "ils font"], "j’ai fait", "je faisais", "je ferai"),
        V("venir", "приходить", ["je viens", "tu viens", "il vient", "nous venons", "vous venez", "ils viennent"], "je suis venu(e)", "je venais", "je viendrai",
          "так же revenir, devenir (с être) и tenir (с avoir: j’ai tenu)"),
        V("prendre", "брать", ["je prends", "tu prends", "il prend", "nous prenons", "vous prenez", "ils prennent"], "j’ai pris", "je prenais", "je prendrai",
          "так же apprendre (учить) и comprendre (понимать)"),
        V("pouvoir", "мочь", ["je peux", "tu peux", "il peut", "nous pouvons", "vous pouvez", "ils peuvent"], "j’ai pu", "je pouvais", "je pourrai"),
        V("vouloir", "хотеть", ["je veux", "tu veux", "il veut", "nous voulons", "vous voulez", "ils veulent"], "j’ai voulu", "je voulais", "je voudrai",
          "вежливо: je voudrais — я бы хотела"),
        V("devoir", "быть должной", ["je dois", "tu dois", "il doit", "nous devons", "vous devez", "ils doivent"], "j’ai dû", "je devais", "je devrai",
          "совет: tu devrais — тебе бы стоило"),
        V("savoir", "знать, уметь", ["je sais", "tu sais", "il sait", "nous savons", "vous savez", "ils savent"], "j’ai su", "je savais", "je saurai",
          "savoir + инфинитив — уметь: Je sais nager."),
        V("connaître", "знать (кого-то, место)", ["je connais", "tu connais", "il connaît", "nous connaissons", "vous connaissez", "ils connaissent"], "j’ai connu", "je connaissais", "je connaîtrai",
          "connaître — человека или место, savoir — факт: Je connais Marie. Je sais où elle habite."),
        V("voir", "видеть", ["je vois", "tu vois", "il voit", "nous voyons", "vous voyez", "ils voient"], "j’ai vu", "je voyais", "je verrai"),
        V("dire", "сказать", ["je dis", "tu dis", "il dit", "nous disons", "vous dites", "ils disent"], "j’ai dit", "je disais", "je dirai"),
        V("mettre", "класть, надевать", ["je mets", "tu mets", "il met", "nous mettons", "vous mettez", "ils mettent"], "j’ai mis", "je mettais", "je mettrai"),
        V("partir", "уезжать", ["je pars", "tu pars", "il part", "nous partons", "vous partez", "ils partent"], "je suis parti(e)", "je partais", "je partirai",
          "так же dormir (je dors, nous dormons; j’ai dormi)"),
        V("sortir", "выходить", ["je sors", "tu sors", "il sort", "nous sortons", "vous sortez", "ils sortent"], "je suis sorti(e)", "je sortais", "je sortirai"),
        V("boire", "пить", ["je bois", "tu bois", "il boit", "nous buvons", "vous buvez", "ils boivent"], "j’ai bu", "je buvais", "je boirai"),
        V("écrire", "писать", ["j’écris", "tu écris", "il écrit", "nous écrivons", "vous écrivez", "ils écrivent"], "j’ai écrit", "j’écrivais", "j’écrirai"),
        V("lire", "читать", ["je lis", "tu lis", "il lit", "nous lisons", "vous lisez", "ils lisent"], "j’ai lu", "je lisais", "je lirai"),
        V("vivre", "жить", ["je vis", "tu vis", "il vit", "nous vivons", "vous vivez", "ils vivent"], "j’ai vécu", "je vivais", "je vivrai",
          "habiter — жить где-то (адрес), vivre — жить вообще: J’habite à Moscou. Je vis seule."),
        V("croire", "верить, думать", ["je crois", "tu crois", "il croit", "nous croyons", "vous croyez", "ils croient"], "j’ai cru", "je croyais", "je croirai"),
        V("recevoir", "получать", ["je reçois", "tu reçois", "il reçoit", "nous recevons", "vous recevez", "ils reçoivent"], "j’ai reçu", "je recevais", "je recevrai"),
        V("ouvrir", "открывать", ["j’ouvre", "tu ouvres", "il ouvre", "nous ouvrons", "vous ouvrez", "ils ouvrent"], "j’ai ouvert", "j’ouvrais", "j’ouvrirai",
          "в présent спрягается как глагол на -er; так же offrir, découvrir"),
        V("se lever", "вставать", ["je me lève", "tu te lèves", "il se lève", "nous nous levons", "vous vous levez", "ils se lèvent"], "je me suis levé(e)", "je me levais", "je me lèverai"),
    ),
    p("Falloir — только с il: il faut (нужно), il a fallu, il fallait, il faudra. Pleuvoir — тоже: il pleut, il a plu, il pleuvait, il pleuvra."),

    h("Глагол + инфинитив"),
    grid(
        ["конструкция", "примеры глаголов", "пример"],
        [
            ["глагол + инфинитив", "aimer, adorer, préférer, détester, vouloir, pouvoir, devoir, savoir, aller, espérer", "J’aime lire. Je dois partir."],
            ["глагол + à + инфинитив", "commencer à, apprendre à, réussir à, aider à, continuer à", "J’apprends à nager."],
            ["глагол + de + инфинитив", "essayer de, finir de, arrêter de, oublier de, décider de, avoir besoin de, avoir envie de, venir de", "J’ai envie de dormir. J’ai oublié de fermer la porte."],
        ],
        fr=[1, 2],
    ),

    h("Выражения с avoir и faire"),
    grid(
        ["avoir", "перевод", "faire", "перевод"],
        [
            ["avoir faim / soif", "хотеть есть / пить", "il fait beau / froid / chaud", "погода хорошая / холодно / жарко"],
            ["avoir chaud / froid", "мне жарко / холодно", "faire du sport", "заниматься спортом"],
            ["avoir peur (de)", "бояться", "faire la cuisine", "готовить"],
            ["avoir raison / tort", "быть правой / неправой", "faire les courses", "ходить за покупками"],
            ["avoir sommeil", "хотеть спать", "faire le ménage", "убираться"],
            ["avoir besoin de", "нуждаться", "faire une promenade", "гулять"],
            ["avoir envie de", "хотеть (захотелось)", "faire la queue", "стоять в очереди"],
            ["avoir 30 ans", "мне 30 лет", "faire attention", "быть внимательной"],
            ["avoir mal à la tête", "болит голова", "faire la fête", "праздновать, тусоваться"],
        ],
        fr=[0, 2],
    ),
)

# ---------------------------------------------------------------- предлоги
section(
    "prepositions", "Предлоги места и времени",
    "Где, куда, откуда и когда. Плюс слияние à и de с артиклем: без него предлоги не работают.",
    h("Слияние с артиклем"),
    grid(
        ["", "+ le", "+ la", "+ l’", "+ les"],
        [
            ["à", "au (au cinéma)", "à la (à la gare)", "à l’ (à l’école)", "aux (aux toilettes)"],
            ["de", "du (près du parc)", "de la (près de la gare)", "de l’ (près de l’école)", "des (près des magasins)"],
        ],
        fr=[0, 1, 2, 3, 4],
    ),

    h("Города и страны"),
    grid(
        ["что", "где / куда", "откуда", "пример"],
        [
            ["город", "à", "de / d’", "J’habite à Paris. Je viens de Moscou."],
            ["страна женского рода (обычно на -e)", "en", "de / d’", "Je vais en France. Elle vient d’Italie."],
            ["страна на гласную", "en", "d’", "en Iran, d’Iran"],
            ["страна мужского рода", "au", "du", "Il habite au Japon. Je viens du Canada."],
            ["страна во множественном числе", "aux", "des", "aux États-Unis, des Pays-Bas"],
        ],
        fr=[1, 2, 3],
    ),
    note("Le Mexique, le Cambodge, le Mozambique — мужского рода, хотя на -e: au Mexique."),

    h("Где: положение в пространстве"),
    grid(
        ["предлог", "значение", "пример"],
        [
            ["dans", "в (внутри)", "dans la boîte, dans le métro, dans la rue (на улице)"],
            ["sur", "на", "sur la table, sur la place"],
            ["sous", "под", "sous le lit"],
            ["devant", "перед", "devant la maison"],
            ["derrière", "за, позади", "derrière la porte"],
            ["entre", "между", "entre la poste et la banque"],
            ["à côté de", "рядом с", "à côté du cinéma"],
            ["près de", "близко от", "près de la gare"],
            ["loin de", "далеко от", "loin du centre"],
            ["en face de", "напротив", "en face de l’hôtel"],
            ["au milieu de", "посреди", "au milieu de la place"],
            ["au bout de", "в конце", "au bout de la rue"],
            ["autour de", "вокруг", "autour du lac"],
            ["à gauche de / à droite de", "слева от / справа от", "à droite de la fenêtre"],
            ["au-dessus de / au-dessous de", "над / под (уровнем)", "au-dessus du lit"],
            ["chez", "у, к (кому-то); в заведение по профессии", "chez moi, chez Marie, chez le médecin"],
        ],
        fr=[0, 2],
    ),
    grid(
        ["куда и как", "пример"],
        [
            ["à + место", "à la maison, au bureau, à la gare, au marché, à la plage"],
            ["à la campagne / à la montagne / à la mer", "за городом / в горах / на море"],
            ["en + транспорт (внутри)", "en voiture, en train, en avion, en bus, en métro, en taxi"],
            ["à + транспорт (сверху) и пешком", "à pied, à vélo, à cheval"],
        ],
        fr=[0, 1],
    ),

    h("Когда: предлоги времени"),
    grid(
        ["предлог", "значение", "пример"],
        [
            ["à", "в (час)", "à 8 heures, à midi, à minuit"],
            ["en", "в (месяц, год, время года)", "en mars, en 2026, en été, en automne, en hiver (но: au printemps)"],
            ["le", "дата; день недели с le — каждый", "le 9 novembre; le lundi (по понедельникам), lundi (в этот понедельник)"],
            ["vers", "около", "vers 20 heures"],
            ["de … à / du … au", "с … до", "de 9 h à 18 h, du lundi au vendredi"],
            ["jusqu’à", "до", "jusqu’à demain, jusqu’à 5 heures"],
            ["à partir de", "начиная с", "à partir de lundi"],
            ["avant / après", "до / после", "avant le dîner, après le travail; avant de partir"],
            ["dans", "через (в будущем)", "dans deux jours, dans une heure"],
            ["il y a", "назад", "il y a trois ans"],
            ["depuis", "с (какого-то момента), уже (и продолжается)", "J’apprends le français depuis octobre / depuis deux mois."],
            ["pendant", "в течение (законченный отрезок)", "J’ai dormi pendant huit heures."],
            ["en", "за (сколько времени ушло)", "J’ai lu le livre en deux jours."],
            ["pour", "на (запланированный срок)", "Je pars pour une semaine."],
        ],
        fr=[0, 2],
    ),
    note("Depuis + présent, хотя по-русски часто прошедшее: Je travaille ici depuis 2020. — Я работаю здесь с 2020 года. Il y a — точка в прошлом с passé composé: Je suis arrivée il y a deux heures."),
    grid(
        ["вчера и завтра", ""],
        [
            ["avant-hier · hier · aujourd’hui · demain · après-demain", "позавчера · вчера · сегодня · завтра · послезавтра"],
            ["ce matin · cet après-midi · ce soir · cette nuit", "сегодня утром · днём · вечером · ночью"],
            ["la semaine dernière · la semaine prochaine", "на прошлой неделе · на следующей неделе"],
            ["l’année dernière · l’année prochaine", "в прошлом году · в следующем году"],
            ["tout à l’heure · bientôt · tout de suite", "недавно или скоро · скоро · сразу"],
        ],
        fr=[0],
    ),
)

# ---------------------------------------------------------------- местоимения и артикли
section(
    "pronouns", "Местоимения и артикли",
    "Кто, кого, кому, чей — и какой артикль поставить перед существительным.",
    h("Личные местоимения"),
    grid(
        ["подлежащее", "ударное", "прямое (кого? что?)", "косвенное (кому?)", "возвратное"],
        [
            ["je", "moi", "me (m’)", "me (m’)", "me"],
            ["tu", "toi", "te (t’)", "te (t’)", "te"],
            ["il / elle / on", "lui / elle / soi", "le / la (l’)", "lui", "se"],
            ["nous", "nous", "nous", "nous", "nous"],
            ["vous", "vous", "vous", "vous", "vous"],
            ["ils / elles", "eux / elles", "les", "leur", "se"],
        ],
        fr=[0, 1, 2, 3, 4],
    ),
    ex(["Moi, j’aime le thé. Et toi ?", "Я люблю чай. А ты?"],
       ["Tu viens chez moi ?", "Придёшь ко мне?"],
       ["Ce film ? Je le regarde ce soir.", "Этот фильм? Я его смотрю сегодня вечером."],
       ["Je téléphone à Marie. → Je lui téléphone.", "Я звоню Мари. → Я ей звоню."]),
    p("Ударные — после предлога и для выделения: avec moi, pour eux, C’est lui. On — «мы» в разговоре и «люди вообще»: On va au cinéma ? Глагол после on — в форме il: on va, on fait."),
    p("Косвенное lui / leur заменяет à + человек: parler à, téléphoner à, donner à, dire à, écrire à, demander à, répondre à."),

    h("Y и en"),
    grid(
        ["", "что заменяет", "пример"],
        [
            ["y", "à + место или вещь; «там, туда»", "Tu vas à Paris ? Oui, j’y vais. Je pense à mon examen → J’y pense."],
            ["en", "de + вещь; количество; «оттуда»", "Tu veux du café ? Oui, j’en veux. Tu as des frères ? J’en ai deux."],
        ],
        fr=[0, 2],
    ),
    p("Порядок, если местоимений несколько: me, te, se, nous, vous → le, la, les → lui, leur → y → en. Je te le donne. Je le lui donne. Il y en a."),

    h("Притяжательные"),
    grid(
        ["чей", "м. р.", "ж. р.", "мн. ч."],
        [
            ["мой", "mon", "ma", "mes"],
            ["твой", "ton", "ta", "tes"],
            ["его / её", "son", "sa", "ses"],
            ["наш", "notre", "notre", "nos"],
            ["ваш", "votre", "votre", "vos"],
            ["их", "leur", "leur", "leurs"],
        ],
        fr=[1, 2, 3],
    ),
    note("Son / sa зависит от рода вещи, а не владельца: sa maison — и «его дом», и «её дом». Перед гласной ma, ta, sa → mon, ton, son: mon amie."),

    h("Артикли"),
    grid(
        ["артикль", "формы", "когда", "пример"],
        [
            ["определённый", "le, la, l’, les", "конкретное, уже известное; вкусы и всё вообще", "J’aime le café. Le livre est sur la table."],
            ["неопределённый", "un, une, des", "один какой-то, ещё не известный; считаемое", "Je prends un café. Il y a des enfants."],
            ["частичный", "du, de la, de l’, des", "немного чего-то неисчисляемого", "Je bois du café. Je mange de la soupe."],
            ["после отрицания и количества", "de, d’", "pas de, beaucoup de, un peu de, trop de, combien de", "Je n’ai pas de chat. Beaucoup de gens."],
        ],
        fr=[1, 3],
    ),
    grid(
        ["указательное «этот»", "", ""],
        [
            ["ce", "м. р.", "ce livre"],
            ["cet", "м. р. перед гласной", "cet homme, cet ami"],
            ["cette", "ж. р.", "cette ville"],
            ["ces", "мн. ч.", "ces gens"],
        ],
        fr=[0, 2],
    ),
)
