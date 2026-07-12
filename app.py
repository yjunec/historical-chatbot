"""
Hugging Face Spaces / 클라우드 배포용 진입점
"""

from historical_chatbot_ui import create_app, THEME, CUSTOM_CSS
import os

demo = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        theme=THEME,
        css=CUSTOM_CSS,
    )
