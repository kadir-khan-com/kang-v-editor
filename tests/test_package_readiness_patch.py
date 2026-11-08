import unittest
from core.package_readiness import classify_package, timing_pending


class ReadinessTests(unittest.TestCase):
    def test_unaccepted_text_is_draft(self):
        r = classify_package({}, [], True)
        self.assertEqual(r["package_status"], "draft_package_ready")
        self.assertFalse(r["accepted"])

    def test_auto_scene_is_draft(self):
        r = classify_package({"transcript_accepted": True, "scene_plan_human_approved": False}, [], True)
        self.assertEqual(r["package_status"], "draft_package_ready")

    def test_interpolated_word_is_pending(self):
        status = {"transcript_accepted": True, "scene_plan_human_approved": True}
        r = classify_package(status, [{"timing_method": "interpolated_after_review"}], True)
        self.assertTrue(r["changed_word_timing_review_required"])
        self.assertEqual(r["package_status"], "draft_package_ready")

    def test_changed_word_verified_still_not_final_acceptance(self):
        status = {"transcript_accepted": True, "scene_plan_human_approved": True}
        r = classify_package(status, [{"timing_method": "interpolated_after_review", "timing_status": "human_verified"}], True)
        self.assertEqual(r["package_status"], "package_generated_pending_verification")
        self.assertFalse(r["accepted"])
        self.assertEqual(r["full_audio_sync"], "NOT_TESTED")

    def test_qa_failure_cannot_be_ready(self):
        r = classify_package({"transcript_accepted": True, "scene_plan_human_approved": True}, [], False)
        self.assertEqual(r["package_status"], "qa_failed")

    def test_original_asr_not_human_verified_by_default(self):
        r = classify_package({"transcript_accepted": True, "scene_plan_human_approved": True}, [{"timing_status": "asr"}], True)
        self.assertEqual(r["full_audio_sync"], "NOT_TESTED")
        self.assertFalse(r["accepted"])


if __name__ == "__main__":
    unittest.main()
