import subprocess
import os

#os.chdir("C:\Everything Else\Blackhat\www\server\cfgtojson\src\cfgtojson")
#output = subprocess.check_output(["java", "-jar", "cfgtojson-0.1.1-SNAPSHOT-standalone.jar", '''"<B> ::= 'a'<B>'b' | eps ;"'''])
output = subprocess.check_output(["lein", "run"], shell=True)
print(output)
query = raw_input("To exit, enter any character.")