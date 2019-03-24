import locust


class StressBehavior(locust.TaskSet):
    @locust.task(weight=3)
    def users_get(self) -> None:
        self.client.get(
            '/users',

        )

    @locust.task(weight=2)
    def status(self) -> None:
        self.client.get('/status')

    @locust.task(weight=1)
    def swagger_json(self) -> None:
        self.client.get('/openapi.json')


class StressLocust(locust.HttpLocust):
    task_set = StressBehavior
    min_wait = 5000
    max_wait = 30000
