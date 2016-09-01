(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('ChooseUserController', ChooseUserController);

  /** @ngInject */
  function ChooseUserController($cookies, UserService) {
    var vm = this;

    vm.ChooseUser = function (type) {
      $cookies.put('userType', type);
      UserService.chooseRole(type);
    };
  }

})();
