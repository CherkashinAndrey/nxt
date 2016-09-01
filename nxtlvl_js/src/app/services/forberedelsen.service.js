(function () {
  'use strict';

  angular.module('nxtlvl').service('ForberedelsenService', ForberedelsenService);

  /** @ngInject */
  function ForberedelsenService($http, URL_SERV, $state) {
    var duties = {duties: []};
    var autocomplits = ['Lorem', 'Lorem ipsum', 'Lorem ipsum dolor', 'Lorem ipsum dolor sit', 'Lorem ipsum dolor sit amet'];
    var date = ['24. februar 2016', '12. april 2015', '2. april 2015'];
    var box1 = ['Kendt', 'Ukendt', 'Nyt'];
    var box2 = ['Let', 'Middel', 'Svær'];

    var service = {
      addDutie: addDutie,
      getDuties: getDuties,
      getDate: getDate,
      getAutocomplit: getAutocomplit,
      selectComplaxity: selectComplaxity,
      changeLevel: changeLevel,
      changeComplexity: changeComplexity,
      levelChange: levelChange,
      removeDutie: removeDutie,
      reciveBox1: reciveBox1,
      reciveBox2: reciveBox2,
      overwriteDuties: overwriteDuties,
      getActiveDevPlan: getActiveDevPlan,
      getAllDevPlan: getAllDevPlan,
      getDevPlanCreate:getDevPlanCreate,
      getAllCompetence: getAllCompetence,
      getAllEmployees: getAllEmployees
    };

    return service;

    function getActiveDevPlan () {
      console.log( URL_SERV + "/employee_active_development_plan/");
      return $http({
                    method: 'GET',
                    url: URL_SERV + "/employee_active_development_plan/",
                    xhrFields: {
                      withCredentials: true
                    }
                  });
    }

    function getAllDevPlan () {
      console.log( URL_SERV + "/employee_all_development_plans/");
      return $http({
                    method: 'GET',
                    url: URL_SERV + "/employee_all_development_plans/",
                    xhrFields: {
                      withCredentials: true
                    }
                  });
    }
    function getDevPlanCreate () {
      console.log( URL_SERV + "/development_plan/create/");
        return $http({
          method: 'GET',
          url: URL_SERV + "/development_plan/create/",
          xhrFields: {
            withCredentials: true
          }
        });     
    }

    function getAllCompetence () {
      console.log( URL_SERV + "/all_competence/");
        return $http({
          method: 'GET',
          url: URL_SERV + "/all_competence/",
          xhrFields: {
            withCredentials: true
          }
        });     
    }

    function getAllEmployees () {
      console.log( URL_SERV + "/employees/all/");
        return $http({
          method: 'GET',
          url: URL_SERV + "/employees/all/",
          xhrFields: {
            withCredentials: true
          }
        });     
    }

    function addDutie (newDutie) {
      duties.duties.push({name: newDutie, level: '', complexity: ''});
    }

    function getDuties() {
      return duties;
    }

    function getDate() {
      return date;
    }

    function getAutocomplit() {
      return autocomplits;
    }

    function selectComplaxity (i, complaxity) {
      duties.duties[i].complexity = complaxity;
    }

    function changeLevel (i, level) {
      duties.duties[i].level = level;
    }

    function changeComplexity (index, value) {
      duties.duties[index].complexity = value;
    }

    function levelChange (index, value) {
      duties.duties[index].level = value;
    }

    function removeDutie (index) {
      duties.duties.splice(index, 1);
    }

    function reciveBox1 () {
      return box1;
    }

    function reciveBox2 () {
      return box2;
    }

    function overwriteDuties (oldDuties) {
      duties.duties = oldDuties;
    }

  }

})();
