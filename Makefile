dockerImage = rxinui/obinoubot:latest
dockerContainer = obinoubot-1

build-image:
	docker image build -t $(dockerImage) .

deploy-image:
	docker push $(dockerImage)

run-docker:
	docker rm -f $(dockerContainer)
	docker run --name $(dockerContainer) -e APP_ENV=dev $(dockerImage)

stop-docker:
	docker kill $(dockerContainer)