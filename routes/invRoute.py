from fastapi import APIRouter


router2=APIRouter(
    tags=["invenModule"]
)

@router2.get("/invenModule/test")
async def test2():
    return {"username2":"test2"}
