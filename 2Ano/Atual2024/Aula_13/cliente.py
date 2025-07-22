import json

class Cliente:
    def __init__(self, id_client: int, name: str, email: str, fone: str) -> None:
        self.id_client = id_client
        self.name = name
        self.email = email
        self.fone = fone

    @property
    def id_client(self) -> int: return self.__id_client

    @id_client.setter
    def id_client(self, new_value: int) -> None:
        self.__id_client = new_value

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, new_value: str) -> None:
        self.__name = new_value

    @property
    def email(self) -> str: return self.__email

    @email.setter
    def email(self, new_value: str) -> None:
        self.__email = new_value

    @property
    def fone(self) -> str: return self.__fone

    @fone.setter
    def fone(self, new_value: str) -> None:
        self.__fone = new_value

    def __str__(self) -> str:
        return f"Cliente {self.id_client} : {self.name} - {self.email} -> {self.fone}"
    
class ClienteUI:
    __objects: list[Cliente] = []
    __cur_id: int = 0
    
    @staticmethod
    def menu() -> int:
        print("1 - Inserir Cliente\n2 - Listar Clientes\n3 - Listar Cliente específico\n4 - Atualizar Cliente\n5 - Excluir Cliente\n6 - Abrir clientes de um arquivo\n7 - Salvar clientes em um arquivo\n8 - Sair")
        return int(input("- Escolha uma opção acima: "))
    
    @classmethod
    def main(cls) -> None:
        while True:
            opt = cls.menu()

            match opt:
                case 1: cls.inserir()
                case 2: cls.listar()
                case 3: cls.listar_id()
                case 4: cls.atualizar()
                case 5: cls.excluir()
                case 6: cls.abrir()
                case 7: cls.salvar()
                case 8:
                    print("Saindo do programa...")
                    break
                case _: print("Opção Inválida!")

    @classmethod
    def inserir(cls) -> None:
        name = input("- Nome do Novo Cliente: ")
        email = input("- Email do Novo Cliente: ")
        fone = input("- Fone do Novo Cliente: ")
        cls.__objects.append(Cliente(cls.__cur_id, name, email, fone))
        cls.__cur_id += 1

    @classmethod
    def listar(cls) -> None:
        if len(cls.__objects) <= 0:
            print("Não há clientes.")
            return
    
        for c in cls.__objects: print(c)

    @classmethod
    def listar_id(cls) -> None:
        if len(cls.__objects) <= 0:
            print("Não há clientes.")
            return
    
        find_id = int(input("- Insira o ID procurado: "))
        for c in cls.__objects: 
            if c.id_client == find_id:
                print(c)
                break
        else:
            print(f"Cliente {find_id} não encontrado!")
    
    @classmethod
    def atualizar(cls) -> None:
        if len(cls.__objects) <= 0:
            print("Não há clientes.")
            return
    
        find_id = int(input("- Insira o ID para ser atualizado: "))
        for c in cls.__objects: 
            if c.id_client == find_id:
                print(c)
                c.name = input("- Insira o novo nome: ")
                c.email = input("- Insira o novo email: ")
                c.fone = input("- Insira o novo fone: ")
                print(c)
                break
        else:
            print(f"Cliente {find_id} não encontrado!")
    
    @classmethod
    def excluir(cls) -> None:
        if len(cls.__objects) <= 0:
            print("Não há clientes.")
            return
    
        find_id = int(input("- Insira o ID para ser excluído: "))
        for c in cls.__objects: 
            if c.id_client == find_id:
                cls.__objects.remove(c)
                print("Cliente excluido com sucesso!")
                break
        else:
            print(f"Cliente {find_id} não encontrado!")

    @classmethod
    def abrir(cls) -> None:
        filename = input("- Insira o nome do arquivo: ")

        with open(filename, "r") as json_file:
            data_clients = json.load(json_file)
            cls.__objects.clear()
            cls.__cur_id = 0

            for c in data_clients:
                cls.__objects.append(Cliente(c["id_client"], c["name"], c["email"], c["fone"]))
                cls.__cur_id = max(cls.__cur_id, c["id_client"])
            
            print("Arquivo aberto com sucesso!")

    @classmethod
    def salvar(cls) -> None:
        if len(cls.__objects) <= 0:
            print("Não há objetos.")
            return
        
        all_objs_json: list[dict] = []
        for c in cls.__objects:
            c_obj = vars(c)
            c_new_obj = {}

            for k in c_obj.keys():
                c_new_obj[cls.__unmangle_str(k)] = c_obj[k]
            
            all_objs_json.append(c_new_obj)
        
        with open("clientes.json", "w") as json_file:
            json.dump(all_objs_json, json_file, indent=4)
            print("Arquivo gravado com sucesso!")
    
    @staticmethod
    def __unmangle_str(name: str) -> str:
        return name.split("__")[1] if "__" in name else name

if __name__ == "__main__":
    ClienteUI.main()
