'use strict';

class App {
  constructor() {
    this.modal = new Modal();
    this.display = new Display($('#canvas'));
    this.connection = new Connection();
    this.moveDirection = {x: 0, y: 0};

    // connect to server stuff
    this.modal.show(false);
    this.modal.submit(this.connect.bind(this));
    $('#disconnect-btn').click(() => {
      this.connection.disconnect();
    });

    // handle move start
    $(document).keydown(event => {
      switch(this.keyDirection(event)) {
        case 'up':
          this.movePlayer({y: -1}); break;
        case 'down':
          this.movePlayer({y: 1}); break;
        case 'left':
          this.movePlayer({x: -1}); break;
        case 'right':
          this.movePlayer({x: 1}); break;
      }
    });

    // handle move end
    $(document).keyup(event => {
      switch(this.keyDirection(event)) {
        case 'up':
        case 'down':
          this.movePlayer({y: 0}); break;
        case 'left':
        case 'right':
          this.movePlayer({x: 0}); break;
      }
    });
  }

  keyDirection(event) {
    // move with arrow keys or WASD
    switch(event.key) {
      case 'w':
      case 'W':
      case 'ArrowUp':
        return 'up';
      case 'a':
      case 'A':
      case 'ArrowLeft':
        return 'left';
      case 's':
      case 'S':
      case 'ArrowDown':
        return 'down';
      case 'd':
      case 'D':
      case 'ArrowRight':
        return 'right';
      default:
        return null;
    }
  }

  movePlayer(direction) {
    var xold = this.moveDirection.x;
    var yold = this.moveDirection.y;
    var xnew = (direction.x != undefined) ? direction.x : xold;
    var ynew = (direction.y != undefined) ? direction.y : yold;

    // if direction changed
    if (xnew != xold || ynew != yold) {
      this.moveDirection = {x: xnew, y: ynew};
      this.connection.send_data('move', this.moveDirection);
    }
  }

  connect(ip, name) {
    this.connection.connect(ip,
        (event) => this.onopen(event, name),
        (event) => this.onmessage(event),
        (event) => this.onclose(event));
  }

  onopen(event, name) {
    this.modal.hide();
    this.connection.send_data('newplayer', { name });
  }

  onmessage(event) {
    var data = JSON.parse(event.data);
    this.display.draw(data);
  }

  onclose(event) {
    this.modal.show(!event.wasClean);
  }
}


$(() => {
  var app = new App();
});
