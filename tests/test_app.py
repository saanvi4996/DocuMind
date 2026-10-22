from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_app_starts_without_documents(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception
    assert at.title[0].value == "🧠 DocuMind"


def test_summarise_without_documents_warns():
    at = AppTest.from_file(APP, default_timeout=60).run()
    next(b for b in at.button if "Summarise" in b.label).click().run()
    assert not at.exception
    assert any("upload and process" in w.value.lower() for w in at.warning)
