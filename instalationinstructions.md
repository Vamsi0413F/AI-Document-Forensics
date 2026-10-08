# VERIDOC — Installation & Setup

Follow the steps below to install the required dependencies and run VERIDOC locally.

## Prerequisites

Make sure you have the following installed:

- Python 3.9 or later
- pip
- Tesseract OCR

## 1. Navigate to the Project Directory

Open a terminal and navigate to the project folder:

```bash
cd AI-Document-Forensics
2. Create a Virtual Environment
Create a Python virtual environment:
python -m venv .venv

3. Activate the Virtual Environment
Windows
.venv\Scripts\activate

macOS / Linux
source .venv/bin/activate

4. Install Required Dependencies
Install all required Python packages using requirements.txt:
pip install -r requirements.txt

5. Install Tesseract OCR
VERIDOC uses Tesseract OCR for extracting text from scanned documents and images.
Windows
Install Tesseract OCR and add the Tesseract installation directory to your system PATH.
macOS
If Homebrew is installed:
brew install tesseract
6. Run the Application
Start the VERIDOC Streamlit application:
streamlit run app.py

7. Open the Application
After Streamlit starts, open the following URL in your browser:
http://localhost:8501
