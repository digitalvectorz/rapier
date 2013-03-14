# parseconfig.py
# | Configuration Parser

COMMENT_CHAR = ';'
OPTION_CHAR = '='
DICT_CHAR_O	= '['
DICT_CHAR_C = ']'

def parse_config(filename):
	options = {}
	dict_cnt = 0
	f = open(filename)
	tline = ''
	for line in f:
		# First, remove comments:
		if COMMENT_CHAR in line:
			# split on comment char, keep only preceding part
			line, comment = line.split(COMMENT_CHAR, 1)
		# Second, find lines with an option=value:
		# Get dictionaries
		if DICT_CHAR_O in line:
			dict_cnt = dict_cnt + 1
			line = line.replace("[","")
		if dict_cnt:
			if DICT_CHAR_C in line:
				dict_cnt = dict_cnt - 1
				line = line.replace("]","")
			tline = tline + line.strip()
	
		if not dict_cnt:		
			if tline:
				line = tline
			if OPTION_CHAR in line:
				# split on option char
				option, value = line.split(OPTION_CHAR, 1)
				# strip spaces
				option = option.strip()
				value = value.strip()
				value = value.replace(',',' ')
				# store in dictionary:
				options[option] = value
				tline = ''

		print options
	f.close()
	return options

		
