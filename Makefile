dockerImage = rxinui/obinoubot:latest
dockerContainer = obinoubot-1
tokenBot = $(shell cat ./token)
build-image:
	docker image build -t $(dockerImage) --build-arg TOKEN_BOT=$(tokenBot) --build-arg APP_ENV=prod  .

deploy-image:
	docker push $(dockerImage)

run-docker:
	docker rm -f $(dockerContainer)
	docker run --name $(dockerContainer) -e APP_ENV=dev $(dockerImage)

run-docker-prod:
	docker rm -f $(dockerContainer)
	docker run --name $(dockerContainer) -e APP_ENV=prod -e TOKEN_BOT=$(tokenBot) $(dockerImage)

dev-run:
	docker-compose watch

stop-docker:
	docker kill $(dockerContainer)

test:
	echo $(tokenBot)

