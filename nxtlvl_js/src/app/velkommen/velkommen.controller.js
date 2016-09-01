(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .controller('VelkommenController', VelkommenController);

  /** @ngInject */
  function VelkommenController(translateService) {
    var vm = this;

    vm.translate = translateService.getTextTranslate();
    console.log("222222222222",vm.translate);

  }

})();
