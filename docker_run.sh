docker run \
  -ti \
  --name covid-dashboard \
  --publish 8050:8050 \
  --volume dashboard-volume:/home/appuser/app/data \
covid-dashboard