# fastapi-docker-template
A template repo to use as a starting point for building [Dockerized](https://www.docker.com/) APIs using Python 3.8 and [FastAPI](https://fastapi.tiangolo.com/). With strict and extensive code quality tools, like [black](https://github.com/psf/black), [flake8](https://gitlab.com/pycqa/flake8), [isort](https://pycqa.github.io/isort/), [pytest](https://docs.pytest.org) and [pytest-cov](https://github.com/pytest-dev/pytest-cov) right out of the box.

## Getting Started
To use this template, first generate a new repository from it, by clicking **"[Use this template](https://github.com/lyngon/fastapi-docker-template/generate)"** and select a name and visibility settings etc for the new repository.
Then clone the new repository as normal, after which it is recommemnded to:
1. Update the `.env` file in the repository root to reflect your new project. Paticularly:
    - Change the `COMPOSE_PROJECT_NAME` variable to represent your project name.
        
        This variable will both be used as service prefix when running with *docker-compose*, as well as used   

