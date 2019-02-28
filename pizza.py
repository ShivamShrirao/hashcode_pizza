#!/usr/bin/env python3

import sys
# r rows
# c columns
# [r,c]

# cell = M or T
# atleast L of each and atmost H total cells per slice

if len(sys.argv)!=3:
	print("Format:\npython3",sys.argv[0],"input.in out.txt")
	sys.exit(0)

with open(sys.argv[1],"r") as f:
	inp = f.read().split()

rows=int(inp.pop(0))
cols=int(inp.pop(0))
L=int(inp.pop(0))
H=int(inp.pop(0))

for i in range(len(inp)):
	inp[i]=list(inp[i])

# svd_inp=inp.copy()

class slice:
	def __init__(self):
		self.st_r = 0
		self.st_c = 0
		self.end_r = 0
		self.end_c = 0
		self.size = 1
		self.tomato = 0
		self.mush = 0
		self.satisfy=False

	def get_size(self):
		self.size = (self.end_r-self.st_r+1)*(self.end_c-self.st_c+1)
		return self.size

	def init_st(self):
		st=inp[self.st_r][self.st_c]
		if st=='T':
			self.tomato+=1
		else:
			self.mush+=1

	def count_right(self):
		if self.end_c<(cols-1):
			toms=0
			msh =0
			for j in range(self.st_r,self.end_r+1):
				if inp[j][self.end_c+1]=='T':
					toms+=1
				elif inp[j][self.end_c+1]=='M':
					msh+=1
				else:
					return 0,0
			return toms, msh
		else:
			return 0,0

	def expand_right(self, toms, msh):
		self.end_c+=1
		self.tomato+=toms
		self.mush+=msh

	def count_down(self):
		if self.end_r<(rows-1):
			toms=0
			msh =0
			for j in range(self.st_c,self.end_c+1):
				if inp[self.end_r+1][j]=='T':
					toms+=1
				elif inp[self.end_r+1][j]=='M':
					msh+=1
				else:
					return 0,0
			return toms, msh
		else:
			return 0,0

	def expand_down(self, toms, msh):
		self.end_r+=1
		self.tomato+=toms
		self.mush+=msh

	def count_left(self):
		if self.st_c>1:
			toms=0
			msh =0
			for j in range(self.st_r,self.end_r+1):
				if inp[j][self.st_c-1]=='T':
					toms+=1
				elif inp[j][self.st_c-1]=='M':
					msh+=1
				else:
					return 0,0
			return toms, msh
		else:
			return 0,0	

	def expand_left(self, toms, msh):
		self.st_c-=1
		self.tomato+=toms
		self.mush+=msh

	def count_up(self):
		if self.st_r>1:
			toms=0
			msh =0
			for j in range(self.st_c,self.end_c+1):
				if inp[self.st_r-1][j]=='T':
					toms+=1
				elif inp[self.st_r-1][j]=='M':
					msh+=1
				else:
					return 0,0
			return toms, msh
		else:
			return 0,0
			
	def expand_up(self, toms, msh):
		self.st_r-=1
		self.tomato+=toms
		self.mush+=msh

	def fill_some(self, num):
		for i in range(self.st_r,self.end_r+1):
			for j in range(self.st_c,self.end_c+1):
				inp[i][j]=num

slices=[slice()]
slices[0].init_st()
size=slices[-1].get_size()
ct=st=0
x,y=0,0
while st<rows*cols:
	ct+=1
	st+=1
	size=slices[-1].get_size()
	while size<=H:
		ct=0
		if (slices[-1].tomato < L) or (slices[-1].mush < L):
			mat={"rt":slices[-1].count_right(),
				"lt":slices[-1].count_left(),
				"uu":slices[-1].count_up(),
				"dn":slices[-1].count_down()}
			if slices[-1].tomato < slices[-1].mush:
				dr=0
			else:
				dr=1
			msx='rt'
			if mat['lt'][dr]>mat[msx][dr]:
				msx='lt'
			if mat['uu'][dr]>mat[msx][dr]:
				msx='uu'
			if mat['dn'][dr]>mat[msx][dr]:
				msx='dn'
			if mat[msx]==(0,0):
				break
			if msx=='rt':
				slices[-1].expand_right(mat[msx][0],mat[msx][1])
			elif msx=='lt':
				slices[-1].expand_left(mat[msx][0],mat[msx][1])
			elif msx=='uu':
				slices[-1].expand_up(mat[msx][0],mat[msx][1])
			else:
				slices[-1].expand_down(mat[msx][0],mat[msx][1])
		else:
			slices[-1].satisfy=True
			print('\r',x,y,end='')
			st=0
			slices[-1].fill_some(len(slices)-1)
			break
		size=slices[-1].get_size()

	if not slices[-1].satisfy:
		slices.pop()
	slices.append(slice())
	y=(y+1)%cols
	if y==0:
		x=(x+1)%rows
	while inp[x][y]!='T' and inp[x][y]!='M':
		y=(y+1)%cols
		if y==0:
			x=(x+1)%rows
	slices[-1].end_r=slices[-1].st_r=x
	slices[-1].end_c=slices[-1].st_c=y

print('\n')

def get_holes():
	done=False
	for x in range(rows):
		for y in range(cols):
			if inp[x][y]=='T' or inp[x][y]=='M':
				try:
					uu=inp[x-1][y]
					uu+=0
				except:
					uu=None
				try:
					rt=inp[x][y+1]
					rt+=0
				except:
					rt=None
				try:
					lt=inp[x][y-1]
					lt+=0
				except:
					lt=None
				try:
					dn=inp[x+1][y]
					dn+=0
				except:
					dn=None
				avs=[]
				if uu is not None:
					if slices[uu].get_size()<H:
						avs.append('uu')
				if rt is not None:
					if slices[rt].get_size()<H:
						avs.append('rt')
				if lt is not None:
					if slices[lt].get_size()<H:
						avs.append('lt')
				if dn is not None:
					if slices[dn].get_size()<H:
						avs.append('dn')
				ll=len(avs)
				for nu in range(ll):
					if avs[nu]=='uu':
						mts = slices[uu].count_down()
						if mts!=(0,0):
							slices[uu].end_r+=1
							if slices[uu].get_size()>H:
								slices[uu].end_r-=1
							else:
								slices[uu].satisfy=True
								done=True
								slices[uu].fill_some(uu)
					elif avs[nu]=='rt':
						mts = slices[rt].count_left()
						if mts!=(0,0):
							slices[rt].st_c-=1
							if slices[rt].get_size()>H:
								slices[rt].st_c+=1
							else:
								slices[rt].satisfy=True
								done=True
								slices[rt].fill_some(rt)
					elif avs[nu]=='lt':
						mts = slices[lt].count_right()
						if mts!=(0,0):
							slices[lt].end_c+=1
							if slices[lt].get_size()>H:
								slices[lt].end_c-=1
							else:
								slices[lt].satisfy=True
								done=True
								slices[lt].fill_some(lt)
					elif avs[nu]=='dn':
						mts = slices[dn].count_up()
						if mts!=(0,0):
							slices[dn].st_r-=1
							if slices[dn].get_size()>H:
								slices[dn].st_r+=1
							else:
								slices[dn].satisfy=True
								done=True
								slices[dn].fill_some(dn)
	return done

while get_holes():
	pass

f=open(sys.argv[2],'w')
f.write(str(len(slices)-1)+'\n')
total=0
for sl in slices:
	if sl.satisfy:
		print(sl.st_r,sl.st_c,sl.end_r,sl.end_c)
		f.write("{0} {1} {2} {3}\n".format(sl.st_r,sl.st_c,sl.end_r,sl.end_c))
		total+=sl.get_size()
f.close()
print("Total points:", total)
print("Max possible:", rows*cols)