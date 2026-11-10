# -*- coding: utf-8 -*-
"""Собирает public/data/reference.json — справочник для вкладки «Теория».

Запуск из корня проекта: python3 content/build_reference.py
Текст справочника — в content/reference.py.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reference import SECTIONS  # noqa: E402

OUT = os.path.join(HERE, "..", "public", "data", "reference.json")
TYPES = {"p", "h", "grid", "ex", "note", "line", "verbs"}

ids = [s["id"] for s in SECTIONS]
assert len(ids) == len(set(ids)), "id разделов повторяются"
for s in SECTIONS:
    for b in s["blocks"]:
        assert b["t"] in TYPES, (s["id"], b["t"])
        if b["t"] == "grid":
            n = len(b["head"])
            for r in b["rows"]:
                assert len(r) == n, (s["id"], b["head"][0], r)
            assert all(0 <= i < n for i in b["fr"]), (s["id"], b["head"])
        if b["t"] == "ex":
            assert all(len(x) == 2 for x in b["items"]), s["id"]

data = {"sections": SECTIONS}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

for s in SECTIONS:
    kinds = {}
    for b in s["blocks"]:
        kinds[b["t"]] = kinds.get(b["t"], 0) + 1
    print(s["id"], "·", s["title"], "·", ", ".join(f"{k} {v}" for k, v in kinds.items()))
print("глаголов в карточках:", sum(len(b["items"]) for s in SECTIONS for b in s["blocks"] if b["t"] == "verbs"))
