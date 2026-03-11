# 25. OnPrem Solution - Zulip

## 솔루션 개요
- 원본: https://github.com/zulip/zulip
- 목적: 메시징/협업 시스템을 Docker로 운영할 때의 의존 서비스(DB, 큐, 캐시) 개념을 이해합니다.
- 동기화 스크립트: `../_shared-onprem-core/sync-solutions.sh`

## Docker 수업 관점 학습 포인트
- 애플리케이션 외부 의존성(메시지큐/캐시)의 필요성
- 다중 컨테이너 서비스의 기동 순서와 상태 점검
- 로그/메트릭 기반 운영 가시성 확보

## 실습 절차
1. 통합 스택 기동
```bash
cd ../_shared-onprem-core
./start.sh
```
2. Zulip 인증 API 확인
```bash
curl -s http://localhost:9002/health
curl -s http://localhost:9002/members
```
3. 로그인/JWT 발급 확인
```bash
curl -s -X POST http://localhost:9002/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"zulip_member1","password":"123456"}'
```
4. DB 컨테이너 상태 확인
```bash
docker ps --filter name=zulip-rdbms
```

## 체크 포인트
- 인증 API는 살아있지만 내부 의존성이 죽었을 때 로그로 감지 가능한지
- 재기동 후 세션/데이터 일관성이 유지되는지
- 운영 문서에 헬스체크와 롤백 절차가 포함되어 있는지

## 과제(권장)
- 메시징 서비스 특성에 맞는 모니터링 지표 5개 제안
- 의존 서비스 장애(DB/큐/캐시) 시나리오별 대응 절차 작성
- 팀 표준 incident report 템플릿으로 실습 결과 정리
