# DAY 3 과제 정리

## 1. SPEC API

SPEC API란 API의 구조와 동작 방식을 명세(Specification)한 문서 기반의 API 설계 방식이다.
API가 어떤 엔드포인트를 가지고, 어떤 요청/응답 형식을 따르는지를 표준화된 형식으로 기술한다.

### 주요 개념

- **OpenAPI Specification (OAS)** : REST API를 JSON 또는 YAML 형식으로 기술하는 표준 스펙
- **기계가 읽을 수 있는 문서** : 사람뿐 아니라 도구(Swagger UI, Postman 등)가 자동으로 해석 가능
- **FastAPI와의 관계** : FastAPI는 코드를 작성하는 것만으로 OpenAPI 스펙을 자동 생성해준다

### SPEC API가 필요한 이유

```
클라이언트(프론트엔드)  ←→  API 명세서  ←→  서버(백엔드)

- 명세서가 없으면 : 어떤 URL로 요청해야 하는지, 어떤 데이터를 보내야 하는지 구두로 전달
- 명세서가 있으면 : 문서를 보고 바로 개발 가능, 오해 없이 협업 가능
```

---

## 2. Open API와 Swagger API Docs

Open API는 REST API를 기술하기 위한 표준 규격이다.
Swagger UI는 이 Open API 명세를 사람이 보기 좋게 시각화하고 직접 테스트까지 할 수 있는 도구이다.

### FastAPI에서 자동 제공하는 문서 경로

| 경로 | 도구 | 설명 |
|------|------|------|
| `/docs` | Swagger UI | 시각적인 API 문서 + 직접 테스트 가능 |
| `/redoc` | ReDoc | 읽기 전용 API 문서 (더 깔끔한 UI) |
| `/openapi.json` | JSON 원본 | OpenAPI 스펙 원본 데이터 |

### Swagger UI 활용법

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Meeting API",          # 문서 제목
    description="회의 생성 API",  # 문서 설명
    version="1.0.0",              # API 버전
)

class CreateMeetingResponse(BaseModel):
    url_code: str = Field(description="회의 URL 코드. unique 합니다.")
```

- `title`, `description`, `version` : Swagger UI 상단에 표시되는 앱 정보
- `Field(description=...)` : 각 필드에 설명을 추가하여 문서에 표시
- `tags` : 라우터에 태그를 달아 Swagger에서 그룹으로 묶어 표시

### Swagger UI에서 할 수 있는 것

```
1. API 목록 확인     → 어떤 엔드포인트가 있는지 한눈에 파악
2. 요청/응답 스키마  → 어떤 데이터를 보내고 받는지 확인
3. 직접 테스트       → "Try it out" 버튼으로 실제 요청 전송
4. 응답 확인         → 서버에서 돌아온 응답 코드와 데이터 확인
```

---

## 3. 써드 파티 라이브러리

써드 파티 라이브러리란 Python 기본 표준 라이브러리도 아니고, 내가 직접 만든 코드도 아닌,
외부 개발자나 팀이 만들어 배포한 라이브러리를 말한다.

### 구분 정리

| 종류 | 예시 | 설명 |
|------|------|------|
| 표준 라이브러리 | `os`, `json`, `datetime` | Python 설치 시 기본 포함 |
| 써드 파티 라이브러리 | `fastapi`, `pydantic`, `sqids` | pip/poetry로 별도 설치 필요 |
| 직접 만든 모듈 | `app/dtos/`, `app/apis/` | 프로젝트 내부 코드 |

### 이번 과제에서 사용한 써드 파티 라이브러리

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.13"
fastapi = "*"       # 웹 프레임워크
uvicorn = "*"       # ASGI 서버
orjson = "*"        # 빠른 JSON 직렬화
sqids = "*"         # ID 인코딩/디코딩 라이브러리
pydantic = "*"      # 데이터 유효성 검사
```

### 써드 파티 라이브러리 사용 시 주의점

- 라이브러리 버전 관리가 중요하다 → `poetry.lock` 파일로 버전을 고정
- 유지보수 중인 라이브러리인지 확인 (최근 업데이트, 이슈 대응 여부)
- 보안 취약점이 있을 수 있으니 신뢰할 수 있는 출처에서 설치

---

## 4. 암호화와 복호화

암호화(Encryption)란 원본 데이터를 특정 규칙에 따라 다른 형태로 변환하는 것이고,
복호화(Decryption)란 암호화된 데이터를 다시 원본으로 되돌리는 것이다.

### 단방향 vs 양방향

| 구분 | 설명 | 예시 |
|------|------|------|
| 단방향 (해싱) | 암호화만 가능, 복호화 불가 | 비밀번호 저장 (bcrypt, SHA-256) |
| 양방향 | 암호화, 복호화 모두 가능 | 데이터 전송 암호화 (AES, RSA) |
| 인코딩/디코딩 | 암호화 목적이 아닌 변환 | Base64, Sqids |

### 왜 ID를 인코딩하는가?

```
DB에서 사용하는 숫자 ID (예: 1, 2, 3)를 그대로 URL에 노출하면...

- 전체 데이터 수를 유추할 수 있다  →  /meetings/1, /meetings/2, /meetings/3
- 순차 탐색 공격에 취약하다         →  /meetings/999999 로 접근 시도

해결책: ID를 인코딩하여 외부에는 의미를 알 수 없는 문자열로 노출
예시: 1  →  "abc123xyz"
```

---

## 5. Sqids 라이브러리

Sqids는 숫자(정수)를 짧고 고유한 문자열 ID로 인코딩하고, 다시 숫자로 디코딩할 수 있는 라이브러리이다.
URL에 DB의 숫자 ID를 그대로 노출하지 않고 안전하게 변환할 때 사용한다.

### 설치

```bash
poetry add sqids
```

### 기본 사용법

```python
from sqids import Sqids

sqids = Sqids()

# 인코딩: 숫자 → 문자열
encoded = sqids.encode([1])       # "Uk"
encoded = sqids.encode([1, 2, 3]) # "86Rf07"

# 디코딩: 문자열 → 숫자
decoded = sqids.decode("Uk")      # [1]
decoded = sqids.decode("86Rf07")  # [1, 2, 3]
```

### 옵션 설정

```python
from sqids import Sqids

sqids = Sqids(
    alphabet="abcdefghijklmnopqrstuvwxyz",  # 사용할 문자 집합 커스텀
    min_length=8,                            # 최소 길이 지정
)

encoded = sqids.encode([1])  # 최소 8자 이상의 문자열로 인코딩
```

### Sqids의 특징

- **가역적(Reversible)** : 인코딩한 값을 다시 디코딩하면 원래 숫자로 복원된다
- **결정론적(Deterministic)** : 같은 숫자는 항상 같은 문자열로 인코딩된다
- **충돌 없음** : 서로 다른 숫자는 항상 서로 다른 문자열로 인코딩된다
- **암호화가 아님** : 보안 목적의 암호화가 아닌 ID 난독화(obfuscation) 용도

---

## 6. FastAPI 라우터 구성 (SPEC API 기반)

FastAPI의 `APIRouter`를 활용하면 엔드포인트를 기능별로 모듈화하고,
Swagger 문서에도 자동으로 반영되는 SPEC API 라우터를 구성할 수 있다.

### 이번 과제의 폴더 구조

```
DAY_3_과제/
├── asgi.py                          # 서버 실행 진입점
├── app/
│   ├── __init__.py                  # FastAPI 앱 생성 및 라우터 등록
│   ├── apis/
│   │   └── v1/
│   │       └── meeting_router.py   # 라우터 정의
│   └── dtos/
│       ├── create_meeting_response.py  # 응답 스키마
│       └── frozen_config.py            # Pydantic 설정
```

### 라우터 구성 방법

```python
# app/apis/v1/meeting_router.py
from fastapi import APIRouter
from app.dtos.create_meeting_response import CreateMeetingResponse

# prefix : URL 공통 경로, tags : Swagger 문서 그룹명
edgedb_router = APIRouter(prefix="/v1/edgedb/meetings", tags=["Meeting"])
mysql_router  = APIRouter(prefix="/v1/mysql/meetings",  tags=["Meeting"])

@edgedb_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abc")
```

```python
# app/__init__.py
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.apis.v1.meeting_router import edgedb_router, mysql_router

app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(edgedb_router)
app.include_router(mysql_router)
```

### 주요 옵션 정리

| 옵션 | 위치 | 설명 |
|------|------|------|
| `prefix` | `APIRouter` | 해당 라우터의 모든 경로에 붙는 공통 URL |
| `tags` | `APIRouter` | Swagger UI에서 라우터를 묶어 표시하는 그룹명 |
| `description` | 데코레이터 | 해당 엔드포인트의 설명 (Swagger에 표시) |
| `default_response_class` | `FastAPI` | 기본 응답 형식 지정 (ORJSONResponse = 빠른 JSON) |

### DTO와 frozen 설정

```python
# app/dtos/frozen_config.py
from pydantic import ConfigDict

FROZEN_CONFIG = ConfigDict(frozen=True)
# frozen=True : 모델 인스턴스 생성 후 값 변경 불가 (불변 객체)
# 응답 데이터가 실수로 수정되는 것을 방지

# app/dtos/create_meeting_response.py
from typing import Annotated
from pydantic import BaseModel, Field
from app.dtos.frozen_config import FROZEN_CONFIG

class CreateMeetingResponse(BaseModel):
    model_config = FROZEN_CONFIG

    url_code: Annotated[str, Field(description="회의 URL 코드. unique 합니다.")]
    # Annotated[타입, Field(...)] : 타입 힌트와 Field 옵션을 함께 표현하는 방법
```

### 결과 확인

서버 실행 후 `http://localhost:8000/docs` 접속 시 아래와 같이 확인 가능하다.

```
POST /v1/edgedb/meetings  →  meeting 을 생성합니다.
POST /v1/mysql/meetings   →  meeting 을 생성합니다.
```
