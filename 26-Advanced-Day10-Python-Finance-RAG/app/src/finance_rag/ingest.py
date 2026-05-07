from __future__ import annotations  # 타입 힌트 문자열 지연 평가 (Python 3.10 이전 호환성)

from dataclasses import dataclass  # 불변 데이터 클래스 생성을 위한 데코레이터
from pathlib import Path           # 파일 경로 조작을 위한 객체지향 API


@dataclass(frozen=True)  # frozen=True: 인스턴스 생성 후 필드 수정 불가 (불변 객체)
class Chunk:
    """문서에서 추출한 단일 텍스트 청크(조각)를 표현하는 불변 데이터 클래스."""
    source: str   # 원본 파일명 (예: "interest_rate.md")
    section: str  # 문서 내 섹션 제목 (예: "금리 계산 방법")
    text: str     # 실제 텍스트 내용 (정규화된 단일 단락)


def _normalize_text(text: str) -> str:
    """텍스트 내 연속 공백을 단일 공백으로 정규화합니다."""
    return " ".join(text.split())
    # text.split(): 공백/탭/개행 기준으로 단어 분리 (연속 공백도 처리)
    # " ".join(...): 단어들을 단일 공백으로 재조합


def _split_by_section(content: str) -> list[tuple[str, str]]:
    """마크다운 문서를 '## 섹션' 단위로 분리하여 (섹션 제목, 내용) 튜플 목록을 반환합니다."""
    sections: list[tuple[str, str]] = []   # 완성된 (섹션 제목, 내용) 쌍을 저장하는 리스트
    current_title = "Introduction"          # 첫 '## 섹션' 이전 내용의 기본 섹션 제목
    current_lines: list[str] = []           # 현재 섹션의 줄 목록 (누적용)

    for line in content.splitlines():       # 문서를 줄 단위로 순회
        if line.startswith("## "):
            # '## '로 시작하는 줄은 새 섹션의 시작
            if current_lines:
                # 이전 섹션에 내용이 있으면 저장
                sections.append((current_title, "\n".join(current_lines).strip()))
                current_lines = []          # 다음 섹션을 위해 줄 버퍼 초기화
            current_title = line.removeprefix("## ").strip()
            # removeprefix("## "): "## "를 제거하여 순수 섹션 제목 추출
            # .strip(): 앞뒤 공백 제거
            continue                        # 제목 줄 자체는 내용으로 포함하지 않음

        if line.startswith("# "):
            # '# '로 시작하는 줄은 문서 최상위 제목 (H1) - 내용에서 제외
            continue                        # H1 제목 줄은 건너뜀

        current_lines.append(line)          # 일반 내용 줄은 현재 섹션 버퍼에 추가

    if current_lines:
        # 마지막 섹션(루프 종료 후 남은 내용) 저장
        sections.append((current_title, "\n".join(current_lines).strip()))

    return [(title, text) for title, text in sections if text]
    # 내용이 빈 섹션은 필터링하여 제외


def _split_paragraphs(section_text: str, max_chars: int = 280) -> list[str]:
    """섹션 텍스트를 최대 max_chars 글자 단위의 단락 청크로 분할합니다."""
    chunks: list[str] = []  # 분할된 단락 청크들을 저장하는 리스트
    paragraph = " ".join(line.strip() for line in section_text.splitlines() if line.strip())
    # 섹션의 모든 줄을 하나의 단일 단락 문자열로 합침 (빈 줄 제외)

    if not paragraph:
        return chunks  # 내용이 없으면 빈 리스트 반환

    while len(paragraph) > max_chars:
        # 단락이 최대 글자 수를 초과하는 동안 분할 반복
        split_point = paragraph.rfind(". ", 0, max_chars)
        # rfind: max_chars 이전에서 마지막 '. '(문장 끝)을 찾아 자연스러운 분할점 결정

        if split_point == -1:
            # '. '을 찾지 못하면 공백 위치에서 분할 시도
            split_point = paragraph.rfind(" ", 0, max_chars)

        if split_point == -1:
            # 공백도 없으면 정확히 max_chars 위치에서 강제 분할
            split_point = max_chars

        piece = paragraph[: split_point + 1].strip()
        # split_point+1까지 잘라내어 분할 청크 생성 ('. ' 포함)

        if piece:
            chunks.append(piece)  # 내용이 있는 청크만 추가

        paragraph = paragraph[split_point + 1 :].strip()
        # 분할한 부분을 제거하고 남은 텍스트로 계속 처리

    if paragraph:
        chunks.append(paragraph)  # 마지막 남은 단락 조각 추가

    return chunks  # 분할된 단락 청크 리스트 반환


def load_chunks(corpus_dir: Path) -> list[Chunk]:
    """corpus 디렉토리의 모든 마크다운 파일을 읽어 Chunk 목록으로 반환합니다."""
    if not corpus_dir.exists() or not corpus_dir.is_dir():
        # corpus 디렉토리가 존재하지 않거나 디렉토리가 아닌 경우 예외 발생
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    all_chunks: list[Chunk] = []                            # 전체 청크 저장 리스트
    for file_path in sorted(corpus_dir.glob("*.md")):
        # corpus_dir 내의 모든 .md 파일을 정렬 순으로 처리 (재현성 보장)
        content = file_path.read_text(encoding="utf-8")    # 파일 전체 내용을 UTF-8로 읽기
        for section, text in _split_by_section(content):  # 마크다운을 섹션 단위로 분리
            for paragraph in _split_paragraphs(text):     # 각 섹션을 단락 청크로 분리
                normalized = _normalize_text(paragraph)   # 텍스트 정규화 (연속 공백 정리)
                if normalized:
                    # 정규화 후 내용이 있는 청크만 저장
                    all_chunks.append(
                        Chunk(
                            source=file_path.name,  # 원본 파일명 (경로 제외)
                            section=section,         # 섹션 제목
                            text=normalized,         # 정규화된 텍스트 내용
                        )
                    )

    if not all_chunks:
        # 처리 결과 청크가 하나도 없으면 예외 발생 (빈 corpus 방지)
        raise ValueError("No chunks were created from corpus files.")

    return all_chunks  # 모든 청크 리스트 반환
