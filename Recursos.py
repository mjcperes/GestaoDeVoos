# -*- coding: utf-8 -*-
# MÓDULO RECURSOS PARA EXECUTAR OS VOOS

import csv
import os
import pandas as pd
from datetime import datetime as dt

# Definição de constante PATH com a localização dos ficheiros csv
# PATH='C:/Users/mario/Workspace_VSC/Projetos_VSC/10793/Python/'

script_path = os.path.dirname(__file__) #retira a diretoria onde está o script
PATH=script_path + '/'

# Lista de aeronaves: Criação de objeto do tipo pandas dataframe com ficheiro csv
if os.path.isfile(PATH+'listaAeronaves.csv'): # verificar se o ficheiro já existe    
    aeronaves_csv=pd.read_csv(PATH+'listaAeronaves.csv') # criação de variável aeronaves_csv do tipo pandas dataframe
    aeronPanda=True # variável booleana que confirma se objeto do tipo pandas dataframe foi criado
else:
    aeronPanda=False

# Lista de rotas: Criação de objeto do tipo pandas dataframe com ficheiro csv
if os.path.isfile(PATH+'listaRotas.csv'): # verificar se o ficheiro já existe    
    rotas_csv=pd.read_csv(PATH+'listaRotas.csv') # criação de variável rotas_csv do tipo pandas dataframe
    rotaPanda=True # variável booleana que confirma se objeto do tipo pandas dataframe foi criado
else:
    rotaPanda=False

# Lista de voos: Criação de objeto do tipo pandas dataframe com ficheiro csv
if os.path.isfile(PATH+'listaVoos.csv'): # verificar se o ficheiro já existe    
    voos_csv=pd.read_csv(PATH+'listaVoos.csv') # criação de variável rotas_csv do tipo pandas dataframe
    vooPanda=True # variável booleana que confirma se objeto do tipo pandas dataframe foi criado
else:
    vooPanda=False

# ----------------------------------AERONAVES-----------------------------------
# ------------------------------------------------------------------------------
# Criação da classe pai Aeronaves (genérica)
class Aeronaves:
    def __init__(self, tipo):
        # Construtor da classe        
        self.tipo=tipo
        self.matricula=''
        self.marcaModelo=''
        self.lotacaoEcon=0
        self.alcance=0
        self.ativa=0 # variável para definir se a aeronave está ao serviço da companhia aérea (0-não está ao serviço / 1-está ao serviço)
    
    # Método para inserir aeronaves do tipo Turboprop (turbo-hélice)
    def inserirAeronave(self):
        print(f"\nCriação de nova aeronave do tipo {self.tipo}\n")        
        self.matricula=input('Digite a matrícula: ')
        # Validação se matrícula já existe
        while self.existeMatricula(self.matricula):
            self.matricula=input('Matrícula já existe! Insira outra matrícula: ')
        self.marcaModelo=input('Digite a marca e o modelo: ')
        self.alcance=int(input('Digite o alcance em kms: '))
        self.lotacaoEcon=int(input('Digite a lotação em classe económica: '))        
        self.ativa=1
        # condição para chamar os métodos infoAeronave() e listaAeronaves() apenas nesta classe
        if self.tipo=='Turboprop':
            print(self.infoAeronave())
            self.listaAeronaves()

    # Método para receber as variáveis da aeronave
    def infoAeronave(self):
        aeronaveTurboProp={'Matrícula':self.matricula, 'Marca e modelo':self.marcaModelo, 'Tipo':self.tipo, 'Em serviço': self.ativa, 'Alcance':self.alcance, 
                           'Lotação em económica':self.lotacaoEcon, 'Lotação em executiva': 0}
        return aeronaveTurboProp
        

    # Método para criar ou atualizar ficheiro csv com dados das aeronaves
    def listaAeronaves(self):
        global aeronaves_csv
        global aeronPanda
        #Lista que define o cabeçalho do ficheiro csv
        cabecalho = ['Matrícula', 'Marca e modelo', 'Tipo', 'Em serviço', 'Alcance', 'Lotação económica', 'Lotação Executiva']
        #Criação de lista usando uma Comprehension Expression para extração dos valores para carregar em ficheiro csv
        dadosAeron=[i for i in self.infoAeronave().values()]        
        
        # Verificar se o ficheiro já existe. Se não existir será criado.
        if aeronPanda==True:            
            # inclui-se 'a' para acrescentar linhas (append)
            with open(PATH+'listaAeronaves.csv', 'a', encoding='utf-8') as ficheiro: 
                writer=csv.writer(ficheiro, lineterminator='\n')    # lineterminator='\n' indica ao windows que o caracter para mudar de linha é '\n' em vez de '\r\n'                            
                writer.writerow(dadosAeron) # se o ficheiro já existir não insere o cabeçalho                
        else:
            # inclui-se 'w' para escrever (write)
            with open(PATH+'listaAeronaves.csv', 'w', encoding='utf-8') as ficheiro:
                writer=csv.writer(ficheiro, lineterminator='\n')
                writer.writerow(cabecalho) # se o ficheiro não existir insere o cabeçalho
                writer.writerow(dadosAeron)
                aeronPanda=True
        # atualização de variável aeronaves_csv do tipo pandas dataframe
        aeronaves_csv=pd.read_csv(PATH+'listaAeronaves.csv')
    
    
    # Método para consultar aeronaves no ficheiro csv usando uma dataframe do pandas
    def consultaAeronaves(self, linhas, matr):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global aeronaves_csv
        global aeronPanda
        # Verificar se o ficheiro já existe.
        if aeronPanda==True:
            aeronaves_csv=pd.read_csv(PATH+'listaAeronaves.csv') # se existir atualiza variável aeronaves_csv do tipo pandas dataframe
            if linhas>1:
                print(aeronaves_csv.head(linhas))
            else:
                # Verificar se matrícula existe.
                if self.existeMatricula(matr):
                    aeronUnica=aeronaves_csv[aeronaves_csv['Matrícula']==matr]
                    print(aeronUnica.head())
                else:
                    print('Matrícula não existe!')                
        else:
            print('Não existem aeronaves inseridas!')


    # Método para atualizar aeronaves ativas ou remover aeronaves no ficheiro csv usando uma dataframe do pandas
    def atualizaAeronave(self, matric, opcaoAtz):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global aeronaves_csv
        global aeronPanda
        if aeronPanda==True:
            # Verificar se matrícula existe.
            if self.existeMatricula(matric):
                if opcaoAtz=='R': # opção de remover aeronave
                     # atualização da dataframe excluindo a matrícula selecionada
                     aeronaves_csv=aeronaves_csv[aeronaves_csv['Matrícula'] != matric]
                     # escrever a dataframe de novo para o ficheiro csv
                     aeronaves_csv.to_csv(PATH+'listaAeronaves.csv', index=False) # o argumento index=False faz com que não inclua a primeira coluna com os índices
                elif opcaoAtz=='T': # opção de atualizar aeronave ativa/inativa
                    ativaInativa=aeronaves_csv.loc[aeronaves_csv['Matrícula']==matric, 'Em serviço'].values[0]
                    if ativaInativa==1:
                        ativaInativa=0
                    else:
                        ativaInativa=1
                    # atualização da dataframe com o novo valor par 'Em serviço'
                    aeronaves_csv.loc[aeronaves_csv['Matrícula']==matric, 'Em serviço']=ativaInativa
                    # escrever a dataframe de novo para o ficheiro csv
                    aeronaves_csv.to_csv(PATH+'listaAeronaves.csv', index=False)
            else:
                print('Matrícula não existe!')
            
            # atualização de variável aeronaves_csv do tipo pandas dataframe após consultas/alterações
            aeronaves_csv=pd.read_csv(PATH+'listaAeronaves.csv')

        else:
            print('Não existem aeronaves inseridas!')
        
    # Método para verificar se a matrícula existe
    def existeMatricula(self, mtrl):
        if aeronPanda==True:
            if mtrl in aeronaves_csv['Matrícula'].values: # verificação se variável idRota já existe no dataframe
                return True
            else:
                return False
        else:
            return False


# Criação da classe filha para aeronaves a jato
class AeronavesJato(Aeronaves):
    def __init__(self, tipo):
        # Inicialização dos atributos da classe pai
        super().__init__(tipo)
        self.lotacaoExec=0

    # Método para inserir aeronaves do tipo Jato por herança do método na classe pai
    def inserirAeronave(self):                    
        super().inserirAeronave() # chama método inserirAeronave() da classe pai mas sem chamar os outros métodos de modo a permitir a variável local lotacaoExec
        self.lotacaoExec=int(input('Digite a lotação em classe executiva: '))
        print(self.infoAeronave())
        super().listaAeronaves() # chamada do método listaAeronaves() da classe pai só depois de se atribuir um valor à variável lotacaoExec

    # Método para receber as variáveis da aeronave
    def infoAeronave(self):
        # aeronaveJato=Aeronaves.infoAeronave(self) # código alternativo à linha abaixo
        aeronaveJato=super().infoAeronave()
        aeronaveJato['Lotação em executiva']=self.lotacaoExec
        return aeronaveJato    

# ----------------------------------ROTAS---------------------------------------
# ------------------------------------------------------------------------------
# Criação da classe Rotas para definição dos destinos dos voos
class Rotas:
    def __init__(self):
        # Construtor da classe
        self.idRota=''
        self.aeropPartida=''
        self.aeropChegada=''
        self.distancia=0
        self.restricao=0  # restrição da rota por existir pelo menos um aeroporto não certificado para a dimensão da aeronave (0-sem restrições / 1-com restrições)        
    
    # Método para inserir novas rotas
    def inserirRota(self):
        self.idRota=input('\nIndique o ID da rota: ')
        self.idRota='R'+self.idRota
        print(f"\nCriação de nova rota com o ID {self.idRota}\n")
        # Validação se idRota já existe
        while self.existeRota(self.idRota):
            self.idRota=input('ID da rota já existe! Insira outro ID: ')
            self.idRota='R'+self.idRota
            print(f"\nCriação de nova rota com o ID {self.idRota}\n")            
        
        self.aeropPartida=input('Digite o aeroporto de partida: ')
        self.aeropChegada=input('Digite o aeroporto de chegada: ')
        self.distancia=int(input('Digite a distância em Kms: '))
        self.restricao=input('Indique se há aeroporto(s) com restrições (0-sem restrições / 1-com restrições): ')
        # validação do tipo de restrição
        while self.restricao!='0' and self.restricao!='1':
            print('\nPor favor indique 0 ou 1 para a restrição!')
            self.restricao=input('Indique se há aeroporto(s) com restrições (0-sem restrições / 1-com restrições): ')
        self.restricao=int(self.restricao) # conversão da variável restricao para int depois da validação        
        print(self.infoRota())
        self.listaRotas()

    # Método para receber as variáveis da rota
    def infoRota(self):
        rota={'ID da rota':self.idRota, 'Origem':self.aeropPartida, 'Destino':self.aeropChegada, 
              'Distância':self.distancia, 'Restrição':self.restricao}
        return(rota)

    # Método para criar ou atualizar ficheiro csv com dados das rotas
    def listaRotas(self):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global rotas_csv
        global rotaPanda        
        # Lista que define o cabeçalho do ficheiro csv das rotas
        cabecalhoRota = ['ID da rota', 'Origem', 'Destino', 'Distância', 'Restrição']
        # Criação de lista usando uma Comprehension Expression para extração dos valores para carregar em ficheiro csv
        dadosRota=[i for i in self.infoRota().values()]
        
        # Verificar se o ficheiro já existe. Se não existir será criado.
        if rotaPanda==True:            
            # inclui-se 'a' para acrescentar linhas (append)
            with open(PATH+'listaRotas.csv', 'a', encoding='utf-8') as fichRot: 
                writer=csv.writer(fichRot, lineterminator='\n')    # lineterminator='\n' indica ao windows que o caracter para mudar de linha é '\n' em vez de '\r\n'                            
                writer.writerow(dadosRota) # se o ficheiro já existir não insere o cabeçalho                
        else:
            # inclui-se 'w' para escrever (write)
            with open(PATH+'listaRotas.csv', 'w', encoding='utf-8') as fichRot:
                writer=csv.writer(fichRot, lineterminator='\n')
                writer.writerow(cabecalhoRota) # se o ficheiro não existir insere o cabeçalho
                writer.writerow(dadosRota)
                rotaPanda=True
        # atualização de variável rotas_csv do tipo pandas dataframe após consultas/alterações
        rotas_csv=pd.read_csv(PATH+'listaRotas.csv')
    
    
    # Método para consultar rotas no ficheiro csv usando uma dataframe do pandas
    def consultaRotas(self, linhas, idRota):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global rotas_csv
        global rotaPanda
        # Verificar se o ficheiro já existe.        
        if rotaPanda==True:
            rotas_csv=pd.read_csv(PATH+'listaRotas.csv') # se existir atualiza variável rotas_csv do tipo pandas dataframe
            if linhas>1:                
                print(rotas_csv.head(linhas))
            else:
                # Verificar se idRota existe.
                if self.existeRota(idRota):
                    rotaUnica=rotas_csv[rotas_csv['ID da rota']==idRota]
                    print(rotaUnica.head())
                else:
                    print('Rota não existe!')                
        else:
            print('Não existem rotas inseridas!')               
    

    # Método para atualizar rotas ativas ou remover rotas no ficheiro csv usando uma dataframe do pandas    
    def atualizaRota(self, idRt):
        # declaração da variáveis globais para não serem tratada como locais dentro do método        
        global rotas_csv
        global rotaPanda        
        if rotaPanda==True:
            rotas_csv=pd.read_csv(PATH+'listaRotas.csv') # se existir atualiza variável rotas_csv do tipo pandas dataframe
            # Verificar se rota existe.
            if self.existeRota(idRt):
                # atualização da dataframe excluindo a rota selecionada
                rotas_csv=rotas_csv[rotas_csv['ID da rota'] != idRt]
                # reescrever a dataframe de novo para o ficheiro csv
                rotas_csv.to_csv(PATH+'listaRotas.csv', index=False) # o argumento index=False faz com que não inclua a primeira coluna com os índices
                input('Rota apagada! Enter para continuar...')
            else:
                print('Rota não existe!')
            
            # atualização de variável aeronaves_csv do tipo pandas dataframe após consultas/alterações
            rotas_csv=pd.read_csv(PATH+'listaRotas.csv')

        else:
            print('Não existem rotas inseridas!')
    
    # Método para verificar se a rota existe
    def existeRota(self, idRta):
        if rotaPanda==True:
            if idRta in rotas_csv['ID da rota'].values: # verificação se variável idRota já existe no dataframe
                return True
            else:
                return False
        else:
            return False
                


# ----------------------------------VOOS----------------------------------------
# ------------------------------------------------------------------------------
# Criação da classe Voos para definição dos dos voos
class Voos:
    def __init__(self):
        self.registo=0      # registo único de cada voo
        self.rotaVoo=''     # obtém os dados relativos à rota previamente carregada
        self.matriculaA=''  # matrícula da aeronave: obtém os dados relativos à aeronave        
        # self.estado=3     # estado do voo (1-On Time / 2-Delayed / 3-Canceled): por defeito considera-se cancelado / não efetuado # (em desenvolvimento)
        self.dataVoo=''
        self.horaPartida=''
        self.horaChegada=''
        self.tempoVoo=''
        self.paxEcon=0
        self.receitaPaxEc=0
        self.paxExec=0
        self.receitaPaxExec=0
    
    # Método para inserir novos voos
    def inserirVoo(self):
        # Atribuição automática do ID do voo        
        global voos_csv # declaração da variáveis globais para não serem tratada como locais dentro do método
        global vooPanda
        if vooPanda==True:
            self.registo=int(voos_csv.loc[voos_csv.index[-1], 'ID do voo']) + 1
        else:
            self.registo=1000 # caso o ficheiro csv e o pandas dataframe ainda não existam o registo ID dos voos começa em 1000
        
        print(f"\nRegisto de novo voo com o ID {self.registo}\n")
        self.rotaVoo=input('Indique o código da rota: ')
        # Validação se idRota existe
        rotaV1=Rotas() # criação de objeto do tipo Rota()
        while rotaV1.existeRota(self.rotaVoo)==False:
            self.rotaVoo=input('\nRota não existe! Indique um código existente: ')
        
        self.matriculaA=input('Indique a matrícula da aeronave: ')
        # Validação se matrícula existe
        AeronV1=Aeronaves('Turboprop') # criação de objeto do tipo Aeronaves
        while AeronV1.existeMatricula(self.matriculaA)==False:
            self.matriculaA=input('\nMatrícula não existe! Indique uma matrícula existente: ')
        
        # Validação do formato da data do voo
        self.dataVoo=input('Digite a data do voo no formato "aaaa-mm-dd": ')
        erroFormatoData=True
        while erroFormatoData:
            try:
                self.dataVoo=dt.strptime(self.dataVoo, '%Y-%m-%d').date()
                erroFormatoData=False
            except ValueError:
                print(f"'{self.dataVoo} Não tem o formato de data correto")
                self.dataVoo=input('Digite a data do voo no formato "aaaa-mm-dd": ')
        
        self.horaPartida=input('Digite a hora (UTC) de partida no formato "hh:mm": ')
        self.horaChegada=input('Digite a hora (UTC) de chegada no formato "hh:mm": ')
        # Validação do formato das horas
        while self.validaHoras(self.horaPartida, self.horaChegada)==False:
            print('As horas estão num formato incorreto ou hora de partida superior a hora de chegada!')
            self.horaPartida=input('Digite a hora (UTC) de partida no formato "hh:mm": ')
            self.horaChegada=input('Digite a hora (UTC) de chegada no formato "hh:mm": ')
        
        # depois de validado o formato das horas obtém-se o tempo de voo
        self.tempoVoo=self.validaHoras(self.horaPartida, self.horaChegada)[-1]

        self.paxEcon=input('Digite o número de passageiros em classe económica: ')
        self.receitaPaxEc=input('Digite a receita dos passageiros em classe económica: ')

        # verificação se a aeronave tem classe executiva:
        if aeronaves_csv.loc[aeronaves_csv['Matrícula'] == self.matriculaA, 'Tipo'].values[0]=='Turboprop':
            self.paxExec = 0
            self.receitaPaxExec = 0
        else:
            self.paxExec=input('Digite o número de passageiros em classe executiva: ')
            self.receitaPaxExec=input('Digite a receita dos passageiros em classe executiva: ')          
        
        print(self.infoVoos())
        self.listaVoos()

    # Método para receber as variáveis dos voos
    def infoVoos(self):
        global rotas_csv
        global aeronaves_csv

        origem = rotas_csv.loc[rotas_csv['ID da rota'] == self.rotaVoo, 'Origem'].values[0] # retira informação do df rotas_csv
        destino = rotas_csv.loc[rotas_csv['ID da rota'] == self.rotaVoo, 'Destino'].values[0] # values[0] permite que os índices não sejam imprimidos
        distancia = rotas_csv.loc[rotas_csv['ID da rota'] == self.rotaVoo, 'Distância'].values[0]

        aeronave = aeronaves_csv.loc[aeronaves_csv['Matrícula'] == self.matriculaA, 'Marca e modelo'].values[0] # retira informação do df voos_csv

        totalPax = int(self.paxEcon) + int(self.paxExec)
        totalReceita = int(self.receitaPaxEc) + int(self.receitaPaxExec)
        
        
        voo={'ID do voo':self.registo, 'Data':self.dataVoo.strftime('%Y-%m-%d'), 'Matrícula':self.matriculaA, 'Aeronave':aeronave, 'Origem':origem, 
             'Hora partida': self.horaPartida, 'Destino':destino, 'Hora chegada': self.horaChegada, 'Kms':distancia, 'Tempo de voo':self.tempoVoo, 
             'Pax económica':self.paxEcon, 'Receita pax econ':self.receitaPaxEc, 'Pax executiva':self.paxExec, 'Receita pax exec':self.receitaPaxExec, 
             'Total pax':totalPax, 'Total receita': totalReceita}
        return(voo)
    
    
    # Método para criar ou atualizar ficheiro csv com dados dos voos
    def listaVoos(self):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global voos_csv
        global vooPanda        
        # Lista que define o cabeçalho do ficheiro csv dos voos
        cabecalhoVoos = ['ID do voo', 'Data', 'Matrícula', 'Aeronave', 'Origem', 'Hora partida', 'Destino', 'Hora chegada', 'Kms', 
                         'Tempo de voo', 'Pax económica', 'Receita pax econ', 'Pax executiva', 'Receita pax exec', 'Total pax', 'Total receita']
        # Criação de lista usando uma Comprehension Expression para extração dos valores para carregar em ficheiro csv
        dadosVoo=[i for i in self.infoVoos().values()]
        
        # Verificar se o ficheiro já existe. Se não existir será criado.
        if vooPanda==True:            
            # inclui-se 'a' para acrescentar linhas (append)
            with open(PATH+'listaVoos.csv', 'a', encoding='utf-8') as fichVoo:
                writer=csv.writer(fichVoo, lineterminator='\n')    # lineterminator='\n' indica ao windows que o caracter para mudar de linha é '\n' em vez de '\r\n'                            
                writer.writerow(dadosVoo) # se o ficheiro já existir não insere o cabeçalho                
        else:
            # inclui-se 'w' para escrever (write)
            with open(PATH+'listaVoos.csv', 'w', encoding='utf-8') as fichVoo:
                writer=csv.writer(fichVoo, lineterminator='\n')
                writer.writerow(cabecalhoVoos) # se o ficheiro não existir insere o cabeçalho
                writer.writerow(dadosVoo)
                vooPanda=True
        # atualização de variável voos_csv do tipo pandas dataframe após consultas/alterações
        voos_csv=pd.read_csv(PATH+'listaVoos.csv')

    
    # Método para consultar voos no ficheiro csv usando uma dataframe do pandas
    def consultaVoos(self, linhas, idVoo):
        # declaração da variáveis globais para não serem tratada como locais dentro do método
        global voos_csv
        global vooPanda
        # Verificar se o ficheiro já existe.        
        if rotaPanda==True:
            voos_csv=pd.read_csv(PATH+'listaVoos.csv') # se existir atualiza variável voos_csv do tipo pandas dataframe
            if linhas>1:                
                print(voos_csv.head(linhas))
            else:
                # Verificar se idVoo existe.
                if self.existeVoo(idVoo):
                    vooUnico=voos_csv[voos_csv['ID do voo']==idVoo]
                    print(vooUnico.head())
                else:
                    print('Voo não existe!')                
        else:
            print('Não existem voos inseridos!')



    # Método para validar horas e calcular tempo de voo
    def validaHoras(self, hrPart, hrCheg):
        horaValida=False
        tempoVoo=''
        try:
            hrP=int(hrPart[0:2])
            mnP=int(hrPart[-2:])
            hrC=int(hrCheg[0:2])
            mnC=int(hrCheg[-2:])
            horaValida=True
        except ValueError:
            print('Horas incorretas!')
            horaValida=False
        if horaValida==True:
            if 0 <= hrP <=23 and 0 <= mnP <= 59 and 0 <= hrC <= 23 and 0 <= mnC <= 59:
                if hrP>hrC or (hrP==hrC and mnP>mnC):
                    horaValida=False                
                else:                    
                    duracaoHr=hrC-hrP
                    if mnC<mnP:
                        duracaoMn=mnC-mnP+60
                        duracaoHr-=1
                    else:
                        duracaoMn=mnC-mnP
                    
                    tempoVoo=f"{duracaoHr}:{duracaoMn:02d}"            

        if horaValida==True:
            return horaValida, tempoVoo            
        else:
            return horaValida
        

    # Método para verificar se voo existe
    def existeVoo(self, idVoo):
        if vooPanda==True:
            if idVoo in voos_csv['ID do voo'].values: # verificação se variável idVoo já existe no dataframe
                return True
            else:
                return False
        else:
            return False



if __name__ == '__main__':
    # teste1=Rotas()
    # print(teste1.infoRota())
    
    # dataVoo=input('Digite a data do voo no formato "aaaa-mm-dd": ')
    # erroFormato=True
    # while erroFormato:
    #     try:
    #         dataVoo=dt.strptime(dataVoo, '%Y-%m-%d').date()
    #         erroFormato=False
    #     except ValueError:
    #         print(f"'{dataVoo} Não tem o formato de data correto")
    #         dataVoo=input('Digite a data do voo no formato "aaaa-mm-dd": ')
    # print(dataVoo)

    # teste2=Voos()
    # print(teste2.validaHoras('13:25', '14:15')[-1])

    # global rotas_csv
    # global aeronaves_csv

    # rotas_csv=pd.read_csv(PATH+'listaRotas.csv')
    # aeronaves_csv=pd.read_csv(PATH+'listaAeronaves.csv')
    
    # origem = rotas_csv.loc[rotas_csv['ID da rota'] == 'R100', 'Origem'].values[0]
    # destino = rotas_csv.loc[rotas_csv['ID da rota'] == 'R100', 'Destino'].values[0]
    # distancia = rotas_csv.loc[rotas_csv['ID da rota'] == 'R100', 'Distância'].values[0]    
    # aeronave = aeronaves_csv.loc[aeronaves_csv['Matrícula'] == 'CS-DJB', 'Marca e modelo'].values[0]
    # print(origem)
    # print(destino)
    # print(distancia)
    # print(aeronave)

    # dataVoo=dt.strptime('2024-03-01', '%Y-%m-%d').date()
    # print(dataVoo)

    # vooUnico=voos_csv[voos_csv['ID do voo']==1000]
    # print(vooUnico.head())

    # registo=int(voos_csv.loc[voos_csv.index[-1], 'ID do voo']) + 1
    # print(registo)

    # tipo = aeronaves_csv.loc[aeronaves_csv['Matrícula'] == 'CS-TRD', 'Tipo'].values[0] # =='Turboprop'
    # print(tipo)

    ## import os
    # script_dir = os.path.dirname(os.path.abspath('__Recursos.py__')) # retira a diretoria onde está o script
    # print(f"The script is located in: {script_dir}") # impressão da diretoria
    # current_path = os.getcwd()
    # script_path = os.path.abspath(__file__)
    script_path = os.path.dirname(__file__)
    print(f"The script is located in: {script_path}") # impressão da diretoria
    # PATH = script_dir
    # PATH = current_path
    PATH = script_path
    print(PATH)
    print(PATH+'listaAeronaves.csv')


