class BingoBox:
    player = None
    row = None
    column = None
    match_cells = None
    match_consecutive_cell = 3
    
    def __init__(self, row, column, match_if=True):
        self.row = row
        self.column = column
        self.match_cells = match_if
    
    def redim(self, row, col):
        self.row = row
        self.column = col
        
    def assign(self, ls):
        self.player = ls
        
    def find_match(self, cond):
        self.match_cells = cond
        #depricated
    
    def alter(self, condition):
        #depricated
        if self.match_cells == False:
            return not condition
        
        else: return condition
    
    def match_consecutive(self, n:int):
        self.match_consecutive_cell = n
        
    def check_column(self, find=1):
        total = 0
        for i in range(self.column):
            self.match = True
            flag = self.match_consecutive_cell
            for j in range(self.row):
                if self.player[i + self.row * j] != find:
                    self.match = False
                    break
                flag-=1
                
                if flag == 0:
                    break

            if self.match:
                print(f'[Column {i}]: match')
                total += 1

        return total

    def check_row(self, find=1):
        total = 0
        flag = self.match_consecutive_cell
        for i in range(self.row):
            self.match = True
            for j in range(self.column):
                if self.player[i * self.column + j] != find:
                    self.match = False
                    break
                
                flag -= 1
                if flag == 0:
                    break

            if self.match:
                print(f'[Row   {i} ]:  match')
                total += 1

        return total

    def check_diagonal(self, find=1):
        total = 0
        match1, match2 = (True, True)
        flag = self.match_consecutive_cell
        
        for j in range(self.row):
            if self.player[self.column-1 + (self.row-1) * j] != find:
                match1 = False

            if self.player[(self.column+1) * j] != find:
                match2 = False

            if not(match1 or match2):
                break
            
            flag -= 1
            if flag == 0:
                break
            
        if match2:
            total += 1
            print('[Diagonal 1]:  match') 

        if match1: 
            total += 1
            print('[Diagonal 2]: match')

        return total

    def check_all(self, find=1):
        return self.check_column(find=find) + self.check_diagonal(find=find) + self.check_row(find=find)
  
 

if __name__ == '__main__':
	B = BingoBox(3,3)
	i = map(lambda x: list(map(int, x.split())), input().split('\n'))
	
	for f in i:
		print(f)
		B.assign(f)
	print(B.check_all(find = -1))

'''
0 0 0 -1 -1 -1 1 1 1
-1 0 -1 1 -1 1 -1 1 -1
-1 1 1 -1 -1 1 -1 1 1
'''
 
 