from fastapi import APIRouter


routerHr=APIRouter(
    tags=["hrMgtModule"]
)

@routerHr.get("/hrMgtModule/test")
async def test4():
    return {"username4":"test4"}
