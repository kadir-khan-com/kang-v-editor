import csv
import json

from PIL import Image

from core import asset_index as ai, broll_match as bm
from core.visuals import validate

NOPROF = {"entities": [], "profiles": []}  # pure keyword matching, no scene profiles


def _setup(tmp_path):
    d = tmp_path / "lib"
    d.mkdir()
    names = ["nageshwar_shiva_statue.jpg", "nageshwar_temple_front.jpg", "gomti_ghat_steps.jpg",
             "bet_dwarka_boats.jpg", "dwarka_temple_town.jpg", "dwarka_sunset_beach.jpg"]
    for k, n in enumerate(names):  # distinct pixels -> distinct sha256 / asset_id
        Image.new("RGB", (1920, 1080), (40 * k, 90, 160)).save(d / n)
    (d / "CREDITS.json").write_text(json.dumps([{"file": n, "licence": "CC0", "author": "me"} for n in names]),
                                    encoding="utf-8")
    idx = json.loads(open(ai.ingest(d)["index"], encoding="utf-8").read())
    words = [{"word": w, "start": i, "end": i + 0.9} for i, w in enumerate(
        "नागेश्वर ज्योतिर्लिंग में शिव की प्रतिमा है गोमती घाट पर स्नान फिर बेट द्वारका नाव से हम आज बात करेंगे".split())]
    scenes = {"scenes": [
        {"id": "S01", "start": 0.0, "end": 6.0, "first_word": 0, "last_word": 6, "text": ""},
        {"id": "S02", "start": 6.0, "end": 10.0, "first_word": 7, "last_word": 11, "text": ""},
        {"id": "S03", "start": 10.0, "end": 14.0, "first_word": 12, "last_word": 14, "text": ""},
        {"id": "S04", "start": 14.0, "end": 18.0, "first_word": 15, "last_word": 19, "text": ""}],
        "duration": 18.0}
    return d, idx, words, scenes


def test_match_top3_reason_scores_and_pending(tmp_path):
    _, idx, words, scenes = _setup(tmp_path)
    sg = bm.match(scenes, idx, words, profiles=NOPROF)
    s1, s2, s3, s4 = sg["scenes"]
    assert s1["candidates"][0]["path"] == "nageshwar_shiva_statue.jpg" and "nageshwar" in s1["candidates"][0]["reason"]
    assert s2["candidates"][0]["path"] == "gomti_ghat_steps.jpg"
    assert s3["candidates"][0]["path"] == "bet_dwarka_boats.jpg"
    assert s4["matched_candidates"] == 0 and s4["needs_manual"] and s4["confidence"] == "none"
    assert all(s["approval_status"] == "awaiting_user" for s in sg["scenes"])
    assert all(0 < c["score"] <= 1 for s in sg["scenes"] for c in s["candidates"] if not c["fallback"])
    assert len({c["path"] for c in s1["candidates"]}) == len(s1["candidates"]) <= 3


def test_repeat_penalty_downranks_earlier_pick(tmp_path):
    _, idx, words, _ = _setup(tmp_path)
    w2 = words + [{"word": "नागेश्वर", "start": 30, "end": 31}, {"word": "मंदिर", "start": 31, "end": 32}]
    sc = {"scenes": [{"id": "S01", "start": 0, "end": 6, "first_word": 0, "last_word": 5},
                     {"id": "S02", "start": 6, "end": 8, "first_word": len(words), "last_word": len(words) + 1}]}
    sg = bm.match(sc, idx, w2)
    first = sg["scenes"][0]["candidates"][0]["path"]
    again = [c for c in sg["scenes"][1]["candidates"] if c["path"] == first]
    assert not again or "already #1" in again[0]["reason"]


def test_approve_writes_valid_visuals_csv_only_for_chosen(tmp_path):
    d, idx, words, scenes = _setup(tmp_path)
    sg = bm.match(scenes, idx, words, profiles=NOPROF)
    sp = tmp_path / "s.csv"
    bm.write_csv(sg, sp)
    rows = list(csv.DictReader(open(sp, encoding="utf-8-sig")))
    for r in rows:
        if r["scene"] in ("S01", "S02", "S03") and r["rank"] == "1":
            r["choose"] = "1"
        if r["scene"] == "S01" and r["rank"] == "2":
            r["choose"] = "x"
        if r["scene"] == "S04":
            r["choose"] = ""
    with open(sp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = bm.approve(sp, idx, tmp_path / "v.csv", scenes)
    assert not bad["ok"] and any("S04" in p for p in bad["problems"])
    ok = bm.approve(sp, idx, tmp_path / "v.csv", scenes, allow_missing=True)
    assert ok["ok"] and ok["shots"] == 4 and ok["scenes"] == 3
    from core.visuals import read_csv
    vr = read_csv(tmp_path / "v.csv")
    assert vr[1]["shot_start"] == "3.000"
    plan = dict(scenes, scenes=[dict(s, title=s["id"], word_count=1) for s in scenes["scenes"]])
    chk = validate(vr, plan, d)
    assert chk["ok"], chk["problems"]


def test_hit_at_k():
    sg = {"scenes": [{"scene_id": "S01", "confidence": "high", "candidates": [{"path": "a.jpg"}]},
                     {"scene_id": "S02", "confidence": "low", "candidates": [{"path": "b.jpg"}]}]}
    ev = bm.hit_at_k(sg, {"S01": {"a.jpg"}, "S02": {"z.jpg"}})
    assert ev["hits"] == 1 and ev["high_conf_hits"] == 1 and ev["high_conf_scenes"] == 1


def test_qa_fallback_fill_and_approve_broll_cli(tmp_path):
    import subprocess, sys
    d, idx, words, scenes = _setup(tmp_path)
    sg = bm.match(scenes, idx, words, profiles=NOPROF)
    q = bm.qa(sg, ["S01", "S02", "S03", "S04"])
    assert q["structure"] == "PASS" and q["coverage"] == "4/4" and q["scenes_with_3"] == "4/4"
    assert q["duplicate_in_scene"] == [] and q["auto_selected"] is False
    s4 = sg["scenes"][3]
    assert s4["matched_candidates"] == 0 and s4["confidence"] == "none" and all(c["fallback"] for c in s4["candidates"])
    assert len(q["fallback_candidates"]) >= 3
    with __import__("pytest").raises(ValueError):
        bm.choices_from_spec(sg, "S01=D")
    sp, ip, scp = tmp_path / "sg.json", tmp_path / "idx.json", tmp_path / "scenes.json"
    for p_, o in ((sp, sg), (ip, idx), (scp, scenes)):
        p_.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    r = subprocess.run([sys.executable, str(root / "kang.py"), "approve-broll", str(sp), str(ip), str(scp),
                        "--out", str(tmp_path / "v.csv"), "--choices", "S01=AB,S02=A,S03=C,S04=skip", "--allow-missing"],
                       capture_output=True, text=True, encoding="utf-8", cwd=root)
    assert r.returncode == 0, r.stdout + r.stderr
    ap = json.loads((tmp_path / "approved_broll.json").read_text(encoding="utf-8"))
    assert ap["approved_by"] == "user" and ap["skipped"] == ["S04"]
    assert ap["scenes"][0]["options"] == ["A", "B"]


def test_interactive_reprompts_on_bad_letter(tmp_path):
    _, idx, words, scenes = _setup(tmp_path)
    sg = bm.match(scenes, idx, words, profiles=NOPROF)
    answers = iter(["Z", "A", "", "b", "ac"])
    got = bm.interactive_choices(sg, ask=lambda _: next(answers), show=lambda *_: None)
    assert list(got) == ["S01", "S03", "S04"] and len(got["S04"]) == 2


def test_minor_entity_downweighted_and_outro_profile(tmp_path):
    _, idx, _, _ = _setup(tmp_path)
    cfg = {"entities": ["nageshwar", "gomti"], "secondary_entity_factor": 0.5, "profile_weight": 0.6,
           "profiles": [{"name": "outro", "position": "last", "any": ["सब्सक्राइब"], "prefer": ["sunset", "beach"]}]}
    w = [{"word": x} for x in "गोमती गोमती घाट मंदिर नागेश्वर मंदिर".split()] + \
        [{"word": x} for x in "वीडियो पसंद आए तो सब्सक्राइब करें".split()]
    sc = {"scenes": [{"id": "S01", "start": 0, "end": 6, "first_word": 0, "last_word": 5},
                     {"id": "S02", "start": 6, "end": 9, "first_word": 6, "last_word": 11}]}
    sg = bm.match(sc, idx, w, profiles=cfg)
    s1, s2 = sg["scenes"]
    assert s1["candidates"][0]["path"] == "gomti_ghat_steps.jpg"
    ng = [c for c in s1["candidates"] if c["path"].startswith("nageshwar")]
    assert ng and all("minor mention" in c["reason"] for c in ng)
    assert s2["profile"] == "outro" and s2["confidence"] == "profile" and s2["needs_manual"]
    assert s2["candidates"][0]["path"] == "dwarka_sunset_beach.jpg" and "profile:outro" in s2["candidates"][0]["reason"]
