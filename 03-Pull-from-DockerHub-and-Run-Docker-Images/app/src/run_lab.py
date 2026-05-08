from __future__ import annotations  # 타입 힌트 문자열 지연 평가 (Python 3.10 이전 호환성)

from pathlib import Path  # 파일 경로 조작을 위한 객체지향 API

from finance_rag import FinanceRAG  # 금융공학 RAG 모듈에서 메인 클래스 임포트


def main() -> None:
    """금융공학 RAG 대화형 실습 루프를 실행하는 진입점 함수."""
    base_dir = Path(__file__).resolve().parent.parent
    # __file__: 현재 파일(run_lab.py)의 경로
    # .resolve(): 절대 경로로 변환 (심볼릭 링크 해석 포함)
    # .parent.parent: run_lab.py → src → app 디렉토리 (두 단계 위)

    corpus_dir = base_dir / "corpus"
    # corpus_dir: 금융 문서들이 저장된 corpus 폴더 경로 (app/corpus/)

    rag = FinanceRAG(corpus_dir=corpus_dir)
    # FinanceRAG 인스턴스 생성: corpus 폴더의 문서들을 로드하고 TF-IDF 인덱스를 구축

    print("=== Python + 금융공학 RAG Lab ===")  # 실습 시작 안내 메시지 출력
    print("종료하려면 'exit' 입력")              # 종료 방법 안내 메시지 출력

    while True:  # 사용자 입력을 반복적으로 처리하는 무한 루프
        question = input("\n질문> ").strip()
        # input(): 사용자로부터 질문 텍스트를 입력받음
        # .strip(): 앞뒤 공백 제거

        if question.lower() in {"exit", "quit"}:
            # 사용자가 'exit' 또는 'quit'(대소문자 무관)를 입력하면 루프 종료
            print("랩을 종료합니다.")  # 종료 메시지 출력
            break                      # while 루프 탈출

        if not question:
            # 빈 문자열이 입력된 경우 질문 재입력 요청
            print("질문을 입력해 주세요.")  # 안내 메시지 출력
            continue                        # 루프 처음으로 돌아가 다시 입력 받음

        result = rag.ask(question)
        # RAG 시스템에 질문을 전달하고 RAGResult(answer, citations)를 받음

        print("\n[답변]")         # 답변 섹션 헤더 출력
        print(result.answer)     # TF-IDF 검색 기반으로 생성된 답변 텍스트 출력

        print("\n[근거 문서]")    # 근거 문서 섹션 헤더 출력
        if not result.citations:
            print("- 없음")      # 관련 문서가 없을 경우 "없음" 출력
        else:
            for citation in result.citations:
                print(f"- {citation}")  # 각 근거 문서(파일명 > 섹션 > 점수)를 출력


if __name__ == "__main__":
    main()  # 이 파일이 직접 실행될 때만 main() 호출 (모듈로 임포트 시 실행하지 않음)
