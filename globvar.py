main_instance=3596686256
var2='Hello'

def set(**kwargs):
	file = open('globvar.py', 'r')
	prev = file.read().split('\n')
	file.close()
	for i,j in kwargs.items():
		ind=0
		for f in prev[:2]:
			dt = f.split('=')
			if dt[0] == i:
				dt[1] = j
				prev[ind] = f'{dt[0]}={dt[1]}'
			
			ind += 1
			print(ind)
		
	wfile = open('globvar.py', 'w')
	for f in prev:
		wfile.write(f+'\n')
	wfile.close()

if __name__ == '__main__':
		set(main_instance=0b11001, var2="'Hello'")
		
			
		
		
			














