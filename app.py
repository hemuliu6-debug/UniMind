"""UniMind unified website entry point."""
import json
import os
from pathlib import Path
import urllib.request
import webbrowser

import gradio as gr
from dotenv import load_dotenv
from modules import circuit, math_subject, physics, programming
from ui_design import (
    ASSET_DIR, SUBJECTS, make_theme, header_html, course_icon, html_block,
    HERO_HTML, SUBJECT_HEADING, WORKSPACE_HEADING, GUIDE_HTML, FOOTER_HTML,
)

load_dotenv(Path(__file__).resolve().with_name(".env"))
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 7860

def build_app():
    demo_mode = os.getenv("DEMO_MODE", "1") == "1"
    with gr.Blocks(title="UniMind · 大学课程 AI 学习助手", analytics_enabled=False) as demo:
        with gr.Column(elem_id="page-shell"):
            html_block(header_html(demo_mode), elem_id="site-header")
            html_block(HERO_HTML, elem_id="hero-block")
            with gr.Column(elem_id="subjects"):
                html_block(SUBJECT_HEADING)
                course_buttons = {}
                with gr.Row(elem_id="subject-cards"):
                    for key, meta in SUBJECTS.items():
                        with gr.Column(min_width=210, elem_classes=["course-card", "course-" + meta["color"]]):
                            html_block(course_icon(meta))
                            course_buttons[key] = gr.Button(
                                meta["title"] + "  ↗", elem_classes=["course-button"],
                                variant="secondary", size="lg",
                            )
                            gr.Markdown(meta["description"], elem_classes=["course-description"])
                            html_block('<p class="course-tags">' + meta["tags"] + '</p>')
            with gr.Column(elem_id="workspace"):
                html_block(WORKSPACE_HEADING)
                with gr.Tabs(selected="circuit", elem_id="subject-tabs", overflow_behavior="wrap") as tabs:
                    with gr.Tab("模拟电路", id="circuit"):
                        circuit.build_tab()
                    with gr.Tab("高等数学", id="math"):
                        math_subject.build_tab()
                    with gr.Tab("大学物理", id="physics"):
                        physics.build_tab()
                    with gr.Tab("Python 编程", id="programming"):
                        programming.build_tab()
                mode_tip = "当前为离线演示，展示检索与问答流程。" if demo_mode else "在线模式已启用，提交问题将消耗模型 API 额度。"
                gr.Markdown(mode_tip + " 每次提问独立处理，请提供完整上下文。",
                            elem_classes=["workspace-disclaimer"])
            html_block(GUIDE_HTML, elem_id="guide")
            html_block(FOOTER_HTML, elem_id="footer-block")

        for key, button in course_buttons.items():
            button.click(
                fn=lambda selected=key: gr.Tabs(selected=selected), inputs=None, outputs=tabs,
                queue=False, api_visibility="private",
                js="() => {document.getElementById('workspace')?.scrollIntoView({behavior:'smooth',block:'start'}); return [];}",
            )
    return demo

def existing_unimind(url):
    """Reuse this website when start_windows.bat is double-clicked twice."""
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url + "/config", timeout=2) as response:
            config = json.load(response)
        labels = {
            c.get("props", {}).get("label")
            for c in config.get("components", []) if c.get("type") == "tabitem"
        }
        return str(config.get("title", "")).startswith("UniMind") and {
            "模拟电路", "高等数学", "大学物理", "Python 编程"
        }.issubset(labels)
    except (OSError, ValueError):
        return False

def launch_app():
    url = f"http://{SERVER_NAME}:{SERVER_PORT}"
    if existing_unimind(url):
        print("[INFO] UniMind is already running. Opening " + url)
        webbrowser.open(url)
        return
    build_app().launch(
        server_name=SERVER_NAME, server_port=SERVER_PORT, share=False, inbrowser=True,
        theme=make_theme(), css_paths=[ASSET_DIR / "theme.css"], footer_links=[],
    )

if __name__ == "__main__":
    launch_app()
