import click


@click.command()
@click.argument('rule_id')
@click.argument('xpi_url')
@click.option('--server', default='https://aus4-admin.mozilla.org')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def main(rule_id, xpi_url, server, username, password):
    pass


if __name__ == '__main__':
    main()
