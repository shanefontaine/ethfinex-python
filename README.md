# ethfinex-python

[![Build Status](https://travis-ci.org/shanefontaine/ethfinex-python.svg?branch=master)](https://travis-ci.org/shanefontaine/ethfinex-python)
[![Downloads](https://pepy.tech/badge/ethfinex-python)](https://pepy.tech/project/ethfinex-python)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/shanefontaine/ethfinex-python/master/LICENSE)

The unofficial Python client for the [Ethfinex](https://www.ethfinex.com/api_docs) and [Ethfinex Trustless](https://ethfinex.docs.apiary.io/#) APIs.

##### Provided under MIT License by Shane Fontaine.
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

_I am in no way affiliated with or funded by Ethfinex, Ethfinex Trustless, Ethfinex Inc., Bitfinex, iFinex Inc., Tether, Tether Limited, or any subsidiaries or affiliates of any of the previously mentioned entities._

## Functionality
- A simple to use Python wrapper for both public and authenticated endpoints.
- [Easy trading directly against Ethfinex Trustless, Bitfinex and Ethfinex orderbooks](https://blog.ethfinex.com/introducing-ethfinex-trustless-2f7390955fe0/)
- Simple parsing of data returned from the Ethfinex API

## Under Development
- Better error handling
- Tests

## Getting Started
This README is documentation on the syntax of the python client presented in this repository. See function docstrings for full syntax details.
This API attempts to present a clean interface to Ethfinex, but in order to use it to its full potential, you must familiarize yourself with the official Ethfinex documentation.

- https://www.ethfinex.com/api_docs

You may manually install the project or use pip:

```python
pip install ethfinex-python

# or

pip install git+git://github.com/shanefontaine/ethfinex-python.git
```

### Public Client
Only some endpoints in the API are available to everyone. The public endpoints can be reached using PublicClient

```python
import ethfinex
public_client = ethfinex.PublicClient()
```

### PublicClient Methods
- [get_platform_status](https://docs.bitfinex.com/v2/reference#rest-public-platform-status)
```python
public_client.get_platform_status()
```

- [get_ticker](https://docs.bitfinex.com/v2/reference#rest-public-ticker)
```python
# Get the ticker for a specific pair.
public_client.get_ticker('tBTCUSD')
```

- [get_trades](https://docs.bitfinex.com/v2/reference#rest-public-trades)
```python
# Get the trades for a specific pair
public_client.get_trades('tBTCUSD')
# To include a start and end time
public_client.get_trades('tBTCUSD', start=1514764800000, end=1514765700000)
# To reverse the order that data is delivered (old to new)
public_client.get_trades('tBTCUSD', start=1514764800000, end=1514765700000, sort=1)
```

- [get_books](https://docs.bitfinex.com/v2/reference#rest-public-books)
```python
# Get the books for a specific pair
public_client.get_books('tBTCUSD')
# To get more or less granular precision
public_client.get_books('tBTCUSD', precision='P1')
```

- [get_stats](https://docs.bitfinex.com/v2/reference#rest-public-stats)
```python
# Get the stats for a specific pair
public_client.get_stats('tBTCUSD', 'funding.size', 'long', 'hist')
# To reverse the order that data is delivered (old to new)
public_client.get_stats('tBTCUSD', 'funding.size', 'long', 'hist', sort=1)
```

- [get_candles](https://docs.bitfinex.com/v2/reference#rest-public-candles)
```python
# Get the candles for a specific pair
public_client.get_candles('tBTCUSD', '1m', 'hist')
# To include a start and end time
public_client.get_candles('tBTCUSD', '1m', 'hist', start=1514764800000, end=1514765700000)
```

## Testing
Unit tests are under development using the pytest framework. Contributions are welcome!

To run the full test suite, in the project directory run:

```
python -m pytest
```

## Changelog

_0.1.2_
- Major README update

_0.1.1_
- Add CI
- Add `public_client` tests

_0.1.0_
- Fully functional public client.

_0.0.1_
- Original PyPI release.
