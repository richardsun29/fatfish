'use strict';

class App {
  constructor() {
    this.modal = new Modal();
    this.display = new Display($('#canvas'));
    this.leaderboard = new Leaderboard($('#leaderboard'));
    this.connection = new Connection();
    this.moveDirection = {x: 0, y: 0};
    this.dead = false;

    // connect to server stuff
    this.modal.show(null);
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
    try {
      this.connection.connect(ip,
          (event) => this.onopen(event, name),
          (event) => this.onmessage(event),
          (event) => this.onclose(event));
    } catch(e) {
      this.modal.show('Connection Error');
    }
  }

  onopen(event, name) {
    this.modal.hide();
    this.connection.send_data('newplayer', { name });
    this.dead = false;
  }

  onmessage(event) {
    var data = JSON.parse(event.data);
    if (data.status == 'dead') {
      this.dead = true;
      this.connection.disconnect();
    }
    else {
      this.display.draw(data);
      this.leaderboard.update(data);
    }
  }

  onclose(event) {
    if (event.wasClean) {
      if (this.dead) {
        this.modal.show('You got eaten!');
      }
      else {
        this.modal.show();
      }
    }
    else {
      this.modal.show('Connection Error');
    }
  }
}


$(() => {
  var app = new App();
});
