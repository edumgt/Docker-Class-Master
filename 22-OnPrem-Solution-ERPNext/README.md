# 22. OnPrem Solution - ERPNext

## 솔루션 개요
- 원본: https://github.com/frappe/erpnext
- 목적: ERPNext + MariaDB 조합을 Docker로 운영하며 데이터 계층 특성을 학습합니다.
- 동기화 스크립트: `../_shared-onprem-core/sync-solutions.sh`

## Docker 수업 관점 학습 포인트
- PostgreSQL이 아닌 MariaDB를 사용하는 서비스 구성 차이
- DB 초기화 스크립트(`docker/db-init`) 동작 이해
- 컨테이너 헬스체크 기반 의존성 기동 순서

## 실습 절차
1. 통합 스택 기동
```bash
cd ../_shared-onprem-core
./start.sh
```
2. ERPNext 인증 API 확인
```bash
curl -s http://localhost:9001/health
curl -s http://localhost:9001/members
```
3. 로그인/JWT 발급 확인
```bash
curl -s -X POST http://localhost:9001/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"erpnext_member1","password":"123456"}'
```
4. MariaDB 컨테이너/포트 확인
```bash
docker ps --filter name=erpnext-rdbms
```

## 체크 포인트
- `erpnext-rdbms` 초기화가 완료되고 healthcheck가 통과하는지
- API 응답 지연이 있을 때 DB readiness를 먼저 점검하는지
- 데이터 볼륨 삭제 시 재기동 영향도를 이해하는지

## 과제(권장)
- MariaDB 백업/복구 명령을 1회 실행 후 기록
- 로그인 실패 케이스(비밀번호 오입력) 응답 코드 정리
- ERPNext와 Odoo의 DB 운영 차이를 비교 문서로 작성
