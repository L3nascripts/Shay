import random
import os

from shay3 import (
    modo_academico_arabe,
    modo_academico_persa,
    modo_academico_urdu,
    transliterar
)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def normalizar_vogais(texto):
    return (
        texto.replace('ā', 'aa')
             .replace('ī', 'ii')
             .replace('ū', 'uu')
             .strip().lower()
    )


def escolher_idioma():
    print("1 - Árabe")
    print("2 - Persa")
    print("3 - Urdu")
    escolha = input("Escolha o idioma: ").strip()

    if escolha == '1':
        return modo_academico_arabe, "Árabe"
    elif escolha == '2':
        return modo_academico_persa, "Persa"
    elif escolha == '3':
        return modo_academico_urdu, "Urdu"
    else:
        print("Opção inválida.")
        return None, None


def quebrar_em_unidades(translit):
    grupos = ['kh', 'gh', 'sh', 'th', 'dh', 'ch', 'zh', 'DH']
    unidades = []
    i = 0
    while i < len(translit):
        if translit[i:i+2] in grupos:
            unidades.append(translit[i:i+2])
            i += 2
        else:
            unidades.append(translit[i])
            i += 1
    return unidades


def jogo_normal(mapa, idioma):
    letras = list(mapa.keys())
    pontos = 0
    total = 10

    for rodada in range(1, total + 1):
        letra = random.choice(letras)
        correta = mapa[letra]

        alternativas = set([correta])
        while len(alternativas) < 4:
            alt = random.choice(list(mapa.values()))
            if alt != correta:
                alternativas.add(alt)

        alternativas = list(alternativas)
        random.shuffle(alternativas)

        print(f"\nRodada {rodada}/{total}")
        print(f"Qual é a transliteração de '{letra}'?")
        for i, alt in enumerate(alternativas, 1):
            print(f"{i} - {alt}")

        tentativa = input("Sua resposta (1-4): ").strip().lower()

        if tentativa not in ['1', '2', '3', '4']:
            print("Resposta inválida.")
            continue

        tentativa = int(tentativa) - 1

        if alternativas[tentativa] == correta:
            print("Correto!")
            pontos += 1
        else:
            print(f"Errado. A correta era '{correta}'.")

    percentual = (pontos / total) * 100
    print(f"\nVocê fez {pontos}/{total} pontos. ({percentual:.1f}% de acerto)")
    input("Pressione Enter para voltar ao menu...")


def jogo_reverso(mapa, idioma):
    letras = list(mapa.keys())
    valores = list(mapa.values())
    pontos = 0
    total = 10

    for rodada in range(1, total + 1):
        correta = random.choice(valores)
        letra_correta = [k for k, v in mapa.items() if v == correta][0]

        alternativas = set([letra_correta])
        while len(alternativas) < 4:
            alt = random.choice(letras)
            if alt != letra_correta:
                alternativas.add(alt)

        alternativas = list(alternativas)
        random.shuffle(alternativas)

        print(f"\nRodada {rodada}/{total}")
        print(f"Qual é a letra para a transliteração '{correta}'?")
        for i, alt in enumerate(alternativas, 1):
            print(f"{i} - {alt}")

        tentativa = input("Sua resposta (1-4): ").strip().lower()

        if tentativa not in ['1', '2', '3', '4']:
            print("Resposta inválida.")
            continue

        tentativa = int(tentativa) - 1

        if alternativas[tentativa] == letra_correta:
            print("Correto!")
            pontos += 1
        else:
            print(f"Errado. A correta era '{letra_correta}'.")

    percentual = (pontos / total) * 100
    print(f"\nVocê fez {pontos}/{total} pontos. ({percentual:.1f}% de acerto)")
    input("Pressione Enter para voltar ao menu...")


def jogo_memoria(mapa, idioma):
    limpar_tela()
    print(f"Jogo da Memória - {idioma}")

    pares = random.sample(list(mapa.items()), 6)
    cartas = []
    for letra, translit in pares:
        cartas.append(('L', letra))
        cartas.append(('T', translit))

    random.shuffle(cartas)
    visivel = ['[?]' for _ in cartas]
    encontrados = []
    tentativas = 0

    while len(encontrados) < len(cartas):
        limpar_tela()
        print("\n".join(f"{i + 1}: {visivel[i]}" for i in range(len(cartas))))
        print("\nDigite 'sair' para voltar ao menu.")

        c1 = input("\nEscolha a primeira carta (número): ").strip()
        if c1.lower() == 'sair':
            break
        c2 = input("Escolha a segunda carta (número): ").strip()
        if c2.lower() == 'sair':
            break

        if not (c1.isdigit() and c2.isdigit()):
            print("Entrada inválida.")
            input("Enter para continuar...")
            continue

        c1, c2 = int(c1) - 1, int(c2) - 1

        if c1 == c2 or c1 not in range(len(cartas)) or c2 not in range(len(cartas)):
            print("Escolha inválida.")
            input("Enter para continuar...")
            continue

        visivel[c1] = f"[{cartas[c1][1]}]"
        visivel[c2] = f"[{cartas[c2][1]}]"
        limpar_tela()
        print("\n".join(f"{i + 1}: {visivel[i]}" for i in range(len(cartas))))

        l1, v1 = cartas[c1]
        l2, v2 = cartas[c2]

        tentativas += 1

        if (l1 != l2) and (
            (l1 == 'L' and mapa[v1] == v2) or (l1 == 'T' and mapa[v2] == v1)
        ):
            print("Par correto!")
            encontrados += [c1, c2]
        else:
            print("Não é um par.")
            visivel[c1] = '[?]'
            visivel[c2] = '[?]'

        input("Enter para continuar...")

    if len(encontrados) == len(cartas):
        percentual = (len(pares) / tentativas) * 100 if tentativas > 0 else 0
        print(f"\nVocê encontrou todos os pares em {tentativas} tentativas.")
        print(f"Percentual de acerto: {percentual:.1f}%")
    input("Pressione Enter para voltar ao menu...")


def jogo_palavras():
    mapa = modo_academico_arabe

    palavras = {
        'acucar': 'سكر', 'califa': 'خليفة', 'azeite': 'زيت', 'almofada': 'مخدة',
        'sofa': 'صوفا', 'pijama': 'پايجامه', 'xadrez': 'الشطرنج', 'quiosque': 'كشك',
        'gengibre': 'زنجبیل', 'jantar': 'چاشت', 'acafrao': 'زعفران'
    }

    origem = {p: 'Árabe' for p in palavras}
    origem['sofa'] = 'Persa'
    origem['pijama'] = 'Persa'
    origem['jantar'] = 'Persa'
    origem['gengibre'] = 'Persa'
    origem['quiosque'] = 'Persa'

    while True:
        print("\nModo de jogo:")
        print("1 - Usar Transliteração")
        print("2 - Usar Escrita Real (alfabeto árabe/persa)")
        modo = input("Escolha (1 ou 2): ").strip()

        if modo in ['1', '2']:
            break
        else:
            print("Opção inválida. Escolha 1 ou 2.")

    lista = list(palavras.items())
    random.shuffle(lista)

    rodadas = min(10, len(lista))
    pontos = 0

    for i in range(rodadas):
        palavra, escrita = lista[i]
        translit = transliterar(escrita).replace(' ', '')
        origem_palavra = origem.get(palavra, "Desconhecida")

        unidades = quebrar_em_unidades(translit)
        random.shuffle(unidades)
        letras_embaralhadas = ' '.join(unidades)

        print(f"\nRodada {i + 1}/{rodadas}")
        print(f"Palavra: {palavra.upper()}")
        print(f"Origem: {origem_palavra}")
        print(f"Letras na transliteração (embaralhadas): {letras_embaralhadas}")

        resposta = input("Digite como ficaria no idioma alvo (ou 'sair' para encerrar): ").strip()

        if resposta.lower() == 'sair':
            break

        correto = escrita
        correto_translit = translit

        if modo == '1':
            if normalizar_vogais(resposta) == normalizar_vogais(correto_translit):
                print("Correto!")
                pontos += 1
            else:
                print(f"Errado. A resposta correta era: {correto_translit}")
        else:
            if normalizar_vogais(resposta) == normalizar_vogais(correto):
                print("Correto!")
                pontos += 1
            else:
                print(f"Errado. A resposta correta era: {correto}")

        print(f"Como fica no alfabeto: {correto}")

    percentual = (pontos / rodadas) * 100 if rodadas > 0 else 0
    print(f"\nVocê acertou {pontos}/{rodadas} palavras.")
    print(f"Percentual de acerto: {percentual:.1f}%")
    input("Pressione Enter para voltar ao menu...")


def menu_principal():
    while True:
        limpar_tela()
        print("Jogo de Transliteração")
        print("1 - Jogo Normal (Letra → Transliteração)")
        print("2 - Modo Reverso (Transliteração → Letra)")
        print("3 - Jogo da Memória")
        print("4 - Jogo de Palavras")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao in ['1', '2', '3']:
            mapa, idioma = escolher_idioma()
            if not mapa:
                input("Pressione Enter para continuar...")
                continue

            if opcao == '1':
                jogo_normal(mapa, idioma)
            elif opcao == '2':
                jogo_reverso(mapa, idioma)
            elif opcao == '3':
                jogo_memoria(mapa, idioma)

        elif opcao == '4':
            jogo_palavras()

        elif opcao == '5':
            print("Saindo do jogo...")
            break
        else:
            input("Opção inválida. Pressione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()
