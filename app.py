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
MAX_VISION_PAGES = 8
PDF_SCALE = 1.25
JPEG_QUALITY = 78
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
        "analyze_all_pages": False,
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


def build_ollama_messages(user_text: str) -> list:
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

    selected = []
    if st.session_state.analyze_all_pages:
        for file in files:
            for page_idx, encoded in enumerate(file["pages_b64"]):
                selected.append((file["name"], page_idx, encoded))
                if len(selected) >= MAX_VISION_PAGES:
                    break
            if len(selected) >= MAX_VISION_PAGES:
                break
    elif files:
        file_idx = min(st.session_state.active_file_idx, len(files) - 1)
        file = files[file_idx]
        page_idx = min(st.session_state.active_page_idx, file["page_count"] - 1)
        selected.append((file["name"], page_idx, file["pages_b64"][page_idx]))

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
        "max_tokens": 800,
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
        st.session_state.analyze_all_pages = st.checkbox(
            "Analyze all pages",
            value=st.session_state.analyze_all_pages,
            help=f"Send at most {MAX_VISION_PAGES} pages per question.",
        )

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

        full_response = ""
        response_placeholder = chat_container.empty()
        with st.spinner("Thinking..."):
            for chunk in stream_ollama_response(build_ollama_messages(user_text)):
                full_response += chunk
                response_placeholder.markdown(
                    f'<div class="model-bubble">{render_with_citations(full_response)} ▌</div>',
                    unsafe_allow_html=True,
                )

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
