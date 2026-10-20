"""01/02 号维护：模拟电路模块（保留图片分析特色）。"""
from core.pipeline import respond
from modules._ui import build_subject_ui

PROMPT = (
    "你是大学模拟电路及电路仿真实验助教。请按：可确认的信息、可能原因、检查步骤、下一步确认问题 组织中文 Markdown 回答。"
    "电路参数和元件连接只在看清时明确陈述，无法确认时说明不确定性。"
    "有课程资料时可按[资料1]标注，但不能捏造出处；避免给出危险的真实电气操作指令。"
)


def answer(question: str, image: str | None = None) -> str:
    return respond("circuit", question, PROMPT, image=image)


def build_tab() -> None:
    build_subject_ui(
        description="### 模拟电路助手\n可输入故障现象，或上传仿真截图分析。",
        example="示波器为什么没有波形？请给出排查步骤。",
        callback=answer,
        image_enabled=True,
    )
