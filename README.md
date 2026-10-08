# AI-Document-Forensics

# VERIDOC — AI-Powered Document Forensics

> An AI-assisted document forensic screening platform that analyzes PDFs and images for content inconsistencies, formatting anomalies, metadata irregularities, suspicious visual regions, and other forensic indicators.

## Team

**Team Name:** Inception

| Member | Contribution |
| ------ | ------------ |
| Harish | Document Intelligence — text extraction, OCR, content consistency and document-level anomaly detection |
| Abhijith | Forensic Analysis — formatting analysis, metadata extraction, visual analysis and SHA-256 fingerprinting |
| Rajaneesh | AI & Risk Engine — Gemma-based reasoning, evidence interpretation, tampering hypotheses and risk assessment |
| Vamsi krishna | Frontend & System Integration — dashboard, document workflow, module integration, evidence visualization, reports, testing and demo |

## Problem Statement

### The Problem

Digital documents such as certificates, invoices, identification documents, letters and official records can be modified using readily available editing tools.

Traditional verification often requires manual inspection of:

- Text consistency
- Dates and identification numbers
- Fonts and formatting
- Document metadata
- Images and visual regions
- Digital file properties

This process can be time-consuming and difficult to scale.

A small alteration may not be immediately visible to a human reviewer, especially when the document appears visually authentic.

VERIDOC addresses this problem by providing an automated first-level forensic screening system that identifies suspicious indicators and organizes them into an explainable evidence report.

### Why We Chose This Problem

Document manipulation is a practical, everyday problem affecting educational institutions, businesses, financial organizations and administrative systems.

We chose this problem because modern document editing tools make manipulation increasingly accessible, while verification is still heavily dependent on manual inspection.

Our goal is not to replace human verification, but to provide investigators and reviewers with a faster way to identify which parts of a document deserve closer examination.

## Solution

VERIDOC is an AI-assisted document forensic screening platform.

A user uploads a PDF or image, after which the system performs multiple independent forensic checks covering:

- Document content
- Formatting and structure
- Metadata
- Visual regions
- Digital fingerprinting

The collected evidence is then aggregated and passed to an AI reasoning layer to generate contextual forensic observations and possible tampering hypotheses.

The final result is presented through an interactive dashboard containing evidence, suspicious regions, risk assessment, origin indicators and recommended manual verification actions.

VERIDOC does not claim to definitively classify a document as genuine or forged. Instead, it identifies forensic indicators that may warrant further investigation.

### Key Features

- **🔍 Content Consistency Analysis** — Identifies inconsistencies in extracted document information such as dates, names, identifiers and other repeated values.
- **🧾 Formatting & Metadata Forensics** — Analyzes fonts, font sizes, layout characteristics, document metadata and digital file properties.
- **🖼️ Visual Evidence & Suspicious Regions** — Identifies document regions and visual elements that require further examination and displays them using page-level visual indicators.
- **🕵️ Evidence-Based Risk Analysis** — Aggregates forensic findings, uses AI-assisted reasoning to generate possible tampering hypotheses, and provides a structured manual verification workflow.

## Innovation and Differentiation

VERIDOC combines multiple forensic signals instead of relying on a single binary fake/real classifier.

The system separates:

**Evidence → Interpretation → Hypothesis → Human Verification**

For example, detecting an unusual font is treated as evidence rather than automatically declaring the document forged.

The platform combines:

- Content-level analysis
- Formatting analysis
- Metadata analysis
- Visual analysis
- Cryptographic fingerprinting
- AI-assisted reasoning
- Human-in-the-loop verification

This multi-signal approach makes the result more explainable than a simple black-box authenticity prediction.

## Technical Implementation

### Architecture

```mermaid
flowchart TD

    A[User Uploads PDF / Image] --> B[Document Processing]

    B --> C[Content Analysis]
    B --> D[Formatting Analysis]
    B --> E[Metadata Analysis]
    B --> F[Visual Analysis]
    B --> G[SHA-256 Fingerprinting]

    C --> H[Evidence Aggregation]
    D --> H
    E --> H
    F --> H
    G --> H

    H --> I[AI Reasoning / Gemma]

    I --> J[Tampering Hypotheses]
    H --> K[Forensic Risk Engine]

    J --> K

    K --> L[VERIDOC Case Object]

    L --> M[Forensic Dashboard]

    M --> N[Evidence]
    M --> O[Suspicious Regions]
    M --> P[Origin Indicators]
    M --> Q[Manual Verification]
    M --> R[Export Report]

    M --> S[(SQLite Case History)]
