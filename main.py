import urllib.request
import urllib.error
import subprocess
import os

try:
    json = urllib.request.urlopen(
        'https://api.github.com/orgs/python-elective-1-spring-2019/repos'
        '?per_page=100')
    json = json.read().decode('utf-8')
    file = open('json.txt', 'w')
    file.write(json)
    file.close()
except urllib.error.HTTPError as e:
    print(e)

file = open('json.txt')
cloneURLStartIndexes = []
json = file.read()

i = 1
while i != 0:
    i = json.find('clone_url', i)
    if i != -1:
        cloneURLStartIndexes.append(i + 12)
    i += 1

cloneURLEndIndexes = []
cloneURLs = []

for j in range(len(cloneURLStartIndexes)):
    cloneURLEndIndex = json.find('"', cloneURLStartIndexes[j])
    cloneURLs.append(json[cloneURLStartIndexes[j]:cloneURLEndIndex])
    j += 1

try:
    os.mkdir('repos')
except FileExistsError as e:
    print(e)

os.chdir('repos')
readMes = []

for url in cloneURLs:
    repoName = url[49:-4]

    if repoName not in os.listdir('.'):
        subprocess.run(['git', 'clone', url])
        os.chdir(repoName)
        readMe = open('README.md').read()
        if readMe.find('## Required reading') != -1:
            readMes.append(readMe)
        os.chdir('..')
    else:
        os.chdir(repoName)
        subprocess.run(['git', 'pull'])
        readMe = open('README.md').read()
        if readMe.find('## Required reading') != -1:
            readMes.append(readMe)
        os.chdir('..')

requiredReadings = []

for rm in readMes:
    requiredReadingIndex = rm.find('## Required reading')
    requiredReadings.append(
        rm[requiredReadingIndex:rm.find('##', requiredReadingIndex + 1)])

completeReadings = ""

for reading in requiredReadings:
    completeReadings += reading[20:]

print(completeReadings)

os.chdir('..')
file = open('required_reading.md', 'w')
file.write(completeReadings)
