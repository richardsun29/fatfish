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

    this.canvas.drawImage({x, y, scale, shadowColor,
      layer: true,
      name: layer,
      source: 'img/fish.png',
      shadowBlur: 20
    });
  }

  getShadowColor(playerSize, fishSize) {
    // color fish red if bigger, yellow if same size, blue if smaller
    if (fishSize > playerSize) {
      return 'red';
    }
    if (fishSize < playerSize) {
      return 'blue';
    }
    return 'yellow';
  }

  draw(data) {
    // this client's fish
    var player = data.players.find(p => p.id == data.id);
    var playerSize = player ? player.size : 0;

    // reset canvas
    this.canvas.removeLayers();
    this.drawBackground();

    // draw fish
    data.players.forEach(p => {
      if (p.id == player.id) {
        this.drawFish(p.id, p.x, p.y, p.size, undefined);
      }
      else {
        this.drawFish(p.id, p.x, p.y, p.size, this.getShadowColor(playerSize, p.size));
      }
    });
    data.nonplayers.forEach(p => {
      this.drawFish(p.id, p.x, p.y, p.size, this.getShadowColor(playerSize, p.size));
    });

    this.canvas.drawLayers();
  }
}
