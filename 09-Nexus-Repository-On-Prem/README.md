# 09장 - Nexus Repository 온프레미스 구축 (Dockerfile 기반)

## Nexus Repository 소개
Nexus Repository OSS는 Maven, npm, Docker Registry 프록시/호스팅 등 다양한 아티팩트 저장소를 제공하는 오픈소스 도구입니다.
CI 빌드 산출물을 중앙 저장소로 관리하여 배포 추적성과 재현성을 높일 수 있습니다.

## 이 장의 목표
- Dockerfile로 Nexus Repository 이미지 생성
- 온프레미스 아티팩트 저장소를 컨테이너로 운영
- 사내 CI/CD 파이프라인의 패키지 허브 역할 구성

## Dockerfile
```dockerfile
FROM sonatype/nexus3:3.70.1

EXPOSE 8081
```

### 구성 포인트
- `sonatype/nexus3` 공식 이미지 사용
- `8081` 포트로 Nexus UI 및 Repository API 제공

## 빌드 및 실행
```bash
# 1) 이미지 빌드
docker build -t onprem-nexus:1.0 .

# 2) 볼륨 생성
docker volume create nexus_data

# 3) 컨테이너 실행
docker run -d --name nexus3 \
  -p 8082:8081 \
  -v nexus_data:/nexus-data \
  onprem-nexus:1.0
```

## 초기 관리자 비밀번호 확인
```bash
docker exec nexus3 cat /nexus-data/admin.password
```

## 운영 팁
- Blob Store 백업 정책을 별도로 구성
- Docker Hosted/Proxy repository를 분리해 캐시와 사설 이미지를 함께 운영
- 정기적인 컴포넌트 정리(Cleanup Policy)로 저장소 비대화 방지

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
