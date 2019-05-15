import click


@click.command()
@click.option('--encrypt', default=False,
              help='Encrypt the text? Currently no effect')
@click.argument('date', required=False, nargs=2)
@click.argument('text', required=False, nargs=-1)
def dry(text, encrypt):
    text = " ".join(text)
    check = False
    click.echo('cccc')
    if text == '':
        text = click.prompt('New entry for date: ', date)
        text, check = check(text)
    while not check:
        check = True


def check_valid(text):
    if ':' in text:
        return True



if __name__ == '__main__':
    dry()
