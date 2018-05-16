var websocket = new WebSocket("ws://127.0.0.1:8765/");

function receive_data(data) {
  $('#recv-msg').text(data);
}

function sendbtn() {
  send_data($('#send-msg').val());
}

function send_data(data) {
  websocket.send(data);
}

$(document).ready(() => {
  // listen for messages
  websocket.onmessage = event => receive_data(event.data);

  // send initial message
  websocket.onopen = () => {};

  // connection close
  websocket.onclose = event => console.log('Websocket closed.', event);
});
