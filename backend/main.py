from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .agent import get_agent_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the query model
class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Titanic Dataset Chat API is running"}

@app.post("/query")
async def process_query(query: Query):
    try:
        response = get_agent_response(query.question)
        # If response is a dict with image, return it directly
        if isinstance(response, dict) and "image" in response:
            return {"response": response}
        # Otherwise wrap the text response
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 