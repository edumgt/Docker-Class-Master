import os           # 환경 변수 읽기용 표준 라이브러리
import time         # DB 재연결 대기(sleep)용 표준 라이브러리
from contextlib import asynccontextmanager  # 비동기 컨텍스트 매니저 생성 데코레이터
from enum import Enum          # 열거형 클래스 정의용
from pathlib import Path as FilePath  # 파일 경로 객체 (내장 Path와 이름 충돌 방지를 위해 별칭 사용)

import psycopg  # PostgreSQL 비동기/동기 드라이버 (psycopg3)
from fastapi import FastAPI, HTTPException, Path  # FastAPI 앱, HTTP 예외, 경로 파라미터
from fastapi.responses import FileResponse    # 파일을 HTTP 응답으로 반환
from fastapi.staticfiles import StaticFiles   # 정적 파일(CSS, JS 등) 서빙
from pydantic import BaseModel, Field         # 요청/응답 데이터 모델 및 필드 설정


# 환경 변수에서 DB 접속 정보를 읽어옴 (기본값은 로컬 개발 환경용)
DB_HOST = os.getenv("DB_HOST", "db")              # DB 서버 호스트명 (컨테이너 이름 "db" 기본값)
DB_PORT = int(os.getenv("DB_PORT", "5432"))       # DB 포트 (PostgreSQL 기본 포트 5432)
DB_NAME = os.getenv("DB_NAME", "app")             # 접속할 DB 이름
DB_USER = os.getenv("DB_USER", "app")             # DB 사용자명
DB_PASSWORD = os.getenv("DB_PASSWORD", "app1234") # DB 비밀번호
STATIC_DIR = FilePath(__file__).parent / "static" # 정적 파일 디렉토리 경로 (이 파일 기준 ./static)


def get_conninfo() -> str:
    """PostgreSQL 접속 문자열(DSN)을 생성하여 반환합니다."""
    return (
        f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
        f"user={DB_USER} password={DB_PASSWORD}"
    )  # psycopg.connect()에서 사용하는 libpq 형식의 접속 문자열


class OrderStatus(str, Enum):
    """주문 상태를 나타내는 열거형. str을 상속하여 JSON 직렬화 시 문자열로 처리됩니다."""
    created = "CREATED"       # 주문 생성됨
    completed = "COMPLETED"   # 주문 완료됨


class DeliveryStatus(str, Enum):
    """배송 상태를 나타내는 열거형."""
    requested = "REQUESTED"    # 배송 요청됨
    preparing = "PREPARING"    # 배송 준비 중
    in_transit = "IN_TRANSIT"  # 배송 중
    delivered = "DELIVERED"    # 배송 완료


class OrderCreate(BaseModel):
    """주문 생성 요청 데이터 모델 (POST /orders 요청 본문)."""
    customer_name: str = Field(..., examples=["Alice"])          # 고객명 (필수)
    product_name: str = Field(..., examples=["Docker Handbook"]) # 상품명 (필수)
    quantity: int = Field(..., ge=1, examples=[2])
    # 수량 (필수, ge=1: 1 이상의 정수만 허용)


class OrderResponse(BaseModel):
    """주문 응답 데이터 모델 (API 응답용)."""
    id: int              # 주문 고유 ID
    customer_name: str   # 고객명
    product_name: str    # 상품명
    quantity: int        # 수량
    status: OrderStatus  # 주문 상태 (CREATED / COMPLETED)
    created_at: str      # 주문 생성 시각 (ISO 8601 문자열)


class DeliveryCreate(BaseModel):
    """배송 요청 생성 데이터 모델 (POST /orders/{id}/delivery-request 요청 본문)."""
    address: str = Field(..., examples=["Seoul, Gangnam-gu"])  # 배송 주소 (필수)


class DeliveryResponse(BaseModel):
    """배송 응답 데이터 모델 (API 응답용)."""
    id: int                    # 배송 고유 ID
    order_id: int              # 연관 주문 ID
    address: str               # 배송 주소
    status: DeliveryStatus     # 배송 상태
    requested_at: str          # 배송 요청 시각 (ISO 8601 문자열)
    delivered_at: str | None   # 배송 완료 시각 (미완료 시 None)


def to_order_response(row: tuple) -> OrderResponse:
    """DB 조회 결과 튜플을 OrderResponse 모델로 변환합니다."""
    return OrderResponse(
        id=row[0],                        # 첫 번째 컬럼: 주문 ID
        customer_name=row[1],             # 두 번째 컬럼: 고객명
        product_name=row[2],              # 세 번째 컬럼: 상품명
        quantity=row[3],                  # 네 번째 컬럼: 수량
        status=row[4],                    # 다섯 번째 컬럼: 주문 상태 문자열
        created_at=row[5].isoformat(),    # 여섯 번째 컬럼: datetime → ISO 8601 문자열 변환
    )


def to_delivery_response(row: tuple) -> DeliveryResponse:
    """DB 조회 결과 튜플을 DeliveryResponse 모델로 변환합니다."""
    return DeliveryResponse(
        id=row[0],                                                 # 배송 ID
        order_id=row[1],                                           # 주문 ID
        address=row[2],                                            # 배송 주소
        status=row[3],                                             # 배송 상태 문자열
        requested_at=row[4].isoformat(),                           # 배송 요청 시각 → ISO 8601 변환
        delivered_at=row[5].isoformat() if row[5] else None,       # 배송 완료 시각 (없으면 None)
    )


def init_db() -> None:
    """애플리케이션 시작 시 DB 테이블을 초기화합니다. DB 준비가 될 때까지 최대 20회 재시도합니다."""
    last_error = None          # 마지막으로 발생한 예외를 저장 (최종 실패 시 재발생)
    for _ in range(20):        # 최대 20번 재시도 (DB 컨테이너 기동 대기)
        try:
            with psycopg.connect(get_conninfo()) as conn:  # DB 연결
                with conn.cursor() as cur:                  # 커서 생성
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS orders (
                            id SERIAL PRIMARY KEY,
                            customer_name TEXT NOT NULL,
                            product_name TEXT NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity > 0),
                            status TEXT NOT NULL DEFAULT 'CREATED',
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        )
                        """
                        # orders 테이블 생성 (없을 경우에만):
                        # id: 자동 증가 기본키
                        # customer_name/product_name: 필수 텍스트
                        # quantity: 양수 정수만 허용
                        # status: 기본값 'CREATED'
                        # created_at: 타임존 포함 현재 시각 자동 입력
                    )
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS deliveries (
                            id SERIAL PRIMARY KEY,
                            order_id INTEGER NOT NULL UNIQUE REFERENCES orders(id) ON DELETE CASCADE,
                            address TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'REQUESTED',
                            requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            delivered_at TIMESTAMPTZ
                        )
                        """
                        # deliveries 테이블 생성 (없을 경우에만):
                        # order_id: orders.id 참조 외래키, 유니크(1주문=1배송), CASCADE 삭제
                        # status: 기본값 'REQUESTED'
                        # delivered_at: 배송 완료 시각 (NULL 허용)
                    )
                conn.commit()  # 테이블 생성 트랜잭션 커밋
            return             # 성공 시 즉시 반환
        except psycopg.OperationalError as exc:
            # DB 접속 실패(아직 기동 중) 시 2초 대기 후 재시도
            last_error = exc   # 에러 저장
            time.sleep(2)      # 2초 대기
    raise last_error           # 20번 모두 실패하면 마지막 예외를 발생시켜 앱 기동 중단


@asynccontextmanager
async def lifespan(_: FastAPI):
    """FastAPI 앱의 수명 주기 관리: 시작 시 DB 초기화를 수행합니다."""
    init_db()  # 앱 시작 시 DB 테이블 초기화 실행
    yield      # 이 지점에서 앱이 실행됨 (종료 시 추가 정리 로직이 있다면 yield 이후에 작성)


app = FastAPI(
    title="Order Delivery API",           # API 제목 (Swagger UI에 표시)
    description=(
        "주문 생성, 배송 요청, 배송 완료 프로세스를 실습하는 FastAPI 예제입니다. "
        "Swagger UI는 /docs, OpenAPI 스키마는 /openapi.json 에서 확인할 수 있습니다."
    ),  # API 설명
    version="1.0.0",                      # API 버전
    lifespan=lifespan,                    # 수명 주기 핸들러 등록
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# /static 경로로 정적 파일 서빙 (CSS, JS, 이미지 등)


@app.get("/", include_in_schema=False)  # OpenAPI 문서에서 제외 (내부용 라우트)
def index() -> FileResponse:
    """루트 경로 접속 시 정적 index.html 페이지를 반환합니다."""
    return FileResponse(STATIC_DIR / "index.html")  # index.html 파일을 HTTP 응답으로 반환


@app.get("/health", tags=["system"], summary="서비스 상태 확인")
def health() -> dict[str, str]:
    """헬스체크 엔드포인트. 서비스 정상 동작 여부를 확인합니다."""
    return {"status": "ok"}  # 단순 상태 응답 반환


@app.get(
    "/orders",
    tags=["orders"],                       # Swagger UI 태그 분류
    summary="주문 목록 조회",               # 엔드포인트 요약 설명
    response_model=list[OrderResponse],    # 응답 스키마 정의
)
def list_orders() -> list[OrderResponse]:
    """모든 주문을 최신순(ID 내림차순)으로 조회하여 반환합니다."""
    with psycopg.connect(get_conninfo()) as conn:   # DB 연결
        with conn.cursor() as cur:                   # 커서 생성
            cur.execute(
                """
                SELECT id, customer_name, product_name, quantity, status, created_at
                FROM orders
                ORDER BY id DESC
                """
                # orders 테이블에서 모든 컬럼을 ID 내림차순으로 조회
            )
            rows = cur.fetchall()  # 모든 조회 결과를 리스트로 가져옴

    return [to_order_response(row) for row in rows]
    # 각 DB 행을 OrderResponse 모델로 변환하여 리스트 반환


@app.post(
    "/orders",
    tags=["orders"],
    summary="주문 생성",
    response_model=OrderResponse,
    status_code=201,  # 생성 성공 시 HTTP 201 Created 반환
)
def create_order(payload: OrderCreate) -> OrderResponse:
    """새 주문을 생성하고 생성된 주문 정보를 반환합니다."""
    with psycopg.connect(get_conninfo()) as conn:  # DB 연결
        with conn.cursor() as cur:                  # 커서 생성
            cur.execute(
                """
                INSERT INTO orders (customer_name, product_name, quantity)
                VALUES (%s, %s, %s)
                RETURNING id, customer_name, product_name, quantity, status, created_at
                """,
                (payload.customer_name, payload.product_name, payload.quantity),
                # %s 플레이스홀더로 SQL 인젝션 방지 (파라미터 바인딩)
                # RETURNING: 삽입된 행의 데이터를 즉시 반환
            )
            row = cur.fetchone()  # 삽입된 주문 데이터 한 행을 가져옴
        conn.commit()             # 트랜잭션 커밋 (데이터 영구 저장)

    return to_order_response(row)  # DB 행을 응답 모델로 변환 후 반환


@app.get(
    "/deliveries",
    tags=["deliveries"],
    summary="배송 목록 조회",
    response_model=list[DeliveryResponse],
)
def list_deliveries() -> list[DeliveryResponse]:
    """모든 배송을 최신순(ID 내림차순)으로 조회하여 반환합니다."""
    with psycopg.connect(get_conninfo()) as conn:  # DB 연결
        with conn.cursor() as cur:                  # 커서 생성
            cur.execute(
                """
                SELECT id, order_id, address, status, requested_at, delivered_at
                FROM deliveries
                ORDER BY id DESC
                """
                # deliveries 테이블에서 모든 컬럼을 ID 내림차순으로 조회
            )
            rows = cur.fetchall()  # 모든 조회 결과를 가져옴

    return [to_delivery_response(row) for row in rows]
    # 각 DB 행을 DeliveryResponse 모델로 변환하여 리스트 반환


@app.post(
    "/orders/{order_id}/delivery-request",
    tags=["deliveries"],
    summary="배송 요청 생성",
    response_model=DeliveryResponse,
    status_code=201,  # 배송 요청 생성 성공 시 HTTP 201 반환
)
def request_delivery(
    payload: DeliveryCreate,
    order_id: int = Path(..., ge=1, description="배송 요청을 생성할 주문 ID"),
    # Path: URL 경로 파라미터, ge=1: 1 이상 정수만 허용
) -> DeliveryResponse:
    """특정 주문에 대한 배송 요청을 생성합니다. 주문이 없거나 이미 배송 요청이 있으면 오류를 반환합니다."""
    with psycopg.connect(get_conninfo()) as conn:  # DB 연결
        with conn.cursor() as cur:                  # 커서 생성
            cur.execute(
                "SELECT id FROM orders WHERE id = %s",
                (order_id,),  # 주문 ID로 주문 존재 여부 확인
            )
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Order not found")
                # 주문이 존재하지 않으면 404 에러 반환

            cur.execute(
                "SELECT id FROM deliveries WHERE order_id = %s",
                (order_id,),  # 같은 주문에 대한 배송 요청이 이미 있는지 확인
            )
            if cur.fetchone() is not None:
                raise HTTPException(status_code=409, detail="Delivery already exists")
                # 배송 요청이 이미 존재하면 409 Conflict 에러 반환

            cur.execute(
                """
                INSERT INTO deliveries (order_id, address)
                VALUES (%s, %s)
                RETURNING id, order_id, address, status, requested_at, delivered_at
                """,
                (order_id, payload.address),
                # 새 배송 레코드 삽입 후 삽입된 데이터 반환
            )
            row = cur.fetchone()  # 삽입된 배송 데이터 한 행을 가져옴
        conn.commit()             # 트랜잭션 커밋

    return to_delivery_response(row)  # DB 행을 응답 모델로 변환 후 반환


@app.patch(
    "/deliveries/{delivery_id}/complete",
    tags=["deliveries"],
    summary="배송 완료 처리",
    response_model=DeliveryResponse,
)
def complete_delivery(
    delivery_id: int = Path(..., ge=1, description="완료 처리할 배송 ID"),
    # ge=1: 1 이상 정수 ID만 허용
) -> DeliveryResponse:
    """배송을 완료 상태로 업데이트하고, 연관 주문도 완료 상태로 변경합니다."""
    with psycopg.connect(get_conninfo()) as conn:  # DB 연결
        with conn.cursor() as cur:                  # 커서 생성
            cur.execute(
                """
                UPDATE deliveries
                SET status = 'DELIVERED', delivered_at = NOW()
                WHERE id = %s
                RETURNING id, order_id, address, status, requested_at, delivered_at
                """,
                (delivery_id,),
                # 배송 상태를 DELIVERED로 변경하고 완료 시각을 현재 시각으로 설정
                # RETURNING으로 업데이트된 데이터를 즉시 반환
            )
            row = cur.fetchone()  # 업데이트된 배송 데이터를 가져옴
            if row is None:
                raise HTTPException(status_code=404, detail="Delivery not found")
                # 해당 배송이 존재하지 않으면 404 에러 반환

            cur.execute(
                """
                UPDATE orders
                SET status = 'COMPLETED'
                WHERE id = %s
                """,
                (row[1],),  # row[1]은 order_id (배송과 연관된 주문 ID)
                # 배송 완료 시 주문 상태도 COMPLETED로 업데이트
            )
        conn.commit()  # 배송 및 주문 상태 업데이트 트랜잭션 커밋

    return to_delivery_response(row)  # 업데이트된 배송 데이터를 응답 모델로 변환 후 반환


@app.get(
    "/orders/{order_id}",
    tags=["orders"],
    summary="주문 상세 조회",
    response_model=OrderResponse,
)
def get_order(order_id: int = Path(..., ge=1, description="조회할 주문 ID")) -> OrderResponse:
    """특정 주문 ID로 주문 상세 정보를 조회합니다. 없으면 404를 반환합니다."""
    with psycopg.connect(get_conninfo()) as conn:  # DB 연결
        with conn.cursor() as cur:                  # 커서 생성
            cur.execute(
                """
                SELECT id, customer_name, product_name, quantity, status, created_at
                FROM orders
                WHERE id = %s
                """,
                (order_id,),  # URL 경로의 order_id로 특정 주문 조회
            )
            row = cur.fetchone()  # 조회 결과 한 행을 가져옴
            if row is None:
                raise HTTPException(status_code=404, detail="Order not found")
                # 주문이 존재하지 않으면 404 에러 반환

    return to_order_response(row)  # DB 행을 응답 모델로 변환 후 반환
