from fastapi import FastAPI, UploadFile, File
from src.adc_orchestrator import ADCPipeline

app = FastAPI(title="Data Compressor API")

@app.post("/upload")
async def upload_stream(file: UploadFile = File(...)):
    content = await file.read()
    # Initialize pipeline with environment credentials
    pipeline = ADCPipeline(...) 
    pipeline.process_file(file.filename, content)
    return {"status": "success", "bytes": len(content)}
