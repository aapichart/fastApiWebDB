from fastapi import APIRouter


router2=APIRouter()

@router2.get("/invenModule/test", tags=["invenModule"])
async def test2():
    return {"username2":"test2"}
