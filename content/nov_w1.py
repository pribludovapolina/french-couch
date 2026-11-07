# -*- coding: utf-8 -*-
"""Ноябрь, неделя 1: возвращение (07.11) и юнит 1 « Souvenirs » (09–14.11).

План и методика: french-plans/noyabr-2026-plan.md, полный образец урока 1.1 — noyabr-2026-urok-1-1.md.
Тексты Ирины, Марты и диалог «Au bureau» написаны для уроков. Ссылки проверены в браузере 07–08.11.2026.

Идентификаторы — ключи прогресса, менять и вставлять в середину нельзя:
  разгон s1…, документ d0…, охота на формы hunt, наблюдение o1…, упражнения e1…, спринт t1…,
  микрозадания текста недели m1…, чтение R-n.
"""
from h import C, L, G, J, O, D, T, th, topic

YT = "https://www.youtube.com/watch?v="
SIM = "https://apprendre.tv5monde.com/fr/tcf/simulation-du-tcf"
TCF17 = "https://apprendre.tv5monde.com/fr/tcf/test-dentrainement-au-tcf?tcf_lot_id=70"
COURSE = "https://apprendre.tv5monde.com/fr/exercices/la-grammaire-en-a2/le-passe-compose-et-limparfait"
PETIT_PRINCE = "https://www.ebooksgratuits.com/pdf/st_exupery_le_petit_prince.pdf"

# Регулярные выражения для «кусков текста» проверяются по ответу в нижнем регистре с прямым апострофом.
LETTERS = "a-zàâçéèêëîïôûùüÿœ"
PC = r"\b(ai|as|a|avons|avez|ont|suis|es|est|sommes|êtes|sont) [" + LETTERS + r"]+"


def VF(q, a):
    """Vrai / faux / on ne sait pas: a — 0, 1 или 2. Варианты не перемешиваются."""
    return {"type": "choice", "q": q, "o": ["vrai", "faux", "on ne sait pas"], "a": a, "fixed": True}


def P(part, q, ph, re, want, pre="", words=(1, 8)):
    """Кусок текста недели: короткий ответ про себя. Проверяется только целевая форма (re), текст уходит в каркас."""
    return {"type": "piece", "part": part, "q": q, "pre": pre, "ph": ph, "re": re, "want": want, "words": list(words)}


def Q(q, o, a=0):
    """Вопрос TCF на 4 варианта (первый — верный, на сайте перемешиваются)."""
    return {"type": "choice", "q": q, "o": o, "a": a}


def video(id, title, src, dur):
    return {"url": YT + id, "title": title, "src": src, "dur": dur}


UNIT = {
    "id": 1, "name": "Souvenirs",
    "situation": "Рассказать, как было: жизнь до переезда и первый день в новом городе.",
    "can": [
        "рассказать, как жила и что делала до переезда",
        "рассказать историю первого дня в новом городе: фон и события",
        "понять уличное интервью о прошлом опыте",
        "собрать блог-пост на 120–150 слов — письменное задание 2 формата TCF",
    ],
    "task": "Vous venez de vous installer en France. Sur votre blog, vous racontez votre vie d’avant et votre premier jour dans votre nouvelle ville. (120–150 mots)",
    "min": 120, "max": 150,
    "parts": [
        {"n": 1, "fr": "Avant", "ru": "где жила, кем работала"},
        {"n": 2, "fr": "Ma vie là-bas", "ru": "привычки, обычный день"},
        {"n": 3, "fr": "Le départ", "ru": "каким был день отъезда (фон)"},
        {"n": 4, "fr": "Le premier jour", "ru": "что случилось (события)"},
        {"n": 5, "fr": "Aujourd’hui", "ru": "что изменилось"},
    ],
}

TV5 = "Курс TV5MONDE « La grammaire en A2 », модуль « Le passé composé et l’imparfait ». "
SAY_TASKS = "Проверка — по субтитрам: ключей к этим вопросам на сайте нет, вопросы открытые."

DAYS = []

# ================================================================ 07.11 · возвращение
DAYS.append({
    "date": "2026-11-07", "type": "контроль", "unit": 0, "lesson": "0", "minutes": 120,
    "topic": "Возвращение: симуляция TCF #2",
    "intro": "Долг 30 октября. Сегодня только симуляция и карточки, новой грамматики нет. Учебная часть ноября начинается в понедельник 9-го.",
    "steps": [
        {"kind": "review", "title": "Карточки", "min": 15},
        {"kind": "tcf", "title": "Симуляция TCF #2 и разбор", "min": 105, "url": SIM,
         "label": "Открыть симулятор TCF", "sub": "TV5MONDE · Test en conditions réelles · 90 мин",
         "task": "90 минут в реальных условиях: без словаря и без пауз. Потом 15 минут разбора: запиши результат, сравни с 1 октября, "
                 "а слова и конструкции, на которых ошиблась, добавь в карточки ниже.",
         "compare": True, "catch": "Слова и фразы, на которых ошиблась"},
    ],
})

DAYS.append({"date": "2026-11-08", "type": "выходной", "minutes": 0, "steps": []})

# ================================================================ 09.11 · урок 1.1 · imparfait
LESSON = [
    {"kind": "review", "title": "Разгон: карточки и спираль", "min": 15},
    {"kind": "doc", "title": "Документ дня", "min": 40},
    {"kind": "observe", "title": "Наблюдение и правило", "min": 10},
    {"kind": "theory", "title": "Теория", "min": 5},
    {"kind": "exercises", "title": "Упражнения", "min": 30},
    {"kind": "sprint", "title": "TCF-спринт", "min": 15},
    {"kind": "course", "title": "Онлайн-курс TV5", "min": 30},
    {"kind": "listening", "title": "Второе аудио", "min": 35},
    {"kind": "wtext", "title": "Текст недели", "min": 15},
    {"kind": "wrap", "title": "Запас и итог дня", "min": 15},
]


def lesson_steps(**over):
    out = []
    for s in LESSON:
        s = dict(s)
        s.update(over.get(s["kind"], {}))
        out.append(s)
    return out


def tf(src, *a):
    return {"type": "transform", "q": "Поставь в passé composé (начни с « Hier, »)", "src": src, "a": list(a)}


DAYS.append({
    "date": "2026-11-09", "type": "учебный", "unit": 1, "lesson": "1.1", "minutes": 210, "unitStart": True,
    "topic": "Imparfait: как было раньше",
    "steps": lesson_steps(listening={"items": [dict(video("If_iJ4geb8A", "What Was Your First Job as a Student? | Easy French 235", "Easy French", "9:48"),
        task="1. Первый просмотр с французскими субтитрами: для 4 человек запиши, кем они работали (1–3 слова на каждого). "
             "2. Второй просмотр: выпиши 3 фразы с imparfait и 1 с passé composé — это корпус для завтрашнего урока. "
             "3. По желанию: повтори вслух одну выписанную фразу. " + SAY_TASKS)]},
        course={"url": COURSE, "stage": "Étapes 01 и 02",
                "task": TV5 + "Сегодня введение и « L’expression d’un événement au passé composé » (12 упражнений): это повтор октября перед завтрашней темой."}),
    "warmup": [
        tf("Je prends le métro.", "Hier, j’ai pris le métro.", "J’ai pris le métro."),
        tf("Nous allons à la gare.", "Hier, nous sommes allés à la gare.", "Hier, nous sommes allées à la gare.", "Nous sommes allés à la gare.", "Nous sommes allées à la gare."),
        tf("Elle se lève tôt.", "Hier, elle s’est levée tôt.", "Elle s’est levée tôt."),
        tf("Tu fais les courses ?", "Hier, tu as fait les courses ?", "Tu as fait les courses ?"),
        tf("Je ne vois pas le film.", "Hier, je n’ai pas vu le film.", "Je n’ai pas vu le film."),
    ],
    "doc": {
        "title": "Ma vie d’avant",
        "who": "Блог Ирины, разработчицы, которая год назад переехала в Лион. Текст написан для урока и нарочно почти целиком в imparfait.",
        "pre": C("Заголовок: « Ma vie d’avant ». О чём, скорее всего, будет текст?", ["о прошлом", "о планах", "жалоба", "рецепт"]),
        "listen": "Шаг 1. Послушай текст без букв (кнопка «Слушать») и ответь на вопросы TCF. Шаг 2. Открой текст, послушай ещё раз и проверь себя.",
        "text": "Il y a un an, je vivais encore à Saint-Pétersbourg. J’avais un petit appartement près du métro et je travaillais dans une start-up. "
                "Tous les matins, je prenais un café en bas de chez moi, puis je marchais jusqu’au bureau. Le soir, j’étais souvent fatiguée, mais j’aimais ma vie. "
                "Le week-end, on allait au bord de la Neva avec des amis : on parlait pendant des heures et on mangeait des pirojki. "
                "En hiver, il faisait très froid, il neigeait presque tous les jours et la nuit tombait à quatre heures. "
                "Je ne parlais pas français, je ne connaissais personne en France… et je ne savais pas encore que tout allait changer.",
        "ru": "Год назад я ещё жила в Петербурге. У меня была маленькая квартира у метро, и я работала в стартапе. Каждое утро я пила кофе внизу у дома, "
              "потом шла пешком до офиса. Вечером я часто уставала, но мне нравилась моя жизнь. По выходным мы с друзьями ходили на набережную Невы: "
              "болтали часами и ели пирожки. Зимой было очень холодно, снег шёл почти каждый день, а темнело в четыре. "
              "Я не говорила по-французски, никого не знала во Франции… и ещё не знала, что всё изменится.",
        "quiz": [
            Q("Où vivait Irina il y a un an ?", ["à Saint-Pétersbourg", "à Lyon", "à Moscou", "à Kazan"]),
            Q("Que faisait-elle tous les matins ?", ["elle prenait un café en bas de chez elle", "elle courait au bord de la Neva", "elle prenait le bus", "elle travaillait à la maison"]),
            Q("Le texte parle surtout…", ["d’habitudes passées", "d’un voyage", "de projets", "d’un problème au travail"]),
            VF("Elle était souvent fatiguée le soir.", 0),
            VF("Elle parlait déjà un peu français.", 1),
            VF("Ses amis travaillaient aussi dans la start-up.", 2),
        ],
        "hunt": {"q": "Охота на формы: нажми на все глаголы, которые описывают прошлое (imparfait). Их 17, одна форма встречается дважды.",
                 "forms": ["vivais", "avais", "travaillais", "prenais", "marchais", "étais", "aimais", "allait", "parlait", "mangeait",
                           "faisait", "neigeait", "tombait", "parlais", "connaissais", "savais"]},
        "chunks": [["il y a un an", "год назад"], ["en bas de chez moi", "внизу у моего дома"], ["j’étais souvent fatiguée", "я часто уставала"],
                   ["au bord de la Neva", "на берегу Невы"], ["pendant des heures", "часами"], ["presque tous les jours", "почти каждый день"],
                   ["la nuit tombait", "темнело (наступала ночь)"], ["je ne connaissais personne", "я никого не знала"]],
    },
    "observe": {
        "intro": "Формы из текста Ирины, разложенные по лицам:",
        "table": [["je", "vivais, avais, travaillais, prenais, marchais, étais, aimais, parlais, connaissais, savais"],
                  ["il / on", "allait, parlait, mangeait, faisait, neigeait, tombait"]],
        "qs": [G("je viv___", "Какое окончание у je?", "ais"), G("on mange___", "Какое окончание у il / on?", "ait")],
        "rule": "Сравни: nous prenons → je prenais, nous faisons → il faisait. Откуда берётся основа?",
        "model": "Основа — это форма nous в présent без -ons: nous pren-ons → pren-, nous fais-ons → fais-. К ней добавляются окончания -ais, -ais, -ait, -ions, -iez, -aient.",
    },
    "theory": [
        th("Форма", "Берём nous в présent, убираем -ons, добавляем -ais, -ais, -ait, -ions, -iez, -aient. Исключение одно: être → j’étais.",
           table=[["nous finissons → je finissais", "я заканчивала"], ["nous buvons → je buvais", "я пила"], ["nous avons → il avait", "у него было"],
                  ["nous faisons → nous faisions", "мы делали"], ["nous prenons → vous preniez", "вы брали"], ["être → ils étaient", "они были"]]),
        th("Ловушки написания", "На слух -ais, -ait, -aient звучат одинаково, различает только письмо.",
           exs=[["je mangeais", "я ела: e перед a остаётся"], ["je commençais", "я начинала: ç перед a"], ["nous étudiions", "мы учились: два i"]]),
        th("Когда imparfait", "Описание, привычка, состояние и фон в прошлом.",
           exs=[["J’avais un petit appartement.", "У меня была маленькая квартира."], ["Tous les matins, je prenais un café.", "Каждое утро я пила кофе."],
                ["J’étais fatiguée, il faisait froid.", "Я устала, было холодно."]]),
        th("Подсказка для русского уха",
           "Где по-русски несовершенный вид про прошлое (жила, работала, ходила), там почти всегда imparfait. Совершённый вид (переехала, встретила) — обычно passé composé, это завтра."),
    ],
    "topics": [topic("t-imparfait", "Imparfait: форма",
                     ("nous finissons → je …", ["finissais", "finais", "finirais"]),
                     ("être → j’…", ["étais", "êtais", "avais"]),
                     ("manger → nous …", ["mangions", "mangeions", "mangons"]))],
    "exercises": [
        C("nous finissons → je ___", ["finissais", "finais", "finirais"]),
        J("avoir (imparfait)", [["j’", "avais"], ["tu", "avais"], ["il", "avait"], ["nous", "avions"], ["vous", "aviez"], ["ils", "avaient"]], q="avoir в imparfait: «у меня было…»"),
        G("Quand j’étais petite, nous ___ à la campagne.", "habiter", "habitions"),
        G("Le samedi, mon père ___ des crêpes.", "faire", "faisait"),
        G("Vous ___ à la cantine ?", "manger", "mangiez"),
        G("Je ___ le travail à neuf heures.", "commencer", "commençais"),
        L("Je parlais avec ma voisine.", ["je parle", "je parlais", "j’ai parlé"], 1),
        L("J’ai parlé avec le directeur.", ["je parle", "je parlais", "j’ai parlé"], 2),
        L("Je parle avec mes collègues.", ["je parle", "je parlais", "j’ai parlé"], 0),
        T("Я каждый день ездила на метро.", "Je prenais le métro tous les jours.", "Tous les jours, je prenais le métro.", "Chaque jour, je prenais le métro.", "Je prenais le métro chaque jour."),
        T("Тогда я никого не знала во Франции.", "À l’époque, je ne connaissais personne en France.", "À cette époque, je ne connaissais personne en France.",
          "À l’époque, je ne connaissais personne en France.", "Alors, je ne connaissais personne en France."),
        O("Собери: «По воскресеньям мы часто гуляли»", ["Le dimanche,", "on", "se promenait", "souvent"], "Le dimanche, on se promenait souvent."),
        Q("TCF · Avant, il ___ beaucoup à Lyon ; maintenant, il fait plus chaud.", ["pleuvait", "a plu", "pleut", "pleuvra"]),
        P(1, "Где ты жила до переезда? Допиши: глагол в imparfait и город.", "j’habitais à …", r"\b(habitais|vivais)\b", "habitais или vivais", pre="Avant, ", words=(3, 5)),
        P(1, "Кем ты работала?", "Je travaillais comme …", r"\b(travaillais|étais)\b", "travaillais (или j’étais + профессия)", words=(3, 6)),
        P(2, "Твоя привычка до переезда (2–4 слова).", "prenais le métro", r"^(ne |n')?[" + LETTERS + r"]+ais\b", "форма je в imparfait на -ais", pre="Tous les matins, je ", words=(2, 5)),
    ],
    "sprint": [
        Q("Quand j’étais étudiante, je ___ dans un café le week-end.", ["travaillais", "ai travaillé", "travaille", "travaillerai"]),
        Q("Il ___ froid, alors j’ai mis mon manteau.", ["faisait", "était", "avait", "fait"]),
        Q("Hier soir, nous ___ au cinéma.", ["sommes allés", "allions", "avons allé", "irions"]),
        Q("Avant, nous ___ à la campagne.", ["habitions", "habitons", "avons habité", "habiterons"]),
        Q("Quand il était petit, mon frère ___ beaucoup de lait.", ["buvait", "boivait", "a bu", "boit"]),
        Q("Vous ___ souvent au restaurant à Moscou ?", ["mangiez", "mangez", "mangeiez", "mangeriez"]),
        Q("Ce matin, elle ___ à sept heures.", ["s’est levée", "se levait", "s’a levée", "est levée"]),
        Q("À l’époque, je ne ___ personne.", ["connaissais", "connaisais", "connaîtrai", "connaît"]),
        Q("Le dimanche, mes parents ___ au marché.", ["allaient", "allait", "sont allés", "vont aller"]),
        Q("Je vais ___ mes amis ce soir.", ["voir", "vu", "vois", "voyais"]),
    ],
    "wtext": {
        "intro": "Каркас текста недели начинает заполняться: твои ответы из упражнений уже стоят в части 1 и 2.",
        "micro": [P(1, "Микрозадание: какой была твоя ville? Прилагательное в женском роде (grande, froide, belle…).", "grande et froide",
                    r"\b[" + LETTERS + r"]+e\b", "прилагательное в женском роде (обычно на -e)", pre="Ma ville était ", words=(1, 3))],
    },
    "wrap": {"task": "Доделай недоделанное или ещё раз послушай текст Ирины и повтори его вслух за озвучкой.",
             "can": ["образовать imparfait любого глагола от формы nous", "описать свои привычки до переезда тремя фразами", "различить на слух je parle / je parlais / j’ai parlé"]},
})

# ================================================================ 10.11 · урок 1.2 · passé composé vs imparfait
DAYS.append({
    "date": "2026-11-10", "type": "учебный", "unit": 1, "lesson": "1.2", "minutes": 210,
    "topic": "Passé composé и imparfait: фон и событие",
    "steps": lesson_steps(listening={"items": [dict(video("q0AUWJambhY", "French People’s Most Memorable Stories About School | Easy French 162", "Easy French", "13:30"),
        task="1. Первый просмотр с французскими субтитрами: для 3 человек запиши одним-двумя словами, о чём их история. "
             "2. Второй просмотр: выпиши 2 фразы-фона (imparfait) и 2 фразы-события (passé composé). "
             "3. По желанию: перескажи вслух одну историю в трёх фразах. " + SAY_TASKS)]},
        course={"url": COURSE, "stage": "Étape 03", "task": TV5 + "Сегодня « La description au passé avec l’imparfait » (12 упражнений)."}),
    "warmup": [
        G("Avant, je ___ à Saint-Pétersbourg.", "habiter, imparfait", "habitais"),
        G("Nous ___ souvent au cinéma.", "aller, imparfait", "allions"),
        G("Il ___ froid en hiver.", "faire, imparfait", "faisait"),
        G("Hier, j’___ mes clés.", "perdre, passé composé", "ai perdu"),
        G("Elle ___ à Lyon en mai.", "arriver, passé composé", "est arrivée"),
    ],
    "doc": {
        "title": "Le jour de mon arrivée",
        "who": "Продолжение блога Ирины: её первый вечер в Лионе. Текст написан для урока, в нём смешаны фон и события.",
        "pre": C("Заголовок: « Le jour de mon arrivée ». О чём будет история?", ["о первом дне в новом городе", "о дне рождения", "о свадьбе", "о работе мечты"]),
        "listen": "Шаг 1. Послушай без текста и ответь на вопросы. Шаг 2. Открой текст, послушай ещё раз и найди события.",
        "text": "Le jour de mon arrivée à Lyon, il pleuvait. Il était sept heures du soir et j’étais très fatiguée après le voyage. "
                "Je cherchais mon nouvel appartement avec une grosse valise et un plan sur mon téléphone. Les rues étaient vides, les magasins étaient fermés "
                "et je ne comprenais pas les panneaux. Soudain, mon téléphone s’est éteint : plus de batterie ! J’ai eu peur. "
                "Alors, je suis entrée dans une petite boulangerie qui était encore ouverte. La boulangère m’a souri, elle m’a donné un croissant "
                "et elle a appelé mon propriétaire. Vingt minutes plus tard, il est arrivé en voiture. Ce soir-là, j’ai compris une chose : à Lyon, je n’étais pas seule.",
        "ru": "В день моего приезда в Лион шёл дождь. Было семь вечера, и я очень устала после дороги. Я искала свою новую квартиру с большим чемоданом "
              "и картой в телефоне. Улицы были пустыми, магазины закрыты, и я не понимала указателей. Вдруг мой телефон выключился: батарея села! Мне стало страшно. "
              "Тогда я зашла в маленькую булочную, которая ещё была открыта. Булочница мне улыбнулась, дала круассан и позвонила моему хозяину квартиры. "
              "Через двадцать минут он приехал на машине. В тот вечер я поняла одну вещь: в Лионе я не одна.",
        "quiz": [
            Q("Quel temps faisait-il quand Irina est arrivée ?", ["il pleuvait", "il neigeait", "il faisait beau", "il faisait très chaud"]),
            Q("Quel problème a-t-elle eu ?", ["son téléphone n’avait plus de batterie", "elle a perdu sa valise", "elle a raté son train", "elle a oublié son adresse"]),
            Q("Qui l’a aidée ?", ["une boulangère", "une voisine", "un policier", "un chauffeur de taxi"]),
            VF("Irina était fatiguée après le voyage.", 0),
            VF("Le propriétaire est arrivé à pied.", 1),
            VF("La boulangère parlait anglais.", 2),
        ],
        "hunt": {"q": "Охота на формы: нажми на причастие (вторую часть) каждого passé composé — это события истории. Их 8.",
                 "forms": ["éteint", "eu", "entrée", "souri", "donné", "appelé", "arrivé", "compris"]},
        "chunks": [["le jour de mon arrivée", "в день моего приезда"], ["une grosse valise", "большой чемодан"], ["les rues étaient vides", "улицы были пустыми"],
                   ["soudain", "вдруг"], ["plus de batterie", "батарея села"], ["j’ai eu peur", "мне стало страшно"],
                   ["vingt minutes plus tard", "через двадцать минут"], ["ce soir-là", "в тот вечер"]],
    },
    "observe": {
        "intro": "Две колонки из текста:",
        "table": [["фон: как было", "il pleuvait · j’étais fatiguée · je cherchais · les rues étaient vides"],
                  ["события: что случилось", "mon téléphone s’est éteint · je suis entrée · elle a appelé · il est arrivé"]],
        "qs": [dict(C("« Il pleuvait » — это…", ["фон: как было", "событие: что случилось"]), fixed=True),
               dict(C("« Il est arrivé en voiture » — это…", ["фон: как было", "событие: что случилось"], 1), fixed=True)],
        "rule": "Когда автор выбирает imparfait, а когда passé composé? Ответь одной строкой.",
        "model": "Imparfait — фон и описание: погода, время, состояние, что происходило. Passé composé — события, которые двигают историю: что случилось потом. "
                 "Сигналы событий: soudain, alors, tout à coup, vingt minutes plus tard.",
    },
    "theory": [
        th("Фон и событие", "Imparfait — декорации сцены, passé composé — действие на сцене.",
           table=[["Il pleuvait.", "Шёл дождь. (фон)"], ["Soudain, le téléphone s’est éteint.", "Вдруг телефон выключился. (событие)"]]),
        th("Одно действие прерывает другое", "Длинное действие — imparfait, то, что его прервало, — passé composé.",
           exs=[["Je cherchais l’appartement quand mon téléphone s’est éteint.", "Я искала квартиру, когда телефон выключился."],
                ["Je dormais quand tu as appelé.", "Я спала, когда ты позвонил."]]),
        th("Слова-сигналы", "Imparfait: tous les jours, souvent, d’habitude, avant, à l’époque, le dimanche. Passé composé: hier, soudain, tout à coup, un jour, ce jour-là, deux fois."),
        th("Подсказка для русского уха",
           "Шла, искала, было — несовершенный вид, imparfait. Пришла, нашла, позвонила — совершённый, passé composé. "
           "Чувство в один момент («мне стало страшно») — тоже событие: j’ai eu peur."),
    ],
    "topics": [topic("t-pc-imp", "Passé composé или imparfait",
                     ("Il ___ quand je suis sortie.", ["pleuvait", "a plu", "pleut"]),
                     ("Soudain, le téléphone ___ .", ["a sonné", "sonnait", "sonne"]),
                     ("Quand j’étais petite, je ___ à pied à l’école.", ["allais", "suis allée", "vais"]))],
    "exercises": [
        Q("Quand je suis arrivée, il ___ .", ["pleuvait", "a plu", "pleut", "pleuvra"]),
        Q("Je dormais quand le téléphone ___ .", ["a sonné", "sonnait", "sonne", "sonnera"]),
        G("Hier, il ___ beau, alors nous sommes allés au parc.", "faire · фон: погода", "faisait"),
        G("Je regardais la télé quand ma sœur ___ .", "arriver · событие прерывает", "est arrivée"),
        G("Quand j’étais petite, j’___ à l’école à pied.", "aller · привычка", "allais"),
        G("Un jour, j’___ mon voisin dans le métro.", "rencontrer · одно событие", "ai rencontré"),
        G("Les rues ___ vides et il faisait nuit.", "être · описание", "étaient"),
        G("Soudain, nous ___ un bruit.", "entendre · soudain → событие", "avons entendu"),
        L("Il faisait froid quand je suis sortie.", ["il faisait froid quand je suis sortie", "il a fait froid quand je sortais", "il fait froid quand je sors"], 0),
        T("Когда я жила в Москве, я работала в банке.", "Quand j’habitais à Moscou, je travaillais dans une banque.", "Quand je vivais à Moscou, je travaillais dans une banque."),
        T("Шёл снег, и вдруг я увидела друга.", "Il neigeait et soudain j’ai vu un ami.", "Il neigeait et soudain j’ai vu mon ami.", "Il neigeait et tout à coup j’ai vu un ami.",
          "Il neigeait et tout à coup j’ai vu mon ami.", "Il neigeait et soudain j’ai vu une amie.", "Il neigeait et soudain j’ai vu mon amie."),
        O("Собери: «Я ждала автобус, когда начался дождь»", ["J’attendais", "le bus", "quand", "il a commencé", "à pleuvoir"], "J’attendais le bus quand il a commencé à pleuvoir."),
        Q("TCF · Nous ___ depuis une heure quand le train est enfin arrivé.", ["attendions", "avons attendu", "attendons", "attendrons"]),
        P(3, "Какая была погода в день отъезда?", "faisait froid / pleuvait", r"\b(faisait|pleuvait|neigeait|était|avait)\b", "фон в imparfait: faisait, pleuvait, neigeait…", pre="Le jour de mon départ, il ", words=(2, 5)),
        P(3, "Что ты чувствовала? Прилагательное в женском роде.", "triste et contente", r"e\b", "прилагательное в женском роде: triste, fatiguée, nerveuse…", pre="J’étais ", words=(1, 4)),
    ],
    "sprint": [
        Q("Quand je suis entrée, mes amis ___ un film.", ["regardaient", "ont regardé", "regardent", "regarderont"]),
        Q("Il était minuit quand le téléphone ___ .", ["a sonné", "sonnait", "sonnera", "sonne"]),
        Q("D’habitude, je ___ à huit heures.", ["me levais", "me suis levée", "m’ai levée", "me lèverais"]),
        Q("Ce jour-là, nous ___ le train de 7 heures.", ["avons pris", "prenions", "prenons", "avons prendu"]),
        Q("Elle ___ fatiguée, alors elle est rentrée.", ["était", "a été", "est", "sera"]),
        Q("Tout à coup, j’___ un bruit.", ["ai entendu", "entendais", "entends", "entendrai"]),
        Q("Avant, il y ___ un cinéma ici.", ["avait", "a eu", "a", "aura"]),
        Q("Demain, nous ___ partir tôt.", ["allons", "allez", "sommes", "avons"]),
        Q("Elle s’est ___ à 7 heures.", ["réveillée", "réveillé", "réveiller", "réveillait"]),
        Q("J’habite ___ France depuis un an.", ["en", "à", "au", "dans"]),
    ],
    "wtext": {
        "intro": "Сегодня в каркас добавились части 3 и 4.",
        "micro": [P(4, "Микрозадание: закончи фразу про себя — фон и событие после soudain (4–8 слов).", "beau et soudain j’ai vu la mer",
                    r"soudain.*" + PC, "после soudain — событие в passé composé", pre="Le jour de mon arrivée, il faisait ", words=(4, 8))],
    },
    "wrap": {"task": "Доделай недоделанное или ещё раз послушай историю Ирины и повтори вслух три события.",
             "can": ["отличить фон (imparfait) от события (passé composé)", "рассказать короткую историю: il faisait…, soudain…", "понять на слух, что было фоном, а что случилось"]},
})

# ================================================================ 11.11 · урок 1.3 · COD + ударные местоимения
DAYS.append({
    "date": "2026-11-11", "type": "учебный", "unit": 1, "lesson": "1.3", "minutes": 210,
    "topic": "Le / la / les в прошедшем времени · moi, toi, lui",
    "steps": lesson_steps(listening={"items": [dict(video("plbEfexGB5U", "Hélène Is Leaving Paris: A French Woman in England | Easy French 160", "Easy French", "17:12"),
        task="1. Первый просмотр с французскими субтитрами: куда и почему уезжает Hélène? Ответь себе одной фразой по-русски. "
             "2. Второй просмотр: выпиши 3 фразы, где она говорит о прошлом. "
             "3. По желанию: скажи вслух 2 фразы о своём переезде. " + SAY_TASKS)]},
        course={"url": COURSE, "stage": "Étape 04", "task": TV5 + "Сегодня « L’alternance du passé composé et de l’imparfait dans le récit » (12 упражнений)."}),
    "warmup": [
        G("Il ___ quand je suis arrivée.", "pleuvoir · фон", "pleuvait"),
        G("Soudain, mon téléphone ___ .", "sonner · событие", "a sonné"),
        G("Avant, nous ___ près du métro.", "habiter", "habitions"),
        G("Je ___ de chez moi à huit heures.", "sortir · passé composé", "suis sortie", "suis sorti"),
        G("Elle ___ très fatiguée ce soir-là.", "être · состояние", "était"),
    ],
    "doc": {
        "title": "innerFrench · E13 « Les malheurs des gagnants du loto »",
        "who": "Подкаст для среднего уровня (B1). Тебе пока не нужно понимать всё: цель — общий смысл и истории о прошлом.",
        "video": video("H-ZywB_iOmM", "E13 Les malheurs des gagnants du loto", "innerFrench", "30:16"),
        "task": "Слушай первые 15 минут с французскими субтитрами, остальное — по желанию. Вопросы ниже — по официальному описанию выпуска. "
                "Потом запиши себе 3 проблемы, которые были у победителей лотереи (по-французски, 2–4 слова на каждую): ключа к ним на сайте нет, проверяй по субтитрам.",
        "pre": C("Название: « Les malheurs des gagnants du loto ». О чём выпуск?", ["о бедах тех, кто выиграл в лотерею", "о том, как выиграть в лотерею", "о казино в Париже", "о лотерее для детей"]),
        "quiz": [
            Q("Selon la présentation de l’épisode, la vie des gagnants a changé…", ["d’une manière qu’ils n’attendaient pas", "exactement comme ils l’imaginaient", "très peu", "seulement pour leur famille"]),
            Q("Qu’est-ce que la société de la loterie en France a mis en place ?", ["une équipe d’experts pour aider les gagnants", "un site pour vendre des billets", "un jeu pour les enfants", "une banque spéciale"]),
            Q("Ce podcast est pour qui ?", ["des apprenants de niveau intermédiaire", "des débutants complets", "des enfants français", "des professeurs"]),
        ],
        "chunks": [["gagner au loto", "выиграть в лотерею"], ["un billet gagnant", "выигрышный билет"], ["changer de vie", "изменить жизнь"],
                   ["une équipe d’experts", "команда экспертов"], ["aider quelqu’un", "помогать кому-то"], ["dépenser de l’argent", "тратить деньги"]],
        "chunksNote": "Слова к теме выпуска.",
    },
    "observe": {
        "intro": "Диалог «Au bureau»: коллега расспрашивает тебя о переезде.",
        "table": [["— Tu as vu ta famille avant de partir ?", "— Oui, je l’ai vue la veille."],
                  ["— Et tes amis ?", "— Je les ai invités chez moi."],
                  ["— Ta valise, tu l’as faite quand ?", "— Je l’ai faite la nuit avant le départ !"],
                  ["— Tu es partie seule ?", "— Non, avec mon chat. Lui, il n’était pas content !"]],
        "qs": [C("« Je les ai invités » — кого «les»?", ["tes amis", "ta famille", "ta valise", "toi"]),
               G("Je l’ai vu___ la veille.", "ta famille → какая буква добавилась к vu?", "e")],
        "rule": "Сравни: ta famille → je l’ai vue; tes amis → je les ai invités. Почему меняется причастие?",
        "model": "Le / la / les заменяют прямое дополнение (кого? что?) и стоят перед глаголом. Если такое местоимение стоит перед avoir, "
                 "причастие согласуется с ним: la → +e (vue), les → +s или +es (invités, prises).",
    },
    "theory": [
        th("Le, la, l’, les: «его, её, их»", "Заменяют прямое дополнение и стоят перед глаголом.",
           table=[["Je vois Marc. → Je le vois.", "Я его вижу."], ["Je vois Anna. → Je la vois.", "Я её вижу."],
                  ["Je vois mes amis. → Je les vois.", "Я их вижу."], ["J’aime cette ville. → Je l’aime.", "Перед гласной — l’."]]),
        th("Место в предложении", "В passé composé — перед avoir. С отрицанием ne … pas обнимают местоимение вместе с avoir. С инфинитивом — перед инфинитивом.",
           exs=[["Je l’ai vu.", "Я его видела."], ["Je ne l’ai pas vu.", "Я его не видела."], ["Je vais la voir.", "Я её увижу."]]),
        th("Согласование причастия", "Если le / la / les стоит перед avoir, причастие получает род и число этого слова. На слух часто не слышно (vu — vue), но écrite, prise, faite слышно.",
           exs=[["La lettre ? Je l’ai écrite.", "Письмо? Я его написала (lettre — ж. р.)."], ["Les photos ? Je les ai prises.", "Фото? Я их сделала."],
                ["Les billets ? Je les ai achetés.", "Билеты? Я их купила."]]),
        th("Ударные местоимения: moi, toi, lui, elle, nous, vous, eux, elles",
           "После предлогов (chez moi, avec lui, pour eux), для выделения (Moi, j’habitais à Kazan.) и в коротких ответах (Et toi ? — Moi aussi.).",
           exs=[["Je suis rentrée chez moi.", "Я вернулась домой."], ["Lui, il n’était pas content.", "А он был недоволен."], ["Je pense à eux.", "Я думаю о них."]]),
    ],
    "topics": [topic("t-cod-pp", "Le / la / les + согласование",
                     ("Ta valise ? Je l’ai …", ["faite", "fait", "faits"]),
                     ("Mes amis ? Je … ai invités.", ["les", "leur", "la"]),
                     ("Il est parti sans …", ["moi", "me", "je"]))],
    "exercises": [
        Q("Tu connais Marie ? — Oui, je ___ connais.", ["la", "le", "lui", "les"]),
        Q("Tu as vu mes clés ? — Non, je ne ___ ai pas vues.", ["les", "la", "leur", "le"]),
        G("Le métro ? Je ___ prenais tous les jours.", "le métro → местоимение", "le"),
        G("Ta valise ? Je l’ai fai___ hier soir.", "согласование с la (valise)", "te"),
        G("Les photos ? Je les ai pri___ à Saint-Pétersbourg.", "согласование с les (photos, ж. р. мн. ч.)", "ses"),
        G("Mes amis ? Je ___ ai invités chez moi.", "mes amis → ?", "les"),
        T("Твою сестру? Я её видела вчера.", "Ta sœur ? Je l’ai vue hier.", "Ta soeur ? Je l’ai vue hier.", "Je l’ai vue hier."),
        T("Я их не знала.", "Je ne les connaissais pas."),
        Q("___, j’habitais à Kazan. Et toi ?", ["Moi", "Je", "Me", "Mon"]),
        Q("Je suis rentrée chez ___ à minuit.", ["moi", "je", "me", "ma"]),
        Q("Mes parents ? Je pense souvent à ___ .", ["eux", "ils", "les", "leur"]),
        O("Собери: «Я её не видела»", ["Je", "ne", "l’ai", "pas", "vue"], "Je ne l’ai pas vue."),
        Q("TCF · Ces chaussures ? Je les ai ___ à Lyon.", ["achetées", "acheté", "achetés", "achetée"]),
        P(2, "Что вы делали с друзьями по выходным? Форма on в imparfait.", "allait au café", r"\b[" + LETTERS + r"]+ait\b", "форма on в imparfait на -ait", pre="Le week-end, avec mes amis, on ", words=(2, 5)),
        P(2, "Как часто ты видела семью? Используй la вместо «ma famille».", "la voyais le dimanche", r"(^|\s)(la|l'|les)\b", "местоимение la / l’ перед глаголом", pre="Ma famille ? Je ", words=(2, 5)),
    ],
    "sprint": [
        Q("Ton passeport ? Je ___ ai oublié à la maison !", ["l’", "le", "lui", "les"]),
        Q("Les clés ? Je les ai ___ sur la table.", ["laissées", "laissé", "laissés", "laissée"]),
        Q("Il est parti sans ___ .", ["moi", "me", "je", "mon"]),
        Q("Cette chanson ? Je l’ai ___ à la radio.", ["entendue", "entendu", "entendus", "entendues"]),
        Q("___, ils habitaient à Nice.", ["Eux", "Ils", "Leur", "Les"]),
        Q("Quand j’étais petite, je ___ souvent chez ma grand-mère.", ["allais", "suis allée", "irai", "irais"]),
        Q("Nous dormions quand l’orage ___ .", ["a commencé", "commençait", "commence", "commencera"]),
        Q("Elles se sont ___ au café.", ["retrouvées", "retrouvé", "retrouvés", "retrouver"]),
        Q("Nous ___ dîner chez Paul ce soir.", ["allons", "avons", "sommes", "faisons"]),
        Q("Je viens ___ Russie.", ["de", "du", "en", "à"]),
    ],
    "wtext": {
        "intro": "Сегодня соединяем твои фразы прошлых дней.",
        "show": [["2026-11-09", "e14"], ["2026-11-09", "e16"], ["2026-11-11", "e14"]],
        "micro": [P(2, "Микрозадание: соедини две свои фразы о прошлой жизни связкой quand / mais / alors / donc (3–10 слов).", "Quand j’habitais à …, je … mais …",
                    r"\b(quand|mais|alors|donc|parce que)\b", "связка quand / mais / alors / donc", words=(3, 10))],
        "dialog": {"title": "Диалог с Claude: коллега расспрашивает о прошлом",
                   "note": "По желанию — голосом. Скопируй запрос, вставь в Claude и отвечай по одной фразе.",
                   "prompt": "Давай разыграем диалог на французском (уровень A2). Ты — мой новый коллега в офисе в Лионе, тебя зовут Thomas. "
                             "Ты расспрашиваешь меня о моей жизни до переезда: где я жила, кем работала, какие у меня были привычки и как прошёл мой первый день во Франции.\n"
                             "Правила: задавай по одному короткому вопросу, говори просто, используй imparfait и passé composé. "
                             "После каждого моего ответа сначала одной строкой по-русски исправь мои ошибки (если их нет — напиши «без ошибок»), потом задай следующий вопрос. "
                             "После 8 вопросов закончи разговор и дай мне по-русски 3 совета: что повторить. Начни с приветствия и первого вопроса."},
    },
    "wrap": {"task": "Доделай недоделанное или перечитай диалог «Au bureau» вслух по ролям.",
             "can": ["заменить существительное местоимением le / la / les", "согласовать причастие после la / les: je l’ai vue", "сказать moi, toi, lui, eux после предлогов: chez moi, avec lui"]},
})

# ================================================================ 12.11 · урок 1.4 · pendant / depuis / il y a / quand
DAYS.append({
    "date": "2026-11-12", "type": "учебный", "unit": 1, "lesson": "1.4", "minutes": 210,
    "topic": "Depuis, il y a, pendant, quand, soudain",
    "steps": lesson_steps(listening={"items": [dict(video("YtFvaBtV1Cc", "What’s Your Life Story? We Asked French People to Share! | Easy French 228", "Easy French", "9:14"),
        task="1. Первый просмотр с французскими субтитрами: для 3 человек запиши одну дату или срок (il y a…, depuis…, pendant…). "
             "2. Второй просмотр: выпиши 2 фразы с depuis, il y a или pendant. "
             "3. По желанию: расскажи вслух свою историю в четырёх фразах. " + SAY_TASKS)]},
        course={"url": COURSE, "stage": "Étape 05", "task": TV5 + "Сегодня « L’organisation du récit avec les indicateurs de temps » (12 упражнений)."}),
    "warmup": [
        G("Ta valise ? Je l’ai fai___ .", "согласование с la", "te"),
        G("Mes amis ? Je ___ ai vus hier.", "mes amis → ?", "les"),
        G("Je dormais quand tu ___ .", "appeler · событие", "as appelé"),
        G("Il est parti sans ___ .", "я → ударное", "moi"),
        G("Avant, on ___ beaucoup.", "sortir · imparfait", "sortait"),
    ],
    "doc": {
        "title": "Deux ans à Lille",
        "who": "Блог-пост Марты, испанки, которая переехала в Лилль. Это образец текста недели: те же 5 частей, что и в твоём каркасе. Написан для урока.",
        "pre": C("Это блог-пост « Deux ans à Lille ». Чего ждать?", ["истории переезда", "рецепта", "рекламы отеля", "новостей"]),
        "listen": "Шаг 1. Послушай без текста и ответь на вопросы. Шаг 2. Открой текст и найди в нём 5 частей: avant, ma vie là-bas, le départ, le premier jour, aujourd’hui.",
        "text": "Bonjour à tous ! Il y a deux ans, j’ai quitté Madrid et je suis venue vivre à Lille. Avant, je travaillais dans une agence de voyages. "
                "J’habitais dans un petit studio au centre-ville et je sortais tous les soirs avec mes amis. "
                "Pendant mes dernières semaines à Madrid, j’étais triste et heureuse en même temps. "
                "Le jour de mon arrivée, il faisait gris et il y avait du vent. Je ne connaissais personne. "
                "Quand je suis sortie de la gare, j’ai pris un taxi pour aller chez ma colocataire, Julie. "
                "Soudain, le taxi s’est arrêté : un grand marché bloquait la rue ! Julie est venue me chercher à pied et nous avons acheté des gaufres ensemble. "
                "Aujourd’hui, j’habite à Lille depuis deux ans. Julie est ma meilleure amie et, moi, j’adore cette ville.",
        "ru": "Всем привет! Два года назад я уехала из Мадрида и переехала жить в Лилль. Раньше я работала в турагентстве. Я жила в маленькой студии в центре "
              "и каждый вечер ходила куда-нибудь с друзьями. Последние недели в Мадриде мне было и грустно, и радостно одновременно. "
              "В день моего приезда было пасмурно и ветрено. Я никого не знала. Когда я вышла из вокзала, я взяла такси, чтобы доехать до соседки по квартире, Жюли. "
              "Вдруг такси остановилось: большой рынок перекрыл улицу! Жюли пришла за мной пешком, и мы вместе купили вафли. "
              "Сегодня я живу в Лилле уже два года. Жюли — моя лучшая подруга, а я обожаю этот город.",
        "quiz": [
            Q("Quand Marta est-elle arrivée à Lille ?", ["il y a deux ans", "il y a deux mois", "l’année dernière", "il y a une semaine"]),
            Q("Que faisait-elle à Madrid ?", ["elle travaillait dans une agence de voyages", "elle était étudiante", "elle travaillait dans une gare", "elle était chauffeur de taxi"]),
            Q("Pourquoi le taxi s’est-il arrêté ?", ["un marché bloquait la rue", "il n’avait plus d’essence", "il pleuvait trop", "Julie l’a arrêté"]),
            VF("Marta était seulement triste de partir.", 1),
            VF("Julie habite toujours avec Marta.", 2),
            VF("Le jour de son arrivée, il faisait beau.", 1),
        ],
        "hunt": {"q": "Охота на формы: нажми на все глаголы в imparfait (фон и привычки). Их 8.",
                 "forms": ["travaillais", "habitais", "sortais", "étais", "faisait", "avait", "connaissais", "bloquait"]},
        "chunks": [["il y a deux ans", "два года назад"], ["j’ai quitté Madrid", "я уехала из Мадрида"], ["une agence de voyages", "турагентство"],
                   ["en même temps", "одновременно"], ["il y avait du vent", "было ветрено"], ["ma colocataire", "моя соседка по квартире"],
                   ["venir chercher quelqu’un", "прийти, заехать за кем-то"], ["depuis deux ans", "уже два года"]],
    },
    "observe": {
        "intro": "Слова времени из текста Марты:",
        "table": [["il y a deux ans, j’ai quitté…", "точка в прошлом: «… назад»"], ["pendant mes dernières semaines", "сколько длилось"],
                  ["j’habite à Lille depuis deux ans", "началось тогда и длится сейчас"], ["quand je suis sortie de la gare", "в какой момент"],
                  ["soudain, le taxi s’est arrêté", "неожиданное событие"]],
        "qs": [dict(C("« J’habite à Lille depuis deux ans » — Марта всё ещё живёт в Лилле?", ["да", "нет"]), fixed=True),
               C("« Il y a deux ans, j’ai quitté Madrid » — il y a здесь значит…", ["… назад", "уже", "в течение", "с тех пор как"])],
        "rule": "Чем отличаются « il y a deux ans » и « depuis deux ans »? Ответь одной строкой.",
        "model": "Il y a + срок = «… назад»: точка в прошлом, обычно с passé composé. Depuis + срок = «уже … / с …»: действие продолжается сейчас, глагол в présent.",
    },
    "theory": [
        th("Il y a — «назад»", "Точка в прошлом.",
           table=[["Je suis arrivée il y a un an.", "Я приехала год назад."], ["Il y a trois jours, j’ai vu Marc.", "Три дня назад я видела Марка."]]),
        th("Depuis — «уже, с»", "Действие началось в прошлом и продолжается сейчас, поэтому глагол в présent — как и в русском «живу уже год».",
           table=[["J’habite ici depuis un an.", "Я живу здесь уже год."], ["J’apprends le français depuis septembre.", "Я учу французский с сентября."]]),
        th("Pendant — «в течение, во время»", "Сколько длилось законченное действие.",
           table=[["J’ai travaillé pendant cinq ans à Moscou.", "Я пять лет работала в Москве."], ["Pendant le voyage, je dormais.", "Во время поездки я спала."]]),
        th("Quand и soudain в рассказе", "Quand + момент, soudain / tout à coup + неожиданное событие в passé composé.",
           exs=[["Quand je suis arrivée, il pleuvait.", "Когда я приехала, шёл дождь."], ["Soudain, le taxi s’est arrêté.", "Вдруг такси остановилось."]]),
    ],
    "topics": [topic("t-temps", "Depuis / il y a / pendant",
                     ("J’habite ici … un an.", ["depuis", "il y a", "pendant"]),
                     ("Je suis arrivée … un an.", ["il y a", "depuis", "pendant"]),
                     ("«Я пять лет работала в банке» → J’ai travaillé … cinq ans.", ["pendant", "depuis", "il y a"]))],
    "exercises": [
        Q("J’habite à Lyon ___ un an.", ["depuis", "il y a", "pendant", "dans"]),
        Q("Je suis arrivée en France ___ un an.", ["il y a", "depuis", "pendant", "dans"]),
        Q("«Я учила английский пять лет» → J’ai appris l’anglais ___ cinq ans.", ["pendant", "depuis", "il y a", "dans"]),
        G("Je connais Julie ___ 2024.", "с 2024 года", "depuis"),
        G("___ trois jours, j’ai reçu une lettre.", "три дня назад", "il y a"),
        G("___ je suis arrivée, il pleuvait.", "когда", "quand"),
        G("Nous marchions dans la rue. ___, nous avons vu un accident.", "вдруг", "soudain", "tout à coup"),
        T("Я живу во Франции уже год.", "J’habite en France depuis un an.", "Je vis en France depuis un an."),
        T("Я приехала в Лион два месяца назад.", "Je suis arrivée à Lyon il y a deux mois.", "Il y a deux mois, je suis arrivée à Lyon.", "Je suis venue à Lyon il y a deux mois."),
        L("J’habite ici depuis trois ans.", ["depuis trois ans", "il y a trois ans", "pendant trois ans"], 0),
        O("Собери: «Во время поездки я читала»", ["Pendant", "le voyage,", "je", "lisais"], "Pendant le voyage, je lisais."),
        Q("TCF · Il est parti ___ dix minutes, tu viens de le rater !", ["il y a", "depuis", "pendant", "dans"]),
        P(1, "Сколько лет ты жила в своём городе? pendant + срок.", "Moscou pendant dix ans", r"\bpendant\b", "pendant + срок", pre="J’ai vécu à ", words=(3, 6)),
        P(5, "Сколько ты живёшь на новом месте? depuis + срок.", "Lyon depuis un an", r"\bdepuis\b", "depuis + срок", pre="Aujourd’hui, j’habite à ", words=(3, 6)),
    ],
    "sprint": [
        Q("Je fais du yoga ___ six mois.", ["depuis", "il y a", "pendant", "dans"]),
        Q("Je l’ai rencontré ___ deux ans, à Paris.", ["il y a", "depuis", "pendant", "dans"]),
        Q("Nous avons parlé ___ toute la soirée.", ["pendant", "depuis", "il y a", "dans"]),
        Q("___ j’étais petite, j’avais un chat.", ["Quand", "Pendant", "Depuis", "Il y a"]),
        Q("Je lisais ___ le téléphone a sonné.", ["quand", "pendant", "depuis", "soudain"]),
        Q("Ta lettre ? Je l’ai ___ hier.", ["reçue", "reçu", "reçus", "reçues"]),
        Q("Avant, je ___ en Russie.", ["vivais", "vis", "ai vivé", "vivrai"]),
        Q("Ils se ___ levés tôt.", ["sont", "ont", "sommes", "est"]),
        Q("Je vais ___ appeler demain.", ["t’", "te", "toi", "tu"]),
        Q("Elle n’___ jamais allée en Italie.", ["est", "a", "ai", "es"]),
    ],
    "wtext": {
        "intro": "Разбор образца: так выглядит часть 4 у Марты. Замени три подчёркнутые детали своими.",
        "model": "Le jour de mon arrivée, il faisait gris. Quand je suis sortie de [la gare], [j’ai pris un taxi]. Soudain, [le taxi s’est arrêté].",
        "micro": [
            P(4, "Деталь 1–2: откуда ты вышла и что сделала (событие).", "l’aéroport, j’ai pris le bus", PC, "событие в passé composé: j’ai pris…", pre="Quand je suis sortie de ", words=(3, 8)),
            P(4, "Деталь 3: что вдруг случилось?", "mon téléphone s’est éteint", PC, "событие в passé composé", pre="Soudain, ", words=(2, 6)),
            P(3, "И ещё одна деталь для части 3: что ты сделала накануне отъезда?", "dit au revoir à mes amis", r"^[" + LETTERS + r"]+(é|i|is|u|it|ert)\b", "participe passé после j’ai: dit, fait, vu…", pre="La veille de mon départ, j’ai ", words=(2, 6)),
        ],
    },
    "wrap": {"task": "Доделай недоделанное или перечитай вслух блог Марты и свой каркас.",
             "can": ["сказать, сколько что-то длится (depuis) или длилось (pendant)", "сказать, когда что-то случилось: il y a…", "построить рассказ: quand…, soudain…"]},
})

# ================================================================ 13.11 · урок 1.5 · TCF-день
DAYS.append({
    "date": "2026-11-13", "type": "учебный", "unit": 1, "lesson": "1.5", "minutes": 210,
    "topic": "TCF-день: серия № 17 и итог недели",
    "steps": [
        {"kind": "review", "title": "Разгон: карточки и спираль", "min": 15},
        {"kind": "tcf", "title": "TCF: серия № 17", "min": 70, "url": TCF17,
         "label": "Открыть серию № 17", "sub": "TV5MONDE · Série d’entraînement n°17",
         "links": [["Structure de la langue", TCF17 + "&competence=SL"], ["Compréhension écrite", TCF17 + "&competence=CE"]],
         "task": "Сегодня части «Structure de la langue» и «Compréhension écrite», аудирование — по желанию. Без словаря, засекай время. "
                 "Потом запиши результат, а вопросы, где ошиблась, добавь в карточки ниже в виде «верная фраза — что было не так».",
         "catch": "Журнал ошибок серии"},
        {"kind": "exercises", "title": "Итог недели: упражнения", "min": 20},
        {"kind": "sprint", "title": "TCF-спринт", "min": 15},
        {"kind": "course", "title": "Онлайн-курс TV5", "min": 30, "url": COURSE, "stage": "Étape 06",
         "task": TV5 + "Сегодня « Bilan : l’expression du passé » (14 упражнений) — итог модуля."},
        {"kind": "listening", "title": "Второе аудио", "min": 35, "items": [dict(video("7n6U46hICDo", "Speaking about the past | Super Easy French 11", "Easy Languages", "4:42"),
            task="1. Посмотри 2 раза с субтитрами. 2. Выпиши 4 вопроса о прошлом, которые задают на улице, и ответь на каждый письменно про себя. "
                 "3. Повтори вслух 5 ответов вслед за людьми (shadowing). " + SAY_TASKS)]},
        {"kind": "wtext", "title": "Текст недели", "min": 15},
        {"kind": "wrap", "title": "Запас и итог дня", "min": 10},
    ],
    "warmup": [
        G("J’habite ici ___ six mois.", "уже полгода", "depuis"),
        G("Je suis arrivée ___ six mois.", "полгода назад", "il y a"),
        G("Les photos ? Je les ai pri___ .", "согласование", "ses"),
        G("Quand je suis entrée, il ___ nuit.", "faire · фон", "faisait"),
        G("Avec ___, je parle russe.", "он → ударное", "lui"),
    ],
    "exercises": [
        Q("Quand j’___ petite, j’habitais à la campagne.", ["étais", "ai été", "suis", "serai"]),
        Q("Hier, il ___ quand je suis sortie.", ["pleuvait", "a plu", "pleut", "pleuvra"]),
        G("Nous ___ quand Paul est arrivé.", "dîner · фон", "dînions"),
        G("Ce matin, j’___ mon bus.", "rater · событие", "ai raté"),
        G("Ta valise ? Je l’ai mi___ dans la voiture.", "согласование с la", "se"),
        G("J’apprends le français ___ septembre.", "с сентября", "depuis"),
        G("Je suis arrivée ___ trois mois.", "три месяца назад", "il y a"),
        Q("Les enfants ? Je pense souvent à ___ .", ["eux", "ils", "leur", "les"]),
        T("Когда я была маленькой, мы жили в Казани.", "Quand j’étais petite, nous habitions à Kazan.", "Quand j’étais petite, nous vivions à Kazan.",
          "Quand j’étais petite, on habitait à Kazan.", "Quand j’étais petite, on vivait à Kazan."),
        T("Я её не узнала.", "Je ne l’ai pas reconnue."),
        D("Il faisait nuit quand je suis arrivée."),
        O("Собери: «Мои фотографии? Я их потеряла»", ["Mes photos ?", "Je", "les", "ai", "perdues"], "Mes photos ? Je les ai perdues."),
    ],
    "sprint": [
        Q("Je ___ dans ce quartier depuis 2023.", ["vis", "ai vécu", "vivais", "vivrai"]),
        Q("Quand nous étions enfants, nous ___ au foot.", ["jouions", "avons joué", "jouons", "jouerons"]),
        Q("Tes lunettes ? Je les ai ___ dans le salon.", ["vues", "vu", "vus", "vue"]),
        Q("Il a habité à Rome ___ dix ans, puis il est rentré.", ["pendant", "depuis", "il y a", "dans"]),
        Q("Je cuisinais quand, tout à coup, le chat ___ sur la table.", ["a sauté", "sautait", "saute", "sautera"]),
        Q("Avec ___, je parle toujours français.", ["elle", "la", "sa", "l’"]),
        Q("Hier soir, j’___ très fatiguée, alors je me suis couchée tôt.", ["étais", "ai", "suis", "serai"]),
        Q("Elle s’est ___ de train.", ["trompée", "trompé", "trompés", "tromper"]),
        Q("On ___ au restaurant ce soir ?", ["va", "vont", "allons", "est"]),
        Q("Il ___ Moscou il y a un an.", ["a quitté", "quittait", "quitte", "quittera"]),
    ],
    "wtext": {
        "intro": "Перед субботой: перестрой одну свою фразу с местоимением.",
        "micro": [P(3, "Микрозадание: перестрой фразу «J’ai quitté ma ville en …» так, чтобы вместо «ma ville» было местоимение (5–8 слов).",
                    "Ma ville ? Je l’ai quittée en juillet.", r"(^|\s)(l'|la|le|les)\b", "местоимение l’ / la / le / les перед глаголом", words=(4, 9))],
    },
    "wrap": {"task": "Доделай недоделанное. Вопросы серии, где ошиблась, — в карточки.",
             "can": ["сделать «структуры языка» TCF на время", "разобрать свои ошибки и превратить их в карточки"]},
})

# ================================================================ 14.11 · урок 1.6 · финал юнита
DAYS.append({
    "date": "2026-11-14", "type": "финал", "unit": 1, "lesson": "1.6", "minutes": 120,
    "topic": "Финал юнита: текст недели, Le Petit Prince, Lupin",
    "steps": [
        {"kind": "review", "title": "Карточки", "min": 10},
        {"kind": "wtext", "title": "Текст недели: довести до 120–150 слов", "min": 30, "final": True},
        {"kind": "reading", "title": "Le Petit Prince", "min": 30, "chapters": "12–17", "url": PETIT_PRINCE,
         "task": "Читай вслух. Нажимай на незнакомые слова и добавляй нужные в карточки."},
        {"kind": "film", "title": "Lupin, серия 1", "min": 40, "film": "Lupin, сезон 1, серия 1",
         "where": "Сериал идёт на Netflix: открой его в приложении. Ссылку не даю, она зависит от страны.",
         "task": "Смотри с французскими субтитрами. В серии много рассказов о прошлом — лови imparfait и passé composé и выпиши 5 фраз в поле ниже."},
        {"kind": "wrap", "title": "Faites le point", "min": 10},
    ],
    "wtext": {
        "intro": "Сайт собрал твои куски за неделю в черновик. Доведи его до 120–150 слов: добавь начало и концовку, две связки "
                 "(d’abord, ensuite, alors, mais, enfin), проверь формы. Потом скопируй запрос для Claude, исправь 3 места, которые он отметит, и прочитай текст вслух.",
        "checklist": ["начало: обращение к читателям блога (Bonjour à tous !)", "все 5 частей: avant, ma vie là-bas, le départ, le premier jour, aujourd’hui",
                      "фон в imparfait, события в passé composé", "минимум две связки: d’abord, ensuite, alors, mais, enfin",
                      "il y a / depuis / pendant хотя бы по разу", "концовка: что ты чувствуешь сейчас", "от 120 до 150 слов"],
    },
    "wrap": {"task": "Итог юнита. Отметь, что получается, — честно, без спешки. Что пока не получается, повтори на следующей неделе.",
             "unit": True,
             "can": ["прочитать свой текст недели вслух без запинок"]},
})

# Le Petit Prince, главы 16–17 (12–15 берутся из reading_quiz.py: в октябре 31.10 был пропущен).
PP_16_17 = {
    "gloss": [["la Terre", "Земля"], ["un milliard", "миллиард"], ["un ballet", "балет"], ["le sable", "песок"],
              ["seul", "одинокий, один"], ["un navire", "корабль"], ["un anneau", "кольцо"], ["regretter", "скучать, сожалеть"]],
    "quiz": [
        C("Глава 16. Какой была седьмая планета?", ["Земля", "Марс", "астероид B 612"]),
        C("Кого, по словам рассказчика, на Земле очень много?", ["взрослых: королей, географов, деловых людей, пьяниц, честолюбцев", "цветов и барашков", "лётчиков"]),
        C("Глава 17. Кого принц первым встретил на Земле?", ["змею", "лиса", "лётчика"]),
        C("Где он оказался?", ["в пустыне, в Африке", "в большом городе", "на острове"]),
        C("Что змея говорит о людях?", ["среди людей тоже одиноко", "люди очень добрые", "людей на Земле нет"]),
    ],
}
