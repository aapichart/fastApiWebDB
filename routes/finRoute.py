from fastapi import APIRouter


routerFin=APIRouter(
    tags=["financeModule"]
)

@routerFin.get("/financeModule/test")
async def test3():
    return {"username3":"test3"}
