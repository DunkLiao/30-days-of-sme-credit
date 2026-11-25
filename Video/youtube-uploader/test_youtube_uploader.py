import json
import tempfile
import unittest
from pathlib import Path

from youtube_uploader import build_parser, validate_video, write_json


class UploaderSafetyTests(unittest.TestCase):
    def test_auth_can_request_new_account_selection(self):
        args = build_parser().parse_args(["auth", "--reauthorize"])
        self.assertTrue(args.reauthorize)

    def test_made_for_kids_must_be_json_boolean(self):
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / "Day01.mp4"
            video.write_bytes(b"video")
            item = {
                "day": 1,
                "topic": "授信原則",
                "title": "第 01 天｜授信原則",
                "description": "說明",
                "video_path": video,
                "thumbnail_path": None,
                "tags": [],
                "privacy_status": "public",
                "made_for_kids": "false",
            }
            self.assertTrue(any("made_for_kids" in error for error in validate_video(item)))
            item["made_for_kids"] = False
            self.assertEqual(validate_video(item), [])

    def test_missing_topic_is_reported_instead_of_crashing(self):
        from youtube_uploader import format_video

        item = format_video({"day": 1, "topic": None, "video": "../Day01.mp4"}, {"defaults": {"title": "第{day}天｜{topic}"}})
        self.assertTrue(any("topic" in error for error in validate_video(item)))

    def test_failed_state_serialization_keeps_previous_record(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "upload_state.json"
            write_json(path, {"01": {"video_id": "previous"}})
            with self.assertRaises(TypeError):
                write_json(path, {"invalid": object()})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["01"]["video_id"], "previous")
            self.assertFalse(path.with_name(path.name + ".tmp").exists())


if __name__ == "__main__":
    unittest.main()
