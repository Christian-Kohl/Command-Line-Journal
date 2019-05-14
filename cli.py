# https://www.makeuseof.com/tag/python-command-line-programs-click/
import click
import random


@click.command()
@click.option('--total', default=3, help='Number of vegetables to output.')
@click.option('--gravy', default=False, help='Do they have gravy?')
def veg(total, gravy):
    """ Basic method will return a random vegetable"""
    for number in range(total):
        if gravy:
            print(random.choice(['Carrot', 'Potato', 'Turnip', 'Parsnip']),
                  'with Gravy!')
        else:
            print(random.choice(['Carrot', 'Potato', 'Turnip', 'Parsnip']))


if __name__ == '__main__':
    veg()
