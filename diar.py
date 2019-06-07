import click
import numpy as np
from pathlib import Path
import os


def input_diar(abs_root):
    return np.load(abs_root + 'diarpy/file.npy')

@click.command()
@click.argument('text', required=True, nargs=-1)
def diar(text):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/diarpy.npy'
    print(os.listdir())
    exist = os.path.exists(file_path)
    if exist:
        dary = np.load('diarpy.npy')
    else:
        click.echo('Your diary will be stored in:' + file_path)
        np.save(file_path, np.zeros((10, 10)))

if __name__ == '__main__':
    diar()
