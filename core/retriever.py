"""第一版轻量检索：在各学科 JSON 知识库中按关键词匹配。
不是向量检索；后续可更换实现，只需保持 search() 接口。
"""
import json
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parents[1] / "knowledge"
ALLOWED_SUBJECTS = {"circuit", "math", "physics", "programming"}


def search(subject: str, question: str, top_k: int = 2) -> list[dict]:
    if subject not in ALLOWED_SUBJECTS:
        raise ValueError("不支持的学科")
    data = json.loads((KNOWLEDGE_DIR / f"{subject}.json").read_text(encoding="utf-8"))
    q = question.lower().strip()
    if not q:
        return []
    ranked = []
    for item in data:
        keywords = [str(k).lower() for k in item.get("keywords", [])]
        score = sum(2 for k in keywords if k and k in q)
        # 标题命中加分，不对长篇内容进行宽泛匹配
        title = str(item.get("title", "")).lower()
        if title and title in q:
            score += 3
        if score > 0:
            ranked.append((score, item))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in ranked[:max(0, top_k)]]


def format_context(items: list[dict]) -> str:
    if not items:
        return "没有匹配到课程资料。不要编造课程来源；可利用一般知识回答并说明缺少资料。"
    return "\n\n".join(
        f"[资料{i}] 标题：{item['title']}\n来源：{item['source']}\n内容：{item['content']}"
        for i, item in enumerate(items, 1)
    )


def format_source_list(items: list[dict]) -> str:
    if not items:
        return "\n\n---\n*本次未检索到匹配的课程资料。*"
    lines = ["\n\n---\n**本次检索到的资料（请核对答案是否正确引用）：**"]
    for i, item in enumerate(items, 1):
        lines.append(f"- [资料{i}] {item['title']} — {item['source']}")
    return "\n".join(lines)
