# solida-gui

Container Docker application that facilitate the reproducibility and portability of NGS pipelines.
It can easily organize the deployment, the data management and the execution 
of a Snakemake based workflow

solida-gui container include:
- [solida](https://github.com/solida-core/solida): Python command-line tool 
- Graphical User Iterface developed in Django


## Requirements

You need [docker-engine](https://docs.docker.com/engine/installation/) 
and [docker-compose](https://docs.docker.com/compose/install/)  
See [docker-compose docs](https://docs.docker.com/compose/reference/overview/)

## Quick start

Create the workdir tree:
```bash
mkdir ~/solida-core             #path where installing solida, configs file, profiles and pipelines
mkdir ~/solida-core/projects    #path where deploying projects in localhost
```

> You can change these paths as you prefer, but remember to modify docker-compose.yaml file accordly
> ```yaml
> ...
> volumes:
>      - ~/solida-core:/root
>      - ~/solida-core/projects:/root/projects
> ...
>```

Clone the repository:  
```bash
git clone https://github.com/ratzeni/solida-gui.git
```

Cd into the docker directory:  
```bash
cd solida-gui
```
Bring up the containers:  
```bash
docker-compose up
```

Point your browser to: 
`http://0.0.0.0:8000` 
