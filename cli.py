import click


@click.command()
@click.option('--encrypt', default=False,
              help='Encrypt the text? Currently no effect')
@click.argument('text', required=False, nargs=-1)
def dry(text, encrypt):
    if text == ():
        new_input(encrypt)
    elif len(text) == 1:
        text = click.prompt('Please input a proper value')
        dry_rec(text, encrypt)
    else:
        has_input(text)


def dry_rec(text, encrypt):
    if text is None:
        new_input(encrypt)
    elif len(text) == 1:
        text = click.prompt('Please input a proper value')
        dry_rec(text, encrypt)
    else:
        has_input(text)


def new_input(encrypt):
    text = click.prompt('Welcome to dry! Please input your diary entry')
    dry_rec(text, encrypt)


def has_input(text):
    if isinstance(text, tuple):
        text = " ".join(text)
    click.echo(text)


if __name__ == '__main__':
    dry()
