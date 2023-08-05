[![PyPI version](https://badge.fury.io/py/honestybox-measurement.svg)](https://badge.fury.io/py/honestybox-measurement)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/honestybox-measurement.svg)](https://pypi.python.org/pypi/honestybox-measurement/)
[![GitHub license](https://img.shields.io/github/license/honesty-box/honestybox-measurement)](https://github.com/honesty-box/honestybox-measurement/blob/master/LICENSE)
[![GitHub Actions (Tests)](https://github.com/honesty-box/honestybox-measurement/workflows/Tests/badge.svg)](https://github.com/honesty-box/honestybox-measurement)
[![GitHub Actions (Quality)](https://github.com/honesty-box/honestybox-measurement/workflows/Quality/badge.svg)](https://github.com/honesty-box/honestybox-measurement)
[![Honesty Box Twitter](https://img.shields.io/twitter/follow/honestybox?style=social)](https://twitter.com/honestybox)

# honestybox-measurement

A framework for measuring things and producing structured results.

## Requirements

`honestybox-measurement` supports Python 3.5 to Python 3.8 inclusively.

## Development

### Git hooks

[pre-commit](https://pre-commit.com/) hooks are included to ensure code quality
on `commit` and `push`. Install these hooks like so:

```shell script
$ pre-commit install && pre-commit install -t pre-push
asd
```

## Releases

To ensure releases are always built on the latest codebase, *changes are only ever merged to `release` from `master`*.

### Creating a release
1. Ensure that master is up to date:

    ```shell script
    $ git checkout master
    $ git pull origin
    ```

2. Switch to release and ensure it is up to date:

    ```shell script
    $ git checkout release
    $ git pull origin
    ```

3. Merge from master:

    ```shell script
    $ git merge master
    ```

4. Add a new release to `CHANGELOG.md` and include all changes in `[Unreleased]`.

5. Update version number in `pyproject.toml`

6. Commit the changes to the `release` branch with comment `Release <version number>`

    ```shell script
    $ git add CHANGELOG.md pyproject.toml
    $ git commit -m 'Release v<x>.<y>.<z>`
    ```

7. Tag the commit with the release number:

    ```shell script
    $ git tag v<x>.<y>.<z>
    ```

8. Push the commit and tags upstream:

    ```shell script
    $ git push && git push --tags
    ```

9. Merge changes into master and push upstream:

    ```shell script
    $ git checkout master
    $ git merge release
    $ git push
    ```


### Publishing a release

1. Install [poetry](https://poetry.eustace.io)

2. Checkout the release:

    ```shell script
    $ git checkout v<x>.<y>.<z>
    ```

3. Publish the release:

    ```shell script
    $ poetry publish --build
    ```
