"""Openverse fetch (v12): mock HTTP only, no network."""
import io
import json
import urllib.error

from PIL import Image, ImageDraw

from core import openverse_fetch as OV
from core import stock_common as SC


def _cfg(min_width=1600):
    cfg = SC.load_cfg()
    cfg["openverse"]["min_width"] = min_width
    cfg["eye_rejects"] = {}
    return cfg


def _img(w=2000, h=1200, seed=0):
    im = Image.new("RGB", (w, h), (20 + seed * 40 % 200, 90, 160))
    d = ImageDraw.Draw(im)
    for k in range(6):  # structure so dHash differs per seed
        x = (seed * 97 + k * 311) % w
        d.rectangle([x, (k * 150 + seed * 53) % h, x + 300, (k * 150 + seed * 53) % h + 200],
                    fill=((seed * 70 + k * 40) % 255, (k * 90) % 255, (seed * 30) % 255))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=90)
    return b.getvalue()


def _res(i, title, lic="by-sa", width=2400, tags=(), source="wikimedia"):
    return {"id": f"id{i}", "title": title, "url": f"https://img.example/{i}.jpg",
            "foreign_landing_url": f"https://landing.example/{i}", "creator": f"Ann {i}", "creator_url": "https://u",
            "license": lic, "license_version": "4.0", "license_url": f"https://creativecommons.org/licenses/{lic}/4.0/",
            "provider": source, "source": source, "filetype": "jpg", "tags": [{"name": t} for t in tags],
            "mature": False, "width": width, "height": 1500}


def _api(results):
    return json.dumps({"result_count": len(results), "page_count": 1, "results": results}).encode()


def _fake(results, calls, img_w=2000):
    def get(url):
        calls.append(url)
        if url.startswith("https://api.openverse.org"):
            return _api(results)
        i = int(url.rsplit("/", 1)[1].split(".")[0])
        return _img(w=img_w, seed=i)
    return get


def test_query_url_licence_filter_and_page_size():
    u = OV.query_url("dwarka", _cfg())
    assert "license=by%2Cby-sa%2Ccc0%2Cpdm" in u and "page_size=20" in u and "key=" not in u


def test_check_rejects_licence_size_and_wrong_places():
    cfg = _cfg()
    p = lambda r: OV.parse_results({"results": [r]})[0]  # noqa: E731
    assert "licence" in OV.check(p(_res(1, "Dwarka temple", lic="by-nc")), cfg)
    assert "width" in OV.check(p(_res(2, "Dwarka temple", width=900)), cfg)
    assert "wrong place" in OV.check(p(_res(3, "Dwarkadhish temple Mathura")), cfg)
    assert "wrong place" in OV.check(p(_res(4, "Dwarka Sector 21 Metro Station")), cfg)
    assert "wrong place" in OV.check(p(_res(5, "DSS Academy Dwarka")), cfg)
    assert "wrong place" in OV.check(p(_res(6, "Krishna temple", tags=["vrindavan"])), cfg)
    assert "wrong place" in OV.check(p(_res(7, "Shivrajpur - National Highway 76 - Allahabad")), cfg)
    assert "Dwarka-area cue" in OV.check(p(_res(8, "Beautiful temple at sunset")), cfg)
    assert OV.check(p(_res(9, "Bhadkeshwar Mahadev Temple, Dwarka")), cfg) is None


def test_min_width_is_configurable():
    r = OV.parse_results({"results": [_res(1, "Dwarka beach", width=1700)]})[0]
    assert OV.check(r, _cfg(1600)) is None
    assert "width" in OV.check(r, _cfg(2000))


def test_fetch_downloads_credits_and_rejects(tmp_path):
    calls = []
    res = [_res(1, "Bhadkeshwar Mahadev Temple, Dwarka"), _res(2, "Dwarka Sector 9 metro station (Delhi)"),
           _res(3, "Dwarka beach", lic="by-nd"), _res(4, "Gomti ghat Dwarka", lic="cc0")]
    r = OV.fetch([{"scene": "S10", "query": "dwarka", "count": 5}], tmp_path / "ov", cfg=_cfg(),
                 get=_fake(res, calls), pause_s=0)
    assert r["fetched"] == 2 and r["status"] == "PASS"
    cred = json.loads((tmp_path / "ov" / "CREDITS.json").read_text(encoding="utf-8"))
    assert {c["licence"] for c in cred} == {"CC BY-SA 4.0", "CC0"}
    for c in cred:
        assert c["source"] == "openverse" and c["label"] == "representative" and c["author"] and c["licence_url"]
        assert c["source_page"].startswith("https://landing.example/") and c["sha256"] and c["dhash"]
        assert (tmp_path / "ov" / c["file"]).is_file()
    rej = json.loads((tmp_path / "ov" / "rejected.json").read_text(encoding="utf-8"))
    reasons = " ".join(x["reason"] for x in rej)
    assert "wrong place" in reasons and "not in by/by-sa/cc0/pdm" in reasons
    assert "CC BY-SA 4.0" in (tmp_path / "ov" / "CREDITS.txt").read_text(encoding="utf-8")


def test_cache_24h_second_run_makes_no_api_call(tmp_path):
    calls = []
    res = [_res(1, "Bhadkeshwar Mahadev Temple, Dwarka")]
    OV.fetch([{"scene": "S10", "query": "bhadkeshwar", "count": 1}], tmp_path / "ov", cfg=_cfg(), get=_fake(res, calls),
             pause_s=0)
    n_api = sum(1 for u in calls if "api.openverse.org" in u)
    r2 = OV.fetch([{"scene": "S10", "query": "bhadkeshwar", "count": 1}], tmp_path / "ov", cfg=_cfg(),
                  get=_fake(res, calls), pause_s=0)
    assert n_api == 1 and sum(1 for u in calls if "api.openverse.org" in u) == 1
    assert r2["http"]["bhadkeshwar"] == ["cache"]


def test_dedupe_sha256_and_perceptual_against_pool(tmp_path):
    pool = tmp_path / "pool"
    pool.mkdir()
    (pool / "same.jpg").write_bytes(_img(seed=1))  # exact same bytes as result 1
    im = Image.open(io.BytesIO(_img(seed=2))).resize((1280, 768))  # resized copy of result 2
    im.save(pool / "resized.jpg", quality=70)
    calls = []
    res = [_res(1, "Dwarka temple one"), _res(2, "Dwarka temple two"), _res(3, "Dwarka temple three")]
    r = OV.fetch([{"scene": "S01", "query": "dwarka", "count": 5}], tmp_path / "ov", cfg=_cfg(),
                 get=_fake(res, calls), pause_s=0, pool_dirs=[pool])
    rej = json.loads((tmp_path / "ov" / "rejected.json").read_text(encoding="utf-8"))
    stages = {x["openverse_id"]: x["stage"] for x in rej}
    assert stages.get("id1") == "sha256" and stages.get("id2") == "dhash"
    assert r["fetched"] == 1


def test_known_commons_title_is_skipped(tmp_path):
    calls = []
    res = [_res(1, "Dwarka 1")]
    r = OV.fetch([{"scene": "S01", "query": "dwarka", "count": 1}], tmp_path / "ov", cfg=_cfg(), get=_fake(res, calls),
                 pause_s=0, known_titles=["File:Dwarka 1.jpg"])
    assert r["fetched"] == 0 and not any("img.example" in u for u in calls)


def test_429_uses_seed_and_says_so(tmp_path):
    seed = tmp_path / "ov" / "_seed"
    seed.mkdir(parents=True)
    (seed / "openverse_dwarka.json").write_text(json.dumps(
        {"_provenance": "test", "query": "dwarka", "data": {"result_count": 1, "page_count": 1,
                                                          "results": [_res(1, "Gomti ghat Dwarka")]}}), encoding="utf-8")

    def get(url):
        if "api.openverse.org" in url:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)
        return _img(seed=1)
    r = OV.fetch([{"scene": "S06", "query": "dwarka", "count": 1}], tmp_path / "ov", cfg=_cfg(), get=get, pause_s=0)
    assert r["http"]["dwarka"] == [429, "seed_webfetch"] and r["fetched"] == 1 and r["status"] == "WARN"
    assert not list((tmp_path / "ov" / "_cache").rglob("*.json"))  # seeds are never cached


def test_wikimedia_original_gets_1920_thumb():
    c = {"url": "https://upload.wikimedia.org/wikipedia/commons/9/94/Bhadkeshwar_Mahadev_Temple%2C_Dwarka.jpg",
         "width": 5568}
    assert OV.download_url(c, _cfg()).endswith("/thumb/9/94/Bhadkeshwar_Mahadev_Temple%2C_Dwarka.jpg/1920px-"
                                               "Bhadkeshwar_Mahadev_Temple%2C_Dwarka.jpg")
