import os, sys, math

def load_data(path):
	f = open(path, 'r')
	ret = []
	for line in f:
		p = frozenset(map(int, line.split()))
		ret.append(p)
	f.close()
	return ret

lazy = {}

def count_set(s, data):
	s = frozenset(s)
	if s in lazy:
		return lazy[s]
	ret = 0
	for x in data:
		if s.issubset(x):
			ret += 1
	lazy[s] = ret
	return ret

def gen_subset(s):
	ret = []
	for x in s:
		ret = ret + [y | set([x]) for y in ret]
		ret.append(set([x]))
	ret.remove(s)
	return ret

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage : python <progname> <data_file>'
		exit()
	progname, data_file = sys.argv
	data = load_data(data_file)

	min_support = 0.4
	min_confidence = 0.7

	L = {}

	for x in reduce(lambda x, y : list(x) + list(y), data):
		x = frozenset([x])
		L.setdefault(x, 0)
		L[x] += 1

	n = len(data)
	abs_min_support = math.ceil(min_support * n)
	abs_min_confidence = math.ceil(min_confidence * n)

	_L = {}
	for x in L:
		if L[x] >= abs_min_support:
			_L[x] = L[x]
	L = _L

	max_k = len(L)

	all_L = {}

	for k in range(2, max_k + 1):
		new_L = {}
		for x in L:
			for y in L:
				if x == y : continue
				uset = x | y
				iset = x & y
				dset = uset - iset
				if len(dset) != 2 : continue
				if uset in new_L : continue
				flag = True
				for c in uset:
					test = uset - set([c])
					if test not in L:
						flag = False
				if flag:
					cnt = count_set(uset, data)
					if cnt < abs_min_support : continue
					new_L[uset] = cnt
		if len(new_L) == 0 : break
		L = new_L
		all_L.update(new_L)
	
	for x in all_L:
		st = ', '.join(map(str, list(x)))
		print '(%s), supp = %.2f' % (st, 1.0 * all_L[x] / n)
	
	print '\n==========\n'

	pattern  = []

	for x in all_L:
		la = gen_subset(x)
		for a in la:
			b = x - a
			na = count_set(a, data)
			nab = all_L[x]
			conf = 1.0 * nab / na
			if conf > min_confidence:
				nb = count_set(b, data)
				lift = (1.0 * nab / n) / (1.0 * na / n * nb / n)
				pattern.append((a, b, 1.0 * nab / n, conf, lift))

	ans = []

	for (a, b, supp, conf, lift) in pattern:
		sta = ', '.join(map(str, list(a)))
		stb = ', '.join(map(str, list(b)))
		if b == set([7]) or b == set([8]):
			ans.append((a, b, supp, conf, lift))
		print '(%s) --> (%s), supp = %.2f, conf = %.2f, lift = %.2f' % (sta, stb, supp, conf, lift)

	print '\n==========\n'

	ans.sort(cmp = lambda x, y : cmp(x[3], y[3]), reverse = True)

	for (a, b, supp, conf, lift) in ans:
		sta = ', '.join(map(str, list(a)))
		stb = ', '.join(map(str, list(b)))
		print '(%s) --> (%s), supp = %.2f, conf = %.2f, lift = %.2f' % (sta, stb, supp, conf, lift)