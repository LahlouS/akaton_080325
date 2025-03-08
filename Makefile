NAME = hackaton
CONTAINER = podman

PORT = 8000:8000
ENV_FILE = .env

VOLUME = $(shell pwd):/app

all: build run


build:
	@$(CONTAINER) build -t $(NAME) . 

run:
	@$(CONTAINER) run \
		-it --rm \
		--env-file $(ENV_FILE) \
		-p $(PORT) \
		-v $(VOLUME) \
		localhost/$(NAME):latest \
		python main.py 

bash:
	@$(CONTAINER) run \
		-it --rm \
		--env-file $(ENV_FILE) \
		-p $(PORT) \
		-v $(VOLUME) \
		localhost/$(NAME):latest \
		bash 