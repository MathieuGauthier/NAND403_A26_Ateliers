import random
from maya import cmds
from PySide6.QtWidgets import (
                                QGroupBox,
                                QHBoxLayout,
                                QLabel,
                                QSpinBox,
                                QWidget,
                                QPushButton,
                                QVBoxLayout,
                                QGridLayout,
                                QDoubleSpinBox
                                )


class FenceGenerator(QWidget):

    def __init__(self):
            super().__init__()
            self.setWindowTitle("Atelier 6")
            self.setMinimumWidth(400)
            self.build_ui()


    def build_ui(self):

        self.interface = QVBoxLayout(self)
        self.interface.setSpacing(10)


#------------------------------ Poteau Vertical -----------------------------------------
# A group box allows you to group related widgets together in a frame with a title on top

        self.group_v = QGroupBox("Poteau Vertical")
        self.layout_v = QVBoxLayout()
        self.group_v.setLayout(self.layout_v)

    # Scale (Dimension du poteau Vertical) -----------------------------------------------------
        self.scale_v = QGridLayout()

    # Spinbox size et aussi les valeurs du polycube. Utiliser dans la fonction Generer.
        self.spinbox_v_x = QDoubleSpinBox()
        self.spinbox_v_y = QDoubleSpinBox()


        for spinbox in (self.spinbox_v_x, self.spinbox_v_y):
            spinbox.setFixedSize(126, 25)   # largeur, hauteur

    # Titre
        self.scale_v.addWidget(QLabel("Largeur ( X )"),0,1)
        self.scale_v.addWidget(QLabel("Hauteur ( Y )"),0,2)

    # Spinbox
        self.scale_v.addWidget(QLabel("Dimension : "),1,0)
        self.scale_v.addWidget(self.spinbox_v_x,1,1)
        self.scale_v.addWidget(self.spinbox_v_y,1,2)

    # Ajouter au groupbox
        self.layout_v.addLayout(self.scale_v)


    # Distance entre poteau -------------------------------------------------------
        self.distance = QHBoxLayout()

        self.spinbox_distance = QDoubleSpinBox()
        self.spinbox_distance.setFixedSize(260,25) # Largeur,Hauteur

        self.distance.addWidget(QLabel("Distance : "))
        self.distance.addWidget(self.spinbox_distance)

    # Ajouter au groupbox
        self.layout_v.addLayout(self.distance)

    # Ajouter le groupbox a interface
        self.interface.addWidget(self.group_v)


#------------------------------ Poteau Horizontal  -----------------------------------------

        self.group_h = QGroupBox("Poteau Horizontal")
        self.layout_h = QVBoxLayout()
        self.group_h.setLayout(self.layout_h)

    # Scale (dimension du poteau en Horizontal) -------------------------------------
        self.scale_h = QGridLayout()

    # Spinbox size et aussi les valeurs du polycube. Utiliser dans la fonction Generer.
        self.spinbox_h_x = QDoubleSpinBox()
        self.spinbox_h_y = QDoubleSpinBox()

        for spinbox in (self.spinbox_h_x, self.spinbox_h_y):
            spinbox.setFixedSize(126, 25)   # largeur, hauteur

    # Titre
        self.scale_h.addWidget(QLabel("Largeur ( X )"),0,1)
        self.scale_h.addWidget(QLabel("Hauteur ( Y )"),0,2)


    # Spinbox
        self.scale_h.addWidget(QLabel("Dimension : "),1,0)
        self.scale_h.addWidget(self.spinbox_h_x,1,1)
        self.scale_h.addWidget(self.spinbox_h_y,1,2)


    # Ajouter au groupbox
        self.layout_h.addLayout(self.scale_h)

    # Nombre de poteau entre les poteaux verticales. Utiliser dans la Fonction generer.
        self.poteaux_h = QHBoxLayout() # ph

        self.spinbox_ph = QSpinBox()
        self.spinbox_ph.setFixedSize(260,25) # Largeur,Hauteur

        self.poteaux_h.addWidget(QLabel("Quantitée : "))
        self.poteaux_h.addWidget(self.spinbox_ph)

    # Ajouter au groupbox
        self.layout_h.addLayout(self.poteaux_h)

    # Ajouter le groupbox a interface
        self.interface.addWidget(self.group_h)


#------------------------------ Nombre de repetition --------------------------------------
        self.group_rep = QGroupBox("Nombre de clotures")
        layout_rep = QHBoxLayout()
        self.group_rep.setLayout(layout_rep)

        self.spinbox_rep = QSpinBox()
        layout_rep.addWidget(QLabel("Quantitée : "))
        self.spinbox_rep.setFixedSize(260,25) # Largeur,Hauteur
        layout_rep.addWidget(self.spinbox_rep)

        self.interface.addWidget(self.group_rep)

#------------------------------- Boutton Générer -----------------------------------------
        
        self.create_button = QPushButton("Générer")
        self.create_button.clicked.connect(self.generer)
        self.interface.addWidget(self.create_button)


    def generer(self):
        # Je dois egaliser (x = t) les valeurs x,y avec les valeurs dans le spinbox pour creer les objets.

        # Poteau Vertical (VALEURS)
        valeur_v_x = self.spinbox_v_x.value()
        valeur_v_y = self.spinbox_v_y.value()
        distance = self.spinbox_distance.value()

        # Poteau Horizontal (VALEURS)
        valeur_h_x = self.spinbox_h_x.value()
        valeur_h_y = self.spinbox_h_y.value()
        nb_poteau_h = self.spinbox_ph.value()


        # Nombre de cloture qui doit etre generer (Nombre de fois quon va executer la boucle)
        nb_clotures = self.spinbox_rep.value()


        cmds.undoInfo(openChunk=True)
        try:

            # Espacement entre chaque poteau vertical
            espace = valeur_v_x + distance

            # Boucle  iteration pour generer la cloture un nombre de fois.
            for i in range(nb_clotures):

                pos_poteau_x = i*espace

                # Poteau Vertical ------------------------------------------------------------------------------------------------------------------------------------------
                # poteau = je set le Wight, height et depth avec les valeur du spinbox, je nomme le polyCude et lui attribute un chiffre depend du nombre de poteau generer.
                # Le [0] est un index qui point sur l'objet dans la scene qui va etre deplacé : poteau_v_1.

                poteau_v = cmds.polyCube(w=valeur_v_x, h=valeur_v_y, d=valeur_v_x, name=f"poteau_v_{i + 1}")[0]

                # la commande move bouge le pulyCube en x = 0, y = la moitier de sa hauteur pour le centrer au monde.
                # le poteau a la fin indique quoi deplacer dans maya.

                cmds.move(pos_poteau_x, valeur_v_y / 2, 0, poteau_v)
                # ------------------------------------------------------------------------------------------------------------------------------------------------------------

                
                
                # Boucle pour generer les poteaux horizontals entre chaque poteau vertical.--------------------------------------------------------

                # Milieu de l'espace entre ce poteau et le suivant
                centre_x = pos_poteau_x + valeur_v_x / 2 + distance / 2

                for j in range(nb_poteau_h):
                    ratio = (j + 1) / (nb_poteau_h + 1) # le ratio evite a un poteau d'etre au limite du poteau vertical

                    poteau_h = cmds.polyCube(w=distance, h=valeur_h_y, d=valeur_h_x, name=f"poteau_h_{i + 1}_{j + 1}")[0]
                    cmds.move(centre_x, valeur_v_y * ratio, 0, poteau_h)


        finally:
            cmds.undoInfo(closeChunk=True)
     







def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = FenceGenerator()
    tool_window.show()

main()