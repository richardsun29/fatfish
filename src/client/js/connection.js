'use strict';

class Connection {
  constructor() {
  }

  connect(addr, onopen, onmessage, onclose) {
    this.websocket = new WebSocket('ws://' + addr);

    this.websocket.onopen = onopen;
    this.websocket.onmessage = onmessage;
    this.websocket.onclose = onclose;
  }

  disconnect() {
    if (this.websocket) {
      this.websocket.close();
    }
  }

  send_data(action, value) {
    console.log({action, value});
    if (this.websocket) {
      this.websocket.send(JSON.stringify({action, value}));
    }
  }
}
