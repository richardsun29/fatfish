'use strict';

class Display {

  constructor(canvas) {
    this.canvas = canvas;
    this.width = 800;
    this.height = 544;

    this.drawBackground();
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
    var layer = `fish${id}`;
    var scale = size / 10;

    x = this.width  * x / 100;
    y = this.height * y / 100;

    this.canvas.drawImage({x, y, scale, shadowColor,
      layer: true,
      name: layer,
      source: 'img/fish.png',
      shadowBlur: 20
    });
  }

  draw(data) {
    this.canvas.removeLayers();
    this.drawBackground();

    // draw fish
    data.players.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.size, 'blue');
    });
    data.nonplayers.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.size, p.id%2 ? 'green': 'red');
    });

    this.canvas.drawLayers();
  }
}
