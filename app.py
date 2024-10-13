import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, 
                             QFormLayout, QGroupBox)

class ProductForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.create_database()

    def initUI(self):
        self.setWindowTitle('Formulario de Productos')

        # Layout principal
        layout = QVBoxLayout()

        # Grupo para el formulario
        form_group = QGroupBox("Detalles del Producto")
        form_layout = QFormLayout()

        self.product_name = QLineEdit()
        self.product_price = QLineEdit()
        self.image_path = QLineEdit()
        self.image_path.setReadOnly(True)
        self.image_button = QPushButton('Cargar Imagen')
        self.image_button.clicked.connect(self.load_image)

        form_layout.addRow(QLabel('Nombre:'), self.product_name)
        form_layout.addRow(QLabel('Precio:'), self.product_price)
        form_layout.addRow(QLabel('Imagen:'), self.image_path)
        form_layout.addRow(self.image_button)

        form_group.setLayout(form_layout)

        # Botón para guardar
        save_button = QPushButton('Guardar Producto')
        save_button.clicked.connect(self.save_product)

        layout.addWidget(form_group)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def create_database(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                image_path TEXT
            )
        ''')
        self.conn.commit()

    def load_image(self):
        # Usar QFileDialog sin crear una instancia de Option
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar Imagen", 
            "", 
            "Images (*.png *.xpm *.jpg);;All Files (*)"
        )
        if file_name:
            self.image_path.setText(file_name)

    def save_product(self):
        name = self.product_name.text()
        price = self.product_price.text()
        image_path = self.image_path.text()

        if name and price and image_path:
            self.cursor.execute('''
                INSERT INTO products (name, price, image_path) VALUES (?, ?, ?)
            ''', (name, float(price), image_path))
            self.conn.commit()

            # Limpiar los campos después de guardar
            self.product_name.clear()
            self.product_price.clear()
            self.image_path.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ProductForm()
    form.show()
    sys.exit(app.exec())
