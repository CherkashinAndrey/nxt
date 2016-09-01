(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .service('translationService', translationService);

  /** @ngInject */
  function translationService($state, $localStorage, $rootScope, STATES, $http, translateService) {
    
    var service = {
      getTranslation: getTranslation
    };

    return service;

    function getTranslation(language) {
      var languageFilePath = 'translation_' + language + '.json';

      console.log('getTranslation',language,languageFilePath);

      $http.get("/app/translate/" + languageFilePath)
      .then(function(response) {
          translateService.addTextTranslate(response.data);
      });

    }

  }

})();
