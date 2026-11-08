"""Pixabay fetch + v12 stock assignment: mock HTTP only, no network, no real key."""
import json
import subprocess
import urllib.error

from core import pixabay_fetch as PX
from core import stock_assign as SA
from core import stock_common as SC


def _cfg():
    cfg = SC.load_cfg()
    cfg["eye_rejects"] = {}
    cfg["eye_ok"] = {}
    cfg["pixabay"]["require_eye_ok"] = False
    return cfg


def _hit(i, tags, dur=10, w=1920, ai=False, lq=False):
    return {"id": i, "pageURL": f"https://pixabay.com/videos/id-{i}/", "tags": tags, "duration": dur, "user": f"user{i}",
            "user_id": 100 + i, "isAiGenerated": ai, "isLowQuality": lq, "downloads": 1000 - i, "likes": 1,
            "videos": {"large": {"url": f"https://cdn.pixabay.com/video/{i}_large.mp4", "width": w, "height": w * 9 // 16,
                                 "size": 1000, "thumbnail": f"https://cdn.pixabay.com/video/{i}_large.jpg"},
                       "tiny": {"url": f"https://cdn.pixabay.com/video/{i}_tiny.mp4", "width": 640, "height": 360,
                                "size": 10, "thumbnail": ""}}}


def _fake(hits, calls):
    def get(url):
        calls.append(url)
        if "pixabay.com/api" in url:
            return json.dumps({"total": len(hits), "totalHits": len(hits), "hits": hits}).encode()
        return ("MEDIA" + url).encode()
    return get


def test_query_url_uses_placeholder_never_a_key():
    u = PX.query_url("sea waves", _cfg(), "video")
    assert u.startswith("https://pixabay.com/api/videos/?key=__SAVED_KEY__&") and "q=sea+waves" in u
    assert PX.query_url("sea", _cfg(), "image").startswith("https://pixabay.com/api/?key=__SAVED_KEY__&")


def test_check_rejects_wrong_place_ai_people_landmark_and_size():
    cfg = _cfg()
    v = lambda h: PX.parse_hits({"hits": [h]})[0]  # noqa: E731
    assert "wrong place" in PX.check(v(_hit(1, "market, souq, kuwait")), cfg)
    assert "wrong place" in PX.check(v(_hit(2, "beach, alibaug, mumbai")), cfg)
    assert "wrong place" in PX.check(v(_hit(3, "temple, iskcon bangalore")), cfg)
    assert "wrong place" in PX.check(v(_hit(4, "temple, kyoto, japan")), cfg)
    assert "AI-generated" in PX.check(v(_hit(5, "sea", ai=True)), cfg)
    assert "identifiable-person" in PX.check(v(_hit(6, "sea, girl, portrait")), cfg)
    assert "landmark" in PX.check(v(_hit(7, "sea, mosque, minaret")), cfg)
    assert "rendition" in PX.check(v(_hit(8, "sea waves", w=1280)), cfg)
    assert "duration" in PX.check(v(_hit(9, "sea waves", dur=60)), cfg)
    assert PX.check(v(_hit(10, "sea, waves, water")), cfg) is None


def test_rank_prefers_4_to_15_seconds():
    cfg = _cfg()
    hs = PX.parse_hits({"hits": [_hit(1, "sea", dur=28), _hit(2, "sea", dur=8), _hit(3, "sea", dur=3)]})
    assert [h["id"] for h in PX.rank(hs, cfg)][0] == 2


def test_rate_limiter_100_per_60s():
    t = [0.0]
    slept = []
    lim = SC.RateLimiter(100, 60.0, clock=lambda: t[0], sleep=lambda d: (slept.append(d), t.__setitem__(0, t[0] + d)))
    for _ in range(100):
        lim.wait()
    assert not slept
    lim.wait()
    assert slept and 59.9 < slept[0] <= 60.1


def test_fetch_caches_24h_and_writes_credits(tmp_path):
    calls = []
    hits = [_hit(1, "sea, waves", dur=12), _hit(2, "souq, kuwait, sea"), _hit(3, "sea, ocean", dur=9, ai=True)]
    q = [{"theme": "sea_waves", "query": "sea waves", "kind": "video"}]
    r = PX.fetch(q, tmp_path / "px", cfg=_cfg(), get=_fake(hits, calls), download_get=_fake(hits, calls), per_query=3)
    assert r["fetched"] == 1 and r["api_requests"] == 1
    cred = json.loads((tmp_path / "px" / "CREDITS.json").read_text(encoding="utf-8"))[0]
    assert cred["licence"] == "Pixabay Content License" and cred["licence_family"] == "PIXABAY_CL"
    assert cred["label"] == "representative" and cred["author"] == "user1" and cred["source_page"].endswith("id-1/")
    txt = (tmp_path / "px" / "CREDITS.txt").read_text(encoding="utf-8")
    assert "NOT Creative Commons" in txt and "__SAVED_KEY__" not in txt
    r2 = PX.fetch(q, tmp_path / "px", cfg=_cfg(), get=_fake(hits, calls), download_get=_fake(hits, calls), per_query=3)
    assert r2["api_requests"] == 0 and r2["cache_hits"] == 1  # 24 h response cache
    for p in (tmp_path / "px" / "_cache").rglob("*.json"):
        assert "__SAVED_KEY__" in p.read_text(encoding="utf-8")  # placeholder only, never a real key


def test_require_eye_ok_downloads_only_looked_at_items(tmp_path):
    calls = []
    cfg = _cfg()
    cfg["pixabay"]["require_eye_ok"] = True
    cfg["eye_ok"] = {"pixabay:2": "ok"}
    hits = [_hit(1, "sea"), _hit(2, "sea"), _hit(3, "sea")]
    r = PX.fetch([{"theme": "sea_waves", "query": "sea", "kind": "video"}], tmp_path / "px", cfg=cfg,
                 get=_fake(hits, calls), download_get=_fake(hits, calls), per_query=3)
    assert r["fetched"] == 1 and json.loads((tmp_path / "px" / "CREDITS.json").read_text(encoding="utf-8"))[0]["pixabay_id"] == 2


def test_verify_auth_reports_status_without_key():
    def bad(url):
        raise urllib.error.HTTPError(url, 400, "Bad Request", {}, None)
    a = PX.verify_auth(_cfg(), get=bad, kind="image")
    assert a["auth"] == "FAIL" and a["http"] == 400
    ok = PX.verify_auth(_cfg(), get=lambda u: json.dumps({"totalHits": 5, "hits": []}).encode(), kind="video")
    assert ok == {"kind": "video", "http": 200, "auth": "PASS", "total_hits": 5}


# --------------------------------------------------------------------------- v12 assignment (pure function)
def _rows():
    def r(b, s, e, role, asset, match, text=""):
        return {"beat": b, "scene": "S21", "start": s, "end": e, "first_word_time": s, "text": text, "asset": asset,
                "source_dir": "assets/x", "asset_source": "v9", "match": match, "role": role, "v9_shot": "S21.1",
                "licence": "CC BY-SA", "title": "", "source_page": "", "notes": ""}
    return [r("S21_b01", 0.0, 4.0, "v9_shot", "S21_1_view_of_dwarka.jpg", "representative"),
            r("S21_b02", 4.0, 8.0, "continued_with_motion", "S21_1_view_of_dwarka.jpg", "representative", "बजट"),
            r("S21_b03", 8.0, 12.0, "continued_with_motion", "S21_1_view_of_dwarka.jpg", "representative", "ट्रेन टिकट"),
            r("S21_b04", 12.0, 16.0, "continued_with_motion", "S21_1_view_of_dwarka.jpg", "representative", "कमेंट"),
            r("S10_b01", 16.0, 20.0, "v9_shot", "S10_1_bhadkeshwar_mahadev_temple.jpg", "exact"),
            r("S10_b02", 20.0, 24.0, "continued_with_motion", "S10_1_bhadkeshwar_mahadev_temple.jpg", "exact", "सागर")]


def _pool():
    def p(key, src, kind, theme=None, title="", dur=None):
        return {"key": key, "source": src, "kind": kind, "theme": theme, "title": title, "text": title, "file": key + ".x",
                "dir": "/tmp", "licence": "L", "source_page": "", "duration": dur}
    return [p("pixabay:1", "pixabay", "video", "train_india", "Pixabay video 1: rails", 10),
            p("pixabay:2", "pixabay", "video", "sky_clouds", "Pixabay video 2: clouds", 10),
            p("pixabay:3", "pixabay", "video", "sea_waves", "Pixabay video 3: sea", 2.0),  # too short for a 4 s beat
            p("openverse:a", "openverse", "image", None, "Bhadkeshwar Mahadev Temple, Dwarka"),
            p("openverse:b", "openverse", "image", None, "Nageshwar temple Dwarka")]


def test_plan_stock_priority_caps_labels_no_repeat():
    from core import beats as B
    cfg = _cfg()
    cfg["assign"]["hold_cap_other_s"] = 4.5
    rows, dec = SA.plan_stock(_rows(), _pool(), cfg, B.load_rules(), {})
    by = {r["beat"]: r for r in rows}
    assert by["S21_b02"]["role"] == "continued_with_motion"  # held 4.0 s < cap 4.5: photo/parallax keeps it
    assert by["S21_b03"]["asset"] == "pixabay:1.x" and by["S21_b03"]["match"] == "representative"  # train theme
    assert by["S21_b04"]["asset"] == "pixabay:2.x"  # comment -> sky
    # exact shot: same-place Openverse photo (Bhadkeshwar) replaces at once, labelled exact; Nageshwar never used here
    assert by["S10_b02"]["asset"] == "openverse:a.x" and by["S10_b02"]["match"] == "exact"
    assert all(r["asset"] != "openverse:b.x" for r in rows)
    assert all(r["match"] == "representative" for r in rows if r["asset"].startswith("pixabay"))
    assert B.assign_qa([{k: v for k, v in r.items() if k != "_pick"} for r in rows])["pass"]


def test_plan_stock_photo_never_comes_back_after_stock():
    from core import beats as B
    cfg = _cfg()
    cfg["assign"]["hold_cap_other_s"] = 0.0
    pool = [p for p in _pool() if p["key"] == "pixabay:2"]
    rows, _ = SA.plan_stock(_rows()[:4], pool, cfg, B.load_rules(), {})
    assets = [r["asset"] for r in rows]
    assert assets == ["S21_1_view_of_dwarka.jpg", "pixabay:2.x", "pixabay:2.x", "pixabay:2.x"]
    assert B.assign_qa([{k: v for k, v in r.items() if k != "_pick"} for r in rows])["pass"]


def test_trim_video_frame_exact_no_audio(tmp_path):
    src = tmp_path / "src.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30:duration=6",
                    "-f", "lavfi", "-i", "sine=duration=6", "-shortest", "-c:v", "libx264", "-c:a", "aac", str(src)],
                   check=True)
    t = SA.trim_video(src, tmp_path / "out.mp4", 2.4, fps=25)
    assert t["frames"] == 60 and t["width"] == 1920 and t["height"] == 1080 and not t["has_audio"]
    assert abs(t["duration"] - 2.4) < 0.05
