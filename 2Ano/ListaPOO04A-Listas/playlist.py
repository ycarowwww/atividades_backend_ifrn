from datetime import date, timedelta

class Musica:
    def __init__(self, titulo: str, artista: str, album: str, data_inclusao: date, duracao: timedelta) -> None:
        self.__titulo = titulo
        self.__artista = artista
        self.__album = album
        self.__data_inclusao = data_inclusao
        self.__duracao = duracao

    def get_duracao(self) -> timedelta: return self.__duracao
    
    def __str__(self) -> str:
        return f"{self.__titulo} [{self.__artista} do {self.__album} {self.__data_inclusao}] - {self.__duracao}"
    
    def __add__(self, other: object | timedelta) -> timedelta:
        if isinstance(other, timedelta): return self.__duracao + other
        return self.__duracao + other.__duracao # type: ignore

class Playlist:
    def __init__(self, nome: str, descricao: str, musicas: list[Musica]) -> None:
        self.__nome = nome
        self.__descricao = descricao
        self.__musicas = musicas

    def inserir(self, nova_musica: Musica) -> None:
        self.__musicas.append(nova_musica)
    
    def listar(self) -> list[Musica]: 
        return self.__musicas

    def tempo_total(self) -> timedelta:
        tempo_total: timedelta = timedelta(seconds=0)
        for i in range(len(self.__musicas)):
            tempo_total += self.__musicas[i].get_duracao()
        
        return tempo_total
    
    def __str__(self) -> str:
        return f"{self.__nome} | {self.__descricao} : {len(self.__musicas)}"
    
m1: Musica = Musica("teste", "Teuku Miadora", "Miadora", date(1969, 3, 29), timedelta(minutes=15))
m2: Musica = Musica("teste2", "Rogerio da Silva", "Silvestre", date(1999, 4, 7), timedelta(minutes=7, seconds=30))

playlist1: Playlist = Playlist("sla", "sla meu, musicas estranhas", [m1, m2])

for i in playlist1.listar():
    print(i)

print(playlist1.tempo_total())