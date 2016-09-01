(function () {
  'use strict';

  angular.module('nxtlvl').directive('fileReadImage', fileReadImage);

  /** @ngInject */
  function fileReadImage($q /*$base64*/) {
    var reader;
    var slice = Array.prototype.slice;
   /* var base64EncodedString;*/
    var decodedString;
    var temp,result;
    return {
        restrict: 'A',
        require: '?ngModel',

        link: function(scope, element, attrs, ngModel) {
         //   debugger
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
                       // scope.MedarbejdereAnsatCtrl.srcFile = file.name;
                       // console.log('uploadme--->>>',scope.MedarbejdereAnsatCtrl.uploadme);
                       scope.profileCtrl.photoInfo = {
                            name: file.name,
                            size: file.size,
                            type: file.type
                       };

                       console.log("photoInfo",scope.profileCtrl.photoInfo);

                        reader.onload = function(e) {
                            deferred.resolve(e.target.result);
                            temp = e.target.result;
                            
                            // "data:image/jpeg;base64"
                            console.log("Info",temp.split(",")[0]);

                            scope.profileCtrl.srcFile = temp;
                            //debugger
                            console.log('srcFile',scope.profileCtrl.srcFile);
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