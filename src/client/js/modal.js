'use strict';

class Modal {
  constructor() {
    this.modal = $('#connect-modal');
    this.alert = $('#connect-error');
    this.submitbtn = $('#connect-submit');
  }

  show(error = false) {
    this.modal.modal({backdrop: 'static', keyboard: false});
    error ? this.showError() : this.hideError();
  }

  hide() {
    this.modal.modal('hide');
  }

  showError() {
    this.alert.show();
  }

  hideError() {
    this.alert.hide();
  }

  submit(callback) {
    this.submitbtn.click(() => {
      var ip = $('#server-ip').val();
      var name = $('#player-name').val();
      callback(ip, name);
    });
  }
}
