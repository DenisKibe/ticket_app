$(document).ready(function() {
  $('.mdb-select').materialSelect();

  $('#userId').val(JSON.parse(sessionStorage.getItem('U')).data.user_id);


});
