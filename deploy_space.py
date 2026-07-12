#!/usr/bin/env python3
"""
Hugging Face Spaces 배포 스크립트

사용 전 Hugging Face 로그인이 필요합니다:
  pip install huggingface_hub
  huggingface-cli login

실행:
  python deploy_space.py
"""

import os
import sys

from huggingface_hub import HfApi, upload_folder

SPACE_NAME = "historical-chatbot"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    username = HfApi().whoami()["name"]
    repo_id = f"{username}/{SPACE_NAME}"

    print(f"🚀 Space 배포 시작: {repo_id}")

    api = HfApi()
    api.create_repo(
        repo_id,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
        private=False,
    )

    upload_folder(
        folder_path=PROJECT_DIR,
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=[".env", ".git", "__pycache__", ".DS_Store", "deploy_space.py"],
    )

    print()
    print("✅ 배포 완료!")
    print(f"🌐 공개 URL: https://huggingface.co/spaces/{repo_id}")
    print()
    print("⚠️  마지막 단계: Space Settings → Secrets 에 OPENAI_API_KEY 를 추가하세요.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        print()
        print("해결 방법:")
        print("  1. pip install huggingface_hub")
        print("  2. huggingface-cli login")
        print("  3. python deploy_space.py")
        sys.exit(1)
