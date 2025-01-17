import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel, QMessageBox, QSystemTrayIcon, QHBoxLayout, QDialog, QCheckBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer, Qt

class CountdownTimer:
    def __init__(self, label, pause_button):
        self.label = label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_seconds = 0
        self.next_minutes = 0  # To hold the next countdown minutes
        self.is_paused = False  # Track if the timer is paused
        self.pause_button = pause_button  # Reference to the pause/resume button
        self.work_flag = True  # Initialize work_flag to True

    def start(self, minutes, next_minutes=None):
        self.minutes = minutes  # Store the countdown minutes
        self.remaining_seconds = minutes * 60  # Convert minutes to seconds
        self.next_minutes = next_minutes  # Store the next countdown minutes
        self.timer.start(1000)  # Update every second
        self.is_paused = False  # Ensure the timer is not paused
        self.pause_button.setText("Pause")  # Set button text to "Pause"
        self.pause_button.clicked.disconnect()  # Disconnect any previous connections
        self.pause_button.clicked.connect(pause_timer)  # Connect to pause_timer

    def update_timer(self):
        if self.remaining_seconds > 0 and not self.is_paused:
            mins, secs = divmod(self.remaining_seconds, 60)
            timer_display = '{:02d}:{:02d}'.format(mins, secs)
            if self.work_flag:
                self.label.setText(f"Should take rest in : \n{timer_display}")  # Update the label with the timer
            else:
                self.label.setText(f"Should start working in : \n{timer_display}")
            self.remaining_seconds -= 1
        elif self.remaining_seconds == 0:
            self.label.setText(f"Should take rest in : \n00:00")  # Update the label with the timer
            self.timer.stop()
            self.show_notification()  # Show notification when the countdown is complete
            self.next_minutes = entry_y.value() if self.work_flag else entry_x.value()
            self.work_flag = not self.work_flag  # Toggle the work_flag
            self.start(self.next_minutes, self.minutes)  # Start the next countdown
      
    def pause(self):
        self.is_paused = True  # Set the paused state to True
        self.timer.stop()  # Stop the timer
        self.pause_button.setText("Resume")  # Change button text to "Resume"
        self.pause_button.clicked.disconnect()  # Disconnect any previous connections
        self.pause_button.clicked.connect(resume_timer)  # Connect to resume_timer

    def resume(self):
        if self.is_paused:  # Only resume if currently paused
            self.is_paused = False  # Set the paused state to False
            self.timer.start(1000)  # Resume the timer
            self.pause_button.setText("Pause")  # Change button text back to "Pause"
            self.pause_button.clicked.disconnect()  # Disconnect any previous connections
            self.pause_button.clicked.connect(pause_timer)  # Connect to pause_timer

    def show_notification(self):
        notification_W2R = QSystemTrayIcon(window)  # Create a new notification for Work to Rest
        notification_W2R.setIcon(icon)
        notification_W2R.show()

        if self.work_flag:
            notification_W2R.showMessage("PC Usage Reminder", "Time to take rest!", QSystemTrayIcon.Information, 2000)
        else:
            notification_R2W = ModalDialog()  # Create a new notification for Rest to Work
            notification_R2W.exec_()

class ModalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Usage Reminder")
        self.setGeometry(100, 100, 300, 100)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Ensure the dialog stays on top


        message = QLabel("Are you ready to go back to work?")
        message.setFont(QFont('Arial', 14))
        message.setAlignment(Qt.AlignCenter)

        accept_button = QPushButton("Yes")
        accept_button.setFont(QFont('Arial', 12))
        accept_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(accept_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

def start_timer():
    try:
        total_minutes_x = total_minutes_y = 1
        total_minutes_x = entry_x.value()  # Get value from QSpinBox for X
        if total_minutes_x < 0:
            raise ValueError("ValueError")
        total_minutes_y = entry_y.value()  # Get value from QSpinBox for Y
        if total_minutes_y < 0:
            raise ValueError("ValueError")
        countdown_timer.start(total_minutes_x, total_minutes_y)  # Start countdown for X and set Y as next
    except ValueError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Input Error")
        msg.setWindowIcon(icon)
        msg.setInformativeText("Please enter positive integers for both countdown.")
        msg.setWindowTitle("Error")
        msg.exec_()

def pause_timer():
    countdown_timer.pause()  # Call the pause method

def resume_timer():
    countdown_timer.resume()  # Call the resume method

def toggle_dark_mode(state):
    if state == Qt.Checked:
        app.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: #ffffff;
            }
            QSpinBox {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #ffffff;  
            }
            QLabel {
                color: #ffffff;
            }
        """)
    else:
        app.setStyleSheet("")

def set_buttons(layout):
    # Create a horizontal layout for the buttons
    button_layout = QHBoxLayout()

    start_button = QPushButton("Start")
    start_button.setFixedWidth(200)
    start_button.setFont(QFont('Arial', 12))
    start_button.clicked.connect(start_timer)
    button_layout.addWidget(start_button)

    pause_button = QPushButton("Pause")
    pause_button.setFixedWidth(200)
    pause_button.setFont(QFont('Arial', 12))
    pause_button.clicked.connect(pause_timer)  # Initially connect to pause
    button_layout.addWidget(pause_button)

    # Add the horizontal button layout to the main layout
    layout.addLayout(button_layout)

def show_main_window():
    window.showNormal()
    window.activateWindow()

if __name__ == '__main__':
    #create_shortcut()  # Create the desktop shortcut

    # Create the main window
    app = QApplication(sys.argv)

    window = QWidget()
    screen_geometry = app.primaryScreen().availableGeometry()
    scaling_factor = 1.5  # Scaling factor for 150% scaling
    window_width, window_height = 450,300
    window_x = screen_geometry.width() - window_width
    window_y = screen_geometry.height() - window_height
    window.setGeometry(window_x, window_y, window_width, window_height)
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    window.setWindowTitle("PC USAGE TIMER")

    # Set the icon (provide your own icon file path)
    icon = QIcon("C:\\Users\\deryd\\Desktop\\WORKSPACE\\Personal Projects\\pcUseTimeReminder\\timer_alarm_digital_clock_wake_up_icon_262704.ico")  # Update with your icon path
    window.setWindowIcon(icon)

    # Create and place the input fields and buttons
    layout = QVBoxLayout()

    # Create a horizontal layout for the labels and input boxes
    time_input_layout = QHBoxLayout()

    # Create vertical layouts for each label and input box pair
    entry_x_layout = QVBoxLayout()
    entry_x_label = QLabel("Working Time:")
    entry_x_label.setFont(QFont('Arial', 14))  # Set font to Arial
    entry_x_layout.addWidget(entry_x_label)
    entry_x = QSpinBox()
    entry_x.setRange(0, 120)  # Set range for X (0 to 120 minutes)
    entry_x.setValue(25)  # Set default value to 25 mins
    entry_x.setSingleStep(5)  # Increase/decrease by 5 mins
    entry_x.setFont(QFont('Arial', 14))  # Set font to Arial
    entry_x.setSuffix(" mins")  # Append mins to the value
    entry_x_layout.addWidget(entry_x)
    time_input_layout.addLayout(entry_x_layout)

    entry_y_layout = QVBoxLayout()
    entry_y_label = QLabel("Rest Time:")
    entry_y_label.setFont(QFont('Arial', 14))  # Set font to Arial
    entry_y_layout.addWidget(entry_y_label)
    entry_y = QSpinBox()
    entry_y.setRange(0, 120)  # Set range for Y (0 to 120 minutes)
    entry_y.setValue(5)  # Set default value to 5 mins
    entry_y.setSingleStep(5)  # Increase/decrease by 5 mins
    entry_y.setFont(QFont('Arial', 14))  # Set font to Arial
    entry_y.setSuffix(" mins")  # Append mins to the value
    entry_y_layout.addWidget(entry_y)
    time_input_layout.addLayout(entry_y_layout)

    # Add the horizontal layout to the main layout
    layout.addLayout(time_input_layout)
    
    # Create a horizontal layout for the buttons
    button_layout = QHBoxLayout()

    start_button = QPushButton("Start")
    start_button.setFixedWidth(200)
    start_button.setFont(QFont('Arial', 12))
    start_button.clicked.connect(start_timer)
    button_layout.addWidget(start_button)

    pause_button = QPushButton("Pause")
    pause_button.setFixedWidth(200)
    pause_button.setFont(QFont('Arial', 12))
    pause_button.clicked.connect(pause_timer)  # Initially connect to pause
    button_layout.addWidget(pause_button)

    # Add the horizontal button layout to the main layout
    layout.addLayout(button_layout)
    
    # Create a label to display the timer
    label = QLabel()
    label.setFont(QFont('Arial', 24))  # Correctly set the font
    label.setAlignment(Qt.AlignCenter)  # Center align the text
    layout.addWidget(label)

    # Create a toggle switch for dark mode
    dark_mode_toggle = QCheckBox("Dark Mode")
    dark_mode_toggle.setFont(QFont('Arial', 12))
    dark_mode_toggle.stateChanged.connect(toggle_dark_mode)
    dark_mode_toggle.setCheckState(Qt.Checked)  # Set dark mode as default
    layout.addWidget(dark_mode_toggle)

    toggle_dark_mode(Qt.Checked)  

    window.setLayout(layout)
    
    # Initialize the countdown timer
    countdown_timer = CountdownTimer(label, pause_button)

    window.show()
    sys.exit(app.exec_())