from flask import Flask  # Flask 웹 프레임워크에서 앱 생성 클래스 임포트

app = Flask(__name__)
# Flask 애플리케이션 인스턴스 생성
# __name__: 현재 모듈 이름을 전달하여 Flask가 리소스 경로를 올바르게 찾도록 설정


@app.get("/")  # HTTP GET 요청을 "/" 경로에 매핑하는 라우트 데코레이터
def hello():
    """루트 경로 요청에 대한 JSON 응답을 반환합니다. Trivy 취약점 스캔 데모용 앱입니다."""
    return {"message": "Trivy scan demo app"}
    # 딕셔너리를 반환하면 Flask가 자동으로 JSON 응답으로 변환 (Content-Type: application/json)


if __name__ == "__main__":
    # 이 파일이 직접 실행될 때만 아래 코드 실행 (모듈로 임포트 시 실행하지 않음)
    app.run(host="0.0.0.0", port=5000)
    # host="0.0.0.0": 모든 네트워크 인터페이스에서 수신 (컨테이너 외부 접근 허용)
    # port=5000: 5000번 포트에서 수신
