from fastapi import FastAPI, UploadFile, Depends
import pandas as pd
from models import TerroristValid
from db import get_db

app = FastAPI()

@app.get('/')
def root():
    return {'mess': 'ok'}

@app.post('/top-threats/')
def upload_csv(file: UploadFile, collection=Depends(get_db)):
    df = pd.read_csv(file.file)
    df.sort_values(by=['danger_rate'], ascending=False, inplace=True)
    terrs = df.to_dict('index')
    
    top_models = []
    top_docs = []
    
    for terr in terrs.values():
        terr_valid_model = TerroristValid(**terr)
        top_models.append(terr_valid_model)
        top_docs.append(terr_valid_model.model_dump())
        if len(top_models) == 5:
            break
    
    collection.insert_many(top_docs)
    
    return {'count': len(top_models),
            'top': top_models}
    
@app.get('/get_all')
def get_threats(collection=Depends(get_db)):
    threads = collection.find({}, {"_id": 0})
    return list(threads)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)