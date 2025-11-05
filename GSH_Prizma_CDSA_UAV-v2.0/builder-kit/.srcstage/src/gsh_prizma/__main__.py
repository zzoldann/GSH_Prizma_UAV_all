# -*- coding: utf-8 -*-
import sys

try:
    from gsh_prizma import __version__ as _VER
except Exception:
    _VER = "dev"

def _gui():
    try:
        from gsh_prizma.ui.app import main  # абсолютный импорт
        return main()
    except Exception as e:
        # Фоллбек: маленькое окно + автозакрытие, чтобы smoke не падал
        from PySide6 import QtWidgets, QtCore
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        w = QtWidgets.QWidget()
        w.setWindowTitle(f"GSH Prizma v{_VER} — Fallback GUI ({e.__class__.__name__})")
        w.resize(420, 160)
        w.show()
        QtCore.QTimer.singleShot(1000, app.quit)
        return app.exec()

def _smoke():
    from PySide6 import QtWidgets, QtCore
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    w = QtWidgets.QWidget()
    w.setWindowTitle(f"GSH Prizma v{_VER} — SMOKE")
    w.resize(360, 120)
    w.show()
    QtCore.QTimer.singleShot(800, app.quit)
    return app.exec()

if __name__ == "__main__":
    if "--version" in sys.argv:
        print(_VER); raise SystemExit(0)
    if "--smoke" in sys.argv:
        raise SystemExit(_smoke())
    raise SystemExit(_gui())
