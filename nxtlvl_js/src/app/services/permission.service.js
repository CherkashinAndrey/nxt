(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .service('permissionService', permissionService);

  /** @ngInject */
  function permissionService($state, $localStorage, $rootScope, STATES) {
    
    var service = {
      init: init
    };

    return service;

    function init(event, toState, toParams, fromState) {

      var requiredState = '';
      var isStateAccessable = false;
        if ( !$localStorage.users && toState.name !== "login" && fromState.url == "^") {
          requiredState = 'login';
          event.preventDefault();
          $state.go(requiredState); 
          return;
        } 
        else {

          if ( toState.name !== STATES[0] ) {
            if (toState.data.roles.find(
              function (el) {
                return el == $localStorage.users.role;
              })) 
            {
              requiredState = toState.name;
              isStateAccessable = true;
            }
          }

          if (!isStateAccessable) {
              requiredState = 'login';
            
            if ($localStorage.lastUserStateName == requiredState) {
              return;
            }
            $localStorage['lastUserStateName'] = requiredState;
            event.preventDefault();
            $state.go(requiredState); 
          }
    }
  }

  }

})();
