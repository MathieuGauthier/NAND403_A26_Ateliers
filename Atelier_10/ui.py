import animator
from maya import cmds
from maya import OpenMayaUI as omui  
from shiboken6 import wrapInstance
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QSlider,QSpinBox,QLabel,QPushButton,QMessageBox)


def get_maya_main_window():
    """Retourne la fenêtre principale de Maya (on s'en sert comme parent)."""
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer), QWidget)


class UiAnimator(QWidget):

    def __init__(self):
        # Parent = Maya + flag Tool : la fenêtre reste toujours devant Maya
        super().__init__(get_maya_main_window())
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(300)

        # L'objet mémorisé au clic (None = pas encore choisi)
        self.source = None

        self.build_ui()

    # ---------------- Construction de l'interface ----------------
    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # Deux sliders : chaque ligne = un slider + un label de valeur
        self.count_slider, count_row = self.create_slider_row(1, 100, 10)
        form.addRow("Copies", count_row)

        self.radius_slider, radius_row = self.create_slider_row(1, 50, 10)
        form.addRow("Radius", radius_row)

        # Le seed redevient un QSpinBox
        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(0, 9999)
        form.addRow("Seed", self.seed_spin)

        # LIVE EDIT : chaque changement de valeur refait le scatter
        self.count_slider.valueChanged.connect(self.refresh)
        self.radius_slider.valueChanged.connect(self.refresh)
        self.seed_spin.valueChanged.connect(self.refresh)

        scatter_button = QPushButton("Scatter")
        scatter_button.clicked.connect(self.on_scatter_clicked)
        layout.addWidget(scatter_button)

    # ---------------- Fonction d'optimisation ----------------
    # Les 2 sliders sont construits pareil : une seule fonction les crée.
    def create_slider_row(self, minimum, maximum, value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)

        # Le label affiche la valeur actuelle du slider
        value_label = QLabel(str(value))
        value_label.setMinimumWidth(35)

        # Quand le slider bouge, on met à jour le texte du label
        slider.valueChanged.connect(lambda new_value: value_label.setText(str(new_value))) # str est la fonction qui convertit une valeur en texte.

        row = QHBoxLayout()
        row.addWidget(slider)
        row.addWidget(value_label)
        return slider, row

    # ---------------- Fonctions des widgets ----------------
    def on_scatter_clicked(self):
        """Au clic : on mémorise l'objet sélectionné, puis on scatter."""
        source = animator.get_selected_object()
        if source is None:
            QMessageBox.warning(self, "Scatter", "Select an object first.")
            return
        self.source = source
        self.refresh()

    def refresh(self):
        """Refait le scatter avec les valeurs actuelles de l'interface."""
        # Pas d'objet mémorisé, ou objet supprimé : on ne fait rien
        if self.source is None or not cmds.objExists(self.source):
            return

        animator.scatter(
            source=self.source,
            count=self.count_slider.value(),
            radius=self.radius_slider.value(),
            seed=self.seed_spin.value()
        )