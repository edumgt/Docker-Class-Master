from __future__ import annotations

from pathlib import Path

from finance_rag import FinanceRAG


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    corpus_dir = base_dir / "corpus"
    rag = FinanceRAG(corpus_dir=corpus_dir)

    print("=== Python + 금융공학 RAG Lab ===")
    print("종료하려면 'exit' 입력")

    while True:
        question = input("\n질문> ").strip()
        if question.lower() in {"exit", "quit"}:
            print("랩을 종료합니다.")
            break
        if not question:
            print("질문을 입력해 주세요.")
            continue

        result = rag.ask(question)
        print("\n[답변]")
        print(result.answer)
        print("\n[근거 문서]")
        if not result.citations:
            print("- 없음")
        else:
            for citation in result.citations:
                print(f"- {citation}")


if __name__ == "__main__":
    main()
