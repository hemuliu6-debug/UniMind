"""Shared subject workspace; model prompts remain in each subject module."""
import gradio as gr
from ui_design import EMPTY_ANSWER, EXTRA_EXAMPLES, html_block


# The API does not expose a completion percentage: this is an indeterminate
# waiting indicator, followed by a real completed/error state.
WAITING_HTML = """
<div class="answer-status is-running" role="status" aria-live="polite" aria-busy="true">
  <div class="status-line"><strong>AI 正在生成解答</strong><span>请稍候</span></div>
  <div class="answer-progress-track" role="progressbar" aria-label="正在等待模型回答" aria-valuetext="正在生成，完成比例未知">
    <span class="answer-progress-fill"></span>
  </div>
  <p>正在处理你的问题，回答生成后会自动显示。</p>
</div>
"""
DONE_HTML = """
<div class="answer-status is-complete" role="status" aria-live="polite">
  <div class="status-line"><strong>解答已生成</strong><span>已完成</span></div>
  <div class="answer-progress-track"><span class="answer-progress-fill"></span></div>
</div>
"""
ERROR_HTML = """
<div class="answer-status is-error" role="status" aria-live="polite">
  <div class="status-line"><strong>本次解答未完成</strong><span>可以重试</span></div>
  <p>请查看页面提示，调整问题或稍后重试。</p>
</div>
"""

def _begin_answer():
    return (
        gr.update(value=WAITING_HTML, visible=True),
        gr.update(value="正在生成…", interactive=False),
        gr.update(interactive=False),
    )

def _finish_answer(answer):
    text = (answer or "").strip()
    if text.startswith(("请输入问题", "请先输入问题")):
        status = gr.update(value="", visible=False)
    else:
        status = gr.update(value=ERROR_HTML if text.startswith("⚠") else DONE_HTML, visible=True)
    return status, gr.update(value="开始解答  ↗", interactive=True), gr.update(interactive=True)

def _fail_answer():
    return (
        gr.update(value=ERROR_HTML, visible=True),
        gr.update(value="开始解答  ↗", interactive=True),
        gr.update(interactive=True),
    )

def build_subject_ui(*, description: str, example: str, callback, image_enabled=False, multiline=False) -> None:
    subject = callback.__module__.split(".")[-1]
    if subject == "math_subject":
        subject = "math"
    gr.Markdown(description, elem_classes=["subject-description"])
    with gr.Row(elem_classes=["workspace-panels"]):
        with gr.Column(scale=5, min_width=290, elem_classes=["question-panel"]):
            html_block('<div class="panel-heading"><span class="panel-number">01</span><div><h3>提出你的问题</h3><p>条件越清晰，思路越有方向。</p></div></div>')
            question = gr.Textbox(
                label="代码 / 报错 / 问题" if multiline else "题目与已知条件",
                lines=7 if multiline else 5, max_lines=18,
                placeholder=example, elem_classes=["question-input"],
            )
            if image_enabled:
                image = gr.Image(
                    label="上传电路截图（可选）", type="filepath", height=180,
                    sources=["upload"], elem_classes=["circuit-upload"],
                )
            with gr.Row(elem_classes=["action-row"]):
                submit = gr.Button("开始解答  ↗", variant="primary", scale=3, elem_classes=["submit-button"])
                reset = gr.Button("清空", variant="secondary", scale=1, min_width=76, elem_classes=["reset-button"])
            gr.Examples(
                examples=[[example]] + [[item] for item in EXTRA_EXAMPLES.get(subject, [])],
                inputs=[question], label="没有思路？试试这些问题", elem_id="examples-" + subject,
            )
        with gr.Column(scale=6, min_width=310, elem_classes=["answer-panel"]):
            html_block('<div class="panel-heading"><span class="panel-number answer-number">02</span><div><h3>一起理清思路</h3><p>关注推导过程，也关注适用条件。</p></div><span class="answer-chip">AI 解答</span></div>')
            progress_status = html_block("", visible=False, elem_classes=["answer-progress"])
            result = gr.Markdown(
                EMPTY_ANSWER, elem_classes=["answer-text"], buttons=["copy"],
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False},
                    {"left": "\\(", "right": "\\)", "display": False},
                    {"left": "\\[", "right": "\\]", "display": True},
                ],
            )
            html_block('<p class="answer-footnote">参考资料会随回答显示；没有匹配资料时会明确提示。</p>')
    inputs = [question, image] if image_enabled else [question]
    status_outputs = [progress_status, submit, reset]
    begin_event = submit.click(
        fn=_begin_answer, inputs=None, outputs=status_outputs, queue=False,
        show_progress="hidden", api_visibility="private",
    )
    answer_event = begin_event.then(
        fn=callback, inputs=inputs, outputs=result, show_progress="hidden",
    )
    answer_event.success(
        fn=_finish_answer, inputs=result, outputs=status_outputs, queue=False,
        show_progress="hidden", api_visibility="private",
    )
    answer_event.failure(
        fn=_fail_answer, inputs=None, outputs=status_outputs, queue=False,
        show_progress="hidden", api_visibility="private",
    )
    if image_enabled:
        reset.click(
            fn=lambda: ("", None, EMPTY_ANSWER, gr.update(value="", visible=False)),
            outputs=[question, image, result, progress_status],
            queue=False, show_progress="hidden", api_visibility="private",
        )
    else:
        reset.click(
            fn=lambda: ("", EMPTY_ANSWER, gr.update(value="", visible=False)),
            outputs=[question, result, progress_status],
            queue=False, show_progress="hidden", api_visibility="private",
        )
