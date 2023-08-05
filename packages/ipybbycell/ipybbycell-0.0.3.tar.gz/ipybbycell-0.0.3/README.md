# ipy bby cell

BBY cell template extension for Jupyter Notebook

## Installation

You can install using `pip`:

```bash
pip install ipybbycell
jupyter nbextension install --sys-prefix --py ipybbycell
jupyter nbextension enable --sys-prefix --py ipybbycell
```

## Development

```bash
docker run --rm -it -p 8888:8888 -v $(pwd):/home/jovyan jupyter/minimal-notebook bash
```

```bash
pip install -e ".[test, examples]"
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipybbycell
jupyter nbextension enable --sys-prefix --py ipybbycell
jupyter notebook
```

[http://localhost:8888](http://localhost:8888)

## Publish

```bash
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/ipybbycell-*
```
