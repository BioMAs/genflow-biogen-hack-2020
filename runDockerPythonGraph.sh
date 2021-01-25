IMAGENAME=fjrmore/pax2graphml
chmod -R 777 ./data
#OPT=" -v $PWD/data:/home/user/data "

OPT=""
docker run -p 80:8888 -p 6006:6006 -it $OPT -u user -w /home/user $IMAGENAME  bash -c "jupyter lab  --ip 0.0.0.0 "

