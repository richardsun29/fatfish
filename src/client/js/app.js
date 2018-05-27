'use strict';

class App {
  constructor() {
    this.modal = new Modal();
    this.display = new Display($('#canvas'));
    this.connection = new Connection();

    this.modal.show(false);
    this.modal.submit(this.connect.bind(this));

    $('#disconnect-btn').click(() => {
      this.connection.disconnect();
    });
  }

  connect(ip, name) {
    this.connection.connect(ip, this.onopen.bind(this),
                                this.onmessage.bind(this),
                                this.onclose.bind(this));
  }

  onopen(event) {
    this.modal.hide();
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
