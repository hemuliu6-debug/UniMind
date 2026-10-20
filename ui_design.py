"""UniMind presentation layer; no model credentials or API logic."""
from pathlib import Path
import gradio as gr

ASSET_DIR = Path(__file__).resolve().parent / "assets"

SUBJECTS = {
    "circuit": {"title": "模拟电路", "en": "CIRCUITS", "symbol": "∿", "color": "blue",
                "description": "读懂电路与波形，找到排查思路。",
                "tags": "电路分析 / 仿真截图 / 故障排查"},
    "math": {"title": "高等数学", "en": "MATHEMATICS", "symbol": "∫", "color": "violet",
             "description": "拆解每一步推导，理解公式背后。",
             "tags": "微积分 / 公式推导 / 易错点"},
    "physics": {"title": "大学物理", "en": "PHYSICS", "symbol": "λ", "color": "teal",
                "description": "从现象到原理，让抽象变得清晰。",
                "tags": "物理建模 / 定律分析 / 单位检查"},
    "programming": {"title": "Python 编程", "en": "PROGRAMMING", "symbol": "</>", "color": "orange",
                    "description": "理清代码逻辑，让报错有迹可循。",
                    "tags": "报错分析 / 代码讲解 / 修改建议"},
}

EXTRA_EXAMPLES = {
    "circuit": ["运算放大器的虚短和虚断分别在什么条件下成立？"],
    "math": ["用一个例子解释定积分的几何意义。"],
    "physics": ["如何判断一个过程中机械能是否守恒？"],
    "programming": ["Python 的列表和元组有什么区别？"],
}

EMPTY_ANSWER = """
<div class="answer-empty">
  <div class="empty-spark" aria-hidden="true">✦</div>
  <h3>让思路，在这里展开</h3>
  <p>写下问题，或选一道示例。<br>从关键概念到解题步骤，一起把问题弄懂。</p>
  <div class="empty-steps"><span>理解问题</span><i>→</i><span>梳理思路</span><i>→</i><span>逐步解答</span></div>
</div>
"""

def make_theme():
    return gr.themes.Soft(
        primary_hue="blue", secondary_hue="violet", neutral_hue="slate",
        font=["Segoe UI", "Microsoft YaHei", "PingFang SC", "sans-serif"],
        font_mono=["Cascadia Code", "Consolas", "monospace"],
    ).set(
        body_background_fill="#ffffff", body_background_fill_dark="#ffffff",
        body_text_color="#172033", body_text_color_dark="#172033",
        block_background_fill="#ffffff", block_background_fill_dark="#ffffff",
        input_background_fill="#f8fafc", input_background_fill_dark="#f8fafc",
        block_border_color="#e8edf5", block_border_color_dark="#e8edf5",
        block_label_text_color="#475569", block_label_text_color_dark="#475569",
        button_primary_background_fill="#2877ef", button_primary_background_fill_dark="#2877ef",
        button_primary_text_color="#ffffff", button_primary_text_color_dark="#ffffff",
    )

def header_html(demo_mode):
    mode = "离线演示" if demo_mode else "DeepSeek · 在线模式"
    return f"""
<header class="site-nav">
  <div class="nav-inner">
    <a class="brand" href="#top" aria-label="UniMind 首页">
      <span class="brand-mark" aria-hidden="true">U<span>·</span></span>
      <span>UniMind<small>让学习，更进一步</small></span>
    </a>
    <nav aria-label="主导航">
      <a href="#subjects">探索学科</a><a href="#workspace">学习工作台</a><a href="#guide">使用指南</a>
    </nav>
    <span class="mode-badge {'is-demo' if demo_mode else ''}"><i></i>{mode}</span>
  </div>
</header>
"""

HERO_HTML = """
<section class="hero" id="top">
  <div class="hero-orbit orbit-one" aria-hidden="true">∫</div>
  <div class="hero-orbit orbit-two" aria-hidden="true">λ</div>
  <span class="hero-badge"><span>✦</span> 你的大学课程 AI 学习伙伴</span>
  <h1>把问题弄懂，<br><span>让知识真正属于你。</span></h1>
  <p>从一道题、一张电路图，到一段代码。<br class="mobile-break">四个学科，一个专注理解的学习空间。</p>
  <div class="hero-actions">
    <a class="cta-primary" href="#workspace">开始学习 <span aria-hidden="true">↗</span></a>
    <a class="cta-secondary" href="#subjects">探索四个学科 <span aria-hidden="true">↓</span></a>
  </div>
  <div class="hero-features"><span>课程资料辅助</span><i></i><span>分步骤讲解</span><i></i><span>随时提出问题</span></div>
</section>
"""

SUBJECT_HEADING = """
<div class="section-heading">
  <div><span class="eyebrow">EXPLORE & LEARN</span><h2>今天，想弄懂什么？</h2></div>
  <p>选择一个学科，从你的问题开始。</p>
</div>
"""

WORKSPACE_HEADING = """
<div class="section-heading workspace-heading">
  <div><span class="eyebrow">YOUR LEARNING SPACE</span><h2>专注问题，慢慢想明白。</h2></div>
  <span class="section-note">学习工作台 <span aria-hidden="true">↙</span></span>
</div>
"""

GUIDE_HTML = """
<section class="guide-content">
  <div class="guide-intro"><span class="eyebrow">A LITTLE GUIDANCE</span><h2>一个好问题，<br>是理解的开始。</h2><p>把卡住的地方说清楚，让每一次提问更有收获。</p></div>
  <div class="guide-steps">
    <article><span>01</span><div><h3>选一个学科</h3><p>切换到对应课程，让回答更贴近你的学习内容。</p></div></article>
    <article><span>02</span><div><h3>给出完整信息</h3><p>写明题目、已知条件和疑惑；电路问题还可以附上截图。</p></div></article>
    <article><span>03</span><div><h3>理解，再验证</h3><p>跟着推导检查条件、单位和结论，重要结果请结合课本核对。</p></div></article>
  </div>
</section>
"""
FOOTER_HTML = """
<footer class="site-footer">
 <div><strong>UniMind<span>·</span></strong><p>让每一次提问，都成为理解的起点。</p></div>
 <p>AI 辅助学习 · 重要结果请核验<br><span>在线提问与图片会发送至模型服务商，请勿提交敏感信息。</span></p>
 <a href="#top" aria-label="返回顶部">↑</a>
</footer>
"""

def course_icon(meta):
    symbol = meta["symbol"].replace("<", "&lt;").replace(">", "&gt;")
    return f'<div class="course-top"><span class="course-icon {meta["color"]}" aria-hidden="true">{symbol}</span><span class="course-en">{meta["en"]}</span></div>'


def html_block(value, **kwargs):
    return gr.HTML(value, apply_default_css=False, **kwargs)
