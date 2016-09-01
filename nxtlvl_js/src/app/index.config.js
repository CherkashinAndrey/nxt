(function() {
  'use strict';

  angular
    .module('nxtlvl')
    .config(config);

  /** @ngInject */
  function config($logProvider, toastrConfig, $httpProvider, cfpLoadingBarProvider) {
    // Enable log

   // cfpLoadingBarProvider.spinnerTemplate = '<div><span class="fa fa-spinner">Custom Loading Message...</div>';

    $logProvider.debugEnabled(true);

    // Set options third-party lib
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
   // toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;

    $httpProvider.defaults.withCredentials = true;
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    
    //$httpProvider.defaults.stripTrailingSlashes = false;

  }

})();
