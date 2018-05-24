'use strict';

class Display {
  constructor(canvas) {
    this.canvas = canvas;
  }

  drawBackground() {
    this.canvas.drawImage({
      layer: true,
      source: 'img/background.jpg',
      scale: 1,
      x: 800 / 2,
      y: 544 / 2,
    });
  }

  drawFish(id, x, y, size, shadowColor) {
    var layer = `fish${id}`;
    var scale = 0.1; //size;

    // check if layer exists
    if (this.canvas.getLayer(layer)) {
      // change layer
      this.canvas.setLayer(layer, {x, y, scale, shadowColor});
    }
    else {
      // create new layer
      this.canvas.drawImage({x, y, scale, shadowColor,
        layer: true,
        name: layer,
        source: 'img/fish.png',
        shadowBlur: 20
      });
    }
  }
}
