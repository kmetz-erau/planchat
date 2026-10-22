
Loading older messages…
streamlit cloud
That is a Streamlit Cloud startup/dependency issue. The page-scanning code has not run yet.

Add a requirements.txt file in the same folder as your app:

streamlit
PyMuPDF
Pillow
requests
Important: use PyMuPDF, not fitz; your code imports fitz, but PyMuPDF provides that module.

Also verify:

Your entry file is named app.py.
requirements.txt is in the repository root or beside app.py.
Streamlit Cloud → Manage app → Secrets contains:
OLLAMA_API_KEY = "your-key"
Then use Reboot app or redeploy. Streamlit Cloud installs dependencies from requirements.txt located beside the entrypoint or in the repository root. 

If it still spins, check Manage app → Logs. If there are no build logs at all, check Streamlit’s service status.

did all that
Worked for 11s
Then the next step is the deployment log—this spinner alone doesn’t identify the cause.

In Streamlit Cloud:

Open the app.
Click ⋮ → Manage app.
Open Logs.
Copy the first red traceback or the last 30 lines, if present.
If the logs are completely blank, try Reboot app once. If it still hangs, create a temporary app.py containing only:

import streamlit as st

st.title("Startup test")
st.success("Streamlit is running")
If that also spins, it’s a Streamlit Cloud/repository deployment issue.
If it loads, the issue is in the app code or dependency environment.
Send me the log output or the result of that startup test.

improve response, speed it up BATCH 1 — pages 1–4]
Based on the provided pages (1 through 4), there are no electrical panels shown or listed. These pages consist of the Cover Sheet, General Notes, Mechanical Schedules, and Ceiling Plans for HVAC replacement 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf.

[BATCH 2 — pages 5–8]
Based on the provided pages (pages 5 through 8), there are no electrical panels visible. These pages consist of Mechanical (HVAC) demolition and new installation plans, including thermostat panels (T-STAT PANEL) and roof plan details 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf.

[BATCH 3 — pages 9–12]
Based on the provided pages (pages 9, 10, 11, and 12), there are no electrical panels shown or listed. These pages contain mechanical floor plans, roof plans, sequence of operations, and controls specifications 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf.

[BATCH 4 — pages 13–16]
Based on the provided pages (13, 14, 15, and 16), there are no electrical panels visible. These pages consist of HVAC system details and mechanical specifications 📄  ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf.

[BATCH 5 — pages 17–20]
Based on the provided pages, the following electrical panels/distribution boards are listed in the Symbol Legend:

120V/208V Branch Circuit Panelboard, Surface Mounted 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 19
120V/208V Branch Circuit Panelboard, Recessed Mounted 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 19
Enclosed Cable Case Circuit Breaker Bin 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 19
These pages contain a legend of symbols rather than a floor plan; therefore, I cannot count the total quantity of panels installed in the building from this batch.

[BATCH 6 — pages 21–24]
Based on the provided pages, I count 4 electrical panels:

PANEL ACP-1: First Floor Plan - Demo - Electrical 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 21
PANEL ACP-2: First Floor Plan - Demo - Electrical 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 21
PANEL ACP-3: First Floor Plan - Demo - Electrical 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 21
PP-2: Roof Plan - Demo - Electrical 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 23
[BATCH 7 — pages 25–28]
Based on the provided pages from batch 7, I count 2 electrical panels:

PANEL ACP-1 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 26
PANEL ACP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 26
[BATCH 8 — pages 29–32]
Based on the provided pages, the following electrical panels are identified:

Plan Views (Page 29):

Janitor RM 214: Panel HAC-1, Panel EP-1 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 29
Server Room 114: Panel DP-1, Panel HAC-1, Panel HAC-2, Panel EP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 29
Mechanical Room: Panel DP-1, Panel DP-2, Panel EP-1, Panel EP-2, Panel HAC-1, Panel HAC-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 29
Riser Diagram (Page 30):

Mechanical/Electrical Room 214: Panel HAC-1, Panel RP-1, Panel LP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 30
Electrical/Mechanical Room: Panel DP-1, Panel DP-2, Panel RP-1, Panel LP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 30
Mechanical Room 114: Panel DP-1, Panel EP-1 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 30
Equipment Yard 1: Panel EP-1 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 30
Equipment Yard 2: Panel EP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 30
Panel Schedules (Pages 31-32):

Page 31: Existing DP-1, Revised ACP-1, Existing ACP-3, Revised ACP-3, Existing ACP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 31
Page 32: Existing HAC-2, Existing HAC-1, Existing EP-2, Revised HAC-2, Revised HAC-1, Revised EP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 32
[BATCH 9 — pages 33–34]
Based on the provided Equipment Feeder Schedule on page 33, there are 13 distinct electrical panels listed:

LP-1 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-2 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-3 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-4 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-5 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-6 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-7 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-8 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-9 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-10 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-11 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-12 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
LP-13 📄 ALUMNI CENTER - ISSUE FOR PERMIT - SIGNED AND SEALED (1).pdf, page 33
…
Improved and saved:

Reviews all pages.
Uses 8 pages per vision request instead of 4.
Reduces image size for faster uploads.
Limits model output to 450 tokens.
Removes repetitive introductions and unrelated descriptions.
Separates unique panels, page occurrences, and legend/schedule items.

Pasted text(20261022-124450).txt
Document
i need the response to be better. When I ask how many electical panels it needs to comes back with the total count and the names
Updated the app so electrical-panel count questions now return:

Total distinct electrical panels: #
Panel names: ...
Source pages: ...
Notes: ...
It deduplicates repeated panel appearances across plans, risers, schedules, and legends.


Pasted text(20261022-124450).txt
Document
what if i ask how many ahus?
It will now handle questions like:

“How many AHUs?”
“How many RTUs?”
“How many VAVs?”
“How many pumps?”
“How many boilers?”
“How many chillers?”
It returns:

Total distinct items requested: #
Names/identifiers: ...
Source pages: ...
Notes: ...
It also deduplicates repeated equipment across plans, schedules, risers, and legends.


Pasted text(20261022-124450).txt
Document
import base64
import html
import io
import json
import re
from datetime import datetime

import fitz
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="PlanChat AI", page_icon="📐", layout="wide")

MAX_TOTAL_MB = 45
PAGE_BATCH_SIZE = 8
PDF_SCALE = 1.25
JPEG_QUALITY = 68
OLLAMA_HOST = "https://ollama.com"
OLLAMA_MODEL = "gemma4:31b-cloud"
OLLAMA_API_KEY = st.secrets["OLLAMA_API_KEY"]

st.markdown("""
<style>
.stApp{background:#111827;color:#f3f4f6}
section[data-testid="stSidebar"]{background:#1f2937}
.user-bubble{background:#2563eb;color:white;padding:10px 14px;border-radius:18px 18px 4px 18px;margin:6px 0 6px 15%;line-height:1.6}
.model-bubble{background:#1f2937;color:#e5e7eb;padding:10px 14px;border-radius:18px 18px 18px 4px;margin:6px 15% 6px 0;line-height:1.6;border:1px solid #374151;white-space:pre-wrap}
.file-chip{display:inline-block;background:#1e3a5f;color:#93c5fd;padding:2px 8px;border-radius:99px;font-size:11px}
</style>
""", unsafe_allow_html=True)


def init_state():
    defaults = {
        "messages": [],
        "uploaded_files": [],
        "active_file_idx": 0,
        "active_page_idx": 0,
        # Keep a separate page position for every file.  Streamlit reruns the
        # script after every widget interaction, so one global page index can
        # otherwise make the viewer jump back to the cover page.
        "page_by_file": {},
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()


def pdf_to_images(pdf_bytes: bytes) -> list[Image.Image]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    matrix = fitz.Matrix(PDF_SCALE, PDF_SCALE)
    try:
        for page in doc:
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB, alpha=False)
            images.append(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    finally:
        doc.close()
    return images


def image_to_base64(img: Image.Image) -> str:
    # Encode once at upload time instead of on every question.
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def process_uploaded_file(uploaded) -> dict | None:
    name = uploaded.name
    data = uploaded.read()
    size_mb = len(data) / (1024 * 1024)
    current_total = sum(f["size_mb"] for f in st.session_state.uploaded_files)

    if current_total + size_mb > MAX_TOTAL_MB:
        st.error(f"Skipped {name}: total upload limit is {MAX_TOTAL_MB} MB.")
        return None

    ext = name.lower().rsplit(".", 1)[-1]
    try:
        if ext == "pdf":
            pages = pdf_to_images(data)
            file_type = "pdf"
        elif ext in {"png", "jpg", "jpeg", "tif", "tiff", "webp", "bmp"}:
            pages = [Image.open(io.BytesIO(data)).convert("RGB")]
            file_type = "image"
        else:
            st.warning(f"Skipped {name}: unsupported format.")
            return None
    except Exception as exc:
        st.error(f"Failed to read {name}: {exc}")
        return None

    return {
        "name": name,
        "pages": pages,
        "pages_b64": [image_to_base64(page) for page in pages],
        "page_count": len(pages),
        "size_mb": size_mb,
        "type": file_type,
    }


def build_ollama_messages(user_text: str, selected_pages=None) -> list:
    files = st.session_state.uploaded_files
    messages = [{
        "role": "system",
        "content": f"""You are PlanChat AI, a technical assistant for drawings and construction documents.
You are not a Licensed Professional Engineer. Be concise and technical.
Uploaded files:
{chr(10).join(f"({i + 1}) {f['name']} — {f['page_count']} pages" for i, f in enumerate(files))}
After each fact, dimension, or observation cite the source as [[Citation:ExactFileName]].
Only claim what is visible. Flag clearly unsafe conditions."""
    }]

    # Keep only recent turns; old turns add latency and rarely help with drawing questions.
    for msg in st.session_state.messages[-6:]:
        if msg["text"].startswith(("✅ Loaded", "⚠️")):
            continue
        messages.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["text"],
        })

    # The viewer's current page is only for display.  When no batch is passed,
    # include every page; the caller may pass a smaller batch to avoid an
    # oversized vision request.
    if selected_pages is None:
        selected = [
            (file["name"], page_idx, encoded)
            for file in files
            for page_idx, encoded in enumerate(file["pages_b64"])
        ]
    else:
        selected = selected_pages

    content = []
    for image_no, (name, page_idx, encoded) in enumerate(selected, 1):
        content.extend([
            {"type": "text", "text": f"Image {image_no}: {name}, page {page_idx + 1}"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{encoded}"
            }},
        ])
    content.append({"type": "text", "text": user_text})
    messages.append({"role": "user", "content": content})
    return messages


def build_consolidation_messages(question: str, batch_reports: list[str]) -> list:
    files = st.session_state.uploaded_files
    reports = "\n\n".join(
        f"--- Batch {i + 1} ---\n{report}"
        for i, report in enumerate(batch_reports)
    )
    return [
        {
            "role": "system",
            "content": f"""You are consolidating page-by-page drawing reviews for PlanChat AI.
Uploaded files:
{chr(10).join(f"- {f['name']}" for f in files)}

Answer the user's question using only the batch reports below. For electrical-panel count
questions, deduplicate repeated appearances of the same panel across plans, risers, schedules,
and legends. Count distinct panel identifiers, not every occurrence. Treat existing/revised
versions as one panel unless the question explicitly asks for existing versus revised.
Return exactly this format:
Total distinct electrical panels: <number>
Panel names: <comma-separated names>
Source pages: <panel name: page numbers; ...>
Notes: <one short note about legend-only items, uncertainty, or scope>
Do not include batch headings or a narrative introduction.""",
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nBatch reports:\n{reports}",
        },
    ]


def stream_ollama_response(messages: list):
    response_url = f"{OLLAMA_HOST}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
    }
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
        "max_tokens": 450,
    }

    try:
        with requests.post(
            response_url, json=payload, headers=headers,
            stream=True, timeout=(20, 180)
        ) as response:
            if not response.ok:
                yield f"⚠️ Ollama error {response.status_code}: {response.text}"
                return

            for raw_line in response.iter_lines(decode_unicode=True):
                if not raw_line or not raw_line.startswith("data: "):
                    continue
                data = raw_line[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue
    except requests.exceptions.ConnectionError:
        yield f"⚠️ Cannot connect to Ollama Cloud at {OLLAMA_HOST}."
    except requests.exceptions.Timeout:
        yield "⚠️ Request timed out. Try analyzing one page instead of all pages."


def render_with_citations(text: str) -> str:
    safe = html.escape(text)
    return re.sub(
        r"\[\[Citation:([^\]]+)\]\]",
        r'<span class="file-chip">📄 \1</span>',
        safe,
    )


def generate_report() -> str:
    lines = [
        "OFFICIAL RECORD OF REVIEW — PLANCHAT AI",
        "=" * 72,
        f"DATE: {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"MODEL: {OLLAMA_MODEL} @ {OLLAMA_HOST}",
        "NOTE: AI output only. Not a PE-stamped document.",
        "",
        "[DOCUMENTS]",
    ]
    for i, file in enumerate(st.session_state.uploaded_files, 1):
        lines.append(f"{i}. {file['name']} ({file['page_count']} pages)")
    lines += ["", "[TRANSCRIPT]", "-" * 72]
    for msg in st.session_state.messages:
        if msg["text"].startswith("✅ Loaded"):
            continue
        role = "REQUESTER" if msg["role"] == "user" else "PLANCHAT AI"
        lines.append(f"\n{role}:\n{msg['text']}\n" + "-" * 72)
    return "\n".join(lines)


with st.sidebar:
    st.markdown("## 📐 PlanChat AI")
    st.warning("AI assistant only. Not a Licensed PE. Verify all outputs.")

    uploaded = st.file_uploader(
        "Drop PDFs or images",
        type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "webp"],
        accept_multiple_files=True,
    )

    if uploaded:
        existing = {f["name"] for f in st.session_state.uploaded_files}
        new_count = 0
        for uploaded_file in uploaded:
            if uploaded_file.name in existing:
                continue
            with st.spinner(f"Processing {uploaded_file.name}..."):
                result = process_uploaded_file(uploaded_file)
            if result:
                st.session_state.uploaded_files.append(result)
                existing.add(uploaded_file.name)
                new_count += 1

        if new_count:
            total_pages = sum(f["page_count"] for f in st.session_state.uploaded_files)
            st.session_state.messages.append({
                "role": "model",
                "text": f"✅ Loaded {new_count} file(s) — {total_pages} pages ready.",
                "timestamp": datetime.now().timestamp(),
            })
            st.rerun()

    files = st.session_state.uploaded_files
    if files:
        st.markdown("### Loaded files")
        for i, file in enumerate(files):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                if st.button(f"📄 {file['name'][:24]}", key=f"file_{i}"):
                    if st.session_state.active_file_idx != i:
                        st.session_state.active_file_idx = i
                        st.session_state.active_page_idx = st.session_state.page_by_file.get(
                            file["name"], 0
                        )
                        st.rerun()
            with col_b:
                if st.button("✕", key=f"delete_{i}"):
                    files.pop(i)
                    st.session_state.page_by_file.pop(file["name"], None)
                    st.session_state.active_file_idx = 0
                    st.session_state.active_page_idx = 0
                    st.rerun()

        total_pages = sum(f["page_count"] for f in files)
        st.caption(f"{len(files)} file(s) · {total_pages} pages")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🗂️ Clear files", use_container_width=True):
            st.session_state.uploaded_files = []
            st.session_state.page_by_file = {}
            st.session_state.active_file_idx = 0
            st.session_state.active_page_idx = 0
            st.rerun()

    if st.session_state.messages:
        st.download_button(
            "📄 Download report",
            generate_report(),
            file_name=f"PlanChat_Report_{datetime.now():%Y-%m-%d}.txt",
            mime="text/plain",
            use_container_width=True,
        )

left_col, right_col = st.columns([3, 2], gap="medium")

with left_col:
    st.markdown("#### 📐 Drawing viewer")
    files = st.session_state.uploaded_files
    if not files:
        st.info("Upload plans in the sidebar to begin.")
    else:
        file_idx = min(st.session_state.active_file_idx, len(files) - 1)
        active_file = files[file_idx]
        st.session_state.active_file_idx = file_idx

        if active_file["page_count"] > 1:
            file_key = active_file["name"]
            saved_page = min(
                st.session_state.page_by_file.get(file_key, 0),
                active_file["page_count"] - 1,
            )
            page_idx = st.slider(
                "Page",
                1,
                active_file["page_count"],
                saved_page + 1,
                key=f"page_{file_key}",
            ) - 1
        else:
            page_idx = 0

        # Persist the viewer position by filename, not only in the transient
        # widget value.  This survives reruns caused by chat, uploads, and
        # changing files without forcing the user back to page 1.
        st.session_state.page_by_file[active_file["name"]] = page_idx
        st.session_state.active_page_idx = page_idx

        if active_file["page_count"] > 1:
            previous_col, next_col = st.columns(2)
            with previous_col:
                if st.button(
                    "← Previous page",
                    disabled=page_idx == 0,
                    use_container_width=True,
                    key=f"previous_{file_key}",
                ):
                    st.session_state.page_by_file[file_key] = page_idx - 1
                    st.session_state[f"page_{file_key}"] = page_idx
                    st.rerun()
            with next_col:
                if st.button(
                    "Next page →",
                    disabled=page_idx >= active_file["page_count"] - 1,
                    use_container_width=True,
                    key=f"next_{file_key}",
                ):
                    st.session_state.page_by_file[file_key] = page_idx + 1
                    st.session_state[f"page_{file_key}"] = page_idx + 2
                    st.rerun()

        st.image(
            active_file["pages"][page_idx],
            use_container_width=True,
            caption=f"{active_file['name']} · page {page_idx + 1}",
        )

with right_col:
    st.markdown("#### 💬 Ask PlanChat")
    chat_container = st.container(height=480)

    with chat_container:
        for msg in st.session_state.messages:
            css = "user-bubble" if msg["role"] == "user" else "model-bubble"
            body = (
                html.escape(msg["text"])
                if msg["role"] == "user"
                else render_with_citations(msg["text"])
            )
            st.markdown(f'<div class="{css}">{body}</div>', unsafe_allow_html=True)

    has_files = bool(st.session_state.uploaded_files)
    input_col, button_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input(
            "Message",
            placeholder="Ask about the drawings..." if has_files else "Upload plans first",
            disabled=not has_files,
            label_visibility="collapsed",
            key="chat_input",
        )
    with button_col:
        send = st.button(
            "Send",
            disabled=not has_files or not user_input.strip(),
            use_container_width=True,
        )

    if send and user_input.strip():
        user_text = user_input.strip()
        st.session_state.messages.append({
            "role": "user",
            "text": user_text,
            "timestamp": datetime.now().timestamp(),
        })

        all_pages = [
            (file["name"], page_idx, encoded)
            for file in st.session_state.uploaded_files
            for page_idx, encoded in enumerate(file["pages_b64"])
        ]
        full_response = ""
        batch_reports = []
        response_placeholder = chat_container.empty()
        batches = [
            all_pages[start:start + PAGE_BATCH_SIZE]
            for start in range(0, len(all_pages), PAGE_BATCH_SIZE)
        ]

        for batch_no, page_batch in enumerate(batches, 1):
            batch_text = (
                f"Analyze pages in batch {batch_no} of {len(batches)} for this question. "
                "Use only the pages shown in this batch. Be concise: return only findings "
                "that answer the question, with page numbers. Do not repeat the question, "
                "do not add an introduction, and do not describe unrelated pages. "
                "For equipment or panel-count questions, separate: (1) unique identifiers, "
                "(2) occurrences by page, and (3) legend/schedule-only items. Do not count "
                "a legend, riser, or schedule as a separate installed item unless the question "
                "specifically asks for listed items. Flag existing/revised status when visible.\n\n"
                f"Question: {user_text}"
            )
            batch_response = ""
            response_placeholder.markdown(
                f'<div class="model-bubble">Reviewing page batch '
                f'{batch_no}/{len(batches)}…</div>',
                unsafe_allow_html=True,
            )
            for chunk in stream_ollama_response(
                build_ollama_messages(batch_text, selected_pages=page_batch)
            ):
                batch_response += chunk
                response_placeholder.markdown(
                    f'<div class="model-bubble">Reviewing page batch '
                    f'{batch_no}/{len(batches)}…<br><br>'
                    f'{render_with_citations(batch_response)} ▌</div>',
                    unsafe_allow_html=True,
                )
            full_response += (
                f"\n\n[BATCH {batch_no} — pages "
                f"{page_batch[0][1] + 1}–{page_batch[-1][1] + 1}]\n"
                f"{batch_response}"
            )
            batch_reports.append(batch_response)

        lower_question = user_text.lower()
        is_panel_count_question = (
            "panel" in lower_question
            and any(term in lower_question for term in (
                "how many", "count", "number", "total", "list", "names"
            ))
        )
        if is_panel_count_question:
            response_placeholder.markdown(
                '<div class="model-bubble">Consolidating and deduplicating panel names…</div>',
                unsafe_allow_html=True,
            )
            consolidated = ""
            for chunk in stream_ollama_response(
                build_consolidation_messages(user_text, batch_reports)
            ):
                consolidated += chunk
                response_placeholder.markdown(
                    f'<div class="model-bubble">{render_with_citations(consolidated)} ▌</div>',
                    unsafe_allow_html=True,
                )
            full_response = consolidated

        response_placeholder.markdown(
            f'<div class="model-bubble">{render_with_citations(full_response)}</div>',
            unsafe_allow_html=True,
        )
        st.session_state.messages.append({
            "role": "model",
            "text": full_response,
            "timestamp": datetime.now().timestamp(),
        })
        st.rerun()


