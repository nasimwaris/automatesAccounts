from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import shutil, os
from sqlalchemy.orm import Session
from . import database, models, schemas
from .utils import pdf_validator, ocr_processor

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload", response_model=schemas.UploadResponse)
def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.ReceiptFile(file_name=file.filename, file_path=path)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

@app.post("/validate")
def validate(db: Session = Depends(get_db)):
    files = db.query(models.ReceiptFile).filter(models.ReceiptFile.is_valid == False).all()
    for f in files:
        valid = pdf_validator.is_valid_pdf(f.file_path)
        f.is_valid = valid
        f.invalid_reason = None if valid else "Not a valid PDF"
        db.commit()
    return {"validated": len(files)}

@app.post("/process")
def process(db: Session = Depends(get_db)):
    files = db.query(models.ReceiptFile).filter(models.ReceiptFile.is_valid == True, models.ReceiptFile.is_processed == False).all()
    for f in files:
        text = ocr_processor.extract_text_from_pdf(f.file_path)
        fields = ocr_processor.extract_fields(text)
        new_receipt = models.Receipt(**fields, file_path=f.file_path)
        db.add(new_receipt)
        f.is_processed = True
        db.commit()
    return {"processed": len(files)}

@app.get("/receipts", response_model=list[schemas.ReceiptOut])
def list_receipts(db: Session = Depends(get_db)):
    return db.query(models.Receipt).all()

@app.get("/receipts/{id}", response_model=schemas.ReceiptOut)
def get_receipt(id: int, db: Session = Depends(get_db)):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt
