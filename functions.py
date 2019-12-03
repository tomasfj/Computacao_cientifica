import numpy as np
#oioioio

class Utente:
    def __init__(self, prioridade, horaEntrada, saida_fase1, saida_fase2, saida_fase3, balcao_Fase2, tempoAt_Balcao_Fase1, tempoAt_BalcaoA_Fase2, tempoAt_BalcaoB_Fase2, tempoAt_BalcaoC_Fase2, tempoAt_Balcao_Fase3):
        self.prioridade = prioridade
        self.horaEntrada = horaEntrada
        self.saida_fase1 = saida_fase1
        self.saida_fase2 = saida_fase2
        self.saida_fase3 = saida_fase3
        self.balcao_Fase2 = balcao_Fase2
        self.tempoAt_Balcao_Fase1 = tempoAt_Balcao_Fase1
        self.tempoAt_BalcaoA_Fase2 = tempoAt_BalcaoA_Fase2
        self.tempoAt_BalcaoB_Fase2 = tempoAt_BalcaoB_Fase2
        self.tempoAt_BalcaoC_Fase2 = tempoAt_BalcaoC_Fase2
        self.tempoAt_Balcao_Fase3 = tempoAt_Balcao_Fase3


# prioridade (0 => geral, 1 => prioritario pos pagamento, 2 => prioritario geral)  --NOT NULL  --PODE MUDAR DURANTE O PROGRAMA
# horaEntrada (entre 9h e 17h)  --NOT NULL
# saida_fase1 (2 => vai para fase 2, 3 => vai para fase 3(saida_fase3 = 0) )  --NOT NULL
# saida_fase2 (0 => sai do sistema, 3 => vai para fase 3(saida_fase3 = 1) )   --NOT NULL
# saida_fase3 (0 => sai do sistema, 2 => vai para fase 2(saida_fase2 = 0) )   --NOT NULL
# balcao_Fase2 (1 => balcao A, 2 => balcao B, 3 => balcao C)
# tempoAt_Balcao_Fase1 (entre 0 min e 3 min)     --NOT NULL
# tempoAt_BalcaoA_Fase2 (entre 0 min e 30 min)   
# tempoAt_BalcaoB_Fase2 (entre 0 min e 20 min)   
# tempoAt_BalcaoC_Fase2 (entre 0 min e 20 min)   
# tempoAt_Balcao_Fase3 (entre 0 min e 3 min)

# exmeplo: utente1 = utente(0, 9, 2, 0, 1, 1, 2, 3, 4, 5);

# FILAS FASE 1
list_Fase1_Geral = [];
list_Fase1_Prioritaria = []
# FILAS FASE 2
list_Fase2_BalcaoA = []
list_Fase2_BalcaoB = []
list_Fase2_BalcaoC = []

# Adicionar o novo utente a uma das filas da Fase 1 (adiciona ao fim das listas)
def entradaNoSistema(utente):
    if(utente.prioridade == 0):
        list_Fase1_Geral.append(utente)
    elif (utente.prioridade == 2):
        list_Fase1_Prioritaria.append(utente)


# Retorna o proximo utente a ser atendido na Fase 1
def escolherAt_Fase1():
    if(not list_Fase1_Prioritaria):            # se a fila prioritaria estiver vazia
        if(not list_Fase1_Geral):
            return(-1)                         # lista geral e lista prioritaria vazias
        else:
            return(list_Fase1_Geral.pop(0))    # devovle primeiro index da lista geral
    else:
        return(list_Fase1_Prioritaria.pop(0))  # devovle primeiro index da lista prioritaria


def addToFila_Fase2(utente):
    if(utente.balcao_Fase2 == 1):
        list_Fase2_BalcaoA.append(utente)
    elif(utente.balcao_Fase2 == 2):
        list_Fase2_BalcaoB.append(utente)
    #elif("ACABAR")


# colocar a percentagem como input. Se 1 então saiu dentro da percentagem e 0 se saiu fora
def random(percent):
    x = np.random.randint(low = 0, high = 101)
    print(x)
    if(x <= percent):
        return(1)
    else:
        return(0)

def totalUtentes():
    return( np.random.randint(low = 120, high = 151) )




# BEGIN

totalUtentes = totalUtentes()
listaUtentes = []
