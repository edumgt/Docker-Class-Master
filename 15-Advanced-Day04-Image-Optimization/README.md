# Day 04 — 이미지 최적화 & 멀티스테이지

## 목표
- 멀티스테이지 빌드로 런타임 이미지를 경량화한다.
- 태그/푸시 전략을 적용한다.

## 진행(권장)
- 30m: 최적화 원칙
- 120m: 멀티스테이지 실습
- 90m: 레지스트리 push/pull
- 120m: (선택) 취약점 스캔
- 60m: 리뷰

## 실습
### Lab 1) 멀티스테이지 적용
- `Dockerfile`을 build/runtime로 분리
- 크기 비교: `docker images`

### Lab 2) 레지스트리 푸시(선택)
- `docker login`
- `docker tag hello-api:dev <repo>/hello-api:<tag>`
- `docker push <repo>/hello-api:<tag>`


## 과제
- 과제: 운영 이미지 최소화(불필요 패키지 제거/USER 설정) 체크리스트 작성


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
