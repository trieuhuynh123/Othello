import asyncio
import pygame
black =  (0, 0, 0)
green = (0, 128, 0)
white = (255, 255, 255)

class Draw:
    def __init__(self):
        self.screen_width=720
        self.screen_height=830
        self.score_height=110
        self.cell_size=90
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Othello")
        self.piece = {True: pygame.image.load("True.png"),
                    False: pygame.image.load("False.png")}
        self.piece_90 = {True: pygame.transform.smoothscale(pygame.image.load("True.png"), (90, 90)),
                    False: pygame.transform.smoothscale(pygame.image.load("False.png"), (90, 90))}
    
    def Draw_Game_Over(self, dark_score, light_score):

        self.screen.fill(black)
        self.screen.blit(self.piece_90[False], (50, 25))
        self.screen.blit(self.piece_90[True], (50, 125))
        font = pygame.font.Font(None, 150)
        text = font.render(f": {dark_score}", True, (128, 128, 128))
        self.screen.blit(text, (200, 25))
        text = font.render(f": {light_score}", True, (128, 128, 128))
        self.screen.blit(text, (200, 125))
        self.screen.blit(pygame.transform.smoothscale(pygame.image.load("Crown.png"), (400, 400)),(159, 200))
        if dark_score>light_score:
            self.screen.blit(pygame.transform.smoothscale(pygame.image.load("False.png"), (400, 400)),(160, 400))
        elif dark_score<light_score:
            self.screen.blit(pygame.transform.smoothscale(pygame.image.load("True.png"), (400, 400)),(160, 400)) 
        pygame.display.flip()

    def Show_Notify(self, color_player):

        transparent_image = pygame.Surface((self.screen_width, 110), pygame.SRCALPHA)
        font = pygame.font.Font("times.ttf", 50)
        noti = "Quân đen mất Lượt" if color_player else "Quân trắng mất lượt"
        text = font.render(noti, True, (255, 0, 0))
        for i in range(-45, 1):
            transparent_image.blit(text, (i*10, 0))
            self.screen.blit(transparent_image, (0, 0))   
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            transparent_image.fill(black)
        for i in range(3, 72):
            transparent_image.blit(text, (i*5, 0))
            self.screen.blit(transparent_image, (0, 0))   
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            transparent_image.fill(black)
        for i in range(36, 81):
            transparent_image.blit(text, (i*10, 0))
            self.screen.blit(transparent_image, (0, 0))   
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            transparent_image.fill(black)

    def Show_Captures(self, captures):
        possible=pygame.transform.smoothscale(pygame.image.load("Possible.png"), (80, 80))
        capture_buffer = pygame.Surface((self.screen_width, self.screen_height - self.score_height), pygame.SRCALPHA)
        for x, y in captures:
            capture_buffer.blit(possible, (y * self.cell_size + 5, x * self.cell_size + 5))
        self.screen.blit(capture_buffer, (0, self.score_height))
        pygame.display.flip()

    def Draw_Flip(self,x,y,color_player, captures): 
        self.screen.blit(self.piece_90[color_player], (x* self.cell_size, y* self.cell_size+ self.score_height))
        pygame.display.flip()
        piece_buffer = pygame.Surface((self.screen_width, self.screen_height - self.score_height), pygame.SRCALPHA)
        for i in range(0, 91, 5):
            for x, y in captures:
                y = y * self.cell_size + (90 - i) / 2
                x = x * self.cell_size + (90 - i) / 2
                piece_buffer.blit(pygame.transform.smoothscale(self.piece[color_player], (i, i)), (y, x))
            self.screen.blit(piece_buffer, (0, self.score_height))
            pygame.display.flip()
            pygame.time.delay(16)

    async def Draw_Pieces(self, board):
        # vẽ quân cờ
        piece_buffer = pygame.Surface((self.screen_width, self.screen_height - self.score_height), pygame.SRCALPHA)
        for x in range(8):
            for y in range(8):
                if board[x][y] is not None:
                    piece_buffer.blit(self.piece_90[board[x][y]], (y * self.cell_size, x * self.cell_size))
        self.screen.blit(piece_buffer, (0, self.score_height))
    
    async def Draw_Gird(self):
        
        # vẽ lười dọc   
        for i in range(8):
            x = i * self.cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (x, self.score_height), (x, self.screen_height))

        # Vẽ lưới ngang
        for i in range(8):
            y = i * self.cell_size + self.score_height
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.screen_width, y))

    async def Draw_Board(self, valid_moves_and_captuers, board):

        # vẽ nền màng hình
        self.screen.fill(green, (0, self.score_height, self.screen_height, self.screen_height))
        await asyncio.gather(self.Draw_Gird(), self.Draw_Pieces(board), self.Show_Valid_Moves(valid_moves_and_captuers))
        pygame.display.flip()

    async def Show_Valid_Moves(self, valid_moves_and_captuers):

        # vẽ các nước đi hợp lệ lên bàn cờ
        possible_buffer = pygame.Surface((self.screen_width, self.screen_height - self.score_height), pygame.SRCALPHA)
        possible=pygame.transform.smoothscale(pygame.image.load("Possible.png"), (80, 80))
        for move, captures in valid_moves_and_captuers.items():
            x,y=move
            # số quân ăn được khi đặt ở đó
            font = pygame.font.Font(None, 50)
            str ="{}".format(len(captures))
            text = font.render(str, True, black)
            possible_buffer.blit(possible, (y * self.cell_size + 5, x * self.cell_size + 5))
            possible_buffer.blit(text, (y * self.cell_size - 10 * len(str) + 45, x * self.cell_size + 30))
        self.screen.blit(possible_buffer, (0, self.score_height))
        
    
    def Show_Score(self, dark_score, light_score, current):
            
        score_buffer = pygame.Surface((self.screen_width, self.score_height))
        score_buffer.fill(black)
    
        score_buffer.blit(self.piece_90[False],(230,10))
        score_buffer.blit(self.piece_90[True],(400,10))

        if current:
            score_buffer.blit(pygame.transform.smoothscale(pygame.image.load("light.png"), (150, 150)),(370,-20))
        else:
            score_buffer.blit(pygame.transform.smoothscale(pygame.image.load("light.png"), (150, 150)),(200,-20))

        font = pygame.font.Font(None, 150)

        str_score = "{}".format(dark_score)
        text = font.render(str_score, True, white)
        score_buffer.blit(text, ( - len(str_score) * 55 + 215, 10))

        str_score = "{}".format(light_score)
        text = font.render(str_score, True, white)
        score_buffer.blit(text, (505, 10))

        self.screen.blit(score_buffer, (0, 0))

        pygame.display.flip()
