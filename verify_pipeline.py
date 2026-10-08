import json
import os
from pipeline.analyzer import analyze_document
from pipeline.report_generator import generate_pdf_report, generate_markdown_report

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    files = [
        "Certificate_Genuine.pdf",
        "Invoice_4582.pdf",
        "Certificate_2026.pdf"
    ]

    for fname in files:
        fpath = os.path.join(base, fname)
        print(f"\n==========================================")
        print(f"ANALYZING: {fname}")
        print(f"==========================================")
        res = analyze_document(fpath, fname)
        print(f"Severity: {res['summary']['severity']}")
        print(f"Total Findings: {res['summary']['total_findings']}")
        print(f"Breakdown: {res['summary']['high']} High, {res['summary']['medium']} Med, {res['summary']['low']} Low")
        print(f"Coverage: {res['summary']['checks_completed']} / {res['summary']['checks_total']}")
        print(f"Categories: {res['categories']}")
        print(f"Evidence count: {len(res['evidence'])}")
        for e in res['evidence']:
            print(f"  [{e['id']}] {e['severity']} - {e['title']} ({e['region']})")
        print(f"Regions detected: {len(res['regions'])}")
        for r in res['regions']:
            print(f"  {r['id']}: [{r['x']},{r['y']},{r['width']},{r['height']}] - {r['severity']}")
        print(f"Hypotheses: {[h['title'] for h in res['hypotheses']]}")
        print(f"Origin Indicators: {res['origin_indicators']}")
        print(f"AI Assessment: {res['ai_assessment']}")

        # Test generating PDF report
        report_pdf = os.path.join(base, f"Report_{fname}.pdf")
        generate_pdf_report(res, report_pdf)
        print(f"Generated PDF Report at: {report_pdf}")

if __name__ == "__main__":
    main()
