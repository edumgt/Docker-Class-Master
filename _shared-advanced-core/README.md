# Docker 과정 

## 구성

- `docs/` : 과정 안내(사전 준비, 평가, 강사용 가이드, 전체 커리큘럼)
- `labs/` : 일자별 실습(코드/명령/미션/체크리스트)
- `capstone/` : 종합 실습(캡스톤) 요구사항/제출물/평가 기준
- `templates/` : 샘플 Dockerfile/compose/Jenkinsfile 템플릿
- `.github/workflows/` : (선택) Markdown 링크/포맷 체크용 CI 예시

## 빠른 시작

1. 이 저장소를 클론합니다.
   - `git clone <YOUR_REPO_URL>`
2. 전체 커리큘럼을 먼저 읽습니다.
   - `docs/syllabus.md`
3. Day 1부터 순서대로 실습을 진행합니다.
   - `labs/day01/README.md` → `labs/day02/README.md` → …

## 권장 학습 환경

- OS: Windows(WSL2) / macOS / Linux
- 필수 설치: Docker Desktop(또는 Docker Engine), Git, VS Code
- 권장: curl, jq, make, (선택) Jenkins, (선택) Trivy

자세한 내용은 `docs/prerequisites.md` 참고.

## 목표

- 컨테이너/이미지/네트워크/스토리지/Compose/디버깅을 **운영 관점**에서 다룰 수 있다.
- Jenkins CI로 **Docker 빌드→테스트→푸시** 자동화 흐름을 구현할 수 있다.
- 캡스톤을 통해 “재현 가능한 배포 단위”를 설계/문서화할 수 있다.

## 라이선스

- 기본: MIT (`LICENSE`)
- 회사/기관 정책에 맞게 변경 가능


