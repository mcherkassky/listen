function startMarquee() {
    
    var menuItemWidth = $(this).width();
    var listItemWidth = $(this).parent().width();
    
    if(menuItemWidth > listItemWidth) {
        var scrollDistance = menuItemWidth - listItemWidth;
        var listItem = $(this).parent();
        // Stop any current animation
        listItem.stop();
        
        // Start animating the left scroll position over 3 seconds, using a smooth linear motion
        listItem.animate({scrollLeft: scrollDistance}, 3000, 'linear');
    }
    console.log('start marquee');

}

function stopMarquee() {
    var listItem = $(this).parent();
    
    // Stop any current animation
    listItem.stop();
    
    // Start animating the left scroll position quickly, with a bit of a swing to the animation.
    // This will make the item seem to 'whip' back to it's starting point
    listItem.animate({scrollLeft: 0}, 'medium', 'swing');

}

// hover() calls the first function when mousing over the element, and the second function when mousing out of it
