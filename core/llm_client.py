
"""DeepSeek API 统一调用模块：支持深度思考与 Token 统计。"""

import base64
import os
from pathlib import Path

from PIL import Image
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

ALLOWED_FORMATS = {
    "PNG": "image/png",
    "JPEG": "image/jpeg",
    "WEBP": "image/webp",
    "GIF": "image/gif",
}

MAX_IMAGE_BYTES = 6 * 1024 * 1024


def _encode_image(path: str) -> dict:
    image_path = Path(path)

    if not image_path.is_file():
        raise ValueError("图片不存在，请重新上传。")

    if image_path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError("图片超过 6MB，请压缩后重试。")

    try:
        with Image.open(image_path) as img:
            mime = ALLOWED_FORMATS.get(img.format)
            img.verify()
    except Exception as exc:
        raise ValueError(
            "无法读取图片，请上传 PNG、JPG、WebP 或 GIF。"
        ) from exc

    if not mime:
        raise ValueError("不支持的图片格式。")

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("ascii")

    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime};base64,{encoded}"
        },
    }


def ask_model(
    subject: str,
    question: str,
    system_prompt: str,
    context: str,
    image: str | None = None,
) -> str:
    """统一 DeepSeek API 调用接口。"""

    question = (question or "").strip()

    if not question and image is None:
        return "请先输入问题，或者上传一张图片。"

    # 离线演示模式
    if os.getenv("DEMO_MODE", "1") == "1":
        return (
            f"### 【离线演示】{subject}模块调用成功\n\n"
            f"**收到的问题：** "
            f"{question or '请分析上传的图片'}\n\n"
            f"**图片：** "
            f"{'已选择（离线模式不分析）' if image else '未上传'}\n\n"
            "**检索状态：** 已执行课程资料检索；"
            "请在在线模式测试实际生成效果。\n\n"
            "*设置 DEMO_MODE=0 后调用云端 DeepSeek。*"
        )

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()

    if not api_key:
        return (
            "⚠️ 未设置 DEEPSEEK_API_KEY。"
            "请在本机 .env 文件中配置。"
        )

    try:
        from openai import OpenAI

        # 构造用户消息
        content = [
            {
                "type": "text",
                "text": question or "请分析上传图片。",
            }
        ]

        if image:
            content.append(_encode_image(image))

        # API 配置
        client = OpenAI(
            api_key=api_key,
            base_url=os.getenv(
                "DEEPSEEK_BASE_URL",
                "https://api.deepseek.com"
            ),
            timeout=float(
                os.getenv("AI_TIMEOUT", "180")
            ),
            max_retries=1,
        )

        # 推理强度
        effort = os.getenv(
            "AI_REASONING_EFFORT", "max"
        ).strip().lower()

        if effort not in {"low", "high", "max"}:
            return "⚠️ 推理强度只能是 low、high 或 max。"

        # 输出 Token 上限
        max_tokens = int(
            os.getenv("AI_MAX_TOKENS", "16384")
        )

        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model=os.getenv(
                "DEEPSEEK_MODEL",
                "deepseek-flash"
            ),
            messages=[
                {
                    "role": "system",
                    "content": (
                        system_prompt
                        + "\n\n参考资料如下：\n"
                        + context
                    ),
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],

            # 开启深度思考
            reasoning_effort=effort,

            extra_body={
                "thinking": {
                    "type": "enabled"
                }
            },

            # 增加输出预算
            max_tokens=max_tokens,

            stream=False,
        )

        choice = response.choices[0]
        answer = choice.message.content or ""

        # 统计 Token 消耗
        usage = response.usage

        if usage:
            details = getattr(
                usage,
                "completion_tokens_details",
                None
            )

            reasoning_tokens = getattr(
                details,
                "reasoning_tokens",
                None
            )

            print("\n===== DeepSeek API 统计 =====")
            print("学科模块:", subject)
            print("推理强度:", effort)
            print("输入 Token:", usage.prompt_tokens)
            print("输出 Token:", usage.completion_tokens)
            print("推理 Token:", reasoning_tokens)
            print("总 Token:", usage.total_tokens)
            print("结束原因:", choice.finish_reason)
            print("============================\n")

        # 检查是否因输出上限而中断
        if choice.finish_reason == "length":
            warning = (
                "\n\n⚠️ 本次回答达到 Token 上限，"
                "内容可能不完整。"
            )
            return (answer + warning) if answer else warning

        return answer or (
            "模型没有返回可见内容，请重试。"
        )

    except ValueError as exc:
        return f"⚠️ 输入或配置问题：{exc}"

    except Exception as exc:
        # 不将 API 密钥或原始服务响应返回前端
        return (
            f"⚠️ API 请求失败（错误类型："
            f"{type(exc).__name__}）。"
            "请检查 API Key、余额、网络、"
            "模型权限和图片大小。"
        )
