(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .directive('breadcrumbs', breadcrumbs);

  /** @ngInject */
  function breadcrumbs() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/directive/breadcrumbs.html',
      controller: breadcrumbsController,
      controllerAs: 'vm'
    };

    return directive;

    /** @ngInject */
    function breadcrumbsController($scope, $localStorage, MedarbejdereService) {
      var vm = this;
      vm.breadcrumbsArray = [];
      var lengthBr;
      var maxLength = 40;

      $scope.$on('breadcrumbsClick' , function(scope , e, user) {
        
        vm.user = user;
        vm.breadcrumbsArray.push({'user' : user, first_name_display : user.first_name == "" ? "udefined" : user.first_name , 
                                        last_name_display : user.last_name,
                                        display : true });

        console.log(' vm.breadcrumbsArray', vm.breadcrumbsArray);

        lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
            return prev += el.first_name_display.length + el.last_name_display.length;
        },0);

        console.log('lengthBr',lengthBr);

        if ( lengthBr >= maxLength ) {
          var itemNumber = 0;
          while ( lengthBr >= maxLength && ( itemNumber < vm.breadcrumbsArray.length -1 )) {

            if ( itemNumber >= 4) {
              vm.breadcrumbsArray[itemNumber].first_name_display = "...",
              vm.breadcrumbsArray[itemNumber].last_name_display = "",
              vm.breadcrumbsArray[itemNumber].display = false
            } else {

            vm.breadcrumbsArray[itemNumber].first_name_display = "...",
            vm.breadcrumbsArray[itemNumber].last_name_display = ""
            vm.breadcrumbsArray[itemNumber].display = true
            }
              itemNumber++;
            
            lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
              return prev += el.first_name_display.length + el.last_name_display.length;
            },0);
          }
        }
        console.log('leng',lengthBr);
      });



      vm.breadcrumbsPopArr = function () {
        vm.breadcrumbsArray.pop();
        console.log("length->", vm.breadcrumbsArray.length);
        console.log(' vm.breadcrumbsArray', vm.breadcrumbsArray);
       // debugger
        lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
            return prev += el.first_name_display.length + el.last_name_display.length;
        },0);

        if (vm.breadcrumbsArray.length <= 0) {
          console.log("ID localStorage",$localStorage.users.employee_id);
          MedarbejdereService.getUsersGet($localStorage.users.employee_id).then(
                function (result) {
                  console.log("groupeUser->",result);
                         $scope.medarbejdereCtrl.showGroup = true;      
                  return $scope.medarbejdereCtrl.groupeUser = result.data.employees;
                }
              ,function (error) {
                  console.log('error:',error);
              });
          return ;
        } else {
          //debugger
              console.log("groupeUserasdasdasdasdasdgroupeUserasdasdasdasdasd");
                          vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].first_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.first_name,
            vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].last_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.last_name    
          $scope.medarbejdereCtrl.onePerson = [vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user];
          if (vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].first_name_display == "...") {
            vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].first_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.first_name,
            vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].last_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.last_name           
          }
        }
        if (lengthBr <= maxLength) {
          var itemNumber = vm.breadcrumbsArray.length - 1;
          MedarbejdereService.getUsersGet(vm.breadcrumbsArray[itemNumber].user.id).then(
            function (result) {
              return $scope.medarbejdereCtrl.groupeUser = result.data.employees;
            }
          ,function (error) {
              console.log('error:',error);
          });
          while ( lengthBr <= maxLength && itemNumber >= 0 ) {
            if (vm.breadcrumbsArray[itemNumber].first_name_display == "...") {
              console.log("groupeUsedasd");
//          debugger
              
              vm.breadcrumbsArray[itemNumber].first_name_display = vm.breadcrumbsArray[itemNumber].user.first_name,
              vm.breadcrumbsArray[itemNumber].last_name_display = vm.breadcrumbsArray[itemNumber].user.last_name           
            }

              itemNumber--;
              lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
              return prev += el.first_name_display.length + el.last_name_display.length;
            },0);

          }
        } 
        console.log("ID localStorage",$localStorage.users.employee_id);
      }

      vm.breadcrumbsLink = function (user) {
        $scope.medarbejdereCtrl.onePerson = [user.user];
        MedarbejdereService.getUsersGet(user.user.id).then(
          function (result) {
            console.log("groupeUser->",result);
            return $scope.medarbejdereCtrl.groupeUser = result.data.employees;
          }
        ,function (error) {
            console.log('error:',error);
        });
        vm.breadcrumbsArray.forEach(function ( el, ind ) {
          if (el.user.id == user.user.id) {
            vm.breadcrumbsArray.splice(ind + 1);
          }   
        })

        if (vm.breadcrumbsArray.length <= 0) {
          console.log("ID localStorage",$localStorage.users.employee_id);
          MedarbejdereService.getUsersGet($localStorage.users.employee_id).then(
                function (result) {
                  console.log("groupeUser->",result);
                          $scope.medarbejdereCtrl.showGroup = true;      
                  return $scope.medarbejdereCtrl.groupeUser = result.data.employees;
                }
              ,function (error) {
                  console.log('error:',error);
              });
          return ;
        } else {
          if (vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].first_name_display == "...") {
            vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].first_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.first_name == "" ? "udefined" : vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.first_name,
            vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].last_name_display = vm.breadcrumbsArray[vm.breadcrumbsArray.length - 1].user.last_name           
          }
        }
        lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
            return prev += el.first_name_display.length + el.last_name_display.length;
        },0);
        
        if (lengthBr <= maxLength) {
          var itemNumber = vm.breadcrumbsArray.length - 1;
          while ( lengthBr <= maxLength && itemNumber >= 0 ) {
            if (vm.breadcrumbsArray[itemNumber].first_name_display == "...") {
              vm.breadcrumbsArray[itemNumber].first_name_display = vm.breadcrumbsArray[itemNumber].user.first_name == "" ? "udefined" : vm.breadcrumbsArray[itemNumber].user.first_name,
              vm.breadcrumbsArray[itemNumber].last_name_display = vm.breadcrumbsArray[itemNumber].user.last_name           
            }
              itemNumber--;
              lengthBr = vm.breadcrumbsArray.reduce(function (prev, el) {
              return prev += el.first_name_display.length + el.last_name_display.length;
            },0);
          }
        } 
        console.log('userURL', user);
      }




    }
  }

})();
