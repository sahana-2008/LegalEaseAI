import streamlit as st
from pathlib import Path

from utils.document_export import (
    format_docx,
    format_pdf,
    format_txt,
)

from utils.text_utils import sanitize_text


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("⚖️ LegalEase")

st.write(
    "AI-powered legal document drafting, editing and export."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("📋 LegalEase")

    mode = st.radio(
        "Choose Mode",
        [
            "Draft Document",
            "Edit Document",
            "Export Document",
        ],
    )

    st.divider()

    st.info(
        "LegalEase is an AI-assisted document tool. "
        "Always review generated legal content before using it."
    )


# ---------------------------------------------------------
# DRAFT DOCUMENT
# ---------------------------------------------------------

if mode == "Draft Document":

    st.header("📝 Draft Legal Document")

    document_type = st.selectbox(
        "Select Document Type",
        [
            "Legal Notice",
            "Rental Agreement",
            "Employment Agreement",
            "Affidavit",
            "Complaint",
            "Application",
            "General Legal Document",
        ],
    )

    user_details = st.text_area(
        "Enter the details for your document",
        placeholder=(
            "Example:\n"
            "Name: Rahul Kumar\n"
            "Purpose: Rental agreement\n"
            "Property: Chennai\n"
            "Duration: 11 months\n"
            "Monthly rent: ₹15,000"
        ),
        height=220,
    )

    if st.button("✨ Generate Draft", use_container_width=True):

        if not user_details.strip():
            st.warning("Please enter the document details.")
        else:

            clean_details = sanitize_text(user_details)

            generated_document = f"""
{document_type.upper()}

This document has been prepared based on the information provided by the user.

DETAILS PROVIDED

{clean_details}

IMPORTANT NOTICE

This is an AI-assisted draft intended for informational and editing purposes.
The document should be reviewed carefully and, where appropriate, checked
by a qualified legal professional before use.

Generated using LegalEase.
"""

            st.session_state["document"] = generated_document

            st.success("Document draft created successfully.")


# ---------------------------------------------------------
# EDIT DOCUMENT
# ---------------------------------------------------------

elif mode == "Edit Document":

    st.header("✏️ Edit Legal Document")

    existing_document = st.text_area(
        "Paste your existing legal document",
        placeholder="Paste your document text here...",
        height=350,
    )

    editing_instruction = st.text_area(
        "What would you like to change?",
        placeholder=(
            "Example:\n"
            "Make the language more professional.\n"
            "Correct grammar.\n"
            "Make the document easier to understand."
        ),
        height=150,
    )

    if st.button("✨ Apply Changes", use_container_width=True):

        if not existing_document.strip():
            st.warning("Please enter a document first.")

        elif not editing_instruction.strip():
            st.warning("Please enter an editing instruction.")

        else:

            clean_document = sanitize_text(existing_document)
            clean_instruction = sanitize_text(editing_instruction)

            edited_document = f"""
EDITED LEGAL DOCUMENT

{clean_document}

EDITOR'S INSTRUCTION

{clean_instruction}

NOTE

The above document has been prepared as an AI-assisted editing draft.
Please review all legal details before use.
"""

            st.session_state["document"] = edited_document

            st.success("Document edited successfully.")


# ---------------------------------------------------------
# EXPORT DOCUMENT
# ---------------------------------------------------------

elif mode == "Export Document":

    st.header("📤 Export Legal Document")

    current_document = st.session_state.get("document", "")

    if not current_document:

        st.info(
            "No document is available yet. "
            "Create or edit a document first."
        )

    else:

        st.subheader("Document Preview")

        st.text_area(
            "Preview",
            current_document,
            height=400,
        )

        st.divider()

        st.subheader("Download Options")

        col1, col2, col3 = st.columns(3)

        # -------------------------------------------------
        # TXT
        # -------------------------------------------------

        with col1:

            if st.button(
                "📄 Prepare TXT",
                use_container_width=True,
            ):

                file_path = format_txt(current_document)

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download TXT",
                        file,
                        file_name=Path(file_path).name,
                        mime="text/plain",
                        use_container_width=True,
                    )

        # -------------------------------------------------
        # DOCX
        # -------------------------------------------------

        with col2:

            if st.button(
                "📝 Prepare DOCX",
                use_container_width=True,
            ):

                file_path = format_docx(current_document)

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download DOCX",
                        file,
                        file_name=Path(file_path).name,
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document"
                        ),
                        use_container_width=True,
                    )

        # -------------------------------------------------
        # PDF
        # -------------------------------------------------

        with col3:

            if st.button(
                "📕 Prepare PDF",
                use_container_width=True,
            ):

                file_path = format_pdf(current_document)

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download PDF",
                        file,
                        file_name=Path(file_path).name,
                        mime="application/pdf",
                        use_container_width=True,
                    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "⚖️ LegalEase — AI-powered legal document drafting, "
    "editing and export."
)
