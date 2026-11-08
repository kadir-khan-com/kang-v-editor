import json

from core import commons_fetch as cf


def _api(pages):
    return json.dumps({"query": {"pages": pages}}).encode("utf-8")


def _page(i, title, lic, width=2000, mime="image/jpeg"):
    return {"index": i, "title": title, "imageinfo": [{"width": width, "height": 1200, "mime": mime, "sha1": str(i),
            "thumburl": f"https://up/{i}.jpg", "descriptionurl": f"https://c/{i}",
            "extmetadata": {"LicenseShortName": {"value": lic}, "LicenseUrl": {"value": "https://cc"},
                            "Artist": {"value": "<a href='x'>Ann &amp; Bo</a>"}, "ImageDescription": {"value": "Temple"},
                            "Categories": {"value": "Dwarka|Temples"}}}]}


def fake_get_factory(pages):
    def get(url):
        if url.startswith(cf.API):
            return _api(pages)
        return ("IMG" + url).encode()
    return get


def test_licence_family():
    assert cf.licence_family("CC BY-SA 4.0") == "CC BY-SA"
    assert cf.licence_family("CC BY 2.0") == "CC BY"
    assert cf.licence_family("CC0") == "CC0"
    assert cf.licence_family("Public domain") == "PD"
    assert cf.licence_family("CC BY-NC 2.0") == "RESTRICTED"
    assert cf.licence_family("CC BY-ND 4.0") == "RESTRICTED"
    assert cf.licence_family("") == "UNKNOWN"


def test_fetch_filters_and_writes_credits(tmp_path):
    pages = [_page(1, "File:A.jpg", "CC BY-SA 4.0"), _page(2, "File:B.jpg", "CC BY-NC 2.0"),
             _page(3, "File:C.jpg", "CC0", width=600), _page(4, "File:D.jpg", "Public domain"),
             _page(5, "File:E.tif", "CC BY 4.0", mime="image/tiff")]
    r = cf.fetch([{"scene": "S01", "query": "dwarka temple", "count": "3"}], str(tmp_path), get=fake_get_factory(pages))
    assert r["fetched"] == 2 and r["licence_families"] == {"CC BY-SA": 1, "PD": 1}
    reasons = " ".join(s["reason"] for s in r["skipped_detail"])
    assert "CC BY-NC" in reasons and "600" in reasons and "tiff" in reasons
    cred = json.loads((tmp_path / "CREDITS.json").read_text(encoding="utf-8"))
    assert cred[0]["author"] == "Ann & Bo" and cred[0]["rights_status"] == "recorded_not_cleared"
    assert cred[0]["file"].startswith("S01_1_") and (tmp_path / cred[0]["file"]).exists() and len(cred[0]["sha256"]) == 64
    assert "NOT cleared" in (tmp_path / "CREDITS.txt").read_text(encoding="utf-8")
    # second run: no duplicates
    r2 = cf.fetch([{"scene": "S01", "query": "dwarka temple"}], str(tmp_path), get=fake_get_factory(pages))
    assert r2["fetched"] == 0 and len(json.loads((tmp_path / "CREDITS.json").read_text(encoding="utf-8"))) == 2


def test_no_sharealike_and_dry_run(tmp_path):
    pages = [_page(1, "File:A.jpg", "CC BY-SA 4.0"), _page(2, "File:B.jpg", "CC BY 4.0")]
    r = cf.fetch([{"scene": "", "query": "x"}], str(tmp_path), no_sharealike=True, dry_run=True,
                 get=fake_get_factory(pages))
    assert r["fetched"] == 1 and r["licence_families"] == {"CC BY": 1}
    assert not (tmp_path / "CREDITS.json").exists()


def test_plan_queries(tmp_path):
    sc = tmp_path / "s.json"
    sc.write_text(json.dumps({"scenes": [{"id": "S01", "title": "t", "text": "द्वारिकाधीश मंदिर गोमती नदी"},
                                          {"id": "S02", "title": "t", "text": "कुछ नहीं"}]}, ensure_ascii=False),
                  encoding="utf-8")
    r = cf.plan_queries(str(sc), str(tmp_path / "q.csv"), place="Dwarka")
    rows = cf.read_queries(str(tmp_path / "q.csv"))
    assert r["scenes"] == 2 and rows[0]["scene"] == "S01"
    assert rows[0]["query"].startswith("Dwarka") and "dwarkadhish" in rows[0]["query"] and "gomti" in rows[0]["query"]


def test_broadens_query_when_no_hits(tmp_path):
    seen = []

    def get(url):
        if url.startswith(cf.API):
            seen.append(url)
            return _api([_page(1, "File:A.jpg", "CC0")]) if "gsrsearch=a+filetype" in url else b'{"batchcomplete":true}'
        return b"IMG"
    r = cf.fetch([{"scene": "S1", "query": "a b c", "count": "1"}], str(tmp_path), get=get)
    assert r["fetched"] == 1 and len(seen) == 3
    assert json.loads((tmp_path / "CREDITS.json").read_text(encoding="utf-8"))[0]["query_used"] == "a"


def test_download_errors_recorded_and_abort(tmp_path):
    pages = [_page(i, f"File:{i}.jpg", "CC0") for i in range(1, 5)]

    def get(url):
        if url.startswith(cf.API):
            return _api(pages)
        raise RuntimeError("HTTP Error 429")
    r = cf.fetch([{"scene": "S1", "query": "q", "count": "3"}], str(tmp_path), get=get, max_errors=2)
    assert r["status"] == "FAIL" and r["aborted_after_errors"] and len(r["download_errors"]) == 2
    assert json.loads((tmp_path / "CREDITS.json").read_text(encoding="utf-8")) == []


def test_skip_3d_and_multiword_place(tmp_path):
    pages = [_page(1, "File:G21D02 Statue 3D.jpg", "CC0"), _page(2, "File:Temple.jpg", "CC0")]
    r = cf.fetch([{"scene": "S1", "query": "q", "count": "2"}], str(tmp_path), get=fake_get_factory(pages))
    assert r["fetched"] == 1 and "3D" in r["skipped_detail"][0]["reason"]
    sc = tmp_path / "s.json"
    sc.write_text(json.dumps({"scenes": [{"id": "S01", "title": "t", "text": "द्वारिकाधीश मंदिर गोमती नदी"}]},
                             ensure_ascii=False), encoding="utf-8")
    cf.plan_queries(str(sc), str(tmp_path / "q.csv"), place="Dwarka Gujarat")
    assert cf.read_queries(str(tmp_path / "q.csv"))[0]["query"] == "Dwarka Gujarat dwarkadhish gomti"


def test_pool_rank_phrase_beats_generic_and_talk_scene_empty():
    def c(t, lic="CC BY-SA 4.0"):
        return {"title": t, "licence": lic, "width": 2000, "mime": "image/jpeg", "description": "", "categories": [],
                "source_page": "u", "thumb": "u", "sha1": t, "author": "a", "licence_url": ""}
    pool = [c("File:Dwarka temple.jpg"), c("File:Bet Dwarka jetty.jpg"), c("File:Bet Dwaraka boat.jpg"),
            c("File:Bet Dwarka NC.jpg", "CC BY-NC 2.0")]
    scenes = [{"id": "S15", "text": "बेट द्वारिका एक टापू है"}, {"id": "S21", "text": "बजट कितना लगेगा"}]
    rk = cf.rank_pool(scenes, pool, per_scene=2)
    assert [x["title"] for x in rk["picks"]["S15"]] == ["File:Bet Dwarka jetty.jpg", "File:Bet Dwaraka boat.jpg"]
    assert rk["picks"]["S21"] == []
    assert rk["pool_free"] == 3


def test_standard_thumb_for_unscaled_original():
    u = "https://upload.wikimedia.org/wikipedia/commons/6/64/View_of_Dwarka_Gujarat.jpg?utm_source=x"
    assert cf.standard_thumb(u, 1500) == ("https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/"
                                         "View_of_Dwarka_Gujarat.jpg/1280px-View_of_Dwarka_Gujarat.jpg")
    t = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/a.jpg/1920px-a.jpg"
    assert cf.standard_thumb(t, 4000) == t and cf.standard_thumb(u, 1000) == u
