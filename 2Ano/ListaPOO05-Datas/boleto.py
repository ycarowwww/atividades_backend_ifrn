from enum import Enum
from datetime import datetime

class Pagamento(Enum):
    EmAberto = 1
    PagoParcial = 2
    Pago = 3

class Boleto:
    def __init__(self, cod_barras: str, data_emissao: datetime, data_vencimento: datetime, valor_boleto: float) -> None:
        self.__cod_barras = cod_barras
        self.__data_emissao = data_emissao
        self.__data_vencimento = data_vencimento
        self.__data_pago = None
        self.__valor_boleto = valor_boleto
        self.__valor_pago = 0
        self.__situacao_pagamento = Pagamento.EmAberto
    
    def pagar(self, valor_pago: float, data_pagamento: datetime) -> None:
        if valor_pago <= 0: raise ValueError("Valor Pago tem que ser um Número maior que 0.")
        if self.__valor_pago >= self.__valor_boleto: raise Exception("O Boleto já foi totalmente Pago.")
        if data_pagamento > self.__data_vencimento: raise Exception("Boleto já Venceu.")

        if valor_pago >= self.__valor_boleto - self.__valor_pago:
            self.__valor_pago = self.__valor_boleto
            self.__situacao_pagamento = Pagamento.Pago
            self.__data_pago = datetime(data_pagamento.year, data_pagamento.month, data_pagamento.day)
        else:
            self.__valor_pago = valor_pago
            self.__situacao_pagamento = Pagamento.PagoParcial
    
    def situacao(self) -> Pagamento: return self.__situacao_pagamento

    def __str__(self) -> str:
        data_pago = self.__data_pago.strftime("%d/%m/%Y") if self.__data_pago else "Não Pago"
        return f"{self.__cod_barras} de R${self.__valor_boleto:.2f} de {self.__data_emissao.strftime("%d/%m/%Y")} para {self.__data_vencimento.strftime("%d/%m/%Y")} : Situação -> {self.__situacao_pagamento.name} | Valor Pago -> R${self.__valor_pago:.2f} | Data Pago -> {data_pago}"