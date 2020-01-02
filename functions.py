import random
import sys

# CLASSE DOS UTENTES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Utente:
    
    def __init__(self, id, prioridade, hora_entrada, tempos):
        self.id = id # identificador do utente
        self.prioridade = prioridade # prioridade ("G" - geral, "R" - prioritário pós pagamento (retorna à fase 2), "P" - prioritário geral)
        self.hora_entrada = hora_entrada # instante em que o utente entrou no sistema
        self.chegadas_filas = {} # instantes de chegada às filas (ex: {"fila_fase_1": None, "fila_fase_2_A": None, "fila_fase_3": None})
        self.tempos = {} # todas as ações do utente e os tempos (ex: {"tr": None, "A": None, "te": None})
        self.percurso = "antes " # todo o percurso do utente no sistema
        self.tempos_espera = {"fila_fase_1": 0, "fila_fase_2_A": 0, "fila_fase_2_B": 0, "fila_fase_2_C": 0, "fila_fase_3": 0} # tempos de espera em todas as filas do sistema
        self.direto = False # define se o utente vai diretamente da fase 1 para a fase 3 ou não
        self.retrocesso_feito = False # define se o utente (que pretende reentrar na fase 2) já reentrou na fase 2 ou não

    def str(self): # método que retorna uma string representativa do objeto (utente)
        aux = ""
        for k,v in self.tempos.items():
            aux += k + ": " + str(v) + ", "
        aux = aux[:-2]
        return "ID: {:<3} | Prioridade: {:<2} | Entrada: {:<6} | Tempos: {:<30}".format(self.id,self.prioridade,self.hora_entrada,aux)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE SUPORTE
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def total_utentes(): # função que calcula o número total de utentes a modelar no sistema
    
    return(random.randint(120,150))

def gerar_utentes(num_utentes): # função que gera todos os utentes que o sistema vai modelar
    
    utentes = []
    id_count = 1
    num_aux = 0

    # FASE 1
    # -----------------------------------------------------------------------------------------
    for i in range(num_utentes):

        # gerar a prioridade
        if(random.randint(1,10)<=2): rand_prioridade = "P"
        else: rand_prioridade = "G"

        num_aux = random.randint(1,100)

        # gerar a hora de entrada no sistema
        if(num_aux<=10): # 10% dos utentes
            rand_hora_entrada = random.randint(0,7200)
        elif(num_aux>10 and num_aux<=35): # 25% dos utentes
            rand_hora_entrada = random.randint(7201,14400)
        elif(num_aux>35 and num_aux<=80): # 45% dos utentes
            rand_hora_entrada = random.randint(14401,21600)
        else: # 20% dos utentes
            rand_hora_entrada = random.randint(21601,28800)

        utentes.append(Utente(id_count,rand_prioridade,rand_hora_entrada,{}))
        id_count += 1

    # tempo no balcão de triagem
    triagem_rapida = random.sample(utentes, int(0.55*num_utentes))
    triagem_media = random.sample(list(set(utentes)-set(triagem_rapida)),int(0.35*num_utentes))
    triagem_lenta = list(set(utentes)-set(triagem_rapida)-set(triagem_media))

    for i in triagem_rapida: # atribuir tempos aos utentes que fazem uma triagem rápida
        i.tempos.update({"tr":random.randint(0,60)})

    for i in triagem_media: # atribuir tempos aos utentes que fazem uma triagem média
        i.tempos.update({"tr":random.randint(60,120)})
    
    for i in triagem_lenta: # atribuir tempos aos utentes que fazem uma triagem lenta
        i.tempos.update({"tr":random.randint(120,180)})
    # -----------------------------------------------------------------------------------------

    # FASE 2
    # -----------------------------------------------------------------------------------
    # escolher que utentes continuam para a fase 2 e quais vão diretamente para a fase 3
    fase_3_direta = random.sample(utentes, int(0.10*num_utentes))
    for i in fase_3_direta: i.direto = True

    fase_2 = list(set(utentes)-set(fase_3_direta))

    balcoes_A = random.sample(fase_2, int(0.35*(len(fase_2))))
    balcoes_B = random.sample(list(set(fase_2)-set(balcoes_A)),int(0.50*(len(fase_2))))
    balcao_C = list(set(fase_2)-set(balcoes_A)-set(balcoes_B))

    for i in balcoes_A: # atribuir tempos aos utentes que vão para os balcões A
        num_aux = random.randint(1,100)
        if(num_aux<=25): i.tempos.update({"A":random.randint(0,300)})
        elif(num_aux>25 and num_aux<=60): i.tempos.update({"A":random.randint(300,900)})
        elif(num_aux>60 and num_aux<=90): i.tempos.update({"A":random.randint(900,1500)})
        else: i.tempos.update({"A":random.randint(1500,1800)})

    for i in balcoes_B: # atribuir tempos aos utentes que vão para os balcões B
        num_aux = random.randint(1,100)
        if(num_aux<=25): i.tempos.update({"B":random.randint(0,300)})
        elif(num_aux>25 and num_aux<=70): i.tempos.update({"B":random.randint(300,600)})
        elif(num_aux>70 and num_aux<=95): i.tempos.update({"B":random.randint(600,900)})
        else: i.tempos.update({"B":random.randint(900,1200)})

    for i in balcao_C: # atribuir tempos aos utentes que vão para o balcão C
        num_aux = random.randint(1,100)
        if(num_aux<=10): i.tempos.update({"C":random.randint(0,300)})
        elif(num_aux>10 and num_aux<=45): i.tempos.update({"C":random.randint(300,600)})
        elif(num_aux>45 and num_aux<=90): i.tempos.update({"C":random.randint(600,900)})
        else: i.tempos.update({"C":random.randint(900,1200)})
    # -----------------------------------------------------------------------------------

    # FASE 3
    # ----------------------------------------------------------------------------------
    # escolher que utentes continuam para a fase 3
    fase_3_A = random.sample(balcoes_A, int(0.20*len(balcoes_A)))
    fase_3_B = random.sample(balcoes_B, int(0.30*len(balcoes_B)))
    fase_3_C = random.sample(balcao_C, int(0.75*len(balcao_C)))

    fase_3_combinada = fase_3_A + fase_3_B + fase_3_C + fase_3_direta

    for i in fase_3_combinada:
        num_aux = random.randint(1,100)
        if(num_aux<=40): i.tempos.update({"te":random.randint(0,60)})
        elif(num_aux>40 and num_aux<=95): i.tempos.update({"te":random.randint(60,120)})
        else: i.tempos.update({"te":random.randint(120,180)})

    # tratar dos utentes que voltam para a fase 2
    fase_3_A_voltam = random.sample(fase_3_A, int(0.30*len(fase_3_A)))
    fase_3_B_voltam = random.sample(fase_3_B, int(0.20*len(fase_3_B)))
    fase_3_C_voltam = random.sample(fase_3_C, int(0.40*len(fase_3_C)))

    tempo_aux = 0
    for i in fase_3_A_voltam: # utentes que retornam aos balcões A da fase 2
        i.prioridade = "R"
        tempo_aux = i.tempos.get("A")
        i.tempos.update({"A":random.randint(1,tempo_aux)})
        i.tempos.update({"A_volta":tempo_aux-i.tempos.get("A")})
        i.tempos_espera.update({"fila_fase_2_A_volta": 0})

    for i in fase_3_B_voltam: # utentes que retornam aos balcões B da fase 2
        i.prioridade = "R"
        tempo_aux = i.tempos.get("B")
        i.tempos.update({"B":random.randint(1,tempo_aux)})
        i.tempos.update({"B_volta":tempo_aux-i.tempos.get("B")})
        i.tempos_espera.update({"fila_fase_2_B_volta": 0})

    for i in fase_3_C_voltam: # utentes que retornam ao balcão C da fase 2
        i.prioridade = "R"
        tempo_aux = i.tempos.get("C")
        i.tempos.update({"C":random.randint(1,tempo_aux)})
        i.tempos.update({"C_volta":tempo_aux-i.tempos.get("C")})
        i.tempos_espera.update({"fila_fase_2_C_volta": 0})
    # ----------------------------------------------------------------------------------
    '''
    print("# UTENTES")
    print("---------")
    for i in utentes: print(i.str())
    print("---------")'''
    return(utentes)

def adicionar_fila(utente, fila): # função que adiciona o utente à fila passada como parâmetro

    if(utente.prioridade=="G"): # utente geral
        fila[1].append(utente)
    
    elif(utente.prioridade=="R"): # utente prioritário sobre os gerais
        fila[1].insert(0,utente)
    
    else: # utente prioritário
        fila[0].append(utente)

def escolher_fila(fila): # função que retorna o próximo utente a ser atendido na fila da fase dada

    if(not fila[0]): # fila prioritária está vazia

        if(not fila[1]): # fila geral também está vazia
            return(None)
        
        else:
            try:
                return(fila[1].pop(0)) # devolve o primeiro utente da lista geral
            except: return(None)

    else:
        try:
            return(fila[0].pop(0))  # devolve o primeiro utente da lista prioritária
        except: return(None)

def proxima_chegada(utentes): # função que calcula a próxima chegada ao sistema

    proxima = 100000000
    utente = None

    for i in utentes:
        if(i.percurso=="antes " and i.hora_entrada<proxima): 
            proxima = i.hora_entrada
            utente = i

    return(proxima,utente)

def proximo_evento(tabela,utentes,balcao_Tr,balcao_Te,balcao_A1,balcao_A2,balcao_B1,balcao_B2,balcao_C1): # função que calcula o próximo evento a considerar

    minimo = 100000000
    evento = ""
    utente = None

    for k,v in tabela.items():
        if(k=="clock" or k=="tipo_evento" or k=="utente"): continue
        if(v<minimo):
            minimo = v
            evento = k
            if(k=="proxima_chegada"): utente = proxima_chegada(utentes)[1]
            elif(k=="partida_triagem"): utente = balcao_Tr
            elif(k=="partida_balcao_A1"): utente = balcao_A1
            elif(k=="partida_balcao_A2"): utente = balcao_A2
            elif(k=="partida_balcao_B1"): utente = balcao_B1
            elif(k=="partida_balcao_B2"): utente = balcao_B2
            elif(k=="partida_balcao_C1"): utente = balcao_C1
            elif(k=="partida_tesouraria"): utente = balcao_Te

    return(minimo,evento,utente)

def parar_simulacao(tabela): # função que determina se devemos parar a simulação ou não

    parar = True
    infinito = 100000000

    for k,v in tabela.items():
        if(k=="clock" or k=="tipo_evento" or k=="utente"): continue
        if(v!=infinito): 
            parar = False
            break
    
    return(parar)

def imprimir_linha_tabela(utente_atual,linha_tabela,fila_fase_1,balcao_Tr,fila_fase_2_A,balcao_A1,balcao_A2,fila_fase_2_B,balcao_B1,balcao_B2,fila_fase_2_C,balcao_C1,fila_fase_3,balcao_Te): # função que imprime uma linha da tabela de simulação

    infinito = 100000000

    if(utente_atual==None): utente = "------"
    else: utente = utente_atual.prioridade + str(utente_atual.id)

    if(linha_tabela.get("tipo_evento")==None):
        tipo = "None"
    else: tipo = linha_tabela.get("tipo_evento")

    # fila fase 1 (formato para imprimir)
    fila_fase_1_imprimir = "P: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_1[0])))))
    fila_fase_1_imprimir += " G: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_1[1])))))
    if(balcao_Tr==None): balcao_Tr_imprimir = "None"
    else: balcao_Tr_imprimir = balcao_Tr.prioridade + str(balcao_Tr.id)

    # fila fase 2 A (formato para imprimir)
    fila_fase_2_A_imprimir = "P: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_A[0])))))
    fila_fase_2_A_imprimir += " G: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_A[1])))))
    if(balcao_A1==None): balcao_A1_imprimir = "None"
    else: balcao_A1_imprimir = balcao_A1.prioridade + str(balcao_A1.id)
    if(balcao_A2==None): balcao_A2_imprimir = "None"
    else: balcao_A2_imprimir = balcao_A2.prioridade + str(balcao_A2.id)

    # fila fase 2 B (formato para imprimir)
    fila_fase_2_B_imprimir = "P: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_B[0])))))
    fila_fase_2_B_imprimir += " G: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_B[1])))))
    if(balcao_B1==None): balcao_B1_imprimir = "None"
    else: balcao_B1_imprimir = balcao_B1.prioridade + str(balcao_B1.id)
    if(balcao_B2==None): balcao_B2_imprimir = "None"
    else: balcao_B2_imprimir = balcao_B2.prioridade + str(balcao_B2.id)

    # fila fase 2 C (formato para imprimir)
    fila_fase_2_C_imprimir = "P: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_C[0])))))
    fila_fase_2_C_imprimir += " G: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_2_C[1])))))
    if(balcao_C1==None): balcao_C1_imprimir = "None"
    else: balcao_C1_imprimir = balcao_C1.prioridade + str(balcao_C1.id)

    # fila fase 3 (formato para imprimir)
    fila_fase_3_imprimir = "P: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_3[0])))))
    fila_fase_3_imprimir += " G: " + ", ".join(list(map(lambda x : str(x),list(map(lambda x : x.id, fila_fase_3[1])))))
    if(balcao_Te==None): balcao_Te_imprimir = "None"
    else: balcao_Te_imprimir = balcao_Te.prioridade + str(balcao_Te.id)

    # próxima chegada
    if(linha_tabela.get("proxima_chegada")==infinito): proxima_chegada_imprimir = "inf."
    else: proxima_chegada_imprimir = linha_tabela.get("proxima_chegada")

    # partida triagem
    if(linha_tabela.get("partida_triagem")==infinito): partida_triagem_imprimir = "inf."
    else: partida_triagem_imprimir = linha_tabela.get("partida_triagem")

    # partida balcão A1
    if(linha_tabela.get("partida_balcao_A1")==infinito): partida_balcao_A1_imprimir = "inf."
    else: partida_balcao_A1_imprimir = linha_tabela.get("partida_balcao_A1")

    # partida balcão A2
    if(linha_tabela.get("partida_balcao_A2")==infinito): partida_balcao_A2_imprimir = "inf."
    else: partida_balcao_A2_imprimir = linha_tabela.get("partida_balcao_A2")

    # partida balcão B1
    if(linha_tabela.get("partida_balcao_B1")==infinito): partida_balcao_B1_imprimir = "inf."
    else: partida_balcao_B1_imprimir = linha_tabela.get("partida_balcao_B1")

    # partida balcão B2
    if(linha_tabela.get("partida_balcao_B2")==infinito): partida_balcao_B2_imprimir = "inf."
    else: partida_balcao_B2_imprimir = linha_tabela.get("partida_balcao_B2")

    # partida balcão C1
    if(linha_tabela.get("partida_balcao_C1")==infinito): partida_balcao_C1_imprimir = "inf."
    else: partida_balcao_C1_imprimir = linha_tabela.get("partida_balcao_C1")

    # partida tesouraria
    if(linha_tabela.get("partida_tesouraria")==infinito): partida_tesouraria_imprimir = "inf."
    else: partida_tesouraria_imprimir = linha_tabela.get("partida_tesouraria")

    # imprimir linha da tabela
    print("| {:<6} | {:<18} | {:<6} | {:<13} | {:<60} | {:<10} | {:<11} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<60} | {:<10} | {:<11} |".format(linha_tabela.get("clock"),tipo,utente,proxima_chegada_imprimir,fila_fase_1_imprimir,balcao_Tr_imprimir,partida_triagem_imprimir,fila_fase_2_A_imprimir,balcao_A1_imprimir,partida_balcao_A1_imprimir,balcao_A2_imprimir,partida_balcao_A2_imprimir,fila_fase_2_B_imprimir,balcao_B1_imprimir,partida_balcao_B1_imprimir,balcao_B2_imprimir,partida_balcao_B2_imprimir,fila_fase_2_C_imprimir,balcao_C1_imprimir,partida_balcao_C1_imprimir,fila_fase_3_imprimir,balcao_Te_imprimir,partida_tesouraria_imprimir))

def utentes_no_intervalo(fase,intervalo,utentes):

    infinito = 100000000
    num_utentes = 0

    # OBTER O INTERVALO REQUISITADO
    # -----------------------------
    if(intervalo=="0"): 
        menor = 0
        maior = 7200
    elif(intervalo=="1"):
        menor = 7201
        maior = 14400
    elif(intervalo=="2"):
        menor = 14401
        maior = 21600
    elif(intervalo=="3"):
        menor = 21601
        maior = 28800
    else:
        menor = 28800
        maior = infinito
    # -----------------------------

    for i in utentes:

        # obter o balcão do utente
        balcao = ""
        if(i.tempos.get("A")!=None): balcao = "A"
        if(i.tempos.get("B")!=None): balcao = "B"
        if(i.tempos.get("C")!=None): balcao = "C"

        # CASOS ESPECIAIS
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if((fase==2 and i.direto) or (fase==3 and i.tempos.get("te")==None)): # casos especiais
            continue

        if(i.prioridade=="R" and fase==2): # um dos utentes que faz retrocesso

            passagem = [0,0]
            # primeira passagem pela fase 2
            passagem[0] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")
            passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao)

            if((passagem[0]>=menor and passagem[0]<=maior) or (passagem[1]>=menor and passagem[1]<=maior) or (menor>=passagem[0] and maior<=passagem[1])): 
                num_utentes += 1
                continue

            # segunda passagem pela fase 2
            passagem[0] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao) + i.tempos_espera.get("fila_fase_3") + i.tempos.get("te")
            passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao) + i.tempos_espera.get("fila_fase_3") + i.tempos.get("te") + i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") + i.tempos.get(balcao + "_volta")
            
            if((passagem[0]>=menor and passagem[0]<=maior) or (passagem[1]>=menor and passagem[1]<=maior) or (menor>=passagem[0] and maior<=passagem[1])): num_utentes += 1
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # CASOS NORMAIS
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            passagem = [0,0]
            # avaliar se o utente esteve na fase e intervalo passados por parâmetro
            if(fase==1): 
                passagem[0] = i.hora_entrada
                passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")
            elif(fase==2):
                passagem[0] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")
                passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao)
            else:
                if(i.direto):
                    passagem[0] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")
                    passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_3") + i.tempos.get("te")
                else:
                    passagem[0] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao)
                    passagem[1] = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao) + i.tempos_espera.get("fila_fase_3") + i.tempos.get("te")
                
            if((passagem[0]>=menor and passagem[0]<=maior) or (passagem[1]>=menor and passagem[1]<=maior) or (menor>=passagem[0] and maior<=passagem[1])): num_utentes += 1
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    return(num_utentes)

def calcular_tempos_espera(utentes,num_utentes): # função que calcula os tempos de espera mínimos, médios e máximos em todas as filas (em períodos parciais e globais)
    
    infinito = 100000000

    # dicionários para os tempos
    tempos_fase_1 = {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}}
    tempos_fase_2 = {"A": {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}}, 
                            "B": {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}},
                            "C": {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}}}
    tempos_fase_3 = {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}}
    tempos_globais = {"0": {"minimo": 0, "medio": 0, "maximo": 0}, "1": {"minimo": 0, "medio": 0, "maximo": 0}, "2": {"minimo": 0, "medio": 0, "maximo": 0}, "3": {"minimo": 0, "medio": 0, "maximo": 0}, "4": {"minimo": 0, "medio": 0, "maximo": 0}, "total": {"minimo": 0, "medio": 0, "maximo": 0}}

    for i in utentes:

        # TEMPOS PARCIAIS NA FASE 1
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # perceber em que intervalo(s) começa e acaba a passagem do utente pela fase 1
        inicio = int((i.hora_entrada)/7200)
        fim = int((i.hora_entrada + i.tempos_espera.get("fila_fase_1"))/7200)

        if(i.tempos_espera.get("fila_fase_1")!=0): # o utente esteve pelo menos 1 instante à espera

            if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo
            
                # tempo de espera médio
                tempos_fase_1.get(str(inicio)).update({"medio": tempos_fase_1.get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_1")})

                # tempo de espera mínimo
                if(i.tempos_espera.get("fila_fase_1")<tempos_fase_1.get(str(inicio)).get("minimo")):
                    tempos_fase_1.get(str(inicio)).update({"minimo": i.tempos_espera.get("fila_fase_1")})

                # tempo de espera máximo
                if(i.tempos_espera.get("fila_fase_1")>tempos_fase_1.get(str(inicio)).get("maximo")):
                    tempos_fase_1.get(str(inicio)).update({"maximo": i.tempos_espera.get("fila_fase_1")})

            elif((fim-inicio)==1): # o utente passou por 2 intervalos
                
                # tempo de espera médio
                tempos_fase_1.get(str(inicio)).update({"medio": tempos_fase_1.get(str(inicio)).get("medio") + (fim*7200) - i.hora_entrada})
                tempos_fase_1.get(str(fim)).update({"medio": tempos_fase_1.get(str(fim)).get("medio") + i.tempos_espera.get("fila_fase_1") - ((fim*7200) - i.hora_entrada)})

                # tempo de espera mínimo (primeiro intervalo)
                if(((fim*7200) - i.hora_entrada)<tempos_fase_1.get(str(inicio)).get("minimo")):
                    tempos_fase_1.get(str(inicio)).update({"minimo": (fim*7200) - i.hora_entrada})

                # tempo de espera máximo (primeiro intervalo)
                if(((fim*7200) - i.hora_entrada)>tempos_fase_1.get(str(inicio)).get("maximo")):
                    tempos_fase_1.get(str(inicio)).update({"maximo": (fim*7200) - i.hora_entrada})

                # tempo de espera mínimo (segundo intervalo)
                if((i.tempos_espera.get("fila_fase_1") - ((fim*7200) - i.hora_entrada))<tempos_fase_1.get(str(fim)).get("minimo")):
                    tempos_fase_1.get(str(fim)).update({"minimo": i.tempos_espera.get("fila_fase_1") - ((fim*7200) - i.hora_entrada)})

                # tempo de espera máximo (segundo intervalo)
                if((i.tempos_espera.get("fila_fase_1") - ((fim*7200) - i.hora_entrada))>tempos_fase_1.get(str(fim)).get("maximo")):
                    tempos_fase_1.get(str(fim)).update({"maximo": i.tempos_espera.get("fila_fase_1") - ((fim*7200) - i.hora_entrada)})

            elif((fim-inicio)==2): # o utente passou por 3 intervalos
                
                # tempo de espera médio
                tempos_fase_1.get(str(inicio)).update({"medio": tempos_fase_1.get(str(inicio)).get("medio") + (fim*7200) - i.hora_entrada})
                tempos_fase_1.get(str(inicio+1)).update({"medio": tempos_fase_1.get(str(inicio+1)).get("medio") + 7200})
                tempos_fase_1.get(str(fim)).update({"medio": tempos_fase_1.get(str(fim)).get("medio") + i.tempos_espera.get("fila_fase_1") - (((fim*7200) - i.hora_entrada) + 7200)})

                # tempo de espera mínimo (primeiro intervalo)
                if(((fim*7200) - i.hora_entrada)<tempos_fase_1.get(str(inicio)).get("minimo")):
                    tempos_fase_1.get(str(inicio)).update({"minimo": (fim*7200) - i.hora_entrada})

                # tempo de espera máximo (primeiro intervalo)
                if(((fim*7200) - i.hora_entrada)>tempos_fase_1.get(str(inicio)).get("maximo")):
                    tempos_fase_1.get(str(inicio)).update({"maximo": (fim*7200) - i.hora_entrada})

                # tempo de espera mínimo (segundo intervalo)
                if(7200<tempos_fase_1.get(str(inicio+1)).get("minimo")):
                    tempos_fase_1.get(str(inicio+1)).update({"minimo": 7200})

                # tempo de espera máximo (segundo intervalo)
                if(7200>tempos_fase_1.get(str(inicio+1)).get("maximo")):
                    tempos_fase_1.get(str(inicio+1)).update({"maximo": 7200})
                
                # tempo de espera mínimo (terceiro intervalo)
                if((i.tempos_espera.get("fila_fase_1") - (((fim*7200) - i.hora_entrada) + 7200))<tempos_fase_1.get(str(fim)).get("minimo")):
                    tempos_fase_1.get(str(fim)).update({"minimo": 7200})

                # tempo de espera máximo (terceiro intervalo)
                if((i.tempos_espera.get("fila_fase_1") - (((fim*7200) - i.hora_entrada) + 7200))>tempos_fase_1.get(str(fim)).get("maximo")):
                    tempos_fase_1.get(str(fim)).update({"maximo": 7200})

            # TODO: mais intervalos??
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if(not i.direto): 

            # TEMPOS PARCIAIS NA FASE 2
            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # obter o balcão do utente
            balcao = ""
            if(i.tempos.get("A")!=None): balcao = "A"
            if(i.tempos.get("B")!=None): balcao = "B"
            if(i.tempos.get("C")!=None): balcao = "C"

            entrada_fase_2 = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")

            inicio = int((entrada_fase_2)/7200)
            fim = int((entrada_fase_2 + i.tempos_espera.get("fila_fase_2_" + balcao))/7200)

            if(i.tempos_espera.get("fila_fase_2_" + balcao)!=0): # o utente esteve pelo menos 1 instante à espera na primeira e (possivelmente) única vez que passou pela fase 2

                if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao)})

                    # tempo de espera mínimo
                    if(i.tempos_espera.get("fila_fase_2_" + balcao)<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": i.tempos_espera.get("fila_fase_2_" + balcao)})

                    # tempo de espera máximo
                    if(i.tempos_espera.get("fila_fase_2_" + balcao)>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": i.tempos_espera.get("fila_fase_2_" + balcao)})

                elif((fim-inicio)==1): # o utente passou por 2 intervalos

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_2})
                    tempos_fase_2.get(balcao).get(str(fim)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao) - ((fim*7200) - entrada_fase_2)})

                    # tempo de espera mínimo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_2})
                    
                    # tempo de espera máximo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_2})

                    # tempo de espera mínimo (segundo intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao) - ((fim*7200) - entrada_fase_2))<tempos_fase_2.get(balcao).get(str(fim)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"minimo": i.tempos_espera.get("fila_fase_2_" + balcao) - ((fim*7200) - entrada_fase_2)})

                    # tempo de espera máximo (segundo intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao) - ((fim*7200) - entrada_fase_2))>tempos_fase_2.get(balcao).get(str(fim)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"maximo": i.tempos_espera.get("fila_fase_2_" + balcao) - ((fim*7200) - entrada_fase_2)})

                elif((fim-inicio)==2): # o utente passou por 3 intervalos

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_2})
                    tempos_fase_2.get(balcao).get(str(inicio+1)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio+1)).get("medio") + 7200})
                    tempos_fase_2.get(balcao).get(str(fim)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao) - (((fim*7200) - entrada_fase_2) + 7200)})

                    # tempo de espera mínimo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_2})
                    
                    # tempo de espera máximo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_2})

                    # tempo de espera mínimo (segundo intervalo)
                    if(7200<tempos_fase_2.get(balcao).get(str(inicio+1)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio+1)).update({"minimo": 7200})

                    # tempo de espera máximo (segundo intervalo)
                    if(7200>tempos_fase_2.get(balcao).get(str(inicio+1)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio+1)).update({"maximo": 7200})

                    # tempo de espera mínimo (terceiro intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao) - (((fim*7200) - entrada_fase_2) + 7200))<tempos_fase_2.get(balcao).get(str(fim)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"minimo": i.tempos_espera.get("fila_fase_2_" + balcao) - (((fim*7200) - entrada_fase_2) + 7200)})

                    # tempo de espera máximo (terceiro intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao) - (((fim*7200) - entrada_fase_2) + 7200))>tempos_fase_2.get(balcao).get(str(fim)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"maximo": i.tempos_espera.get("fila_fase_2_" + balcao) - (((fim*7200) - entrada_fase_2) + 7200)})


                # TODO: mais intervalos??

            if(i.prioridade=="R" and i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")!=0): # o utente esteve pelo menos 1 instante à espera na segunda passagem pela fase 2

                entrada_fase_2 = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao) + i.tempos_espera.get("fila_fase_3") + i.tempos.get("te")

                inicio = int((entrada_fase_2)/7200)
                fim = int((entrada_fase_2 + i.tempos_espera.get("fila_fase_2_" + balcao + "_volta"))/7200)

                if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")})

                    # tempo de espera mínimo
                    if(i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")})

                    # tempo de espera máximo
                    if(i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": i.tempos_espera.get("fila_fase_2_" + balcao + "_volta")})

                elif((fim-inicio)==1): # o utente passou por 2 intervalos

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_2})
                    tempos_fase_2.get(balcao).get(str(fim)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - ((fim*7200) - entrada_fase_2)})

                    # tempo de espera mínimo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_2})
                    
                    # tempo de espera máximo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_2})

                    # tempo de espera mínimo (segundo intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - ((fim*7200) - entrada_fase_2))<tempos_fase_2.get(balcao).get(str(fim)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"minimo": i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - ((fim*7200) - entrada_fase_2)})

                    # tempo de espera máximo (segundo intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - ((fim*7200) - entrada_fase_2))>tempos_fase_2.get(balcao).get(str(fim)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"maximo": i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - ((fim*7200) - entrada_fase_2)})
           
                elif((fim-inicio)==2): # o utente passou por 3 intervalos

                    # tempo de espera médio
                    tempos_fase_2.get(balcao).get(str(inicio)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_2})
                    tempos_fase_2.get(balcao).get(str(inicio+1)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio+1)).get("medio") + 7200})
                    tempos_fase_2.get(balcao).get(str(fim)).update({"medio": tempos_fase_2.get(balcao).get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - (((fim*7200) - entrada_fase_2) + 7200)})

                    # tempo de espera mínimo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)<tempos_fase_2.get(balcao).get(str(inicio)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_2})
                    
                    # tempo de espera máximo (primeiro intervalo)
                    if(((fim*7200) - entrada_fase_2)>tempos_fase_2.get(balcao).get(str(inicio)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_2})

                    # tempo de espera mínimo (segundo intervalo)
                    if(7200<tempos_fase_2.get(balcao).get(str(inicio+1)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(inicio+1)).update({"minimo": 7200})

                    # tempo de espera máximo (segundo intervalo)
                    if(7200>tempos_fase_2.get(balcao).get(str(inicio+1)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(inicio+1)).update({"maximo": 7200}) 

                    # tempo de espera mínimo (terceiro intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - (((fim*7200) - entrada_fase_2) + 7200))<tempos_fase_2.get(balcao).get(str(fim)).get("minimo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"minimo": (i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - (((fim*7200) - entrada_fase_2) + 7200))})

                    # tempo de espera máximo (terceiro intervalo)
                    if((i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - (((fim*7200) - entrada_fase_2) + 7200))>tempos_fase_2.get(balcao).get(str(fim)).get("maximo")):
                        tempos_fase_2.get(balcao).get(str(fim)).update({"maximo": (i.tempos_espera.get("fila_fase_2_" + balcao + "_volta") - (((fim*7200) - entrada_fase_2) + 7200))})  
            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if(i.tempos.get("te")==None): # o utente não passa pela tesouraria
            continue

        # TEMPOS PARCIAIS NA FASE 3
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # obter o balcão do utente
        balcao = ""
        if(i.tempos.get("A")!=None): balcao = "A"
        if(i.tempos.get("B")!=None): balcao = "B"
        if(i.tempos.get("C")!=None): balcao = "C"

        if(i.direto):
            entrada_fase_3 = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr")
        else:
            entrada_fase_3 = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao)

        inicio = int((entrada_fase_3)/7200)
        fim = int((entrada_fase_3 + i.tempos_espera.get("fila_fase_3"))/7200)

        if(i.tempos_espera.get("fila_fase_3")!=0): # o utente esteve pelo menos 1 instante à espera

            if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                # tempo de espera médio
                tempos_fase_3.get(str(inicio)).update({"medio": tempos_fase_3.get(str(inicio)).get("medio") + i.tempos_espera.get("fila_fase_3")})

                # tempo de espera mínimo
                if(i.tempos_espera.get("fila_fase_3")<tempos_fase_3.get(str(inicio)).get("minimo")):
                    tempos_fase_3.get(str(inicio)).update({"minimo": i.tempos_espera.get("fila_fase_3")})

                # tempo de espera máximo
                if(i.tempos_espera.get("fila_fase_3")>tempos_fase_3.get(str(inicio)).get("maximo")):
                    tempos_fase_3.get(str(inicio)).update({"maximo": i.tempos_espera.get("fila_fase_3")})

            elif((fim-inicio)==1): # o utente passou por 2 intervalos

                # tempo de espera médio
                tempos_fase_3.get(str(inicio)).update({"medio": tempos_fase_3.get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_3})
                tempos_fase_3.get(str(fim)).update({"medio": tempos_fase_3.get(str(fim)).get("medio") + i.tempos_espera.get("fila_fase_3") - ((fim*7200) - entrada_fase_3)})

                # tempo de espera mínimo (primeiro intervalo)
                if(((fim*7200) - entrada_fase_3)<tempos_fase_3.get(str(inicio)).get("minimo")):
                    tempos_fase_3.get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_3})
                
                # tempo de espera máximo (primeiro intervalo)
                if(((fim*7200) - entrada_fase_3)>tempos_fase_3.get(str(inicio)).get("maximo")):
                    tempos_fase_3.get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_3})

                # tempo de espera mínimo (segundo intervalo)
                if((i.tempos_espera.get("fila_fase_3") - ((fim*7200) - entrada_fase_3))<tempos_fase_3.get(str(fim)).get("minimo")):
                    tempos_fase_3.get(str(fim)).update({"minimo": i.tempos_espera.get("fila_fase_3") - ((fim*7200) - entrada_fase_3)})

                # tempo de espera máximo (segundo intervalo)
                if((i.tempos_espera.get("fila_fase_3") - ((fim*7200) - entrada_fase_3))>tempos_fase_3.get(str(fim)).get("maximo")):
                    tempos_fase_3.get(str(fim)).update({"maximo": i.tempos_espera.get("fila_fase_3") - ((fim*7200) - entrada_fase_3)})

            elif((fim-inicio)==2): # o utente passou por 3 intervalos

                # tempo de espera médio
                tempos_fase_3.get(str(inicio)).update({"medio": tempos_fase_3.get(str(inicio)).get("medio") + (fim*7200) - entrada_fase_3})
                tempos_fase_3.get(str(inicio+1)).update({"medio": tempos_fase_3.get(str(inicio+1)).get("medio") + 7200})
                tempos_fase_3.get(str(fim)).update({"medio": tempos_fase_3.get(str(fim)).get("medio") + i.tempos_espera.get("fila_fase_3") - (((fim*7200) - entrada_fase_3) + 7200)})

                # tempo de espera mínimo (primeiro intervalo)
                if(((fim*7200) - entrada_fase_3)<tempos_fase_3.get(str(inicio)).get("minimo")):
                    tempos_fase_3.get(str(inicio)).update({"minimo": (fim*7200) - entrada_fase_3})
                
                # tempo de espera máximo (primeiro intervalo)
                if(((fim*7200) - entrada_fase_3)>tempos_fase_3.get(str(inicio)).get("maximo")):
                    tempos_fase_3.get(str(inicio)).update({"maximo": (fim*7200) - entrada_fase_3})

                # tempo de espera mínimo (segundo intervalo)
                if(7200<tempos_fase_3.get(str(inicio+1)).get("minimo")):
                    tempos_fase_3.get(str(inicio+1)).update({"minimo": 7200})

                # tempo de espera máximo (segundo intervalo)
                if(7200>tempos_fase_3.get(str(inicio+1)).get("maximo")):
                    tempos_fase_3.get(str(inicio+1)).update({"maximo": 7200})

                # tempo de espera mínimo (terceiro intervalo)
                if((i.tempos_espera.get("fila_fase_3") - (((fim*7200) - entrada_fase_3) + 7200))<tempos_fase_3.get(str(fim)).get("minimo")):
                    tempos_fase_3.get(str(fim)).update({"minimo": (i.tempos_espera.get("fila_fase_3") - (((fim*7200) - entrada_fase_3) + 7200))})

                # tempo de espera máximo (terceiro intervalo)
                if((i.tempos_espera.get("fila_fase_3") - (((fim*7200) - entrada_fase_3) + 7200))>tempos_fase_3.get(str(fim)).get("maximo")):
                    tempos_fase_3.get(str(fim)).update({"maximo": (i.tempos_espera.get("fila_fase_3") - (((fim*7200) - entrada_fase_3) + 7200))})

            # TODO: mais intervalos??
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ATUALIZAR OS TOTAIS
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    tempos_fase_1.update({"total": {"minimo": min(tempos_fase_1.get("0").get("minimo"),tempos_fase_1.get("1").get("minimo"),tempos_fase_1.get("2").get("minimo"),tempos_fase_1.get("3").get("minimo"),tempos_fase_1.get("4").get("minimo")),
                       "medio": sum([tempos_fase_1.get("0").get("medio"),tempos_fase_1.get("1").get("medio"),tempos_fase_1.get("2").get("medio"),tempos_fase_1.get("3").get("medio"),tempos_fase_1.get("4").get("medio")]),
                       "maximo": max(tempos_fase_1.get("0").get("maximo"),tempos_fase_1.get("1").get("maximo"),tempos_fase_1.get("2").get("maximo"),tempos_fase_1.get("3").get("maximo"),tempos_fase_1.get("4").get("maximo"))}})

    tempos_fase_2.get("A").update({"total": {"minimo": min(tempos_fase_2.get("A").get("0").get("minimo"),tempos_fase_2.get("A").get("1").get("minimo"),tempos_fase_2.get("A").get("2").get("minimo"),tempos_fase_2.get("A").get("3").get("minimo"),tempos_fase_2.get("A").get("4").get("minimo")),
                       "medio": sum([tempos_fase_2.get("A").get("0").get("medio"),tempos_fase_2.get("A").get("1").get("medio"),tempos_fase_2.get("A").get("2").get("medio"),tempos_fase_2.get("A").get("3").get("medio"),tempos_fase_2.get("A").get("4").get("medio")]),
                       "maximo": max(tempos_fase_2.get("A").get("0").get("maximo"),tempos_fase_2.get("A").get("1").get("maximo"),tempos_fase_2.get("A").get("2").get("maximo"),tempos_fase_2.get("A").get("3").get("maximo"),tempos_fase_2.get("A").get("4").get("maximo"))}})

    tempos_fase_2.get("B").update({"total": {"minimo": min(tempos_fase_2.get("B").get("0").get("minimo"),tempos_fase_2.get("B").get("1").get("minimo"),tempos_fase_2.get("B").get("2").get("minimo"),tempos_fase_2.get("B").get("3").get("minimo"),tempos_fase_2.get("B").get("4").get("minimo")),
                       "medio": sum([tempos_fase_2.get("B").get("0").get("medio"),tempos_fase_2.get("B").get("1").get("medio"),tempos_fase_2.get("B").get("2").get("medio"),tempos_fase_2.get("B").get("3").get("medio"),tempos_fase_2.get("B").get("4").get("medio")]),
                       "maximo": max(tempos_fase_2.get("B").get("0").get("maximo"),tempos_fase_2.get("B").get("1").get("maximo"),tempos_fase_2.get("B").get("2").get("maximo"),tempos_fase_2.get("B").get("3").get("maximo"),tempos_fase_2.get("B").get("4").get("maximo"))}})

    tempos_fase_2.get("C").update({"total": {"minimo": min(tempos_fase_2.get("C").get("0").get("minimo"),tempos_fase_2.get("C").get("1").get("minimo"),tempos_fase_2.get("C").get("2").get("minimo"),tempos_fase_2.get("C").get("3").get("minimo"),tempos_fase_2.get("C").get("4").get("minimo")),
                       "medio": sum([tempos_fase_2.get("C").get("0").get("medio"),tempos_fase_2.get("C").get("1").get("medio"),tempos_fase_2.get("C").get("2").get("medio"),tempos_fase_2.get("C").get("3").get("medio"),tempos_fase_2.get("C").get("4").get("medio")]),
                       "maximo": max(tempos_fase_2.get("C").get("0").get("maximo"),tempos_fase_2.get("C").get("1").get("maximo"),tempos_fase_2.get("C").get("2").get("maximo"),tempos_fase_2.get("C").get("3").get("maximo"),tempos_fase_2.get("C").get("4").get("maximo"))}})

    tempos_fase_3.update({"total": {"minimo": min(tempos_fase_3.get("0").get("minimo"),tempos_fase_3.get("1").get("minimo"),tempos_fase_3.get("2").get("minimo"),tempos_fase_3.get("3").get("minimo"),tempos_fase_3.get("4").get("minimo")),
                       "medio": sum([tempos_fase_3.get("0").get("medio"),tempos_fase_3.get("1").get("medio"),tempos_fase_3.get("2").get("medio"),tempos_fase_3.get("3").get("medio"),tempos_fase_3.get("4").get("medio")]),
                       "maximo": max(tempos_fase_3.get("0").get("maximo"),tempos_fase_3.get("1").get("maximo"),tempos_fase_3.get("2").get("maximo"),tempos_fase_3.get("3").get("maximo"),tempos_fase_3.get("4").get("maximo"))}})

    for k,v in tempos_globais.items():
        for k_2,v_2 in v.items():
            if(k_2=="minimo"): v.update({k_2: min(tempos_fase_1.get(k).get(k_2),tempos_fase_2.get("A").get(k).get(k_2), tempos_fase_2.get("B").get(k).get(k_2),tempos_fase_2.get("C").get(k).get(k_2),tempos_fase_3.get(k).get(k_2))})
            elif(k_2=="medio"): v.update({k_2: sum([tempos_fase_1.get(k).get(k_2),tempos_fase_2.get("A").get(k).get(k_2), tempos_fase_2.get("B").get(k).get(k_2),tempos_fase_2.get("C").get(k).get(k_2),tempos_fase_3.get(k).get(k_2)])})
            elif(k_2=="maximo"): v.update({k_2: max(tempos_fase_1.get(k).get(k_2),tempos_fase_2.get("A").get(k).get(k_2), tempos_fase_2.get("B").get(k).get(k_2),tempos_fase_2.get("C").get(k).get(k_2),tempos_fase_3.get(k).get(k_2))})
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # FAZER AS MÉDIAS
    # -----------------------------------------------------------------------------------------------------------------
    for i in ["0","1","2","3","4","total"]:
        if(i=="total"):
            tempos_fase_1.get(i).update({"medio": tempos_fase_1.get(i).get("medio")/num_utentes})
        else:
            utentes_aux = utentes_no_intervalo(1,i,utentes)
            if(utentes_aux!=0):
                tempos_fase_1.get(i).update({"medio": tempos_fase_1.get(i).get("medio")/utentes_aux})

    for i in ["A","B","C"]:
        for j in ["0","1","2","3","4","total"]:
            if(j=="total"):
                tempos_fase_2.get(i).get(j).update({"medio": tempos_fase_2.get(i).get(j).get("medio")/num_utentes})
            else:
                utentes_aux = utentes_no_intervalo(2,j,utentes)
                if(utentes_aux!=0):
                    tempos_fase_2.get(i).get(j).update({"medio": tempos_fase_2.get(i).get(j).get("medio")/utentes_aux})

    for i in ["0","1","2","3","4","total"]:
        if(i=="total"):
            tempos_fase_3.get(i).update({"medio": tempos_fase_3.get(i).get("medio")/num_utentes})
        else:
            utentes_aux = utentes_no_intervalo(3,i,utentes)
            if(utentes_aux!=0):
                tempos_fase_3.get(i).update({"medio": tempos_fase_3.get(i).get("medio")/utentes_aux})
    
    for i in ["0","1","2","3","4","total"]:
        tempos_globais.get(i).update({"medio": tempos_globais.get(i).get("medio")/num_utentes})
    # -----------------------------------------------------------------------------------------------------------------

    return(tempos_fase_1,tempos_fase_2,tempos_fase_3,tempos_globais)

def calcular_taxas_ocupacao(utentes,ultimo_instante): # função que calcula as taxas de ocupação em todas os balcões de atendimento (em períodos parciais e globais)
    
    ocupacoes = {"triagem": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, "A1": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, "A2": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, 
                "B1": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, "B2": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, "C1": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}, 
                "tesouraria": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "total": 0}}

    for i in utentes:

        # TAXAS DE OCUPAÇÃO NA FASE 1
        # -----------------------------------------------------------------------------------------------------------------------------------------------
        if("triagem" in i.percurso):
            
            entrada_triagem = i.hora_entrada + i.tempos_espera.get("fila_fase_1")
            inicio = int((entrada_triagem)/7200)
            fim = int((entrada_triagem + i.tempos.get("tr"))/7200)

            if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                ocupacoes.get("triagem").update({str(inicio): ocupacoes.get("triagem").get(str(inicio)) + i.tempos.get("tr")})
            
            elif((fim-inicio)==1): # o utente passou por 2 intervalos

                ocupacoes.get("triagem").update({str(inicio): ocupacoes.get("triagem").get(str(inicio)) + (fim*7200) - entrada_triagem})
                ocupacoes.get("triagem").update({str(fim): ocupacoes.get("triagem").get(str(fim)) + i.tempos.get("tr") - ((fim*7200) - entrada_triagem)})
        # -----------------------------------------------------------------------------------------------------------------------------------------------

        # TAXAS DE OCUPAÇÃO NA FASE 2
        # ---------------------------------------------------------------------------------------------------------------------------------------------
        if(not i.direto):

            if("balcao_A1" in i.percurso): balcao = "A1"
            elif("balcao_A2" in i.percurso): balcao = "A2"
            elif("balcao_B1" in i.percurso): balcao = "B1"
            elif("balcao_B2" in i.percurso): balcao = "B2"
            elif("balcao_C1" in i.percurso): balcao = "C1"
                
            entrada_balcao = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao[0])
            inicio = int((entrada_balcao)/7200)
            fim = int((entrada_balcao + i.tempos.get(balcao[0]))/7200)

            if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                ocupacoes.get(balcao).update({str(inicio): ocupacoes.get(balcao).get(str(inicio)) + i.tempos.get(balcao[0])})
            
            elif((fim-inicio)==1): # o utente passou por 2 intervalos

                ocupacoes.get(balcao).update({str(inicio): ocupacoes.get(balcao).get(str(inicio)) + (fim*7200) - entrada_balcao})
                ocupacoes.get(balcao).update({str(fim): ocupacoes.get(balcao).get(str(fim)) + i.tempos.get(balcao[0]) - ((fim*7200) - entrada_balcao)})
        # ---------------------------------------------------------------------------------------------------------------------------------------------
    
        if(i.tempos.get("te")==None): # o utente não passa pela tesouraria
            continue
        
        # TAXAS DE OCUPAÇÃO NA FASE 2
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if("tesouraria" in i.percurso): 

            # obter o balcão do utente
            balcao = ""
            if(i.tempos.get("A")!=None): balcao = "A"
            if(i.tempos.get("B")!=None): balcao = "B"
            if(i.tempos.get("C")!=None): balcao = "C"

            if(i.direto):
                entrada_tesouraria = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_3")
            else:
                entrada_tesouraria = i.hora_entrada + i.tempos_espera.get("fila_fase_1") + i.tempos.get("tr") + i.tempos_espera.get("fila_fase_2_" + balcao) + i.tempos.get(balcao) + i.tempos_espera.get("fila_fase_3")

            inicio = int((entrada_tesouraria)/7200)
            fim = int((entrada_tesouraria + i.tempos.get("te"))/7200)

            if(inicio==fim): # caso ideal, estamos sempre no mesmo intervalo

                ocupacoes.get("tesouraria").update({str(inicio): ocupacoes.get("tesouraria").get(str(inicio)) + i.tempos.get("te")})
            
            elif((fim-inicio)==1): # o utente passou por 2 intervalos

                ocupacoes.get("tesouraria").update({str(inicio): ocupacoes.get("tesouraria").get(str(inicio)) + (fim*7200) - entrada_tesouraria})
                ocupacoes.get("tesouraria").update({str(fim): ocupacoes.get("tesouraria").get(str(fim)) + i.tempos.get("te") - ((fim*7200) - entrada_tesouraria)})
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # CALCULAR OS TOTAIS
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    for k,v in ocupacoes.items():
        ocupacoes.get(k).update({"total": ocupacoes.get(k).get("0") + ocupacoes.get(k).get("1") + ocupacoes.get(k).get("2") + ocupacoes.get(k).get("3") + ocupacoes.get(k).get("4")})
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # CONVERTER PARA PERCENTAGENS
    # -------------------------------------------------------------------------------------
    for k,v in ocupacoes.items():
        for k_2,v_2 in v.items():
            if(k_2=="4"): ocupacoes.get(k).update({k_2: (v_2/(ultimo_instante-28800))*100})
            elif(k_2=="total"): ocupacoes.get(k).update({k_2: (v_2/(ultimo_instante))*100})
            else: ocupacoes.get(k).update({k_2: (v_2/7200)*100})
    # -------------------------------------------------------------------------------------
    
    return(ocupacoes)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    num_utentes = total_utentes()
    gerar_utentes(num_utentes)