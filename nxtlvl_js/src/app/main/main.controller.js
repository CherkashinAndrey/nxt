(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($rootScope) {
    $rootScope.$on('$stateChangeSuccess', function() {
      document.body.scrollTop = document.documentElement.scrollTop = 0;
    });
  }
})();
