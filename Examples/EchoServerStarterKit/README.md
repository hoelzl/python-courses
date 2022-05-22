# A Simple Echo Server

Run the server in development mode with

```shell
$ uvicorn echo_server_sk.__main__:app --reload
```

Send a GET request to `http://localhost:8000/docs` to get the OpenAPI
documentation of the service.

Send a GET request to `http://localhost:8000/` to get a "status message".

Send a GET requiest with query parameter `text` to 
`http://localhost:8000/echo`, e.g.

```
http://localhost:8000/echo?text=Hello+world!
```

to get back the text and the reversed text in JSON format.

Send a GET request with query parameter `msg` to 
`http://localhost:8000/rot/13` to get a rot-13 encoded text.
Replace `13` with any number less than or equal to 26 to get
the corresponding rotation. For example:

```
http://localhost:8000/rot/13?msg=URYYB+PENML+JBEYQ+BS+2022
```

To install the server, run:

```shell
$ python -m build
$ pip install dist/echo_server_sk-0.0.1-py3-none-any.whl
```

and then run the server with

```shell
$ uvicorn echo_server.__main__:app
```