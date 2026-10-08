"""
VERIDOC — Forensic Dashboard Styling and Theme
High-contrast, professional digital investigation interface.
"""

FORENSIC_CSS = """
<style>
/* Import Inter / JetBrains Mono font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Global Container & Typography */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, .stCode, [data-testid="stMarkdownContainer"] code {
    font-family: 'JetBrains Mono', monospace !important;
}

/* App Header Styling */
.veridoc-header {
    background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e1b4b 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(99, 102, 241, 0.15);
}

.veridoc-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0;
}

.veridoc-title span.badge {
    background: #4f46e5;
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 9999px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.veridoc-subtitle {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 6px;
    margin-bottom: 0;
    max-width: 800px;
    line-height: 1.5;
}

/* Severity Pill Badges */
.badge-high {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid #ef4444;
    color: #f87171;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-elevated {
    background: rgba(249, 115, 22, 0.15);
    border: 1px solid #f97316;
    color: #fb923c;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-low {
    background: rgba(234, 179, 8, 0.15);
    border: 1px solid #eab308;
    color: #facc15;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-clean {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid #22c55e;
    color: #4ade80;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Hero Concern Banner */
.concern-banner-high {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(185, 28, 28, 0.05) 100%);
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-left: 6px solid #ef4444;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.concern-banner-elevated {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.12) 0%, rgba(194, 65, 12, 0.05) 100%);
    border: 1px solid rgba(249, 115, 22, 0.4);
    border-left: 6px solid #f97316;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.concern-banner-low {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(21, 128, 61, 0.05) 100%);
    border: 1px solid rgba(34, 197, 94, 0.4);
    border-left: 6px solid #22c55e;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

/* Category Card */
.category-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 18px;
    text-align: center;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.category-card:hover {
    border-color: #374151;
    transform: translateY(-2px);
}

.category-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 8px;
}

.category-count {
    font-size: 26px;
    font-weight: 800;
    margin: 4px 0;
}

.category-status {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
}

/* Evidence Card */
.evidence-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border-left-width: 4px;
    transition: border-color 0.2s ease;
}

.evidence-card-high {
    border-left-color: #ef4444;
}

.evidence-card-med {
    border-left-color: #f97316;
}

.evidence-card-low {
    border-left-color: #eab308;
}

.evidence-title {
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
}

.evidence-location {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 8px;
}

.evidence-desc {
    font-size: 13.5px;
    color: #cbd5e1;
    line-height: 1.5;
}

/* Disclaimer Box */
.disclaimer-box {
    background: rgba(30, 41, 59, 0.7);
    border: 1px dashed #475569;
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.5;
    margin-top: 14px;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0f172a;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #475569;
}
</style>
"""
