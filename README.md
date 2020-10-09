# Chromecast API
A simple REST API for sending media, including text-to-speech (tts) to Google Chromecast devices, including Google Home and Nest devices.


## Getting Started 
To use this template, first generate a new repository from it, by clicking **"[Use this template](https://github.com/lyngon/fastapi-docker-template/generate)"** and select a name and visibility settings etc for the new repository.
Then clone the new repository as normal, after which it is recommemnded to:
1. Update the `.env` file in the repository root to reflect your new project. Paticularly:
    - Change the `COMPOSE_PROJECT_NAME` variable to represent your project name.
        
        This variable will both be used as service prefix when running with *docker-compose*, as well as used   

