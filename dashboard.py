import os
import streamlit as st
from utils.file_handler import validate_file, save_temp_file
from pipeline.analyzer import analyze_document
from frontend.styles import FORENSIC_CSS
from frontend.components import (
    render_header,
    render_current_analysis_header,
    render_forensic_categories,
    render_forensic_evidence,
    render_suspicious_regions,
    render_tampering_hypotheses,
    render_origin_indicators,
    render_ai_assessment,
    render_manual_verification,
    render_file_details_and_export,
    render_recent_documents_section,
)


def render_dashboard():
    """Main forensic investigation dashboard layout."""
    st.markdown(FORENSIC_CSS, unsafe_allow_html=True)

    # 1. Top Header
    render_header()

    # 2. New Analysis Container
    st.markdown("### 📂 NEW ANALYSIS")

    u_col1, u_col2 = st.columns([3, 2])

    with u_col1:
        uploaded_file = st.file_uploader(
            "Drop PDF / Image Here or Browse File",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Supported formats: PDF, PNG, JPG, JPEG (Max 30MB)",
            key="file_uploader"
        )

    with u_col2:
        st.markdown("**Or Quick-Load Demo Documents:**")
        d_col1, d_col2, d_col3 = st.columns(3)

        sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_documents")

        with d_col1:
            if st.button("🔴 Certificate 2026\n(High Concern)", key="load_sample_high", use_container_width=True):
                sample_file = os.path.join(sample_dir, "Certificate_2026.pdf")
                if os.path.exists(sample_file):
                    st.session_state["active_file_path"] = sample_file
                    st.session_state["active_filename"] = "Certificate_2026.pdf"
                    st.session_state["trigger_analysis"] = True

        with d_col2:
            if st.button("🟠 Invoice 4582\n(Elevated)", key="load_sample_med", use_container_width=True):
                sample_file = os.path.join(sample_dir, "Invoice_4582.pdf")
                if os.path.exists(sample_file):
                    st.session_state["active_file_path"] = sample_file
                    st.session_state["active_filename"] = "Invoice_4582.pdf"
                    st.session_state["trigger_analysis"] = True

        with d_col3:
            if st.button("🟢 Genuine Cert\n(Low Concern)", key="load_sample_low", use_container_width=True):
                sample_file = os.path.join(sample_dir, "Certificate_Genuine.pdf")
                if os.path.exists(sample_file):
                    st.session_state["active_file_path"] = sample_file
                    st.session_state["active_filename"] = "Certificate_Genuine.pdf"
                    st.session_state["trigger_analysis"] = True

    # Process Uploaded File
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        is_valid, err_msg = validate_file(uploaded_file.name, len(file_bytes))
        if not is_valid:
            st.error(f"❌ {err_msg}")
        else:
            temp_path = save_temp_file(file_bytes, uploaded_file.name)
            # Only set if different from current
            if st.session_state.get("active_file_path") != temp_path:
                st.session_state["active_file_path"] = temp_path
                st.session_state["active_filename"] = uploaded_file.name
                st.session_state["trigger_analysis"] = True

    # Analysis Action Bar
    active_path = st.session_state.get("active_file_path")
    active_name = st.session_state.get("active_filename")

    if active_path:
        st.markdown(f"**Selected File:** `{active_name}`")
        if st.button("⚡ START FORENSIC ANALYSIS", type="primary", use_container_width=True) or st.session_state.get("trigger_analysis"):
            st.session_state["trigger_analysis"] = False

            progress_bar = st.progress(0, text="Initializing forensic analysis...")
            status_placeholder = st.empty()

            def update_progress(val, text):
                progress_bar.progress(val, text=text)
                status_placeholder.caption(f"🔬 Processing: {text}")

            try:
                case = analyze_document(
                    active_path,
                    original_filename=active_name,
                    progress_callback=update_progress
                )
                st.session_state["current_case"] = case
                st.session_state["current_case_file_path"] = active_path
                status_placeholder.empty()
                progress_bar.empty()
                st.success("✅ Forensic Analysis Completed Successfully.")
                st.rerun()
            except Exception as e:
                status_placeholder.empty()
                progress_bar.empty()
                st.error(f"Analysis failed: {str(e)}")

    st.markdown("<hr style='border-color: #1e293b; margin: 24px 0;'/>", unsafe_allow_html=True)

    # 3. Recent Documents Strip
    render_recent_documents_section()

    st.markdown("<hr style='border-color: #1e293b; margin: 28px 0;'/>", unsafe_allow_html=True)

    # 4. Current Analysis Case Presentation
    current_case = st.session_state.get("current_case")
    case_file_path = st.session_state.get("current_case_file_path", active_path)

    if current_case:
        # A. Current Analysis Header
        render_current_analysis_header(current_case)
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        # B. Forensic Categories
        render_forensic_categories(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # C. Forensic Evidence
        render_forensic_evidence(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # D. Suspicious Regions
        if case_file_path and os.path.exists(case_file_path):
            render_suspicious_regions(current_case, case_file_path)
            st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # E. Tampering Hypotheses
        render_tampering_hypotheses(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # F. Origin Indicators
        render_origin_indicators(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # G. AI Reasoning
        render_ai_assessment(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # H. Manual Verification
        render_manual_verification(current_case)
        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # I. File Details & Export Report
        render_file_details_and_export(current_case)

    else:
        # Default placeholder when no analysis has run yet
        st.info("👆 Upload a document or select one of the sample test documents above to begin forensic analysis.")
