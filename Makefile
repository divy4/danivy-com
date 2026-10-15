dev-games-api:
	cd games-api/src/ && python -m fastapi dev --reload

build-games-api:
	podman build -t registry-1.docker.io/divy4/games-api -f games-api/Dockerfile .

run-games-api: build-games-api
	podman run --rm -it -p 8000:8000 -v ~/.kube/config:/root/.kube/config --env K8S_NAMESPACE="${K8S_NAMESPACE}" registry-1.docker.io/divy4/games-api

push-games-api:
	podman push registry-1.docker.io/divy4/games-api

dev-games-ui:
	cd games-ui/ && yarn dev

build-games-ui:
	podman build -t registry-1.docker.io/divy4/games-ui -f games-ui/Dockerfile .

run-games-ui: build-games-ui
	podman run --rm -it -p 8080:8080 registry-1.docker.io/divy4/games-ui

push-games-ui:
	podman push registry-1.docker.io/divy4/games-ui

build-games: build-games-api build-games-ui

push-games: push-games-api push-games-ui
