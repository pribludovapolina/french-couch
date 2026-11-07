# -*- coding: utf-8 -*-
"""Собирает public/data/month2.json — ноябрь 2026 по модели «неделя = юнит».

Запуск из корня проекта: python3 content/build_month2.py
Октябрь собирает build_data.py в month1.json, его этот скрипт не трогает.

Отличия ноября от октября:
- день — урок в очереди (queue): «Сегодня» открывает первый незакрытый урок, а не дату из календаря;
- у дня есть unit и lesson («1.1»), описание юнита лежит в units;
- новые шаги: doc (документ дня), observe (наблюдение и правило), sprint (TCF-спринт на время),
  course (онлайн-курс TV5), wtext (текст недели), wrap (итог дня / Faites le point);
- новый тип упражнения piece — «кусок текста» для текста недели;
- Pimsleur и домашки-сочинения нет.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nov_w1 import UNIT as UNIT1, DAYS as W1, PP_16_17  # noqa: E402
from reading_quiz import READING  # noqa: E402

OUT = os.path.join(HERE, "..", "public", "data", "month2.json")
KINDS = {"review", "doc", "observe", "theory", "exercises", "sprint", "course", "listening", "wtext", "wrap", "tcf", "reading", "film"}

days = [dict(d) for d in W1]


def number(items, prefix, start=1):
    out = []
    for i, it in enumerate(items, start):
        it = dict(it)
        it["id"] = prefix + str(i)
        out.append(it)
    return out


for d in days:
    d["queue"] = True
    d["ready"] = True
    kinds = [s["kind"] for s in d["steps"]]
    assert len(kinds) == len(set(kinds)), (d["date"], "шаг одного вида дважды")
    assert set(kinds) <= KINDS, (d["date"], set(kinds) - KINDS)
    if d["type"] != "выходной":
        assert sum(s["min"] for s in d["steps"]) == d["minutes"], (d["date"], sum(s["min"] for s in d["steps"]), d["minutes"])
    if "warmup" in d:
        d["warmup"] = number(d["warmup"], "s")
    if "exercises" in d:
        d["exercises"] = number(d["exercises"], "e")
    if "sprint" in d:
        d["sprint"] = number(d["sprint"], "t")
    if "doc" in d:
        doc = d["doc"] = dict(d["doc"])
        if doc.get("pre"):
            doc["pre"] = dict(doc["pre"], id="d0")
        doc["quiz"] = number(doc.get("quiz", []), "d")
    if "observe" in d:
        d["observe"] = dict(d["observe"], qs=number(d["observe"]["qs"], "o"))
    if "wtext" in d:
        d["wtext"] = dict(d["wtext"], micro=number(d["wtext"].get("micro", []), "m"))
    for s in d["steps"]:
        if s["kind"] == "reading":
            src = READING["12–15"]
            quiz = [q for q in src["quiz"] if q["type"] == "choice"] + PP_16_17["quiz"] + [q for q in src["quiz"] if q["type"] != "choice"]
            s["gloss"] = src["gloss"] + PP_16_17["gloss"]
            s["quiz"] = number(quiz, "R-")

# Шаги, которые рендерят содержимое дня, должны его находить.
NEED = {"doc": "doc", "observe": "observe", "theory": "theory", "exercises": "exercises", "sprint": "sprint", "wtext": "wtext", "wrap": "wrap"}
for d in days:
    for s in d["steps"]:
        f = NEED.get(s["kind"])
        assert not f or d.get(f), (d["date"], s["kind"], "нет содержимого")

# Ссылки на куски прошлых дней в тексте недели должны существовать.
pieces = {(d["date"], e["id"]) for d in days for e in d.get("exercises", []) + d.get("wtext", {}).get("micro", []) if e["type"] == "piece"}
for d in days:
    for ref in d.get("wtext", {}).get("show", []):
        assert tuple(ref) in pieces, (d["date"], ref)

# Перевод по нажатию: фразы-чанки и словарик глав.
lex = {}
for d in days:
    for fr, ru in d.get("doc", {}).get("chunks", []):
        lex.setdefault(fr.lower().replace("’", "'"), {"lemma": fr, "ru": ru})
    for s in d["steps"]:
        for fr, ru in s.get("gloss", []):
            base = fr.split(" ", 1)[1] if " " in fr and fr.split(" ", 1)[0] in ("un", "une", "le", "la", "les", "des") else fr
            lex.setdefault(base.lower(), {"lemma": fr, "ru": ru})

data = {
    "month": 2, "title": "Ноябрь 2026", "start": days[0]["date"], "end": days[-1]["date"],
    "note": "Готова неделя 1: возвращение и юнит « Souvenirs ». Юниты 2 и 3 появятся до их начала.",
    "units": {"1": UNIT1}, "days": days, "lexicon": lex,
    "unverified": [],
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

ids = collections.Counter()
for d in days:
    for k in ("warmup", "exercises", "sprint"):
        for e in d.get(k, []):
            ids[(d["date"], e["id"])] += 1
print("дней", len(days), "· уроков", sum(1 for d in days if d.get("lesson")),
      "· упражнений", sum(len(d.get("exercises", [])) for d in days),
      "· спринт", sum(len(d.get("sprint", [])) for d in days),
      "· кусков текста", len(pieces), "· лексикон", len(lex))
for d in days:
    if d["type"] != "выходной":
        print(d["date"], d.get("lesson"), d["type"], sum(s["min"] for s in d["steps"]), "мин:", " → ".join(s["kind"] for s in d["steps"]))
