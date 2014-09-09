function ImageExplorerBlock(runtime, element) {

    var hotspot_opened_at = null;

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

      var image_width = reveal.parents('.image-explorer-hotspot').siblings('.image-explorer-background').outerWidth();

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
    $(element).find('.image-explorer-hotspot').bind('click', function(eventObj) {
      eventObj.preventDefault();
      eventObj.stopPropagation();
      $(element).find('.image-explorer-hotspot-reveal').css('display', 'none');

      var target = $(eventObj.currentTarget);
      var reveal = target.find('.image-explorer-hotspot-reveal');

      setRevealPosition(target, reveal);

      reveal.css('display', 'block');
      hotspot_opened_at = new Date().getTime();
      publish_event({
              event_type:'xblock.image-explorer.hotspot.opened',
              item_id: target.data('item-id')
      });
    });

    /* close feedback action */
    $(element).find('.image-explorer-close-reveal').bind('click', function(eventObj) {
      $(element).find('.image-explorer-hotspot-reveal').css('display', 'none');
      eventObj.preventDefault();
      eventObj.stopPropagation();
      var hotspot = $(eventObj.currentTarget).closest('.image-explorer-hotspot');
      var duration = new Date().getTime() - hotspot_opened_at;
      publish_event({
              event_type:'xblock.image-explorer.hotspot.closed',
              item_id: hotspot.data('item-id'),
              duration: String(duration)
      });
    });

    publish_event({
        event_type:'xblock.image-explorer.loaded'
    });
}
