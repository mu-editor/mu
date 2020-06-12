import pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qtapp():
    app = QApplication.instance()
    if app is None:
        global _qapp_instance
        _qapp_instance = QApplication([])
        return _qapp_instance
    else:
        return app
