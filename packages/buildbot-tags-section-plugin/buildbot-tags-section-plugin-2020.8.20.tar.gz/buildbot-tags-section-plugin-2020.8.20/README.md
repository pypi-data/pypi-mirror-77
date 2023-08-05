# Buildbot tags section plugin

The plugin adds a section to the side menu with pre-prepared builders filters by tags.

## Usage

1. Install python package `buildbot-tags-section-plugin`
directory
2. Configure plugin in the `master/master.py` file:
    ```python
        c['www'] = dict(
            ...
            plugins=dict(
                ...
                tags_section_plugin={
                    "sections": [
                        {
                            "name": "MDBE",
                            "filters": [
                                {"name": "Only build", "tags": ["+build", "-test"]},
                                {"name": "Only test", "tags": ["-build", "+test"]}
                            ],
                        },
                        {
                            "name": "MaxScale",
                            "filters": [
                                {"name": "Only build", "tags": ["+build", "-test"]},
                                {"name": "Only test", "tags": ["-build", "+test"]}
                            ],
                        }
                    ],
                }
            )
        )
    ```
3. Reconfigure BuildBot

## Build and distribution

Get more information at https://packaging.python.org/tutorials/packaging-projects/

1. 
    ```
    python3 -m pip install --user --upgrade setuptools wheel
    ```
2.
    ```
    python3 setup.py sdist bdist_wheel
    ```
3.
    ```
    python3 -m pip install --user --upgrade twine
    ```
4.
    ```
    python3 -m twine upload --repository pypi dist/*
    ```