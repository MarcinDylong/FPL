$(document).ready(function () {
    var uls = $('li[data-username=pl-teams]').find('ul')
    var lis = $('li[data-username=pl-teams]').find('ul').find('li');
    
    if (uls.length === 1  ) {
        if (lis.length === 0) {
            alert('Database is empty\nBefore you download data to database some features may not work properly');
        };
    };

});