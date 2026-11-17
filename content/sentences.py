# -*- coding: utf-8 -*-
"""Полная французская фраза из задания — ключ для перевода в translations.py.

Пропуск «___» заполняется правильным ответом («fai___» + «te» → «faite»), из выбора берётся
верный вариант, у диктовки и аудирования — то, что звучит. Задания с русским текстом в вопросе
и схемы вида «nous finissons → je ___» фразой не считаются и перевода не получают.
"""
import re

CYR = re.compile(r"[А-Яа-яЁё]")


def fill(q, a):
    if re.search(r"\w___", q):
        s = re.sub(r"(\w)___", lambda m: m.group(1) + a, q, count=1)
    else:
        i = q.index("___")
        if re.search(r"(^|[.!?]\s+)$", q[:i]):
            a = a[:1].upper() + a[1:]
        rest = q[i + 3:]
        if a.endswith(("’", "'")):
            rest = rest.lstrip()
        s = q[:i] + a + rest
    s = re.sub(r"\s+\.$", ".", s)
    return s[:1].upper() + s[1:]


def full_sentence(ex):
    s = _sentence(ex)
    # «7:45 —», «Soixante et onze = 71» — задания на числа, а не фразы.
    return None if s is None or re.search(r"=|—\s*$", s) else s


def _sentence(ex):
    t = ex["type"]
    if t in ("dictation", "listen"):
        return ex.get("say")
    if t in ("transform", "order"):
        return ex["a"][0]
    q = re.sub(r"^TCF · ", "", ex.get("q") or "")
    if "→" in q or CYR.search(q):
        return None
    if t == "gap" and "___" in q:
        return fill(q, ex["a"][0])
    if t == "choice":
        return fill(q, ex["o"][ex["a"]]) if "___" in q else q
    return None
