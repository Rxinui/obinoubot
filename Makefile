dockerImage = rxinui/obinoubot:latest
dockerContainer = obinoubot-1

build-image:
	docker image build -t $(dockerImage) .

deploy-image:
	docker push $(dockerImage)

run-docker:
	docker rm -f $(dockerContainer)
	docker run --name $(dockerContainer) -e APP_ENV=dev $(dockerImage)

dev-run:
	docker-compose watch

stop-docker:
	docker kill $(dockerContainer)

