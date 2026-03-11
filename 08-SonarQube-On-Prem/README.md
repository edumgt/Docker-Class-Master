# 08장 - SonarQube 온프레미스 구축 (Dockerfile 기반)

## SonarQube 소개
SonarQube는 코드 품질과 보안 취약점을 정적 분석으로 점검하는 대표 오픈소스 플랫폼입니다.
CI 파이프라인에 연동하여 코드 스멜, 버그, 취약점을 Pull Request 단계에서 조기 탐지할 수 있습니다.

## 이 장의 목표
- SonarQube 컨테이너 이미지를 Dockerfile로 구성
- 코드 품질 대시보드를 온프레미스에서 운영
- Jenkins/GitLab CI와 연계 가능한 기본 환경 준비

## Dockerfile
```dockerfile
FROM sonarqube:community

ENV SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true

EXPOSE 9000
```

### 구성 포인트
- `sonarqube:community`: 무료 커뮤니티 에디션
- `9000`: SonarQube 웹 UI/REST API 포트
- 단일 노드 실습 환경을 위한 최소 설정 적용

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-sonarqube:1.0 .

# 2) 볼륨 생성
docker volume create sonarqube_data
docker volume create sonarqube_extensions
docker volume create sonarqube_logs

# 3) 컨테이너 실행
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  -v sonarqube_extensions:/opt/sonarqube/extensions \
  -v sonarqube_logs:/opt/sonarqube/logs \
  onprem-sonarqube:1.0
```

## 초기 접속
- URL: `http://localhost:9000`
- 기본 계정: `admin / admin` (최초 로그인 시 비밀번호 변경)

## 운영 팁
- 운영 환경은 외부 PostgreSQL 연동 권장
- 품질 게이트를 CI 파이프라인 실패 조건으로 연동하면 효과적

---

## 수업 보강 가이드
<!-- course-boost-onprem-v1 -->

### 수업 핵심 관점
- 단일 도구 설치가 목표가 아니라, "소스 -> CI -> 품질 -> 아티팩트 -> 배포" 체인을 완성하는 것이 목표입니다.
- 각 도구는 독립 서비스이면서도 네트워크/계정/권한/스토리지 정책으로 강하게 연결됩니다.

### 실습 운영 체크리스트
- 컨테이너 상태: `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`
- 볼륨 상태: `docker volume ls`
- 로그 확인: `docker logs <container> --tail 200`
- 리소스 점검: `docker stats --no-stream`

### 운영 안정화 과제(권장)
1. 컨테이너 재시작 후 데이터 유지 여부 검증
2. 관리자 계정/초기 비밀번호 변경 절차 문서화
3. 백업/복구 테스트(최소 1회)
4. 서비스 헬스체크/장애 알림 조건 정의

### 품질 평가 기준
- 단순 기동이 아니라 "실패 복구"까지 확인했는가
- 파이프라인 실행 기록과 품질 게이트 결과를 남겼는가
- 사내 도입을 가정한 최소 보안 설정(비밀번호/토큰/권한)을 반영했는가

### 다음 단계
- `11-Integrated-DevSecOps-Lab`로 확장하여 인증/시크릿/관측성을 포함한 운영형 실습으로 연결
