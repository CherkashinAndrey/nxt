(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('localization', localization);

  /** @ngInject */
  function localization() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/localization.directive.html',
      replace:true,
      controller: localizationController,
      controllerAs: 'mv',
      bindToController: false
    };

    return directive;

    /** @ngInject */

    function localizationController(translationService) {
      var mv = this;
      mv.selectedLanguage = "da";
      translationService.getTranslation(mv.selectedLanguage);

      mv.translate = function () {
       
        translationService.getTranslation(mv.selectedLanguage);
      }

    }
  }
})();