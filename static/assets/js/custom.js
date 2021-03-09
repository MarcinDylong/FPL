$(document).ready(function () {

    // Return alert about empty database each time user enter the site with 
    // navigation 
    var uls = $('li[data-username=pl-teams]').find('ul')
    var lis = $('li[data-username=pl-teams]').find('ul').find('li');
    if (uls.length === 1  ) {
        if (lis.length === 0) {
            alert('Database is empty\nBefore you download data to database some features may not work properly');
        };
    };

    // Hover text on mouseenter
    var textDict = {
        "currBest": "Players with best performance on current Gameweek,",
        "allBest": "Players with best performance througn entire season.",
        "mostIn": "This gameweek's most-bought players.",
        "mostOut": "This gameweek's most-sold players.",
        "plAvl": "Injuries, suspensions, unavailabilities",
        "mostPop": "Most popular choices of players by managers.",
        "bonSeason": "Players with most bonus points throughout the Season.",
        "yourTeam": "Player from your Team",
        "betterThan": "You are better than this % of Managers.",
        "upArrow": "Better than previous gameweek",
        "nullArrow": "The sama as previous gameweek",
        "downArrow": "Worse than previous gameweek",
        "noveltyExplain": "Base on popularity of players from your team\nThe lower the more original your team is."
    }

    $(".toolTip").hover(function () {
        var text = $(this).data('value')
        $(this).css('cursor','pointer').attr('title', textDict[text]);
    }, function() {
        $(this).css('cursor','auto');
    });

});