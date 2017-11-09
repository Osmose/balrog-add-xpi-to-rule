import difflib
import hashlib
import json
from urllib.parse import urljoin

import click
import requests


@click.command(help='Add XPI_RELEASE to the Balrog rules specified by RULE_IDS')
@click.argument('xpi_release')
@click.argument('rule_ids', nargs=-1)
@click.option('--server', default='https://aus4-admin.mozilla.org', help='Balrog url')
@click.option('--product', default='SystemAddons', help='product for newly-created releases')
@click.option('--username', prompt=True, help='ldap username (name@mozilla.com)')
@click.option('--password', prompt=True, hide_input=True, help='ldap password')
def main(xpi_release, rule_ids, server, product, username, password):
    session = requests.Session()
    session.auth = (username, password)
    session.headers = {'Accept': 'application/json'}

    for rule_id in rule_ids:
        # Fetch existing rule
        rule = session.get(urljoin(server, f'/api/rules/{rule_id}')).json()

        # Fetch release for rule
        superblob = session.get(urljoin(server, f'/api/releases/{rule["mapping"]}')).json()

        # Construct new superblob with release
        if xpi_release not in superblob['blobs']:
            superblob['blobs'].append(xpi_release)
        name_hash = hashlib.sha256('-'.join(superblob['blobs']).encode()).hexdigest()
        superblob['name'] = f'Superblob-{name_hash}'

        # Check if the superblob already exists
        response = session.get(urljoin(server, f'/api/releases/{superblob["name"]}'))
        if response.status_code == 404:
            create_release = True
        else:
            response.raise_for_status()
            create_release = False

        # Check if the mapping is already set
        update_mapping = rule['mapping'] != superblob['name']

        # Confirm changes
        if create_release:
            click.echo(f'Will add new release {superblob["name"]}:\n')
            click.echo(json.dumps(superblob, indent=2) + '\n')
        if update_mapping:
            click.echo(
                f'Will modify rule {rule_id} (channel: {rule["channel"]}, version: '
                f'{rule["version"]}) from mapping:\n{rule["mapping"]}\nto '
                f'mapping\n{superblob["name"]}\n'
            )
        if update_mapping or create_release:
            if not click.confirm('Apply these changes?'):
                click.echo('Aborted!')
                return
        else:
            click.echo(f'Skipping rule {rule_id}, nothing to change.')
            continue

        csrf_token = session.get(urljoin(server, '/api/csrf_token')).headers['x-csrf-token']

        # Create release
        if create_release:
            response = session.post(urljoin(server, '/api/releases'), json={
                'blob': json.dumps(superblob),
                'name': superblob['name'],
                'product': product,
                'csrf_token': csrf_token,
            })
            try:
                response.raise_for_status()
            except:
                click.echo(response.text)
                raise

        # Save new mapping to rule
        if update_mapping:
            rule['mapping'] = superblob['name']
            response = session.put(urljoin(server, f'/api/scheduled_changes/rules'), json={
                **rule,
                'when': 60000,  # in one minute
                'csrf_token': csrf_token,
            })
            try:
                response.raise_for_status()
            except:
                click.echo(response.text)
                raise

    click.echo('Done!')


if __name__ == '__main__':
    main()
