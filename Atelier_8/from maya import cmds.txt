from maya import cmds
from PySide6.QtWidgets import (QGroupBox,QLabel,QSpinBox,QWidget,
                                QPushButton,QVBoxLayout,QGridLayout,QDoubleSpinBox)

class UiAnimator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Animation")
        self.setMinimumWidth(400)
        self.build_ui()

    
# ------------------------------------------- Fonction qui va construire l'interface -----------------------------------------   
    def build_ui(self):
        
        self.interface = QVBoxLayout(self)
        self.interface.setSpacing(10)


    # -------------------------------------- Section du timing ----------------------------------------------

        # 1: Le groupe (Le contenant)
        groupe_temps = QGroupBox("Animation Timing")
        layout_temps = QGridLayout(groupe_temps)

        # 2 : La ligne pour la duree en frame + un spinbox pour choisir la valeur(intialise a 48)
        label_duration = QLabel("Duration (Frames) : ")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10000)
        self.spin_duration.setValue(100) # Valeur initial de duration

        # 2.1 : A quelle frequence on ajoute une cle sur la ligne de temps
        label_step = QLabel("Steps (Frames) : ")
        self.spin_step = QSpinBox()
        self.spin_step.setRange(1, 10000)
        self.spin_step.setValue(10) # Valeur initial de step

        # 3 : On place le tout dans une Grille
        layout_temps.addWidget(label_duration, 0, 0)
        layout_temps.addWidget(self.spin_duration, 0, 1)
        layout_temps.addWidget(label_step, 0, 2)
        layout_temps.addWidget(self.spin_step, 0, 3)

        # ------------------------------------------ Section du bouton ------------------------------------------------

        generate_button = QPushButton("Generate animation")
        generate_button.clicked.connect(self.generate) # ici, le bouton va detenir la fonction qui detient le code de l'outil.

        # ------------------------------------------- Le layout de l'interface -----------------------------------------
        # Fin : On ajoute ensuite a l'interface
        self.interface.addWidget(groupe_temps)
        self.interface.addWidget(generate_button)


    def generate(self):
        selection = cmds.ls(selection=True, transforms=True)
        if not selection:
            cmds.warning("Please select at least one object to animate.")
            return

        duration = self.spin_duration.value()
        step = self.spin_step.value()

        # Configurer la durée de l'animation
        cmds.playbackOptions(min=0, max=duration)
        
        
        cmds.undoInfo(openChunk=True)
        try:

            for obj in selection:
                # Tout effacer sur l'objet avant de recréer l'animation
                cmds.cutKey(obj, clear=True)

                for frame in range(0, duration + 1, step):
                    cmds.setKeyframe(obj, attribute="translateX",value=frame, time=frame)
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = UiAnimator()
    tool_window.show()

main()