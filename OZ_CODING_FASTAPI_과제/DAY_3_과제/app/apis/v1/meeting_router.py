from fastapi import APIRouter

from app.dtos.create_meeting_response import CreateMeetingResponse

edgedb_router = APIRouter(prefix="/v1/edgedb/meetings", tags=["Meeting"])
mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["Meeting"])
# 원래는 어떤 DB를 쓰는지 URL에 적을 필요 없다.
# 강의에서만 이렇게 진행, 실전에서는 DB이름을 URL에 넣지 않는다.

@edgedb_router.post(
    "",
    description="meeting 을 생성합니다.",
)
async def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abc")


@mysql_router.post(
    "",
    description="meeting 을 생성합니다.",
)
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abc")