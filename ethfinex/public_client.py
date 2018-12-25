import requests


class PublicClient(object):
    """Ethfinex public client API."""

    def __init__(
        self,
        api_url: str = 'https://api.ethfinex.com/v2',
        timeout: int = 30
    ) -> None:
        """Create Ethfinex API public client."""
        self.url = api_url.rstrip('/')
        self.auth = None
        self.session = requests.Session()

    def get_ticker(self, pair) -> list:
        """Get a list of available currency pairs for trading.
        Returns:
            [
              BID,
              BID_SIZE,
              ASK,
              ASK_SIZE,
              DAILY_CHANGE,
              DAILY_CHANGE_PERC,
              LAST_PRICE,
              VOLUME,
              HIGH,
              LOW
            ]
        """
        return self._send_message(f'/ticker/{pair}')

    def _send_message(
        self,
        endpoint: str,
        params: dict = None,
        data: str = None
    ) -> dict:
        """Send API request."""
        url = self.url + endpoint
        r = self.session.request('get', url, params=params, data=data,
                                 auth=self.auth, timeout=30)
        print(r)
        print(r.text)
        return r.json()
