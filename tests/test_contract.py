"""检验四组交付的知识卡与模块接口约定。离线可运行。"""
import json
import inspect
import unittest
from pathlib import Path
from modules import circuit, math_subject, physics, programming

ROOT = Path(__file__).resolve().parents[1]
SPECS = [
    ("circuit", circuit),
    ("math", math_subject),
    ("physics", physics),
    ("programming", programming),
]


class TestInterfaceContract(unittest.TestCase):
    def test_module_signatures(self):
        for subject, module in SPECS:
            with self.subTest(subject=subject):
                params = inspect.signature(module.answer).parameters
                self.assertEqual(list(params), ["question", "image"])
                self.assertTrue(callable(module.build_tab))

    def test_knowledge_data(self):
        for subject, _ in SPECS:
            with self.subTest(subject=subject):
                file = ROOT / "knowledge" / f"{subject}.json"
                cards = json.loads(file.read_text(encoding="utf-8"))
                self.assertIsInstance(cards, list)
                self.assertGreaterEqual(len(cards), 3)
                ids = []
                for card in cards:
                    for key in ("id", "title", "keywords", "content", "source"):
                        self.assertIn(key, card)
                    self.assertIsInstance(card["keywords"], list)
                    self.assertGreaterEqual(len(card["keywords"]), 3)
                    self.assertTrue(str(card["content"]).strip())
                    ids.append(card["id"])
                self.assertEqual(len(ids), len(set(ids)), "知识卡 ID 重复")


if __name__ == "__main__":
    unittest.main()
