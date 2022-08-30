# API for mBART

## How to run the server?
--------------------
1. Install [docker](https://docs.docker.com/get-docker/).
2. in the terminal or cmd, move to the path of the project (inside umls directory).
3. You first need to create the directory for the models. Run in the console:

        $ mkdir -p models
        $ mkdir -p models/mBART

4. Create a directory for logging:

        $ mkdir -p logging

5. Put all the files generated during the training inside the models/mBART directory (config.json, pytorch_model.bin, sentencepiece.bpe.model, special_tokens_map.json, tokenizer_config.json, tokenizer.json).

6. run docker-compose up:

    $ docker-compose up --build -d


## how to verify if the container is running?
---------------------
Let's see if the image is running:

    docker ps -as

## how to send request to the api? Example
    $ curl --request POST --url http://localhost:8000/translate --header 'Content-Type: application/json' --data '{"input": ["<sentence 1>"], "id": 100}'
