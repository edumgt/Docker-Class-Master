# 사전 준비(Prerequisites)

## 필수
- Docker Desktop(Windows/macOS) 또는 Docker Engine(Linux)
- Git
- VS Code (또는 선호 IDE)

## 권장 도구
- curl
- jq
- make
- (선택) Jenkins
- (선택) Trivy (취약점 스캐너)

## 권장 OS별 팁

### Windows (WSL2)
- WSL2 활성화 + Ubuntu 설치 권장
- Docker Desktop에서 WSL Integration 활성화 권장
- 파일 권한/경로 이슈가 생기면 **WSL 내부 경로**에서 실습 권장

### macOS
- Docker Desktop 최신 버전 권장
- Apple Silicon(M 시리즈) 환경에서는 일부 이미지의 아키텍처(amd64/arm64) 확인

### Linux
- Docker Engine 설치 후, `docker` 명령을 sudo 없이 쓰려면 사용자 그룹 설정 필요

## 사전 지식(권장)
- 리눅스 기본 명령어(ls, cd, cat, grep, ps, netstat/ss)
- 포트/프로세스 개념(0.0.0.0, localhost)
- Git 기본(add/commit/push/branch)
