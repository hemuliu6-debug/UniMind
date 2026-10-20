"""运行：python -m unittest discover -s tests -v （不消耗 API 额度）。"""
import os
import unittest

os.environ["DEMO_MODE"] = "1"

from core.retriever import search, format_context
from modules import circuit, math_subject, physics, programming


class TestProject(unittest.TestCase):
    def test_retrieval_match(self):
        results = search("circuit", "示波器为什么没有波形？")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["id"], "c-001")

    def test_retrieval_missing(self):
        self.assertEqual(search("circuit", "火星气候怎么样？"), [])

    def test_format_context(self):
        text = format_context(search("math", "导数怎么求"))
        self.assertIn("[资料1]", text)

    def test_four_modules(self):
        for mod in [circuit, math_subject, physics, programming]:
            with self.subTest(module=mod.__name__):
                reply = mod.answer("测试提问")
                self.assertIn("离线演示", reply)

    def test_image_offline(self):
        reply = circuit.answer("测试截图", image="example.png")
        self.assertIn("离线模式不分析", reply)

    def test_page_build(self):
        from app import build_app
        demo = build_app()
        self.assertIsNotNone(demo)
        config = demo.get_config_file()
        types = [c["type"] for c in config["components"]]
        self.assertIn("image", types)
        self.assertIn("markdown", types)


if __name__ == "__main__":
    unittest.main()
