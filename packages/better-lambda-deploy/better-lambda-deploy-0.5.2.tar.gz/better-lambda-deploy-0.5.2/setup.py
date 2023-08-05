import setuptools

setuptools.setup(
    name="better-lambda-deploy",
    version="0.5.2",
    author="Alex Wiss",
    author_email="alexwisswolf@gmail.com",
    description="A better AWS Lambda deployment framework.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "click >= 7",
        "jinja2 >= 2.10",
        "aws-sam-cli == 0.41",
        "aws-sam-translator == 1.20.1",
        "boto3 >= 1.11",
        "pyrsistent == 0.15.0",
        "future >= 0.18",
        "markupsafe >= 1.1",
        "pyyaml == 5.3",
        "simplejson ~= 3.17",
        "jmespath ~= 0.9.4",
        "python-dateutil < 2.8.1, ~= 2.6",
        "bottle ~= 0.12.0",
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bld=bld.cli.cli:entry_point
    """,
)
