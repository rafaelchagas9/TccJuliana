import os
import numpy as np
import argparse
import bancoDeDados
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile

def salvar_midia(midia_processada):
    usuario = midia_processada["usuario"]
    memoria = midia_processada["memoria"]
    midia = midia_processada["midia"]
    palavras = midia_processada["palavras"]
    frequencias = midia_processada["frequencias"]

    # Salva os dados no banco de dados
    bancoDeDados.Memoria(memoria, midia).salvar()

    # Cria diretorio do usuário
    if not os.path.exists("midias"):
        os.mkdir("midias")

    if not os.path.exists("midias/{}".format(usuario)):
        os.mkdir("midias/{}".format(usuario))

    # Limpa o diretório de midias do usuário
    for arquivo in os.listdir("midias/{}".format(usuario)):
        os.remove("midias/{}/{}".format(usuario, arquivo))
        
    # Salva a imagem e o arquivo de áudio
    os.rename("memoria.png", "midias/{}/{}_memoria.png".format(usuario, usuario))
    os.rename("memoria.wav", "midias/{}/{}_memoria.wav".format(usuario, usuario))
    os.rename("memoria.txt", "midias/{}/{}_memoria.txt".format(usuario, usuario))

    # Salva os dados no arquivo de texto
    with open("palavras.txt", "w", encoding="utf-8") as f:
        for palavra, frequencia in zip(palavras, frequencias):
            f.write("{}: {}\n".format(palavra, frequencia))

    # Salva a imagem e o arquivo de áudio
    os.rename("palavras.txt", "midias/{}/{}_palavras.txt".format(usuario, usuario))


def processar_memoria():
    memoria = args.memoria
    usuario = args.usuario
    midia = args.midia

    # Abre o arquivo de memória (txt) e relaciona trechos da midia com a memória
    with open("memoria.txt", "r", encoding="utf-8") as f:
        conteudo = f.readlines()
        conteudo = [x.strip() for x in conteudo]
    
    # Cria um dicionário com as palavras e suas respectivas frequências
    palavras = []
    for linha in conteudo:
        palavras += linha.split(" ")

    # associa as palavras com as frequências
    palavras = np.array(palavras)
    palavras, frequencias = np.unique(palavras, return_counts=True)
    palavras = palavras[np.argsort(frequencias)[::-1]]
    frequencias = frequencias[np.argsort(frequencias)[::-1]]

    # Cria um gráfico de barras com as palavras mais frequentes
    plt.bar(palavras[:10], frequencias[:10])
    plt.xlabel("Palavras")
    plt.ylabel("Frequência")
    plt.title("Emoções mais frequentes na memória")
    if args.exibir_grafico:
        plt.show()
        
    plt.savefig("memoria.png")

    # Cria uma representação sonora da memória e salva como arquivo de áudio
    rate = 44100
    duration = len(conteudo) * 1
    t = np.linspace(0, duration, rate * duration)
    audio = np.zeros(rate * duration)
    for i, linha in enumerate(conteudo):
        audio[i * rate:(i + 1) * rate] = np.sin(2 * np.pi * 440 * t[i * rate:(i + 1) * rate])
    wavfile.write("memoria.wav", rate, audio)

    return {"usuario": usuario, "memoria": memoria, "midia": midia, "palavras": palavras[:10], "frequencias": frequencias[:10]}


def construir_mapa_de_memorias():
    memoria_processada = processar_memoria()
    salvar_midia(memoria_processada)


def registrar_usuario():
    usuario = args.usuario
    bancoDeDados.Usuario(usuario).salvar()



def main():
    print("Registrando memória: {} \nAssociada ao usuário: {}\nMídia: {}".format(args.memoria, args.usuario, args.midia))
    registrar_usuario()
    construir_mapa_de_memorias()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-u", "--usuario", help="Identificador do usuário")
    args.add_argument("-m", "--midia", help="Mídia a ser associada com a memória (foto, vídeo, áudio)")
    args.add_argument("-mem", "--memoria", help="Memória a ser registrada")
    args.add_argument("-g", "--exibir_grafico", help="Exibir gráfico de emoções mais frequentes", action="store_true")
    args = args.parse_args()

    if args.usuario and args.memoria and args.midia:
        main()
    else:
        print("Por favor, insira os argumentos obrigatórios")