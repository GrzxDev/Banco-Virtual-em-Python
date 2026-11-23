# Projeto #1 - Banco Virtual

import banco
from time import sleep

conta = banco.Banco("0542", "14796", "10487343662", "fleal448@gmail.com")
gloria = banco.Banco("0524", "77053", "27104230653", None, None)
chiquinho = banco.Banco("0524", "77055", None, None, "38991392663")
fred = banco.Banco("0524", "77056", None, None, "38991730304")

contas = {
    "Gloria": gloria,
    "Chiquinho": chiquinho,
    "Fred": fred
}

if __name__ == "__main__":

    while True:
        banco.menu()
        # Opção escolhida
        try:
            escolha = int(input("\nEscolha uma opção: "))
        except ValueError:
            print('Digite uma opção válida. ')
            continue

        if escolha == 1:
            conta.view_saldo()
        elif escolha == 2:
            pix = banco.Pix(conta)
            pix.area(contas)
        elif escolha == 3:
            conta.consultar_dados()
        elif escolha == 4:
            banco.deposito(conta)
        elif escolha == 5:
            conta.extrato()
        elif escolha == 6:
            banco.saque(conta)
        elif escolha == 7:
            print("Saindo do Sistema, até mais.")
            sleep(1.5)
            break
        else:
            print("Opção inválida, tente novamente!\n")