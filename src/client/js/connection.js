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

  send_data(action, data) {
    if (this.websocket && this.websocket.readyState == WebSocket.OPEN) {
      //console.log({action, data});
      this.websocket.send(JSON.stringify({action, data}));
    }
  }
}
