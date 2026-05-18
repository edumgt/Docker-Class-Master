# Day 05 — 네트워킹(브리지/DNS/서비스 디스커버리)

## 목표
- 사용자 정의 네트워크에서 컨테이너 이름 기반 통신을 구성한다.
- 포트 노출 최소화 전략을 이해한다.

## 진행(권장)
- 30m: 네트워크 개요
- 120m: 3-tier 구성
- 120m: 트러블슈팅
- 90m: 설계 과제
- 60m: 리뷰

## 실습
### Lab) 사용자 정의 네트워크
- `docker network create appnet`
- db: `docker run -d --name db --network appnet postgres:16-alpine`
- api: `docker run -d --name api --network appnet -e DB_HOST=db <your-api-image>`
- 컨테이너 내부에서 `ping db` 또는 TCP 연결 확인


## 과제
- 과제: 외부 노출 포트 최소화 설계안(그림/설명) 작성


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
