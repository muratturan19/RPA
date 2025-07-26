from __future__ import annotations

import pandas as pd
import streamlit as st
from pathlib import Path

from main import run_rpa_with_gui

st.set_page_config(page_title="Karmaşık RPA", layout="centered")
st.title("Karmaşık RPA Sistemi")

uploaded_files = st.file_uploader(
    "Excel dosyalarını sürükleyip bırakın",
    type=["xlsx"],
    accept_multiple_files=True,
)

start = st.button("Başla")
progress_bar = st.progress(0.0)
status = st.empty()

if "results" not in st.session_state:
    st.session_state["results"] = None

if start:
    if not uploaded_files:
        st.warning("Lütfen önce dosya seçin")
    else:
        paths: list[Path] = []
        save_dir = Path("uploaded")
        save_dir.mkdir(exist_ok=True)
        for uf in uploaded_files:
            file_path = save_dir / uf.name
            with open(file_path, "wb") as f:
                f.write(uf.getbuffer())
            paths.append(file_path)

        def progress_callback(value: float, message: str) -> None:
            progress_bar.progress(value)
            status.text(message)

        results = run_rpa_with_gui(paths, progress_callback)
        st.session_state["results"] = results
        status.text("Tüm dosyalar işlendi")
        progress_bar.progress(1.0)

if st.session_state.get("results"):
    st.header("Sonuçlar")
    df = pd.DataFrame(st.session_state["results"])
    st.table(df)

    if st.button("PDF Raporu Kaydet"):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        pdf_path = Path("rapor.pdf")
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        c.drawString(100, 800, "RPA Sonuç Raporu")
        y = 760
        for row in st.session_state["results"]:
            line = (
                f"Dosya: {row['file']}  Kayıt: {row['records']}  Başarılı: {row['success']}"
            )
            c.drawString(80, y, line)
            y -= 20
        c.save()
        st.success(f"PDF kaydedildi: {pdf_path}")
