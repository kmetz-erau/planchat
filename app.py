import streamlit as st
import fitz  # PyMuPDF
import base64
import json
import requests
import io
import re
from PIL import Image
from datetime import datetime

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PlanChat AI",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CONFIG (secrets-based) ───────────────────────────────────────────────────
MAX_TOTAL_MB   = 45
OLLAMA_HOST    = "https://ollama.com"
OLLAMA_MODEL   = "kimi-k2.6:cloud"
OLLAMA_API_KEY = st.secrets["OLLAMA_API_KEY"]

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #111827; color: #f3f4f6; }
  section[data-testid="stSidebar"] { background-color: #1f2937; border-right: 1px solid #374151; }
  section[data-testid="stSidebar"] * { color: #d1d5db !important; }
  #MainMenu, footer, header { visibility: hidden; }

  .user-bubble {
    background: #2563eb;
    color: white;
    padding: 10px 14px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0 6px 15%;
    font-size: 14px;
    line-height: 1.6;
    word-wrap: break-word;
  }
  .model-bubble {
    background: #1f2937;
    color: #e5e7eb;
    padding: 10px 14px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 15% 6px 0;
    font-size: 14px;
    line-height: 1.6;
    border: 1px solid #374151;
    word-wrap: break-word;
    white-space: pre-wrap;
  }
  .model-bubble code {
    background: #374151;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 12px;
  }
  .file-chip {
    display: inline-block;
    background: #1e3a5f;
    border: 1px solid #2563eb55;
    color: #93c5fd;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
  }
  .status-bar {
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 11px;
    color: #9ca3af;
    text-align: center;
    margin-top: 8px;
  }
  .section-header {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    margin: 16px 0 8px 0;
  }
  .disclaimer {
    background: #7c2d12;
    border: 1px solid #c2410c;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
    color: #fed7aa;
    margin-bottom: 12px;
  }
  .stTextInput input, .stTextArea textarea {
    background-color: #1f2937 !important;
    color: #f3f4f6 !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
  }
  .stButton button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
  }
  .stButton button:hover { background-color: #1d4ed8 !important; }
  .streamlit-expanderHeader {
    background-color: #1f2937 !important;
    color: #d1d5db !important;
    border: 1px solid #374151 !important;
  }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages":        [],
        "uploaded_files":  [],
        "active_file_idx": 0,
        "ollama_host":     OLLAMA_HOST,
        "ollama_model":    OLLAMA_MODEL,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── PDF / IMAGE PROCESSING ───────────────────────────────────────────────────
def pdf_to_images(pdf_bytes: bytes, scale: float = 1.8) -> list:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    mat = fitz.Matrix(scale, scale)
    for page in doc:
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()
    return images


def image_to_base64(img: Image.Image, fmt: str = "PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def process_uploaded_file(uploaded) -> dict | None:
    name = uploaded.name
    data = uploaded.read()
    size_mb = len(data) / (1024 * 1024)

    current_total = sum(f.get("size_mb", 0) for f in st.session_state.uploaded_files)
    if current_total + size_mb > MAX_TOTAL_MB:
        st.error(f"⚠️ Skipped **{name}**: would exceed {MAX_TOTAL_MB}MB total limit.")
        return None

    ext = name.lower().split(".")[-1]

    if ext == "pdf":
        try:
            pages = pdf_to_images(data)
        except Exception as e:
            st.error(f"Failed to render {name}: {e}")
            return None
        return {
            "name": name, "pages": pages,
            "page_count": len(pages), "size_mb": size_mb, "type": "pdf"
        }
    elif ext in ("png", "jpg", "jpeg", "tif", "tiff", "webp", "bmp"):
        try:
            img = Image.open(io.BytesIO(data)).convert("RGB")
            return {
                "name": name, "pages": [img],
                "page_count": 1, "size_mb": size_mb, "type": "image"
            }
        except Exception as e:
            st.error(f"Failed to read {name}: {e}")
            return None
    else:
        st.warning(f"Skipped **{name}**: unsupported format.")
        return None


# ─── OLLAMA STREAMING ─────────────────────────────────────────────────────────
def build_ollama_messages(user_text: str) -> list:
    files   = st.session_state.uploaded_files
    history = st.session_state.messages

    system_prompt = f"""You are PlanChat AI — a specialized technical assistant for analyzing as-built drawings, blueprints, and construction documents.

CRITICAL: You are an AI, NOT a Licensed Professional Engineer (PE).

UPLOADED FILES:
{chr(10).join(f"({i+1}) {f['name']} — {f['page_count']} page(s)" for i, f in enumerate(files)) or "(none)"}

CITATION PROTOCOL (MANDATORY):
After every fact, dimension, or observation, cite the source file using: [[Citation:ExactFileName]]
Example: "The footing detail on [[Citation:Sheet-S101.pdf]] shows 12-inch spread footings."

BEHAVIORAL PROTOCOLS:
1. Use the vocabulary and rigor of a US Professional Engineer.
2. Only reference codes (IBC, NEC, ADA, NFPA) when visual evidence supports it.
3. Cross-reference between sheets when multiple files are present.
4. Flag any clearly unsafe conditions immediately.
5. Be direct, technical, and fact-based."""

    messages = [{"role": "system", "content": system_prompt}]

    # Prior conversation history (text only)
    for msg in history:
        # Skip system-generated file load messages
        if msg["text"].startswith("✅ Loaded") or msg["text"].startswith("⚠️"):
            continue
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})

    # Latest user turn — attach all page images as vision content
    content_parts = []
    for file in files:
        for page_img in file["pages"]:
            b64 = image_to_base64(page_img)
            content_parts.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"}
            })
    content_parts.append({"type": "text", "text": user_text})

    messages.append({"role": "user", "content": content_parts})
    return messages


def stream_ollama_response(messages: list):
    host  = st.session_state.ollama_host
    model = st.session_state.ollama_model
    url   = f"{host}/v1/chat/completions"

    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
    }

    payload = {
        "model":   model,
        "messages": messages,
        "stream":  True,
    }

    try:
        with requests.post(
            url, json=payload, headers=headers,
            stream=True, timeout=180
        ) as resp:
            if not resp.ok:
                yield f"⚠️ Ollama Cloud error {resp.status_code}: {resp.text}"
                return
            for raw_line in resp.iter_lines():
                if not raw_line:
                    continue
                line = raw_line.decode("utf-8")
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

    except requests.exceptions.ConnectionError:
        yield (
            f"⚠️ **Cannot connect to Ollama Cloud** at `{host}`\n\n"
            f"Check your API key in Streamlit secrets and ensure `{host}` is reachable."
        )
    except requests.exceptions.Timeout:
        yield "⚠️ Request timed out. The model may be loading a large image set — try again."


# ─── CITATION RENDERER ────────────────────────────────────────────────────────
def render_with_citations(text: str) -> str:
    def replacer(m):
        fname = m.group(1)
        return f'<span class="file-chip">📄 {fname}</span>'
    return re.sub(r'\[\[Citation:([^\]]+)\]\]', replacer, text)


# ─── REPORT GENERATOR ─────────────────────────────────────────────────────────
def generate_report() -> str:
    now = datetime.now()
    lines = [
        "OFFICIAL RECORD OF REVIEW — PLANCHAT AI",
        "=" * 72,
        f"DATE: {now.strftime('%Y-%m-%d')}   TIME: {now.strftime('%H:%M:%S')}",
        f"MODEL: {st.session_state.ollama_model} @ {st.session_state.ollama_host}",
        f"SESSION ID: {now.strftime('%Y%m%d%H%M%S').upper()}",
        "NOTE: AI output only. Not a PE-stamped document.",
        "=" * 72,
        "",
        "[DOCUMENTS]",
    ]
    for i, f in enumerate(st.session_state.uploaded_files):
        lines.append(f"  {i+1}. {f['name']}  ({f['page_count']} pages)")
    lines += ["", "[TRANSCRIPT]", "-" * 72]
    for msg in st.session_state.messages:
        if msg["text"].startswith("✅ Loaded"):
            continue
        role_label = "REQUESTER" if msg["role"] == "user" else "PLANCHAT AI"
        ts = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
        clean = msg["text"].replace("[[Citation:", "[").replace("]]", "]")
        lines.append(f"\n[{ts}] {role_label}:\n{clean}\n" + "-" * 72)
    lines.append("\n[END OF RECORD]")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px 0;">
      <div style="background:#1e40af22;border-radius:8px;padding:6px;">
        <span style="font-size:22px;">📐</span>
      </div>
      <div>
        <div style="font-size:18px;font-weight:800;color:#60a5fa;">PlanChat AI</div>
        <div style="font-size:10px;color:#6b7280;font-family:monospace;">
          CLOUD · gpt-oss:120b-cloud
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="disclaimer">⚠️ AI assistant only. Not a Licensed PE. Verify all outputs.</div>',
        unsafe_allow_html=True
    )

    # ── MODEL INFO (read-only on cloud) ──
    st.markdown('<div class="section-header">☁️ Ollama Cloud</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="status-bar" style="text-align:left;padding:10px 12px;">
      <div>🤖 <strong style="color:#93c5fd;">{OLLAMA_MODEL}</strong></div>
      <div style="margin-top:4px;">🔗 {OLLAMA_HOST}</div>
      <div style="margin-top:4px;">🔑 Key: ····{OLLAMA_API_KEY[-6:]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── FILE UPLOAD ──
    st.markdown('<div class="section-header">📁 Upload Plans</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop PDFs or images",
        type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded:
        existing_names = {f["name"] for f in st.session_state.uploaded_files}
        new_count = 0
        for uf in uploaded:
            if uf.name not in existing_names:
                with st.spinner(f"Processing {uf.name}…"):
                    result = process_uploaded_file(uf)
                if result:
                    st.session_state.uploaded_files.append(result)
                    existing_names.add(uf.name)
                    new_count += 1
        if new_count:
            total_pages = sum(f["page_count"] for f in st.session_state.uploaded_files)
            st.session_state.messages.append({
                "role":      "model",
                "text":      f"✅ Loaded {new_count} file(s) — {total_pages} total pages rendered for vision analysis. Ask me anything about the drawings.",
                "timestamp": datetime.now().timestamp()
            })
            st.rerun()

    # ── LOADED FILES LIST ──
    if st.session_state.uploaded_files:
        st.markdown('<div class="section-header">📂 Loaded Files</div>', unsafe_allow_html=True)
        for i, f in enumerate(st.session_state.uploaded_files):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                icon  = "📄" if f["type"] == "pdf" else "🖼️"
                label = f"{icon} {f['name'][:22]}{'…' if len(f['name']) > 22 else ''}"
                if st.button(label, key=f"file_btn_{i}", use_container_width=True):
                    st.session_state.active_file_idx = i
            with col_b:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.uploaded_files.pop(i)
                    st.session_state.active_file_idx = max(
                        0, min(st.session_state.active_file_idx,
                               len(st.session_state.uploaded_files) - 1)
                    )
                    st.rerun()

        total_pages = sum(f["page_count"] for f in st.session_state.uploaded_files)
        total_mb    = sum(f["size_mb"]    for f in st.session_state.uploaded_files)
        st.markdown(
            f'<div class="status-bar">🗂️ {len(st.session_state.uploaded_files)} file(s) · '
            f'{total_pages} pages · {total_mb:.1f} / {MAX_TOTAL_MB} MB</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # ── ACTIONS ──
    st.markdown('<div class="section-header">⚡ Actions</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🗂️ Clear Files", use_container_width=True):
            st.session_state.uploaded_files   = []
            st.session_state.active_file_idx  = 0
            st.rerun()

    if st.session_state.messages:
        report_text = generate_report()
        st.download_button(
            label="📄 Download Report",
            data=report_text,
            file_name=f"PlanChat_Report_{datetime.now().strftime('%Y-%m-%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown(
        '<div class="status-bar">☁️ Ollama Cloud · Files processed in browser memory only</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([3, 2], gap="medium")


# ── LEFT: DRAWING VIEWER ──────────────────────────────────────────────────────
with left_col:
    st.markdown("#### 📐 Drawing Viewer")

    files = st.session_state.uploaded_files
    if not files:
        st.markdown("""
        <div style="background:#1f2937;border:2px dashed #374151;border-radius:12px;
                    padding:60px 20px;text-align:center;color:#6b7280;">
          <div style="font-size:48px;margin-bottom:12px;">📂</div>
          <div style="font-size:16px;font-weight:600;color:#9ca3af;margin-bottom:8px;">
            No files loaded
          </div>
          <div style="font-size:13px;">Upload PDFs or images in the sidebar to begin.</div>
          <div style="margin-top:16px;font-size:11px;font-family:monospace;
                      display:flex;gap:8px;justify-content:center;color:#4b5563;">
            <span style="background:#111827;padding:3px 8px;border-radius:4px;">PDF</span>
            <span style="background:#111827;padding:3px 8px;border-radius:4px;">PNG</span>
            <span style="background:#111827;padding:3px 8px;border-radius:4px;">JPG</span>
            <span style="background:#111827;padding:3px 8px;border-radius:4px;">TIF</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        idx    = min(st.session_state.active_file_idx, len(files) - 1)
        active = files[idx]

        # File badge
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
          <span style="font-size:13px;font-weight:600;color:#93c5fd;">
            {'📄' if active['type'] == 'pdf' else '🖼️'} {active['name']}
          </span>
          <span style="background:#1e3a5f;color:#93c5fd;border:1px solid #2563eb55;
                       padding:1px 8px;border-radius:99px;font-size:10px;font-weight:700;">
            {active['page_count']} page{'s' if active['page_count'] != 1 else ''}
          </span>
        </div>
        """, unsafe_allow_html=True)

        # Page slider for multi-page PDFs
        if active["page_count"] > 1:
            page_num = st.slider(
                "Page",
                min_value=1,
                max_value=active["page_count"],
                value=1,
                key=f"page_slider_{idx}"
            ) - 1
        else:
            page_num = 0

        st.image(
            active["pages"][page_num],
            use_container_width=True,
            caption=f"Page {page_num + 1} of {active['page_count']}"
        )


# ── RIGHT: CHAT ───────────────────────────────────────────────────────────────
with right_col:
    st.markdown("#### 💬 Ask PlanChat")

    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center;padding:40px 0;color:#4b5563;">
              <div style="font-size:32px;margin-bottom:8px;">🤖</div>
              <div style="font-size:13px;color:#6b7280;">Upload plans, then ask anything.</div>
              <div style="font-size:11px;margin-top:6px;color:#374151;">
                Dimensions · Materials · Code compliance · Conflicts
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="user-bubble">{msg["text"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    rendered = render_with_citations(msg["text"])
                    st.markdown(
                        f'<div class="model-bubble">{rendered}</div>',
                        unsafe_allow_html=True
                    )

    # Input row
    has_files  = len(st.session_state.uploaded_files) > 0
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input(
            "Message",
            placeholder="Ask about the drawings…" if has_files else "Upload plans first",
            disabled=not has_files,
            label_visibility="collapsed",
            key="chat_input"
        )
    with btn_col:
        send = st.button(
            "Send",
            disabled=not has_files or not (user_input or "").strip(),
            use_container_width=True
        )

    st.markdown(
        f'<div class="status-bar">☁️ {OLLAMA_MODEL} · Ollama Cloud</div>',
        unsafe_allow_html=True
    )

    # ── SEND & STREAM ──────────────────────────────────────────────────────────
    if send and user_input and user_input.strip():
        user_text = user_input.strip()

        st.session_state.messages.append({
            "role":      "user",
            "text":      user_text,
            "timestamp": datetime.now().timestamp()
        })

        ollama_messages = build_ollama_messages(user_text)
        full_response   = ""

        with chat_container:
            st.markdown(
                f'<div class="user-bubble">{user_text}</div>',
                unsafe_allow_html=True
            )
            response_placeholder = st.empty()

        with st.spinner("Thinking…"):
            for chunk in stream_ollama_response(ollama_messages):
                full_response += chunk
                rendered = render_with_citations(full_response)
                response_placeholder.markdown(
                    f'<div class="model-bubble">{rendered}'
                    f'<span style="opacity:0.4;"> ▌</span></div>',
                    unsafe_allow_html=True
                )

        # Final render — no cursor
        rendered_final = render_with_citations(full_response)
        response_placeholder.markdown(
            f'<div class="model-bubble">{rendered_final}</div>',
            unsafe_allow_html=True
        )

        st.session_state.messages.append({
            "role":      "model",
            "text":      full_response,
            "timestamp": datetime.now().timestamp()
        })

        st.rerun()
