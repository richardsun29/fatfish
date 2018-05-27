'use strict';

class Display {

  constructor(canvas) {
    this.canvas = canvas;
    this.width = 800;
    this.height = 544;

    this.drawBackground();

    // occasionally delete old layers
    setInterval(() => this.cleanup(), 1000);
  }

  layerName(id) {
    return `fish${id}`;
  }

  drawBackground() {
    this.canvas.drawImage({
      layer: true,
      name: 'background',
      source: 'img/background.jpg',
      scale: 1,
      x: this.width / 2,
      y: this.height / 2,
    });
  }

  drawFish(id, x, y, size, shadowColor) {
    var layer = this.layerName(id);
    var scale = size / 10;

    x = this.width  * x / 100;
    y = this.height * y / 100;

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

  // hide fish that no longer exist and mark for cleanup
  hideFish(layer) {
    if (this.canvas.getLayer(layer)) {
      this.canvas.setLayer(layer, {
        x: -100, y: -100,
        scale: 0,
        shadowColor: undefined,
        data: { cleanup: true },
      });
    }
  }

  draw(data) {
    var keepLayer = {'background': true};

    this.drawBackground();

    // draw fish
    data.players.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.size, 'blue');
      keepLayer[this.layerName(p.id)] = true;
    });
    data.nonplayers.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.size, p.id%2 ? 'green': 'red');
      keepLayer[this.layerName(p.id)] = true;
    });

    // hide layers that no longer exist
    this.canvas.getLayers().forEach(layer => {
      if (!keepLayer[layer.name] && !layer.data.cleanup) {
        this.hideFish(layer.name);
      }
    });

    this.canvas.drawLayers();
  }

  cleanup() {
    this.canvas.removeLayers();
  }
}
