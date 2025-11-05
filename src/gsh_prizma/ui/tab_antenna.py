from PySide6 import QtWidgets
from .i18n import STR
from ..core.antenna_firstorder import quarterwave_monopole, patch_rect, mini_yagi_3el, helix_compact
from ..solvers.export_nec import export_monopole_qw
from ..io.export_json import save_json

class AntennaWizardTab(QtWidgets.QWidget):
    def __init__(self, parent=None, lang="ru"):
        super().__init__(parent)
        S = STR[lang]

        self.topo = QtWidgets.QComboBox()
        self.topo.addItems(["Штырь 1/4λ", "Patch (прямоуг.)", "Мини-Яги (3 эл.)", "Спираль (компакт)"])

        self.f0 = QtWidgets.QDoubleSpinBox(); self.f0.setRange(30, 6000); self.f0.setValue(868.0); self.f0.setSuffix(" МГц")
        self.er = QtWidgets.QDoubleSpinBox(); self.er.setRange(1.0, 15.0); self.er.setValue(2.9)
        self.h = QtWidgets.QDoubleSpinBox(); self.h.setRange(0.1, 10.0); self.h.setValue(1.6); self.h.setSuffix(" мм")

        self.btn_calc = QtWidgets.QPushButton("Рассчитать")
        self.btn_export_nec = QtWidgets.QPushButton("Экспорт .nec")
        self.btn_export_json = QtWidgets.QPushButton("Экспорт .json")

        self.out = QtWidgets.QTextEdit(); self.out.setReadOnly(True)

        form = QtWidgets.QFormLayout()
        form.addRow("Топология", self.topo)
        form.addRow("f₀", self.f0)
        form.addRow("ε_r", self.er)
        form.addRow("h", self.h)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btn_calc)
        hbox.addWidget(self.btn_export_nec)
        hbox.addWidget(self.btn_export_json)

        v = QtWidgets.QVBoxLayout(self)
        v.addLayout(form)
        v.addLayout(hbox)
        v.addWidget(self.out)

        self.btn_calc.clicked.connect(self.calc)
        self.btn_export_nec.clicked.connect(self.export_nec)
        self.btn_export_json.clicked.connect(self.export_json)

    def calc(self):
        topo = self.topo.currentText()
        f_Hz = self.f0.value()*1e6
        if topo.startswith("Штырь"):
            res = quarterwave_monopole(f_Hz)
        elif topo.startswith("Patch"):
            res = patch_rect(f_Hz, self.er.value(), self.h.value()/1000.0)
        elif topo.startswith("Мини-Яги"):
            res = mini_yagi_3el(f_Hz)
        else:
            res = helix_compact(f_Hz)

        self.last_result = res
        self.out.setPlainText(str(res))

    def export_nec(self):
        if not hasattr(self, "last_result"):
            self.calc()
        topo = self.topo.currentText()
        f_Hz = self.f0.value()*1e6
        if topo.startswith("Штырь"):
            nec = export_monopole_qw(self.last_result, f_Hz)
            fn = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить .nec", "model.nec", "NEC (*.nec)")[0]
            if fn:
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(nec)
        else:
            QtWidgets.QMessageBox.information(self, "Экспорт .nec", "Экспорт в .nec реализован пока только для штыря.")

    def export_json(self):
        if not hasattr(self, "last_result"):
            self.calc()
        fn = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить .json", "model.json", "JSON (*.json)")[0]
        if fn:
            save_json(self.last_result, fn)
