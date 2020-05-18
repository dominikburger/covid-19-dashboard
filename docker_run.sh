docker run \
  --rm \
  --name covid-19-dashboard \
  --publish 8050:8050 \
  --volume dashboard-volume:/home/appuser/app/data \
dashboard:0.9