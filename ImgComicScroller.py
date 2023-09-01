import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QLabel, QScrollArea, QAction, QFileDialog, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.image = None
        self.label = QLabel(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setStyleSheet("background-color: black;")
        self.scroll_area.verticalScrollBar().setStyleSheet("background-color: black;")
        self.scroll_area.horizontalScrollBar().setStyleSheet("background-color: black;")
        self.setCentralWidget(self.scroll_area)
        self.setStyleSheet("background-color: black; color: gray;")

        self.create_toolbar()

        # Get a list of image paths in the current folder
        self.image_paths = []
        self.current_directory = None
        self.current_image_index = 0

        # Set the initial size of the window to 1600x900
        self.setGeometry(100, 100, 1600, 900)

    def wheelEvent(self, event):
        scroll_speed = 100
        if event.angleDelta().y() > 0:  # Scroll up
            self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() - scroll_speed)
        else:  # Scroll down
            self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() + scroll_speed)

    def create_toolbar(self):
        open_action = QAction("Open Image", self)
        open_action.triggered.connect(self.open_image)

        next_action = QAction("Next Image", self)
        next_action.triggered.connect(self.next_image)

        previous_action = QAction("Previous Image", self)
        previous_action.triggered.connect(self.previous_image)

        scrollbar_button = QAction("Toggle Scroll Bars", self)
        scrollbar_button.triggered.connect(self.toggle_scroll_bars)

        resize_height_button = QAction("Fit Height", self)
        resize_height_button.triggered.connect(self.resize_height_image)

        resize_width_button = QAction("Fit Width", self)
        resize_width_button.triggered.connect(self.resize_width_image)


        # Add a stretchable space to push the actions to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar = self.addToolBar("Toolbar")
        toolbar.addAction(open_action)
        toolbar.addAction(scrollbar_button)

        toolbar.addWidget(spacer)
        
        toolbar.addAction(resize_height_button)
        toolbar.addAction(resize_width_button)
        toolbar.addAction(previous_action)
        toolbar.addAction(next_action)

    def open_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.pn *.jp *.xpm *.jpg *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                self.image = QPixmap(file_path)
                if self.image.isNull():
                    raise Exception("Failed to load image")
                self.image_path = file_path
                self.label.setPixmap(self.image)
                self.label.adjustSize()
                self.scroll_area.ensureVisible(0, 0)
                self.resize_window()
                self.current_directory = os.path.dirname(file_path)
                self.update_image_paths()
                self.current_image_index = self.image_paths.index(self.image_path)
            except Exception as e:
                print(f"Error: {str(e)}")

    def update_image_paths(self):
        self.image_paths = []
        if self.current_directory:
            for file_name in os.listdir(self.current_directory):
                if file_name.lower().endswith((".png", ".pn", ".jpg", ".jpeg", ".jp", ".bmp")):
                    self.image_paths.append(os.path.abspath(os.path.join(self.current_directory, file_name)))
            if self.image_path:
                image_file_name = os.path.basename(self.image_path)
                for i, path in enumerate(self.image_paths):
                    if os.path.basename(path) == image_file_name:
                        self.current_image_index = i
                        print("update_image_paths")
                        return
                self.current_image_index = 0
                print("zero")
        else:
            self.current_image_index = 0
            print("zero")

    def next_image(self):
        if not self.image_paths:
            return
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        try:
            file_path = self.image_paths[self.current_image_index]
            self.load_image(file_path)
        except Exception as e:
            print(f"Error: {str(e)}")

    def previous_image(self):
        if not self.image_paths:
            return
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        try:
            file_path = self.image_paths[self.current_image_index]
            self.load_image(file_path)
        except Exception as e:
            print(f"Error: {str(e)}")

    def load_image(self, file_path):
        try:
            self.image = QPixmap(file_path)
            if self.image.isNull():
                raise Exception("Failed to load image")
            self.image_path = file_path
            self.label.setPixmap(self.image)
            self.label.adjustSize()
            self.scroll_area.ensureVisible(0, 0)
            self.resize_window()
        except Exception as e:
            print(f"Error: {str(e)}")

    def toggle_scroll_bars(self):
        if self.scroll_area.verticalScrollBar().isVisible():
            self.scroll_area.verticalScrollBar().setVisible(False)
            self.scroll_area.horizontalScrollBar().setVisible(False)
        else:
            self.scroll_area.verticalScrollBar().setVisible(True)
            self.scroll_area.horizontalScrollBar().setVisible(True)

    def resize_width_image(self):
        if self.image is None:
            return
        self.label.setPixmap(self.image.scaledToWidth(self.scroll_area.width()))

    def resize_height_image(self):
        if self.image is None:
            return
        self.label.setPixmap(self.image.scaledToHeight(self.scroll_area.height()))

    def resize_window(self):
        image_height = self.image.height()
        window_height = self.height()
        if image_height > window_height and image_height < 1000:
            self.resize(self.width(), image_height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())