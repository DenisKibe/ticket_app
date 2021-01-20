$(document).ready(function() {

  // SideNav Initialization
  $(".button-collapse").sideNav();

    var container = document.querySelector('.custom-scrollbar');
    var ps = new PerfectScrollbar(container, {
    wheelSpeed: 2,
    wheelPropagation: true,
    minScrollbarLength: 20
  });

  $('.mdb-select').materialSelect();

  //logout script
  $('#logoutbtn').click(function(){
    sessionStorage.clear();
    document.cookie="session; expires="+new Date(0);
    window.location="/";
  })

  
});
