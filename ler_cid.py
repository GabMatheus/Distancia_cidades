import requests
import csv
import tkinter as tk
from tkinter import filedialog
from unidecode import unidecode

# Variável global para contar operações
contador_operacoes = 0

def obter_distancia(cidade_origem, cidade_destino, api_key):
    global contador_operacoes
    cidade_origem = unidecode(cidade_origem)
    cidade_destino = unidecode(cidade_destino)
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={cidade_origem}&destinations={cidade_destino}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    try:
        distancia_texto = data['rows'][0]['elements'][0]['distance']['text']
    except KeyError:
        distancia_texto = "Nao foi possivel obter a distancia."
    
    contador_operacoes += 1  
    return distancia_texto

def calcular_e_mostrar_distancia_individual(api_key):
    cidade_origem = input("Digite a cidade de origem/Estado Ex: Ibiá/MG ('sair' para voltar ao menu): ")
    if cidade_origem.lower() == 'sair':
        return
    cidade_destino = input("Digite a cidade de destino/Estado Ex: Ibiá/MG: ")
    distancia = obter_distancia(cidade_origem, cidade_destino, api_key)
    print(f"A distância entre {cidade_origem} e {cidade_destino} é {distancia}.\n")
    print(f"Cidade {contador_operacoes} ok - isso pode demorar um pouco...")

def calcular_e_mostrar_distancia_arquivo(api_key):
    global contador_operacoes
    nome_arquivo_cidades = filedialog.askopenfilename(title="Selecione o arquivo de cidades", filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")))
    if not nome_arquivo_cidades:
        print("Nenhum arquivo selecionado.")
        return
    
    cidades_destino = []
    with open(nome_arquivo_cidades, 'r', encoding='utf-8') as file:  
        for linha in file:
            cidade = linha.strip()  
            cidades_destino.append(cidade)
    
    cidade_origem = input("Digite a cidade de origem/Estado Ex: Ibiá/MG ('sair' para encerrar): ")
    if cidade_origem.lower() == 'sair':
        return
    with open('distancias.csv', mode='w', newline='', encoding='utf-8') as file:  
        writer = csv.writer(file)
        writer.writerow(['Cidade Origem', 'Cidade Destino', 'Distancia'])
        for cidade_destino in cidades_destino:
            if cidade_origem != cidade_destino:
                distancia = obter_distancia(cidade_origem, cidade_destino, api_key)
                cidade_origem_sem_acentos = unidecode(cidade_origem)
                cidade_destino_sem_acentos = unidecode(cidade_destino)
                writer.writerow([cidade_origem_sem_acentos, cidade_destino_sem_acentos, distancia])
                print(f"Cidade {contador_operacoes} ok")
        contador_operacoes += 1  

def menu():
    api_key = "A CHAVE DA API QUE VC SOLICITA"  # Substitua pela sua chave de API do Google Maps
    root = tk.Tk()
    root.withdraw()  # Esconde a janela do Tkinter
    
    while True:
        print("\nMENU:")
        print("1. Calcular e mostrar distância entre duas cidades")
        print("2. Salvar em um arquivo csv a distância entre uma cidade de origem para todas as outras cidades do Brasil")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            calcular_e_mostrar_distancia_individual(api_key)
        elif opcao == '2':
            calcular_e_mostrar_distancia_arquivo(api_key)
        elif opcao == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")
    print(f"Total de operações realizadas: {contador_operacoes}")

if __name__ == "__main__":
    menu()
