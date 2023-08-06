# Minify File Contents Resolver

Reads in the contents of a file and minifies them if applicable.

Syntax:

```yaml
parameters|sceptre_user_data:
  <name>: !minify_file_contents /path/to/file.txt
```

Example:

```yaml
sceptre_user_data:
  inline_lambda_code: !minify_file_contents /path/to/policy.js
```

Add your resolver readme here. Remember to include the following:

- Tell people how to install it (e.g. pip install ...).
- Be clear about the purpose of the resolver, its capabilities and limitations.
- Tell people how to use it.
- Give examples of the resolver in use.

Read our wiki to learn how to use this repo:
https://github.com/Sceptre/project/wiki/Sceptre-Resolver-Template

If you have any questions or encounter an issue
[please open an issue](https://github.com/Sceptre/project/issues/new)

# Testing

We have included a basic testing set up for you. You will need to unit test your code so remember to update `tests/...`.

# Releasing

1. Update the CHANGELOG.md with what has changed (see the example in the CHANGELOG comments).
2. In your virtualenv run `bumpversion --dry-run --verbose patch|minor|major`. You will see that the version number will be updated, a commit is made for the version update and a new git tag will be created.
3. If you are happy with the dry run then execute `bumpversion patch|minor|major`.
4. Push the commit with `git push`.
5. When the build for the above step is complete push the tag `git push origin vX.Y.Z` this will trigger a release build which will deploy to PyPi.
