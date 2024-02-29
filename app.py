import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QTextEdit, QWidget, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices

class DeveloperInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Información del Desarrollador")
        self.setGeometry(100, 100, 300, 150)

        self.setWindowIcon(QIcon('src/info.png'))
        
        layout = QVBoxLayout()
        
        label = QLabel("Desarrollador: Nelson Rivero")
        layout.addWidget(label)
        
        instagram_button = QPushButton("Instagram: riveronelson1")
        instagram_button.clicked.connect(self.open_instagram)
        layout.addWidget(instagram_button)
        
        github_button = QPushButton("GitHub: Nelsonrivero")
        github_button.clicked.connect(self.open_github)
        layout.addWidget(github_button)
        
        self.setLayout(layout)

    def open_instagram(self):
        QDesktopServices.openUrl(QUrl("https://www.instagram.com/riveronelson1"))

    def open_github(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Nelsonrivero"))
        
class OrganizadorArchivosApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.historial_archivos = []

    def initUI(self):
        self.setWindowTitle("Organizador de Archivos")
        self.setGeometry(100, 100, 400, 300)
        
        app_icon = QIcon('src\icon2.ico')
        self.setWindowIcon(app_icon)

        self.layout = QVBoxLayout()

        self.label = QLabel("Seleccione la carpeta de origen:")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Seleccionar Carpeta")
        self.button.clicked.connect(self.organizar_archivos)
        self.layout.addWidget(self.button)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.historial_label = QLabel("Historial de archivos movidos:")
        self.layout.addWidget(self.historial_label)

        self.historial_text = QTextEdit()
        self.layout.addWidget(self.historial_text)

        container = QWidget()
        container.setLayout(self.layout)

        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_developer_info)
        self.layout.addWidget(self.help_button)

        self.setCentralWidget(container)



    def organizar_archivos(self):
        try:
            carpeta_origen = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta de origen")
            if not carpeta_origen:
                return

            if not os.path.exists(carpeta_origen):
                self.status_label.setText(f"La ruta de origen {carpeta_origen} no existe.")
                return

            archivos = os.listdir(carpeta_origen)

            for archivo in archivos:
                archivo_ruta = os.path.join(carpeta_origen, archivo)
                if os.path.isfile(archivo_ruta):
                    _, extension = os.path.splitext(archivo)
                    extension = extension[1:]

                    carpeta_nombre = f"archivos {extension}".strip()
                    carpeta_ruta = os.path.join(carpeta_origen, carpeta_nombre)
                    if not os.path.exists(carpeta_ruta):
                        os.mkdir(carpeta_ruta)

                    shutil.move(archivo_ruta, os.path.join(carpeta_ruta, archivo))
                    mensaje = f"Se ha movido {archivo} a la carpeta {carpeta_nombre}"
                    self.status_label.setText(mensaje)
                    self.historial_archivos.append(mensaje)
                    self.actualizar_historial()

            self.status_label.setText("La organización de archivos se ha completado correctamente.")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def actualizar_historial(self):
        self.historial_text.setPlainText("\n".join(self.historial_archivos))

    def show_developer_info(self):
        developer_dialog = DeveloperInfoDialog()
        developer_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrganizadorArchivosApp()
    window.show()
    sys.exit(app.exec_())
