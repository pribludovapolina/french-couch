# -*- coding: utf-8 -*-
"""Короткие конструкторы для контента уроков."""


def w(id, fr, ru, ex="", exRu="", g=None, forms=None):
    return {"id": "w-" + id, "fr": fr, "ru": ru, "g": g, "ex": ex, "exRu": exRu, "forms": forms or []}


def C(q, o, a=0):
    return {"type": "choice", "q": q, "o": o, "a": a}


def L(say, o, a=0, q="Что прозвучало?"):
    return {"type": "listen", "say": say, "q": q, "o": o, "a": a}


def G(q, ru, *a):
    return {"type": "gap", "q": q, "ru": ru, "a": list(a)}


def J(verb, rows, q=None):
    d = {"type": "conj", "verb": verb, "rows": [list(r) for r in rows]}
    if q:
        d["q"] = q
    return d


def M(q, pairs):
    return {"type": "match", "q": q, "pairs": [list(p) for p in pairs]}


def O(q, words, *a):
    return {"type": "order", "q": q, "words": list(words), "a": list(a)}


def D(say, *a):
    return {"type": "dictation", "say": say, "a": list(a) or [say]}


def T(q, *a):
    return {"type": "translate", "q": q, "a": list(a)}


def ex(*items):
    out = []
    for i, it in enumerate(items, 1):
        d = dict(it)
        d["id"] = "e%d" % i
        out.append(d)
    return out


def th(h, p, table=None, exs=None):
    d = {"h": h, "p": p}
    if table:
        d["table"] = [list(r) for r in table]
    if exs:
        d["ex"] = [list(r) for r in exs]
    return d


def topic(id, title, *quiz):
    return {"id": id, "title": title, "quiz": [{"q": q, "o": o, "a": 0} for q, o in quiz]}


def hw(task, example, minWords=15):
    return {"task": task, "example": example, "minWords": minWords}
