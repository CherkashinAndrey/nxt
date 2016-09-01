(function () {
  'use strict';

  angular.module('nxtlvl').service('translateService', translateService);

  /** @ngInject */
  function translateService() {
    var service = {
      getTextTranslate: getTextTranslate,
      addTextTranslate: addTextTranslate
    };
    var translatePage = {};

    return service;


    function getTextTranslate(newDutie) {
      return translatePage
    }

    function addTextTranslate(text) {
      console.log(text.medarbejdere.TITLE);

      Object.keys(translatePage).forEach( function(el) {
        delete translatePage[el];
      })

      translatePage = Object.assign(translatePage, {
          "medarbejdere":
          {
              "TITLE" : text.medarbejdere.TITLE,
              "BATTON_EMPLOEE" : text.medarbejdere.BATTON_EMPLOEE,
              "BATTON_PREPARATION" : text.medarbejdere.BATTON_PREPARATION,
              "PLACEHOLDER_MED" : text.medarbejdere.PLACEHOLDER_MED
          },
          "velkommen":
          {
              "NAME" : text.velkommen.NAME
          }


      })
    }
  }

})();
