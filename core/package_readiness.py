"""Separate package generation from human acceptance. No media/model execution."""
import json
from pathlib import Path


def timing_pending(words):
    return [i for i, word in enumerate(words)
            if word.get("timing_status") == "unverified"
            or (word.get("timing_method") == "interpolated_after_review"
                and word.get("timing_status") not in {"verified", "human_verified", "aligned_verified"})]


def classify_package(status, words, qa_pass):
    pending = timing_pending(words)
    if not qa_pass:
        state = "qa_failed"
    elif (not status.get("transcript_accepted", False)
          or not status.get("scene_plan_human_approved", False) or pending):
        state = "draft_package_ready"
    else:
        state = "package_generated_pending_verification"
    return {
        "package_status": state,
        "text_accepted": bool(status.get("transcript_accepted", False)),
        "changed_word_timing_review_required": bool(pending),
        "timing_unverified_word_indices": pending,
        "full_audio_sync": "NOT_TESTED",
        "accepted": False,
        "acceptance_scope": "generation_only; final QA/import/visual evidence required",
    }


def finalize_package_readiness(run, result, package_dir, words, report):
    manifest_path = Path(package_dir) / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    status = manifest.setdefault("status", {})
    readiness = classify_package(status, words, bool(report.get("pass", False)))
    status.update(readiness)
    tmp = manifest_path.with_name(manifest_path.name + ".tmp")
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(manifest_path)
    result.update(readiness)
    result["processing_complete"] = True
    run.manifest["package_readiness"] = readiness
    run.set_status(readiness["package_status"])
    run.add_output(manifest_path, "package_manifest")
