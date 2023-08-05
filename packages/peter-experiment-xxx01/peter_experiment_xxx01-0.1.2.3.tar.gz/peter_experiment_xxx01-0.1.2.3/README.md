# Welcome to repository-template

![CI](https://github.com/KENDAXA-Development/repository-template/workflows/CI/badge.svg)


This is a template repository for Kendaxa Open Source projects. It provides the following features:
- MIT license file, the default license for Kendaxa Open Source projects.
- CONTRIBUTING.md file description how the community can contribute to the project.
- README.md file with information about the project.
- Templates for bug reports and feature requests on Github issues.
- Minimal configuration for Actions, the Github CI.
- Python example integrated with Actions with code style and type checking, and automated tests with code coverage.

The files present in the repository are listed below:

```text
├── .github
│   ├── ISSUE_TEMPLATE
│   │   ├── bug_report.md       # Template for bug report issues.
│   │   └── feature_request.md  # Template for feature request issues.
│   └── workflows
│       └── main.yml           # Definition for Github Continuous Integration.
├── .gitignore                  # Files to shouldn't be tracked by git.
├── LICENSE.txt                 # LICENSE file (MIT).
├── README.md                   # You are here!
│
│   # Files below are related to the python example.
│
├── example
│   ├── example.py              # simple module implementation.
│   └── __init__.py
├── tests
│   ├── __init__.py
│   └── test_example.py         # test file for the example module.
├── MANIFEST.in                 # extra files that you want to include in python the package.
├── mypy.ini                    # configuration for mypy (type checking/enforcing).
├── requirements.test.txt       # dependencies required for testing.
├── requirements.txt            # dependencies required to run the package.
├── setup.py                    # configuration for package generation
└── tox.ini                     # configuration for tox and flake8
```

Before starting your Open Source project make sure you read the Kendaxa Open Source Contribution [Guidelines](https://confluence.kendaya.net/display/KXLEIT/Open+Source+Contribution+Guidelines) and [Policy](https://confluence.kendaya.net/display/KXLEIT/Open+Source+Contribution+Policy). The example in python implements code style and typing verification using flake8 and mypy, and unit tests with unittests builtin package. If you are developing in another language look for the corresponding tools.


## Getting started

After creating your repository from this template you can start by filling in this `README.md`. The first section should be a description of the goals of the project and what kind of problems it tries to solve. This section should explain how to install it and basic usage, the Contributing and License sections can be left unchanged, and of course you can create new sections as necessary.

To run the automated tests for the python example just execute `tox`. It will generate a virtual environment with necessary dependencies and install the package in it. Then it will run flake8, mypy, coverage, and the tests from `tests/` directory, finally generating a report in the standard output plus the code coverage html page on `htmlcov/index.html`.


### Continuous Integration

The continuous integration is managed by [Github Actions](https://docs.github.com/en/actions). The file [main.yml](./.github/workflows/main.yml) contains an example with the most important features of it.

The section `on:` states that the CI will run on master and when pull requests are created and the target branch is master. The `runs-on` statement defines the runner which will execute the build, in this case "ubuntu-latest" (check [this link](https://docs.github.com/en/actions/reference/virtual-environments-for-github-hosted-runners) for the complete list of available runners hosted by Github). The `steps` here are equivalent to Tasks in bamboo, you can use pre-defined actions from Github or execute commands and scripts. The first step consists of downloading the repository, than we set up python configuration, run `tox` and finally save the cove coverage html page as an artifact.

### Issue Templates

Issue templates are meant to guide the users and developers on writing well descriptive issues. This repository includes one template for bug report and another for future request, both under `.github/ISSUE_TEMPLATE/` repositories. When clicking on "New Issue" in the project page the user can chose the template, which will provide the issue form with some details already filled in. 

## Contributing

Please check our [contribution guide](./CONTRIBUTING.md).

## License

repository-template is released under the [MIT License](https://opensource.org/licenses/MIT).
