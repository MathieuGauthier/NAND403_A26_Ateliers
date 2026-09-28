from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit,QPushButton,QMessageBox
 
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
       
        #Text edit
        tapped_text = QTextEdit()
        tapped_text.setPlaceholderText("Écrire ici :")
        layout.addWidget(tapped_text)
       
        #Qpushbutton
        button = QPushButton("Print text")
        layout.addWidget(button)

         #Qmessage box fonction
        def message_box(tapped_text):
            message = QMessageBox()
            

 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()