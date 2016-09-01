(function () {
  'use strict';

  angular.module('nxtlvl').service('InfoService', InfoService);

  /** @ngInject */
  function InfoService() {
    var infos = [
      {
        title: 'Forbedre mine styrker som leder (indsatsområde titel)',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '24. februar 2016',
        comments: [],
        check: false
      },
      {
        title: 'Indføre bedre arbejds-rutiner i min dagligdag',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '23. februar 2016',
        comments: [
          {
            author: 'Navn Navnsen',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          },
          {
            author: 'Jane Hahn',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          },
          {
            author: 'Navn Navnsen',
            text: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
            time: '11.22',
            date: '24.02.2016'
          }
        ],
        check: false
      },
      {
        title: 'Give bedre og mere feedback, både positivt og konstruktiv',
        info: 'Pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.',
        date: '22. februar 2016',
        comments: [],
        check: false
      }
    ];

    var service = {
      addComm: addComm,
      checkComm: checkComm,
      getInfo: getInfo,
      submitInfo: submitInfo
    };

    return service;

    function addComm(index, author, text) {
      return infos[index].comments.push({author: author, text: text, time: '11.22', date: '24.02.2016'});
    }

    function checkComm(index) {
      infos[index].check = !infos[index].check;
    }

    function getInfo() {
      return infos;
    }

    function submitInfo(title, info) {
      return infos.push({title: title, info: info, date: '22. februar 2016', comments: []});
    }
  }

})();
