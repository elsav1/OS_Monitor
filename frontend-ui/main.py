import sys
import os
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QSizePolicy, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QFont
import pyqtgraph as pg
import qdarktheme

# Enable antialiasing for smoother graphs
pg.setConfigOptions(antialias=True)

class DataFetcher(QThread):
    newData = pyqtSignal(float, float, float, float, float, int)

    def run(self):
        while True:
            stats = self.read_stats()
            self.newData.emit(*stats)
            time.sleep(2)

    def read_stats(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_stats.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    parts = file.read().strip().split(",")
                    if len(parts) >= 6:
                        return (
                            float(parts[0].strip()),
                            float(parts[1].strip()),
                            float(parts[2].strip()),
                            float(parts[3].strip()),
                            float(parts[4].strip()),
                            int(parts[5].strip())
                        )
            except Exception as e:
                print("Error reading system stats:", e)
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0


class ModernCard(QWidget):
    def __init__(self, title, color_hex):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #AAAAAA;")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.value_label = QLabel("0.0")
        self.value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {color_hex};")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_label)
        self.setLayout(self.layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
                border-radius: 10px;
                border: 1px solid #333333;
            }
        """)

    def update_value(self, value, suffix=""):
        self.value_label.setText(f"{value:.1f}{suffix}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 AI OS Monitor Pro")
        self.setGeometry(100, 100, 1000, 750)

        # Setup system tray
        self.tray_icon = QSystemTrayIcon(self)
        # Using a default system icon just as a placeholder
        icon = self.style().standardIcon(self.style().SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        
        tray_menu = QMenu()
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.showNormal)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Layouts
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.header_layout = QHBoxLayout()
        self.status_label = QLabel("● SYSTEM NORMAL")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.status_label.setStyleSheet("color: #00FF00; padding: 10px;")
        self.header_layout.addWidget(self.status_label)
        self.header_layout.addStretch()
        
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        
        # Cards
        self.cpu_card = ModernCard("CPU Usage", "#00BFFF")
        self.mem_card = ModernCard("Memory", "#32CD32")
        self.disk_card = ModernCard("Disk", "#FFD700")
        self.net_card = ModernCard("Network", "#FF69B4")
        self.swap_card = ModernCard("Swap", "#FFA500")

        self.cards_layout.addWidget(self.cpu_card)
        self.cards_layout.addWidget(self.mem_card)
        self.cards_layout.addWidget(self.disk_card)
        self.cards_layout.addWidget(self.net_card)
        self.cards_layout.addWidget(self.swap_card)

        # Charts Layout
        self.chart_layout = QGridLayout()
        self.chart_layout.setSpacing(15)

        # Function to create identical plots
        def create_plot(title, y_range=None):
            plot = pg.PlotWidget(title=title)
            plot.showGrid(x=True, y=True, alpha=0.3)
            plot.setLabel('bottom', "Time", units="s")
            if y_range:
                plot.setYRange(y_range[0], y_range[1])
            plot.setBackground('#1A1A1A')
            return plot

        self.cpu_plot = create_plot("CPU (%)", (0, 100))
        self.mem_plot = create_plot("Memory (%)", (0, 100))
        self.disk_plot = create_plot("Disk (%)", (0, 100))
        self.net_plot = create_plot("Network (MB/s)") # Dynamic Y axis
        self.swap_plot = create_plot("Swap (%)", (0, 100))
        
        # Line references
        self.cpu_curve = self.cpu_plot.plot(pen=pg.mkPen(color='#00BFFF', width=2))
        self.mem_curve = self.mem_plot.plot(pen=pg.mkPen(color='#32CD32', width=2))
        self.disk_curve = self.disk_plot.plot(pen=pg.mkPen(color='#FFD700', width=2))
        self.net_curve = self.net_plot.plot(pen=pg.mkPen(color='#FF69B4', width=2))
        self.swap_curve = self.swap_plot.plot(pen=pg.mkPen(color='#FFA500', width=2))

        # We need a scatter plot item for CPU anomalies to stand out
        self.anomaly_scatter = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
        self.cpu_plot.addItem(self.anomaly_scatter)

        self.chart_layout.addWidget(self.cpu_plot, 0, 0, 1, 2)
        self.chart_layout.addWidget(self.mem_plot, 1, 0)
        self.chart_layout.addWidget(self.swap_plot, 1, 1)
        self.chart_layout.addWidget(self.disk_plot, 2, 0)
        self.chart_layout.addWidget(self.net_plot, 2, 1)

        # Final layout
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.cards_layout)
        self.main_layout.addLayout(self.chart_layout)
        self.setLayout(self.main_layout)

        # Data buffers
        self.max_points = 60
        self.counter = 0
        self.timestamps = []
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []
        self.swap_data = []
        self.anomaly_data = [] # stores indices where anomaly == 1

        # Data fetcher thread
        self.data_fetcher = DataFetcher()
        self.data_fetcher.newData.connect(self.update_stats)
        self.data_fetcher.start()

    def update_stats(self, cpu, memory, disk, network, swap, anomaly):
        self.counter += 2
        
        self.timestamps.append(self.counter)
        self.cpu_data.append(cpu)
        self.memory_data.append(memory)
        self.disk_data.append(disk)
        self.network_data.append(network)
        self.swap_data.append(swap)
        self.anomaly_data.append(anomaly)

        if len(self.timestamps) > self.max_points:
            self.timestamps = self.timestamps[-self.max_points:]
            self.cpu_data = self.cpu_data[-self.max_points:]
            self.memory_data = self.memory_data[-self.max_points:]
            self.disk_data = self.disk_data[-self.max_points:]
            self.network_data = self.network_data[-self.max_points:]
            self.swap_data = self.swap_data[-self.max_points:]
            self.anomaly_data = self.anomaly_data[-self.max_points:]

        # Update Cards
        self.cpu_card.update_value(cpu, "%")
        self.mem_card.update_value(memory, "%")
        self.disk_card.update_value(disk, "%")
        self.net_card.update_value(network, " MB")
        self.swap_card.update_value(swap, "%")

        if anomaly:
            self.status_label.setText("⚠ ANOMALY DETECTED")
            self.status_label.setStyleSheet("color: #FF0000; padding: 10px;")
        else:
            self.status_label.setText("● SYSTEM NORMAL")
            self.status_label.setStyleSheet("color: #00FF00; padding: 10px;")

        # Update charts
        self.cpu_curve.setData(self.timestamps, self.cpu_data)
        self.mem_curve.setData(self.timestamps, self.memory_data)
        self.disk_curve.setData(self.timestamps, self.disk_data)
        self.net_curve.setData(self.timestamps, self.network_data)
        self.swap_curve.setData(self.timestamps, self.swap_data)

        # Update anomaly scatter plot
        anomaly_x = [self.timestamps[i] for i, a in enumerate(self.anomaly_data) if a == 1]
        anomaly_y = [self.cpu_data[i] for i, a in enumerate(self.anomaly_data) if a == 1]
        self.anomaly_scatter.setData(anomaly_x, anomaly_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme() # Set modern dark theme
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
