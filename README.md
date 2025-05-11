#  Automate Accounts – Developer Hiring Assessment

This project automates the processing of scanned PDF receipts using OCR (Tesseract) and stores the extracted data in an SQLite database. It provides a FastAPI-based backend to upload, validate, process, and retrieve receipt information.

## Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **OCR:** Tesseract (via pytesseract)
- **Database:** SQLite
- **ORM:** SQLAlchemy

## Database Schema

### `receipt_file`
Stores uploaded file metadata:
- `id`, `file_name`, `file_path`
- `is_valid`, `invalid_reason`
- `is_processed`, `created_at`, `updated_at`

### `receipt`
Stores extracted receipt info:
- `id`, `purchased_at`, `merchant_name`, `total_amount`
- `file_path`, `created_at`, `updated_at`

## API Endpoints

| Endpoint           | Method | Description                              |
|--------------------|--------|------------------------------------------|
| `/upload`          | POST   | Upload a PDF receipt                     |
| `/validate`        | POST   | Validate uploaded file as a PDF          |
| `/process`         | POST   | Run OCR and extract receipt info         |
| `/receipts`        | GET    | List all processed receipts              |
| `/receipts/{id}`   | GET    | Get receipt details by ID                |

##  Setup Instructions

```bash
git clone https://github.com/your-username/automate-accounts-developer-hiring-assessment.git
cd automate-accounts-developer-hiring-assessment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
