'use strict';

class Connection {
  constructor(addr) {
    this.addr = 'ws://' + addr;
  }

  connect() {
    this.websocket = new WebSocket(this.addr);

    // listen for messages
    this.websocket.onmessage = event => this.receive_data(event.data);

    // connection close
    this.websocket.onclose = event => console.log('Websocket closed.', event);
  }

  onmessage(callback) {
    this.websocket.onmessage = callback;
  }

  onclose(callback) {
    this.websocket.onclose = callback;
  }

  receive_data(data) {
    //console.log(data);
  }

  send_data(action, value) {
    console.log({action, value});
    this.websocket.send(JSON.stringify({action, value}));
  }
}
