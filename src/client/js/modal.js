'use strict';

class Modal {
  constructor() {
    this.modal = $('#connect-modal');
    this.alert = $('#connect-error');
    this.form = $('#connect-form');
  }

  show(error) {
    this.modal.modal({backdrop: 'static', keyboard: false});
    error ? this.showError(error) : this.hideError();
  }

  hide() {
    this.modal.modal('hide');
  }

  showError(error) {
    this.alert.text(error);
    this.alert.show();
  }

  hideError() {
    this.alert.hide();
  }

  submit(callback) {
    this.form.submit(() => {
      var ip = $('#server-ip').val();
      var name = $('#player-name').val();
      callback(ip, name);
      return false;
    });
  }
}
