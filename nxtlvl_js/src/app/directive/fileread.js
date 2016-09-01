(function () {
  'use strict';

  angular.module('nxtlvl').directive('fileread', fileread);

  /** @ngInject */
  function fileread($q /*$base64*/) {
    var reader;
    var slice = Array.prototype.slice;
   /* var base64EncodedString;*/
    var decodedString;
    var temp,result;
    return {
        restrict: 'A',
        require: '?ngModel',

        link: function(scope, element, attrs, ngModel) {
                if (!ngModel) return;
                ngModel.$render = function() {};

                element.bind('change', function(e) {
                    var element = e.target;
                    console.log('e->',e);

                    $q.all(slice.call(element.files, 0).map(readFile))
                        .then(function(values) {
                            if (element.multiple) ngModel.$setViewValue(values);
                            else ngModel.$setViewValue(values.length ? values[0] : null);
                        });

                    function readFile(file) {
                        var deferred = $q.defer();
                        var reader = new FileReader();
                        scope.MedarbejdereAnsatCtrl.fileName = file.name;
                        console.log('uploadme--->>>',scope.MedarbejdereAnsatCtrl.uploadme);
                        reader.onload = function(e) {
                            console.log (e.target.result) ;
                            deferred.resolve(e.target.result);
                            temp = e.target.result;
                            scope.MedarbejdereAnsatCtrl.file = temp;
                        };
                        reader.onerror = function(e) {
                            console.log('file is not fiend' );
                            deferred.reject(e);
                        };
                        reader.readAsDataURL(file);

                        return deferred.promise;
                    }

                }); //change

            } //link
    }; //return
  }

})();