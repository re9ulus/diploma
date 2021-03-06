from radon.cli_init import cc
from radon.metrics import  h_visit
from radon.tools import _open, iter_filenames, merge_files
from git_walker import git_walker

import shutil
import os

def merge_files_in_folders(folders = []):
    # VERY IMPORTANT - iter_filenames folders must be an ARRAY of string, not single string
    filenames = []
    for filename in iter_filenames(folders,[],[]):
        filenames.append(filename)
    return merge_files(filenames)

# Ciclomatic Complexity
def get_ciclomatic_for_folder(path):
    print("Ciclomatic")
    harvester = cc(path)
    harvester.run()
    data = harvester._to_dicts()
    ranks = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
    for file in data:
        for func in data[file]:
            if 'name' in func:
                if 'rank' in func:
                    ranks[func['rank']] += 1
    return ranks

def get_cc_for_repo(repo_path = 'G:/dev/django', res_filename = 'G:/cc_django.csv', proj_name = 'django'):
    gw = git_walker(repo_path)
    path = gw.create_path(20)
    open(res_filename, 'w+').close()
    with open(res_filename, 'a+') as f:
        f.write("date\tA\tB\tC\tD\tE\tF\tproj_name\n")
    for hash in reversed(path):
        date = gw.get_commit_date(hash)
        gw.reset_to_commit(hash)
        print(date)
        ranks = get_ciclomatic_for_folder([repo_path])
        res = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
            date, ranks['A'], ranks['B'], ranks['C'], ranks['D'], ranks['E'], ranks['F'], proj_name)
        print(res)
        with open(res_filename, 'a+') as f:
            f.write(res)
    gw.pull()

# Halstead metrics
def get_halstead_for_file(filepath):
    print("Halstead metric")
    with _open(filepath) as fobj:
        halstead = h_visit(fobj.read())
        return halstead

def remove_folders(exclude_folders):
    for folder in exclude_folders:
        try:
            print("remove: ", folder)
            if (os.path.isdir(folder)):
                shutil.rmtree(folder)
            else:
                os.remove(folder)
        except:
            print("error: can't remove ", folder)

def get_halstead_for_repo_to_file(repo_path = 'G:/dev/django', res_filename = 'G:/django_halstead.csv',
                          proj_name = 'django', exclude = []):
    gw = git_walker(repo_path)
    path = gw.create_path(20)
    open(res_filename, 'w+').close()
    with open(res_filename, 'a+') as f:
        f.write("date\tlength\tvolume\tdifficulty\teffort\ttime\tbugs\tproj_name\n")
    for hash in reversed(path):
        date = gw.get_commit_date(hash)
        print(date)
        gw.reset_to_commit(hash)
        # Remove folder with docs
        remove_folders(exclude)
        (file_dir, file_name) = merge_files_in_folders(folders = [repo_path])
        holst = get_halstead_for_file(file_dir + '\\' + file_name)
        print(date, holst)
        res = "{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.2f}\t{7}\n".format(
            date, holst.length, holst.volume, holst.difficulty, holst.effort, holst.time, holst.bugs, proj_name)
        with open(res_filename, 'a+') as f:
            f.write(res)
    gw.pull()

def get_static_data_for_repo(repo_path = 'G:/dev/twisted', proj_name = 'twisted', exclude = []):
    # TODO: Test
    gw = git_walker(repo_path)
    number_of_steps = 20
    step = 0
    path = gw.create_path(number_of_steps)
    res = {'date': [], 'length': [], 'volume': [], 'difficulty': [], 'effort': [], 'time': [], 'bugs': [], 'x_error': [],
           'ciclomatic': {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': []},
           'proj_name': proj_name}
    for hash in reversed(path):
        date = gw.get_commit_date(hash)
        print(date)
        gw.reset_to_commit(hash)
        remove_folders(exclude)
        (file_dir, file_name) = merge_files_in_folders(folders = [repo_path])
        holst = get_halstead_for_file(file_dir + '\\' + file_name)
        print(date, holst)
        res['date'].append(date)
        res['length'].append(int(holst.length))
        res['volume'].append(int(holst.volume))
        res['difficulty'].append(int(holst.difficulty))
        res['effort'].append(int(holst.effort))
        res['time'].append(int(holst.time))
        res['bugs'].append(int(holst.bugs + 0.5))
        res['x_error'].append(number_of_steps - step)
        step += 1
        ciclomatic_ranks = get_ciclomatic_for_folder([repo_path])
        for key in ciclomatic_ranks:
            res['ciclomatic'][key].append(ciclomatic_ranks[key])
    gw.pull()
    return res

if __name__ == '__main__':
    print('Start')

    # get_cc_for_repo('G:/dev/bottle', 'G:/bottle_cc.csv', 'bottle')
    # get_halstead_for_repo_to_file('G:/dev/bottle', 'G:/bottle_halstead.csv', 'bottle',
    #                               ['G:/dev/bottle/test/test_importhook.py', 'G:/dev/bottle/test/test_wsgi.py'])

    print('End')