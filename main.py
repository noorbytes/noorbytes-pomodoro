from PyQt5.QtCore import QTimer, Qt, QUrl, QDate, QSize  # Import QDate and QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QMenuBar, QAction, QInputDialog, QMessageBox, QToolButton, QMenu, QStackedWidget
from PyQt5.QtChart import QChartView, QChart, QBarSet, QBarSeries, QBarCategoryAxis

import sqlite3
import sys
import os
import random
import time
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis  # Import for charts



base_dir = os.path.dirname(os.path.abspath(__file__))
app_icon_path = os.path.join(base_dir, "icon.png")
tree_icon_path = os.path.join(base_dir, "design.png")

# Paths to sound files
start_sound_path = os.path.join(base_dir, "sound.wav")
break_sound_path = os.path.join(base_dir, "sound.wav")

# Database Setup
def setup_database():
    conn = sqlite3.connect("trees.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            trees_grown INTEGER
        )
    """)
    conn.commit()
    conn.close()

class PromodApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.quotes = [
    "And say, 'My Lord, increase me in knowledge.' — Qur'an 20:114",
    "The seeking of knowledge is obligatory for every Muslim. — Prophet Muhammad (PBUH)",
    "Whoever follows a path in pursuit of knowledge, Allah will make easy for him a path to Paradise. — Prophet Muhammad (PBUH)",
    "Work hard in silence, let your success be your noise. — Unknown",
    "Your reward for working hard is greater than you can imagine. — Unknown",
    "When you work hard, trust in Allah, and ask Him for success, you are doing it all right. — Unknown",
    "The one who seeks knowledge in the way of Allah will be blessed with success. — Unknown",
    "Do not underestimate the value of small efforts; every step counts. — Unknown",
    "With hard work and sincerity, no goal is too big to achieve. — Unknown",
    "Seek knowledge even if it takes you to China. — Prophet Muhammad (PBUH)",
    "Knowledge is the light that will guide you through the darkness of life. — Unknown",
    "A good deed is like a seed, it grows and multiplies. — Unknown",
    "Patience and perseverance are the keys to success. — Unknown",
    "Success comes to those who keep trying even when the road gets tough. — Unknown",
    "Ask Allah for help, then work hard to reach your goals. — Unknown",
    "The best of you are those who are most beneficial to others. — Prophet Muhammad (PBUH)",
    "When you seek knowledge, you are not only gaining wisdom, you are gaining closeness to Allah. — Unknown",
    "Your effort is your worship. — Unknown",
    "Knowledge is not what is memorized, but what benefits. — Prophet Muhammad (PBUH)",
    "Never stop learning, for life never stops teaching. — Unknown",
    "The strongest among you is the one who controls his anger. — Prophet Muhammad (PBUH)",
    "Do not give up, for victory is near. — Unknown",
    "Verily, with hardship comes ease. — Qur'an 94:6",
    "Success is not the key to happiness. Happiness is the key to success. — Unknown",
    "Work with sincerity, and leave the results to Allah. — Unknown",
    "The best of people are those who are most beneficial to others. — Prophet Muhammad (PBUH)",
    "Keep working hard and trust in Allah’s plan for you. — Unknown",
    "Your success is in the hands of Allah, your effort is in your hands. — Unknown",
    "Doubt kills more dreams than failure ever will. — Unknown",
    "Let your faith in Allah guide your every step. — Unknown",
    "Rise up, and aim high, for Allah will guide your way. — Unknown",
    "Knowledge is a light that leads to success. — Unknown",
    "Do not wait for the perfect moment, take the moment and make it perfect. — Unknown",
    "Your effort is your sincerity, and your sincerity will lead you to success. — Unknown",
    "Patience is the companion of wisdom. — Unknown",
    "The world is a bridge; pass over it, but do not build upon it. — Prophet Muhammad (PBUH)",
    "Strive for excellence in all that you do. — Unknown",
    "A person who has a goal is unstoppable. — Unknown",
    "Success is not about what you accomplish, but what you inspire others to do. — Unknown",
    "Those who strive in the path of Allah will be rewarded beyond measure. — Qur'an 9:20",
    "The more you learn, the more you realize how much you don’t know. — Unknown",
    "Let the challenges you face today be the lessons you learn tomorrow. — Unknown",
    "Work hard, stay humble, and Allah will guide you to success. — Unknown",
    "The best way to predict your future is to create it. — Unknown",
    "Success comes to those who take action. — Unknown",
    "If you want to succeed, work harder than yesterday. — Unknown",
    "In the pursuit of knowledge, let your heart be sincere. — Unknown",
    "Hard work and dedication are the keys to unlock your dreams. — Unknown",
    "Every moment of hardship is a lesson in disguise. — Unknown",
    "Do not rush; success takes time and patience. — Unknown",
    "Good things come to those who work for them. — Unknown",
    "Sincerity in your effort will lead you to success. — Unknown",
    "The harder you work, the luckier you get. — Unknown",
    "Knowledge is power when you use it for good. — Unknown",
    "Don’t let fear stop you from achieving your goals. — Unknown",
    "Let your heart be filled with ambition and trust in Allah’s plan. — Unknown",
    "Believe in yourself and the success that lies ahead. — Unknown",
    "Discipline is the bridge between goals and accomplishment. — Unknown",
    "Your focus determines your success. — Unknown",
    "Trust Allah's plan for you, and your hard work will pay off. — Unknown",
    "A moment of patience in a moment of anger prevents a thousand regrets. — Prophet Muhammad (PBUH)",
    "Stay consistent in your efforts, and success will come. — Unknown",
    "In every challenge, there’s a hidden blessing. — Unknown",
    "Your effort is an act of worship; let your work reflect your faith. — Unknown",
    "Hard work may not always bring immediate results, but it will eventually pay off. — Unknown",
    "Don’t look for success, create it. — Unknown",
    "The more effort you put, the closer you get to your goal. — Unknown",
    "Strive for the best in this world and the next. — Unknown",
    "What you sow today will shape your tomorrow. — Unknown",
    "The best way to find yourself is to lose yourself in the service of others. — Mahatma Gandhi",
    "Success in life comes from doing your best and trusting Allah with the rest. — Unknown",
    "The reward of patience is greater than you can imagine. — Unknown",
    "Seek Allah’s help, then strive with all your might. — Unknown",
    "The reward of the believer’s actions is far greater than their efforts. — Unknown",
    "A small deed with sincerity is better than a grand deed without it. — Unknown"
]

        
        # App state variables
        self.timer = QTimer()
        self.time_left = 45 * 60  # 45 minutes in seconds
        self.break_time = 5 * 60  # 5 minutes in seconds
        self.is_break = False
        self.trees_grown = 0
        self.setWindowIcon(QIcon(app_icon_path))  # Replace with your app icon file path

        # UI setup
        self.init_ui()

        # Connect timer
        self.timer.timeout.connect(self.update_timer)

        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.update_quote)
        self.quote_timer.start(180000)  # Update every 3 minutes

        self.load_progress()
        self.is_paused = False  # Add a flag to track the pause state

        # Initialize sound effects
        self.start_sound = QSound(start_sound_path)
        self.break_sound = QSound(break_sound_path)

        # Load progress from the database
        self.load_progress()

    def init_ui(self):
        self.setWindowTitle("Promodo Tree App")
        self.resize(500, 400)
        
        # Set fonts and styles
        main_font = QFont("Arial", 14)
        self.setStyleSheet("background-color: #40444b; color: #FCE7DD;")
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Stacked Widget for page navigation
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Main Page
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout(self.main_page)

        # Hamburger Menu Button
        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(QIcon(os.path.join(base_dir, "hammy.png")))  # Replace with your hamburger icon path
        self.menu_button.setStyleSheet("background-color: #40444b; border: none;")
        self.menu_button.setPopupMode(QToolButton.InstantPopup)
        self.menu_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.menu_button.setIconSize(QSize(24, 24))

        # Menu
        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #2c2f33;
                color: #FCE7DD;
                border: 1px solid #23272a;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #7289da;
            }
        """)

        # Tree Progress Menu
        self.daily_progress_action = QAction("Daily Progress", self)
        self.daily_progress_action.triggered.connect(self.show_daily_progress)
        self.menu.addAction(self.daily_progress_action)
        self.monthly_progress_action = QAction("Monthly Progress", self)
        self.monthly_progress_action.triggered.connect(self.show_monthly_progress)
        self.menu.addAction(self.monthly_progress_action)
        self.yearly_progress_action = QAction("Yearly Progress", self)
        self.yearly_progress_action.triggered.connect(self.show_yearly_progress)
        self.menu.addAction(self.yearly_progress_action)

        self.menu_button.setMenu(self.menu)
        self.main_layout.addWidget(self.menu_button, alignment=Qt.AlignTop | Qt.AlignRight)

        # Header with image
        header_layout = QHBoxLayout()
        self.icon_label = QLabel()
        pixmap = QPixmap(tree_icon_path)  # Replace with a path to your tree icon file
        self.icon_label.setPixmap(pixmap.scaled(50, 50))
        header_layout.addWidget(self.icon_label)

        self.title_label = QLabel("Promodoro Tree App")
        self.title_label.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: #CC6C70;")
        self.title_label.setAlignment(Qt.AlignCenter)  # Center the title label
        header_layout.addWidget(self.title_label)
        header_layout.setAlignment(Qt.AlignCenter)  # Center the header layout
        self.main_layout.addLayout(header_layout)

        # Time Left label (display text) 
        self.time_left_label = QLabel("Time Left:")
        self.time_left_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.time_left_label.setStyleSheet("color: #FCE7DD;")
        self.time_left_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.time_left_label)

        # Timer label (showing the countdown in a big font)
        self.timer_label = QLabel("45:00")  # Initial time set to 45 minutes
        self.timer_label.setFont(QFont("Arial", 40, QFont.Bold))
        self.timer_label.setStyleSheet("color: #FCE7DD;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_label)

        # Start button
        self.start_button = QPushButton("Start Work")
        self.start_button.setFont(main_font)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #388e3c;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.start_button.clicked.connect(self.start_timer)
        self.main_layout.addWidget(self.start_button)

        # Pause/Resume button
        self.pause_button = QPushButton("Pause Timer")
        self.pause_button.setFont(main_font)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #e65100;
            }
            QPushButton:hover {
                background-color: #fb8c00;
            }
            QPushButton:pressed {
                background-color: #e65100;
            }
        """)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.main_layout.addWidget(self.pause_button)

        # Reset button
        self.reset_button = QPushButton("Reset Timer")
        self.reset_button.setFont(main_font)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #d32f2f;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """)
        self.reset_button.clicked.connect(self.reset_timer)
        self.main_layout.addWidget(self.reset_button)

        # Trees grown label
        self.trees_label = QLabel(f"Total Trees Grown: {self.get_total_trees_grown()}")
        self.trees_label.setFont(QFont("Arial", 25, QFont.Bold))
        self.trees_label.setStyleSheet("color: #FCE7DD;")
        self.trees_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.trees_label)

        # Add a decorative tree vector (placeholder)
        self.tree_vector_label = QLabel()
        vector_pixmap = QPixmap(app_icon_path)  # Replace with a path to your decorative tree file
        self.tree_vector_label.setPixmap(vector_pixmap.scaled(200, 200))
        self.tree_vector_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.tree_vector_label)
        
        self.quote_label = QLabel("Loading quote...")
        self.quote_label.setFont(QFont("Arial", 14, italic=True))
        self.quote_label.setStyleSheet("color: #FCE7DD;")
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setWordWrap(True)  # Enable word wrap
        self.main_layout.addWidget(self.quote_label)

        # Small "Developed by Dev-adalz" text at bottom left
        self.developer_label = QLabel("Developed by Dev-adalz ©")
        self.developer_label.setFont(QFont("Arial", 10))
        self.developer_label.setStyleSheet("color: #FCE7DD;")
        self.developer_label.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.developer_label, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.stacked_widget.addWidget(self.main_page)

        # Set up a timer to update the quote every 3 minutes (180,000 ms)
        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.update_quote)
        self.quote_timer.start(5000)  # Update every 3 minutes

    def show_daily_progress(self):
        date = QDate.currentDate().toString("yyyy-MM-dd")
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM progress WHERE DATE(timestamp) = ?", (date,))
        result = cursor.fetchone()
        trees_today = result[0] if result else 0
        conn.close()
        self.show_progress_page(f"Trees grown today ({date}): {trees_today}", "daily")

    def show_monthly_progress(self):
        date = QDate.currentDate().toString("yyyy-MM")
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT strftime('%d', timestamp) as day, COUNT(*) FROM progress WHERE strftime('%Y-%m', timestamp) = ? GROUP BY day", (date,))
        results = cursor.fetchall()
        conn.close()
        days_in_month = QDate.currentDate().daysInMonth()
        trees_per_day = [0] * days_in_month
        for day, count in results:
            trees_per_day[int(day) - 1] = count
        self.show_progress_page(f"Trees grown this month ({date}):", "monthly", trees_per_day)

    def show_yearly_progress(self):
        date = QDate.currentDate().toString("yyyy")
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT strftime('%m', timestamp) as month, COUNT(*) FROM progress WHERE strftime('%Y', timestamp) = ? GROUP BY month", (date,))
        results = cursor.fetchall()
        conn.close()
        trees_per_month = [0] * 12
        for month, count in results:
            trees_per_month[int(month) - 1] = count
        self.show_progress_page(f"Trees grown this year ({date}):", "yearly", trees_per_month)

    def show_progress_page(self, progress_text, period, data=None):
        progress_page = QWidget()
        progress_layout = QVBoxLayout(progress_page)

        # Progress label
        progress_label = QLabel(progress_text)
        progress_label.setFont(QFont("Arial", 18, QFont.Bold))
        progress_label.setStyleSheet("color: #FCE7DD;")
        progress_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(progress_label)

        # Chart
        chart = QChart()
        chart.setTitle(f"{period.capitalize()} Progress")
        bar_set = QBarSet("Trees Grown")
        if period == "daily":
            bar_set.append([self.get_trees_count(period)])
            categories = [QDate.currentDate().toString("yyyy-MM-dd")]
        elif period == "monthly":
            bar_set.append(data)
            days_in_month = QDate.currentDate().daysInMonth()
            categories = [str(i + 1) for i in range(days_in_month)]
        elif period == "yearly":
            bar_set.append(data)
            categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        chart.createDefaultAxes()
        chart_view = QChartView(chart)
        progress_layout.addWidget(chart_view)

        # Back button
        back_button = QPushButton("Back to Main Page")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #5b6eae;
            }
            QPushButton:hover {
                background-color: #5b6eae;
            }
            QPushButton:pressed {
                background-color: #4e5b8a;
            }
        """)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        progress_layout.addWidget(back_button)

        self.stacked_widget.addWidget(progress_page)
        self.stacked_widget.setCurrentWidget(progress_page)

    def get_trees_count(self, period):
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        if period == "daily":
            date = QDate.currentDate().toString("yyyy-MM-dd")
            cursor.execute("SELECT COUNT(*) FROM progress WHERE DATE(timestamp) = ?", (date,))
        elif period == "monthly":
            date = QDate.currentDate().toString("yyyy-MM")
            cursor.execute("SELECT COUNT(*) FROM progress WHERE strftime('%Y-%m', timestamp) = ?", (date,))
        elif period == "yearly":
            date = QDate.currentDate().toString("yyyy")
            cursor.execute("SELECT COUNT(*) FROM progress WHERE strftime('%Y', timestamp) = ?", (date,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def get_total_trees_grown(self):
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM progress")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def update_quote(self):
        """Update the quote label with a random quote from the list."""
        random_quote = random.choice(self.quotes)
        self.quote_label.setText(random_quote)

    def start_timer(self):
        self.start_sound.play()  # Play start sound
        self.timer_label.setText("Work Focused. Timer Started")
        self.update_ui()  # Ensure UI is updated immediately
        self.timer.start(1000)  # Update every second
        self.start_button.setVisible(False)  # Hide start button

    def toggle_pause(self):
        if self.is_paused:
            self.timer.start(1000)  # Resume the timer
            self.pause_button.setText("Pause Timer")
            self.timer_label.setText("Work Focused. Timer Resumed")
        else:
            self.timer.stop()
            self.pause_button.setText("Resume Timer")
            self.timer_label.setText("Timer Paused")
        self.is_paused = not self.is_paused

    def update_timer(self):
        if not self.is_break:
            self.time_left -= 1
            if self.time_left <= 0:
                self.timer.stop()
                self.is_break = True
                self.time_left = self.break_time
                self.grow_tree()
                self.time_left_label.setText("Break:")
                self.timer_label.setText("Break Time: Relax!")
                self.break_sound.play()  # Play break sound
                self.start_button.setVisible(False)  # Hide start button
                self.timer.start(1000)  # Auto start break timer
        else:
            self.time_left -= 1
            if self.time_left <= 0:
                self.timer.stop()
                self.is_break = False
                self.time_left = 45 * 60
                self.time_left_label.setText("Time Left:")
                self.timer_label.setText("Work Time: Stay Focused!")
                self.start_button.setVisible(True)  # Show start button

        self.update_ui()

    def reset_timer(self):
        self.timer.stop()
        self.time_left = 45 * 60
        self.is_break = False
        self.timer_label.setText("Press Start to grow your tree!")
        self.start_button.setVisible(True)  # Show start button
        self.pause_button.setText("Pause Timer")  # Reset pause button text
        self.is_paused = False  # Reset pause state
        self.update_ui()
    
    def grow_tree(self):
        self.trees_grown += 1
        self.trees_label.setText(f"Trees Grown: {self.trees_grown}")
        
        # Save progress to the database
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO progress (timestamp, trees_grown) VALUES (datetime('now'), ?)" , (self.trees_grown,))
        conn.commit()
        conn.close()

    def load_progress(self):
        """Load the progress from the database."""
        conn = sqlite3.connect("trees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT trees_grown FROM progress ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            self.trees_grown = result[0]
        else:
            self.trees_grown = 0
        self.trees_label.setText(f"Trees Grown: {self.trees_grown}")  # Update the label with the loaded value
        conn.close()

    def update_ui(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")
        
    

if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    window = PromodApp()
    window.show()
    sys.exit(app.exec_())
