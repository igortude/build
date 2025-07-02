import sqlite3
from datetime import datetime
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
import sys

# Função para transferir e limpar os dados
def transferir_e_limpar(conn, cursor):
    """Transfere dados de dados_semana para historico_dados e limpa dados_semana."""
    try:
        cursor.execute("""
            INSERT INTO historico_dados (aluno, prescricao, observacao, dia, turno, check_in, data_criacao)
            SELECT aluno, prescricao, observacao, dia, turno, check_in, data_criacao
            FROM dados_semana
        """)
        conn.commit()
        cursor.execute("DELETE FROM dados_semana")
        conn.commit()
    except Exception as e:
        print(f"Erro ao processar o banco de dados: {e}")
        raise

class LoadingDialog(QDialog):
    """Janela de loading exibida durante o backup."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processando...")
        self.setModal(True)
        layout = QVBoxLayout()
        self.label = QLabel("Fazendo backup e transferindo arquivos...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedSize(300, 100)

def encerrar_com_backup(parent, conn, cursor):
    """Verifica se é sábado e executa o backup antes de encerrar."""
    from PySide6.QtWidgets import QApplication

    # Verificar o dia atual
    hoje = datetime.now()
    dia_atual = hoje.strftime('%A')
    dias_semana = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    if dias_semana.get(dia_atual) == 'Sábado':
        loading_dialog = LoadingDialog(parent)
        loading_dialog.show()
        QApplication.processEvents()

        transferir_e_limpar(conn, cursor)

        loading_dialog.close()
        QMessageBox.information(parent, "Concluído", "Backup e limpeza concluídos!")
    else:
        print(f"Hoje é {dias_semana.get(dia_atual)}. Backup e limpeza não realizados (executados apenas aos sábados).")

# Para teste standalone (opcional)
#if __name__ == "__main__":
#    from PySide6.QtWidgets import QApplication, QMainWindow
#    app = QApplication(sys.argv)
#    window = QMainWindow()
#    conn = sqlite3.connect('/nolimits_DB.db')  # Conexão para teste
#    cursor = conn.cursor()
#    encerrar_com_backup(window, conn, cursor)
#    conn.close()
#    sys.exit(app.exec())