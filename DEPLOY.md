# 공개 배포 가이드 (Hugging Face 계정 불필요)

## 🎉 가장 쉬운 방법 — 1분 만에 공개 URL 만들기

Hugging Face, Render 등 **어떤 계정도 필요 없습니다.**

```bash
cd historical-chatbot
python3 start_public.py
```

실행하면 아래와 같은 **공개 URL**이 자동 생성됩니다:

```
https://xxxxx.trycloudflare.com
```

- ✅ PC 브라우저에서 접속 가능
- ✅ 핸드폰 브라우저에서 접속 가능 (URL 공유)
- ✅ 타인에게 링크만내면 바로 사용 가능

> ⚠️ 이 터미널을 닫으면 URL이 사라집니다.  
> 다시 공개하려면 `python3 start_public.py` 를 다시 실행하세요.

---

## 📱 핸드폰에서 사용하기

1. `start_public.py` 실행 후 나온 공개 URL 복사
2. 핸드폰 브라우저(Chrome, Safari)에 붙여넣기
3. (선택) **공유 → 홈 화면에 추가** → 앱처럼 사용

---

## 💻 로컬에서만 사용 (같은 Wi-Fi 핸드폰 접속)

```bash
cd historical-chatbot
cp .env.example .env   # OPENAI_API_KEY 입력
python3 app.py
```

- PC: http://localhost:7860
- 같은 Wi-Fi 핸드폰: http://(맥 IP주소):7860

---

## ☁️ 24시간 상시 운영 (선택사항)

컴퓨터를 꺼도 계속 운영하려면 무료 클라우드 배포를 사용하세요.

### Render (추천, Hugging Face 불필요)

1. https://render.com 가입 (GitHub 계정으로 가능)
2. **New → Blueprint** → `yjunec/historical-chatbot` 연결
3. 환경변수 `OPENAI_API_KEY` 설정
4. 배포 완료 후 `https://historical-chatbot.onrender.com` 형태 URL 제공

### Hugging Face Spaces (선택)

HF 계정이 있다면 [README.md](README.md)의 안내를 참고하세요.

---

## 🔒 보안

- `.env` 파일은 GitHub에 올리지 마세요
- API 키는 본인만 관리하세요
