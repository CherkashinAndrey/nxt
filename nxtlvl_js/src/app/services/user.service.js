(function () {
  'use strict';

  angular.module('nxtlvl').service('UserService', UserService);

  /** @ngInject */
  function UserService() {
    var user = {
      name: 'Jane Hahn',
      title: 'Partner/cand.comm. & BA scient.pol. Virksomhedsrådgiver & certificeret coach',
      email: 'jane@nxtlvl.dk',
      mobile: '(+45) 12 34 56 78',
      company: 'NXT LVL',
      role: 'Leder',
      ownLeader: 'Navn Navnesen',
      type: 'Classic V1',
      firstDate: '20. Nov. 2001',
      middleDate: '25. Nov. 2001',
      lastDate: '20. Nov. 2002',
      status: 'Ansat',
      potencial: 'Ja',
      note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    };

    var service = {
      getUser: getUser,
      chooseRole: chooseRole,
      overwriteUser: overwriteUser
    };

    return service;

    function getUser() {
      return user;
    }

    function chooseRole(type) {
      console.log('type>>>>>>>>>>>>',type);
      user.role = type;
    }

    function overwriteUser(oldUser) {
      user = oldUser;
    }
  }

})();
