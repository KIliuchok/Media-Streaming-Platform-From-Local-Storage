#!/usr/bin/env python
import postgres
import os

MAIN_DIR = '/Users/kostia/Desktop/Website/public/videoassets/TV Shows'

def find_files_and_dirs():
    dirs = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(MAIN_DIR):
        files.extend(filenames)
        dirs.extend(dirnames)
        break
    return dirs, files

def find_files_in_dir(folder_name):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(MAIN_DIR + "/" + folder_name):
        files.extend(filenames)
        break
    return files

def check_if_entry_already(folder_name):
    cur = conn.cursor()
    sql = 'SELECT dir_name FROM show_names'
    list_of_shows = []

    cur.execute(sql)
    list_of_shows = cur.fetchall()

    print(list(list_of_shows))

    for item in list(list_of_shows):
        if folder_name in list(item):
            print("{0} is in DB already".format(folder_name))
            cur.close()
            return


    sql_insert = "INSERT INTO show_names(dir_name, name) VALUES ('" + folder_name + "', '" + folder_name + "')"
    cur.execute(sql_insert)
    conn.commit()
    cur.close()
    print("Added %s to DB", folder_name)


def parse_and_add_files(folder_name):
    cur = conn.cursor()
    sql = "SELECT * FROM videos WHERE show = '{0}'".format(folder_name)
    list_of_episodes = []

    cur.execute(sql)
    list_of_episodes = cur.fetchall()

    list_of_files_in_dir = find_files_in_dir(folder_name)
    print(list_of_files_in_dir)
    to_remove = []

    for file in list_of_files_in_dir:
        for item in list(list_of_episodes):
            if file in list(item):
                print("{0} episode is in DB already".format(file))
                to_remove.append(file)

    print("TO REMOVE ________________ ", to_remove)
    if len(to_remove) != 0:
        for item in to_remove:
            list_of_files_in_dir.remove(item)


    if len(list_of_files_in_dir) != 0:
        for file in list_of_files_in_dir:
            sql = "INSERT INTO videos(name, show) VALUES ('{0}', '{1}')".format(file, folder_name)
            cur.execute(sql)
            conn.commit()
            print("Added {0} to DB".format(file))

    cur.close()





if __name__ == '__main__':
    conn = postgres.connect()

    dirs, files = find_files_and_dirs()
    print(dirs, files)

    # Check if any folders are not in db
    for item in dirs:
        check_if_entry_already(item)
        parse_and_add_files(item)


    postgres.disconnect(conn)