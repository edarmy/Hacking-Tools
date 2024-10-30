# Find onion link using key words
#!/bin/python
# @Time    : 30/10/2024
# @Author  : DEADARMY
# Version: 1.0

import requests
import random
import re # regular expression

def scrap (newkeyword):
    yourquaries=newkeyword

    if "" in yourquaries:
        yourquaries=yourquaries.replace(" ","+")
    url="https://ahmia.fi/search/?q={}".format(yourquaries)
    request=requests.get(url)
    content=request.text
    regexquries="\w+\.onion"
    minedata=re.findall(regexquries, content)

    n= random.randint(1,9999)

    filename="sites{}.txt".format(str(n))
    print("Saving to file...", filename)
    minedata=list(dict.fromkeys(minedata))

    for k in minedata:
        with open(filename, "a") as file:
            k=k+"\n"
            file.write(k)
    print("All the file written to the text file : ", filename)

    with open (filename) as input_file:
        head=[next(input_file)for x in range(5)]
        contents='\n'.join(map(str,head))


nedata=input('[+] Please input your Quarie: ')
scrap(nedata)