import pytest
from PyQt5.QtWidgets import QApplication

# Keep global reference to avoid being garbage collected
_qapp_instance = None


@pytest.fixture(scope="session", autouse=True)
def qtapp():
    app = QApplication.instance()
    if app is None:
        global _qapp_instance
        _qapp_instance = QApplication([])
        return _qapp_instance
    else:
        return app
