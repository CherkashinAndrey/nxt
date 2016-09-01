(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('asideNav', asideNav);

  /** @ngInject */
  function asideNav() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/aside-navigation.directive.html',
      replace:true,
      controller: asideNavController,
      controllerAs: 'vm'
    };

    return directive;

    /** @ngInject */
    function asideNavController($scope, UserService, $state, $localStorage, LoginService) {
      var vm = this;
      vm.type = $localStorage.usersManager.is_manager//$localStorage.users.is_manager;//UserService.getUser().role;
     // console.log('!!!!!!!!!!', $localStorage.users.role);

      $scope.logOut = function () {
        $localStorage.$reset();
        LoginService.logOut();
        $state.go('login');
      }
    }
  }

})();
