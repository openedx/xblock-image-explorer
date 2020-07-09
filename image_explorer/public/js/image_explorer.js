function applyHotspotButtonStyle(element, data) {
   $(".image-explorer-wrapper button.image-explorer-hotspot", element).css("background", "url("+data['hotspot_image']+") no-repeat scroll 0 0 rgba(0, 0, 0, 0)");
}

function ImageExplorerBlock(runtime, element, data) {

    if (data['authoring_view'] === 'true') {
        applyHotspotButtonStyle(element, data);
    }
    var hotspot_opened_at = null;
    var active_feedback = null;
    // Holds a reference to YouTube API Player objects.
    var video_players = {};

    function publish_event(data) {
      $.ajax({
          type: "POST",
          url: runtime.handlerUrl(element, 'publish_event'),
          data: JSON.stringify(data)
      });
    }

    function setRevealPosition(target, reveal) {
      var reveal_side = reveal.data('side');
      var reveal_width = reveal.outerWidth();
      var target_position_left = target.position().left;
      var hotspot_image_width = target.outerWidth();

      var image_width = reveal.prev('.image-explorer-hotspot').siblings('.image-explorer-background').outerWidth();

      if (reveal_side !== 'left' && reveal_side !== 'right') {
          /* do some calculations with regards which side of the hotspot to open the feedback on */
          if ((target_position_left + reveal_width > image_width) &&
              (target_position_left - reveal_width - hotspot_image_width > 0)) {
              reveal_side = 'left';
          }
          else {
              reveal_side = 'right';
          }
      }
      if (reveal_side === 'left') {
          reveal.css('margin-left', '-' + (reveal_width + hotspot_image_width) + 'px');
      }
    }

    /* reveal feedback action */
    $(element).find('.image-explorer-hotspot').on('click', function(eventObj) {
      if (eventObj.target != this)
        return; // User clicked on the feedback popup, which is a child of the hotspot.
      eventObj.stopPropagation();

      if (active_feedback) {
        close_feedback();
      }
      $(this).addClass('visited');
      var target = $(eventObj.currentTarget);
      var reveal = target.next('.image-explorer-hotspot-reveal');

      setRevealPosition(target, reveal);

      reveal.css('display', 'block');
      reveal.focus();
      active_feedback = reveal;
      feedback_open();
      $(this).trigger('feedback:open');
      hotspot_opened_at = new Date().getTime();
      publish_event({
              event_type:'xblock.image-explorer.hotspot.opened',
              item_id: target.parent('.hotspot-container').data('item-id')
      });
    });
  
  function pauseVideos(hotspot){
    // pause any videos playing in this hotspot
    pauseYoutubeVideos(hotspot);
    pauseOoyalaVideos(hotspot);
    pauseBrightcoveVideos(hotspot);
  }

  function pauseBrightcoveVideos(hotspot){
    hotspot.find('.video-js').each(function(){
      videojs.getPlayer(this.id).pause();
    });
  }

  function pauseOoyalaVideos(hotspot){
    hotspot.find('.oo-player-container').each(function(){
      OO.Player.create(this.id).pause();
    });
  }

  function pauseYoutubeVideos(hotspot) {
    hotspot.find('.youtube-player').each(function() {
      var pauseVideo = function(player) {
        player.pauseVideo();
      };

      if (!video_players[this.id]) {
        // YouTube API does not allow creating multiple YT.Player instances
        // for the same video iframe, so store the reference to the new YT.Player
        // for future use.
        video_players[this.id] = new YT.Player(this.id, {
          events: {
            onReady: function(evt) {
              pauseVideo(evt.target);
            }
          }
        });
      }

      // YT.Player objects take some time to initialize. Before the player is ready,
      // all API methods will throw an error, so try to pause the video, but ignore errors.
      // If YT.Player is not ready at this time, it will be paused in the onReady callback.
      try {
        pauseVideo(video_players[this.id]);
      } catch (e) {}
    });
  }

  function createOoyalaVideos(hotspot){
    // matches pattern OO.Player.create('element_id', video_id);
    var OOregex = /OO.Player.create\(['\"]\w+['\"],['\"][\w+-]+['\"]\)/;

    // Ooyala videos needs to be created on hotspot open
    hotspot.find('script').each(function(){
      if(this.text != '' && this.text.indexOf('OO.Player.create') != -1){
        var script = this.text.replace(/ /g, '');
        // use regex to extract video creation code
        var match = OOregex.exec(script);
        if(match.length > 0){
          eval(match[0]);
        }
      }
    });
  }

  /* open feedback action */
  function feedback_open(){
    var hotspot = active_feedback.closest('.hotspot-container');
    createOoyalaVideos(hotspot);
  }

    /* close feedback action */
    function close_feedback() {
      // Close the visible feedback popup
      var hotspot = active_feedback.closest('.hotspot-container');
      pauseVideos(hotspot);
      hotspot.trigger('feedback:close');
      active_feedback.css('display', 'none');
      var duration = new Date().getTime() - hotspot_opened_at;
      publish_event({
              event_type:'xblock.image-explorer.hotspot.closed',
              item_id: hotspot.data('item-id'),
              duration: String(duration)
      });
      active_feedback = null;
      //Moving focus back to parent hotspot
      $(hotspot).find('.image-explorer-hotspot').focus();
    }

    $(document).on('click', function(eventObj) {
      if (!active_feedback)
        return;
      var target = $(eventObj.target);
      var close_btn = ".image-explorer-close-reveal";
      var clicked_outside_feedback = (target.closest('.image-explorer-hotspot-reveal').length === 0);
      if (target.is(close_btn) || clicked_outside_feedback) {
        close_feedback();
        eventObj.preventDefault();
        eventObj.stopPropagation();
      }
    });

    publish_event({
        event_type:'xblock.image-explorer.loaded'
    });
}
