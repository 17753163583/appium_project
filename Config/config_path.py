import os


def get_project_path():
    project_path = os.path.dirname(os.path.dirname(__file__))
    return project_path


def get_output_path():
    output_path = os.path.join(get_project_path(), 'OutPut')
    return output_path


def get_log_path():
    log_path = os.path.join(get_output_path(), 'log_files')
    return log_path


if __name__ == '__main__':
    print(get_project_path())
    print(get_log_path())
