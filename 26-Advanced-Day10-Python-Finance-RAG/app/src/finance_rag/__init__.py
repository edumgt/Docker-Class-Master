"""Finance engineering RAG lab package.
이 패키지는 금융공학 문서 기반 RAG(Retrieval-Augmented Generation) 실습 모듈입니다.
corpus 폴더의 마크다운 파일을 로드하고 TF-IDF 검색으로 질의응답을 제공합니다.
"""

from .rag import FinanceRAG  # 하위 모듈 rag.py에서 메인 클래스를 임포트하여 패키지 최상위에 노출

__all__ = ["FinanceRAG"]
# __all__: 외부에서 'from finance_rag import *' 사용 시 노출할 공개 API 목록 정의
