import random
from maya import cmds
from PySide6.QtWidgets import (
                                QDoubleSpinBox,
                                QHBoxLayout,
                                QLabel,
                                QSpinBox,
                                QWidget,
                                QPushButton,
                                QVBoxLayout,
                                QGridLayout
                                )                               


class RandomGenerator(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atelier 4-5")
        self.setMinimumWidth(400)
        self.build_ui()
    
    def build_ui(self):
        self.layout_interface = QVBoxLayout(self)
        
        
#---------------- number of objects ------------------------------------------------------------------

        self.number_objects = QHBoxLayout()
        self.number_objects.addWidget(QLabel("Number of objects :"))
        

        # Convenience function to set the minimum, and maximum values with a single function call.
        # QSpinBox use only INT values for the number of onject created. 
        # Every time the value changes QSpinBox emits valueChanged() and textChanged() signals, the former providing a int and the latter a QString. 
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 10000)
        self.number_objects.addWidget(self.spinbox)


        # adding Grid layout to the interface layout
        self.layout_interface.addLayout(self.number_objects)
        self.layout_interface.setSpacing(20)


#---------------- Grid MIN / MAX ------------------------------------------------------------------
       
        self.grid = QGridLayout()

        # Ajout du MIN/MAX dans la position 0 de la grid
        self.grid.addWidget(QLabel("Min"),0,1)
        self.grid.addWidget(QLabel("Max"),0,2)

        # Ajout des position (X,Y,Z) dans la grid
        self.grid.addWidget(QLabel("Position X"), 1, 0)
        self.grid.addWidget(QLabel("Position Y"), 2, 0)
        self.grid.addWidget(QLabel("Position Z"), 3, 0)

        # (X,Y,Z) values = spinbox position fonction.
        self.min_pos_x = self.position(-10)
        self.max_pos_x = self.position(10)
        self.min_pos_y = self.position(-10)
        self.max_pos_y = self.position(10)
        self.min_pos_z = self.position(-10)
        self.max_pos_z = self.position(10)

        # Positionning de (X,Y,Z) spinbox in the grid
        self.grid.addWidget(self.min_pos_x, 1, 1)
        self.grid.addWidget(self.max_pos_x, 1, 2)
        self.grid.addWidget(self.min_pos_y, 2, 1)
        self.grid.addWidget(self.max_pos_y, 2, 2)
        self.grid.addWidget(self.min_pos_z, 3, 1)
        self.grid.addWidget(self.max_pos_z, 3, 2)
        
        # Ajout du scale (Float value), QDoubleSpinBox pour accepter les doubles.
        self.grid.addWidget(QLabel("Scale"), 4, 0)

        # Scale value = DoubleSpinBox fonction
        self.min_scale = self.scale(0.5)
        self.max_scale = self.scale(2.0)

        # Positionning scale doubleSpinbox in the grid
        self.grid.addWidget(self.min_scale, 4, 1)
        self.grid.addWidget(self.max_scale, 4, 2)


        # adding Grid layout to the interface layout
        self.layout_interface.setSpacing(15)
        self.layout_interface.addLayout(self.grid)


#---------------- Button create ---------------------------------------

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_objects)
        self.layout_interface.addWidget(self.create_button)

  
#------------------------------- FONCTIONS -------------------------------
    def scale(self, value = 0.0):
        scale = QDoubleSpinBox()
        scale.setRange(0.01, 10000)
        scale.setValue(value)
        scale.setDecimals(2)
        return scale

    def position(self, value = 0):
        position = QSpinBox()
        position.setRange(-10000, 10000)
        position.setValue(value)
        return position
   
   
    def random_object(self):
        forme = random.choice(["cube", "cylindre", "sphere"])


        if forme == "cube":
            objet = cmds.polyCube()[0]
        elif forme == "cylindre":
            objet = cmds.polyCylinder()[0]  
        else:
            objet = cmds.polySphere()[0]


        # Position est une valeur aleatoire pour chaque axe
        x = random.uniform(self.min_pos_x.value(), self.max_pos_x.value())
        y = random.uniform(self.min_pos_y.value(), self.max_pos_y.value())
        z = random.uniform(self.min_pos_z.value(), self.max_pos_z.value())
        cmds.move(x, y, z, objet)

        # Scale uniforme
        scale = random.uniform(self.min_scale.value(), self.max_scale.value())
        cmds.scale(scale,scale,scale,objet)

       

    def create_objects(self):
        cmds.undoInfo(openChunk=True)
        try:
            for int in range(self.spinbox.value()):
                self.random_object()
        finally:
            cmds.undoInfo(closeChunk=True)


def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = RandomGenerator()
    tool_window.show()

main()