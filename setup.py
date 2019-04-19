from setuptools import setup

setup(
    name="wakuang",  #the project name   
    version="0.1",  #version
    author="johnzjy",
    description="python to stock data analysis by johnzjy",
    license="MIT",
    py_modules=["wk"],
    requires=["tushare", "pandas", "tqdm", "matplotlib"],
    entry_points={
        'console_scripts': [
            'wk=wk:cli',  #the will register the command in to the systerm
        ]
    })
