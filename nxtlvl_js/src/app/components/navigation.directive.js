(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('headerNav', headerNav);

  /** @ngInject */
  function headerNav($state) {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navigation.directive.html',
      replace:true,
      controller: headerNavController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */

    function headerNavController(UserService) {
     // var vm = this;
      vm.selectedLanguage = "en";
     //UserService.getUser().role;
    }
  }
});
