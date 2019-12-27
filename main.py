import sys
from functions import *

# FILAS ([[P], [G]]) E BALCÕES
# ----------------------------
fila_fase_1 = [[],[]]
balcao_Tr = None

fila_fase_2_A = [[],[]]
balcao_A1 = None
balcao_A2 = None

fila_fase_2_B = [[],[]]
balcao_B1 = None
balcao_B2 = None

fila_fase_2_C = [[],[]]
balcao_C1 = None

fila_fase_3 = [[],[]]
balcao_Te = None
# ----------------------------

num_utentes = total_utentes()
utentes = gerar_utentes(num_utentes)
infinito = 100000000
utente_volta = False
nova_chegada = (28800,None)

tabela = []
formato = ["clock", "tipo_evento", "utente", "chegada", "partida_triagem", "partida_balcao_A1", "partida_balcao_A2", "partida_balcao_B1", "partida_balcao_B2", "partida_balcao_C1", "partida_tesouraria"]

tabela.append({"clock": 0, "tipo_evento": "chegada", "utente": proxima_chegada(utentes)[1], "chegada": proxima_chegada(utentes)[0], "partida_triagem": infinito, "partida_balcao_A1": infinito, "partida_balcao_A2": infinito, "partida_balcao_B1": infinito, "partida_balcao_B2": infinito, "partida_balcao_C1": infinito, "partida_tesouraria": infinito})

instante, tipo_evento, utente_atual = proximo_evento(tabela[-1])

balcao_Tr = utente_atual
utente_atual.estado = "triagem"

print("")
print("{:<6} | {:<17} | {:<3} | {:<11} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} |".format(" Clock","Evento","Utente","Chegada","Partida tr.","Partida b_A1","Partida b_A2","Partida b_B1","Partida b_B2","Partida b_C1","Partida te."))
print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in tabela:
    if(i.get("tipo_evento")==None):
        tipo = "None"
    else: tipo = i.get("tipo_evento")
    print("{:<6} | {:<17} | {:<6} | {:<11} | {:<11} | {:<12} | {:<12} | {:<12} | {:<12} | {:<12} | {:<11} |".format(i.get("clock"),"---","---",i.get("chegada"),i.get("partida_triagem"),i.get("partida_balcao_A1"),i.get("partida_balcao_A2"),i.get("partida_balcao_B1"),i.get("partida_balcao_B2"),i.get("partida_balcao_C1"),i.get("partida_tesouraria")))

while(not parar_simulacao(tabela[-1])): # simular o sistema
    
    if(not utente_volta):

        # COLOCAR ALGUNS DADOS NA TABELA
        # ---------------------------------------------------------------------------------------------------------------------------------------
        linha_tabela = {}
        linha_tabela.update({"clock": instante, "tipo_evento": tipo_evento, "utente": utente_atual, "chegada": proxima_chegada(utentes)[0]})
        # ---------------------------------------------------------------------------------------------------------------------------------------

    # CHEGADA AO SISTEMA (ENTRADA NA FASE 1)
    # ----------------------------------------------------------------------------------------
    if(tipo_evento=="chegada"):
        
        if(balcao_Tr==None): # balcão de triagem livre
            balcao_Tr = utente_atual
            linha_tabela.update({"partida_triagem": instante + utente_atual.tempos.get("tr")})
            utente_atual.estado_atual = "triagem"

        else: # balcão de triagem ocupado, o utente vai para a fila 
            adicionar_fila(utente_atual,fila_fase_1)
            utente_atual.chegadas_filas.update({"fila_fase_1": instante})
            utente_atual.estado_atual = "fila_fase_1"
            linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})
        
        # manter os valores da linha anterior da tabela para os restantes campos
        for i in formato[5:]: linha_tabela.update({i: tabela[-1].get(i)})
    # ----------------------------------------------------------------------------------------

    # PARTIDA DA TRIAGEM (ENTRADA NA FASE 2)
    # -------------------------------------------------------------------------------------------------------------------------------------------
    elif(tipo_evento=="partida_triagem" or utente_volta==True):

        # ATUALIZAR A PARTE DA TRIAGEM
        # -----------------------------------------------------------------------------------------
        if(not utente_volta):
            balcao_Tr = escolher_fila(fila_fase_1)

            if(balcao_Tr!=None): # balcão da tesouraria livre
                linha_tabela.update({"partida_triagem": instante + balcao_Tr.tempos.get("tr")})
                balcao_Tr.estado_atual = "triagem"
                balcao_Tr.tempo_de_espera += (instante-balcao_Tr.chegadas_filas.get("fila_fase_1"))

            else:
                linha_tabela.update({"partida_triagem": infinito})
        # -----------------------------------------------------------------------------------------
        
        # COLOCAR O UTENTE NUM DOS BALCÕES (OU FILAS) DA FASE 2
        # ---------------------------------------------------------------------------------------------------------------------------------------
        for i in ["A","B","C"]: # avaliar se há algum balcão para receber o utente, se não metê-lo numa fila
            if(i=="A"): 
                balcoes = [balcao_A1,balcao_A2]
                fila = fila_fase_2_A
            elif(i=="B"): 
                balcoes = [balcao_B1,balcao_B2]
                fila = fila_fase_2_B
            else:
                balcoes = [balcao_C1]
                fila = fila_fase_2_C
            
            if(utente_atual.tempos.get(i)!=None): # verificar para qual tipo de balcão o utente vai
                
                controlo = None
                for j in balcoes: # verificar se algum dos balcões deste tipo está disponível

                    if(j==None): # balcão livre
                        j = utente_atual
                        linha_tabela.update({"partida_balcao_" + i + str(balcoes.index(j)+1): instante + utente_atual.tempos.get(i)})
                        utente_atual.estado_atual = "balcao_" + i + str(balcoes.index(j)+1)
                        controlo = i + str(balcoes.index(j)+1)
                        break

                if(controlo==None): # todos os balcões deste tipo ocupados, o utente vai para a fila
                    adicionar_fila(utente_atual,fila)
                    utente_atual.chegadas_filas.update({"fila_fase_2_" + i: instante})
                    utente_atual.estado_atual = "fila_fase_2_" + i
                
                break

        for i in [b for b in ["A1","A2","B1","B2","C1"] if b!=controlo]: # os valores dos balcões para os quais o utente não foi mantêm-se iguais
            linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})

        if(not utente_atual.direto):
            linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
        
        else: # caso especial para os utentes que vão diretamente da triagem para a tesouraria (fase 1 -> fase 3)

            if(balcao_Te==None): # balcão de tesouraria livre
                balcao_Te = utente_atual
                linha_tabela.update({"partida_tesouraria": instante + utente_atual.tempos.get("te")})
                utente_atual.estado_atual = "tesouraria"

            else: # balcão da tesouraria ocupada, o utente vai para a fila
                adicionar_fila(utente_atual,fila_fase_3)
                utente_atual.chegadas_filas.update({"fila_fase_3": instante})
                utente_atual.estado_atual = "fila_fase_3"
                linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
        # ---------------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------------

    # PARTIDA DO SISTEMA OU RETROCESSO PARA A FASE 2
    # -------------------------------------------------------------------------------------------
    elif(tipo_evento=="partida_tesouraria"):

        linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})
        for i in ["A1","A2","B1","B2","C1"]: # os valores dos balcões mantêm-se iguais
            linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})

        # obter o balcão do utente
        if(utente_atual.tempos.get("A")!=None): balcao = "A"
        if(utente_atual.tempos.get("B")!=None): balcao = "B"
        if(utente_atual.tempos.get("C")!=None): balcao = "C"

        if(utente_atual.tempos.get(balcao + "_volta")!=None): # o utente vai voltar para a fase 2
            utente_volta = True
            continue

        else: utente_atual.estado_atual = "fora"

        balcao_Te = escolher_fila(fila_fase_3)

        if(balcao_Te!=None):
            linha_tabela.update({"partida_tesouraria": instante + balcao_Te.tempos.get("te")})
            balcao_Te.estado_atual = "tesouraria"
            balcao_Te.tempo_de_espera += (instante-balcao_Te.chegadas_filas.get("fila_fase_3"))

        else:
            linha_tabela.update({"partida_tesouraria": infinito})
    # -------------------------------------------------------------------------------------------

    # PARTIDA DE ALGUM BALCÃO A, B OU C
    # --------------------------------------------------------------------------------------------------
    else:

        linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})

        aux = tipo_evento.split("_")[-1]

        # ATUALIZAR A PARTE DOS BALCÕES
        # ----------------------------------------------------------------------------------------------------------
        balcoes = [balcao_A1,balcao_A2,balcao_B1,balcao_B2,balcao_C1]
        balcoes_nomes = ["A1","A2","B1","B2","C1"]

        balcao = balcoes[balcoes_nomes.index(aux)]

        if("A" in aux): fila = fila_fase_2_A
        elif("B" in aux): fila = fila_fase_2_B
        else: fila = fila_fase_2_C

        for i in [b for b in ["A1","A2","B1","B2","C1"] if b!=aux]: # os valores dos outros balcões mantêm-se iguais
            linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})

        balcao = escolher_fila(fila)

        if(balcao!=None):
            linha_tabela.update({"partida_balcao_" + aux: instante + balcao.tempos.get(str(aux[0]))})
            balcao.estado_atual = "balcao_" + aux
            balcao.tempo_de_espera += (instante-balcao.chegadas_filas.get("fila_fase_2_" + str(aux[0])))

        else:
            linha_tabela.update({"partida_balcao_" + aux: infinito})
        # ----------------------------------------------------------------------------------------------------------

        # SEGUIR COM O UTENTE QUE SAIU DOS BALCÕES (ENTROU NA FASE 3)
        # -------------------------------------------------------------------------------------------
        if(utente_atual.tempos.get("Te")==None): # o utente sai do sistema sem passar pela tesouraria
            utente_atual.estado_atual = "fora"

        else:
            if(balcao_Te==None): # balcão de tesouraria livre
                balcao_Te = utente_atual
                linha_tabela.update({"partida_tesouraria": instante + utente_atual.tempos.get("te")})
                utente_atual.estado_atual = "tesouraria"
            else:
                adicionar_fila(utente_atual,fila_fase_3)
                utente_atual.chegadas_filas.update({"fila_fase_3": instante})
                utente_atual.estado_atual = "fila_fase_3"
                linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
        # -------------------------------------------------------------------------------------------

    # atualizar a tabela
    tabela.append(linha_tabela)

    # escolher o próximo evento
    instante, tipo_evento, utente_atual = proximo_evento(tabela[-1])
    utente_volta = False

    if(linha_tabela.get("tipo_evento")==None):
        tipo = "None"
    else: tipo = linha_tabela.get("tipo_evento")
    print("{:<6} | {:<17} | {:<6} | {:<11} | {:<11} | {:<12} | {:<12} | {:<12} | {:<12} | {:<12} | {:<11} |".format(linha_tabela.get("clock"),tipo,(linha_tabela.get("utente")).id,linha_tabela.get("chegada"),linha_tabela.get("partida_triagem"),linha_tabela.get("partida_balcao_A1"),linha_tabela.get("partida_balcao_A2"),linha_tabela.get("partida_balcao_B1"),linha_tabela.get("partida_balcao_B2"),linha_tabela.get("partida_balcao_C1"),linha_tabela.get("partida_tesouraria")))


'''
print("{:<6} | {:<10} | {:<3} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} |".format("Clock","Tipo evento","Utente","Próxima chegada","Partida triagem","Partida balcão A1","Partida balcão A2","Partida balcão B1","Partida balcão B2","Partida balcão C1","Partida tesouraria"))
for i in tabela:
    if(i.get("tipo_utente")==None):
        tipo = "None"
    else: tipo = i.get("tipo_utente")
    print("{:<6} | {:<10} | {:<3} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} | {:<6} |".format(i.get("clock"),tipo,(i.get("utente")).id,i.get("proxima_chegada"),i.get("partida_triagem"),i.get("partida_balcao_A1"),i.get("partida_balcao_A2"),i.get("partida_balcao_B1"),i.get("partida_balcao_B2"),i.get("partida_balcao_C1"),i.get("partida_tesouraria")))'''