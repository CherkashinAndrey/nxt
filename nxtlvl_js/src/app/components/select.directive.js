/*

(function() {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('select', select);

  /** @ngInject */
/*
  
  function select ($window) {
    var directive = {
      link: linkFunc
    };

    return directive;

    function linkFunc() {
      angular.element($window).bind('click', outsideClick);

      function outsideClick(e) {
      if (angular.element('.select-task-select').length) {
          var task = e.target;
          var show = false;

          if (angular.element(task).hasClass('center') || angular.element(task).hasClass('select-opener')) {
            var select = angular.element(task).parent().siblings('.select-options');
            if (angular.element(select[0]).hasClass('ng-show'))
              show = true;
          }

          var select_options = angular.element('.select-options');
          angular.element(select_options).each(function(){
            angular.element(this).removeClass('ng-show').addClass('ng-hide');
          });

          if (angular.element(task).hasClass('center') || angular.element(task).hasClass('select-opener')) {
            var select = angular.element(task).parent().siblings('.select-options');
            angular.element(select[0]).toggleClass('ng-hide ng-show');
            if (show) angular.element(select[0]).toggleClass('ng-hide ng-show');
          }
        }
      }
    }
  }
})();


*/