class MockResponse:
    """
    Мок api ответа для сессии клиента.
    """
    def __init__(self, status, response):
        self.status = status
        self.response = response

    async def json(self):
        return self.response

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
