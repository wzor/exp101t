# -*- coding: utf-8 -*-
# Wise Hide Folder Cracker alpha version

import os

configFile = '%s:\....\\....\hidefolder\hide\_config.ini'
hiddenFlash = '%s:\...\\....\hidefolder\hide\_config.ini'
configFileDir = '%s:\....\\....\hidefolder\hide\\'
hiddenFlashDir = '%s:\...\\....\hidefolder\hide\\'

def getFileList(disk):
    return open(configFile % disk, 'r').readlines()

def printFiles(disk):
    try:
        f = open(hiddenFlash % disk); f.close()
        print('%s is hidden USB Drive!' % disk)
    except:
        try:
            files = getFileList(disk)
            for i in range(0, len(files), 5):
                print('[%s] %s found: %s with %spassword' % ( 
                files[i + 2][11:-1], 
                'Directory' if files[i + 4][-2] == '1' else 'File', 
                files[i + 1][5:-1] + files[i][1:-2], 
                'no ' if len(files[i + 3]) == 10 else ''))
        except: print('Hidden files not found!')

def resetPass(disk, file):
    if file == '*':
        for i in list(map(lambda x: x[1:-2], getFileList(disk)[::5])):
            resetPass(disk, i)
    elif file == '':
        try:
            files  = open(hiddenFlash % disk, 'r').readlines()
            config = open(hiddenFlash % disk, 'w'); files[1] = 'Password=\n'
            config.write(''.join(files))
        except: print('%s is not hidden USB Drive!' % disk)
    else:
        try:
            files  = getFileList(disk)
            if file[0] in ['\'', '"']: file = file[1:-1]
            files[files.index('[%s]\n' % file) + 3] = 'Password=\n'
            config = open(configFile % disk, 'w')
            config.write(''.join(files))
        except: print('File not found!')

def findHiddenDrives():
    for disk in range(ord('A'), ord('Z') + 1):
        try:
            f = open(hiddenFlash % chr(disk)); t = len(f.readlines()[1])
            print('Hidden USB Drive found: %s with %spassword' % (chr(disk), 'no ' if t == 10 else ''))
            f.close()
        except: pass

def recoverFiles(disk, file):
    try:
        try: 
            files = os.listdir(hiddenFlashDir % disk)
            toDir = [disk + ':\\'] * len(files)
            for file, dir in zip(files, toDir):
                os.system('move %s %s' %((hiddenFlashDir % disk) + file, dir))
        except:
            try: 
                files = list(map(lambda x: x[1: -2], open(configFile % disk).readlines()[0::5]))
                toDir = list(map(lambda x: x[5: -1], open(configFile % disk).readlines()[1::5]))
                for file, dir in zip(files, toDir):
                    os.system('move %s %s' %((configFileDir % disk) + file, dir))
            except: print('No hidden files found!')
    except: pass

while True:
    try:
        command = input('  > '); command.strip(); command.replace('  ', ' ')
        command = command.split()
        if command[0] == 'exit':
            exit()
        elif command[0] ==  'list':
            printFiles(command[1])
        elif command[0] == 'reset':
            resetPass(command[1], ' '.join(command[2:]))
        elif command[0] == 'drives':
            findHiddenDrives()
        else: print('Unknown command!')
    except KeyboardInterrupt: exit()
