# DAY 2 과제 정리 

## 1. Shell Script

Shell Script란 리눅스/유닉스 환경에서 명령어들을 순서대로 실행할 수 있도록 작성한 스크립트 파일이다.
`.sh` 확장자를 사용하며, 반복적인 작업을 자동화할 때 주로 활용된다.

### 기본 작성법

```bash
#!/bin/bash
set -eo pipefail

COLOR_GREEN=$(tput setaf 2)
COLOR_NC=$(tput sgr0)

echo "Starting black"
poetry run black .
echo "OK"

echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"
```

- `#!/bin/bash` : 해당 스크립트를 bash로 실행하도록 지정
- `set -eo pipefail` : 오류 발생 시 즉시 종료
- `$(명령어)` : 명령어 치환 (실행 결과를 변수에 저장)

---

## 2. Github Actions

Github Actions란 Github에서 제공하는 CI/CD 자동화 도구이다.
코드를 push하거나 PR을 생성할 때 자동으로 테스트, 빌드, 배포 등의 작업을 실행할 수 있다.

### 주요 활용 사례

- 코드 push 시 자동으로 테스트 실행
- 코드 스타일 검사 자동화 (black, ruff, mypy 등)
- 배포 자동화

---

## 3. Github Actions 스크립트 작성법

Github Actions는 `.github/workflows/` 폴더 안에 YAML 파일로 작성한다.

```yaml
name: CI

on:
  push:

jobs:
  static-analysis:
    runs-on: ubuntu-24.04
    steps:
      - name: Check out the codes
        uses: actions/checkout@v2

      - name: Setup python environment
        uses: actions/setup-python@v2
        with:
          python-version: "3.13"

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 - --version 1.8.5

      - name: Install dependencies
        run: poetry install --no-root

      - name: Run Black
        run: poetry run black . --check

      - name: Run Mypy
        run: poetry run mypy .
```

- `on` : 워크플로우 실행 조건 (push, pull_request 등)
- `jobs` : 실행할 작업 목록
- `steps` : 각 작업의 세부 단계
- `uses` : 미리 만들어진 액션 사용
- `run` : 직접 명령어 실행

---

## 4. Github Actions Cache

Cache를 사용하면 의존성 패키지를 매번 새로 설치하지 않고 저장해두었다가 재사용할 수 있다.
이를 통해 워크플로우 실행 시간을 크게 단축할 수 있다.

```yaml
- name: Cache Poetry dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pypoetry
    key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
    restore-keys: |
      ${{ runner.os }}-poetry-
```

### Cache 이점

- 의존성 설치 시간 단축
- 네트워크 비용 절감
- 동일한 `poetry.lock` 파일이면 캐시를 재사용

---

## 5. Spec API (Swagger UI)

Spec API란 FastAPI에서 자동으로 생성해주는 API 문서화 도구이다.
별도 설정 없이 `/docs` 경로에서 확인할 수 있으며, API를 직접 테스트해볼 수 있다.

```
http://127.0.0.1:8000/docs
```

### Pydantic Field를 활용한 스키마 설정

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "apple",
                "price": 1000,
                "description": "맛있는 사과"
            }
        }
    }
    name: str = Field(description="상품의 이름을 입력하세요")
    price: float | int = Field(gt=0, description="0보다 큰 가격을 입력하세요")
    description: str = Field(default="No description")
```

- `example` : Swagger UI의 Example Value 탭에 예시값 표시
- `default` : Edit Value 탭에 기본값 표시
- `description` : 필드 설명 표시
- `gt`, `ge`, `lt`, `le` : 숫자 범위 제한

---

## 6. FastAPI 라우터 구성

FastAPI에서는 `APIRouter`를 사용하여 라우터를 모듈별로 분리할 수 있다.

### 폴더 구조

```
project/
├── models.py
├── routers/
│   └── products.py
└── main.py
```

### models.py

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float | int = Field(gt=0)
    description: str = "No description"
```

### routers/products.py

```python
from fastapi import APIRouter
from models import Product

router = APIRouter()

@router.post("/products/")
async def post_product(product: Product):
    return {"product": product}
```

### main.py

```python
from fastapi import FastAPI
from routers import products

app = FastAPI()
app.include_router(products.router)
```

- `APIRouter` : 라우터를 모듈별로 분리
- `include_router` : 분리된 라우터를 메인 앱에 등록
- 경로 매개변수와 쿼리 매개변수를 조합하여 다양한 API 구성 가능
