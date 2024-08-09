# Contributing to  Notepad Application

First off, thank you for considering contributing to the Notepad Application! It's people like you that make it such a great tool.

## Table of Contents
1. [Getting Started](#getting-started)
   - [Issues](#issues)
   - [Pull Requests](#pull-requests)
2. [Coding Guidelines](#coding-guidelines)
3. [Commit Message Guidelines](#commit-message-guidelines)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Community](#community)


## Getting Started

Contributions to the Notepad Application are made via Issues and Pull Requests (PRs). A few general guidelines that cover both:

- Search for existing Issues and PRs before creating your own.
- We work hard to makes sure issues are handled in a timely manner but, depending on the impact, it could take a while to investigate the root cause. A friendly ping in the comment thread to the submitter or a contributor can help draw attention if your issue is blocking.

### Issues

Issues should be used to report problems with the application, request a new feature, or to discuss potential changes before a PR is created. When you create a new Issue, a template will be loaded that will guide you through collecting and providing the information we need to investigate.

If you find an Issue that addresses the problem you're having, please add your own reproduction information to the existing issue rather than creating a new one. Adding a [reaction](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) can also help be indicating to our maintainers that a particular problem is affecting more than just the reporter.

### Pull Requests

PRs to our libraries are always welcome and can be a quick way to get your fix or improvement slated for the next release. In general, PRs should:

1. Only fix/add the functionality in question OR address wide-spread whitespace/style issues, not both.
2. Add unit or integration tests for fixed or changed functionality (if a test suite already exists).
3. Address a single concern in the least number of changed lines as possible.
4. Include documentation in the repo or on our [docs site](https://github.com/Hopelezz/NotePad).
5. Be accompanied by a complete Pull Request template (loaded automatically when a PR is created).

For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an Issue to discuss your proposal first. This is not required but can save time creating and reviewing changes.

In general, we follow the ["fork-and-pull" Git workflow](https://github.com/susam/gitpr)

1. Fork the repository to your own Github account
2. Clone the project to your machine
3. Create a branch locally with a succinct but descriptive name
4. Commit changes to the branch
5. Following any formatting and testing guidelines specific to this repo
6. Push changes to your fork
7. Open a PR in our repository and follow the PR template so that we can efficiently review the changes.

## Coding Guidelines

To ensure consistency throughout the source code, keep these rules in mind as you are working:

1. All features or bug fixes **must be tested** by one or more specs (unit-tests).
2. We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
3. We use [Black](https://github.com/psf/black) for code formatting. Run `black .` before committing.
4. We use [Flake8](https://flake8.pycqa.org/en/latest/) for linting. Run `flake8` before committing.

## Commit Message Guidelines

We have very precise rules over how our git commit messages can be formatted. This leads to **more readable messages** that are easy to follow when looking through the **project history**.

### Commit Message Format
Each commit message consists of a **header**, a **body** and a **footer**. The header has a special format that includes a **type**, a **scope** and a **subject**:<type>(<scope>): <subject>
<BLANK LINE>

<body> <BLANK LINE> <footer>he **header** is mandatory and the **scope** of the header is optional.

Any line of the commit message cannot be longer than 100 characters! This allows the message to be easier to read on GitHub as well as in various git tools.

### Type
Must be one of the following:

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **perf**: A code change that improves performance
* **test**: Adding missing tests or correcting existing tests
* **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Testing

We use pytest for our testing framework. To run the tests, use the following command:

pytest


Please ensure all tests pass before submitting a PR.

## Documentation

Documentation is a crucial part of this project. Please ensure that you update the documentation when you make changes to the code.

## Community

Discussions about the Notepad Application take place on this repository's [Issues](https://github.com/Hopelezz/NotePad/issues) and [Pull Requests](https://github.com/Hopelezz/NotePad/pulls) sections. Anybody is welcome to join these conversations.