from fastapi import APIRouter


router6=APIRouter(
    tags=["systemModule"]
) 

@router6.get("/systemModule/test")
async def test6():
    return {"username6":"test6"}
