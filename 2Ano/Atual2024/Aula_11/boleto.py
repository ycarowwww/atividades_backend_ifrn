from datetime import datetime
from enum import Enum

class Pagamento(Enum):
    EmAberto = 0
    PagoParcial = 1
    Pago = 2

class Boleto:
    def __init__(self, cod_barras: str, data_emissao: datetime, data_vencimento: datetime, data_pagamento: datetime, valor_boleto: float, valor_pago: float, situacao: Pagamento) -> None:
        self.cod_barras = cod_barras
        self.data_emissao = data_emissao
        self.data_vencimento = data_vencimento
        self.data_pagamento = data_pagamento
        self.valor_boleto = valor_boleto
        self.valor_pago = valor_pago
        self.situacao = situacao

    # aaa
    @property
    def cod_barras(self) -> str: return self.__cod_barras

    @cod_barras.setter
    def cod_barras(self, cod_barras: str) -> None:
        cod_barras = cod_barras.strip()
        if cod_barras == "": raise ValueError("Code cannot be empty.")
        self.__cod_barras = cod_barras

    @property
    def data_emissao(self) -> datetime: return self.__data_emissao

    @data_emissao.setter
    def data_emissao(self, data_emissao: datetime) -> None:
        self.__data_emissao = data_emissao

    @property
    def data_vencimento(self) -> datetime: return self.__data_vencimento

    @data_vencimento.setter
    def data_vencimento(self, data_vencimento: datetime) -> None:
        self.__data_vencimento = data_vencimento

    @property
    def data_pagamento(self) -> datetime: return self.__data_pagamento

    @data_pagamento.setter
    def data_pagamento(self, data_pagamento: datetime) -> None:
        self.__data_pagamento = data_pagamento

    @property
    def valor_boleto(self) -> float: return self.__valor_boleto

    @valor_boleto.setter
    def valor_boleto(self, valor_boleto: float) -> None:
        if valor_boleto <= 0: raise ValueError("Value cannot be negative.")
        self.__valor_boleto = valor_boleto

    @property
    def valor_pago(self) -> float: return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float) -> None:
        if valor_pago <= 0 or valor_pago > self.valor_boleto: raise ValueError("Value needs to be between 0 and the Max Value.")
        self.__valor_pago = valor_pago

    @property
    def situacao(self) -> Pagamento: return self.__situacao

    @situacao.setter
    def situacao(self, situacao: Pagamento) -> None:
        self.__situacao = situacao

    def pagar(self, valor: float) -> None:
        if self.situacao == Pagamento.Pago: return
        if valor <= 0: raise ValueError("Valor Inválido.")
        if valor == self.valor_boleto:
            self.situacao = Pagamento.Pago
            self.valor_pago = valor
        elif valor > self.valor_pago:
            self.situacao = Pagamento.PagoParcial
            self.valor_boleto = valor

    def __str__(self) -> str:
        return f"Boleto: {self.cod_barras} de R${self.valor_boleto:.2f} | Pago: {self.valor_pago}."

class BoletoUI:
    @staticmethod
    def menu() -> str:
        print("1 - Novo Boleto\n2 - Sair")
        return input("- Selecione uma opção acima: ")
    
    @staticmethod
    def main() -> None:
        while True:
            option = BoletoUI.menu()

            match option:
                case "1": BoletoUI.create_ticket()
                case "2": 
                    print("Saindo do programa")
                    break
                case _: print("Opção Inválida!")
    
    @staticmethod
    def create_ticket() -> None:
        cod_barras = input("- Código de Barras do Boleto: ")
        data_emissao = datetime.strptime(input("- Data de Emissão [DD/MM/YYYY]: "), "%d/%m/%Y")
        data_vencimento = datetime.strptime(input("- Data de Vencimento [DD/MM/YYYY]: "), "%d/%m/%Y")
        data_pagamento = datetime.strptime(input("- Data de Pagamento [DD/MM/YYYY]: "), "%d/%m/%Y")
        valor_boleto = float(input("- Valor do Boleto: "))
        valor_pago = float(input("- Valor Pago: "))
        if valor_pago <= 0: situacao = Pagamento.EmAberto
        elif valor_pago == valor_boleto: situacao = Pagamento.Pago
        else: situacao = Pagamento.PagoParcial
        boleto = Boleto(cod_barras, data_emissao, data_vencimento, data_pagamento, valor_boleto, valor_pago, situacao)
        print(boleto)
        if boleto.situacao != Pagamento.Pago:
            valor_pago = float(input("- Novo valor pago [0 para nada]: "))
            if valor_boleto <= 0: return
            boleto.pagar(valor_pago)
            print(boleto)

if __name__ == "__main__":
    BoletoUI.main()
