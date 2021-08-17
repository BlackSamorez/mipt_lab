import os


def get_subdirectories(path, ignore_dotfiles=False):
    return [_ for _ in os.listdir(path) if os.path.isdir(os.path.join(path, _))
            and not (ignore_dotfiles and _.startswith('.'))]


def main():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    for task_rel_dir in get_subdirectories(root_dir, ignore_dotfiles=True):
        task_full_dir = os.path.join(root_dir, task_rel_dir)
        task_subdirectories = get_subdirectories(task_full_dir)
        assert 'pdf' in task_subdirectories, f'pdf folder is not present in {task_rel_dir}'

        src_names = set(task_subdirectories)
        src_names.remove('pdf')

        pdf_filenames = {_ for _ in os.listdir(os.path.join(task_full_dir, 'pdf'))}
        for pdf_filename in pdf_filenames:
            assert pdf_filename[-len('.pdf'):] == '.pdf',\
                f'{os.path.join(task_rel_dir, "pdf", pdf_filename)} is not a pdf'

        pdf_names = {_[:-len('.pdf')] for _ in pdf_filenames}
        if sorted(pdf_names) != sorted(src_names):
            assert False, f'in task {task_rel_dir} pdf files and source directories do not match: ' \
                          f'{sorted(pdf_names)} != {sorted(src_names)}'

        trash_files = [_ for _ in os.listdir(task_full_dir) if os.path.isfile(os.path.join(task_full_dir, _))]

        assert len(trash_files) == 0, f'trash files in {task_rel_dir}: {trash_files}'


if __name__ == '__main__':
    main()
