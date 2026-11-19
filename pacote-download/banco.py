from time import sleep

dados_bancarios = {
'agencia': 524,
'conta': 77054,
'chaves_pix': {
    'cpf': '123.123.123-12',
    'telefone': '59928022',
    }
}

destinatarios = {
'Gloria': '27104230653',
'Chiquinho': '38991392663',
'Fred': '38991730304'
}

class Banco:
    def __init__(self):
        self.__saldo = 0
        self.limite_cheque_especial = 500
        self.cheque_especial_usado = 300
        self.historico = []

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("Valor inválido!")
        else:
            raise AttributeError("Não é possível alterar o saldo dessa maneira!")

    def _movimentar_saldo(self, valor) -> tuple:
        # Cálculo de Limites
        limite_cheque_disponivel = self.limite_cheque_especial - self.cheque_especial_usado
        limite_total = self.saldo + limite_cheque_disponivel

        # Validações
        if valor <= 0:
            return False, 0

        if valor > limite_total:
            return False, 0

        # Operações
        if valor > self.saldo:
            # Uso de Cheque
            uso_cheque = valor - self.saldo

            self.__saldo = 0
            self.cheque_especial_usado += uso_cheque
            return True, uso_cheque
        else:
            self.__saldo -= valor
            return True, 0

    def depositar(self, valor) -> bool:
        if valor <= 0:
            return False 
        if self.cheque_especial_usado > 0:
            if valor >= self.cheque_especial_usado:
                self.__saldo += (valor - self.cheque_especial_usado)
                self.cheque_especial_usado = 0
            else:
                self.cheque_especial_usado = (self.cheque_especial_usado - valor)
        else:
            self.__saldo += valor

        # Registro no Histórico
        self.historico.append({
            'tipo': 'Depósito', 
            'valor': valor
        })
        return True

    def sacar(self, valor) -> bool:

        sucesso, uso_cheque = self._movimentar_saldo(valor)

        # Falha na Movimentação
        if not sucesso:
            return False

        # Saque com Cheque
        if uso_cheque > 0:
            self.historico.append({
                "tipo": "Saque",
                "valor": valor,
                "cheque": uso_cheque
            })
            return True
        
        # Saque sem Cheque
        else:
            self.historico.append({
                "tipo": "Saque",
                "valor": valor
            })
            return True

    def pix(self, valor) -> bool:

        sucesso, uso_cheque = self._movimentar_saldo(valor)

        # Falha na Movimentação
        if not sucesso:
            return False

        # Pix com Cheque
        if uso_cheque > 0:
            self.historico.append({
                "tipo": "Pix",
                "valor": valor,
                "cheque": uso_cheque
            })
            return True
        # Pix sem Cheque
        else:
            self.historico.append({
                "tipo": "Pix",
                "valor": valor,
            })
            return True

def extrato(conta):
    """
    Exibe o extrato da conta.
    """
    print('== Extrato ==\n')
    quantidade = total_entrada = total_saida = 0

    if not conta.historico:
        print('Nenhuma movimentação realizada. ')
    else:
        for movimentacao in conta.historico:
            if movimentacao['tipo'] == 'Depósito':
                quantidade += 1
                total_entrada += movimentacao['valor']
                print(f'Depósito: ')
                print(f"Valor: + R${movimentacao['valor']:.2f}\n")

            elif movimentacao['tipo'] == 'Pix' and 'cheque' in movimentacao:
                quantidade += 1
                total_saida += movimentacao['valor']
                print(f'Transferência Pix: ')
                print(f"Valor Total da Transferência: - R${movimentacao['valor']:,.2f}")
                print(f"Valor Retirado do Limite: R${movimentacao['cheque']:,.2f}\n")

            elif movimentacao['tipo'] == 'Pix':
                quantidade += 1
                total_saida += movimentacao['valor']
                print('Transferência Pix: ')
                print(f"Valor: - R${movimentacao['valor']:.2f}\n")

            elif movimentacao['tipo'] == 'Saque' and 'cheque' in movimentacao:
                quantidade += 1
                total_saida += movimentacao['valor']
                print('Saque: ')
                print(f"Valor total do saque: - R${movimentacao['valor']:,.2f}")
                print(f"Valor Retirado do Limite: R${movimentacao['cheque']:,.2f}\n")

            elif movimentacao['tipo'] == 'Saque':
                quantidade += 1
                total_saida += movimentacao['valor']
                print('Saque: ')          
                print(f"Valor: - R${movimentacao['valor']:.2f}\n")

    print('=== Resumo ===\n')
    print(f'Movimentações: {quantidade}')
    print(f'Entradas: R${total_entrada:.2f}')
    print(f'Saídas: R${total_saida:.2f}')
    print(f'Saldo Atual: R${conta.saldo:,.2f}')
    print(f'Cheque Especial Utilizado: R${conta.cheque_especial_usado:,.2f}')

def validar_valor():
    """
    Função para validar um valor no projeto, seja pra depósito, tranferência e etc.
    """
    while True:
        try:
            valor = float(input("Digite o valor: R$ "))
            if valor <= 0:
                raise ValueError
        except ValueError:
            print("Valor inválido! Digite um valor válido!")
            continue
        return valor

def menu():
    print('-' * 30)
    print("Banco DuGrau".center(30))
    print('-' * 30)
    print('1 - Saldo')
    print('2 - Area Pix')
    print('3 - Consultar Dados Bancarios ')
    print('4 - Depósito')
    print('5 - Extrato')
    print('6 - Saque')
    print('7 - Sair')

def view_saldo(conta):
    '''
    Menu destinado para a visualização do saldo.
    '''
    print(f'Seu saldo atual é de R${conta.saldo:.2f}\n')

def areapix(conta):
    """
    Menu destinado para a realização com a ferramenta Pix.
    - Tranferência
    - Chaves
    """
    while True:
        print('\n=== ÁREA PIX ===\n')
        print('1 - Realizar uma Transferencia Pix')
        print('2 - Minhas Chaves Pix')
        print('3 - Voltar para o Menu')

        # Opção de Escolha
        try:
            escolhapix = int(input('Escolha uma opção: '))
        except ValueError:
            print('Escolha uma opção válida! ')
            continue

        if escolhapix == 1:
            print(f"O seu saldo atual é de R${conta.saldo:.2f}\n")

            # Dados
            valor = validar_valor()
            chave_pix = input("Digite a chave pix: ").strip(".-")
            chave_encontrada = False
            for pessoa, chave in destinatarios.items():
                if chave_pix == chave:
                    chave_encontrada = True
                    print("\nChave encontrada!")
                    print(f"Destinatário: {pessoa}")
                    resultado = conta.pix(valor)
                    if resultado:
                        print("Tranferência realizada com sucesso!")
                        break
                    else:
                        print("Transferência não realizada!")
                        break
            if chave_encontrada == False:
                print("Nenhuma chave encontrada!")
                continue
        elif escolhapix == 2:
            print(dados_bancarios['chaves_pix']['cpf'])
            print(dados_bancarios['chaves_pix']['telefone'])
        elif escolhapix == 3:
            return

def consultar_dados():
    #Dados Bancários
    print(f"\nAgência: {dados_bancarios['agencia']}")
    print(f"Conta: {dados_bancarios['conta']}\n")
 
def deposito(conta):
        print(f'\nSaldo atual: R${conta.saldo:.2f}\n')

        # Validação de Valor
        valor_deposito = validar_valor()

        # Processamento
        resultado = conta.depositar(valor_deposito)

        if resultado:
            print('Realizando Depósito...')
            sleep(3)
            print("Depósito realizado com sucesso!")
        else:
            print("Não foi possível realizar o depósito.")
        
def saque(conta):
    """
    Função destinada a realização de saques.
    """         
    # Cálculo de Limites
    limite_cheque_disponivel = conta.limite_cheque_especial - conta.cheque_especial_usado
    limite_total = conta.saldo + limite_cheque_disponivel

    print(f'\nSaldo atual: {conta.saldo:.2f}')
    print(f'Limite Cheque especial: {conta.limite_cheque_especial:.2f} ')
    print(f'Limite Total Disponível para Saque: R${limite_total:.2f} ')

    # Validação de Valor
    valor = validar_valor()

    # Interação com Usuário (Uso de Cheque Especial)
    if valor > conta.saldo:
        uso_cheque = valor - conta.saldo
        if uso_cheque <= limite_cheque_disponivel:
            while True:
                choice = input("Você precisará usar seu cheque especial para realizar esse saque, deseja continuar ? [S/N] ").upper()
                if choice not in ("S", "N"):
                    print(f"Digite uma escolha válida! [S/N]")
                else:
                    break
            if choice == "N":
                print(f"Saque cancelado!")
                resultado = False
            else:
                resultado = conta.sacar(valor)
        else:
            print("Limite total indisponível, saque cancelado!")
            resultado = False
    else:
        resultado = conta.sacar(valor)

    # Verificação do Resultado
    if resultado:
        print("Realizando o saque...")
        sleep(1)
        print("Saque realizado com sucesso!")
    else:
        print("Saque não realizado!")