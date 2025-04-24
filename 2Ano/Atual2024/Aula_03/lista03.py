from math import pi, sqrt, floor, ceil

print("Lista 03 de POO")
print("-" * 50)
# Lista de Funções

def Menor(x: int, y: int) -> int: return min(x, y)

def AreaCirculo(raio: float) -> float: return pi * raio ** 2

def Diagonal(b: float, h: float) -> float: return sqrt(b ** 2 + h ** 2)

def VolumeEsfera(r: float) -> float: return 4 / 3 * pi * r ** 3

def VolumeLitros(h: float, l: float, p: float) -> float: return 1000 * h * l * p

def Frete(massa: float, distancia: float) -> float: return 0.01 * massa * distancia

def MenorInteiro(x: float) -> int: return floor(x)

def Soma(inicio: int, fim: int) -> int: return sum(i for i in range(inicio, fim+1))

def Vogais(texto: str) -> list[str]:
    vogals: list[str] = []
    for c in "aeiou":
        if c in texto:
            vogals.append(c)
    return vogals

def Palavra(texto: str, pos: int) -> str:
    spaces_positions = [ i for i, c in enumerate(texto) if c == " " ]
    word_index = 0
    for p in spaces_positions:
        if p < pos:
            word_index += 1
    spaces_positions.insert(0, -1)
    spaces_positions.append(len(texto))
    return texto[spaces_positions[word_index]+1:spaces_positions[word_index+1]]

def Senha(texto: str) -> str:
    words = texto.split()
    words_len = [ str(len(w)) for w in words ]
    return "".join(words_len)

def RemoverEspacos(texto: str) -> str:
    return " ".join(texto.split())

def Referencia(nome: str) -> str:
    names = nome.split()
    last_name = names.pop()
    names = [ n[0] for n in names ]
    return last_name + " " + " ".join(names)

def UltimoDia(mes: int, ano: int) -> int:
    is_leap_year = True if ano % 400 == 0 else (True if ano % 4 == 0 and ano % 100 != 0 else False)
    days_per_month: dict[int, int] = {
        1 : 31,
        2 : 28 + (1 if is_leap_year else 0),
        3 : 31,
        4 : 30,
        5 : 31,
        6 : 30,
        7 : 31,
        8 : 31,
        9 : 30,
        10 : 31,
        11 : 30,
        12 : 31
    }
    return days_per_month[mes]

def MMC(a: int, b: int) -> float:
    def MDC(x: int, y: int) -> int:
        if x == 0 or y == 0:
            return max(x, y)
        else:
            return MDC(y, x % y)
    
    return abs(a * b) / MDC(a, b)

def Primo(n: int) -> bool:
    if n % 2 == 0: return False
    for i in range(3, ceil(n / 2) + 1, 2):
        if n % i == 0:
            return False
    return True

def VelocidadeMedia(distancia: float, tempo: str) -> float:
    time = list(map(int, tempo.split(":")))
    time = time[0] + time[1] / 60 + time[2] / 3600
    return distancia / time

def MostrarOrdenado(a: float, b: float, c: float) -> list[float]:
    nums = [ a, b, c ]
    l = len(nums)
    for i in range(l-1):
        min_idx = i
        for j in range(i+1, l):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums
