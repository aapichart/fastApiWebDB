from fastapi import APIRouter


routerInven=APIRouter(
    tags=["invenModule"]
)

@routerInven.get("/invenModule/test")
async def test2():
    return {"username2":"test2"}
