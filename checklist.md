### error 사안
```bash
root@DESKTOP-O3O4N28:/home/Docker-Class-Master# docker image ls

The command 'docker' could not be found in this WSL 2 distro.
We recommend to activate the WSL integration in Docker Desktop settings.

For details about using Docker Desktop with WSL 2, visit:

https://docs.docker.com/go/wsl2/

root@DESKTOP-O3O4N28:/home/Docker-Class-Master#
```
---
```
문제를 재현하기보다 먼저 이 저장소가 Docker Desktop + WSL 기준으로 안내되어 있는지 확인하고, 지금 에러가 왜 나는지 정리해드릴게요. 그다음 바로 실행 가능한 해결 순서로 안내하겠습니다.
백그라운드 터미널이 pwd 명령으로 완료됨
검색 1건 탐색 마침
에러 원인은 거의 확실합니다. 이 WSL 배포판 안에 Docker CLI가 없는 게 아니라, Docker Desktop과의 WSL 연동이 아직 이 distro에 붙지 않은 상태로 보입니다.
```
---
```
지금 메시지는 Docker 명령 자체가 고장난 게 아니라, 이 WSL 배포판이 Docker Desktop과 아직 연결되지 않았다는 뜻입니다.

해결 순서는 아래대로 하면 됩니다.

Windows에서 Docker Desktop 실행
Docker Desktop에서 Settings > Resources > WSL Integration
Enable integration with my default WSL distro 체크
지금 쓰는 distro도 체크
보통 Ubuntu, Ubuntu-22.04 같은 이름입니다
Apply & Restart
WSL 터미널을 완전히 닫았다가 다시 열기
```

---
```powershell
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "com.docker.backend" -Force -ErrorAction SilentlyContinue
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```