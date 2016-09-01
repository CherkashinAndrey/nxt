(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('onChange', OnChange);

  /** @ngInject */
  function OnChange() {
    var directive = {
      link: linkFunc
    };

    return directive;

    /** @ngInject */
    function linkFunc(scope, element) {
	    element.bind('change', function() {
        	if($(element).hasClass('ng-not-empty')) {
            var prefs = ['-moz-range-thumb', '-webkit-slider-thumb', '-ms-thumb'];
            var scrollId = element[0].id;
            var sheet = document.createElement('style');
            document.body.appendChild(sheet);
            var style = '';
            prefs.map(function (pref) {
              style += 'input' + '#' + scrollId + '[type=range]::' + pref + ' { background: url(images/check-animated-8.gif?x=' + Math.random(1) + '); } ';
            });
            sheet.textContent = style;
      		}
	    });
	  };
  }

})();
