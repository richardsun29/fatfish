# Fat Fish

1. Install dependencies:

NOTE: the server needs Python 3.5 or higher to run
```
cd src/server
pip install -r requirements.txt
```

2. Start the server:
```
cd src/server
python server.py localhost 8765
```

3. Serve the client files (in a different terminal):
```
cd src/client
python -m http.server 8000
```

4. Connect to the client by opening `localhost:8000` in a web browser. The server
address is `127.0.0.1:8765` or whichever port you chose to serve it on.
