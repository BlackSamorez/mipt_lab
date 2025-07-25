#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///


import os
import sys


def get_subdirectories(path, ignore_dotfiles=False):
    output = [filename for filename in os.listdir(path) if os.path.isdir(os.path.join(path, filename))]

    if ignore_dotfiles:
        output = [filename for filename in output if not filename.startswith('.')]

    return output


def exit(reason):
    print(f'Failed integrity check: {reason}')
    sys.exit(1)


def main():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    for task in get_subdirectories(root_dir, ignore_dotfiles=True):
        if task == 'labs_guide':
            continue

        task_content = get_subdirectories(os.path.join(root_dir, task))
        if 'pdf' not in task_content:
            exit(f'pdf folder is not present in {task}')

        authors = set(task_content)
        authors.remove('pdf')

        for author in authors:
            if ' ' in author:
                exit(f'"{os.path.join(task, author)}" should not contain spaces')
            if '_' not in author:
                exit(f'"{os.path.join(task, author)}" should contain "_" separator')
            if author.count('_') != 1:
                exit(f'"{os.path.join(task, author)}" should contain only one "_" separator')

        for filename in os.listdir(os.path.join(root_dir, task, 'pdf')):
            if not filename.endswith('.pdf'):
                exit(f'{os.path.join(task, "pdf", filename)} is not a pdf')

        pdf_authors = {filename[:-len('.pdf')] for filename in os.listdir(os.path.join(root_dir, task, 'pdf'))}

        for author in authors:
            if author in pdf_authors:
                continue
            exit(f'{os.path.join(task, author)} exists, ' +
                 f'while {os.path.join(task, "pdf", author + ".pdf")} does not exist')

        for author in pdf_authors:
            if author in authors:
                continue
            exit(f'{os.path.join(task, "pdf", author + ".pdf")} exists, ' +
                 f'while {os.path.join(task, author)} does not exist')

        trash_files = [
            filename for filename in os.listdir(os.path.join(root_dir, task))
            if os.path.isfile(os.path.join(root_dir, task, filename))
        ]
        if len(trash_files) != 0:
            exit(f'trash files in {task}: {trash_files}')

    print('check_integrity.py found no issues.')


if __name__ == '__main__':
    main()
