# AI-Powered 3-Way Matching Agent

## Overview

This project is an AI-powered Accounts Payable (AP) automation platform that performs **Three-Way Matching** between:

- Supplier Invoice
- Purchase Order (PO)
- Goods Receipt Note (GRN) / Receipt

The solution leverages:

- FastAPI
- LangChain
- OpenAI Compatible API (AI Credits)
- OCR/Text Extraction
- Pydantic Structured Outputs

to automatically:

1. Extract information from uploaded documents
2. Classify documents
3. Validate mandatory fields
4. Perform line-item based 3-way matching
5. Identify discrepancies
6. Return validation and matching results through Swagger UI

---

# Features

## Document Upload

Upload the following documents via Swagger:

- Invoice
- Purchase Order
- Receipt / Goods Receipt Note

---

## AI Document Classification

Automatically identifies uploaded document type.

Supported document categories:

| Document Type | Examples |
|-------------|------------|
| Invoice | Supplier Invoice |
| PurchaseOrder | Purchase Order |
| Receipt | Receipt |
| Receipt | Goods Receipt |
| Receipt | Goods Receipt Note |
| Receipt | GRN |

Document aliases are normalized internally.

Examples:

```text
GoodsReceipt
Goods Receipt
Goods Receipt Note
GRN
```

become:

```text
Receipt
```

---

## AI Extraction

Extracts structured fields using GPT-4o through AI Credits.

Invoice Extraction:

```json
{
  "invoice_number": "",
  "supplier_name": "",
  "po_number": "",
  "subtotal": 0,
  "tax_amount": 0,
  "total_amount": 0,
  "items": []
}
```

Purchase Order Extraction:

```json
{
  "po_number": "",
  "supplier_name": "",
  "subtotal": 0,
  "tax_amount": 0,
  "total_amount": 0,
  "items": []
}
```

Receipt Extraction:

```json
{
  "receipt_number": "",
  "po_number": "",
  "items": []
}
```

---

## Line Item Matching

Matching is performed at SKU level.

Example:

```text
SKU-101
SKU-204
SKU-345
```

Validation checks:

### PO Number Matching

```text
Invoice PO = PO PO = Receipt PO
```

### Amount Matching

```text
Invoice Total = PO Total
```

Tolerance can be configured.

Current:

```text
1%
```

---

### Quantity Matching

Checks:

```text
Ordered Quantity
>=

Invoiced Quantity

Received Quantity
>=

Invoiced Quantity
```

---

## Exception Handling

Documents are routed to review when:

- Incorrect document type
- Missing mandatory fields
- Invalid totals
- Missing SKUs
- Quantity mismatch
- PO mismatch

Example:

```json
{
  "status": "REVIEW_REQUIRED",
  "stage": "VALIDATION"
}
```

---

# Project Structure

```text
app/
│
├── api/
│   └── matching_router.py
│
├── agents/
│   └── document_classifier.py
│
├── ocr/
│   └── ocr_di.py
│
├── services/
│   ├── file_service.py
│   ├── document_service.py
│   ├── classification_service.py
│   ├── extraction_service.py
│   ├── validation_service.py
│   └── matching_service.py
│
├── models/
│   ├── response_models.py
│   └── error_models.py
│
├── utils/
│   ├── prompts.py
│   └── validators.py
│
├── llm.py
├── matching.py
├── schemas.py
└── main.py
```

---

# Architecture

```text
                    ┌──────────────┐
                    │ Swagger UI   │
                    └──────┬───────┘
                           │
                           ▼

              Upload Invoice / PO / Receipt

                           │
                           ▼

                  OCR / Text Extraction

                           │
                           ▼

                   Document Classification

                           │
                           ▼

                  Structured Data Extraction

                           │
                           ▼

                     Validation Layer

                           │
                           ▼

                     3-Way Matching

                           │
                           ▼

                 Success / Review Response
```

---

# Technology Stack

| Layer | Technology |
|---------|-------------|
| API | FastAPI |
| LLM | GPT-4o |
| Endpoint | AI Credits |
| Validation | Pydantic |
| OCR/PDF Parsing | pdfplumber / pypdf |
| Matching Logic | Python |
| Documentation | Swagger UI |

---

# Environment Variables

Create `.env`

```env
OPENAI_API_KEY=your_api_key

OPENAI_ENDPOINT=https://api.aicredits.in/v1

OPENAI_MODEL=gpt-4o
```

---

# Installation

Create virtual environment:

```bash
uv venv --python 3.11
```

Activate:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
uv sync
```

---

# Running the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/api/v1/swagger
```

OpenAPI:

```text
http://localhost:8000/api/v1/openapi.json
```

---

# API Endpoint

## POST

```http
/api/v1/three-way-match
```

### Input

Form Data:

```text
invoice_file
po_file
receipt_file
```

All files are mandatory.

---

# Success Response

```json
{
  "status": "SUCCESS",
  "invoice": {},
  "purchase_order": {},
  "receipt": {},
  "match_result": {
    "status": "MATCHED",
    "score": 100,
    "checks": {
      "po_match": true,
      "amount_match": true,
      "quantity_match": true
    },
    "comments": []
  }
}
```

---

# Classification Review Response

```json
{
  "status": "REVIEW",
  "stage": "CLASSIFICATION",
  "errors": [
    {
      "document": "receipt.pdf",
      "expected": "Receipt",
      "detected": "Unknown"
    }
  ]
}
```

---

# Validation Review Response

```json
{
  "status": "REVIEW_REQUIRED",
  "stage": "VALIDATION",
  "errors": [
    "Missing PO Number",
    "Missing Line Items"
  ]
}
```

---

# Line Item Schema

```json
{
  "sku": "SKU-101",
  "description": "Widget A",
  "quantity": 20,
  "unit_price": 100,
  "amount": 2000
}
```

---

# Matching Rules

## Rule 1

PO Number must match.

```text
Invoice PO
==
Purchase Order PO
==
Receipt PO
```

---

## Rule 2

Invoice Amount must equal PO Amount.

Variance:

```text
1%
```

---

## Rule 3

Received Quantity must be greater than or equal to Invoiced Quantity.

Example:

```text
Received = 20

Invoice = 15

PASS
```

---

# Security

Uploaded files are temporary.

Recommended approach:

```text
Upload File
      ↓
Extract Text
      ↓
Delete File
      ↓
Continue Processing
```

Files should not be retained unless audit requirements demand otherwise.

---

# Current Limitations

This is a POC.

Not yet included:

- PostgreSQL
- LangGraph
- LangSmith
- Human Review UI
- Zoho Integration
- Tally Integration
- Duplicate Invoice Detection
- Vendor Validation
- Fraud Detection
- Workflow Engine

---

# Future Enhancements

## Database

Persist:

```text
Documents
Extraction Results
Matching Results
Review Queue
```

---

## LangGraph Workflow

```text
OCR
↓
Classification
↓
Extraction
↓
Validation
↓
Matching
↓
ERP Posting
```

---

## ERP Integration

Supported targets:

- Zoho Books
- Tally Prime
- SAP S/4HANA
- Oracle Fusion

---

## Human Review Queue

Low-confidence documents can be routed to:

```text
React UI
Power Apps
Copilot Studio
```

for manual correction and approval.

---

# Author

AI-Powered 3-Way Matching Agent

Version:

```text
1.0.0
```

Status:

```text
POC
```