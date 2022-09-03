docker stop topic-detection-webapp
docker rm topic-detection-webapp
chown -R federico:federico /data/containerdata/topicdetection
docker pull php:7.3-apache
docker run -d --name topic-detection-webapp --user 1005:1005 -p 10.32.34.169:8090:80 -v /data/containerdata/topicdetection/volumes/config:/config -v /data/containerdata/topicdetection/Topic-Detection/interface:/var/www/html/topicdetection --network=ape --restart unless-stopped php:7.3-apache
