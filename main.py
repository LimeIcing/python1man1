import urllib.request
import urllib.error
import subprocess
import os


def string_to_file(filename, content):
    file = open(filename, 'w')
    file.write(content)
    file.close()


def pull_files_with_readings(files_with_readings):
    file = open('README.md').read()
    if file.find('## Required reading') != -1:
        files_with_readings.append(file)
    os.chdir('..')


# Pulls JSON from API and saves it locally
try:
    json = urllib.request.urlopen(
        'https://api.github.com/orgs/python-elective-1-spring-2019/repos'
        '?per_page=100')
    json = json.read().decode('utf-8')
    string_to_file('json.txt', json)
except urllib.error.HTTPError as e:
    print(e)

jsonFile = open('json.txt')
json = jsonFile.read()
jsonFile.close()
cloneURLStartIndexes = []

# Finds appropriate Git URLs in JSON object
i = 1
while i != 0:
    i = json.find('clone_url', i)
    if i != -1:
        cloneURLStartIndexes.append(i + 12)
    i += 1

cloneURLEndIndexes = []
cloneURLs = []

# Makes a list of found URLs
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
repoNames = []

for url in cloneURLs:
    repoNames.append(url[49:-4])

    # Clones if repo is not found locally
    # Pulls if it is
    if repoNames[-1] not in os.listdir('.'):
        subprocess.run(['git', 'clone', url])
        os.chdir(repoNames[-1])
        pull_files_with_readings(readMes)
    else:
        os.chdir(repoNames[-1])
        subprocess.run(['git', 'pull'])
        pull_files_with_readings(readMes)

# Deletes local repos if not found in hub
for repo in os.listdir('.'):
    if repo not in repoNames:
        print('Removing ' + repo)
        subprocess.run(['rm', '-rf', repo])

requiredReadings = []

# Finds 'Required Reading' sections in ReadMes
for rm in readMes:
    requiredReadingIndex = rm.find('## Required reading')
    requiredReadings.append(
        rm[requiredReadingIndex:rm.find('##', requiredReadingIndex + 1)])

completeReadingsList = []

# Puts all links into a single list and checks for duplicates
for reading in requiredReadings:
    readings = reading.split('\n')
    for r in readings:
        if r not in completeReadingsList:
            completeReadingsList.append(r)

completeReadingsStr = ''

# Creates a neat list of links in a string
for reading in sorted(completeReadingsList):
    if reading != '' and reading[0] == '*':
        completeReadingsStr += reading[:3] + \
                               reading[3].upper() + reading[4:] + '\n '

os.chdir('..')
string_to_file('required_reading.md', completeReadingsStr)
