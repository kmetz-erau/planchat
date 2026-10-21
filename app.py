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
OLLAMA_MODEL = "qwen3-vl:235b-cloud"
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
