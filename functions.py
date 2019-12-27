import random

# CLASSE DOS UTENTES
# ---------------------------------------------------------------------------------------------------------------------------------------------
class Utente:
    
    def __init__(self, id, prioridade, hora_entrada, tempos):
        self.id = id # identificador do utente
        self.prioridade = prioridade # prioridade (0 - geral, 1 - prioritário pós pagamento, 2 - prioritário geral)
        self.hora_entrada = hora_entrada
        self.chegadas_filas = {} # instantes de chegada às filas (ex: {"fila_fase_1": None, "fila_fase_2_A": None, "fila_fase_3": None})
        self.tempos = {} # todas as ações do utente e os tempos (ex: {"tr": None, "A": None, "te": None})
        self.estado_atual = "antes" # das ações que vai realizar, esta é a que o utente está a realizar num dado momento
        self.tempo_de_espera = 0
        self.direto = False

    def str(self): # retorna uma string que representa o objeto (utente)
        aux = ""
        for k,v in self.tempos.items():
            aux += k + ": " + str(v) + ", "
        aux = aux[:-2]
        return "ID: {:<3} | Prioridade: {:<2} | Entrada: {:<6} | Tempos: {:<30}".format(self.id,self.prioridade,self.hora_entrada,aux)
# ---------------------------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE SUPORTE
# -------------------------------------------------------------------------------------------------------------------------------------------
def total_utentes(): # calcula o número total de utentes a modelar no sistema
    
    return(random.randint(120,150))

def gerar_utentes(num_utentes): # gerar todos os utentes que o sistema vai modelar
    
    utentes = []
    id_count = 1
    num_aux = 0

    # FASE 1
    # -----------------------------------------------------------------------------------------------
    for i in range(num_utentes):

        # gerar a prioridade
        if(random.randint(1,10)<=2): rand_prioridade = 2
        else: rand_prioridade = 0

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
    balcoes_C = list(set(fase_2)-set(balcoes_A)-set(balcoes_B))

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

    for i in balcoes_C: # atribuir tempos aos utentes que vão para os balcões B
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
    fase_3_C = random.sample(balcoes_C, int(0.75*len(balcoes_C)))

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
    for i in fase_3_A_voltam:
        i.prioridade = 1
        tempo_aux = i.tempos.get("A")
        i.tempos.update({"A":random.randint(1,tempo_aux)})
        i.tempos.update({"A_volta":tempo_aux-i.tempos.get("A")})

    for i in fase_3_B_voltam:
        i.prioridade = 1
        tempo_aux = i.tempos.get("B")
        i.tempos.update({"B":random.randint(1,tempo_aux)})
        i.tempos.update({"B_volta":tempo_aux-i.tempos.get("B")})

    for i in fase_3_C_voltam:
        i.prioridade = 1
        tempo_aux = i.tempos.get("C")
        i.tempos.update({"C":random.randint(1,tempo_aux)})
        i.tempos.update({"C_volta":tempo_aux-i.tempos.get("C")})
    # ----------------------------------------------------------------------------------

    for i in utentes: print(i.str())
    return(utentes)

def adicionar_fila(utente, fila): # adiciona o utente à fila passada como parâmetro

    if(utente.prioridade==0): # utente geral
        fila[1].append(utente)
    
    elif(utente.prioridade==1): # utente prioritário sobre os gerais
        fila[1].insert(0,utente)
    
    else: # utente prioritário
        fila[0].append(utente)

def escolher_fila(fila): # retorna o próximo utente a ser atendido na fila da fase dada

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

def proxima_chegada(utentes): # devolve a próxima chegada ao sistema

    proxima = 28800
    utente = None

    for i in utentes:
        if(i.estado_atual=="antes" and i.hora_entrada<proxima): 
            proxima = i.hora_entrada
            utente = i

    return(proxima,utente)

def proximo_evento(tabela): # calcula o próximo evento a considerar

    minimo = 28800
    evento = ""
    utente = tabela.get("utente")

    for k,v in tabela.items():
        if(k=="clock" or k=="tipo_evento" or k=="utente"): continue
        if(v<minimo):
            minimo = v
            evento = k
    
    return(minimo,evento,utente)

def parar_simulacao(tabela): # determina se devemos parar a simulação ou não

    parar = True
    infinito = 100000000

    for k,v in tabela.items():
        if(k=="clock" or k=="tipo_evento" or k=="utente"): continue
        if(v!=infinito): 
            parar = False
            break
    
    return(parar)

def calcular_tempos_espera(utentes):
    # TODO
    return

def calcular_taxas_ocupacao(utentes):
    # TODO
    return
# -------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    num_utentes = total_utentes()
    gerar_utentes(num_utentes)