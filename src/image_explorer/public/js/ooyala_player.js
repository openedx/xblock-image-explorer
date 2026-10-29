$(function(){
    // create Ooyala videos 
    $('.ooyala-element').each(function(){
        OO.Player.create(this.id, $(this).data('video-id')); 
    });
});
