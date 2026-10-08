# -*- coding: utf-8 -*-
"""Собирает data/month1.json: расписание из xlsx + контент дней.

Запуск: python3 content/build_data.py  (из корня проекта; нужен openpyxl)
Результат: public/data/month1.json
"""
import json, re, os
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
# Таблица плана лежит рядом (content/plan.xlsx); путь можно переопределить переменной PLAN_XLSX.
XLSX = os.environ.get("PLAN_XLSX") or os.path.join(HERE, "plan.xlsx")
OUT = os.path.join(HERE, "..", "public", "data", "month1.json")

PIMSLEUR = "https://drive.google.com/drive/folders/1b5_nBYan7rJt0qyTf-kOKC_jps3y8en7"
SIM = "https://apprendre.tv5monde.com/fr/tcf/simulation-du-tcf"
PETIT_PRINCE = "https://www.ebooksgratuits.com/pdf/st_exupery_le_petit_prince.pdf"
SPOTIFY = "https://open.spotify.com/playlist/0A2qCpZ6J0nnY8osSAMzku"

# innerFrench: проверено поиском YouTube 25.09.2026
INNER = {
    1: ("MHoDEP-rF4c", "E01 Apprendre le français naturellement", "28:15"),
    2: ("7AN9sOz7aKQ", "E02 Vivre avec des robots", "29:26"),
    3: ("7F9_g5Je7IQ", "E03 Les pays les plus heureux du monde", "27:55"),
    4: ("inLWWqEAM3I", "E04 La théorie du genre", "31:37"),
    5: ("8GZI272O4u8", "E05 Le nouveau Président français", "32:44"),
    6: ("9rSS3DKctX8", "E06 Les avantages cachés de l’apprentissage d’une langue", "29:07"),
    7: ("NGFUl2W_XYo", "E07 Les théories du complot", "33:04"),
    8: ("TyDeoPtRI5I", "E08 La vérité sur les Français", "29:04"),
    9: ("ub9ZNmMawLA", "E09 La décroissance", "30:52"),
    10: ("qyT269VhDeA", "E10 L’expérience de Milgram", "32:27"),
}
# Super Easy French под тему дня (проверено поиском YouTube 25.09.2026)
SEF = {
    "01": ("fq_4V-Ia1z0", "Super Easy French 1 — for absolute beginners", "5:00"),
    "02": ("tCd_4uCD5eo", "How To Introduce Yourself in French · Super Easy French 196", "6:58"),
    "05": ("__Cu2nwgAjA", "100 French Words, Expressions & Sentences Every Beginner Should Know · SEF 151", "14:04"),
    "06": ("aMx0d42wzBs", "Everyday Conversation In Slow French · SEF 161", "7:22"),
    "07": ("_9hbPW7tbLU", "Taking a Train From Paris to Brussels · SEF 170", "7:15"),
    "08": ("stJ-_TRSbQE", "50 Real Life Sentences with the Verb “Pouvoir” · SEF 190", "11:30"),
    "09": ("5mutmziGppo", "Stop Making These Beginners’ Mistakes in French! · SEF 157", "11:01"),
    "12": ("tcF32PewZqY", "Morning Routine in Slow French · SEF 158", "8:44"),
    "13": ("2l7akQYoxZE", "Talking About Hobbies in Slow French · SEF 184", "9:30"),
    "14": ("g8oOzEYCfs8", "20 Most Common French Adjectives · SEF 178", "7:39"),
    "15": ("OcK-23KTX58", "Morning routines · Super Easy French 15", "4:38"),
    "16": ("QfK3NVD3cYg", "Time in French: Explanations & Real-Life Examples · SEF 182", "10:15"),
    "19": ("MGihIbHXCQ8", "How To Count in French From 1 to 99 · SEF 195", "8:07"),
    "20": ("zqF32466pDM", "How To Name And Describe Clothes… in French · SEF 146", "10:47"),
    "21": ("UXMB6Ms_2Uw", "House Vocabulary For Beginners in French · SEF 128", "8:39"),
    "22": ("cBNeZ6RWWZQ", "Directions, locations, movement · Super Easy French 60", "4:34"),
    "23": ("VidF6hKAiZo", "Slow French Conversation: Making Plans · SEF 175", "5:50"),
}
SONGS_Q = {
    "03": "Stromae Papaoutai", "10": "Angèle Balance ton quoi", "17": "Angèle Balance ton quoi",
    "24": "Édith Piaf La vie en rose", "31": "Stromae Alors on danse",
}

def yt(vid):
    return f"https://www.youtube.com/watch?v={vid}"

def yts(q):
    from urllib.parse import quote_plus
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)

wb = load_workbook(XLSX)
ws = wb["Месяц 1"]
days = []
for r in range(2, 33):
    date, wd, typ, mins, b1, b2, b3, res, det = [ws.cell(r, c).value for c in range(1, 10)]
    link = ws.cell(r, 8).hyperlink.target if ws.cell(r, 8).hyperlink else None
    d = date.strftime("%Y-%m-%d")
    dd = date.strftime("%d")
    day = {"date": d, "type": typ, "minutes": mins, "plan": {"b1": b1 or "", "b2": b2 or "", "b3": b3 or "", "details": det or "", "resource": res or "", "resourceUrl": link}}
    steps = []
    wdn = date.weekday()
    pims = re.search(r"Pimsleur French (I{1,3}|IV|V),? (уроки? [\d–]+)", (b2 or "") + " " + (b3 or ""))
    pim = {"kind": "pimsleur", "title": "Pimsleur", "url": PIMSLEUR,
           "lessons": f"French {pims.group(1)}, {pims.group(2)}" if pims else ""}
    inner = re.search(r"innerFrench, эпизод (\d+) \(([^)]+)\)", b3 or "")
    listen_items = []
    if inner:
        n = int(inner.group(1)); vid, t, dur = INNER[n]
        first = "первое" in inner.group(2)
        listen_items.append({"src": "innerFrench", "title": t, "dur": dur, "url": yt(vid),
                             "task": "Первое прослушивание: не останавливай и не переводи. Понимать 10–30% — нормально, это и есть нужный уровень." if first
                             else "Повтор того же эпизода: слушай ещё раз и выпиши 10 новых слов в поле ниже."})
    if dd in SEF and "Super Easy French" in (b3 or ""):
        vid, t, dur = SEF[dd]
        listen_items.append({"src": "Easy French", "title": t, "dur": dur, "url": yt(vid),
                             "task": "Смотри с французскими субтитрами. Полезные фразы — в поле «Слова из эпизода»."})
    if typ == "выходной":
        steps = []
    elif typ == "лёгкий":
        steps = [
            {"kind": "review", "title": "Повторение", "min": 15},
            {"kind": "song", "title": "Песня", "min": 15, "song": SONGS_Q.get(dd, ""), "url": yts(SONGS_Q.get(dd, "")), "playlist": SPOTIFY,
             "task": "Спой песню прошлой недели. Если хочешь, вставь её текст ниже, и слова станут кликабельными."},
            {"kind": "listening", "title": "Подкаст для удовольствия", "min": 15, "items": [
                {"src": "innerFrench", "title": INNER[5][1], "dur": INNER[5][2], "url": yt(INNER[5][0]), "task": "Любой отрывок, без задач."}]},
        ]
    elif wdn == 5:  # суббота
        ch = re.search(r"главы ([\d–]+)", b2 or "")
        steps = [
            {"kind": "review", "title": "Повторение", "min": 10},
            {"kind": "song", "title": "Песня", "min": 30, "song": SONGS_Q.get(dd, ""), "url": yts(SONGS_Q.get(dd, "")), "playlist": SPOTIFY,
             "task": "Послушай, найди текст, разбери незнакомые слова и выучи припев. Вставь текст ниже, чтобы слова стали кликабельными."},
            {"kind": "reading", "title": "Le Petit Prince", "min": 40, "chapters": ch.group(1) if ch else "", "url": PETIT_PRINCE,
             "task": "Читай вслух. Нажимай на незнакомые слова и добавляй нужные в карточки."},
            {"kind": "film", "title": "Кино", "min": 40, "film": "Astérix et Obélix — мультфильм или фильм с французскими субтитрами",
             "url": yts("Astérix et Obélix film français"),
             "task": "Смотри с французскими субтитрами. 5–10 слов, которые услышала несколько раз, добавь в карточки."},
        ]
    elif d == "2026-10-30":
        steps = [
            {"kind": "review", "title": "Повторение", "min": 10},
            {"kind": "tcf", "title": "TCF: контрольная симуляция", "min": 110, "url": SIM,
             "task": "90 минут в реальных условиях, потом 20 минут разбора. Запиши результат и сравни с 1 октября."},
            dict(pim, min=30),
        ]
    elif typ == "разгрузка":
        steps = [
            {"kind": "review", "title": "Повторение", "min": 10},
            {"kind": "theory", "title": "Теория", "min": 20},
            {"kind": "exercises", "title": "Упражнения", "min": 30},
            {"kind": "vocab", "title": "Словарь дня", "min": 15},
            dict(pim, min=30),
            {"kind": "listening", "title": "Аудирование", "min": 30, "items": listen_items},
            {"kind": "homework", "title": "Домашка", "min": 15},
        ]
    else:
        steps = [
            {"kind": "review", "title": "Повторение", "min": 10},
            {"kind": "theory", "title": "Теория", "min": 25},
            {"kind": "exercises", "title": "Упражнения", "min": 40},
            {"kind": "homework", "title": "Домашка", "min": 10},
            {"kind": "vocab", "title": "Словарь дня", "min": 20},
            dict(pim, min=60),
            {"kind": "listening", "title": "Аудирование", "min": 45, "items": listen_items},
        ]
    ORDER = ["review", "tcf", "theory", "vocab", "exercises", "listening", "pimsleur", "reading", "song", "film", "homework"]
    day["steps"] = sorted(steps, key=lambda st: ORDER.index(st["kind"]))
    day["ready"] = False
    days.append(day)

# ---------------- Контент уроков ----------------
from content_days import CONTENT as C0, LEXICON_EXTRA
from content_w1 import CONTENT as C1
from content_w2 import CONTENT as C2
from content_w3 import CONTENT as C3
from content_w4 import CONTENT as C4
from listening_quiz import INNER as LQ_INNER, SEF as LQ_SEF
from reading_quiz import READING
from urllib.parse import urlparse, parse_qs

CONTENT = {}
for part in (C0, C1, C2, C3, C4):
    CONTENT.update(part)

from drills import DRILLS

# Новое распределение времени: Pimsleur — 1 урок (30 мин), освободившееся время — на практику
MINUTES = {
    # Pimsleur — по желанию и не входит в минуты дня; его 30 минут ушли на практику
    "study": {"review": 25, "theory": 20, "vocab": 15, "exercises": 40, "drill": 35, "listening": 40, "homework": 35},
    "deload": {"review": 20, "theory": 15, "vocab": 10, "exercises": 30, "drill": 25, "listening": 25, "homework": 25},
    "2026-10-01": {"review": 0, "tcf": 90, "theory": 10, "vocab": 5, "exercises": 25, "drill": 25, "listening": 20, "homework": 35},
    "2026-10-02": {"review": 20, "theory": 20, "vocab": 15, "exercises": 40, "drill": 35, "listening": 40, "homework": 40},
}
FUN = {  # видео «для удовольствия»: проверено поиском YouTube 03.10.2026
    "2026-10-02": ("Oy_Ez-7kjIY", "FRENCH VLOG for French learners", "Piece of French", "4:27"),
    "2026-10-04": ("roxNeI1McwQ", "I speak ONLY French while cooking!", "Learn French With Justine", "7:33"),
    "2026-10-07": ("1yMv8gxsJqc", "A Summer Day in Paris · French Vlog", "Learn French With Justine", "8:19"),
    "2026-10-09": ("ofyFo4GCddc", "A Day in Paris · Slow French Vlog", "Adeline Talks", "10:23"),
    "2026-10-11": ("sMuyVaEy8I4", "My Morning Routine · Easy French Listening", "Learn French With Justine", "11:22"),
    "2026-10-14": ("XrqVl4jhl00", "What I Eat in a Day in France · Slow French Vlog", "Learn French With Justine", "15:14"),
    "2026-10-16": ("Zpcrn1b6baQ", "Days With Me in Slow French", "Piece of French", "14:30"),
    "2026-10-18": ("rYDxNFhAvTc", "Cook with Me in Slow French", "Piece of French", "26:50"),
    "2026-10-21": ("ylXpZDZxKEg", "A Day in My Life · Slow French Vlog", "Adeline Talks", "11:51"),
    "2026-10-23": ("hlmA1vM6iKA", "Apprends le français naturellement avec ce vlog", "Gaspard Français", "9:47"),
    "2026-10-25": ("CJq0x2bj-hk", "What I Eat in a Week in French · Slow French Vlog", "Piece of French", "16:08"),
    "2026-10-28": ("AJ364qdlxf4", "I Speak ONLY French While Packing", "Learn French With Justine", "12:10"),
}
ORDER2 = ["review", "tcf", "theory", "vocab", "exercises", "drill", "listening", "pimsleur", "reading", "song", "film", "homework"]

NEEDS = {"theory", "vocab", "exercises", "homework"}
for day in days:
    c = CONTENT.get(day["date"])
    if c:
        day.update({k: v for k, v in c.items() if k not in ("steps",)})
        if "steps" in c:
            day["steps"] = c["steps"]
    day["ready"] = bool(c) or not any(st["kind"] in NEEDS for st in day["steps"])
    if day["date"] in DRILLS:
        if not any(st["kind"] == "drill" for st in day["steps"]):
            day["steps"].append({"kind": "drill", "title": "Практикум", "min": 0})
        day["drill"] = [dict(x, id="D-%d" % n) for n, x in enumerate(DRILLS[day["date"]], 1)]
        mins = MINUTES.get(day["date"]) or MINUTES["deload" if day["type"] == "разгрузка" else "study"]
        for st in day["steps"]:
            if st["kind"] in mins:
                st["min"] = mins[st["kind"]]
        day["steps"].sort(key=lambda st: ORDER2.index(st["kind"]))
    for st in day["steps"]:
        if st["kind"] == "listening":
            for i, it in enumerate(st.get("items", [])):
                vid = parse_qs(urlparse(it["url"]).query).get("v", [""])[0]
                quiz, topic = None, False
                if vid in LQ_INNER:
                    quiz = LQ_INNER[vid]["repeat" if it["task"].startswith("Повтор") else "first"]
                elif vid in LQ_SEF:
                    q = LQ_SEF[vid]
                    if isinstance(q, dict):
                        quiz, topic = q["q"], True
                    else:
                        quiz = q
                if quiz and not st["title"].startswith("Подкаст для удовольствия"):
                    it["quiz"] = [dict(x, id="L%d-%d" % (i, n)) for n, x in enumerate(quiz, 1)]
                    it["topicQuiz"] = topic
        if st["kind"] == "reading" and st.get("chapters") in READING:
            r = READING[st["chapters"]]
            st["gloss"] = r["gloss"]
            st["quiz"] = [dict(x, id="R-%d" % n) for n, x in enumerate(r["quiz"], 1)]

pim_n = 0
for day in days:
    for st in day["steps"]:
        if st["kind"] == "pimsleur":
            ls = []
            for _ in range(2):
                pim_n += 1
                lvl, les = divmod(pim_n - 1, 30)
                ls.append([["I", "II", "III"][lvl], les + 1])
            st["list"] = ls
            st["lessons"] = " и ".join("French %s, урок %d" % (l, n) for l, n in ls)
            st["optional"] = True
            st["min"] = 60
            st.pop("level", None); st.pop("lesson", None)
    if day["date"] == "2026-10-30":
        for st in day["steps"]:
            if st["kind"] == "review":
                st["min"] = 40
    if day["date"] in FUN:
        vid, t, ch, dur = FUN[day["date"]]
        day["fun"] = {"url": "https://www.youtube.com/watch?v=" + vid, "title": t, "channel": ch, "dur": dur}

# лексикон для перевода по нажатию: формы → {lemma, ru}
lex = {}
for day in days:
    for w in day.get("vocab", []):
        for f in w.get("forms", []) + [w["fr"]]:
            lex.setdefault(f.lower(), {"lemma": w["fr"], "ru": w["ru"]})
for r in READING.values():
    for fr, ru in r["gloss"]:
        base = fr.split(" ", 1)[1] if fr.split(" ", 1)[0] in ("un", "une", "le", "la", "les", "des") and " " in fr else fr
        lex.setdefault(base.lower(), {"lemma": fr, "ru": ru})
lex.update({k: v for k, v in LEXICON_EXTRA.items() if k not in lex})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
data = {"month": 1, "start": "2026-10-01", "end": "2026-10-31", "days": days, "lexicon": lex,
        "unverified": ["Pimsleur: содержимое папки Francés не удалось просмотреть — номера уроков по стандартной структуре French I–V"]}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
ready = [d for d in days if d["ready"]]
def lq(d):
    return sum(len(it.get("quiz", [])) for st in d["steps"] for it in st.get("items", [])) + sum(len(st.get("quiz", [])) for st in d["steps"])
print("days", len(days), "ready", len(ready),
      "exercises", sum(len(d.get("exercises", [])) for d in days),
      "listening/reading quiz", sum(lq(d) for d in days),
      "words", sum(len(d.get("vocab", [])) for d in days), "topics", sum(len(d.get("topics", [])) for d in days), "lexicon", len(lex))
import collections
ids = collections.Counter(w["id"] for d in days for w in d.get("vocab", []))
print("dup vocab ids", [k for k, v in ids.items() if v > 1])
tids = collections.Counter(t["id"] for d in days for t in d.get("topics", []))
print("dup topic ids", [k for k, v in tids.items() if v > 1])
for d in days:
    if any(st["kind"] == "exercises" for st in d["steps"]):
        print(d["date"], d["type"], "ex", len(d.get("exercises", [])), "words", len(d.get("vocab", [])), "min", sum(st["min"] for st in d["steps"] if not st.get("optional")), "/", d["minutes"])
