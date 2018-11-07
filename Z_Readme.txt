Run Readme:

this file explain how to run the docker with the jupyter notebook:
run this following commands:

docker build -t zebra .

docker run -it -p 9999:9999/tcp <ID> /bin/bash

cd /tmp

jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port=9999

then go over the notebook
and after that check the 2 zip files with the other components