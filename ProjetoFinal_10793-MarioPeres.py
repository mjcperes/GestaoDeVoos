# -*- coding: utf-8 -*-

# PROJETO FINAL UFCD 10793 - FUNDAMENTOS DE PYTHON

# GESTÃO DE VOOS DE COMPANHIA AÉREA

import csv
import pandas as pd
import os
import Recursos as Rc



# Criação da função main() onde se iniciará o programa
def main():
    # Menu com as várias opções do programa
    print(
        f"\n1 - Inserir voos"        
        f"\n2 - Inserir/consultar/atualizar aeronaves"
        f"\n3 - Inserir/consultar/apagar rotas"
        f"\n4 - Informação de voos"
        f"\n5 - Sair"
    )    
    # validação opções do menu
    try:
         opcaoMenu=int(input("Digite uma opção do menu [1 a 5]: "))
         while opcaoMenu<1 or opcaoMenu>5:
              print('Por favor digite uma opção correta [1 a 5]')
              continua()
    except ValueError:
         print('Por favor digite uma opção correta [1 a 5]')
         continua()
         
    # INSERÇÃO DE VOOS
    if opcaoMenu==1:
        voo1=Rc.Voos()
        voo1.inserirVoo()
        continua()    
    
    # MANIPULAÇÃO DE AERONAVES
    elif opcaoMenu==2:
        print('\n1 - Inserir aeronave / 2 - Consultar aeronaves / 3 - Atualizar aeronave')        
        opcaoAeronave=int(input('Indique a sua opção (1, 2 ou 3): '))        
        if opcaoAeronave==1:
             tipoAeronave=int(input('\nIndique o tipo de aeronave (1-Turboprop / 2-Jato): '))
             if tipoAeronave==1:
                 aviao1=Rc.Aeronaves('Turboprop')
                 aviao1.inserirAeronave()
                 continua()
             elif tipoAeronave==2:
                 aviao1=Rc.AeronavesJato('Jato')
                 aviao1.inserirAeronave()
                 continua()
             else:
                  print('Escolha incorreta! Por favor escolha apenas opções válidas!')
                  continua()  
        elif opcaoAeronave==2:
             tipoConsulta=input('\nIndique se pretende consultar lista de aeronaves (L/l) ou apenas uma aeronave (A/a): ')
             if tipoConsulta=='L' or tipoConsulta=='l':
                  linhas=int(input('Indique o número máximo de linhas do relatório: '))
                  aviao2=Rc.Aeronaves('Turboprop') # é indiferente neste caso criar o objeto da classe pai ou filha
                  aviao2.consultaAeronaves(linhas, '')
                  continua()
             elif tipoConsulta=='A' or tipoConsulta=='a':
                  matr=input('Indique a matrícula da aeronave a consultar: ')
                  aviao2=Rc.Aeronaves('Turboprop')
                  aviao2.consultaAeronaves(1, matr) # consulta de apenas 1 linha com a matrícula escolhida
                  continua()
        elif opcaoAeronave==3:
             matrAtualizar=input('Indique a matrícula da aeronave a atualizar: ')
             opcaoAtualiza=input('Indique se pretende alterar estado ativa/inativa (T/t) ou se pretende remover (R/r): ')
             opcaoAtualiza=opcaoAtualiza.upper()
             aviao3=Rc.Aeronaves('Turboprop')
             aviao3.atualizaAeronave(matrAtualizar, opcaoAtualiza)
             continua()
        else:
             print('Escolha incorreta! Por favor escolha apenas opções válidas!')
             continua()
    
    # MANIPULAÇÃO DE ROTAS
    elif opcaoMenu==3:
         print('\n1 - Inserir rota / 2 - Consultar rotas / 3 - Apagar rota')
         opcaoRota=int(input('Indique a sua opção (1, 2 ou 3): '))
         if opcaoRota==1:              
              rota1=Rc.Rotas()
              rota1.inserirRota()
              continua()
         elif opcaoRota==2:
              tpCons=input('\nIndique se pretende consultar lista de rotas (L/l) ou apenas uma rota (A/a): ')
              tpCons=tpCons.upper()
              if tpCons=='L':
                  linhas=int(input('Indique o número máximo de linhas do relatório: '))
                  rota2=Rc.Rotas()
                  rota2.consultaRotas(linhas, '')
                  continua()
              elif tpCons=='A':
                  idRota=str(input('Indique a rota a consultar: '))
                  rota2=Rc.Rotas()
                  rota2.consultaRotas(1, idRota) # consulta de apenas 1 linha com o idRota escolhido
                  continua()
         elif opcaoRota==3:
              apagaRota=input('Indique o ID da rota a apagar: ')
              rota3=Rc.Rotas()
              rota3.atualizaRota(apagaRota)
              continua()
         else:
             print('Escolha incorreta! Por favor escolha apenas opções válidas!')
             continua()
    
    # INFORMAÇÃO DE VOOS
    elif opcaoMenu==4:
         tpCons=input('\nIndique se pretende consultar lista de voos (L/l) ou apenas um voo (A/a): ')
         tpCons=tpCons.upper()
         if tpCons=='L':
              linhas=int(input('Indique o número máximo de linhas do relatório: '))
              voo1=Rc.Voos()
              voo1.consultaVoos(linhas, '')
              continua()
         elif tpCons=='A':
              idVoo=int(input('Indique o voo a consultar: '))
              voo1=Rc.Voos()
              voo1.consultaVoos(1, idVoo) # consulta de apenas 1 linha com o idVoo escolhido
              continua()
    

    # SAIR DO PROGRAMA
    elif opcaoMenu==5:
         sair=input('Tem a certeza que pretende sair (s / n)? ')
         sair=sair.upper()
         if sair=='N':
              continua()
         else:
              exit('Saída do programa!')



# Método para sair do ecrã e voltar ao menu principal
def continua():
     input('\nPressione enter para continuar!')
     os.system('cls') # limpa o terminal em windows
     main()             

# Invocação da função main()
main()


