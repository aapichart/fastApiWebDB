from fastapi import APIRouter


router5=APIRouter(
    tags=["purchasingModule"]
)

@router5.get("/purchasingModule/test")
async def test5():
    return {"username5":"test5"}
