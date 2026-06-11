# Exam Catalyst

Exam Catalyst is a web application that analyzes previous year papers and syllabus documents to identify the most important topics for exam preparation.

The goal is to help students maximize marks when preparation time is limited by focusing on concepts that are most likely to appear in examinations.

---

## Problem

Students often rely on repeated keywords when analyzing previous year papers. However, the same concept can be tested through different wording and question styles.

Exam Catalyst focuses on identifying important **topics**, not repeated keywords.

---

## Features

* Upload multiple previous year papers and syllabus documents.
* Support for text PDFs, scanned PDFs, and images.
* Automatic text extraction and OCR.
* AI-powered question extraction.
* Topic mapping based on the syllabus.
* Topic ranking using multiple factors.
* Privacy-first processing with temporary file storage.
* Parallel file processing for improved performance.

---

## How It Works

### 1. Upload Files

Users upload:

* Previous year papers
* Syllabus documents

### 2. Text Extraction

The system automatically determines the file type and routes it to the appropriate processing pipeline.

Supported formats:

* Text PDFs
* Scanned PDFs
* Images

### 3. Question Extraction

AI extracts:

* Individual questions
* Associated marks

and returns structured data.

### 4. Topic Mapping

Each question is mapped to exactly one syllabus topic.

If a confident mapping cannot be determined, the system returns:

```text
unknown
```

instead of guessing.

### 5. Topic Ranking

Topics are ranked using:

* Frequency across papers
* Marks weightage
* Recency

The final output is a ranked list of topics without exposing internal scoring calculations.

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI

### Planned Components

* OCR Pipeline
* AI Processing Pipeline
* Topic Ranking Engine

---

## Privacy

Uploaded files are:

1. Stored temporarily
2. Processed
3. Deleted immediately after processing

No permanent file storage is required.

---

## Project Status

Currently under active development.

Completed:

* FastAPI backend setup
* GET and POST endpoints
* Frontend-backend communication
* Multi-file upload pipeline
* Temporary file management

In Progress:

* Text extraction pipeline
* OCR integration
* AI processing workflow
* Topic ranking engine

---

## Project Goal

Provide students with a simple answer to a difficult question:

> "If I don't have time to study everything, what should I study first?"
