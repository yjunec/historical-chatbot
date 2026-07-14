"""
역사적 인물 챗봇 - Gradio 웹 UI
"""

import os

import httpx
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from historical_chatbot import (
    HISTORICAL_FIGURES,
    HistoricalFigureChatbot,
)

FIGURE_ICONS = {
    "알베르트 아인슈타인": "🧑‍🔬",
    "세종대왕": "👑",
    "마리 퀴리": "⚗️",
    "레오나르도 다 빈치": "🎨",
    "넬슨 만델라": "✊",
}

FIGURE_BY_NAME = {figure["name"]: figure for figure in HISTORICAL_FIGURES.values()}
FIGURE_NAMES = list(FIGURE_BY_NAME.keys())

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap');

.gradio-container,
.gradio-container * {
    font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif !important;
    word-break: keep-all;
}
.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
}
.main-header {
    text-align: center;
    padding: 1rem 0 0.5rem;
}
.main-header h1 {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 700;
    color: #8B6914 !important;
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: #8B6914 !important;
    margin-bottom: 0.25rem;
    line-height: 1.4;
}
.main-header p {
    color: #6B5B4E;
    font-size: clamp(0.85rem, 2.5vw, 0.95rem);
    line-height: 1.5;
}
.figure-card {
    background: linear-gradient(145deg, #FDF8F0 0%, #F5EDE0 100%);
    border: 1px solid #D4C4A8;
    border-radius: 12px;
    padding: 1rem;
    margin-top: 0.5rem;
}
.figure-card .era {
    color: #8B6914;
    font-weight: 600;
    font-size: 0.85rem;
}
.figure-card .background {
    color: #5C4F3D;
    font-size: 0.85rem;
    line-height: 1.5;
    margin-top: 0.5rem;
}
.sidebar-title {
    font-weight: 700;
    color: #4A3728;
    font-size: 1rem;
}
footer {
    display: none !important;
}
button, .gr-button, .gr-button * {
    font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
    -webkit-font-smoothing: antialiased;
}
@media (max-width: 768px) {
    .gradio-container {
        padding: 0.5rem !important;
    }
    .main-header {
        padding: 0.5rem 0;
    }
    button {
        min-height: 44px !important;
    }
    textarea, input {
        font-size: 16px !important;
    }
}
"""

THEME = gr.themes.Soft(
    primary_hue="amber",
    secondary_hue="orange",
    neutral_hue="stone",
)

load_dotenv()
client = OpenAI(http_client=httpx.Client())


def get_figure_info(name: str) -> str:
    figure = FIGURE_BY_NAME[name]
    icon = FIGURE_ICONS.get(name, "📜")
    return (
        f'<div class="figure-card">'
        f'<div class="era">{icon} {figure["era"]}</div>'
        f'<div class="background">{figure["background"]}</div>'
        f"</div>"
    )


def get_welcome_message(name: str) -> str:
    figure = FIGURE_BY_NAME[name]
    icon = FIGURE_ICONS.get(name, "")
    return (
        f"{icon} 안녕하세요! 저는 **{figure['name']}**입니다.\n\n"
        f"*{figure['era']}*\n\n"
        f"궁금한 것이 있으시면 무엇이든 물어보세요."
    )


def start_conversation(figure_name: str):
    figure = FIGURE_BY_NAME[figure_name]
    bot = HistoricalFigureChatbot(client, figure)
    history = [{"role": "assistant", "content": get_welcome_message(figure_name)}]
    return bot, history, get_figure_info(figure_name)


def chat_response(message: str, history: list, bot: HistoricalFigureChatbot | None):
    if bot is None:
        gr.Warning("먼저 역사적 위인을 선택하고 '대화 시작' 버튼을 눌러주세요.")
        return "", history, bot

    if not message.strip():
        return "", history, bot

    try:
        answer = bot.chat(message)
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": answer},
        ]
        return "", history, bot
    except Exception as e:
        if bot.messages and bot.messages[-1]["role"] == "user":
            bot.messages.pop()
        gr.Warning(f"오류가 발생했습니다: {e}")
        return "", history, bot


def reset_conversation(figure_name: str):
    return start_conversation(figure_name)


def create_app() -> gr.Blocks:
    with gr.Blocks(title="역사적 위인과의 대화") as demo:
        bot_state = gr.State(None)

        gr.HTML(
            """
            <meta charset="utf-8">
            <div class="main-header">
                <h1>📜 역사적 위인과의 대화</h1>
                <p>위대한 역사적 위인들과 직접 대화해보세요</p>
            </div>
            """
        )

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=260):
                gr.Markdown("### 🎭 인물 선택", elem_classes=["sidebar-title"])

                figure_dropdown = gr.Dropdown(
                    choices=FIGURE_NAMES,
                    value=FIGURE_NAMES[0],
                    label="대화할 역사적 위인",
                    interactive=True,
                )

                figure_info = gr.HTML(get_figure_info(FIGURE_NAMES[0]))

                with gr.Row():
                    start_btn = gr.Button("대화 시작", variant="primary", scale=2)
                    reset_btn = gr.Button("초기화", variant="secondary", scale=1)

                gr.Markdown(
                    "**사용 방법**\n"
                    "1. 인물을 선택합니다\n"
                    "2. '대화 시작'을 클릭합니다\n"
                    "3. 자유롭게 질문하세요\n"
                    "4. '초기화'로 대화를 새로 시작할 수 있습니다"
                )

            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="대화",
                    height=480,
                    layout="bubble",
                    placeholder="인물을 선택하고 '대화 시작'을 눌러주세요.",
                    buttons=["copy"],
                )

                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="질문을 입력하세요... (예: 시간 여행이 가능할까요?)",
                        scale=5,
                        show_label=False,
                        container=False,
                    )
                    send_btn = gr.Button("전송", variant="primary", scale=1, min_width=80)

                gr.Examples(
                    examples=[
                        ["시대를 초월해 만나게 되어 영광입니다. 당신의 가장 큰 업적은 무엇인가요?"],
                        ["평생을 돌아보며 가장 후회하는 일이 있으신가요?"],
                        ["오늘날의 세상을 본다면 어떤 생각이 드시나요?"],
                        ["젊은이들에게 해주고 싶은 조언이 있으신가요?"],
                    ],
                    inputs=msg_input,
                    label="💡 질문 예시",
                )

        figure_dropdown.change(
            fn=get_figure_info,
            inputs=figure_dropdown,
            outputs=figure_info,
        )

        start_btn.click(
            fn=start_conversation,
            inputs=figure_dropdown,
            outputs=[bot_state, chatbot, figure_info],
        )

        reset_btn.click(
            fn=reset_conversation,
            inputs=figure_dropdown,
            outputs=[bot_state, chatbot, figure_info],
        )

        msg_input.submit(
            fn=chat_response,
            inputs=[msg_input, chatbot, bot_state],
            outputs=[msg_input, chatbot, bot_state],
        )
        send_btn.click(
            fn=chat_response,
            inputs=[msg_input, chatbot, bot_state],
            outputs=[msg_input, chatbot, bot_state],
        )

        demo.load(
            fn=start_conversation,
            inputs=figure_dropdown,
            outputs=[bot_state, chatbot, figure_info],
        )

    return demo


def launch_app(**kwargs):
    port = int(os.environ.get("PORT", os.environ.get("GRADIO_SERVER_PORT", 7860)))
    server_name = os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0")

    app = create_app()
    app.launch(
        server_name=server_name,
        server_port=port,
        share=kwargs.pop("share", False),
        theme=THEME,
        css=CUSTOM_CSS,
        **kwargs,
    )


if __name__ == "__main__":
    launch_app()
