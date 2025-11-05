
import math
from PySide6 import QtWidgets, QtCore
from .i18n import STR
from ..core.link_budget import sensitivity_dBm, Lmax_dB, invert_distance
from ..core.link_models import hata_L_urban, hata_L_suburban, hata_L_open, cost231_L, d_horizon_km

# Prefer modern backend; fallback to qt5agg if needed
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # Matplotlib 3.6+
    from matplotlib.figure import Figure
    HAVE_MPL = True
except Exception:
    try:
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        HAVE_MPL = True
    except Exception:
        HAVE_MPL = False

class LinkBudgetTab(QtWidgets.QWidget):
    def __init__(self, parent=None, lang="ru"):
        super().__init__(parent)
        self.lang = lang
        S = STR[lang]

        self.p_tx = QtWidgets.QDoubleSpinBox(); self.p_tx.setRange(-200, 50); self.p_tx.setValue(14)
        self.g_tx = QtWidgets.QDoubleSpinBox(); self.g_tx.setRange(-10, 30); self.g_tx.setValue(2.15)
        self.g_rx = QtWidgets.QDoubleSpinBox(); self.g_rx.setRange(-10, 30); self.g_rx.setValue(2.15)
        self.l_sys = QtWidgets.QDoubleSpinBox(); self.l_sys.setRange(0, 40); self.l_sys.setValue(2)

        self.nf = QtWidgets.QDoubleSpinBox(); self.nf.setRange(0, 20); self.nf.setValue(3)
        self.bw = QtWidgets.QDoubleSpinBox(); self.bw.setDecimals(3); self.bw.setRange(0.001, 1000.000); self.bw.setValue(0.125)
        self.snr = QtWidgets.QDoubleSpinBox(); self.snr.setRange(-30, 30); self.snr.setValue(7.5)
        self.margin = QtWidgets.QDoubleSpinBox(); self.margin.setRange(0, 20); self.margin.setValue(0.0)
        self.lbf = QtWidgets.QDoubleSpinBox(); self.lbf.setRange(0, 40); self.lbf.setValue(12.0)

        self.f = QtWidgets.QDoubleSpinBox(); self.f.setRange(30, 6000); self.f.setValue(868.0)
        self.hb = QtWidgets.QDoubleSpinBox(); self.hb.setRange(0.1, 12000.0); self.hb.setValue(5.0)
        self.hm = QtWidgets.QDoubleSpinBox(); self.hm.setRange(0.1, 12000.0); self.hm.setValue(2.0)

        self.env = QtWidgets.QComboBox(); self.env.addItems(["Городская", "Пригород", "Село/Дер", "Равнинная", "Море/Река"])
        self.model = QtWidgets.QComboBox(); self.model.addItems(["Hata", "COST-231"])
        self.bigcity = QtWidgets.QCheckBox(S["lbl_bigcity"])
        self.metro = QtWidgets.QCheckBox(S["lbl_metro"])

        self.chk_logx = QtWidgets.QCheckBox(S["chk_logx"]); self.chk_logx.setChecked(True)
        self.xlim = QtWidgets.QSpinBox(); self.xlim.setRange(10, 3000); self.xlim.setValue(1000)

        # Results
        self.lbl_lmax = QtWidgets.QLabel("?")
        self.lbl_dlink = QtWidgets.QLabel("?")
        self.lbl_dhor = QtWidgets.QLabel("?")
        self.lbl_dtheor = QtWidgets.QLabel("?")

        form = QtWidgets.QFormLayout()
        form.addRow(S["lbl_p_tx"], self.p_tx)
        form.addRow(S["lbl_g_tx"], self.g_tx)
        form.addRow(S["lbl_g_rx"], self.g_rx)
        form.addRow(S["lbl_l_sys"], self.l_sys)
        form.addRow(S["lbl_nf"], self.nf)
        form.addRow(S["lbl_bw"], self.bw)
        form.addRow(S["lbl_snr"], self.snr)
        form.addRow(S["lbl_margin"], self.margin)
        form.addRow(S["lbl_lbf"], self.lbf)
        form.addRow(S["lbl_f"], self.f)
        form.addRow(S["lbl_hb"], self.hb)
        form.addRow(S["lbl_hm"], self.hm)
        form.addRow(S["lbl_env"], self.env)
        form.addRow(S["lbl_model"], self.model)
        form.addRow("", self.bigcity)
        form.addRow("", self.metro)
        form.addRow(self.chk_logx, QtWidgets.QLabel(S["lbl_xlim"]))
        form.addRow("", self.xlim)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addLayout(form)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel(S["res_lmax"]), 0, 0)
        grid.addWidget(self.lbl_lmax, 0, 1)
        grid.addWidget(QtWidgets.QLabel(S["res_dlink"]), 1, 0)
        grid.addWidget(self.lbl_dlink, 1, 1)
        grid.addWidget(QtWidgets.QLabel(S["res_dhor"]), 2, 0)
        grid.addWidget(self.lbl_dhor, 2, 1)
        grid.addWidget(QtWidgets.QLabel(S["res_dtheor"]), 3, 0)
        grid.addWidget(self.lbl_dtheor, 3, 1)
        vbox.addLayout(grid)

        if HAVE_MPL:
            self.fig = Figure()
            self.canvas = FigureCanvas(self.fig)
            vbox.addWidget(self.canvas)
        else:
            vbox.addWidget(QtWidgets.QLabel("Установите matplotlib для графиков."))

        # wiring
        for w in [self.p_tx,self.g_tx,self.g_rx,self.l_sys,self.nf,self.bw,self.snr,self.margin,self.lbf,self.f,self.hb,self.hm,self.env,self.model,self.bigcity,self.metro,self.chk_logx,self.xlim]:
            if isinstance(w, (QtWidgets.QComboBox, QtWidgets.QCheckBox)):
                if isinstance(w, QtWidgets.QComboBox):
                    w.currentIndexChanged.connect(self.recalc)
                else:
                    w.stateChanged.connect(self.recalc)
            else:
                w.valueChanged.connect(self.recalc)

        QtCore.QTimer.singleShot(0, self.recalc)

    def model_fn(self):
        model = self.model.currentText()
        env = self.env.currentText()
        f = float(self.f.value())
        hb = float(self.hb.value())
        hm = float(self.hm.value())
        big = self.bigcity.isChecked()
        metro = self.metro.isChecked()

        if model == "Hata":
            if env == "Городская":
                return lambda d_km: hata_L_urban(f, hb, hm, d_km, big_city=big)
            elif env == "Пригород":
                return lambda d_km: hata_L_suburban(f, hb, hm, d_km, big_city=big)
            else:
                return lambda d_km: hata_L_open(f, hb, hm, d_km, big_city=big)
        else:
            if env == "Городская":
                return lambda d_km: cost231_L(f, hb, hm, d_km, big_city=big, metropolis=metro)
            elif env == "Пригород":
                return lambda d_km: cost231_L(f, hb, hm, d_km, big_city=big, metropolis=metro) - (2.0*(math.log10(max(f/28.0,1e-12)))**2 + 5.4)
            else:
                lf = math.log10(max(f,1e-9))
                return lambda d_km: cost231_L(f, hb, hm, d_km, big_city=big, metropolis=metro) - (4.78*(lf**2) - 18.33*lf + 40.94)

    def recalc(self):
        B_Hz = float(self.bw.value()) * 1e6
        Smin = sensitivity_dBm(B_Hz, float(self.nf.value()), float(self.snr.value()), float(self.margin.value()))
        Lmax = Lmax_dB(float(self.p_tx.value()), float(self.g_tx.value()), float(self.g_rx.value()),
                       float(self.l_sys.value()), Smin, float(self.lbf.value()))
        fn = self.model_fn()
        try:
            dlink = invert_distance(Lmax, lambda d_km, fn=fn: fn(d_km), d_bounds_km=(0.01, float(self.xlim.value())))
        except Exception:
            dlink = float("nan")
        dhor = d_horizon_km(float(self.hb.value()), float(self.hm.value()))
        dtheor = min(dlink, dhor) if not math.isnan(dlink) else dhor

        self.lbl_lmax.setText(f"{Lmax:.2f}")
        self.lbl_dlink.setText(f"{dlink:.3f}")
        self.lbl_dhor.setText(f"{dhor:.3f}")
        self.lbl_dtheor.setText(f"{dtheor:.3f}")

        if HAVE_MPL:
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            xs = []
            ys = []
            xmax = float(self.xlim.value())
            n = 400
            for i in range(n):
                if self.chk_logx.isChecked():
                    d = 10**(math.log10(0.01) + (math.log10(xmax)-math.log10(0.01))*i/(n-1))
                else:
                    d = 0.01 + (xmax-0.01)*i/(n-1)
                xs.append(d)
                ys.append(fn(d))
            ax.plot(xs, ys)
            ax.set_xlabel("Расстояние, км" + (" (лог)" if self.chk_logx.isChecked() else ""))
            ax.set_ylabel("Потери L(d), дБ")
            ax.set_xscale("log" if self.chk_logx.isChecked() else "linear")
            ax.axhline(Lmax, linestyle="--")
            ax.set_title("Модель потерь")
            self.fig.tight_layout()
            self.canvas.draw_idle()
