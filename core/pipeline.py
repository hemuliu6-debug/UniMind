"""统一 RAG 流程：检索 → 构造参考资料 → 大模型生成 → 展示可核验来源。"""
from core.retriever import search, format_context, format_source_list
from core.llm_client import ask_model


def respond(subject: str, question: str, prompt: str, image: str | None = None) -> str:
    if not (question or "").strip() and image is None:
        return "请输入问题或上传图片。"
    sources = search(subject, question)
    answer = ask_model(subject, question, prompt, format_context(sources), image=image)
    return answer + format_source_list(sources)
