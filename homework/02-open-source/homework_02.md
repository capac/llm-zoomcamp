# Homework #2

Solutions and commands used for the homework.

## Solutions

### Solution for question 1

```
docker run -it --rm --entrypoint=bash -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Solution for question 2

```
{"schemaVersion":2,"mediaType":"application/vnd.docker.distribution.manifest.v2+json","config":{"mediaType":"application/vnd.docker.container.image.v1+json","digest":"sha256:887433b89a901c156f7e6944442f3c9e57f3c55d6ed52042cbb7303aea994290","size":483},"layers":[{"mediaType":"application/vnd.ollama.image.model","digest":"sha256:c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12","size":1678447520},{"mediaType":"application/vnd.ollama.image.license","digest":"sha256:097a36493f718248845233af1d3fefe7a303f864fae13bc31a3a9704229378ca","size":8433},{"mediaType":"application/vnd.ollama.image.template","digest":"sha256:109037bec39c0becc8221222ae23557559bc594290945a2c4221ab4f303b8871","size":136},{"mediaType":"application/vnd.ollama.image.params","digest":"sha256:22a838ceb7fb22755a3b0ae9b4eadde629d19be1f651f73efb8c6b4e2cd0eea0","size":84}]}
```

### Solution for question 3

Running the LLM. Output from "10 * 10":

```
Sure, here is the answer to your question:  10 * 10 = 100
```
To achieve this result, I first ran in the terminal the command:
```
> docker run -it --rm -v ./ollama_files:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
Then I ran the following command in a separate terminal:
```
> docker exec -it ollama /bin/bash
> ollama run gemma:2b
>>> 
```
This gave me the prompt for the answer to the homework question.

### Solution for question 4

After downloading the weights, what is the size of the folder?  1.6 GB.

I ran the modified Docker command:
```
> mkdir ollama_files
> docker run -it --rm -v ./ollama_files:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
> docker exec -it ollama ollama pull gemma:2b
```

### Solution for question 5

Question 5. Adding the weights. Dockerfile (1 point)
```
COPY [ "ollama_files/", "./"]
```

### Solution for question 6

Serving the LLM. Number of output tokens: 398.

See `homework_02.py` for the complete answer.
