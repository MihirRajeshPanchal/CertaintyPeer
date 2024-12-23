from certaintypeer.endpoints import hybrid_search
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(hybrid_search.router)


@app.get("/")
def root():
    return {"message": "Welcome to CertaintyPeer!"}