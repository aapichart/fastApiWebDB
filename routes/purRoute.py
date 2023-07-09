from fastapi import APIRouter


routerPur=APIRouter(
    tags=["purchasingModule"]
)

@routerPur.get("/purchasingModule/test")
async def test5():
    return {"username5":"test5"}
