import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from ai_core.gemini_generator import GeminiDocumentGenerator
import streamlit as st
from pathlib import Path

from ai_core.gemini_generator import GeminiDocumentGenerator

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
# INITIALIZE AI
# ---------------------------------------------------------

generator = GeminiDocumentGenerator()


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

    if generator.client:
        st.success("🤖 Gemini AI Connected")
    else:
        st.warning("⚠️ Gemini AI Not Connected")

    st.info(
        "LegalEase is an AI-assisted document tool. "
        "Always review generated legal content before using it."
    )


# =========================================================
# DRAFT DOCUMENT
# =========================================================

if mode == "Draft Document":

    st.header("📝 Draft Legal Document")

    # -----------------------------------------------------
    # DOCUMENT TYPE
    # -----------------------------------------------------

    document_type = st.selectbox(
        "1. Document Type",
        [
            "Contract",
            "Non-Disclosure Agreement (NDA)",
            "Rental Agreement",
            "Employment Agreement",
            "Affidavit",
            "Legal Notice",
            "Complaint",
            "Application",
            "General Legal Document",
        ],
    )

    # -----------------------------------------------------
    # PARTIES INVOLVED
    # -----------------------------------------------------

    parties = st.text_area(
        "2. Parties Involved",
        placeholder=(
            "Example:\n"
            "Party 1: Sahana\n"
            "Party 2: Rahul"
        ),
        height=120,
    )

    # -----------------------------------------------------
    # TERMS AND CONDITIONS
    # -----------------------------------------------------

    terms = st.text_area(
        "3. Terms and Conditions",
        placeholder=(
            "Example:\n"
            "Monthly rent: ₹15,000\n"
            "Duration: 11 months\n"
            "Property: Chennai\n"
            "Payment must be made every month."
        ),
        height=180,
    )

    # -----------------------------------------------------
    # EFFECTIVE DATE
    # -----------------------------------------------------

    effective_date = st.date_input(
        "4. Effective Date"
    )

    # -----------------------------------------------------
    # GENERATE BUTTON
    # -----------------------------------------------------

    if st.button(
        "✨ Generate Legal Document",
        use_container_width=True,
    ):

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not parties.strip():

            st.warning(
                "Please enter the parties involved."
            )

        elif not terms.strip():

            st.warning(
                "Please enter the terms and conditions."
            )

        elif not generator.client:

            st.error(
                "Gemini AI is not connected. "
                "Please check GEMINI_API_KEY in the .env file."
            )

        else:

            # ---------------------------------------------
            # CLEAN USER INPUT
            # ---------------------------------------------

            clean_parties = sanitize_text(
                parties
            )

            clean_terms = sanitize_text(
                terms
            )

            # ---------------------------------------------
            # GEMINI PROMPT
            # ---------------------------------------------

            prompt = f"""
You are a professional legal document drafting assistant.

Create a structured and professional legal document using ONLY
the information provided by the user.

DOCUMENT TYPE:
{document_type}

PARTIES INVOLVED:
{clean_parties}

TERMS AND CONDITIONS:
{clean_terms}

EFFECTIVE DATE:
{effective_date}

IMPORTANT INSTRUCTIONS:

1. Create a properly structured legal document.
2. Use clear and professional legal language.
3. Add suitable headings and clauses.
4. Use only the information provided by the user.
5. Do not invent names, dates, amounts, addresses, or obligations.
6. Do not change the parties involved.
7. Do not change the terms and conditions.
8. Include the effective date provided above.
9. Add signature sections where appropriate.
10. Return only the legal document.
11. Do not provide explanations before or after the document.

Generate the final document now.
"""

            # ---------------------------------------------
            # GENERATE USING GEMINI
            # ---------------------------------------------

            try:

                with st.spinner(
                    "🤖 Gemini AI is preparing your document..."
                ):

                    response = generator.client.models.generate_content(
                        model=generator.model,
                        contents=prompt,
                    )

                generated_document = response.text or ""

                # -----------------------------------------
                # SHOW RESULT
                # -----------------------------------------

                if generated_document.strip():

                    st.session_state["document"] = (
                        generated_document.strip()
                    )

                    st.success(
                        "✅ Legal document generated successfully!"
                    )

                    st.subheader(
                        "📄 Generated Document"
                    )

                    st.text_area(
                        "Document Preview",
                        generated_document,
                        height=550,
                    )

                else:

                    st.error(
                        "Gemini returned an empty response."
                    )

            except Exception as e:

                st.error(
                    f"AI document generation failed: {e}"
                )


# =========================================================
# EDIT DOCUMENT
# =========================================================

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

    if st.button(
        "✨ Apply Changes",
        use_container_width=True,
    ):

        if not existing_document.strip():

            st.warning(
                "Please enter a document first."
            )

        elif not editing_instruction.strip():

            st.warning(
                "Please enter an editing instruction."
            )

        elif not generator.client:

            st.error(
                "Gemini AI is not connected. "
                "Please check GEMINI_API_KEY in the .env file."
            )

        else:

            clean_document = sanitize_text(
                existing_document
            )

            clean_instruction = sanitize_text(
                editing_instruction
            )

            prompt = f"""
You are a professional legal document editing assistant.

Rewrite the following legal document according to the user's
editing instruction.

EXISTING DOCUMENT:
{clean_document}

EDITING INSTRUCTION:
{clean_instruction}

Rules:
- Keep the original meaning.
- Do not change names, dates, amounts, addresses, or important facts
  unless the user explicitly asks you to change them.
- Improve grammar and clarity when requested.
- Use clear and professional legal language.
- Preserve important information.
- Return only the edited document.
- Do not include explanations.
"""

            try:

                with st.spinner(
                    "🤖 Gemini AI is editing your document..."
                ):

                    response = generator.client.models.generate_content(
                        model=generator.model,
                        contents=prompt,
                    )

                edited_document = response.text or ""

                if edited_document.strip():

                    st.session_state["document"] = (
                        edited_document.strip()
                    )

                    st.success(
                        "✅ Document edited successfully."
                    )

                    st.subheader(
                        "📄 Edited Document"
                    )

                    st.text_area(
                        "Edited Document Preview",
                        edited_document,
                        height=500,
                    )

                else:

                    st.error(
                        "Gemini returned an empty response."
                    )

            except Exception as e:

                st.error(
                    f"AI document editing failed: {e}"
                )


# =========================================================
# EXPORT DOCUMENT
# =========================================================

elif mode == "Export Document":

    st.header("📤 Export Legal Document")

    current_document = st.session_state.get(
        "document",
        "",
    )

    if not current_document:

        st.info(
            "No document is available yet. "
            "Create or edit a document first."
        )

    else:

        st.subheader("📄 Document Preview")

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

                file_path = format_txt(
                    current_document
                )

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download TXT",
                        file,
                        file_name=Path(
                            file_path
                        ).name,
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

                file_path = format_docx(
                    current_document
                )

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download DOCX",
                        file,
                        file_name=Path(
                            file_path
                        ).name,
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

                file_path = format_pdf(
                    current_document
                )

                with open(
                    file_path,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇️ Download PDF",
                        file,
                        file_name=Path(
                            file_path
                        ).name,
                        mime="application/pdf",
                        use_container_width=True,
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "⚖️ LegalEase — AI-powered legal document drafting, "
    "editing and export."
)


