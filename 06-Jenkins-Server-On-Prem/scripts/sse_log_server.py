#!/usr/bin/env python3
# 이 스크립트는 로그 파일을 SSE(Server-Sent Events) 방식으로 실시간 스트리밍하는 HTTP 서버입니다.
# Jenkins 파이프라인 등의 설치 로그를 브라우저에서 실시간으로 확인할 때 사용됩니다.

import argparse  # 커맨드라인 인자 파싱 라이브러리
import os        # 운영체제 파일/경로 유틸리티
import time      # sleep 등 시간 관련 유틸리티
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
# BaseHTTPRequestHandler: HTTP 요청 핸들러 기반 클래스
# ThreadingHTTPServer: 요청마다 별도 스레드를 생성하는 HTTP 서버 (동시 다중 클라이언트 지원)


class SSEHandler(BaseHTTPRequestHandler):
    """SSE(Server-Sent Events) 프로토콜로 로그를 스트리밍하는 HTTP 요청 핸들러."""

    log_file = None  # 스트리밍할 로그 파일 경로 (클래스 변수 - 모든 인스턴스에서 공유)

    def do_GET(self):
        """GET 요청을 처리하는 메서드. /events 경로에서만 SSE 스트림을 제공합니다."""
        if self.path not in ("/events", "/events/"):
            # /events 또는 /events/ 외의 경로로 요청 시 404 반환
            self.send_response(404)       # HTTP 상태 코드 404(Not Found) 전송
            self.end_headers()            # 헤더 전송 완료
            self.wfile.write(b"Not Found")  # 응답 본문에 "Not Found" 텍스트 작성
            return                        # 이후 처리 중단

        # SSE 스트림을 위한 HTTP 응답 헤더 설정
        self.send_response(200)                              # HTTP 200 OK 상태 코드 전송
        self.send_header("Content-Type", "text/event-stream")  # SSE 전용 MIME 타입 설정
        self.send_header("Cache-Control", "no-cache")          # 브라우저 캐시 비활성화 (실시간성 보장)
        self.send_header("Connection", "keep-alive")           # 연결 유지 (스트리밍을 위해 연결을 끊지 않음)
        self.end_headers()                                     # 헤더 전송 완료

        # 로그 파일이 생성될 때까지 대기 (파이프라인이 아직 시작 전일 수 있음)
        while not os.path.exists(self.log_file):
            time.sleep(0.5)  # 0.5초 간격으로 파일 존재 여부 재확인

        try:
            with open(self.log_file, "r", encoding="utf-8", errors="replace") as f:
                # encoding="utf-8": UTF-8 인코딩으로 파일 읽기
                # errors="replace": 디코딩 오류 발생 시 대체 문자(?)로 처리
                # 파일 처음부터 스트리밍하여 나중에 접속한 클라이언트도 전체 로그를 볼 수 있도록 함
                while True:
                    line = f.readline()  # 파일에서 한 줄씩 읽기
                    if line:
                        # 읽은 줄이 있으면 SSE 형식으로 클라이언트에 전송
                        payload = line.rstrip("\r\n")  # 줄 끝의 캐리지 리턴(\r) 및 개행(\n) 제거
                        self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                        # SSE 형식: "data: <내용>\n\n" (이중 개행이 이벤트 구분자)
                        self.wfile.flush()  # 버퍼를 즉시 클라이언트로 전송 (실시간성 보장)
                    else:
                        # 새 줄이 없으면 0.3초 대기 후 재시도 (새 로그 발생 대기)
                        time.sleep(0.3)
        except (BrokenPipeError, ConnectionResetError):
            # 클라이언트가 연결을 끊은 경우 조용히 종료
            return

    def log_message(self, fmt, *args):
        """기본 HTTP 서버 콘솔 로그 출력을 억제합니다 (불필요한 stderr 출력 방지)."""
        return  # 아무것도 출력하지 않음


def main():
    """서버 진입점: 인자 파싱 후 SSE HTTP 서버를 시작합니다."""
    parser = argparse.ArgumentParser(description="SSE log streamer")  # 인자 파서 생성
    parser.add_argument("--host", default="127.0.0.1")                # 바인딩 호스트 (기본값: 루프백)
    parser.add_argument("--port", type=int, default=18080)            # 수신 포트 (기본값: 18080)
    parser.add_argument("--log-file", required=True)                  # 스트리밍할 로그 파일 경로 (필수)
    args = parser.parse_args()                                         # 인자 파싱 실행

    SSEHandler.log_file = args.log_file              # 파싱된 로그 파일 경로를 핸들러 클래스에 설정
    server = ThreadingHTTPServer((args.host, args.port), SSEHandler)
    # ThreadingHTTPServer: 지정 호스트:포트에서 SSEHandler를 사용하는 멀티스레드 서버 생성
    server.serve_forever()                           # 서버를 무한 루프로 실행 (Ctrl+C로 종료)


if __name__ == "__main__":
    main()  # 이 파일이 직접 실행될 때만 main() 호출 (모듈로 임포트 시에는 실행하지 않음)
