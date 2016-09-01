(function () {
  'use strict';
  var  host;
  if (location.host == "localhost:3000") {
    host = "http://nxtlvl-dev-8000.chisw.us";
  } 

  if (location.host == "enso-dev.chisw.us") {
    host = "http://enso-dev-8000.chisw.us";
  } 

  if (location.host == "nxtlvl-dev.chisw.us") {
    host = "http://nxtlvl-dev-8000.chisw.us";
  }
  
  angular
    .module('nxtlvl')
    .constant('KeyCode', {
      keyUp: 38,
      keyDown: 40,
      keyEnter: 13
    })
  .constant('ADMINS', ['admin'])
  .constant('LEADERS', ['admin', 'leader'])
  .constant('USERS', ['admin', 'leader', 'user'])
  .constant('STATES', ['login','resetpassword','changepassword','admin','leader','user'])
  .constant('ROLES', ['admin', 'leader', 'manager', 'user'])
  .constant('CLASS', ['A','B','C'])
  .constant('URL_SERV', host);  //'http://nxtlvl-dev-8000.chisw.us' //http://enso-dev-8000.chisw.us

})();
