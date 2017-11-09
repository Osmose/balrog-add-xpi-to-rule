# balrog-add-xpi-to-rule

This package contains a script for writing to the [Balrog][] API. It automates
adding a new system add-on to a set of Balrog rules that are using superblob
rules.

Here's the setup: You're maintaining Balrog rules for system add-ons. You have
a new system add-on that needs to go out to several versions of Firefox that
have existing rules. The following is assumed to be true:

- Every rule is already mapped to a superblob, which is a Release that refers
  to other Releases.
- All of the rules are in a single product.

What this script does is go through each rule, copy the existing superblob, add
the new Release to the superblob, create a new Release, and map the rule to the
new Release. In other words, this lets you update the existing set of rules with
the new system add-on while preserving the existing add-ons in the rule.

## Installation

This isn't up on PyPI, so your best bet is to check out the repo and install it
as an editable package:

```sh
$ git clone https://github.com/Osmose/balrog-add-xpi-to-rule.git
$ cd balrog-add-xpi-to-rule
$ pip install -e .
```

It's been manually tested on Python 3.6 and probably won't work on earlier
versions.

## Usage

```
Usage: balrog-add-xpi-to-rule [OPTIONS] XPI_RELEASE [RULE_IDS]...

  Add XPI_RELEASE to the Balrog rules specified by RULE_IDS

Options:
  --server TEXT    Balrog url
  --product TEXT   product for newly-created releases
  --username TEXT  ldap username (name@mozilla.com)
  --password TEXT  ldap password
  --help           Show this message and exit.
```

The `--username` and `--password` fields will prompt you if you do not provide
them. The server defaults to the Balrog admin server, and the product defaults
to `SystemAddons`.

If you wanted to add the `my-new-addon-1.0` release to rules `567` and `890`:

```sh
$ balrog-add-xpi-to-rule --username=username@mozilla.com my-new-addon-1.0 567 890
```

## License

Licensed under the MIT License. See `LICENSE` for details.
