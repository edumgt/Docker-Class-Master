# 흐름-1: Docker Hub에서 이미지 내려받아 실행

## 1. Docker 버전 확인 및 Docker Hub 로그인
```bash
docker version
docker login
```

## 2. Docker Hub에서 이미지 Pull
```bash
docker pull stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

## 3. 이미지 실행 및 애플리케이션 접속
- Docker Hub에서 이미지 이름을 복사해 실행합니다.
```bash
docker run --name app1 -p 80:8080 -d stacksimplify/dockerintro-springboot-helloworld-rest-api:1.0.0-RELEASE
```

### 이미지 목록 확인
```bash
docker image ls
```

### 브라우저 접속
- http://localhost/hello

![alt text](image.png)
![alt text](image-1.png)

## 참고: Apple Silicon(Mac) 환경
1. Apple Silicon용 Docker Desktop을 설치합니다.
   - https://docs.docker.com/desktop/mac/install/
2. 아래 명령으로 Nginx 컨테이너를 실행합니다.

```bash
docker run --name kube1 -p 80:80 --platform linux/amd64 -d stacksimplify/kubenginx:1.0.0
```

- http://localhost

### 예시 출력
```text
kalyanreddy@Kalyans-Mac-mini-2 ~ % docker run --name kube1 -p 80:80 --platform linux/amd64 -d  stacksimplify/kubenginx:1.0.0
370f238d97556813a4978572d24983d6aaf80d4300828a57f27cda3d3d8f0fec
kalyanreddy@Kalyans-Mac-mini-2 ~ % curl http://localhost
<!DOCTYPE html>
<html>
   <body style="background-color:lightgoldenrodyellow;">
      <h1>Welcome to Stack Simplify</h1>
      <p>Kubernetes Fundamentals Demo</p>
      <p>Application Version: V1</p>
   </body>
</html>%
kalyanreddy@Kalyans-Mac-mini-2 ~ %
```

## 4. 실행 중인 컨테이너 목록 확인
```bash
docker ps
docker ps -a
docker ps -a -q
```

### Docker Desktop 목록 확인(동일 내용)
![alt text](image-2.png)

## 5. 컨테이너 터미널 접속
```bash
docker exec -it <container-name> /bin/sh
```

![alt text](image-3.png)

### 예시
```text
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it app1 /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  322 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 May  9  2019 run
drwxr-xr-x    2 root     root          4096 May  9  2019 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals> docker exec -it 300039d4d0f39ce638d9678765d09ab92705c42544b6920f30f5e2c14890cfca /bin/sh
/ # ls -al
total 18840
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 .
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 ..
-rwxr-xr-x    1 root     root             0 Jun 29 01:31 .dockerenv
-rw-r--r--    1 root     root      19225249 Nov 23  2019 app.jar
drwxr-xr-x    2 root     root          4096 May  9  2019 bin
drwxr-xr-x    5 root     root           340 Jun 29 01:31 dev
drwxr-xr-x    1 root     root          4096 Jun 29 01:31 etc
drwxr-xr-x    2 root     root          4096 May  9  2019 home
drwxr-xr-x    1 root     root          4096 May 11  2019 lib
drwxr-xr-x    5 root     root          4096 May  9  2019 media
drwxr-xr-x    2 root     root          4096 May  9  2019 mnt
drwxr-xr-x    2 root     root          4096 May  9  2019 opt
dr-xr-xr-x  319 root     root             0 Jun 29 01:31 proc
drwx------    1 root     root          4096 Jun 29 01:36 root
drwxr-xr-x    2 root     root          4096 Jun 29 01:31 run
drwxr-xr-x    2 root     root          4096 Jun 29 01:31 sbin
drwxr-xr-x    2 root     root          4096 May  9  2019 srv
dr-xr-xr-x   13 root     root             0 Jun 29 01:31 sys
drwxrwxrwt    5 root     root          4096 Jun 29 01:31 tmp
drwxr-xr-x    1 root     root          4096 May 11  2019 usr
drwxr-xr-x    1 root     root          4096 May  9  2019 var
/ # exit
PS C:\edumgt-java-education\docker-fundamentals>
```

## 6. 컨테이너 중지 및 시작
```bash
docker stop <container-name>
docker start <container-name>
```

## 7. 컨테이너 삭제
```bash
docker stop <container-name>
docker rm <container-name>
```

## 8. 이미지 삭제
```bash
docker images
docker rmi <image-id>
```

## Docker Desktop에서 상태 확인
![alt text](image-4.png)
- `:` 클릭 → 상세 뷰 클릭

![alt text](image-5.png)

---

## 수업 보강 가이드
<!-- course-boost-foundation-v1 -->

### 학습 목표(보강)
- Docker CLI를 단순 암기하지 않고, "이미지/컨테이너/볼륨/네트워크"의 관계로 설명할 수 있다.
- 동일 실습을 `run` 단건 명령과 `compose` 방식으로 모두 재현할 수 있다.
- 장애가 났을 때 `logs`, `inspect`, `exec`로 원인을 1차 분석할 수 있다.

### 실습 전 체크리스트
- `docker version` / `docker info`가 정상 출력되는지 확인
- 로컬에 사용 가능한 디스크 여유 10GB 이상 확보
- 포트 충돌 확인: `80`, `443`, `8080`, `3306`, `5432`

### 수업 운영(권장)
1. 개념 설명 20분: 컨테이너와 VM의 차이, 레이어/캐시 개념
2. 데모 20분: 강사가 명령 실행 후 결과 해석 시연
3. 실습 60분: 학습자 직접 실행 + 체크포인트 제출
4. 회고 20분: 실패 사례 공유, 재현 가능한 명령 정리

### 제출물(권장)
- 실행 명령 히스토리(중요 명령 10개 이상)
- `docker ps -a`, `docker images` 결과 캡처
- 장애 1건 이상 재현 + 해결 과정(runbook 10줄 이상)

### 평가 포인트
- 명령 실행 자체보다 "왜 이 명령을 썼는지" 설명 가능한지
- 동일 결과를 다른 방법(run/compose)으로 재현 가능한지
- 정리 문서에 복구 절차가 포함되어 있는지
