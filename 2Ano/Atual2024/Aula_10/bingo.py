from random import randint

class Bingo:
    def __init__(self, num: int) -> None:
        self.__num = num
        self.__balls = [ n for n in range(1, self.__num + 1) ]
        self.__drawed_balls: list[int] = []
    
    def draw(self) -> int:
        if len(self.__balls) <= 0: return -1

        ball_index: int = randint(0, len(self.__balls) - 1)
        ball: int = self.__balls.pop(ball_index)
        self.__drawed_balls.append(ball)

        return ball

    def drawed(self) -> list[int]: return self.__drawed_balls

class UI:
    @staticmethod
    def main() -> None:
        game = None
        
        while True:
            option: int = UI.menu()

            match option:
                case 1: 
                    game = UI.start_game()
                case 2:
                    if game is None:
                        print("Jogo não iniciado...")
                        continue
                    UI.draw_ball(game)
                case 3:
                    if game is None:
                        print("Jogo não iniciado...")
                        continue
                    UI.drawed_balls(game)
                case 4:
                    print("Saindo do Programa...")
                    return
                case _:
                    print("Opção Inválida. Tente Novamente...")
            
            print("=" * 50)
    
    @staticmethod
    def menu() -> int:
        print("1 - Iniciar um Novo Jogo\n2 - Sortear um Número\n3 - Verificar os Números Sorteados\n4 - Sair")
        return int(input("- Selecione uma opção acima: "))

    @staticmethod
    def start_game() -> Bingo:
        num: int = int(input("- Quantidade de Bolas: "))
        return Bingo(num)

    @staticmethod
    def draw_ball(bingo: Bingo) -> None:
        ball: int = bingo.draw()
        if ball <= -1:
            print("Bolas Acabaram...")
        else:
            print(f"Bola Sorteada: {ball}")

    @staticmethod
    def drawed_balls(bingo: Bingo) -> None:
        print("Bolas Sorteadas:")
        print(*bingo.drawed(), sep=" ")

if __name__ == "__main__":
    UI.main()
