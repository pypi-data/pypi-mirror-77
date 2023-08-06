import setuptools

setuptools.setup(
    name='SpecularLang',
    version='1.1.1',
    packages=setuptools.find_packages(),
    url='https://github.com/Bluepuff71/SpecularLang',
    license='MIT',
    author='Emery Porter',
    author_email='emeryporter99@gmail.com',
    description='Programming language that allows writers to create event-driven, complex character scenes within game engines using Specular.',
    install_requires=['antlr4-python3-runtime', 'antlr_denter'],
    entry_points={
        "console_scripts": [
            "slang = SpecularLang.compile:main",
        ]
    },
    python_requires='>=3.5'
)
