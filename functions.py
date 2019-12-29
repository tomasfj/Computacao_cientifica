import random
import sys

# CLASSE DOS UTENTES
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Utente:
    
    def __init__(self, id, prioridade, hora_entrada, tempos):
        self.id = id # identificador do utente
        self.prioridade = prioridade # prioridade ("G" - geral, "R" - prioritário pós pagamento (retorna à fase 2), "P" - prioritário geral)
        self.hora_entrada = hora_entrada # instante em que o utente entrou no sistema
        self.chegadas_filas = {} # instantes de chegada às filas (ex: {"fila_fase_1": None, "fila_fase_2_A": None, "fila_fase_3": None})
        self.tempos = {} # todas as ações do utente e os tempos (ex: {"tr": None, "A": None, "te": None})
        self.estado_atual = "antes" # das ações que vai realizar, esta é a que o utente está a realizar num dado momento
        self.tempos_espera = {"fila_fase_1": 0, "fila_fase_2_A": 0, "fila_fase_2_B": 0, "fila_fase_2_C": 0, "fila_fase_3": 0} # tempos de espera em todas as filas do sistema
        self.direto = False # define se o utente vai diretamente da fase 1 para a fase 3 ou não 
        self.retrocesso_feito = False # define se o utente (que pretende reentrar na fase 2) já reentrou na fase 2 ou não

    def str(self): # método que retorna uma string representativa do objeto (utente)
        aux = ""
        for k,v in self.tempos.items():
            aux += k + ": " + str(v) + ", "
        aux = aux[:-2]
        return "ID: {:<3} | Prioridade: {:<2} | Entrada: {:<6} | Tempos: {:<30}".format(self.id,self.prioridade,self.hora_entrada,aux)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE SUPORTE
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def total_utentes(): # função que calcula o número total de utentes a modelar no sistema
    
    return(random.randint(120,150))

def gerar_utentes(num_utentes): # função que gera todos os utentes que o sistema vai modelar
    
    utentes = []
    id_count = 1
    num_aux = 0

    # FASE 1
    # -----------------------------------------------------------------------------------------------
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
    # -----------------------------------------------------------------------------------------------

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

    for i in fase_3_B_voltam: # utentes que retornam aos balcões B da fase 2
        i.prioridade = "R"
        tempo_aux = i.tempos.get("B")
        i.tempos.update({"B":random.randint(1,tempo_aux)})
        i.tempos.update({"B_volta":tempo_aux-i.tempos.get("B")})

    for i in fase_3_C_voltam: # utentes que retornam ao balcão C da fase 2
        i.prioridade = "R"
        tempo_aux = i.tempos.get("C")
        i.tempos.update({"C":random.randint(1,tempo_aux)})
        i.tempos.update({"C_volta":tempo_aux-i.tempos.get("C")})
    # ----------------------------------------------------------------------------------

    # for i in utentes: print(i.str())
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
        if(i.estado_atual=="antes" and i.hora_entrada<proxima): 
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
    print("| {:<6} | {:<18} | {:<6} | {:<13} | {:<35} | {:<10} | {:<11} | {:<35} | {:<11} | {:<12} | {:<11} | {:<12} | {:<35} | {:<11} | {:<12} | {:<11} | {:<12} | {:<35} | {:<11} | {:<12} | {:<35} | {:<10} | {:<11} |".format(linha_tabela.get("clock"),tipo,utente,proxima_chegada_imprimir,fila_fase_1_imprimir,balcao_Tr_imprimir,partida_triagem_imprimir,fila_fase_2_A_imprimir,balcao_A1_imprimir,partida_balcao_A1_imprimir,balcao_A2_imprimir,partida_balcao_A2_imprimir,fila_fase_2_B_imprimir,balcao_B1_imprimir,partida_balcao_B1_imprimir,balcao_B2_imprimir,partida_balcao_B2_imprimir,fila_fase_2_C_imprimir,balcao_C1_imprimir,partida_balcao_C1_imprimir,fila_fase_3_imprimir,balcao_Te_imprimir,partida_tesouraria_imprimir))

def calcular_tempos_espera(utentes): # função que calcula os tempos de espera mínimos, médios e máximos em todas as filas (em períodos parciais e globais)
    soma=0
    soma_fase_1=0
    soma_fila_fase_2_A=0
    soma_fila_fase_1=0
    soma_fila_fase_2_C=0
    soma_fila_fase_2_B=0
    soma_fila_fase_3=0
    for utente in utentes:
        for i in utente.tempos_espera.items():
            soma+=i[1]
        soma_fila_fase_2_A += utente.tempos_espera['fila_fase_2_A']
        soma_fila_fase_1 += utente.tempos_espera['fila_fase_1']
        soma_fila_fase_2_C += utente.tempos_espera['fila_fase_2_C']
        soma_fila_fase_2_B += utente.tempos_espera['fila_fase_2_B']
        soma_fila_fase_3 += utente.tempos_espera['fila_fase_3']
    return soma,soma_fila_fase_1, soma_fila_fase_2_A, soma_fila_fase_2_B , soma_fila_fase_2_C, soma_fila_fase_3 

def calcular_taxas_ocupacao(utentes): # função que calcula as taxas de ocupação em todas os balcões de atendimento (em períodos parciais e globais)
    # TODO
    return
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    num_utentes = total_utentes()
    gerar_utentes(num_utentes)
