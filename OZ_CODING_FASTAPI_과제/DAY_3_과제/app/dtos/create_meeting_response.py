from typing import Annotated

from pydantic import BaseModel, Field

from app.dtos.frozen_config import FROZEN_CONFIG


class CreateMeetingResponse(BaseModel):
    model_config = FROZEN_CONFIG

    url_code: Annotated[str, Field(description="회의 URL 코드. unqiue 합니다.")]
    # str = Field()를 썻을 경우 기존 파이썬에서는 타입힌트가 일치하지 않기 때문에 Annotated를 사용하여 description같은 옵션들을 추가할 수 있게 된다.

# 파이썬에서는 타입정의를 여러개 하는것 안돼기에 Annotated를 사용해서 str이라는 타입을 정의하고 Field에서 여러가지 옵션들을 사용한다고하는데
# 어차피 우리는 BaseModel과 Field를 사용하기 위해 pydantic라이브러리를 사용해야하는데 그럼 굳이 Annotated를 사용해야하나
# 그냥 pydantic스럽게 '***: str = Field(description="이런 식으로 사용")' 사용하면 되는것 아닌가 의구심이 든다.