import sys

api_table_database = {}
max_brief_len = 0
max_param_len = 0
max_prototype_len = 0

num_args = len(sys.argv)
if (num_args != 5):
	print ("\nScript expects following inputs")
	print ("\narg1 : Input header file") 
	print ("\narg2 : Output file to update table")
	print ("\narg3 : Table start line")
	print ("\narg4 : Table end line")
	sys.exit(1)

# Check to ensure the presence of input header file
try:
	with open(sys.argv[1]) as file:
		pass
except IOError:
	print("\nargv[1] : The input header file is not present")
	sys.exit(1)


# Check to ensure the presence of output file
try:
	with open(sys.argv[2]) as file:
		pass
except IOError:
	print("\nargv[2] : The output file not available to edit")
	sys.exit(1)

start_line = int(sys.argv[3])
end_line = int(sys.argv[4])

def get_table_details(in_file, api_table_database, max_brief_len, max_param_len, max_prototype_len):
	api_cnt = 0
	param_collection_started = 0
	param_start_idx = 0
	api_table_details = []
	# Read the input file
	with open(in_file, 'r') as f:
		for line in f:
			if ('@brief' in line):
				#print(line[line.find('-') + 1:].strip())
				api_table_details.append(1)
				api_table_details.append(line[line.find('-') + 1:].strip())
				continue
			if ('@param' in line):
				param_start_idx = line.find('-') + 2
				#print(line[param_start_idx:].rstrip('\n'))
				api_table_details.append(1)
				api_table_details.append(line[param_start_idx:].rstrip('\n')+'<br/>')
				param_collection_started = 1
				continue
			if (param_collection_started == 1) and ('@return' not in line):
				#print(line[param_start_idx:].rstrip('\n'))
				api_table_details[2] = api_table_details[2] + 1
				api_table_details.append(line[param_start_idx:].rstrip('\n')+'<br/>')
			else:
				param_collection_started = 0
			if ('(' in line) and (';' == line[-2]) and ('/*' != line[:2]) and ('*' != line.strip()[0]):
				#print(line.rstrip('\n'))
				api_table_details.append(1)
				api_table_details.append(line.rstrip('\n'));
				api_cnt = api_cnt + 1
				api_table_database.update({api_cnt:api_table_details})
				api_table_details = []
	print("api_cnt = " + str(api_cnt))
	#print(api_table_database)

def get_max_len(api_table_database):
	"""
	Return the max text length for Prototype, Description and Parameters field of API table

	"""
	pro_len = 0
	des_len = 0
	par_len = 0
	for idx, details in api_table_database.items():
		pro_idx = 5 + details[2] - 1 
		if pro_len < len(details[pro_idx]):
			pro_len = len(details[pro_idx])
		if des_len < len(details[1]):
			des_len = len(details[1])
		if par_len < len(details[3]):
			par_len = len(details[3])
	return pro_len, des_len, par_len

def populate_table(out_file, api_table_databse, start_line, end_line):
	if (start_line > end_line) and (start_line < 1):
		print("\nInvalid input : The table insertion line range is not correct");
		sys.exit(1)
	
	with open(out_file, 'r') as textobj:
		line_list = list(textobj)	#puts all lines in a list

	if not line_list:
		print("\nThe sys.argv[2] is empty and the table insertion range is not correct!")
		sys.exit(1)

	start_idx = start_line
	end_idx   = end_line

	while (start_line <= end_line) and (start_line <= len(line_list)):
		del line_list[start_line - 1]
		end_line = end_line - 1

	# Get the max text length for each field : Prototype, Description and Parameters
	max_prototype_len, max_description_len, max_param_len = get_max_len(api_table_database)
	print(max_prototype_len)
	print(max_description_len)
	print(max_param_len)

	# Start populating the API table
	# First update table heading
	pro_string = "Prototype"
	des_string = "Description"
	par_string = "Parameters"
	line_list.insert(start_idx - 1, "| No | "+ pro_string + " "*(max_prototype_len-1-len(pro_string)) + "| " 
	                                 + des_string + " "*(max_description_len-1-len(des_string)) + "| " 
					 + par_string + " "*(max_param_len-1-len(par_string)) + "|\n")
	start_idx += 1				
	line_list.insert(start_idx - 1, "|----|" + "-"*max_prototype_len + "|" + "-"*max_description_len + "|" + "-"*max_param_len + "|\n")

	start_idx += 1
	for idx, details in api_table_database.items():
		pro_idx = 5 + details[2] - 1
		line_list.insert(start_idx - 1, "| " + str(idx).zfill(2) + " | " + details[pro_idx] + " "*(max_prototype_len-1-len(details[pro_idx])) + "| "
						+ details[1] + " "*(max_description_len-1-len(details[1])) + "| "
						+ details[3] + " "*(max_param_len-1-len(details[3])) + "|\n")
		start_idx += 1

	#Re-write the file from line_list
	with open(out_file, 'w') as textobj:
		for line in line_list:
			textobj.write(line)


get_table_details(sys.argv[1], api_table_database, max_brief_len, max_param_len, max_prototype_len)

populate_table(sys.argv[2], api_table_database, start_line, end_line)
