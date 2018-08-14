$(function(){
    $('#ooyalaplayer_2').closest('.image-explorer-hotspot').on('feedback:open', function (evt) {
        var video_id = $('#ooyalaplayer_2').data("video-id")
        OO.Player.create('ooyalaplayer_2', video_id);
    }).on('feedback:close', function (evt) {
        OO.Player.create('ooyalaplayer_2').pause();
    });
});
