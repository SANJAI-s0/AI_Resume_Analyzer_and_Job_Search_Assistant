import tempfile
from pathlib import Path
import pytest

from app import app
from database import db as database_module


@pytest.fixture
def client(monkeypatch):
    app.config["TESTING"] = True

    # Use temp directory instead of open file (Windows-safe)
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            database_module,
            "DB_PATH",
            Path(tmpdir) / "test.db"
        )

        database_module.init_db()

        with app.test_client() as client:
            yield client
