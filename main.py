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

# PREPARATIVOS INICIAIS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
num_utentes = total_utentes()
utentes = gerar_utentes(num_utentes)
infinito = 100000000
utente_volta = False # serve para reutilizar o código da partida da triagem quando há uma reentrada na fase 2
iteracoes = 0

tabela = [] # tabela com a simulação completa
formato = ["clock", "tipo_evento", "utente", "proxima_chegada", "partida_triagem", "partida_balcao_A1", "partida_balcao_A2", "partida_balcao_B1", "partida_balcao_B2", "partida_balcao_C1", "partida_tesouraria"] # colunas a usar na tabela
tabela.append({"clock": 0, "tipo_evento": "chegada", "utente": proxima_chegada(utentes)[1], "proxima_chegada": proxima_chegada(utentes)[0], "partida_triagem": infinito, "partida_balcao_A1": infinito, "partida_balcao_A2": infinito, "partida_balcao_B1": infinito, "partida_balcao_B2": infinito, "partida_balcao_C1": infinito, "partida_tesouraria": infinito}) # primeira linha da tabela

# primeiro utente e primeiro evento
instante, tipo_evento, utente_atual = proximo_evento(tabela[-1],utentes,balcao_Tr,balcao_Te,balcao_A1,balcao_A2,balcao_B1,balcao_B2,balcao_C1)
utente_atual.percurso += "triagem "

# IMPRIMIR CABEÇALHO E PRIMEIRA LINHA DA TABELA
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\n# TABELA")
print("--------")
print("| {:<6} | {:<18} | {:<3} | {:<11} | {:<60} | {:<6} | {:<6} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<60} | {:<6} | {:<6} |".format("Clock","Evento","Utente","Próx. chegada","Fila triagem","Estado tr.","Partida tr.","Fila balcões A","Estado A1","Partida A1","Estado A2","Partida A2","Fila balcões B","Estado B1","Partida B1","Estado B2","Partida B2","Fila balcão C","Estado C1","Partida C1","Fila tesouraria","Estado te.","Partida te."))
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in tabela:
    if(i.get("tipo_evento")==None):
        tipo = "None"
    else: tipo = i.get("tipo_evento")
    print("| {:<6} | {:<18} | {:<6} | {:<13} | {:<60} | {:<10} | {:<11} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<11} | {:<12} | {:<60} | {:<11} | {:<12} | {:<60} | {:<10} | {:<11} |".format(i.get("clock"),"------","------",i.get("proxima_chegada"),"P:  G:  ","None","inf.","P:  G:  ","None","inf.","None","inf.","P:  G:  ","None","inf.","None","inf.","P:  G:  ","None","inf.","P:  G:  ","None","inf."))
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# SIMULAR O SISTEMA
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while(not parar_simulacao(tabela[-1])):

    if(not utente_volta): # preparativos iniciais

        if(tipo_evento=="proxima_chegada"): tipo_evento = "chegada"
        linha_tabela = {}

    # ENTRADA NA FASE 1
    # ----------------------------------------------------------------------------------------
    if(tipo_evento=="chegada"):
        
        if(balcao_Tr==None): # balcão de triagem livre
            balcao_Tr = utente_atual
            linha_tabela.update({"partida_triagem": instante + utente_atual.tempos.get("tr")})
            utente_atual.percurso += "triagem "

        else: # balcão de triagem ocupado, o utente vai para a fila de espera da triagem
            adicionar_fila(utente_atual,fila_fase_1)
            utente_atual.chegadas_filas.update({"fila_fase_1": instante})
            utente_atual.percurso += "fila_fase_1 "
            linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})
        
        # manter os valores da linha anterior da tabela para os restantes campos
        for i in formato[5:]: linha_tabela.update({i: tabela[-1].get(i)})
    # ----------------------------------------------------------------------------------------

    # ENTRADA/REENTRADA NA FASE 2 OU ENTRADA DIRETA NA FASE 3
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif(tipo_evento=="partida_triagem" or utente_volta==True):

        if(not utente_volta):
            # ATUALIZAR A PARTE DA TRIAGEM
            # ------------------------------------------------------------------------------------------------------------------------------------------------------
            balcao_Tr = escolher_fila(fila_fase_1)

            if(balcao_Tr!=None): # balcão da tesouraria livre
                linha_tabela.update({"partida_triagem": instante + balcao_Tr.tempos.get("tr")})
                balcao_Tr.percurso += "triagem "
                balcao_Tr.tempos_espera.update({"fila_fase_1": balcao_Tr.tempos_espera.get("fila_fase_1") + (instante-balcao_Tr.chegadas_filas.get("fila_fase_1"))})

            else:
                linha_tabela.update({"partida_triagem": infinito})
            # ------------------------------------------------------------------------------------------------------------------------------------------------------

            # ATUALIZAR A PARTE DA TESOURARIA
            # -------------------------------------------------------------------------------------------------------
            if(not utente_atual.direto):
                linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
            
            else: # caso especial para os utentes que vão diretamente da triagem para a tesouraria (fase 1 -> fase 3)

                if(balcao_Te==None): # balcão de tesouraria livre
                    balcao_Te = utente_atual
                    linha_tabela.update({"partida_tesouraria": instante + utente_atual.tempos.get("te")})
                    utente_atual.percurso += "tesouraria "

                else: # balcão da tesouraria ocupada, o utente vai para a fila
                    adicionar_fila(utente_atual,fila_fase_3)
                    utente_atual.chegadas_filas.update({"fila_fase_3": instante})
                    utente_atual.percurso += "fila_fase_3 "
                    linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
            # -------------------------------------------------------------------------------------------------------
        
        # COLOCAR O UTENTE NUM DOS BALCÕES (OU FILAS) DA FASE 2
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------
        # avaliar se há algum balcão para receber o utente, se não metê-lo numa fila
        controlo = None

        if(utente_atual.tempos.get("A")!=None or (utente_volta==True and utente_atual.tempos.get("A_volta")!=None)): # o utente pretende ir para um balcão do tipo A
            
            # avaliar que tempo será usado (o da primeira vez que o utente vai para um balcão ou quando reentra (se reentrar) na fase 2)
            if(utente_volta): 
                tempo_aux = utente_atual.tempos.get("A_volta")
                utente_atual.retrocesso_feito = True
            else: tempo_aux = utente_atual.tempos.get("A")

            if(balcao_A1==None): # balcão A1 livre
                balcao_A1 = utente_atual
                linha_tabela.update({"partida_balcao_A1": instante + tempo_aux})
                if(not utente_volta):
                    utente_atual.percurso += "balcao_A1 "
                else:
                    utente_atual.percurso += "balcao_A1_volta "
                controlo = "A1"

            elif(balcao_A2==None): # balcão A2 livre
                balcao_A2 = utente_atual
                linha_tabela.update({"partida_balcao_A2": instante + tempo_aux})
                if(not utente_volta):
                    utente_atual.percurso += "balcao_A2 "
                else:
                    utente_atual.percurso += "balcao_A2_volta "
                controlo = "A2"

            if(controlo==None): # todos os balcões deste tipo ocupados, o utente vai para a fila
                adicionar_fila(utente_atual,fila_fase_2_A)
                if(not utente_volta):
                    utente_atual.chegadas_filas.update({"fila_fase_2_A": instante})
                    utente_atual.percurso += "fila_fase_2_A "
                else:
                    utente_atual.chegadas_filas.update({"fila_fase_2_A_volta": instante})
                    utente_atual.percurso += "fila_fase_2_A_volta "

        elif(utente_atual.tempos.get("B")!=None or (utente_volta==True and utente_atual.tempos.get("B_volta")!=None)): # o utente pretende ir para um balcão do tipo B

            # avaliar que tempo será usado (o da primeira vez que o utente vai para um balcão ou quando reentra (se reentrar) na fase 2)
            if(utente_volta): 
                tempo_aux = utente_atual.tempos.get("B_volta")
                utente_atual.retrocesso_feito = True
            else: tempo_aux = utente_atual.tempos.get("B")

            if(balcao_B1==None): # balcão B1 livre
                balcao_B1 = utente_atual
                linha_tabela.update({"partida_balcao_B1": instante + tempo_aux})
                if(not utente_volta):
                    utente_atual.percurso += "balcao_B1 "
                else:
                    utente_atual.percurso += "balcao_B1_volta "
                controlo = "B1"

            elif(balcao_B2==None): # balcão B2 livre
                balcao_B2 = utente_atual
                linha_tabela.update({"partida_balcao_B2": instante + tempo_aux})
                if(not utente_volta):
                    utente_atual.percurso += "balcao_B2 "
                else:
                    utente_atual.percurso += "balcao_B2_volta "
                controlo = "B2"

            if(controlo==None): # todos os balcões deste tipo ocupados, o utente vai para a fila
                adicionar_fila(utente_atual,fila_fase_2_B)
                if(not utente_volta):
                    utente_atual.chegadas_filas.update({"fila_fase_2_B": instante})
                    utente_atual.percurso += "fila_fase_2_B "
                else:
                    utente_atual.chegadas_filas.update({"fila_fase_2_B_volta": instante})
                    utente_atual.percurso += "fila_fase_2_B_volta "

        elif(utente_atual.tempos.get("C")!=None or (utente_volta==True and utente_atual.tempos.get("C_volta")!=None)): # o utente pretende ir para um balcão do tipo B

            # avaliar que tempo será usado (o da primeira vez que o utente vai para um balcão ou quando reentra (se reentrar) na fase 2)
            if(utente_volta): 
                tempo_aux = utente_atual.tempos.get("C_volta")
                utente_atual.retrocesso_feito = True
            else: tempo_aux = utente_atual.tempos.get("C")

            if(balcao_C1==None): # balcão C1 livre
                balcao_C1 = utente_atual
                linha_tabela.update({"partida_balcao_C1": instante + tempo_aux})
                if(not utente_volta):
                    utente_atual.percurso += "balcao_C1 "
                else:
                    utente_atual.percurso += "balcao_C1_volta "
                controlo = "C1"

            if(controlo==None): # todos os balcões deste tipo ocupados, o utente vai para a fila
                adicionar_fila(utente_atual,fila_fase_2_C)
                if(not utente_volta):
                    utente_atual.chegadas_filas.update({"fila_fase_2_C": instante})
                    utente_atual.percurso += "fila_fase_2_C "
                else:
                    utente_atual.chegadas_filas.update({"fila_fase_2_C_volta": instante})
                    utente_atual.percurso += "fila_fase_2_C_volta "

        if(not utente_volta):
            # os valores dos balcões para os quais o utente não foi mantêm-se iguais
            for i in [b for b in ["A1","A2","B1","B2","C1"] if b!=controlo]:
                linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # PARTIDA DO SISTEMA OU RETROCESSO PARA A FASE 2
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    elif(tipo_evento=="partida_tesouraria"):
        
        # manter os valores das restantes colunas
        linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})
        for i in ["A1","A2","B1","B2","C1"]:
            linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})

        # obter o balcão do utente
        balcao = ""
        if(utente_atual.tempos.get("A")!=None): balcao = "A"
        if(utente_atual.tempos.get("B")!=None): balcao = "B"
        if(utente_atual.tempos.get("C")!=None): balcao = "C"

        # ATUALIZAR A PARTE DA TESOURARIA
        # ------------------------------------------------------------------------------------------------------------------------------------------------------
        balcao_Te = escolher_fila(fila_fase_3)

        if(balcao_Te!=None):
            linha_tabela.update({"partida_tesouraria": instante + balcao_Te.tempos.get("te")})
            balcao_Te.percurso += "tesouraria "
            balcao_Te.tempos_espera.update({"fila_fase_3": balcao_Te.tempos_espera.get("fila_fase_3") + (instante-balcao_Te.chegadas_filas.get("fila_fase_3"))})

        else:
            linha_tabela.update({"partida_tesouraria": infinito})

        if(utente_atual.tempos.get(balcao + "_volta")!=None): # o utente vai voltar para a fase 2
            utente_volta = True
            continue

        else: utente_atual.percurso += "fora "
        # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------

    # PARTIDA DE ALGUM BALCÃO A, B OU C
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        linha_tabela.update({"partida_triagem": tabela[-1].get("partida_triagem")})
        aux = tipo_evento.split("_")[-1]

        # ATUALIZAR A PARTE DOS BALCÕES
        # ---------------------------------------------------------------------------------------------------------------------------------
        if("A" in aux): fila = fila_fase_2_A
        elif("B" in aux): fila = fila_fase_2_B
        else: fila = fila_fase_2_C

        for i in [b for b in ["A1","A2","B1","B2","C1"] if b!=aux]: # os valores dos outros balcões mantêm-se iguais
            linha_tabela.update({"partida_balcao_" + i: tabela[-1].get("partida_balcao_" + i)})

        if(aux=="A1"): 
            balcao_A1 = escolher_fila(fila)

            if(balcao_A1!=None):
                linha_tabela.update({"partida_balcao_A1": instante + balcao_A1.tempos.get("A")})
                balcao_A1.percurso += "balcao_A1 "

                if(balcao_A1.prioridade=="R" and balcao_A1.retrocesso_feito):
                    balcao_A1.tempos_espera.update({"fila_fase_2_A_volta": (instante-balcao_A1.chegadas_filas.get("fila_fase_2_A_volta"))})
                else:
                    balcao_A1.tempos_espera.update({"fila_fase_2_A": (instante-balcao_A1.chegadas_filas.get("fila_fase_2_A"))})

            else:
                linha_tabela.update({"partida_balcao_A1": infinito})

        elif(aux=="A2"): 
            balcao_A2 = escolher_fila(fila)

            if(balcao_A2!=None):
                linha_tabela.update({"partida_balcao_A2": instante + balcao_A2.tempos.get("A")})
                balcao_A2.percurso += "balcao_A2 "
                
                if(balcao_A2.prioridade=="R" and balcao_A2.retrocesso_feito):
                    balcao_A2.tempos_espera.update({"fila_fase_2_A_volta": (instante-balcao_A2.chegadas_filas.get("fila_fase_2_A_volta"))})
                else:
                    balcao_A2.tempos_espera.update({"fila_fase_2_A": (instante-balcao_A2.chegadas_filas.get("fila_fase_2_A"))})

            else:
                linha_tabela.update({"partida_balcao_A2": infinito})

        elif(aux=="B1"): 
            balcao_B1 = escolher_fila(fila)

            if(balcao_B1!=None):
                linha_tabela.update({"partida_balcao_B1": instante + balcao_B1.tempos.get("B")})
                balcao_B1.percurso += "balcao_B1 "
                
                if(balcao_B1.prioridade=="R" and balcao_B1.retrocesso_feito):
                    balcao_B1.tempos_espera.update({"fila_fase_2_B_volta": (instante-balcao_B1.chegadas_filas.get("fila_fase_2_B_volta"))})
                else:
                    balcao_B1.tempos_espera.update({"fila_fase_2_B": (instante-balcao_B1.chegadas_filas.get("fila_fase_2_B"))})

            else:
                linha_tabela.update({"partida_balcao_B1": infinito})

        elif(aux=="B2"): 
            balcao_B2 = escolher_fila(fila)

            if(balcao_B2!=None):
                linha_tabela.update({"partida_balcao_B2": instante + balcao_B2.tempos.get("B")})
                balcao_B2.percurso += "balcao_B2 "
                
                if(balcao_B2.prioridade=="R" and balcao_B2.retrocesso_feito):
                    balcao_B2.tempos_espera.update({"fila_fase_2_B_volta": (instante-balcao_B2.chegadas_filas.get("fila_fase_2_B_volta"))})
                else:
                    balcao_B2.tempos_espera.update({"fila_fase_2_B": (instante-balcao_B2.chegadas_filas.get("fila_fase_2_B"))})

            else:
                linha_tabela.update({"partida_balcao_B2": infinito})

        elif(aux=="C1"): 
            balcao_C1 = escolher_fila(fila)

            if(balcao_C1!=None):
                linha_tabela.update({"partida_balcao_C1": instante + balcao_C1.tempos.get("C")})
                balcao_C1.percurso += "balcao_C1 "
                
                if(balcao_C1.prioridade=="R" and balcao_C1.retrocesso_feito):
                    balcao_C1.tempos_espera.update({"fila_fase_2_C_volta": (instante-balcao_C1.chegadas_filas.get("fila_fase_2_C_volta"))})
                else:
                    balcao_C1.tempos_espera.update({"fila_fase_2_C": (instante-balcao_C1.chegadas_filas.get("fila_fase_2_C"))})

            else:
                linha_tabela.update({"partida_balcao_C1": infinito})
        # ---------------------------------------------------------------------------------------------------------------------------------

        # SEGUIR COM O UTENTE QUE SAIU DOS BALCÕES (ENTRADA NA FASE 3) OU SAÍDA DO SISTEMA
        # ----------------------------------------------------------------------------------------------------------------------------------

        if(utente_atual.tempos.get("te")==None or utente_atual.retrocesso_feito==True): # o utente sai do sistema sem passar pela tesouraria
            utente_atual.percurso += "fora "
            linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
        else:
            if(balcao_Te==None): # balcão de tesouraria livre
                balcao_Te = utente_atual
                linha_tabela.update({"partida_tesouraria": instante + utente_atual.tempos.get("te")})
                utente_atual.percurso += "tesouraria "
            else:
                adicionar_fila(utente_atual,fila_fase_3)
                utente_atual.chegadas_filas.update({"fila_fase_3": instante})
                utente_atual.percurso += "fila_fase_3 "
                linha_tabela.update({"partida_tesouraria": tabela[-1].get("partida_tesouraria")})
        # ----------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # CALCULAR ALGUNS DADOS EM FALTA NESTA LINHA DA TABELA
    # ------------------------------------------------------------------------------------------------------------------------------------------
    linha_tabela.update({"clock": instante, "tipo_evento": tipo_evento, "utente": utente_atual, "proxima_chegada": proxima_chegada(utentes)[0]})
    # ------------------------------------------------------------------------------------------------------------------------------------------

    # FIM DE ITERAÇÃO
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # atualizar a tabela
    tabela.append(linha_tabela)

    # imprimir a última linha da tabela
    imprimir_linha_tabela(utente_atual,linha_tabela,fila_fase_1,balcao_Tr,fila_fase_2_A,balcao_A1,balcao_A2,fila_fase_2_B,balcao_B1,balcao_B2,fila_fase_2_C,balcao_C1,fila_fase_3,balcao_Te)

    # escolher o próximo evento
    instante, tipo_evento, utente_atual = proximo_evento(tabela[-1],utentes,balcao_Tr,balcao_Te,balcao_A1,balcao_A2,balcao_B1,balcao_B2,balcao_C1)
    
    utente_volta = False
    iteracoes+=1
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print("--------")

# APRESENTAR OS TEMPOS DE ESPERA E TAXAS DE OCUPAÇÃO
# -----------------------------------------------------------------------------------------------------------------------------------------------------
print("\n# TEMPOS DE ESPERA MÍNIMOS, MÉDIOS E MÁXIMOS")
print("--------------------------------------------")
tempos_parciais_fase_1,tempos_parciais_fase_2,tempos_parciais_fase_3,tempos_globais = calcular_tempos_espera(utentes,num_utentes,tabela[-1].get("clock"))
print("## Tempos de espera na Fase 1 (triagem)")
for k,v in tempos_parciais_fase_1.items():
    intervalo = ""
    if(k=="0"): intervalo = "9-11h OU 0-7200s"
    elif(k=="1"): intervalo = "11-13h OU 7200-14400s"
    elif(k=="2"): intervalo = "13-15h OU 14400-21600s"
    elif(k=="3"): intervalo = "15-17h OU 21600-28800s"
    elif(k=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
    else: intervalo = "TOTAL"
    if(v.get("minimo")=="-"):
        print(intervalo + " => mínimo: - médio: - máximo: -")
    else:
        print((intervalo + " => mínimo: " + str(v.get("minimo")) + " médio: {:0.2f} máximo: " + str(v.get("maximo"))).format(v.get("medio")))

print("\n## Tempos de espera na Fase 2 (balcões)")
for k,v in tempos_parciais_fase_2.items():
    
    if(k=="A"): # balcões de tipo A
        print("| Balcões de tipo A")
        for k_2,v_2 in v.items():
            intervalo = ""
            if(k_2=="0"): intervalo = "9-11h OU 0-7200s"
            elif(k_2=="1"): intervalo = "11-13h OU 7200-14400s"
            elif(k_2=="2"): intervalo = "13-15h OU 14400-21600s"
            elif(k_2=="3"): intervalo = "15-17h OU 21600-28800s"
            elif(k_2=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
            else: intervalo = "TOTAL"
            if(v_2.get("minimo")=="-"):
                print(intervalo + " => mínimo: - médio: - máximo: -")
            else:
                print((intervalo + " => mínimo: " + str(v_2.get("minimo")) + " médio: {:0.2f} máximo: " + str(v_2.get("maximo"))).format(v_2.get("medio")))

    elif(k=="B"): # balcões de tipo B
        print("\n| Balcões de tipo B")
        for k_2,v_2 in v.items():
            intervalo = ""
            if(k_2=="0"): intervalo = "9-11h OU 0-7200s"
            elif(k_2=="1"): intervalo = "11-13h OU 7200-14400s"
            elif(k_2=="2"): intervalo = "13-15h OU 14400-21600s"
            elif(k_2=="3"): intervalo = "15-17h OU 21600-28800s"
            elif(k_2=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
            else: intervalo = "TOTAL"
            if(v_2.get("minimo")=="-"):
                print(intervalo + " => mínimo: - médio: - máximo: -")
            else:
                print((intervalo + " => mínimo: " + str(v_2.get("minimo")) + " médio: {:0.2f} máximo: " + str(v_2.get("maximo"))).format(v_2.get("medio")))

    else: # balcões de tipo A
        print("\n| Balcão de tipo C")
        for k_2,v_2 in v.items():
            intervalo = ""
            if(k_2=="0"): intervalo = "9-11h OU 0-7200s"
            elif(k_2=="1"): intervalo = "11-13h OU 7200-14400s"
            elif(k_2=="2"): intervalo = "13-15h OU 14400-21600s"
            elif(k_2=="3"): intervalo = "15-17h OU 21600-28800s"
            elif(k_2=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
            else: intervalo = "TOTAL"
            if(v_2.get("minimo")=="-"):
                print(intervalo + " => mínimo: - médio: - máximo: -")
            else:
                print((intervalo + " => mínimo: " + str(v_2.get("minimo")) + " médio: {:0.2f} máximo: " + str(v_2.get("maximo"))).format(v_2.get("medio")))

print("\n## Tempos de espera na Fase 3 (tesouraria)")
for k,v in tempos_parciais_fase_3.items():
    intervalo = ""
    if(k=="0"): intervalo = "9-11h OU 0-7200s"
    elif(k=="1"): intervalo = "11-13h OU 7200-14400s"
    elif(k=="2"): intervalo = "13-15h OU 14400-21600s"
    elif(k=="3"): intervalo = "15-17h OU 21600-28800s"
    elif(k=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
    else: intervalo = "TOTAL"
    if(v.get("minimo")=="-"):
        print(intervalo + " => mínimo: - médio: - máximo: -")
    else:
        print((intervalo + " => mínimo: " + str(v.get("minimo")) + " médio: {:0.2f} máximo: " + str(v.get("maximo"))).format(v.get("medio")))

print("\n## Tempos de espera globais")
for k,v in tempos_globais.items():
    intervalo = ""
    if(k=="0"): intervalo = "0-7200s"
    elif(k=="1"): intervalo = "7200-14400s"
    elif(k=="2"): intervalo = "14400-21600s"
    elif(k=="3"): intervalo = "21600-28800s"
    elif(k=="4"): intervalo = ">17h OU 28800-" + str(tabela[-1].get("clock")) + "s"
    else: intervalo = "TOTAL"
    if(v.get("minimo")=="-"):
        print(intervalo + " => mínimo: - médio: - máximo: -")
    else:
        print((intervalo + " => mínimo: " + str(v.get("minimo")) + " médio: {:0.2f} máximo: " + str(v.get("maximo"))).format(v.get("medio")))
print("--------------------------------------------")

print("\n# TAXAS DE OCUPAÇÃO")
print("-------------------")
taxas = calcular_taxas_ocupacao(utentes,tabela[-1].get("clock"))
for k,v in taxas.items():
    print("> " + k.capitalize())
    for k_2,v_2 in v.items():
        intervalo = ""
        if(k_2=="0"): intervalo = "0-7200s"
        elif(k_2=="1"): intervalo = "7200-14400s"
        elif(k_2=="2"): intervalo = "14400-21600s"
        elif(k_2=="3"): intervalo = "21600-28800s"
        elif(k_2=="4"): intervalo = "28800-" + str(tabela[-1].get("clock")) + "s"
        else: intervalo = "TOTAL"
        print(intervalo + " => %.2f%%" % (v_2))
    if(k!="tesouraria"): print("") # só para ficar bonito
print("-------------------")
# -----------------------------------------------------------------------------------------------------------------------------------------------------