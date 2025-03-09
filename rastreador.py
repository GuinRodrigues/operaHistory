import os
import sqlite3
import shutil
import datetime

def ver_historico(caminho):
    if not os.path.exists(caminho):
        print("O arquivo de histórico não foi encontrado.")
        exit()

    copia_temporaria = "History_copy.db"
    shutil.copy2(caminho, copia_temporaria)

    conn = sqlite3.connect(copia_temporaria)
    cursor = conn.cursor()

    cursor.execute("SELECT url, last_visit_time FROM urls ORDER BY last_visit_time DESC")
    return conn, cursor

def converter_tempo(tempo):
    if tempo == 0:
        return "desconhecido"
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=tempo)
    return epoch_start + delta

def processar_historico(cursor, data_do_cliente):
    historico = []

    for url, tempo in cursor.fetchall():
        data_visita = converter_tempo(tempo)

        if data_visita != "desconhecido":
            if data_visita.date() == data_do_cliente:
                hora_visita = data_visita.strftime("%H:%M:%S")
                historico.append((hora_visita, url))
    return historico

def exibir_historico(historico, data_do_cliente):
    if historico:
        print(f"Sites visitados em {data_do_cliente}:\n")
        for hora, url in historico:
            print(f"{hora} - Hora: {url}")
    else:
        print(f"Nenhum site visitado em {data_do_cliente}.")

def pedir_data():
    data_do_cliente = input("Digite a data que deseja verificar (AAAA-MM-DD): ")
    try:
        data_do_cliente = datetime.datetime.strptime(data_do_cliente, "%Y-%m-%d").date()
    except ValueError:
        print("Data inválida.")
        exit()
    return data_do_cliente

def main():
    HISTORY_PATH = os.path.expanduser(r"~\AppData\Roaming\Opera Software\Opera GX Stable\History")
    conn, cursor = ver_historico(HISTORY_PATH)

    while True:
        data_documento = pedir_data()
        if data_documento is None:
            break
        historico = processar_historico(cursor, data_documento)
        exibir_historico(historico, data_documento)
    
    conn.close()
    os.remove("History_copy.db")

if __name__ == "__main__":
    main()
        
