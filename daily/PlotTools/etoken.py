
import re

import re
regex = re.compile('E|\d+|\.|\,|\n|\-')
def token(string): 
	return regex.findall(string)

