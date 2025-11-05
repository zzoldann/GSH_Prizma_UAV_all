# -*- coding: utf-8 -*-
from PySide6 import QtWidgets, QtCore
import json, os, sys

def resource_path(*parts):
    """Возвращает путь к ресурсу и в исходниках, и в onefile (sys._MEIPASS)."""
    base = getattr(sys, "_MEIPASS", os.getcwd())
    p = os.path.join(base, *parts)
    if os.path.exists(p):
        return p
    # запасной вариант — из текущей директории проекта
    alt = os.path.join(os.getcwd(), *parts)
    return alt

HELP_FILE = resource_path("assets", "help", "help_ru.json")

def load_help():
    try:
        with open(HELP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    helpmap = load_help()

    w = QtWidgets.QWidget()
    w.setWindowTitle("GSH Prizma — GUI")
    layout = QtWidgets.QVBoxLayout(w)

    form = QtWidgets.QFormLayout()
    for key in ["model","env","f_mhz","bw_mhz","h_tx_m","h_rx_m","sigma_db"]:
        le = QtWidgets.QLineEdit()
        meta = helpmap.get(key, {})
        le.setPlaceholderText(meta.get("label", key))
        if "tooltip" in meta: le.setToolTip(meta["tooltip"])
        if "whats_this" in meta: le.setWhatsThis(meta["whats_this"])
        form.addRow(meta.get("label", key), le)
    layout.addLayout(form)

    btn = QtWidgets.QPushButton("Закрыть")
    btn.clicked.connect(w.close)
    layout.addWidget(btn, alignment=QtCore.Qt.AlignRight)

    w.resize(800, 500)
    w.show()
    return app.exec()
