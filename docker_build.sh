docker build . -t dashboard:0.9
# docker run --rm -it --entrypoint=/usr/bin/python3.7 dashboard:0.9


docker run \
  --rm \
  --name covid-19-dashboard \
  --publish 8050:8050 \
dashboard:0.9