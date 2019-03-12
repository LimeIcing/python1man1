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


def main():
    # Pulls JSON from API and saves it locally
    try:
        json = urllib.request.urlopen(
            'https://api.github.com/orgs/python-elective-1-spring-2019/repos'
            '?per_page=100')
        json = json.read().decode('utf-8')
        string_to_file('json.txt', json)
    except urllib.error.HTTPError as e:
        print(e)

    json_file = open('json.txt')
    json = json_file.read()
    json_file.close()
    clone_url_start_indexes = []

    # Finds appropriate Git URLs in JSON object
    i = 1
    while i != 0:
        i = json.find('clone_url', i)
        if i != -1:
            clone_url_start_indexes.append(i + 12)
        i += 1

    clone_urls = []

    # Makes a list of found URLs
    for j in range(len(clone_url_start_indexes)):
        clone_url_end_index = json.find('"', clone_url_start_indexes[j])
        clone_urls.append(json[clone_url_start_indexes[j]:clone_url_end_index])
        j += 1

    try:
        os.mkdir('repos')
    except FileExistsError as e:
        print(e)

    os.chdir('repos')
    read_mes = []
    repo_names = []

    for url in clone_urls:
        repo_names.append(url[49:-4])

        # Clones if repo is not found locally
        # Pulls if it is
        if repo_names[-1] not in os.listdir('.'):
            subprocess.run(['git', 'clone', url])
            os.chdir(repo_names[-1])
            pull_files_with_readings(read_mes)
        else:
            os.chdir(repo_names[-1])
            subprocess.run(['git', 'pull'])
            pull_files_with_readings(read_mes)

    # Deletes local repos if not found in hub
    for repo in os.listdir('.'):
        if repo not in repo_names:
            print('Removing ' + repo)
            subprocess.run(['rm', '-rf', repo])

    required_readings = []

    # Finds 'Required Reading' sections in ReadMes
    for rm in read_mes:
        required_reading_index = rm.find('## Required reading')
        required_readings.append(rm[required_reading_index:rm.find(
            '##', required_reading_index + 1)])

    complete_readings_list = []

    # Puts all links into a single list and checks for duplicates
    for reading in required_readings:
        readings = reading.split('\n')
        for r in readings:
            if r not in complete_readings_list:
                complete_readings_list.append(r)

    complete_readings_str = ''

    # Creates a neat list of links in a string
    for reading in sorted(complete_readings_list):
        if reading != '' and reading[0] == '*':
            first_letter_index = -1
            i = 0

            while first_letter_index == -1:
                if reading[i].isalpha():
                    first_letter_index = i
                i += 1

            complete_readings_str += reading[:first_letter_index] + \
                                     reading[first_letter_index].upper() + \
                                     reading[first_letter_index + 1:] + '\n '
        else:
            print(reading)

    os.chdir('..')
    string_to_file('required_reading.md', complete_readings_str)


if __name__ == '__main__':
    main()
