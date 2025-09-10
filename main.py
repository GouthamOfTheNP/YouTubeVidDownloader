from pytubefix import YouTube
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QComboBox, QLabel, QVBoxLayout, QWidget, \
	QSizePolicy, QFileDialog
from PyQt6.QtCore import Qt
import sys
import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context(cafile=certifi.where())


class DownloaderWindow(QMainWindow):
	def __init__(self):
		self.folder_path = ""
		self.file_name = ""
		self.error_code = ""

		super().__init__()
		central_widget = QWidget(self)
		self.setCentralWidget(central_widget)
		self.setWindowTitle("YouTube Video Downloader")
		self.setMinimumSize(400, 300)

		self.title = QLabel()
		self.title.setText("Download YouTube Videos")
		self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.success_area = QLineEdit(self)
		self.success_area.setReadOnly(True)
		self.success_area.setPlaceholderText(self.error_code)
		self.success_area.hide()

		self.link_area = QLineEdit(self)
		self.link_area.setPlaceholderText("Enter YouTube video link here")
		self.link_area.returnPressed.connect(self.download)
		self.link_area.textChanged.connect(self.update_quality_options)

		self.quality_option = QComboBox(self)
		self.quality_option.addItem("Select video quality")

		self.open_folder_button = QPushButton("Open Folder", self)
		self.open_folder_button.clicked.connect(self.open_file_dialog)

		self.file_name_choice = QLineEdit(self)
		self.file_name_choice.setPlaceholderText("Enter your preferred filename")
		self.file_name_choice.textChanged.connect(self.update_file_name)

		download_button = QPushButton("Download", self)
		download_button.clicked.connect(self.download)
		download_button.clicked.connect(lambda clear: self.quality_option.clear())
		download_button.clicked.connect(lambda add: self.quality_option.addItem("Select video quality"))
		download_button.clicked.connect(lambda clear: self.link_area.clear())

		self.title.setMinimumHeight(20)
		self.title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.title.setStyleSheet("padding: 10%;")
		self.link_area.setMinimumHeight(40)
		self.link_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.link_area.setStyleSheet("padding: 10%;")
		self.quality_option.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.open_folder_button.setMinimumHeight(40)
		self.open_folder_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.open_folder_button.setStyleSheet("padding: 10%;")
		self.file_name_choice.setMinimumHeight(40)
		self.file_name_choice.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.file_name_choice.setStyleSheet("padding: 10%;")
		download_button.setMinimumHeight(40)
		download_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		download_button.setStyleSheet("padding: 10%;")
		self.success_area.setMinimumHeight(30)
		self.success_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		vbox = QVBoxLayout(central_widget)
		vbox.addWidget(self.title)
		vbox.addStretch()
		vbox.addWidget(self.link_area)
		vbox.addStretch()
		vbox.addWidget(self.quality_option)
		vbox.addStretch()
		vbox.addWidget(self.open_folder_button)
		vbox.addStretch()
		vbox.addWidget(self.file_name_choice)
		vbox.addStretch()
		vbox.addWidget(download_button)
		vbox.addStretch()
		vbox.addWidget(self.success_area)
		vbox.addStretch()
		vbox.setSpacing(0)
		vbox.setContentsMargins(10, 0, 10, 0)
		self.setLayout(vbox)

		self.show()

	def open_file_dialog(self):
		self.folder_path = QFileDialog.getExistingDirectory(self, "Open Directory")
		if self.folder_path:
			print("Selected Folder", self.folder_path)

	def update_file_name(self):
		self.file_name = self.file_name_choice.text().strip()

	def download(self):
		try:
			link = self.link_area.text().strip()
			selected_option = self.quality_option.currentText()
			resolution, mime_type, *fps = selected_option.split()
			progressive = True if "true" in selected_option.lower() else False
			fps_value = fps[0] if fps else None

			yt = YouTube(link)
			stream_to_download = ""
			for stream in yt.streams:
				if ((str(stream.resolution) == resolution) and (stream.mime_type == mime_type) and bool(progressive) ==
						stream.includes_audio_track):
					stream_to_download = stream
			if self.file_name == "":
				self.file_name = yt.title + resolution + '.' + mime_type.split('/')[1]
			else:
				if mime_type.split("/")[1] in self.file_name:
					self.file_name = self.file_name.split(".")[0]
				self.file_name = self.file_name + '.' + mime_type.split('/')[1]
			stream_to_download.download(output_path=self.folder_path, filename=self.file_name)
			self.error_code = "Successfully downloaded " + resolution
		except Exception as e:
			print(e)
			self.error_code = "Failed to download. Video is not available or does not exist"
		finally:
			self.success_area.setText(self.error_code)
			self.success_area.show()

	def update_quality_options(self):
		link = self.link_area.text().strip()
		if link:
			try:
				list_options = []
				yt = YouTube(link)
				self.quality_option.clear()

				for stream in yt.streams:
					list_options.append(
						f"{str(stream.resolution)} {stream.mime_type} {str(stream.fps) + " fps" if stream.resolution else ''} Includes audio: {stream.includes_audio_track}")

				self.quality_option.addItems(list_options)
			except Exception as e:
				print(e)
				self.quality_option.clear()
				self.quality_option.addItem("Failed to load video quality options")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = DownloaderWindow()
	sys.exit(app.exec())
