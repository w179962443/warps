

nvidia-docker run -dti --name bloom_faster_transformer \
--restart=always --gpus all --network=host \
--shm-size 5g \
-v /home/user/workspace/code :/workspace/code \
-v/ home/user/workspace/data :/workspace/data \
-v/ home/user/workspace/model :/workspace/model \
-v/ home/user/workspace/output :/workspace/output \
-w /workspace \
nvcr.io/nvidia/pytorch:22.89-py3 \
bash


docker run --name temp_redis_1013 -d redis redis-server --save 60 1 --loglevel warning

