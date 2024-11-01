import sys
import os
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main import separate_audio  # Importing the separate_audio function

class AudioSeparatorApp(QWidget):
    def __init__(self, parent=None):
        super(AudioSeparatorApp, self).__init__(parent)
        self.resize(800, 600)
        
        # Layout setup
        layout = QVBoxLayout()
        
        # Button to select file
        self.select_file_btn = QPushButton("Select Audio File")
        self.select_file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_btn)
        
        # Text field to display selected file path
        self.file_path_display = QLineEdit()
        self.file_path_display.setReadOnly(True)
        layout.addWidget(self.file_path_display)
        
        # Button to start separation process
        self.process_btn = QPushButton("Separate Audio")
        self.process_btn.clicked.connect(self.process_audio)
        layout.addWidget(self.process_btn)
        
        # Text field to display status
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(self.status_display)
        
        self.setLayout(layout)
        self.setWindowTitle("Audio Separator App")

    def select_file(self):
        # Open file dialog to select .mp3 or .wav files
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Audio files (*.mp3 *.wav)")
        if fname:
            self.file_path_display.setText(fname)
            self.status_display.append(f"Selected file: {fname}")

    def process_audio(self):
        input_audio_path = self.file_path_display.text()
        if not input_audio_path:
            self.status_display.append("Please select a file first.")
            return
        
        # Specify output directory for separated files
        output_directory = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Run the separation process
        try:
            self.status_display.append("Processing, please wait...")
            separate_audio(input_audio_path, output_directory)
            self.status_display.append("Audio separation complete.")
            
            # Zip the output folder for download
            zip_path = os.path.join(os.getcwd(), "separated_audio.zip")
            shutil.make_archive("separated_audio", 'zip', output_directory)
            self.status_display.append(f"Output saved to: {zip_path}")
            
            # Cleanup
            shutil.rmtree(output_directory)  # Optionally remove temporary files

        except Exception as e:
            self.status_display.append(f"An error occurred: {str(e)}")
            return

def main():
    app = QApplication(sys.argv)
    ex = AudioSeparatorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
