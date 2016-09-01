(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('LoginController', LoginController);

  /** @ngInject */
  function LoginController(LoginService) {
    var vm = this;
    vm.invalidForm = false;
    vm.emailPattern = '\\w+.?\\w+@[a-zA-Z_]+?\\.[a-zA-Z]{2,6}';

    var login = {};
     // vm.login = " ";
     // vm.passw = "";

    vm.signin = function (valid, e) {
      console.log('controllerLogin->', vm.login, vm.passw);

      login = {
        "email": vm.login,
        "password": vm.passw
      }
     // debugger
      if ( valid ) {
        vm.invalidForm = true;
        angular.element(e.target).addClass('form-error');
        return;
      }
      angular.element(e.target).removeClass('form-error');
      //LoginService.userLogin(login, angular.element(e.target))
      LoginService.postLogin(login)
    }

    vm.activeRow = function(e) {
      angular.element(e.target).closest('.input-row').addClass("active-row");
    }

    vm.noActiveRow = function (e) {
      if (angular.element(e)[0].target.value.length < 1) {
        angular.element(e.target).closest('.input-row').removeClass("active-row");
      }
    }

    vm.isInvalid = function(element) {
      //debugger
      return element.$invalid && element.$dirty || element.$invalid && vm.invalidForm
    }

  }

})();