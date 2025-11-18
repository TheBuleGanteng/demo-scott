import os
import streamlit as st
from typing import cast
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


def inject_custom_css() -> None:
    """Inject CSS for green primary button and full-screen spinner overlay."""
    st.markdown(
        """
        <style>
        /* Green primary button with hover animation */
        .stFormSubmitButton button,
        button[kind="primary"] {
            background-color: #22c55e !important;  /* green-500 */
            color: #ffffff !important;
            border-radius: 9999px !important;
            border: none !important;
            padding: 0.4rem 1.4rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition:
                background-color 150ms ease,
                transform 150ms ease,
                box-shadow 150ms ease;
        }

        .stFormSubmitButton button:hover,
        button[kind="primary"]:hover {
            background-color: #16a34a !important;  /* green-600 */
            transform: translateY(-1px);
            box-shadow: 0 8px 16px rgba(22, 163, 74, 0.35);
        }

        .stFormSubmitButton button:active,
        button[kind="primary"]:active {
            background-color: #15803d !important;  /* green-700 */
            transform: translateY(0);
            box-shadow: none;
        }

        /* Full-screen semi-opaque spinner overlay */
        div.stSpinner {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: rgba(0, 0, 0, 0.35) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 10000 !important;
        }

        /* Style the spinner text */
        div.stSpinner > div,
        div.stSpinner > div > div,
        div.stSpinner [data-testid="stMarkdownContainer"],
        div.stSpinner [data-testid="stText"],
        div.stSpinner p,
        div.stSpinner span {
            font-weight: bold !important;
            font-size: 1.5rem !important;
            text-align: center !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.warning(
        "⚠️ OPENAI_API_KEY is not set. "
        "Set it in your environment or in a .env file to generate opportunities."
    )

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_opportunities(process_text: str, primary_goal: str, industry: str | None) -> str:
    """
    Call the LLM to generate AI opportunities for the provided process.
    Returns markdown text.
    """
    system_prompt = f"""
You are an AI strategist helping large US-based enterprises identify high-ROI AI use cases.

The user will describe an existing business process.
Your job is to propose 3–5 concrete AI solutions.

For each solution, return:

1. **Name**
2. **One-sentence description**
3. **Primary value driver**: Cost Savings | Revenue Uplift | Risk Reduction
4. **Estimated impact** on that value driver: Low | Medium | High
5. **Implementation complexity**: Low | Medium | High
6. **Key data required**
7. **Suggested MVP** that could be tested within 4–6 weeks

Optimize your suggestions for the user's stated primary goal: {primary_goal}.
Industry context (optional): {industry or "not specified"}.

Be specific and practical, not buzzwordy.
Ground your answers in realistic enterprise constraints (data quality, governance, IT/security review, etc.).
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": process_text},
        ],
        temperature=0.4,
    )

    return cast(str, response.choices[0].message.content)


def main() -> None:
    st.set_page_config(
        page_title="AI Opportunity Finder (Prototype)",
        layout="wide",
    )
    
    # Apply button + spinner styling
    inject_custom_css()

    st.title("AI Opportunity Finder (Prototype)")
    st.caption(
        "Paste a brief description of a current workflow and get concrete AI opportunities "
        "with impact & complexity estimates."
    )

    with st.form("process_form"):
        process_text = st.text_area(
            "1. Describe the current process",
            height=220,
            placeholder=(
                "Example: Our customer support team handles ~2,000 emails per day. "
                "Agents manually read each email, classify the issue, reply using templates, "
                "and escalate to Tier 2 when they’re unsure..."
            ),
        )

        primary_goal = st.selectbox(
            "2. What is the main goal?",
            ["Cost savings", "Revenue uplift", "Risk reduction / compliance"],
        )

        industry = st.text_input(
            "3. (Optional) Industry / context",
            placeholder="e.g., banking, insurance, retail, B2B SaaS",
        )

        submitted = st.form_submit_button("Generate AI opportunities", type="primary")

    if submitted:
        if not process_text.strip():
            st.error("Please describe the current process before generating opportunities.")
            return

        if not OPENAI_API_KEY:
            st.error(
                "OPENAI_API_KEY is not configured. "
                "Set it in your environment or in a .env file and restart the app."
            )
            return

        with st.spinner("Thinking through opportunities..."):
            ideas_markdown = generate_opportunities(process_text, primary_goal, industry or None)

        st.markdown("### Suggested AI Opportunities")
        st.markdown(ideas_markdown)


if __name__ == "__main__":
    main()

