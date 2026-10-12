from time import sleep

dados_bancarios = {
'agencia': 524,
'conta': 77054,
'chaves_pix': {
    'cpf': '104.873.436-62',
    'telefone': '38991935116',
    }
}

destinatarios = {
'Gloria': '27104230653',
'Chiquinho': '38991392663',
'Fred': '38991730304'
}

class Banco:
    def __init__(self):
        self.saldo = 1500
        self.limite_cheque_especial = 500
        self.cheque_especial_usado = 0
        self.historico = []

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

            elif movimentacao['tipo'] == 'Transferência' and 'cheque' in movimentacao:
                quantidade += 1
                total_saida += movimentacao['valor']
                print(f'Transferência: ')
                print(f"Valor Total da Transferência: - R${movimentacao['valor']:,.2f}")
                print(f"Valor Retirado do Limite: R${movimentacao['cheque']:,.2f}\n")

            elif movimentacao['tipo'] == 'Transferência':
                quantidade += 1
                total_saida += movimentacao['valor']
                print('Transferência: ')
                print(f"Valor: - R${movimentacao['valor']:.2f}")
                print(f"Chave: {movimentacao['chave']}\n")

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
                print(f'Valor: - R${movimentacao['valor']:.2f}\n')

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
            valor = float(input('Digite o valor: R$ '))
        except ValueError:
            print('Valor inválido! Digite um valor válido! ')
            continue

        if valor > 0:
            return valor
        
        print('Valor inválido! Digite um valor maior que zero. ')

def menu():
    print('-' * 12)
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

        # Entrada dos Dados
        try:
            escolhapix = int(input('Escolha uma opção: '))
        except ValueError:
            print('Escolha uma opção válida! ')
            continue
        if escolhapix == 1:
            print(f'O seu saldo atual é de R${conta.saldo:.2f} ')

            # Validação
            valor = validar_valor()
            chave_pix = str(input('Digite a Chave Pix: '))
            chave_encontrada = False
            for pessoa, chave in destinatarios.items():
                if chave_pix == chave:
                    chave_encontrada = True
                    print('\nChave encontrada! ')
                    print(f'Destinatário: {pessoa}')
                    break
            if chave_encontrada == False:
                print('Nenhuma chave encontrada! ')
            else:
                if valor > conta.saldo:
                    print(f'O seu saldo é insuficiente!\nVocê usará {valor - conta.saldo} do seu cheque especial. ')
                    while True:
                        escolha = (input(('Deseja continuar ? [S/N] '))).upper()
                        if escolha in ('S','N'):
                            break
                        print('Opção Inválida. Digite "S" ou "N". ')
                    if escolha == 'S':
                        uso_cheque = valor - conta.saldo
                        limite_disponivel = conta.limite_cheque_especial - conta.cheque_especial_usado
                        if uso_cheque <= limite_disponivel:
                            # Processamento
                            print(f'Realizando a transferência...')
                            sleep(3)
                            print('Transferência Realizada com Sucesso! ')

                            # Atualização de Saldo
                            conta.saldo = 0
                            conta.cheque_especial_usado += uso_cheque
                            print(f'Saldo atual: R${conta.saldo:.2f}')

                            # Registro no Histórico
                            conta.historico.append({
                                'tipo': 'Transferência',
                                'valor': valor,
                                'chave': chave_pix,
                                'cheque': uso_cheque
                            })
                        else:
                            print(f'Limite insuficiente! Seu limite atual é de R${limite_disponivel:.2f}. ')
                else:
                    print('Realizando a transferência...')
                    sleep(3)
                    print('Transferência Realizada com Sucesso! ')
                    conta.saldo -= valor
                    print(f'Saldo atual: R${conta.saldo:.2f}')
                    conta.historico.append({
                        'tipo': 'Transferência',
                        'valor': valor,
                        'chave': chave_pix
                    })
        elif escolhapix == 2:
            print(dados_bancarios['chaves_pix']['cpf'])
            print(dados_bancarios['chaves_pix']['telefone'])
        elif escolhapix == 3:
            return()

def consultar_dados():
    #Dados Bancários
    print(f"\nAgência: {dados_bancarios['agencia']}")
    print(f"Conta: {dados_bancarios['conta']}\n")
 
def deposito(conta):
    while True:
        print(f'\nSaldo atual: R${conta.saldo:.2f}\n')

        # Digitando o Valor
        valor_deposito = validar_valor()

        # Processamento
        print('Realizando Depósito...')
        sleep(3)

        # Atualizando Valores
        if conta.cheque_especial_usado > 0:
            if valor_deposito >= conta.cheque_especial_usado:
                valor_para_saldo = valor_deposito - conta.cheque_especial_usado
                conta.saldo += valor_para_saldo
                conta.cheque_especial_usado = 0
            else:
                valor_para_quitar = valor_deposito
                conta.saldo = 0
                conta.cheque_especial_usado -= valor_para_quitar
        else:
            conta.saldo += valor_deposito

        print(f'Saldo atualizado: R${conta.saldo:.2f}')

        # Registro no Histórico
        conta.historico.append({
            'tipo': 'Depósito', 
            'valor': valor_deposito
        })
        return()

def saque(conta):
    """
    Função destinada a realização de saques.
    """                                                                                                         
    # Limite do Cheque e Limite Total Disponível
    limite_cheque_disponivel = conta.limite_cheque_especial - conta.cheque_especial_usado
    limite_total = conta.saldo + limite_cheque_disponivel

    print(f'\nSaldo atual: {conta.saldo:.2f}')
    print(f'Limite Cheque especial: {conta.limite_cheque_especial:.2f} ')
    print(f'Limite Total Disponível para Saque: R${limite_total:.2f} ')

    # Validação do Valor
    valor_saque = validar_valor()

    if valor_saque > limite_total:
        print('Limite Total Indisponível para Saque. ')
        return()

    if valor_saque > conta.saldo:
        # Valor Utilizado do Cheque Especial
        uso_cheque = valor_saque - conta.saldo

        print(f'Você usará R${uso_cheque:.2f} do seu Cheque Especial. ')
        if uso_cheque <= limite_cheque_disponivel:
            while True:
                escolha = str(input('Deseja continuar ? [S/N] ')).upper()
                if escolha in ('S', 'N'):
                    break
                else:
                    print('Digite uma opção válida! ')
            if escolha == 'S':
                conta.saldo = 0
                conta.cheque_especial_usado += uso_cheque
                print(f'Saque Realizado com Sucesso!\n Saldo atual: R${conta.saldo:,.2f} ')
                conta.historico.append({
                'tipo': 'Saque',
                'valor': valor_saque,
                'cheque': uso_cheque
            })
            else:
                print('Saque Cancelado! ')
        else:
            print('Saque indisponível!\n Motivo: Limite Total Insuficiente. ')
    else:
        conta.saldo -= valor_saque
        print(f'Saque realizado com sucesso!\n Saldo atual: R${conta.saldo:.2f}')
        conta.historico.append({
            'tipo': 'Saque',
            'valor': valor_saque
        })