# 23. OnPrem Solution - Tryton

## 솔루션 개요
- 원본: https://github.com/tryton/tryton
- 목적: 모듈형 비즈니스 소프트웨어 Tryton의 컨테이너 운영 패턴을 학습합니다.
- 동기화 스크립트: `../_shared-onprem-core/sync-solutions.sh`

## Docker 수업 관점 학습 포인트
- PostgreSQL 기반 서비스의 기본 배포 패턴
- 서비스 간 DNS 이름(컨테이너 이름) 통신 원리
- 구성 변경 시 재배포/롤백 전략

## 실습 절차
1. 통합 스택 기동
```bash
cd ../_shared-onprem-core
./start.sh
```
2. Tryton 인증 API 확인
```bash
curl -s http://localhost:9004/health
curl -s http://localhost:9004/members
```
3. 로그인/JWT 발급 확인
```bash
curl -s -X POST http://localhost:9004/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"tryton_member1","password":"123456"}'
```
4. DB 컨테이너 상태 확인
```bash
docker ps --filter name=tryton-rdbms
```

## 체크 포인트
- 서비스 재시작(`docker restart tryton-auth`) 후 정상 복구되는지
- DB 의존 서비스가 준비되기 전에 뜰 때의 실패 로그를 해석할 수 있는지
- 런타임 설정 변경 시 필요한 재기동 범위를 판단할 수 있는지

## 과제(권장)
- Tryton 사용자 1건 추가/조회 시나리오 작성
- 로그 기반 장애 원인 분석 리포트 1건 작성
- 공통 인증 API 구조를 다른 솔루션에 재사용 가능한지 설계 의견 작성
