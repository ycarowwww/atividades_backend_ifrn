from datetime import datetime, timedelta

class Treino:
    def __init__(self, id_t: int, date: datetime, distance: float, time: timedelta) -> None:
        self.id_t = id_t
        self.date = date
        self.distance = distance
        self.time = time
    
    @property
    def id_t(self) -> int: return self.__id_t

    @id_t.setter
    def id_t(self, new_value: int) -> None:
        self.__id_t = new_value
    
    @property
    def date(self) -> datetime: return self.__data

    @date.setter
    def date(self, new_value: datetime) -> None:
        self.__data = new_value
    
    @property
    def distance(self) -> float: return self.__distance

    @distance.setter
    def distance(self, new_value: float) -> None:
        self.__distance = new_value
    
    @property
    def time(self) -> timedelta: return self.__time

    @time.setter
    def time(self, new_value: timedelta) -> None:
        self.__time = new_value

    def __str__(self) -> str:
        return f"Treino : {self.id_t} em {self.date.strftime("%d/%m/%Y")} com {self.distance} de distância e {self.time} de tempo."

class TreinoUI:
    __treinos: list[Treino] = []
    __id_atual = 0

    @staticmethod
    def menu() -> int:
        print("1 - Inserir treino\n2 - Listar treinos\n3 - Listar um treino específico\n4 - Atualizar treino\n5 - Excluir treino\n6 - Treino mais rápido\n7 - Sair")
        return int(input("- Selecione uma opção acima: "))

    @classmethod
    def main(cls) -> None:
        while True:
            option = cls.menu()

            match option:
                case 1: cls.inserir()
                case 2: cls.listar()
                case 3: cls.listar_id()
                case 4: cls.atualizar()
                case 5: cls.excluir()
                case 6: cls.mais_rapido()
                case 7: 
                    print("Saindo do programa...")
                    break
                case _:
                    print("Opção Inválida!")

    @classmethod
    def inserir(cls) -> None:
        date = datetime.strptime(input("- Insira a data [dd/mm/yyyy]: "), "%d/%m/%Y")
        distance = float(input("- Insira a distância percorrida: "))
        time = datetime.strptime(input("- Insira o tempo [hh:mm:ss]: "), "%H:%M:%S")
        time = timedelta(seconds=time.second, minutes=time.minute, hours=time.hour)
        cls.__treinos.append(Treino(cls.__id_atual, date, distance, time))
        cls.__id_atual += 1
        print("Data adicionada com Sucesso!")
    
    @classmethod
    def listar(cls) -> None:
        for treino in cls.__treinos:
            print(treino)

    @classmethod
    def listar_id(cls) -> None:
        search_id = int(input("- Insira o ID procurado: "))
        
        for treino in cls.__treinos:
            if treino.id_t == search_id:
                print(treino)
                break
        else:
            print("Nenhum treino encontrado.")

    @classmethod
    def atualizar(cls) -> None:
        search_id = int(input("- Insira o ID para atualizar: "))
        
        for treino in cls.__treinos:
            if treino.id_t == search_id:
                print(treino)
                treino.date = datetime.strptime(input("- Insira a nova data [dd/mm/yyyy]: "), "%d/%m/%Y")
                treino.distance = float(input("- Insira a nova distância percorrida: "))
                time = datetime.strptime(input("- Insira o novo tempo [hh:mm:ss]: "), "%H:%M:%S")
                time = timedelta(seconds=time.second, minutes=time.minute, hours=time.hour)
                treino.time = time
                print("Treino atualizado com sucesso!")
                break
        else:
            print("Treino não encontrado...")

    @classmethod
    def excluir(cls) -> None:
        search_id = int(input("- Insira o ID para excluir: "))
        
        for treino in cls.__treinos:
            if treino.id_t == search_id:
                cls.__treinos.remove(treino)
                print("Treino removido com sucesso.")
                break
        else:
            print("Nenhum treino encontrado.")

    @classmethod
    def mais_rapido(cls) -> None:
        if len(cls.__treinos) <= 0:
            print("Treinos não encontrados.")
            return
        
        treino_procurado = None
        speed_treino = 0
        for treino in cls.__treinos:
            speed = treino.distance / treino.time.seconds
            if speed > speed_treino:
                treino_procurado = treino
                speed_treino = speed
        
        print("Treino encontrado:")
        print(treino_procurado)
        print(f"Velocidade: {speed_treino:.2f}")

if __name__ == "__main__":
    TreinoUI.main()
