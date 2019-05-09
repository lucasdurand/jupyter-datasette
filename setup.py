from glob import glob
import setuptools

setuptools.setup(
    name="jupyter-datasette",
    version='0.1.0',
    url="https://github.com/lucasdurand/jupyter-datasette",
    author="Lucas Durand",
    description="Simple Jupyter extension to integrate a Datasette instance with your Notebook environment",
    packages=setuptools.find_packages(),
    install_requires=[
        'datasette',
        'notebook',
    ],
    data_files=[
        ('share/jupyter/nbextensions/jupyter-datasette', glob('jupyter-datasette/static/*')),
        ('etc/jupyter/jupyter_notebook_config.d', ['jupyter-datasette/etc/serverextension.json']),
        ('etc/jupyter/nbconfig/notebook.d', ['jupyter-datasette/etc/nbextension.json'])
    ],
    zip_safe=False,
    include_package_data=True
)
