# Day 09 — Jenkins CI로 Docker 빌드/푸시

## 목표
- Jenkinsfile로 빌드→테스트→푸시 파이프라인을 만든다.
- 태깅 전략을 적용한다.

## 진행(권장)
- 30m: Jenkins+Docker 연동
- 120m: Pipeline 기초
- 180m: 실습(빌드/푸시)
- 60m: 태그 전략
- 30m: 리뷰

## 실습
### Lab) Jenkinsfile 적용
- `templates/Jenkinsfile` 참고
- credentialsId: `dockerhub` (username/password) 등록
- stages: checkout → test → build → login → push

### 체크 포인트
- 빌드 실패 시 로그에서 원인 찾기
- 브랜치별 TAG 정책 적용


## 과제
- 과제: 브랜치/PR 태그 규칙 설계 및 Jenkinsfile에 반영


## 체크리스트
- [ ] 명령어/결과를 README에 기록했다
- [ ] 실패/오류 상황을 1개 이상 재현하고 해결했다
- [ ] “왜 이런 결과가 나왔는지”를 한 줄로 설명할 수 있다
