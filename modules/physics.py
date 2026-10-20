"""05/06 号维护：大学物理模块。"""
from core.pipeline import respond
from modules._ui import build_subject_ui

PROMPT = (
    "你是大学物理助教。请区分已知量、要求的物理量、公式适用条件、代入和单位检查。"
    "实验问题先分析原理，再说明误差或诊断方法。对无法判断的信息应说明。"
    "引用参考资料时只能使用实际提供的资料编号。"
)


def answer(question: str, image: str | None = None) -> str:
    return respond("physics", question, PROMPT)


def build_tab() -> None:
    build_subject_ui(
        description="### 大学物理助手\n原理讲解、公式与单位检查。",
        example="为什么电场力做功与路径无关？请说明适用条件。",
        callback=answer,
    )
