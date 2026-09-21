# 01 : Ouvrir un fichier json dans python | JSON file_path and fonction load
import sys
import json
from Pyside6.QtWidgets import 

json_file = sys.argv[1]
print("Path >>>>>>>>> " + json_file + " <<<<<<<<<<<")

try:
    file = open(json_file)
    data = json.load(file)
    print(type(data))

except: 
    print(f"Could not load from {json_file}")


for i in data:
    for k in i.keys():
        print(k)


QApplication([])
QMainWindow()
window.show();
sys.exit(app.exec())