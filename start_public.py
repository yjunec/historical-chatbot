#!/usr/bin/env python3
"""
공개 URL로 챗봇 실행 (Hugging Face 계정 불필요)

Cloudflare Tunnel을 사용해 누구나 브라우저·핸드폰에서 접속할 수 있는
공개 URL을 자동으로 생성합니다.
"""

import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", 7860))
ENV_FILE = PROJECT_DIR / ".env"
PARENT_ENV = PROJECT_DIR.parent / ".env"


def ensure_env():
    if not ENV_FILE.exists() and PARENT_ENV.exists():
        ENV_FILE.write_text(PARENT_ENV.read_text(encoding="utf-8"), encoding="utf-8")
        print("✅ .env 파일을 준비했습니다.")

    if not ENV_FILE.exists():
        print("❌ OPENAI_API_KEY가 필요합니다.")
        print(f"   {PROJECT_DIR / '.env.example'} 파일을 참고해 .env 를 만드세요.")
        sys.exit(1)


def start_gradio():
    return subprocess.Popen(
        [sys.executable, str(PROJECT_DIR / "app.py")],
        cwd=PROJECT_DIR,
        env={**os.environ, "PORT": str(PORT), "GRADIO_SERVER_NAME": "127.0.0.1"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def wait_for_server(timeout=60):
    import urllib.request

    url = f"http://127.0.0.1:{PORT}/"
    for _ in range(timeout):
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


def start_tunnel():
    return subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def extract_public_url(output: str) -> str | None:
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", output)
    return match.group(0) if match else None


def main():
    ensure_env()

    print("🚀 챗봇 서버를 시작합니다...")
    gradio_proc = start_gradio()

    if not wait_for_server():
        print("❌ 챗봇 서버 시작에 실패했습니다.")
        gradio_proc.terminate()
        sys.exit(1)

    print("✅ 로컬 서버 준비 완료")
    print("🌐 공개 URL을 생성합니다...")

    tunnel_proc = start_tunnel()
    public_url = None
    combined_output = ""

    for _ in range(90):
        line = tunnel_proc.stdout.readline()
        if not line:
            if tunnel_proc.poll() is not None:
                break
            time.sleep(0.2)
            continue
        combined_output += line
        print(line.rstrip())
        public_url = extract_public_url(combined_output)
        if public_url:
            break

    if not public_url:
        print("❌ 공개 URL 생성에 실패했습니다.")
        gradio_proc.terminate()
        tunnel_proc.terminate()
        sys.exit(1)

    url_file = PROJECT_DIR / "PUBLIC_URL.txt"
    url_file.write_text(public_url + "\n", encoding="utf-8")

    print()
    print("=" * 55)
    print("  🎉 공개 배포 완료! (Hugging Face 계정 불필요)")
    print("=" * 55)
    print(f"  🌐 공개 URL : {public_url}")
    print(f"  📱 핸드폰   : 위 URL을 브라우저에서 열기")
    print(f"  💻 로컬     : http://localhost:{PORT}")
    print("=" * 55)
    print("  ⚠️  이 터미널을 닫으면 공개 URL이 사라집니다.")
    print("  다시 실행: python start_public.py")
    print("=" * 55)
    print()

    def shutdown(*_):
        print("\n👋 서버를 종료합니다...")
        gradio_proc.terminate()
        tunnel_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        gradio_proc.wait()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
