# 캡스톤 프로젝트 (Day 10)

## 목표
작은 서비스라도 **운영 가능한 컨테이너 시스템**으로 설계/구현/문서화합니다.

## 요구사항(필수)
- 최소 3개 서비스 구성
  - 예: `web(nginx)` + `api(node/spring/python)` + `db(postgres/mysql)`
- `docker-compose.yml`로 로컬에서 한 번에 구동
- `Dockerfile`에 **멀티스테이지 빌드** 적용(가능한 경우)
- Jenkins CI에서 다음 단계 자동화
  - checkout → test → docker build → tag → push
- 장애 시나리오 2개 이상
  - 재현 절차 + 원인 + 해결 + 재발 방지(체크리스트)

## 제출물
- `README.md`: 실행 방법/구성도/환경변수 안내
- `docker-compose.yml`
- `Dockerfile`(필요한 서비스별)
- `Jenkinsfile`
- `runbook.md`: 장애 대응 문서(최소 2개)

## 평가 기준(예시)
- 재현성(클린 환경에서 구동): 30
- Compose/네트워크/볼륨 설계: 20
- 이미지 최적화/보안 기본: 20
- CI 파이프라인 완성도: 20
- 문서화/Runbook 품질: 10
