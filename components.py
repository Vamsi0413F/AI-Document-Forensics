import os
import streamlit as st
from PIL import Image, ImageDraw
from typing import Dict, Any, List, Optional
from utils.file_handler import extract_document_pages_as_images
from pipeline.report_generator import generate_pdf_report, generate_markdown_report, generate_json_report
from storage.database import get_recent_cases, delete_case, rename_case


def render_header():
    """Renders the top application branding banner."""
    st.markdown(
        """
        <div class="veridoc-header">
            <h1 class="veridoc-title">
                🔎 VERIDOC <span class="badge">AI DOCUMENT FORENSICS</span>
            </h1>
            <p class="veridoc-subtitle">
                AI-assisted forensic screening and multi-modal integrity triage platform.
                Identifies anomalies, typographic variances, metadata discrepancies, and suspicious visual regions to assist human forensic examiners.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_severity_badge_html(severity: str) -> str:
    s = severity.upper()
    if s == "HIGH":
        return '<span class="badge-high">🔴 HIGH</span>'
    elif s in ["ELEVATED", "MEDIUM"]:
        return '<span class="badge-elevated">🟠 ELEVATED</span>'
    elif s == "LOW":
        return '<span class="badge-low">🟡 LOW</span>'
    else:
        return '<span class="badge-clean">🟢 CLEAN</span>'


def render_current_analysis_header(case: Dict[str, Any]):
    """Renders the Current Analysis overview, SHA-256, overall concern, and coverage."""
    doc = case.get("document", {})
    summary = case.get("summary", {})
    sev = summary.get("severity", "LOW")

    filename = doc.get("filename", "document.pdf")
    file_type = doc.get("file_type", "PDF")
    pages = doc.get("pages", 1)
    sha256 = doc.get("sha256", "N/A")
    short_sha = doc.get("short_sha256", sha256[:8] + "...")

    high_c = summary.get("high", 0)
    med_c = summary.get("medium", 0)
    low_c = summary.get("low", 0)
    total_f = summary.get("total_findings", 0)
    completed_checks = summary.get("checks_completed", 8)
    total_checks = summary.get("checks_total", 10)

    banner_class = "concern-banner-high" if sev == "HIGH" else (
        "concern-banner-elevated" if sev in ["ELEVATED", "MEDIUM"] else "concern-banner-low"
    )
    banner_icon = "🔴" if sev == "HIGH" else ("🟠" if sev in ["ELEVATED", "MEDIUM"] else "🟢")

    st.markdown(
        f"""
        <div style="margin-top: 10px; margin-bottom: 8px;">
            <span style="font-size: 13px; font-weight: 700; color: #64748b; letter-spacing: 1px; text-transform: uppercase;">
                CURRENT ANALYSIS
            </span>
            <div style="font-size: 22px; font-weight: 800; color: #f8fafc; margin-top: 4px;">
                📄 {filename}
            </div>
            <div style="font-size: 13px; color: #94a3b8; font-family: monospace; margin-top: 2px;">
                {file_type} • {pages} Page(s) • SHA-256: <b>{short_sha}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Concern Banner
    st.markdown(
        f"""
        <div class="{banner_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="font-size: 24px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;">
                        {banner_icon} {sev} CONCERN
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #e2e8f0; margin-top: 4px;">
                        {total_f} Significant Findings &nbsp;•&nbsp;
                        <span style="color: #f87171;">{high_c} High</span> &nbsp;•&nbsp;
                        <span style="color: #fb923c;">{med_c} Medium</span> &nbsp;•&nbsp;
                        <span style="color: #facc15;">{low_c} Low</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0.5px; text-transform: uppercase;">
                        Analysis Coverage
                    </div>
                    <div style="font-size: 18px; font-weight: 800; color: #38bdf8;">
                        {completed_checks} / {total_checks} Checks Completed
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_forensic_categories(case: Dict[str, Any]):
    """Renders the 4 core forensic categories: CONTENT, FORMAT, METADATA, VISUAL."""
    cats = case.get("categories", {})
    c_col1, c_col2, c_col3, c_col4 = st.columns(4)

    categories_spec = [
        ("CONTENT", cats.get("content", {}), "📝 Text & OCR Integrity", c_col1),
        ("FORMAT", cats.get("format", {}), "📐 Typographic & Layout", c_col2),
        ("METADATA", cats.get("metadata", {}), "🗂️ Timestamps & Creator", c_col3),
        ("VISUAL", cats.get("visual", {}), "🔍 ELA & Splice Scan", c_col4),
    ]

    for title, cat_data, subtitle, col in categories_spec:
        sev = cat_data.get("severity", "CLEAN")
        count = cat_data.get("findings", 0)

        color = "#ef4444" if sev == "HIGH" else (
            "#f97316" if sev in ["ELEVATED", "MEDIUM"] else (
                "#eab308" if sev == "LOW" else "#22c55e"
            )
        )
        icon = "🔴" if sev == "HIGH" else ("🟠" if sev in ["ELEVATED", "MEDIUM"] else ("🟡" if sev == "LOW" else "🟢"))

        with col:
            st.markdown(
                f"""
                <div class="category-card">
                    <div class="category-title">{title}</div>
                    <div class="category-count" style="color: {color};">
                        {icon} {count}
                    </div>
                    <div class="category-status">
                        {count} Finding{'s' if count != 1 else ''}
                    </div>
                    <div style="font-size: 10px; color: #64748b; margin-top: 6px;">
                        {subtitle}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_forensic_evidence(case: Dict[str, Any]):
    """Renders detailed forensic evidence cards with observations and locations."""
    st.markdown("### 🔬 FORENSIC EVIDENCE")
    evidence_items = case.get("evidence", [])

    if not evidence_items:
        st.info("✅ No anomalous forensic evidence observed across the inspected parameters.")
        return

    # Filter selector if many items
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Showing all {len(evidence_items)} forensic observations. Note: Observations indicate potential irregularities warranting human verification.")
    with col2:
        filter_opt = st.selectbox("Filter Severity", ["All", "HIGH", "MEDIUM", "LOW"], key="ev_filter", label_visibility="collapsed")

    filtered = [e for e in evidence_items if filter_opt == "All" or e["severity"] == filter_opt]

    for item in filtered:
        sev = item.get("severity", "LOW")
        card_class = "evidence-card-high" if sev == "HIGH" else (
            "evidence-card-med" if sev in ["MEDIUM", "ELEVATED"] else "evidence-card-low"
        )
        badge = get_severity_badge_html(sev)

        st.markdown(
            f"""
            <div class="evidence-card {card_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                    <div class="evidence-title">
                        <b>{item.get('id')}</b> — {item.get('title')}
                    </div>
                    <div>{badge}</div>
                </div>
                <div class="evidence-location">
                    📍 Page {item.get('page', 1)} • {item.get('region', 'Document Canvas')}
                </div>
                <div class="evidence-desc">
                    {item.get('description')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def draw_bounding_boxes_on_image(image: Image.Image, regions: List[Dict[str, Any]], selected_region_id: Optional[str] = None) -> Image.Image:
    """Draws colored rectangular bounding boxes and region labels on document image."""
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated)

    color_map = {
        "HIGH": (239, 68, 68),       # Red
        "ELEVATED": (249, 115, 22),   # Orange
        "MEDIUM": (249, 115, 22),
        "LOW": (234, 179, 8),        # Yellow
    }

    img_w, img_h = annotated.size

    for r in regions:
        sev = r.get("severity", "ELEVATED")
        is_selected = (selected_region_id == r.get("id"))
        box_color = (59, 130, 246) if is_selected else color_map.get(sev, (249, 115, 22))
        line_width = 4 if is_selected else 3

        rx = max(0, min(r.get("x", 0), img_w - 10))
        ry = max(0, min(r.get("y", 0), img_h - 10))
        rw = min(r.get("width", 50), img_w - rx)
        rh = min(r.get("height", 50), img_h - ry)

        # Draw box
        draw.rectangle([rx, ry, rx + rw, ry + rh], outline=box_color, width=line_width)

        # Draw label tag banner
        label_text = f" {r.get('id', 'Region')} "
        tag_w = len(label_text) * 8 + 8
        tag_h = 18
        draw.rectangle([rx, max(0, ry - tag_h), rx + tag_w, ry], fill=box_color)
        draw.text((rx + 4, max(0, ry - tag_h) + 2), label_text, fill=(255, 255, 255))

    return annotated


def render_suspicious_regions(case: Dict[str, Any], file_path: str):
    """Renders the document preview with interactive highlighted regions."""
    st.markdown("### 🖼️ SUSPICIOUS REGIONS")
    regions = case.get("regions", [])

    if not regions:
        st.markdown(
            """
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 24px; text-align: center; color: #94a3b8;">
                🟢 No anomalous visual regions or compression discontinuities detected on document preview.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Extract document pages
    pages = extract_document_pages_as_images(file_path, max_pages=3)
    total_pages = len(pages)

    p_col1, p_col2 = st.columns([1, 1])

    # Region quick buttons
    doc_sha = case.get("document", {}).get("sha256", "default")[:10]
    reg_key = f"selected_region_{doc_sha}"

    with p_col1:
        st.markdown("**Detected Regions:**")
        reg_btn_cols = st.columns(min(len(regions), 4))
        valid_ids = [r["id"] for r in regions]
        selected_region = st.session_state.get(reg_key)
        if not selected_region or selected_region not in valid_ids:
            selected_region = valid_ids[0] if valid_ids else None
            st.session_state[reg_key] = selected_region

        for idx, r in enumerate(regions[:4]):
            col = reg_btn_cols[idx]
            sev_icon = "🔴" if r["severity"] == "HIGH" else "🟠"
            with col:
                if st.button(f"{sev_icon} {r['id']}", key=f"btn_reg_{doc_sha}_{r['id']}", use_container_width=True):
                    st.session_state[reg_key] = r["id"]
                    selected_region = r["id"]

        # Show active region info
        target_reg = next((r for r in regions if r["id"] == selected_region), regions[0])
        st.markdown(
            f"""
            <div style="background: #1e293b; border-left: 4px solid {'#ef4444' if target_reg['severity'] == 'HIGH' else '#f97316'}; border-radius: 6px; padding: 12px; margin-top: 10px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">
                    {target_reg['id']} (Page {target_reg.get('page', 1)})
                </div>
                <div style="font-size: 12px; color: #94a3b8; font-family: monospace; margin: 4px 0;">
                    Coordinates: [X: {target_reg.get('x')}, Y: {target_reg.get('y')}, W: {target_reg.get('width')}, H: {target_reg.get('height')}]
                </div>
                <div style="font-size: 13px; color: #cbd5e1;">
                    <b>Reason:</b> {target_reg.get('reason', 'Visual anomaly detected')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page_to_show = target_reg.get("page", 1) - 1
        page_to_show = max(0, min(page_to_show, total_pages - 1))

    with p_col2:
        st.markdown(f"**Visual Preview (Page {page_to_show + 1}):**")
        base_img = pages[page_to_show]
        page_regions = [r for r in regions if r.get("page", 1) == page_to_show + 1]
        annotated_img = draw_bounding_boxes_on_image(base_img, page_regions, selected_region)
        st.image(annotated_img, caption=f"Document Canvas — Page {page_to_show + 1} with Highlighted Regions", use_container_width=True)


def render_tampering_hypotheses(case: Dict[str, Any]):
    """Renders Tampering Hypotheses with evidence references and strict objective language."""
    st.markdown("### 🎯 TAMPERING HYPOTHESES")
    hypotheses = case.get("hypotheses", [])

    if not hypotheses:
        st.markdown(
            """
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 16px; color: #94a3b8;">
                🟢 No conclusive tampering hypotheses formulated. Inspected features demonstrate baseline consistency.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for h in hypotheses:
        sev = h.get("severity", "LOW")
        sev_color = "#ef4444" if sev == "HIGH" else ("#f97316" if sev in ["ELEVATED", "MEDIUM"] else "#eab308")
        sev_icon = "🔴" if sev == "HIGH" else ("🟠" if sev in ["ELEVATED", "MEDIUM"] else "🟡")
        ev_pills = " ".join([f"<span style='background: #1e293b; color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; margin-right: 4px;'>{eid}</span>" for eid in h.get("evidence", [])])

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">
                        {sev_icon} {h.get('title')}
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">
                        Corroborating Evidence: {ev_pills}
                    </div>
                </div>
                <div>
                    <span style='background: rgba({ "239, 68, 68, 0.15" if sev == "HIGH" else "249, 115, 22, 0.15"}); color: {sev_color}; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 6px;'>
                        {sev} CONFIDENCE
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("ℹ️ *Note: Tampering hypotheses represent investigative avenues based on anomalous patterns, not definitive legal proof.*")


def render_origin_indicators(case: Dict[str, Any]):
    """Renders Origin Indicators with required disclaimer."""
    st.markdown("### 🤖 ORIGIN INDICATORS")
    origins = case.get("origin_indicators", {})

    syn_status = origins.get("synthetic_ai", "NOT DETECTED")
    img_status = origins.get("image_manipulation", "NOT DETECTED")

    col1, col2 = st.columns(2)

    def get_status_badge(status):
        if status == "DETECTED":
            return '<span class="badge-high">🔴 DETECTED</span>'
        elif status == "POSSIBLE":
            return '<span class="badge-elevated">🟠 POSSIBLE</span>'
        else:
            return '<span class="badge-clean">🟢 NOT DETECTED</span>'

    with col1:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">
                    Synthetic / AI Indicators
                </div>
                <div style="margin-top: 6px;">
                    {get_status_badge(syn_status)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">
                    Image Manipulation Indicators
                </div>
                <div style="margin-top: 6px;">
                    {get_status_badge(img_status)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Required prominent disclaimer
    st.markdown(
        """
        <div class="disclaimer-box">
            <b>⚠ MANDATORY FORENSIC NOTICE:</b> Origin indicators are calculated from pattern heuristics and error rate disparities.
            Indicators are <u>not conclusive proof</u> of artificial intelligence generation or document forgery.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_assessment(case: Dict[str, Any]):
    """Renders the AI / Gemma reasoning section."""
    st.markdown("### 🧠 AI REASONING SYNTHESIS")
    assessment = case.get("ai_assessment", "Assessment unavailable.")
    source = case.get("ai_source", "Gemma Forensic Reasoner")

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 18px 22px;">
            <div style="font-size: 12px; font-weight: 700; color: #818cf8; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 6px;">
                {source}
            </div>
            <div style="font-size: 14px; color: #f1f5f9; line-height: 1.6;">
                "{assessment}"
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_manual_verification(case: Dict[str, Any]):
    """Renders interactive manual verification checklist for the human investigator."""
    doc_sha = case.get("document", {}).get("sha256", "default")[:10]
    recs = case.get("recommendations", [
        "Verify suspicious date / number",
        "Inspect highlighted regions",
        "Compare with trusted source if available",
        "Verify with issuing authority",
    ])

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### ⚠️ MANUAL VERIFICATION")
    with col_h2:
        if st.button("↺ Reset Checklist", key=f"reset_chk_btn_{doc_sha}", help="Reset checkmarks for this document"):
            for idx in range(len(recs)):
                st.session_state[f"chk_{doc_sha}_{idx}"] = False
            st.rerun()

    completed_checks = 0
    for idx, rec in enumerate(recs):
        widget_key = f"chk_{doc_sha}_{idx}"
        is_checked = st.checkbox(rec, key=widget_key)
        if is_checked:
            completed_checks += 1

    progress = completed_checks / max(len(recs), 1)
    st.progress(progress, text=f"Human Examiner Verification Progress: {completed_checks} / {len(recs)} Actions Completed")


def render_file_details_and_export(case: Dict[str, Any]):
    """Renders file technical specs and Export Report button."""
    st.markdown("### 📋 FILE DETAILS & REPORT EXPORT")
    doc = case.get("document", {})
    summary = case.get("summary", {})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <table style="width: 100%; font-size: 13px; color: #cbd5e1;">
                <tr><td style="color: #64748b; padding: 4px 0;">File Type:</td><td><b>{doc.get('file_type', 'PDF')}</b></td></tr>
                <tr><td style="color: #64748b; padding: 4px 0;">File Size:</td><td><b>{doc.get('file_size', 'N/A')}</b></td></tr>
                <tr><td style="color: #64748b; padding: 4px 0;">Page Count:</td><td><b>{doc.get('pages', 1)}</b></td></tr>
            </table>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <table style="width: 100%; font-size: 13px; color: #cbd5e1;">
                <tr><td style="color: #64748b; padding: 4px 0;">SHA-256:</td><td><code style="font-size: 11px;">{doc.get('sha256', 'N/A')}</code></td></tr>
                <tr><td style="color: #64748b; padding: 4px 0;">Coverage:</td><td><b>{summary.get('checks_completed', 8)} / {summary.get('checks_total', 10)} Checks</b></td></tr>
            </table>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # Export Buttons
    e_col1, e_col2, e_col3 = st.columns(3)

    # 1. PDF Report
    pdf_report_path = os.path.join("reports", f"VERIDOC_Report_{doc.get('filename')}.pdf")
    try:
        generate_pdf_report(case, pdf_report_path)
        with open(pdf_report_path, "rb") as f:
            pdf_bytes = f.read()
        with e_col1:
            st.download_button(
                label="📄 Export PDF Report",
                data=pdf_bytes,
                file_name=f"VERIDOC_Report_{doc.get('filename')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except Exception as e:
        with e_col1:
            st.error(f"PDF generation note: {e}")

    # 2. Markdown Report
    md_content = generate_markdown_report(case)
    with e_col2:
        st.download_button(
            label="📝 Export Markdown",
            data=md_content,
            file_name=f"VERIDOC_Report_{doc.get('filename')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # 3. JSON Export
    json_content = generate_json_report(case)
    with e_col3:
        st.download_button(
            label="💾 Export JSON Case",
            data=json_content,
            file_name=f"VERIDOC_Case_{doc.get('filename')}.json",
            mime="application/json",
            use_container_width=True,
        )


def render_recent_documents_section():
    """Renders recent document analyses loaded from SQLite."""
    cases = get_recent_cases(limit=6)

    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 16px; font-weight: 700; color: #f8fafc;">
                🕘 RECENT DOCUMENTS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not cases:
        st.caption("No recent analyses stored yet. Upload a document or load a demo sample above.")
        return

    for c in cases:
        sev = c.get("severity", "LOW")
        sev_badge = get_severity_badge_html(sev)
        cid = c.get("id")

        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.markdown(f"**📄 {c.get('filename')}**")
            st.caption(f"{c.get('file_type')} • {c.get('pages', 1)} Page(s) • {c.get('formatted_time')}")
        with col2:
            st.markdown(sev_badge, unsafe_allow_html=True)
        with col3:
            st.markdown(f"**{c.get('total_findings', 0)}** Findings")
            st.caption(f"{c.get('checks_completed', 8)}/{c.get('checks_total', 10)} Checks")
        with col4:
            b_open, b_del = st.columns(2)
            with b_open:
                if st.button("Open", key=f"rec_open_{cid}"):
                    from storage.database import get_case_by_id
                    loaded = get_case_by_id(cid)
                    if loaded:
                        st.session_state["current_case"] = loaded
                        st.rerun()
            with b_del:
                if st.button("✕", key=f"rec_del_{cid}", help="Delete record"):
                    delete_case(cid)
                    st.rerun()
