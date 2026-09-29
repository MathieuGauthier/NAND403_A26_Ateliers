from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTextEdit,
                               QPushButton,QMessageBox, QDialog)
class MessageBoard(QWidget): #La class irrite de la class QWidget.
    def __init__(self): # Constructeur
        super().__init__() # Constructeur QWidget
        self.setWindowTitle("Message board")
        self.create_ui()

    def create_ui(self):
        print("create UI")
        layout = QVBoxLayout(self)
        label = QLabel("Message Board")
        layout.addWidget(label)
       
        # Text edit
        self.tapped_text = QTextEdit()
        self.tapped_text.setPlaceholderText("Écrire ici :")
        layout.addWidget(self.tapped_text)      
        
        # Qpushbutton
        button = QPushButton("Print text")
        button.clicked.connect(self.message_box)
        layout.addWidget(button)

    # Qmessage box fonction
    def message_box(self):
        message = QDialog(self)
        message.setWindowTitle("Message")
        

        layout = QVBoxLayout(message)

        label = QLabel(self.tapped_text.toPlainText())
        layout.addWidget(label)

        button = QPushButton("Fermer")
        button.clicked.connect(message.close)
        layout.addWidget(button)

        message.exec()

      

def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()