dev-games-api:
	cd games-api/src/ && python -m fastapi dev --reload

build-games-api:
	podman build -t danivy-com-games-api -f games-api/Dockerfile .

run-games-api: build-games-api
	podman run --rm -it -p 8000:8000 -v ~/.kube/config:/root/.kube/config danivy-com-games-api

dev-games-ui:
	cd games-ui/ && yarn dev

build-games-ui:
	podman build -t danivy-com-games-ui -f games-ui/Dockerfile .

run-games-ui: build-games-ui
	podman run --rm -it -p 8080:8080 danivy-com-games-ui

debug-games-ui: build-games-ui
	podman run --rm -it -p 8080:8080 --entrypoint ash danivy-com-games-ui 
