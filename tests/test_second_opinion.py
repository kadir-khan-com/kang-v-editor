from core import second_opinion as so


def W(text, t0=0.0):
    return [{"word": t, "start": t0 + i, "end": t0 + i + 0.8} for i, t in enumerate(text.split())]


def test_hint_aligns_replacement_and_agreement():
    words = W("देखने क गंटों तक इंतजार करते हैं")
    al = so.align(words, [{"start": 0, "end": 100, "text": "देखने के लिए घंटों तक इंतजार करते हैं।"}])
    assert so.hint(al, 1, 2) == "के लिए घंटों"
    assert so.hint(al, 3, 3) == "तक"
    rows = so.annotate_rows([{"id": "R1", "first": "1", "last": "2"}, {"id": "R2", "first": "4", "last": "5"}], al, words)
    assert rows[0]["nemotron_agrees"] == "no" and rows[0]["nemotron_diff"] == "content"
    assert rows[1]["nemotron_agrees"] == "yes" and rows[1]["nemotron_diff"] == ""


def test_normalization_ignores_nukta_chandrabindu_punct():
    assert so.norm("यहाँ,") == so.norm("यहां") and so.norm("ज़रूर") == so.norm("जरूर")


def test_classify_kinds():
    assert so.classify("2,500,000 रुपये", "दो हजार से ढाई हजार रुपये") == "number"
    assert so.classify("railway station", "रेलवे स्टेशन") == "script"
    assert so.classify("कहा", "कहां") == "spelling"
    assert so.classify("बेड द्वारका", "मंदिर") == "content"
    assert so.classify("श्री कृष्ण", "श्रीकृष्ण") == "spacing"


def test_words_never_modified():
    words = W("आप आप ऑटो")
    before = [dict(w) for w in words]
    so.align(words, [{"start": 0, "end": 10, "text": "आप ऑटो"}])
    assert words == before
