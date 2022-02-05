import asyncio

class Request:
    def __init__(self, *args, **kwargs):
        """Create a request for JSON data from a url"""
        self.bot = args[0]
        self.url = kwargs.pop('url')
        self.params = kwargs.pop('params', {})
        return asyncio.run(self.send())
    
    @property
    def _url(self):
        """Return the url of the request"""
        return self.url
    
    @property
    def _params(self):
        """Return the params of the request"""
        return self.params
    
    @property
    def _sessions(self):
        """The HTTP Session"""
        return self.bot.http._HTTPClient__session
    
    async def send(self):
        """Send the request"""
        response = await self.session.get(self._url, params=self._params)
        return await response.json()
