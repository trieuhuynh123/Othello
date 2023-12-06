import pygame
from OthelloPackage.Draw import Draw
from OthelloPackage.OthelloGame import OthelloGame

class Controller:
    
    def __init__(self):
        self.current_player = False
        self.draw = Draw()
        self.game=OthelloGame(4,True)

    async def Start_Game(self):
        pygame.init()
        valid_moves_and_captuers=self.game.Valid_Moves_With_Captures(self.current_player)
        score={True:2,False:2}
        await self.draw.Draw_Board(valid_moves_and_captuers, self.game.board)
        self.draw.Show_Score(score[False], score[True], self.current_player)
        x_old, y_old = -1, -1
        running = True
        flag=False
        is_over = False
            
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if event.button == 1:  
                        x, y = event.pos 
                        x //= self.draw.cell_size
                        y -= self.draw.score_height
                        y //= self.draw.cell_size 
                        if (y, x) in valid_moves_and_captuers:
                            captures = valid_moves_and_captuers[y, x]
                            score[self.current_player] += (len(captures)+1)
                            score[not self.current_player] -= len(captures)
                            self.game.Move(y, x, self.current_player, captures)
                            valid_moves_and_captuers = self.game.Valid_Moves_With_Captures(not self.current_player)
                            if valid_moves_and_captuers:
                                self.draw.Draw_Flip(x, y , self.current_player,captures)
                                await self.draw.Draw_Board(valid_moves_and_captuers, self.game.board)    
                                self.current_player= not self.current_player
                                self.draw.Show_Score(score[False],score[True], self.current_player)
                            else:
                                valid_moves_and_captuers = self.game.Valid_Moves_With_Captures(self.current_player)
                                self.draw.Draw_Flip(x, y, self.current_player,captures)
                                await self.draw.Draw_Board(valid_moves_and_captuers, self.game.board)    
                                self.draw.Show_Score(score[False], score[True], self.current_player)
                                if not valid_moves_and_captuers:
                                    self.draw.Draw_Game_Over(score[False], score[True])
                                    is_over = True
                                    break
                                else:
                                    self.draw.Show_Notify(self.current_player)
                                    self.draw.Show_Score(score[False], score[True], self.current_player)
                        if self.current_player==True:
                            try:
                                x,y=self.game.Find_Best_Move(valid_moves_and_captuers)                           
                                click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(y*91, x*91+110), button=1)
                                pygame.event.post(click_event)
                            except:
                                return
                elif event.type == pygame.MOUSEMOTION  and not is_over:
                    x, y = pygame.mouse.get_pos()
                    x //= self.draw.cell_size
                    y -= self.draw.score_height
                    y //= self.draw.cell_size 
                    if (x, y) != (x_old,y_old):
                        x_old, y_old=x, y
                        if (y, x) in valid_moves_and_captuers:
                            await self.draw.Draw_Board(valid_moves_and_captuers, self.game.board)  
                            self.draw.Show_Captures(valid_moves_and_captuers[y, x])   
                            flag=True 
                        elif not (y, x) in valid_moves_and_captuers and flag:
                            await self.draw.Draw_Board(valid_moves_and_captuers, self.game.board)  
                            flag=False

    