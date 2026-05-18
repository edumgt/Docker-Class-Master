# Day 03 — 이미지 기초 & Dockerfile 작성

## 목표
- Dockerfile로 애플리케이션 이미지를 만든다.
- 레이어/캐시 개념을 이해하고 `.dockerignore`를 적용한다.

## 진행(권장)
- 30m: 이미지 구조
- 90m: Dockerfile 문법
- 120m: 실습(Hello API)
- 90m: 캐시 최적화
- 90m: 리뷰/정리

## 실습
### Lab) Hello API 이미지 만들기(예: Node)
1) `templates/Dockerfile.node` 참고하여 Dockerfile 작성
2) `docker build -t hello-api:dev .`
3) `docker run --rm -p 3000:3000 hello-api:dev`

### 체크 포인트
- `docker image ls`에서 용량 확인
- `docker history hello-api:dev`로 레이어 확인


## 과제
- 과제: 캐시 최적화 전/후 빌드 시간 및 이미지 크기 비교 리포트 작성


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
