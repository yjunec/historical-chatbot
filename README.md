---
title: 역사적 인물과의 대화
emoji: 📜
colorFrom: amber
colorTo: orange
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: mit
short_description: 역사적 인물과 대화하는 AI 챗봇
---

# 📜 역사적 인물과의 대화

OpenAI API를 활용해 알베르트 아인슈타인, 세종대왕, 마리 퀴리 등 역사적 인물과 대화할 수 있는 챗봇입니다.

## 🌐 GitHub 저장소

**https://github.com/yjunec/historical-chatbot**

## 🌐 공개 URL 만들기 (계정 불필요!)

Hugging Face 계정 없이도 바로 공개할 수 있습니다:

```bash
cd historical-chatbot
python3 start_public.py
```

생성된 `https://xxxxx.trycloudflare.com` URL을 핸드폰·PC 브라우저에서 열면 됩니다.
자세한 내용은 [DEPLOY.md](DEPLOY.md) 참고.

## ✨ 기능

- 5명의 역사적 인물 선택 (아인슈타인, 세종대왕, 마리 퀴리, 레오나르도 다 빈치, 넬슨 만델라)
- 인물별 말투·성격·시대적 배경 반영
- 대화 맥락 유지 (연속 질문 가능)
- 모바일·PC 브라우저 모두 지원

## 🚀 로컬 실행

```bash
git clone https://github.com/yjunec/historical-chatbot.git
cd historical-chatbot
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY 입력
python app.py
```

브라우저에서 http://localhost:7860 접속

## ☁️ Hugging Face Spaces 배포

1. [Hugging Face](https://huggingface.co) 계정 생성
2. [New Space](https://huggingface.co/new-space) → SDK: **Gradio** 선택
3. 이 GitHub 저장소 연결 또는 파일 업로드
4. Space **Settings → Repository secrets** 에 `OPENAI_API_KEY` 추가

## 📱 모바일 사용

배포된 URL을 스마트폰 브라우저(Chrome, Safari)에서 열면 바로 사용할 수 있습니다.
홈 화면에 추가하면 앱처럼 사용할 수도 있습니다.

## 📁 프로젝트 구조

```
historical-chatbot/
├── app.py                  # 배포용 진입점
├── historical_chatbot.py   # 챗봇 로직
├── historical_chatbot_ui.py # Gradio UI
├── requirements.txt
└── .env.example
```

## ⚠️ 주의사항

- `.env` 파일은 Git에 올리지 마세요 (API 키 보호)
- OpenAI API 사용량에 따라 비용이 발생할 수 있습니다
