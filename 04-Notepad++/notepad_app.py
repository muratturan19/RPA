import streamlit as st
from pathlib import Path
from notepad_automation import NotepadPPAutomation

try:
    import docx  # type: ignore
except Exception:  # pragma: no cover - library might not be installed in tests
    docx = None

st.title("📝 Notepad++ RPA")

uploaded_file = st.file_uploader(
    "Bir .txt veya .docx dosyası yükleyin", type=["txt", "docx"]
)

if st.button("RPA'yı Başlat"):
    if not uploaded_file:
        st.error("Lütfen önce bir dosya yükleyin.")
    else:
        if uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
        else:
            if docx is None:
                st.error("docx desteği bulunamadı")
                st.stop()
            document = docx.Document(uploaded_file)
            text = "\n".join(p.text for p in document.paragraphs)

        bot = NotepadPPAutomation()
        bot.launch()
        bot.new_file()
        bot.write_text(text)
        save_path = r"D:\\Mira\\Mira.py"
        bot.save_file(save_path)
        bot.close()
        st.success(f"Metin Notepad++ ile kaydedildi: {save_path}")
