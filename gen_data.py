import os, sys

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage : python <progname> <input_file> <output_file>'
		exit()
	progname, input_file, output_file = sys.argv

	input_file = open(input_file, 'r')
	output_file = open(output_file, 'w')

	for line in input_file:
		p = line.split()
		q = []
		for x in p:
			if x == 'yes':
				q.append(1);
			else:
				q.append(0);
		if float(p[0].replace(',', '.')) > 38.0 - 1e-9:
			q[0] = 1
		q = [x[0] + 1 for x in enumerate(q) if x[1] == 1]
		output_file.write(' '.join(map(str, q)) + '\n')

	input_file.close()
	output_file.close()
