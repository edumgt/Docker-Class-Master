# 24. OnPrem Solution - Taiga

## 솔루션 개요
- 원본: https://github.com/taigaio/taiga-docker
- 목적: 협업/프로젝트 관리 도구를 Docker로 운영하면서 서비스 품질 점검 절차를 익힙니다.
- 동기화 스크립트: `../_shared-onprem-core/sync-solutions.sh`

## Docker 수업 관점 학습 포인트
- 프로젝트 관리 도구의 상태 데이터와 계정 데이터 분리
- 포트 매핑/서비스 네이밍 표준화
- 운영 관점 모니터링 항목(응답시간, 오류율) 정의

## 실습 절차
1. 통합 스택 기동
```bash
cd ../_shared-onprem-core
./start.sh
```
2. Taiga 인증 API 확인
```bash
curl -s http://localhost:9003/health
curl -s http://localhost:9003/members
```
3. 로그인/JWT 발급 확인
```bash
curl -s -X POST http://localhost:9003/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"taiga_member1","password":"123456"}'
```
4. DB 컨테이너 상태 확인
```bash
docker ps --filter name=taiga-rdbms
```

## 체크 포인트
- API 헬스체크와 실제 로그인 동작이 모두 정상인지
- 컨테이너 로그에서 경고/오류를 분리해 읽을 수 있는지
- 운영 시 필요한 백업 주기 기준을 제시할 수 있는지

## 과제(권장)
- Taiga 서비스 장애 대응 runbook(탐지/조치/검증) 작성
- 포트 충돌 상황을 재현하고 해결 절차 문서화
- Taiga/ERPNext의 운영 난이도 차이 분석
