# 공개 배포 가이드

챗봇을 **누구나 브라우저·핸드폰**에서 사용할 수 있게 배포하는 방법입니다.

## ✅ 1단계: GitHub (완료)

코드가 이미 GitHub에 올라가 있습니다:

**https://github.com/yjunec/historical-chatbot**

---

## 🌐 2단계: Hugging Face Spaces 배포 (추천, 무료)

가장 쉬운 공개 배포 방법입니다. PC·핸드폰 브라우저 모두 지원합니다.

### 방법 A: 웹에서 GitHub 연결 (가장 쉬움)

1. https://huggingface.co/join 에서 계정 생성 (무료)
2. https://huggingface.co/new-space 접속
3. 설정:
   - **Space name**: `historical-chatbot`
   - **License**: MIT
   - **Space SDK**: `Gradio`
   - **Space hardware**: `CPU basic` (무료)
4. **Create Space** 클릭
5. **Files and versions** 탭 → **Add file** → **Sync from GitHub repository**
   - Repository: `yjunec/historical-chatbot`
6. **Settings** → **Repository secrets** → **New secret**
   - Name: `OPENAI_API_KEY`
   - Value: 본인의 OpenAI API 키
7. Space가 빌드되면 공개 URL이 생성됩니다:
   - `https://huggingface.co/spaces/본인아이디/historical-chatbot`

### 방법 B: CLI로 배포

```bash
pip install huggingface_hub
huggingface-cli login
cd historical-chatbot
python deploy_space.py
```

이후 Space Settings에서 `OPENAI_API_KEY` 시크릿을 추가하세요.

---

## 📱 핸드폰에서 사용하기

배포가 완료되면:

1. 핸드폰 브라우저(Chrome, Safari)에서 Space URL 접속
2. (선택) **공유 → 홈 화면에 추가** → 앱처럼 사용 가능

---

## 🖥️ 같은 Wi-Fi에서 로컬 접속 (개발/테스트용)

```bash
cd historical-chatbot
cp .env.example .env   # API 키 입력
python app.py
```

- PC: http://localhost:7860
- 같은 Wi-Fi의 핸드폰: http://(PC의 IP주소):7860
  - Mac IP 확인: `ifconfig | grep "inet "`

---

## ☁️ Render 배포 (대안)

1. https://render.com 가입
2. **New → Blueprint** → GitHub `yjunec/historical-chatbot` 연결
3. 환경변수 `OPENAI_API_KEY` 설정
4. 배포 후 `https://historical-chatbot.onrender.com` 형태의 URL 제공

---

## 🔒 보안 주의

- `.env` 파일은 **절대 GitHub에 올리지 마세요**
- API 키는 Hugging Face / Render의 **Secrets**에만 저장하세요
