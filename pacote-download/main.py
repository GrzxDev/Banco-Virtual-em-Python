# Projeto #1 - Banco Virtual

import banco

conta1 = banco.Banco()

while True:
    banco.menu()
    # Opção escolhida
    try:
        escolha = int(input('Escolha uma opção: '))
    except ValueError:
        print('Digite uma opção válida. ')
        continue

    if escolha == 1:
        banco.view_saldo(conta1)
    elif escolha == 2:
        banco.areapix(conta1)
    elif escolha == 3:
        banco.consultar_dados()
    elif escolha == 4:
        banco.deposito(conta1)
    elif escolha == 5:
        banco.extrato(conta1)
    elif escolha == 6:
        banco.saque(conta1)
    elif escolha == 7:
        break
    else:
        print('Opção inválida, tente novamente! ')
        print()