from fastapi import FastAPI, HTTPException
from squirro.db import ESDatabase
from pydantic import BaseModel
from squirro.summarize import summary

app = FastAPI()
db = ESDatabase()

mappings = {'properties': {'text': {'type':'text'}} }
settings={'number_of_shards': 1, 'number_of_replicas': 1}

class File(BaseModel):
    text: str

class Id(BaseModel):
    document_id: str

class Summary(BaseModel):
    document_id: str
    summary: str
    
@app.get("/")
def root_page():
    return "Hello everyone! Look for the APIs specs you sent :)"

@app.post("/files/", response_model=Id)
async def insert_item(item: File):
    db.create_index(index="files", mappings=mappings, settings=settings)
    id = db.insert_file("files", item.dict())
    retVal = Id(document_id=id if id is not None else "")
    return retVal

@app.get("/files/", response_model=File)
async def get_file(id: str):
    text = db.get_file(index="files", id=id)
    retVal = File(text=text if text is not None else "Document ID not found!")
    return retVal

@app.get("/summaries/", response_model=Summary)
async def get_summary(id: str):
    summary_text = db.get_file(index="summaries", id=id)
    if summary_text is None:
        db.create_index(index="summaries", mappings=mappings, settings=settings)
        text = db.get_file("files", id)
        if text is not None:
            # Do summary task here
            file = File(text=summary(text))
            db.insert_file("summaries", file.dict(), id=id)
            summary_text = Summary(document_id=id, summary=file.text)
            return summary_text
        else:
            raise HTTPException(status_code=404, detail="Document id not found")
    retVal = Summary(document_id=id, summary=summary_text)
    return retVal
