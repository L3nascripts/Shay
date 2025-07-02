import os

# ===== VARIÁVEIS GLOBAIS =====
usar_harakat = True
usar_fonetico = False

# ===== FUNÇÕES AUXILIARES =====

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

# ===== DICIONÁRIOS DE TRANSLITERAÇÃO =====

modo_academico_arabe = {
    'ا': 'ā', 'أ': 'a2', 'إ': 'i2', 'آ': 'aa2', 'ء': '2', 'ؤ': 'u2', 'ئ': '2y',
    'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'H', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh',
    'ص': 'S', 'ض': 'D', 'ط': 'T', 'ظ': 'DH', 'ع': '3', 'غ': 'gh',
    'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n',
    'ه': 'h', 'و': 'ū', 'ي': 'ī', 'ى': 'ā', 'ة': 'ah',
    'َ': 'a', 'ِ': 'i', 'ُ': 'u', 'ً': 'an', 'ٍ': 'in', 'ٌ': 'un',
    'ْ': '', 'ّ': '',
}

modo_academico_persa = modo_academico_arabe.copy()
modo_academico_persa.update({
    'پ': 'p', 'چ': 'ch', 'ژ': 'zh', 'گ': 'g', 'ی': 'ī', 'ک': 'k'
})

modo_academico_urdu = modo_academico_persa.copy()
modo_academico_urdu.update({
    'ٹ': 'T', 'ڈ': 'D', 'ڑ': 'R', 'ں': 'ñ', 'ھ': 'h', 'ہ': 'h',
    'ے': 'e', 'ۂ': 'ah'
})

# ===== DICIONÁRIOS REVERSOS =====


translit_reverso = {
    '2aa': 'آ', '2a': 'أ', '2i': 'إ', '2u': 'ؤ', '2y': 'ئ', '2': 'ء',

    'aa': 'ا', 'ii': 'ي', 'uu': 'و', 'ā': 'ا', 'ī': 'ي', 'ū': 'و',
    'a': 'َ', 'i': 'ِ', 'u': 'ُ',

    'sh': 'ش', 'th': 'ث', 'dh': 'ذ', 'ch': 'چ', 'zh': 'ژ',
    'gh': 'غ', 'kh': 'خ',

    'H': 'ح', 'S': 'ص', 'D': 'ض', 'T': 'ط', 'DH': 'ظ',

    'b': 'ب', 't': 'ت', 'j': 'ج', 'd': 'د', 'r': 'ر', 'z': 'ز', 's': 'س',
    'f': 'ف', 'q': 'ق', 'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن', 'h': 'ه',
    'w': 'و', 'y': 'ي', 'g': 'گ', 'p': 'پ', '3': 'ع'
}


translit_reverso_persa = translit_reverso.copy()
translit_reverso_persa.update({'y': 'ی', 'k': 'ک'})

translit_reverso_urdu = translit_reverso_persa.copy()
translit_reverso_urdu.update({
    'T': 'ٹ', 'D': 'ڈ', 'R': 'ڑ', 'ñ': 'ں', 'e': 'ے', 'ah': 'ۂ',
    'ii': 'ی', 'ī': 'ی', 'y': 'ی'
})

# ===== EXCEÇÕES =====

excecoes_transliteracao = {
    'urduu': 'اردو',
    'allahu': 'اللهُ',
    'bismillah': 'بسم الله',
    'alhamdulillah': 'الحمد لله',
    'mashaallah': 'ما شاء الله',
    'inshallah': 'إن شاء الله',
    'subhanallah': 'سبحان الله'
}

# ===== ORDENAÇÃO =====

chaves_reversas = sorted(translit_reverso, key=lambda x: -len(x))
chaves_reversas_persa = sorted(translit_reverso_persa, key=lambda x: -len(x))
chaves_reversas_urdu = sorted(translit_reverso_urdu, key=lambda x: -len(x))

# ===== NÚMEROS =====

numeros_arabes = {str(i): chr(0x0660 + i) for i in range(10)}
numeros_latinos = {v: k for k, v in numeros_arabes.items()}

# ===== FUNÇÕES DE TRANSLITERAÇÃO =====

def transliterar(texto):
    resultado = ''
    idioma = detectar_idioma(texto)

    if idioma == 'Urdu':
        mapa = modo_academico_urdu
    elif idioma == 'Persa':
        mapa = modo_academico_persa
    else:
        mapa = modo_academico_arabe

    pular = False
    for i, caractere in enumerate(texto):
        if pular:
            pular = False
            continue
        if caractere == 'ة':
            if i == len(texto) - 1 or texto[i + 1] in ' \n\t':
                resultado += 'ah'
            else:
                resultado += 'h'
        elif caractere == 'ّ':
            continue
        elif i + 1 < len(texto) and texto[i + 1] == 'ّ':
            base = mapa.get(caractere, caractere)
            resultado += base * 2
            pular = True
        else:
            base = mapa.get(caractere, caractere)
            resultado += base

    if usar_fonetico:
        resultado = resultado.replace('ā', 'aa').replace('ī', 'ii').replace('ū', 'uu')

    return resultado


def transliterar_reverso(texto, modo='arabe'):
    texto_limp = texto  # <<< CORREÇÃO: Removido .lower()

    if usar_fonetico:
        texto_limp = texto_limp.replace('aa', 'ā').replace('ii', 'ī').replace('uu', 'ū')

    if texto_limp.lower() in excecoes_transliteracao:
        return excecoes_transliteracao[texto_limp.lower()]

    if texto_limp.lower() == "allah":
        return 'ﷲ'

    if texto_limp.endswith('aa'):
        texto_limp = texto_limp[:-2] + 'ā_maqsurah'

    if modo == 'arabe':
        chaves = chaves_reversas
        tabela = translit_reverso
    elif modo == 'persa':
        chaves = chaves_reversas_persa
        tabela = translit_reverso_persa
    elif modo == 'urdu':
        chaves = chaves_reversas_urdu
        tabela = translit_reverso_urdu
    else:
        return texto

    resultado = ''
    i = 0
    while i < len(texto_limp):
        if texto_limp[i:i + 11] == 'ā_maqsurah':
            resultado += 'ى'
            i += 11
            continue
        if texto_limp[i:i + 2] == 'ah' and (i + 2 == len(texto_limp) or texto_limp[i + 2] in ' \n\t'):
            resultado += 'ة'
            i += 2
            continue

        encontrou = False
        for chave in chaves:
            if texto_limp[i:i + len(chave)] == chave:
                if texto_limp[i:i + len(chave) * 2] == chave * 2:
                    resultado += tabela[chave] + 'ّ'
                    i += len(chave) * 2
                else:
                    valor = tabela[chave]
                    if valor in ['َ', 'ِ', 'ُ'] and not usar_harakat:
                        pass
                    else:
                        resultado += valor
                    i += len(chave)
                encontrou = True
                break
        if not encontrou:
            resultado += texto_limp[i]
            i += 1
    return resultado

# ===== INSERÇÃO MANUAL DE HARAKAT =====

def inserir_harakat_interativo(texto):
    resultado = ''
    consoantes = set('ابتثجحخدذرزسشصضطظعغفقكلمنهوىيپچژگٹڈڑںھہ')

    i = 0
    while i < len(texto):
        char = texto[i]
        resultado += char

        if char in consoantes:
            proximo = texto[i + 1] if i + 1 < len(texto) else ''
            if proximo not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']:
                print(f"\nLetra '{char}' sem harakāt após ela.")
                escolha = input("Adicionar: (a) Fatha, (i) Kasra, (u) Damma ou (s) Sukun? ").lower()

                if escolha == 'a':
                    resultado += 'َ'
                elif escolha == 'i':
                    resultado += 'ِ'
                elif escolha == 'u':
                    resultado += 'ُ'
                elif escolha == 's':
                    resultado += 'ْ'
                else:
                    print("Opção inválida. Nenhum harakāt adicionado.")

        i += 1

    print("\nTexto final com harakāt inseridos:")
    print(resultado)
    return resultado

# ===== CONVERSÃO DE NÚMEROS =====

def converter_numeros_para_arabe(texto):
    return ''.join(numeros_arabes.get(c, c) for c in texto)

def converter_numeros_para_latino(texto):
    return ''.join(numeros_latinos.get(c, c) for c in texto)

# ===== DETECÇÃO DE IDIOMA =====

def detectar_idioma(texto):
    texto = texto.strip()
    if not texto:
        return 'Desconhecido'

    caracteres_urdu = set('ٹڈڑںےۂ')
    caracteres_persa = set('پچژگکیی')
    caracteres_arabe = set('ابتثجحخدذرزسشصضطظعغفقكلمنهوىيةءآأإؤئ')

    cont_urdu = sum(1 for c in texto if c in caracteres_urdu)
    cont_persa = sum(1 for c in texto if c in caracteres_persa)
    cont_arabe = sum(1 for c in texto if c in caracteres_arabe)

    if cont_urdu > 0:
        return 'Urdu'
    elif cont_persa > 0:
        return 'Persa'
    elif cont_arabe > 0:
        return 'Árabe'
    else:
        return 'Desconhecido'

# ===== MAPA DE TRANSLITERAÇÃO =====

def mostrar_mapa():
    limpar_tela()
    print("=== Mapa de Transliteração ===\n")

    print("Letras do Alfabeto Árabe:")
    for letra, translit in modo_academico_arabe.items():
        print(letra, "→", translit)

    print("\nLetras exclusivas do Persa:")
    letras_persa = ['پ', 'چ', 'ژ', 'گ', 'ک', 'ی']
    for letra in letras_persa:
        translit = modo_academico_persa.get(letra, "")
        print(letra, "→", translit)

    print("\nLetras exclusivas do Urdu:")
    letras_urdu = ['ٹ', 'ڈ', 'ڑ', 'ں', 'ھ', 'ہ', 'ے', 'ۂ']
    for letra in letras_urdu:
        translit = modo_academico_urdu.get(letra, "")
        print(letra, "→", translit)

    print("\nHarakāt (Sinais de Vogais e Outros):")
    print("َ → a (Fatha)")
    print("ِ → i (Kasra)")
    print("ُ → u (Damma)")
    print("ْ → sukun (sem vogal)")
    print("ّ → shadda (duplica consoante)")
    print("ً → an (tanwin fatha)")
    print("ٍ → in (tanwin kasra)")
    print("ٌ → un (tanwin damma)")

    print("\nNúmeros:")
    for num, arabe in numeros_arabes.items():
        print(num, "→", arabe)

    print("\n===========================")

# ===== SALVAR HISTÓRICO =====

def salvar_historico(historico):
    nome = input("Nome do arquivo (sem extensão): ").strip() or "historico_transliteracao"
    with open(nome + ".txt", "w", encoding="utf-8") as f:
        for idx, item in enumerate(historico, 1):
            if len(item) == 3:
                entrada, saida, idioma_interno = item
                idiomas = {'arabe': 'Árabe', 'persa': 'Persa', 'urdu': 'Urdu'}
                idioma = idiomas.get(idioma_interno, 'Desconhecido')
                tag = "Idioma selecionado"
            else:
                entrada, saida = item
                idioma = detectar_idioma(entrada if any(ord(c) > 127 for c in entrada) else saida)
                tag = "Idioma detectado"
            f.write(f"{idx}. Original: {entrada}\n")
            f.write(f"   Resultado: {saida}\n")
            f.write(f"   {tag}: {idioma}\n\n")
    print(f"Histórico salvo como {nome}.txt")

# ===== MENU PRINCIPAL =====

def principal():
    global usar_harakat, usar_fonetico
    historico = []

    while True:
        limpar_tela()
        print("=== Bem-vind@ ao Shay 3.1 ===")
        print("1 - Latino → Árabe/Persa/Urdu")
        print("2 - Árabe/Persa/Urdu → Latino")
        print("3 - Latino → Números Árabes")
        print("4 - Números Árabes → Latino")
        print("5 - Ver mapa de transliteração")
        print(f"6 - Ativar/Desativar Harakāt (atual: {'Ativado' if usar_harakat else 'Desativado'})")
        print(f"7 - Ativar/Desativar Modo Fonético (atual: {'Ativado' if usar_fonetico else 'Desativado'})")
        print("8 - Sair")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            print("1 - Árabe\n2 - Persa\n3 - Urdu")
            idioma = input("Escolha o idioma: ").strip()
            modo = {'1': 'arabe', '2': 'persa', '3': 'urdu'}.get(idioma)
            if not modo:
                print("Opção inválida.")
                pausar()
                continue
            texto = input("Digite o texto em latino: ").strip()
            resultado = transliterar_reverso(texto, modo=modo)
            print("\n→ Resultado:", resultado)
            historico.append((texto, resultado, modo))
            pausar()

        elif opcao == '2':
            texto = input("Digite texto em árabe/persa/urdu: ").strip()

            inserir = input("Deseja inserir manualmente os harakāt? (s/n): ").lower()
            if inserir == 's':
                texto = inserir_harakat_interativo(texto)

            idioma = detectar_idioma(texto)
            print(f"\n→ Idioma detectado: {idioma}")
            resultado = transliterar(texto)
            print("\n→ Resultado:", resultado)
            historico.append((texto, resultado))
            pausar()

        elif opcao == '3':
            texto = input("Digite números ou texto com números: ").strip()
            resultado = converter_numeros_para_arabe(texto)
            print("\n→ Resultado:", resultado)
            historico.append((texto, resultado))
            pausar()

        elif opcao == '4':
            texto = input("Digite números árabes orientais: ").strip()
            resultado = converter_numeros_para_latino(texto)
            print("\n→ Resultado:", resultado)
            historico.append((texto, resultado))
            pausar()

        elif opcao == '5':
            mostrar_mapa()
            pausar()

        elif opcao == '6':
            usar_harakat = not usar_harakat
            print(f"Harakāt agora está {'ativado' if usar_harakat else 'desativado'}.")
            pausar()

        elif opcao == '7':
            usar_fonetico = not usar_fonetico
            print(f"Modo fonético agora está {'ativado' if usar_fonetico else 'desativado'}.")
            pausar()

        elif opcao == '8':
            if historico:
                salvar = input("Deseja salvar o histórico? (s/n): ").lower()
                if salvar == 's':
                    salvar_historico(historico)
            print("Saindo, hora de tomar um chá...")
            break

        else:
            print("Opção inválida.")
            pausar()

# ===== EXECUTAR =====

if __name__ == "__main__":
    principal()
