'use strict';

class Display {
  width = 800;
  height = 544;

  constructor(canvas) {
    this.canvas = canvas;
  }

  drawBackground() {
    this.canvas.drawImage({
      layer: true,
      source: 'img/background.jpg',
      scale: 1,
      x: width / 2,
      y: height / 2,
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

  draw(data) {
    data.nonplayers.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.id%2 ? 'green': 'red');
    });

    this.canvas.drawLayers();
  }
}
