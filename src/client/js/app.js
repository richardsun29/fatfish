'use strict';

$(() => {
  var display = new Display($('#canvas'));
  display.drawBackground();

  /*
  var y = 100;
  setInterval(function() {
    display.drawFish(1, 100, y++, 10, 'blue');
    display.canvas.drawLayers();
  }, 100);
  */

  var connection = new Connection('127.0.0.1:8765');
  connection.connect();

  connection.onmessage(data => {
    display.draw(data);
  });
});
