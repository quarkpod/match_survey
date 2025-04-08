from setuptools import setup, find_packages

project = "match_survey"
description = "Prepare and process polling responses on a soccer team."
with open("config/requirements.txt") as requirement_file:
    requirements = requirement_file.read().split()

setup(
    name=project,
    description=description,
    version="0.0.0",
    author="",
    author_email="",
    install_requires=requirements,
    packages=[project],
    package_dir={
        project: f'src/{project}'},
    },
    scripts=['bin/gather']
)
