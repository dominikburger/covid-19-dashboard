# COVID-19 Dashboard
![dashboard_preview](docs/dashboard_preview.png)
This project aims to visualize the infection data of the ongoing COVID-19 
pandemic in an understandable and appealing way. Building on the CSSE dataset of
the Johns Hopkins Unversity, we are using the Python framework Dash to create a
dashboard. It provides information about the current worldwide development of 
the disease and shows both daily charts as well as charts covering the time
frame from disease outbreak up to the current day. 

## Installation & Requirements
The following instructions assume that the your current working directory is a local copy of the repository.
At the moment, there are two ways to run the dashboard on your own machine:
#### Anaconda
Create a new Anaconda environment called *covid-dashboard* by using the provided *environment.yml*
(the environment name is changeable by editing the first line in the yaml file):
```
conda env create -f environment.yml
```
You can then activate the enviroment and start up the dashboard running `python3 app.py` 

#### Docker
Build your own docker image using the provided Dockerfile via
```
docker build . --rm -t covid-dashboard
```
to create an image called *covid-dashboard*. When running the container, it is 
advised to mount a volume where the downloaded and parsed data is stored. This 
can be a local folder (don't forget to change the host path in the `docker run [...]` 
command if do so) or a docker volume for example. If you want to use the latter,
you can create a volume named *dashboard-volume* using:
```
docker volume create dashboard-volume
```
After the build process has successfully completed, you can run the image in a
container via
```
docker run \
  -ti \
  --name covid-dashboard \
  --publish 8050:8050 \
  --volume dashboard-volume:/home/appuser/app/data \
covid-dashboard
```
You can also use `docker_build.sh` and `docker_run.sh` which contain the commands
specified above.

## Usage
The dashboard is web based and can be accessed via browsing to 
`http://0.0.0.0:8050/` with a browser of your choice.

