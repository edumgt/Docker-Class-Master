# 가상화(VM) vs 컨테이너(Container)

가상화와 컨테이너화는 모두 애플리케이션을 격리하고 자원을 효율적으로 쓰기 위한 기술이지만, 구조와 동작 방식에 차이가 있습니다. 아래에서 핵심 차이를 요약하고, 참고 이미지를 함께 제공합니다.

## 한눈에 보는 차이

| 항목 | 가상화 (VM) | 컨테이너 (Container) |
| --- | --- | --- |
| 격리 수준 | 하드웨어 수준(완전 격리) | 프로세스 수준(OS 커널 공유) |
| 운영 체제 | 각 VM에 게스트 OS 필요 | 호스트 OS 커널 공유 |
| 자원 오버헤드 | 높음(게스트 OS 부팅/자원 소비) | 낮음(경량/빠른 시작) |
| 시작 시간 | 수분 | 수초 |
| 이미지 크기 | 수 GB | 수 MB |
| 이식성 | 하이퍼바이저 의존적 | 높음(OCI 표준 준수 시) |
| 보안 | 강력(완전 격리) | 상대적 약함(커널 취약점 공유 가능) |
| 적합 용도 | 다른 OS 실행, 강력한 격리 | 마이크로서비스, 빠른 배포/스케일링 |

> 가상화는 강력한 격리가 필요할 때 유용하며, 컨테이너화는 자원 효율성과 배포 속도를 우선할 때 적합합니다. 두 기술은 상호 보완적으로 사용될 수 있습니다(예: VM 내부에서 컨테이너 실행).

## 아키텍처 비교 다이어그램

아래 이미지는 VM과 컨테이너 아키텍처의 차이를 시각적으로 보여줍니다.

![가상화와 컨테이너 아키텍처 비교](https://github.com/user-attachments/assets/c4956919-0498-49b1-a29d-a2a2308816c7)

![VM vs 컨테이너 비교 요약](https://github.com/user-attachments/assets/f8e8b755-d21e-4561-aa67-cf8077f52dee)

![컨테이너 런타임 구조 예시](https://github.com/user-attachments/assets/8e8c65b9-3386-4777-bf55-8229ba7cc7e6)

## Open Container Initiative (OCI) 개요

Open Container Initiative(OCI)는 2015년 Docker 주도로 Linux Foundation 산하에 설립된 오픈 거버넌스 프로젝트입니다. 컨테이너 기술의 **벤더 독립성**과 **상호 운용성**을 높이기 위해 표준을 정의합니다.

### 핵심 사양

- **Image Specification (image-spec)**: 컨테이너 이미지 형식(매니페스트, 레이어, 구성)을 정의
- **Runtime Specification (runtime-spec)**: 컨테이너 실행 환경과 라이프사이클(create/start/stop/delete)을 정의
- **Distribution Specification (distribution-spec)**: 이미지 레지스트리와의 API 프로토콜을 정의

이 표준들은 Docker, containerd, CRI-O 등 주요 런타임에서 채택되어 컨테이너 이식성과 안정성을 높입니다.

## 참고 링크

- https://blog.bytebytego.com
- https://netapp.com
- https://medium.com
- https://www.prnewswire.com
