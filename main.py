from fastapi import FastAPI, UploadFile
import pandas as pd
from models import TerroristValid

app = FastAPI()

@app.get('/')
def root():
    return {'mess': 'ok'}

@app.post('/top-threats/')
def upload_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    df.sort_values(by=['danger_rate'], ascending=False, inplace=True)
    terrs = df.to_dict('index')
    
    top = []
    for terr in terrs.values():
        terr_valid = TerroristValid(**terr)
        top.append(terr_valid)
        if len(top) == 5:
            break
        
    return {'count': len(top),
            'top': top}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)