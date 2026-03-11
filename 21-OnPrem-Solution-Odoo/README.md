# 21. OnPrem Solution - Odoo

## 솔루션 개요
- 원본: https://github.com/odoo/odoo
- 목적: Odoo를 Docker 기반으로 빠르게 기동하고, 인증 API/DB 연동 흐름을 이해합니다.
- 동기화 스크립트: `../_shared-onprem-core/sync-solutions.sh`

## Docker 수업 관점 학습 포인트
- 애플리케이션 컨테이너와 DB 컨테이너 분리 구조
- 환경변수 기반 설정 주입 방식
- 상태 저장 데이터(볼륨)와 이미지의 역할 분리

## 실습 절차
1. 통합 스택 기동
```bash
cd ../_shared-onprem-core
./start.sh
```
2. Odoo 인증 API 확인
```bash
curl -s http://localhost:9000/health
curl -s http://localhost:9000/members
```
3. 로그인/JWT 발급 확인
```bash
curl -s -X POST http://localhost:9000/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"odoo_member1","password":"123456"}'
```
4. DB 포트 확인
```bash
docker ps --filter name=odoo-rdbms
```

## 체크 포인트
- `odoo-auth`와 `odoo-rdbms`가 모두 healthy 상태인지
- 로그인 응답에 토큰이 포함되는지
- 컨테이너 재시작 후 사용자 데이터가 유지되는지

## 과제(권장)
- 비밀번호 정책 변경 시 영향 범위를 문서화
- Odoo 계정 1개 추가 생성 후 로그인 검증
- 장애 시나리오(DB down) 재현 후 복구 절차 정리
