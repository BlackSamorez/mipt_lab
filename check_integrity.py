import os
import logging
import sys

def get_subdirectories(path, ignore_dotfiles=False):
    return [_ for _ in os.listdir(path) if os.path.isdir(os.path.join(path, _))
            and not (ignore_dotfiles and _.startswith('.'))]

def main():
    logging.getLogger().setLevel(logging.INFO)
    root_dir = os.path.dirname(os.path.realpath(__file__))
    for task_rel_dir in get_subdirectories(root_dir, ignore_dotfiles=True):
        if task_rel_dir == 'labs_guide':
            continue

        task_full_dir = os.path.join(root_dir, task_rel_dir)
        task_subdirectories = get_subdirectories(task_full_dir)
        if 'pdf' not in task_subdirectories:
            logging.error(f'pdf folder is not present in {task_rel_dir}')
            sys.exit(1)

        src_names = set(task_subdirectories)
        src_names.remove('pdf')

        for src_name in src_names:
            if ' ' in src_name:
                logging.error(f'"{os.path.join(task_rel_dir, src_name)}" should not contain spaces')
                sys.exit(1)
            if '_' not in src_name:
                logging.error(f'"{os.path.join(task_rel_dir, src_name)}" should contain "_" separator')
                sys.exit(1)

        pdf_filenames = {_ for _ in os.listdir(os.path.join(task_full_dir, 'pdf'))}
        for pdf_filename in pdf_filenames:
            if pdf_filename[-len('.pdf'):] != '.pdf':
                logging.error(f'{os.path.join(task_rel_dir, "pdf", pdf_filename)} is not a pdf')
                sys.exit(1)

        pdf_names = {_[:-len('.pdf')] for _ in pdf_filenames}
        if sorted(pdf_names) != sorted(src_names):
            logging.error(f'in task {task_rel_dir} pdf files and source directories do not match: ' \
                          f'{sorted(pdf_names)} != {sorted(src_names)}')
            sys.exit(1)

        trash_files = [_ for _ in os.listdir(task_full_dir) if os.path.isfile(os.path.join(task_full_dir, _))]

        assert len(trash_files) == 0, f'trash files in {task_rel_dir}: {trash_files}'

    logging.info('check_integrity.py found no issues.')


if __name__ == '__main__':
    main()
