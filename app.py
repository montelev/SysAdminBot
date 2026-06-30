import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

# Prefer Streamlit Cloud secrets, fall back to local .env
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = os.getenv("GROQ_API_KEY", "")

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SysAdminBot",
    page_icon="🖥️",
    layout="centered",
)

st.title("🖥️ SysAdminBot")
st.caption(
    "AI-powered infrastructure scripting — type a task in plain English and get "
    "a production-ready PowerShell or Bash script instantly."
)
st.divider()

# ---------------------------------------------------------------------------
# System prompt factory
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """You are a Senior Systems Administrator with 15+ years of enterprise experience.
Your ONLY job is to produce a complete, production-ready {lang} script based on the task the user describes.

Rules you MUST follow without exception:
1. Output ONLY the script — no markdown fences, no preamble, no trailing prose.
2. Begin the script with a comment block that includes: Purpose, Author placeholder, Date placeholder, and Version.
3. Every non-trivial line of code must have an inline comment explaining what it does.
4. Wrap all risky operations in try/catch (PowerShell) or trap/set -e (Bash) error handling.
5. Define all configurable values (usernames, group names, paths, etc.) as clearly named variables at the top.
6. Follow the principle of least privilege — never use blanket admin rights when a scoped permission suffices.
7. If the task involves credentials, use secure credential objects — never plaintext passwords.
8. If the task is ambiguous or potentially destructive, add a prominent WARNING comment inside the script.
9. End the script with a brief "# --- END OF SCRIPT ---" comment.

Target environment: {env_label}
"""

def build_system_prompt(lang: str, env_label: str) -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(lang=lang, env_label=env_label)


# ---------------------------------------------------------------------------
# Sidebar — configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    environment = st.radio(
        "Target Environment",
        options=["Windows Server (PowerShell)", "Linux / macOS (Bash)"],
        index=0,
    )

    st.divider()
    st.markdown("**About**")
    st.markdown(
        "SysAdminBot uses the Google Gemini API to translate plain-English "
        "IT tasks into secure, commented scripts ready for production use."
    )
    st.markdown(
        "[Get a free Gemini API key](https://aistudio.google.com/app/apikey)",
        unsafe_allow_html=False,
    )

    st.divider()
    api_key_input = st.text_input(
        "Groq API Key (overrides .env)",
        type="password",
        placeholder="Paste key here to use without .env",
    )

# If the user pasted a key in the sidebar, use it for this session
if api_key_input.strip():
    genai.configure(api_key=api_key_input.strip())
    effective_key = api_key_input.strip()
else:
    effective_key = API_KEY

# ---------------------------------------------------------------------------
# Derive language / label from environment selection
# ---------------------------------------------------------------------------
if "Windows" in environment:
    lang = "PowerShell"
    env_label = "Windows Server (Active Directory / IIS / Hyper-V capable)"
    lang_tag = "powershell"
else:
    lang = "Bash"
    env_label = "Linux / macOS (systemd, cron, OpenSSH capable)"
    lang_tag = "bash"

# ---------------------------------------------------------------------------
# Main input area
# ---------------------------------------------------------------------------
example_tasks = {
    "PowerShell": "Create an Active Directory group called 'Sales-Full-Access' and add the user 'jdoe' to it.",
    "Bash": "Create a new Linux user called 'devops_svc', lock the account from password login, and add them to the 'docker' group.",
}

task_input = st.text_area(
    f"📋 Describe your {lang} task",
    height=130,
    placeholder=example_tasks[lang],
)

generate_btn = st.button("⚡ Generate Script", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------
if generate_btn:
    if not effective_key:
        st.error(
            "No Gemini API key found. Add `GEMINI_API_KEY` to your `.env` file "
            "or paste it in the sidebar."
        )
        st.stop()

    if not task_input.strip():
        st.warning("Please describe a task before generating.")
        st.stop()

    with st.spinner(f"Generating {lang} script…"):
        try:
            client = Groq(api_key=effective_key)
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": build_system_prompt(lang, env_label)},
                    {"role": "user", "content": task_input.strip()},
                ],
                temperature=0.2,
            )
            script_output = chat.choices[0].message.content.strip()

            # Strip accidental markdown fences the model sometimes adds
            if script_output.startswith("```"):
                lines = script_output.splitlines()
                script_output = "\n".join(
                    line for line in lines
                    if not line.strip().startswith("```")
                ).strip()

        except Exception as exc:
            st.error(f"Groq API error: {exc}")
            st.stop()

    st.success("Script generated successfully!")
    st.divider()

    st.subheader(f"📄 Generated {lang} Script")
    st.code(script_output, language=lang_tag)

    st.download_button(
        label=f"⬇️ Download script{'  (.ps1)' if lang == 'PowerShell' else '  (.sh)'}",
        data=script_output,
        file_name=f"sysadminbot_script.{'ps1' if lang == 'PowerShell' else 'sh'}",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()
    st.caption(
        "⚠️ **Administrator's Note:** Always review generated scripts in a test "
        "environment before deploying to production. Verify permissions and "
        "variable values match your specific infrastructure."
    )
