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

    def get_platform_status(self) -> str:
        """Get the current status of the platform.
        Returns:
            1=operative
            0=maintenance
        """
        return self._send_message('/platform/status')

    def get_ticker(self, pair: str) -> list:
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

    def get_trades(
        self,
        pair: str,
        limit: int = 0,
        start: int = 0,
        end: int = 0,
        sort: int = 0
    ) -> list:
        """Get all the pertinent details of the trade, such as price, size and
        time. `sort=1` will sort results from old to new.
        Returns:
        [
            [
                ID,
                MTS,
                AMOUNT,
                PRICE
            ]
        ]
        """
        params = {}
        if limit:
            params['limit'] = limit
        if start and end and start < end:
            params['start'] = start
            params['end'] = end
        else:
            raise ValueError('The start time cannot be after the end time.')
        if sort:
            params['sort'] = sort
        return self._send_message(f'/trades/{pair}/hist', params=params)

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
