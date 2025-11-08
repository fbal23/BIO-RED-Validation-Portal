#!/usr/bin/env python3
"""
BIO-RED T2.1 Partner Data Validation Portal
Streamlit web interface for partners to upload and validate data submissions
"""

import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add parent directory to path to import validation module
sys.path.append(str(Path(__file__).parent.parent))
from scripts.validate_submission import validate_file, TEMPLATE_SCHEMAS

# Page configuration
st.set_page_config(
    page_title="BIO-RED Data Validation Portal",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #C8E6C9;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFF9C4;
        border-left: 5px solid #FFC107;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFCDD2;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔬 BIO-RED Data Validation Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload and validate your data submissions before formal submission</div>', unsafe_allow_html=True)

# Sidebar - Partner Information and Instructions
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    ### How to use this portal:

    1. **Select your region** from the dropdown
    2. **Choose template type** you want to validate
    3. **Upload your Excel file**
    4. **Review validation results**
    5. **Fix any errors** and re-upload if needed

    ---

    ### Template Types:

    1. **Organization Registry** - Partner organizations
    2. **Stakeholder Mapping** - Key stakeholders
    3. **Value Chain Mapping** - Value chains
    4. **Funding Sources** - Available funding
    5. **Focus Group Notes** - Focus group data
    6. **Interview Summary** - Interview insights
    7. **Business Case Profile** - Success stories
    8. **Trend Brief** - Emerging trends
    9. **Policy Analysis** - Policy landscape

    ---

    ### Quality Standards:

    - ✅ **95% completeness** required
    - ✅ All **required fields** must be present
    - ✅ Valid **data types** (numbers, URLs, emails)
    - ✅ **Dropdown values** must match template

    ---

    ### Need Help?

    📧 Email: support@biored-project.eu
    📱 AI Assistant available 24/7
    """)

    st.divider()

    # Partner region selection
    partner_region = st.selectbox(
        "Select Your Region",
        ["Portugal (PT16)", "Greece (EL54)", "Lithuania (LT01)",
         "Bulgaria (BG41)", "France (FR10)", "Denmark (DK01)", "Sweden (SE12)"],
        help="Choose your partner region"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📤 Upload Your Data File")

    # Template type selection
    template_options = {
        "1. Organization Registry": "1_Organization_Registry",
        "2. Stakeholder Mapping": "2_Stakeholder_Mapping",
        "3. Value Chain Mapping": "3_Value_Chain_Mapping",
        "4. Funding Sources": "4_Funding_Sources",
        "5. Focus Group Notes": "5_Focus_Group_Notes",
        "6. Interview Summary": "6_Interview_Summary",
        "7. Business Case Profile": "7_Business_Case_Profile",
        "8. Trend Brief": "8_Trend_Brief",
        "9. Policy Analysis": "9_Policy_Analysis"
    }

    selected_template = st.selectbox(
        "Select Template Type",
        list(template_options.keys()),
        help="Choose the template type you are submitting"
    )

    template_key = template_options[selected_template]

    # File upload
    uploaded_file = st.file_uploader(
        "Upload Excel File (.xlsx)",
        type=["xlsx"],
        help="Upload your completed template file for validation"
    )

with col2:
    st.header("ℹ️ Template Info")

    if template_key in TEMPLATE_SCHEMAS:
        schema = TEMPLATE_SCHEMAS[template_key]

        st.markdown(f"""
        <div class="info-box">
            <strong>Required Fields:</strong> {len(schema.get('required_fields', []))}
            <br>
            <strong>Optional Fields:</strong> {len(schema.get('optional_fields', []))}
            <br>
            <strong>Dropdown Fields:</strong> {len(schema.get('dropdowns', {}))}
        </div>
        """, unsafe_allow_html=True)

        # Show required fields
        with st.expander("View Required Fields"):
            for field in schema.get('required_fields', []):
                st.write(f"- {field.replace('_', ' ')}")

        # Special note for Organization Registry
        if template_key == "1_Organization_Registry":
            st.info("""
            **Enhancement Targets:**
            - Min 30 enhanced CORDIS orgs
            - Min 10 new organizations
            - Min 3 fields per enhanced org
            """)

# Process uploaded file
if uploaded_file is not None:
    st.divider()

    # Save uploaded file temporarily
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file_path = temp_dir / f"{uploaded_file.name}"

    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Validate the file
    with st.spinner("🔍 Validating your submission..."):
        try:
            # Run validation
            validation_report = validate_file(str(temp_file_path))

            # Display results
            st.header("📊 Validation Results")

            # Status header
            status = validation_report['status']
            if status == "VALIDATED":
                st.markdown(f"""
                <div class="success-box">
                    <h2>✅ VALIDATION PASSED</h2>
                    <p>Your submission meets all quality standards!</p>
                </div>
                """, unsafe_allow_html=True)
            elif status == "VALIDATED_WITH_WARNINGS":
                st.markdown(f"""
                <div class="warning-box">
                    <h2>⚠️ VALIDATED WITH WARNINGS</h2>
                    <p>Your submission is acceptable but has some warnings. Please review below.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-box">
                    <h2>❌ VALIDATION FAILED</h2>
                    <p>Your submission has errors that must be fixed before formal submission.</p>
                </div>
                """, unsafe_allow_html=True)

            # Metrics in columns
            st.subheader("Summary Metrics")
            metric_cols = st.columns(4)

            with metric_cols[0]:
                st.metric("Total Errors", validation_report['summary']['total_errors'])
            with metric_cols[1]:
                st.metric("Total Warnings", validation_report['summary']['total_warnings'])
            with metric_cols[2]:
                st.metric("Checks Passed", validation_report['summary']['checks_passed'])
            with metric_cols[3]:
                st.metric("Checks Failed", validation_report['summary']['checks_failed'])

            # Errors section
            if validation_report['errors']:
                st.subheader("❌ Errors to Fix")
                for idx, error in enumerate(validation_report['errors'], 1):
                    st.error(f"{idx}. {error}")

            # Warnings section
            if validation_report['warnings']:
                st.subheader("⚠️ Warnings")
                for idx, warning in enumerate(validation_report['warnings'], 1):
                    st.warning(f"{idx}. {warning}")

            # Detailed validation results
            st.subheader("🔍 Detailed Validation Checks")

            results = validation_report['validation_results']

            # Schema compliance
            if 'schema_compliance' in results:
                with st.expander("Schema Compliance", expanded=True):
                    check = results['schema_compliance']
                    status_icon = "✅" if check['status'] == "PASS" else "❌"
                    st.write(f"**Status:** {status_icon} {check['status']}")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Present Fields:**")
                        for field in check.get('present_fields', []):
                            st.write(f"✅ {field.replace('_', ' ')}")

                    with col_b:
                        if check.get('missing_fields'):
                            st.write("**Missing Fields:**")
                            for field in check['missing_fields']:
                                st.write(f"❌ {field.replace('_', ' ')}")

            # Completeness
            if 'completeness' in results:
                with st.expander("Data Completeness", expanded=True):
                    check = results['completeness']
                    status_icon = "✅" if check['status'] == "PASS" else "⚠️"

                    completeness_pct = check['overall'] * 100
                    target_pct = check['target'] * 100

                    st.write(f"**Status:** {status_icon} {check['status']}")
                    st.progress(check['overall'])
                    st.write(f"**Overall Completeness:** {completeness_pct:.1f}% (Target: {target_pct:.0f}%)")

                    # Field-level completeness
                    if check.get('field_stats'):
                        st.write("**Field-level Completeness:**")
                        field_df = pd.DataFrame(check['field_stats']).T
                        field_df['completeness_pct'] = (field_df['completeness'] * 100).round(1)
                        field_df = field_df[['filled', 'total', 'completeness_pct']]
                        field_df.columns = ['Filled', 'Total', 'Completeness (%)']
                        st.dataframe(field_df, use_container_width=True)

                    # Low completeness fields
                    if check.get('low_completeness_fields'):
                        st.warning("**Fields with low completeness (<80%):**")
                        for field, stats in check['low_completeness_fields'].items():
                            st.write(f"- {field.replace('_', ' ')}: {stats['completeness']*100:.1f}%")

            # Data types
            if 'data_types' in results:
                with st.expander("Data Type Validation"):
                    check = results['data_types']
                    status_icon = "✅" if check['status'] == "PASS" else "❌"
                    st.write(f"**Status:** {status_icon} {check['status']}")

                    if check.get('errors'):
                        for error in check['errors']:
                            st.error(error)
                    else:
                        st.success("All data types are valid!")

            # Dropdown validation
            if 'dropdown_validation' in results:
                with st.expander("Dropdown Value Validation"):
                    check = results['dropdown_validation']
                    status_icon = "✅" if check['status'] == "PASS" else "❌"
                    st.write(f"**Status:** {status_icon} {check['status']}")

                    if check.get('invalid_values'):
                        st.error("**Invalid dropdown values found:**")
                        for field, invalid_vals in check['invalid_values'].items():
                            st.write(f"- **{field.replace('_', ' ')}:** {', '.join(invalid_vals)}")
                    else:
                        st.success("All dropdown values are valid!")

            # Quality metrics
            if 'quality_metrics' in results:
                with st.expander("Quality Metrics"):
                    metrics = results['quality_metrics']

                    metric_cols2 = st.columns(4)
                    with metric_cols2[0]:
                        st.metric("Total Rows", metrics.get('total_rows', 0))
                    with metric_cols2[1]:
                        st.metric("Non-Empty Rows", metrics.get('non_empty_rows', 0))
                    with metric_cols2[2]:
                        st.metric("Duplicates", metrics.get('duplicates', 0))
                    with metric_cols2[3]:
                        fields_used = metrics.get('fields_used', 0)
                        fields_total = metrics.get('fields_total', 0)
                        st.metric("Fields Used", f"{fields_used}/{fields_total}")

            # Enhancement targets (for Organization Registry)
            if 'enhancement_targets' in results:
                with st.expander("Enhancement Targets (Organization Registry)", expanded=True):
                    check = results['enhancement_targets']
                    status_icon = "✅" if check['status'] == "PASS" else "⚠️"
                    st.write(f"**Status:** {status_icon} {check['status']}")

                    enh_cols = st.columns(2)
                    with enh_cols[0]:
                        st.metric(
                            "Enhanced CORDIS Orgs",
                            check['enhanced_orgs'],
                            delta=check['enhanced_orgs'] - check['enhanced_target'],
                            delta_color="normal"
                        )
                        st.caption(f"Target: {check['enhanced_target']}")

                    with enh_cols[1]:
                        st.metric(
                            "New Organizations",
                            check['new_orgs'],
                            delta=check['new_orgs'] - check['new_target'],
                            delta_color="normal"
                        )
                        st.caption(f"Target: {check['new_target']}")

            # Download validation report
            st.divider()
            st.subheader("📥 Download Report")

            col_download1, col_download2 = st.columns(2)

            with col_download1:
                # JSON report
                report_json = json.dumps(validation_report, indent=2)
                st.download_button(
                    label="📄 Download JSON Report",
                    data=report_json,
                    file_name=f"{uploaded_file.name}_validation_report_{timestamp}.json",
                    mime="application/json"
                )

            with col_download2:
                # Summary text report
                summary_text = f"""BIO-RED T2.1 Validation Report
File: {uploaded_file.name}
Region: {partner_region}
Template: {selected_template}
Validation Time: {validation_report['metadata']['validation_timestamp']}

STATUS: {validation_report['status']}

SUMMARY:
- Total Errors: {validation_report['summary']['total_errors']}
- Total Warnings: {validation_report['summary']['total_warnings']}
- Checks Passed: {validation_report['summary']['checks_passed']}
- Checks Failed: {validation_report['summary']['checks_failed']}

ERRORS:
"""
                for error in validation_report['errors']:
                    summary_text += f"- {error}\n"

                summary_text += "\nWARNINGS:\n"
                for warning in validation_report['warnings']:
                    summary_text += f"- {warning}\n"

                st.download_button(
                    label="📝 Download Text Report",
                    data=summary_text,
                    file_name=f"{uploaded_file.name}_validation_summary_{timestamp}.txt",
                    mime="text/plain"
                )

            # Next steps
            st.divider()
            st.subheader("🎯 Next Steps")

            if status == "VALIDATED":
                st.success("""
                ✅ **Your file is ready for submission!**

                - Download the validation report for your records
                - Submit your file through the official submission portal
                - You will receive confirmation within 24 hours
                """)
            elif status == "VALIDATED_WITH_WARNINGS":
                st.warning("""
                ⚠️ **Your file can be submitted, but consider addressing warnings:**

                - Review the warnings above
                - Consider improving data completeness or enhancement targets
                - You can submit as-is or fix warnings and re-validate
                """)
            else:
                st.error("""
                ❌ **Please fix errors before submission:**

                1. Download the validation report
                2. Fix all errors listed above
                3. Re-upload your corrected file
                4. Repeat until validation passes

                Need help? Contact support@biored-project.eu
                """)

        except Exception as e:
            st.error(f"""
            **Validation Error:**

            An error occurred during validation: {str(e)}

            Please ensure:
            - Your file is a valid Excel (.xlsx) file
            - The file follows the correct template structure
            - All worksheets are present

            If the problem persists, contact support@biored-project.eu
            """)

        finally:
            # Clean up temporary file
            if temp_file_path.exists():
                temp_file_path.unlink()

else:
    # Initial state - show example
    st.info("""
    👆 **Get Started:**

    1. Select your region from the sidebar
    2. Choose the template type you want to validate
    3. Upload your Excel file
    4. Review the instant validation results

    ---

    **Why validate before submission?**

    - ✅ Get instant feedback on data quality
    - ✅ Reduce errors and rework
    - ✅ Speed up approval process
    - ✅ Ensure your data meets quality standards

    ---

    **Need templates?**

    Download templates from the [Partner Portal](https://fbal23.github.io/ProjMgmt/partner-portal.html)
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #757575; padding: 1rem;">
    BIO-RED T2.1 Regional Biohealth Ecosystem Analysis<br>
    Data Validation Portal v1.0 | Powered by Streamlit<br>
    © 2025 BIO-RED Consortium | <a href="mailto:support@biored-project.eu">support@biored-project.eu</a>
</div>
""", unsafe_allow_html=True)
