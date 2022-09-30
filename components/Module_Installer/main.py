import os


def InstallAllModules():
    os.system(f'pip install -r requirements.txt')
    os.system(f'python -m pip install --upgrade pip')
    print("\n\n\n\nPlease Restart this Software\n\n\n\nThanks for your Co-operation")
    exit()
