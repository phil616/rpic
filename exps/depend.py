from fastapi import FastAPI, APIRouter, Depends,Request

def injection(name):
    print("injection",name)
def reqhandle(req:Request):
    print("reqhandle",req.app.routes)
app = FastAPI()

router = APIRouter(dependencies=[Depends(injection),Depends(reqhandle)])

@router.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}
app.include_router(router)

# injection exp success