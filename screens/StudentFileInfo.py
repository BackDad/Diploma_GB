from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class StudentInfoDialog(QDialog):
    def __init__(self, student_data, parent=None):
        super().__init__(parent)

        # Создаем макет для диалогового окна
        layout = QVBoxLayout()

        # Добавляем виджеты с информацией об ученике на макет
        for key, value in student_data.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)

        # Кнопка для закрытия диалогового окна
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(button_box)
        self.setLayout(layout)
