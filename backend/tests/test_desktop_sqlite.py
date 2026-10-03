from app.config import default_database_url,desktop_data_dir
def test_desktop_database_is_sqlite(monkeypatch,tmp_path):
    monkeypatch.setenv("MAKETECH_DATA_DIR",str(tmp_path))
    assert default_database_url().startswith("sqlite:///")
    assert default_database_url().endswith("extractor.db")
