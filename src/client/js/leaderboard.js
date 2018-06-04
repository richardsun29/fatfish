'use strict';

class Leaderboard {
  constructor(tbody) {
    this.tbody = tbody;
  }

  update(data) {
    var leaders = data.players.sort((a, b) => b.size - a.size);
    var html = leaders.map((p, i) => {
      return `<tr ${p.id == data.id ? 'class="table-primary"' : ''}>
        <td>${i+1}</td>
        <td>${p.name}</td>
        <td>${Math.floor(p.size)}</td>
      </tr>`;
    }).join('');
    this.tbody.html(html);
  }
}
