import sys
from app import curSor, connekt, add_player, remove_player, record_performance, remove_performance
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QComboBox, QVBoxLayout, QPushButton, QLabel, QDialog, QLineEdit, QTableView, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIntValidator, QDoubleValidator


class MyWindow(QMainWindow):
    def __init__(self):       
        super().__init__()    
        self.setWindowTitle("Scout App")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        btn_add_player = QPushButton('Add Player')
        layout.addWidget(btn_add_player)
        btn_add_player.clicked.connect(self.handle_add_player)

        btn_view_players = QPushButton('View Players')
        layout.addWidget(btn_view_players)
        btn_view_players.clicked.connect(self.handle_view_players)

        btn_edit_players = QPushButton('Update Player Information')
        layout.addWidget(btn_edit_players)
        btn_edit_players.clicked.connect(self.handle_edit_player)

        btn_remove_players = QPushButton('Remove Player Information')
        layout.addWidget(btn_remove_players)
        btn_remove_players.clicked.connect(self.handle_remove_player)  

        btn_remove_performance = QPushButton('Remove Performance Information')
        layout.addWidget(btn_remove_performance)
        btn_remove_performance.clicked.connect(self.handle_remove_performance)

        btn_add_performance = QPushButton('Record Performance')
        layout.addWidget(btn_add_performance)
        btn_add_performance.clicked.connect(self.handle_add_performance)
        
        btn_view_performance = QPushButton('View Performance')
        layout.addWidget(btn_view_performance)
        btn_view_performance.clicked.connect(self.handle_view_performance)

        btn_update_performance = QPushButton('Update Performance')
        layout.addWidget(btn_update_performance)
        btn_update_performance.clicked.connect(self.handle_edit_performance)

    def handle_add_player(self):
        dialog = AddPlayerDialog(curSor,connekt)
        dialog.exec()
    
    def handle_view_players(self):
        dialog = ViewPlayerDialog(curSor)
        dialog.exec()

    def handle_edit_player(self):
        dialog = UpdatePlayerDialog(curSor,connekt)
        dialog.exec()
    
    def handle_remove_player(self):
        dialog = DeletePlayerDialog(curSor,connekt)
        dialog.exec()

    def handle_add_performance(self):
        dialog = AddPerformanceDialog(curSor,connekt)
        dialog.exec()
    
    def handle_view_performance(self):
        dialog = ViewPerformanceDialog(curSor)
        dialog.exec()

    def handle_edit_performance(self):
        dialog = UpdatePerformanceDialog(curSor,connekt)
        dialog.exec()
    
    def handle_remove_performance(self):
        dialog = DeletePerformanceDialog(curSor,connekt)
        dialog.exec()


class ViewPlayerDialog(QDialog):
    def __init__(self, curSor):
        super().__init__()
        self.setWindowTitle('Players')
        self.setMinimumSize(600,400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        table = QTableWidget()
        layout.addWidget(table)

        curSor.execute('SELECT * FROM players_tbl')
        rows = curSor.fetchall()

        table.setColumnCount(6)
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(['ID', 'Name', 'DOB', 'Weight', 'Height', 'Position'])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

class UpdatePlayerDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt
        self.setWindowTitle('Edit Player Table')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Player ID'))
        self.player_id_input = QLineEdit()
        self.player_id_input.setValidator(QIntValidator())  # integers only
        layout.addWidget(self.player_id_input)

        self.column_choice = QComboBox()
        self.column_choice.addItems(['Full Name', 'Date of Birth', 'Weight', 'Height', 'Position'])
        layout.addWidget(self.column_choice)

        layout.addWidget(QLabel('New Value'))
        self.new_value = QLineEdit()
        layout.addWidget(self.new_value)

        btn_save = QPushButton('Save')
        btn_save.clicked.connect(self.handle_save)
        layout.addWidget(btn_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)        


    def handle_save(self):
        player_id = self.player_id_input.text()
        column = self.column_choice.currentText()
        new_value = self.new_value.text()

        if column == 'Full Name' :
            self.curSor.execute('UPDATE players_tbl SET full_name = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Date of Birth' :
            self.curSor.execute('UPDATE players_tbl SET date_of_birth = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Weight' :
            self.curSor.execute('UPDATE players_tbl SET weight = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Height' :
            self.curSor.execute('UPDATE players_tbl SET height = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Position' :
            self.curSor.execute('UPDATE players_tbl SET positions = %s WHERE player_id = %s', (new_value, player_id))
        self.connekt.commit()
        self.player_id_input.clear()
        self.new_value.clear()

    
class AddPlayerDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt 
        self.setWindowTitle('Add Player')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Full Name"))
        self.full_name = QLineEdit()
        layout.addWidget(self.full_name)

        layout.addWidget(QLabel("Date of Birth"))
        self.date_of_birth = QLineEdit()
        layout.addWidget(self.date_of_birth)

        layout.addWidget(QLabel("Weight"))
        self.weight = QLineEdit()
        self.weight.setValidator(QDoubleValidator())  # decimals only
        layout.addWidget(self.weight)

        layout.addWidget(QLabel("Height"))
        self.tallness = QLineEdit()
        self.tallness.setValidator(QDoubleValidator())  # decimals only
        layout.addWidget(self.tallness)

        layout.addWidget(QLabel("Position"))
        self.position = QLineEdit()
        layout.addWidget(self.position)

        btn_save = QPushButton('Save')
        layout.addWidget(btn_save)
        btn_save.clicked.connect(self.handle_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)
    def handle_save(self):
        name = self.full_name.text()
        dob = self.date_of_birth.text()
        weight_input = self.weight.text()
        height_input = self.tallness.text()
        position_input = self.position.text()
        for field in [self.full_name, self.date_of_birth, self.weight, self.tallness, self.position]:
            field.clear()

        add_player(self.curSor, self.connekt, name, dob, weight_input, height_input,position_input)

class DeletePlayerDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt 
        self.setWindowTitle('Remove Player')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Player ID'))
        self.player_id_input = QLineEdit()
        self.player_id_input.setValidator(QIntValidator())  # integers only
        layout.addWidget(self.player_id_input)

        btn_save = QPushButton('Save')
        layout.addWidget(btn_save)
        btn_save.clicked.connect(self.handle_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)        


    def handle_save(self):
        player_id_input = self.player_id_input.text()

        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to remove this player?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            remove_player(self.curSor, self.connekt, player_id_input)

        for field in [self.player_id_input]:
            field.clear()

class ViewPerformanceDialog(QDialog):
    def __init__(self, curSor):
        super().__init__()
        self.setWindowTitle('Player Performance')
        self.setMinimumSize(600,400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        table = QTableWidget()
        layout.addWidget(table)

        curSor.execute('SELECT * FROM performance_tbl')
        rows = curSor.fetchall()

        table.setColumnCount(10)
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(['ID', 'Goals', 'Saves', 'Assists', 'Clears', 'Fouls', 'Total Passes', 'Complete Passes', 'Passing Accuracy', 'Remarks'])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

class UpdatePerformanceDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt
        self.setWindowTitle('Edit Performance Table')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Player ID'))
        self.player_id = QLineEdit()
        self.player_id.setValidator(QIntValidator())  # integers only
        layout.addWidget(self.player_id)

        self.column_choice = QComboBox()
        self.column_choice.addItems(['Goals Scored', 'Goals Saved', 'Assists', 'Clears', 'Fouls', 'Total Passes', 'Passes Completed', 'Remarks'])
        layout.addWidget(self.column_choice)

        layout.addWidget(QLabel('New Value'))
        self.new_value = QLineEdit()
        layout.addWidget(self.new_value)

        btn_save = QPushButton('Save')
        btn_save.clicked.connect(self.handle_save)        
        layout.addWidget(btn_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)        


    def handle_save(self):
        player_id = self.player_id.text()
        column = self.column_choice.currentText()
        new_value = self.new_value.text()

        if column == 'Goals Scored' :
            self.curSor.execute('UPDATE performance_tbl SET goals_scored = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Goals Saved' :
            self.curSor.execute('UPDATE performance_tbl SET goals_saved = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Assists' :
            self.curSor.execute('UPDATE performance_tbl SET assists = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Clears' :
            self.curSor.execute('UPDATE performance_tbl SET clears = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Fouls' :
            self.curSor.execute('UPDATE performance_tbl SET fouls_commited = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Total Passes' :
            self.curSor.execute('UPDATE performance_tbl SET passes_attempted = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Passes Completed' :
            self.curSor.execute('UPDATE performance_tbl SET passes_completed = %s WHERE player_id = %s', (new_value, player_id))
        elif column == 'Remarks' :
            self.curSor.execute('UPDATE performance_tbl SET remarks = %s WHERE player_id = %s', (new_value, player_id))    
        self.connekt.commit()
        self.player_id.clear()
        self.new_value.clear()

    
class AddPerformanceDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt 
        self.setWindowTitle('Add Record Performance')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Player ID'))
        self.player_id = QLineEdit()
        self.player_id.setValidator(QIntValidator())  # integers only
        layout.addWidget(self.player_id)

        layout.addWidget(QLabel('Goals'))
        self.goals = QLineEdit()
        self.goals.setValidator(QIntValidator())
        layout.addWidget(self.goals)

        layout.addWidget(QLabel('Saves'))
        self.saves = QLineEdit()
        self.saves.setValidator(QIntValidator())
        layout.addWidget(self.saves)

        layout.addWidget(QLabel('Assists'))
        self.assists = QLineEdit()
        self.assists.setValidator(QIntValidator())
        layout.addWidget(self.assists)        

        layout.addWidget(QLabel('Clears'))
        self.clears = QLineEdit()
        self.clears.setValidator(QIntValidator())
        layout.addWidget(self.clears)        

        layout.addWidget(QLabel('Fouls'))
        self.fouls = QLineEdit()
        self.fouls.setValidator(QIntValidator())
        layout.addWidget(self.fouls)

        layout.addWidget(QLabel('Total Passes'))
        self.total_passes = QLineEdit()
        self.total_passes.setValidator(QIntValidator())
        layout.addWidget(self.total_passes)

        layout.addWidget(QLabel('Completed Passes'))
        self.completed_passes = QLineEdit()
        self.completed_passes.setValidator(QIntValidator())
        layout.addWidget(self.completed_passes)

        layout.addWidget(QLabel('Remarks'))
        self.remarks = QLineEdit()
        layout.addWidget(self.remarks)

        btn_save = QPushButton('Save')
        layout.addWidget(btn_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)

        btn_save.clicked.connect(self.handle_save)
    def handle_save(self):
        which_player = self.player_id.text()
        goals_scored = self.goals.text()
        goals_saved = self.saves.text()
        total_assists = self.assists.text()
        clears_done = self.clears.text()
        fouls_commited = self.fouls.text()
        passes_made = self.total_passes.text()
        passes_done = self.completed_passes.text()
        your_remarks = self.remarks.text()        
        for field in [self.goals, self.saves, self.assists, self.clears, self.fouls, self.total_passes, self.completed_passes, self.remarks]:
            field.clear()

        record_performance(self.curSor, self.connekt, which_player, goals_scored, goals_saved, total_assists, clears_done, fouls_commited, passes_made, passes_done, your_remarks)

class DeletePerformanceDialog(QDialog):
    def __init__(self, curSor, connekt):
        super().__init__()
        self.curSor = curSor
        self.connekt = connekt 
        self.setWindowTitle('Remove Performance')

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Player ID'))
        self.player_id = QLineEdit()
        self.player_id.setValidator(QIntValidator())  # integers only
        layout.addWidget(self.player_id)

        btn_save = QPushButton('Save')
        layout.addWidget(btn_save)
        btn_save.setDefault(False)
        btn_save.setAutoDefault(False)        
        btn_save.clicked.connect(self.handle_save)


    def handle_save(self):
        player_id = self.player_id.text()

        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to remove this player's performance?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            remove_performance(self.curSor, self.connekt, player_id)

        for field in [self.player_id]:
            field.clear()


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
curSor.close()
connekt.close()
