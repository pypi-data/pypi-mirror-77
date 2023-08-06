# Swim System Python Implementation
[![PyPI version](https://badge.fury.io/py/swimai.svg)](https://badge.fury.io/py/swimai)
[![Build Status](https://travis-ci.com/swimos/swim-system-python.svg?branch=master)](https://travis-ci.com/swimos/swim-system-python)
[![codecov](https://codecov.io/gh/swimos/swim-system-python/branch/master/graph/badge.svg)](https://codecov.io/gh/swimos/swim-system-python)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/code-of%20conduct-green.svg)](CODE_OF_CONDUCT.md)
[![chat](https://img.shields.io/badge/chat-Gitter-green.svg)](https://gitter.im/swimos/community)
<a href="https://www.swimos.org"><img src="https://docs.swimos.org/readme/marlin-blue.svg" align="left"></a>

The **Swim System** Python implementation provides a standalone set of
frameworks for building massively real-time streaming WARP clients.

The **Swim Python Client** is a streaming API client for linking to lanes 
of stateful Web Agents using the WARP protocol, enabling massively 
real-time applications that continuously synchronize all shared states 
with ping latency. WARP is like pub-sub without the broker, 
enabling every state of a Web API to be streamed, without 
interference from billions of queues.
<br>
## Installation
`pip install swimai`
## Usage
```python
# Setting the value of a value lane on a remote agent.
import time

from swimai import SwimClient

with SwimClient() as swim_client:
    host_uri = 'ws://localhost:9001'
    node_uri = '/unit/foo'
    lane_uri = 'info'

    value_downlink = swim_client.downlink_value()
    value_downlink.set_host_uri('ws://localhost:9001')
    value_downlink.set_node_uri('/unit/foo')
    value_downlink.set_lane_uri('info')
    value_downlink.open()

    new_value = 'Hello from Python!'
    value_downlink.set(new_value)

    print('Stopping the client in 2 seconds')
    time.sleep(2)
```
## Development

### Dependencies
##### Code dependencies
`pip install -r requirements.txt`
##### Development tools dependencies
`pip install -r requirements-dev.txt`
### Run unit tests
##### Basic:
1) Install async test package: `pip install aiounittest`
2) Run tests: `python -m unittest`

##### With coverage:
1) Install async test package: `pip install aiounittest`
2) Install coverage package: `pip install coverage`
3) Generate report: `coverage run --source=swimai -m unittest`
4) View report: `coverage report -m`

### Run Lint
##### Manual
1) Install lint package: `pip install flake8`
2) Run checks: `flake8`
##### Automatic (before commit)
1) Install commit hook package: `pip install pre-commit`
2) Run hook installation: `pre-commit install`
### Build package
##### Building source distribution
1) Run: `python setup.py sdist`
##### Building wheel
1) Install wheel package: `pip install wheel`
2) Run: `python setup.py sdist`

