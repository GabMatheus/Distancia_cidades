import requests
import csv
import sqlite3
from unidecode import unidecode
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# Variável global para contar operações
contador_operacoes = 0
interromper_calculo = False  

def obter_distancia(cidade_origem, cidade_destino, api_key):
    global contador_operacoes
    cidade_origem = unidecode(cidade_origem)
    cidade_destino = unidecode(cidade_destino)
    
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={cidade_origem}&destinations={cidade_destino}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    try:
        if data['status'] == 'OK' and data['rows']:
            elements = data['rows'][0].get('elements', [])
            if elements:
                distancia_texto = elements[0].get('distance', {}).get('text', 'Distância não encontrada')
            else:
                distancia_texto = "Não há elementos de distância para as cidades informadas."
        else:
            distancia_texto = "Não foi possível obter a distância entre as cidades. Verifique os nomes das cidades."
    except (KeyError, IndexError):
        distancia_texto = "Erro ao processar a resposta da API."
    
    contador_operacoes += 1  
    return distancia_texto

def obter_cidades_db():
    conn = sqlite3.connect('cidades.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM cidades")
    cidades = cursor.fetchall()
    conn.close()
    return [cidade[0] for cidade in cidades]

def salvar_distancias_csv(cidade_origem, api_key, progress_callback):
    cidades_destino = obter_cidades_db()
    
    with open('distancias.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cidade Origem', 'Cidade Destino', 'Distancia'])
        
        for idx, cidade_destino in enumerate(cidades_destino):
            if cidade_origem != cidade_destino:
                if interromper_calculo: 
                    break

                distancia = obter_distancia(cidade_origem, cidade_destino, api_key)
                cidade_origem_sem_acentos = unidecode(cidade_origem)
                cidade_destino_sem_acentos = unidecode(cidade_destino)
                writer.writerow([cidade_origem_sem_acentos, cidade_destino_sem_acentos, distancia])
                
                # Atualiza a barra de progresso
                progress_callback.emit(idx + 1, len(cidades_destino))
                print(f"Distância calculada para {cidade_destino}. Total de operações realizadas: {contador_operacoes}")

class WorkerThread(QThread):
    progress_update = pyqtSignal(int, int)
    
    def __init__(self, cidade_origem, api_key):
        super().__init__()
        self.cidade_origem = cidade_origem
        self.api_key = api_key

    def run(self):
        global interromper_calculo
        interromper_calculo = False
        salvar_distancias_csv(self.cidade_origem, self.api_key, self.progress_update)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora de Distância entre Cidades')
        self.setGeometry(100, 100, 400, 350)
        
        self.layout = QVBoxLayout()
        
        # Caixa de entrada para cidade origem
        self.origem_input = QLineEdit(self)
        self.origem_input.setPlaceholderText('Digite a cidade de origem/Estado Ex: Ibiá/MG')
        self.layout.addWidget(self.origem_input)
        
        # Caixa de entrada para cidade destino
        self.destino_input = QLineEdit(self)
        self.destino_input.setPlaceholderText('Digite a cidade de destino/Estado Ex: Ibiá/MG')
        self.layout.addWidget(self.destino_input)
        
        # Botão para calcular distância
        self.calcular_button = QPushButton('Calcular Distância', self)
        self.calcular_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.calcular_button.clicked.connect(self.calcular_distancia)
        self.layout.addWidget(self.calcular_button)
        
        # Caixa de texto para exibir o resultado
        self.resultado_text = QTextEdit(self)
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet("font-size: 14px; color: #333; padding: 10px;")
        self.layout.addWidget(self.resultado_text)
        
        # Barra de progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)
        
        # Botão para calcular e salvar distâncias para todas as cidades
        self.calcular_todas_button = QPushButton('Calcular Distâncias para todas as cidades', self)
        self.calcular_todas_button.setStyleSheet("background-color: #FF5722; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.calcular_todas_button.clicked.connect(self.calcular_distancia_todas)
        self.layout.addWidget(self.calcular_todas_button)
        
        # Botão para interromper o cálculo
        self.interromper_button = QPushButton('Interromper e Salvar Progresso', self)
        self.interromper_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.interromper_button.clicked.connect(self.interromper_calculo)
        self.layout.addWidget(self.interromper_button)
        
        self.setLayout(self.layout)

    def calcular_distancia(self):
        cidade_origem = self.origem_input.text()
        cidade_destino = self.destino_input.text()
        if cidade_origem and cidade_destino:
            api_key = "chave API maps" 
            distancia = obter_distancia(cidade_origem, cidade_destino, api_key)
            self.resultado_text.setText(f"A distância entre {cidade_origem} e {cidade_destino} é {distancia}.\n")
            self.resultado_text.append(f"Total de operações realizadas: {contador_operacoes}")

    def calcular_distancia_todas(self):
        cidade_origem = self.origem_input.text()
        if cidade_origem:
            api_key = "Chave api maps"  
            self.worker = WorkerThread(cidade_origem, api_key)
            self.worker.progress_update.connect(self.atualizar_progress_bar)
            self.worker.start()

    def atualizar_progress_bar(self, current, total):
        if total > 0:
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)
            self.resultado_text.setText(f"Calculando... ({progress}%)")
        
    def interromper_calculo(self):
        global interromper_calculo
        interromper_calculo = True  # Interrompe o cálculo
        self.resultado_text.setText("Cálculo interrompido. Progresso salvo até o ponto atual.")
        self.progress_bar.setValue(0)  # Reseta a barra de progresso

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
