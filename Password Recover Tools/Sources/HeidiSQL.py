import re, sys

filename = sys.argv[1]

def decrypt(s):
    return ''.join(chr(int(s[i:i + 2], 16) - int(s[-1])) for i in range(0, len(s), 2))[:-1]
    
text = open(filename, mode = 'r', encoding = 'utf-8').read()

passes = re.findall(r'Servers\\.+\\Password<\|\|\|>1<\|\|\|>([\dA-F]+)', text)
passes = list(map(decrypt, passes))
users  = re.findall(r'Servers\\.+\\User<\|\|\|>1<\|\|\|>(\w+)', text)
hosts  = re.findall(r'Servers\\.+\\Host<\|\|\|>1<\|\|\|>([\w.-]+)', text)
ports  = re.findall(r'Servers\\.+\\Port<\|\|\|>1<\|\|\|>(\d+)', text)

maxHost = str(max(map(len,  hosts)))
maxPass = str(max(map(len, passes)))
maxUser = str(max(map(len,  users)))
maxPort = str(max(map(len,  ports)))

print(((' {:<'+maxHost+'} {:<'+maxUser+'} {:<'+maxPass+'} {:<'+maxPort+'}').format('Host', 'User', 'Password', 'Port')))
print(' ' + '=' * 78)

for host, user, passw, port in zip(hosts, users, passes, ports):
    print(((' {:<'+maxHost+'} {:<'+maxUser+'} {:<'+maxPass+'} {:<'+maxPort+'}').format(host, user, passw, port)))
