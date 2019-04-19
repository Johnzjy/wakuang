from setuptools import setup

setup(
    name="wakuang",
    version="0.1",
    author="johnzjy",
    description="python to stock data analysis by johnzjy",
    license="MIT",
    py_modules=["wk"],
    requires=["tushare","pandas","tqdm","matplotlib"],
    entry_points={
        'console_scripts': [
            'wk=wk:cli'
            
        ]}
    )