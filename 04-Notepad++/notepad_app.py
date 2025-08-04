import streamlit as st
from notepad_automation import NotepadPPAutomation

try:
    import docx  # type: ignore
except Exception:  # pragma: no cover - library might not be installed in tests
    docx = None


def _read_uploaded_text(file):
    """Return text content of uploaded file."""
    file.seek(0)
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    if docx is None:
        st.error("docx desteği bulunamadı")
        st.stop()
    document = docx.Document(file)
    return "\n".join(p.text for p in document.paragraphs)


st.title("📝 Notepad++ RPA")

uploaded_file = st.file_uploader(
    "Bir .txt veya .docx dosyası yükleyin", type=["txt", "docx"]
)

col1, col2 = st.columns(2)
with col1:
    start_hotkey = st.button("🚀 RPA Başlat", key="start_rpa_kb")
with col2:
    start_mouse = st.button("🖱️ RPA Başlat - 2", key="start_rpa_mouse")

st.markdown(
    """
    <style>
    div[id="start_rpa_kb"] button {
        background-color: #4CAF50;
        color: white;
    }
    div[id="start_rpa_mouse"] button {
        background-color: #FF5722;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if start_hotkey or start_mouse:
    if not uploaded_file:
        st.error("Lütfen önce bir dosya yükleyin.")
    else:
        text = _read_uploaded_text(uploaded_file)
        bot = NotepadPPAutomation()
        bot.launch()
        if start_hotkey:
            bot.new_file()
        else:
            bot.new_file_mouse()
        bot.write_text(text)
        save_path = r"D:\\Mira\\Mira.py"
        if start_hotkey:
            bot.save_file(save_path)
            bot.close()
        else:
            bot.save_file_mouse(save_path)
            bot.close_mouse()
        st.success(f"Metin Notepad++ ile kaydedildi: {save_path}")
