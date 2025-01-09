import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QScrollArea
)

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("PEP-8 Check")
        self.setGeometry(100, 100, 500, 570)

        self.list_lines = []

        main_layout = QVBoxLayout()

        self.title = QLabel('Vérification de PEP-8')
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.title)

        self.file_layout = QHBoxLayout()

        self.open_file_button = QPushButton("Ouvrir un fichier")
        self.open_file_button.clicked.connect(self.open_file)
        self.file_layout.addWidget(self.open_file_button)

        self.verify_button = QPushButton("Vérfier la PEP-8")
        self.verify_button.clicked.connect(self.verify)
        self.file_layout.addWidget(self.verify_button)

        self.save_button = QPushButton("Sauvegarder le fichier")
        self.save_button.clicked.connect(self.save)
        self.file_layout.addWidget(self.save_button)

        main_layout.addLayout(self.file_layout)

        self.file_label = QLabel("Aucun fichier ouvert")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scrollable_label = QScrollArea()
        self.scrollable_label.setWidget(self.file_label)
        self.scrollable_label.setWidgetResizable(True)

        main_layout.addWidget(self.scrollable_label)

        self.lignes_widget = QWidget()

        self.lignes = QFormLayout(self.lignes_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.lignes_widget)
        self.scroll_area.setWidgetResizable(True)

        main_layout.addWidget(self.scroll_area, stretch=1)


        self.setLayout(main_layout)


    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose a file", "",
            "Python Files (*.py);;All Files (*);;Text Files (*.txt)",
            options=options
        )

        if file_path:
            self.file_path = file_path
            self.file_name = self.file_path
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.file_text = file.read()
                self.file_label.setText(f"Fichier : {self.file_name}")
            except Exception as e:
                self.file_label.setText(f"Error reading file: {e}")
                self.file_text = None

        if self.file_text:
            self.list_lines = []
            self.list_lines = self.file_text.split("\n")

        self.update_lines()

    def verify(self):
        def check_length(line):
            if len(line) > 79:
                return False
            
            return True
            
        def check_commas(line):
            if "#" in line:
                return True
            
            for i, char in enumerate(line):
                if char == ",":
                    if i >= len(line) - 1:
                        return True
                    
                    if line[i - 1] == " ":
                        return False
                    
                    elif line[i + 1] != " " and line[i + 1] != ")" and line[i + 1] != "\n":
                        return False
            
            return True
    
        def check_parenthesis(line):
            if "#" in line:
                return True

            for i, char in enumerate(line):
                if i >= len(line) - 1:
                    return True
                
                if char == "(" and line[i + 1] == " ":
                    return False
                
                if char == ")" and line[i - 1] == " " and line[i - 2] != " ":
                    return False
                
            return True

        def check_points(line):
            if "#" in line:
                return True
            
            for i, char in enumerate(line):
                if char == ":" and line[i - 1] == " ":
                    return False
                
            return True

        def check_hashtag(line):
            if "#" in line:
                hash_pos = line.find("#")
                return hash_pos
            
            return None

        self.get_lines()
        self.errors_nb = 0
        for i, line in enumerate(self.list_lines):
            self.current_index = i

            if not check_length(line):
                print(f"La ligne {i + 1} est trop longue : {line}")
                self.errors_nb += 1

            hash_pos = check_hashtag(line)
            if hash_pos:
                self.current_line = line[:hash_pos]
            else:
                self.current_line = line

            if not check_commas(self.current_line):
                print(f"Attention à la virgule ligne {i + 1} : {self.current_line}")
                self.errors_nb += 1

            elif not check_parenthesis(self.current_line):
                print(f"Attention aux parenthèse ligne {i + 1} : {self.current_line}")
                self.errors_nb += 1

            elif not check_points(self.current_line):
                print(f"Attention aux deux-points ligne {i + 1} : {self.current_line}")
                self.errors_nb += 1

        print(f"Tu as fait {self.errors_nb} erreur{"s" if self.errors_nb > 1 else ""} en {len(self.list_lines)} lignes")

    def update_lines(self):
        self.labels = []

        while self.lignes.count() > 0:
            item = self.lignes.takeAt(0)
            item.widget().deleteLater()

        for line in self.list_lines:
            self.labels.append(QLineEdit(f"{line}"))
        
        for i, label in enumerate(self.labels):
            self.lignes.addRow(str(i + 1), label)

    def get_lines(self):
        self.list_lines = []
        for i in range(self.lignes.rowCount()):
            item = self.lignes.itemAt(i, QFormLayout.FieldRole)
            if item is not None:  # Check if the item exists
                widget = item.widget()
                if isinstance(widget, QLineEdit):
                    self.list_lines.append(widget.text())

    def save(self):
        self.get_lines()
        with open(self.file_path, "w", encoding='utf-8') as file:
            for i, line in enumerate(self.list_lines):
                file.write(line + str("\n" if i != len(self.list_lines) - 1 else ""))

app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())