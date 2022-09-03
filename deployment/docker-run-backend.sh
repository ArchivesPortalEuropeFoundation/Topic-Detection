docker stop topic-detection-backend
docker rm topic-detection-backend
docker run -d --name topic-detection-backend --cpus 4 -p 10.32.34.169:8091:5000 -v /data/containerdata/topicdetection/volumes/config:/config -v /data/containerdata/topicdetection/volumes/data:/webapp/data -v /data/containerdata/topicdetection/volumes/word-embs:/webapp/word-embs --network=ape --restart unless-stopped topic-detection:dev
