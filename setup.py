from glob import glob
import setuptools

setuptools.setup(
    name="jupyter_datasette",
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
        ('share/jupyter/nbextensions/jupyter_datasette', glob('jupyter_datasette/static/*')),
        ('etc/jupyter/jupyter_notebook_config.d', ['jupyter_datasette/etc/serverextension.json']),
        ('etc/jupyter/nbconfig/notebook.d', ['jupyter_datasette/etc/nbextension.json'])
    ],
    zip_safe=False,
    include_package_data=True
)
