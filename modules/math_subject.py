"""03/04 号维护：高等数学模块。"""
from core.pipeline import respond
from modules._ui import build_subject_ui

PROMPT = (
    "你是大学高等数学辅导老师。请先说明适用的定理与条件，再逐步推导、检查答案。"
    "公式用 Markdown 支持的 LaTeX 数学定界符 $...$ 或 $$...$$，不要裸输出转义符。"
    "缺少条件不要编造。检索资料只在有关时使用，引用资料编号不得虚构。"
)


def answer(question: str, image: str | None = None) -> str:
    return respond("math", question, PROMPT)


def build_tab() -> None:
    build_subject_ui(
        description="### 高等数学助手\n分步解题、公式推导及易错点分析。",
        example="求函数 f(x)=x^2e^x 的导数，并说明步骤。",
        callback=answer,
    )
