import  copy
import  math
cost_table = [
            [100, -20, 10, 5, 5, 10, -20, 100], 
            [-20, -50, -2, -2, -2, -2, -50, -20], 
            [10, -2, -1, -1, -1, -1, -2, 10], 
            [5, -2, -1, -1, -1, -1, -2, 5], 
            [5, -2, -1, -1, -1, -1, -2, 5], 
            [10, -2, -1, -1, -1, -1, -2, 10], 
            [-20, -50, -2, -2, -2, -2, -50, -20], 
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
    
class  OthelloGame:
    def  __init__(self, depth, color, size=8):
        self.size = size
        self.board = [[None] * size  for _ in range(size)]  #  Mảng  2D  đại  diện  cho  bàn  cờ
        self.depth = depth
        self.bot = color
        self.Initialize_Board()

    def  Initialize_Board(self):
        self.board[3][3] = True
        self.board[4][4] = True
        self.board[4][3] = False
        self.board[3][4] = False

    def  Move(self, x, y, color_player, captures):
        """
        Thực  hiện  nước  cờ  và  lật  các  quân  bị  bắt.
        Args:
            color_player:  màu  của  quân  đang  được  xét.
            captures: quân sẽ bị lật
        """
        self.board[x][y] = color_player
        self.Flip_Captures(captures)
        
    def  Valid_Moves_With_Captures(self, color_player):
        """
        Trả  về  các  quân  cờ  của  đối  thủ  sẽ  bị  bắt  nếu  đi  vào  tạo  độ  x, y.
        Args:
            color_player:  màu  của  quân  đang  được  xét.

        Returns:
            Một  dic  trong  đó  key  là  (x, y)  tạo  độ  nước  đi  hợp  lệ  và  value  là  1  list  chứa  tọa  độ  các  quân  sẽ  bị  bắt.
        """
        return {(x, y): opponents_capture
                for x in range(8) for y in range(8)
                if self.board[x][y] is None and (opponents_capture := self.Find_Captures(x, y, color_player))}

    def  Find_Captures(self, x, y, color_player):
        """
        Trả  về  các  quân  cờ  của  đối  thủ  sẽ  bị  bắt  nếu  đi  vào  tạo  độ  x, y.
        Args:
            x, y:  tạo  độ  đặt  quân  xuống.
            color_player:  màu  của  quân  vừa  đặt  xuống.

        Returns:
            Một  list  chứa  tạo  độ  các  quân  bị  lật.
        """
        captures=[]  #  mảng  chứa  các  quân  bị  bắt

        #mảng  dùng  để  duyệt  8  hướng  xem  có  ăn  được  quân  nào  không
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dx, dy in directions:
            x_check, y_check = x + dx, y + dy
            temp_captures=[]  #  mảng  chứa  các  quân  bị  bắt  ở  mỗi  hướng

            #  cho  vòng  lặp  chạy  nếu  đang  còn  trong  bàn  cờ, không  gặp  ô  nào  trống  và  phải  khác  màu  quân  vừa  đặt  xuống
            while  0 <= x_check < self.size and 0 <= y_check < self.size and self.board[x_check][y_check] != None and self.board[x_check][y_check] != color_player:
                temp_captures.append((x_check, y_check))
                x_check += dx
                y_check += dy

            #  nếu  hết  vòng  lặp  trên  mà  vẫn  trong  bàn  cờ  và  tại  đó  là  quân  cùng  màu  hay  không
            if 0 <= x_check < self.size and 0 <= y_check < self.size and self.board[x_check][y_check] == color_player:
                captures += temp_captures

        return captures
      
    def  Flip_Captures(self, captures):
        """
        Lật  các  quân  bị  bắt.
        Args:
            captures:  list  chứa  tọa  độ  các  quân  sẽ  bị  lật.
        """
        for x, y in captures:
            self.board[x][y] = not self.board[x][y]
    
    def  Find_Best_Move(self, valid_moves_and_captuers):
        """
        Tìm  ra  nước  đi  tốt  nhất.
        Args:
            valid_moves_and_captuers:  một  dic  có  key  là  nước  cờ  và  value  là  list  chứa  các  quân  sẽ  bị  lật.
        Return:
            Một  tuple  (x, y)  là  nước  đi  tốt  nhất
        """
        best_move=None
        best_eval = -math.inf
        for move, captures in valid_moves_and_captuers.items():
            x, y = move
            new_game = copy.deepcopy(self)  
            new_game.Move(x, y, self.bot, captures)
            eval = new_game.Alpha_Beta(False, self.depth-1, -math.inf, math.inf, not self.bot)
            if eval  >  best_eval:
                best_eval = eval
                best_move=  move
        return best_move

    def  Alpha_Beta(self, maximizing_player, depth, alpha, beta, color_player):
        """
        Tính điểm tại trạng thái.
        Args:
            maximizing_player: dùng để phân biệt người chơi max hay min.
            depth: độ sâu của trạng thái hiện tại.
            alpha: giá trị của alpha.
            beta: giá trị của beta.
            color_player: lược của người chơi nào.
        Return:
            Giá trị điểm tại trạng thái đó.
        """
        if depth == 0:
            return self.Value_Board(self.board)
        
        valid_moves_and_captuers = self.Valid_Moves_With_Captures(color_player)

        if not valid_moves_and_captuers:
            if not self.Valid_Moves_With_Captures(not color_player):
                return self.Value_Board(self.board)
            return self.Alpha_Beta(not maximizing_player, depth, alpha, beta, not color_player)
            
        if maximizing_player:
            max_eval = -math.inf
            for move, opponents_to_capture in valid_moves_and_captuers.items():
                x, y = move
                new_game = copy.deepcopy(self)  
                new_game.Move(x, y, color_player, opponents_to_capture)
                eval = new_game.Alpha_Beta(False, depth-1, alpha, beta, not color_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move, opponents_to_capture in valid_moves_and_captuers.items():
                x, y = move
                new_game = copy.deepcopy(self)  
                new_game.Move(x, y, color_player, opponents_to_capture)
                eval = new_game.Alpha_Beta(True, depth-1, alpha, beta, not color_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def  Value_Board(self, grid):
        """
        Dựa vào cost_table tính điểm các quân cờ trên bàn cờ.
        Args:
            grid: vị trí quân cờ.
        Return:
            Giá trị điểm của bàn cờ.
        """
        score = 0
        color_oponent = not self.bot
        for row in range(0, 8):
            for col in range(0, 8):
                if grid[row][col] == self.bot:
                    score += cost_table[row][col]
                elif grid[row][col] == color_oponent:
                    score -= cost_table[row][col]
        return score
