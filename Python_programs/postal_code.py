regex_integer_in_range = r"^[1-9][0-9][0-9][0-9][0-9][0-9]$"	# Do not delete 'r'.
regex_alternating_repetitive_digit_pair = r"(?=0.0)|(?=1.1)|(?=2.2)|(?=3.3)|(?=4.4)|(?=5.5)|(?=6.6)|(?=7.7)|(?=8.8)|(?=9.9)"	# Do not delete 'r'.


import re
P = input()

print (bool(re.match(regex_integer_in_range, P)) 
and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2)