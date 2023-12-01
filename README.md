# RCONClient

This Python script implements a basic RCON (Remote Console) client to communicate with an RCON server. It allows sending commands and receiving responses from an RCON-enabled game or server.

## Overview

The RCONClient class provides functionality to establish a TCP connection to the RCON server, perform login/authentication using a password, send commands, and handle responses from the server.

## Installation
1. Clone the repository or download the code file.
2. Install the required dependencies:
```pip install socket```

## Usage:
1. Create an instance of the ```RCONClient``` class, providing the server host, port, and password:
```python
with RCONClient('localhost', 27020, '12345') as rcon_client:
```
2. Execute RCON commands using the ```command()``` method:
```python
rcon_client.command('listplayers')
```
3. The response from the server will be printed to the console.

## Features

  - Establishes a TCP connection to the RCON server
  - Performs authentication with the server using the provided password
  - Executes RCON commands and handles the response
  - Provides a context manager for simplified usage

