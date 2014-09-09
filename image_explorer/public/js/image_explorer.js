function ImageExplorerBlock(runtime, element) {

    var hotspot_opened_at = null;
    var active_feedback = null;

    function publish_event(data) {
      $.ajax({
          type: "POST",
          url: runtime.handlerUrl(element, 'publish_event'),
          data: JSON.stringify(data)
      });
    }

    /* reveal feedback action */
    $(element).find('.image-explorer-hotspot').on('click', function(eventObj) {
      eventObj.preventDefault();
      if (eventObj.target != this)
        return; // User clicked on the feedback popup, which is a child of the hotspot.
      eventObj.stopPropagation();
      $(element).find('.image-explorer-hotspot-reveal').css('display', 'none');

      var target = $(eventObj.currentTarget);
      var target_position_left = target.position().left;
      var hotspot_image_width = target.outerWidth();
      var reveal = target.find('.image-explorer-hotspot-reveal');
      var reveal_width = reveal.outerWidth();
      var parent_wrapper = reveal.parents('.image-explorer-hotspot');
      var image_element = parent_wrapper.siblings('.image-explorer-background');
      var image_width = image_element.outerWidth();

      /* do some calculations with regards which side of the hotspot to open the feedback on */
      if ((target_position_left + reveal_width > image_width) && (target_position_left - reveal_width - hotspot_image_width > 0)) {
        reveal.css('margin-left', '-' + (reveal_width + hotspot_image_width) + 'px');
      }
      reveal.css('display', 'block');
      active_feedback = reveal;
      hotspot_opened_at = new Date().getTime();
      publish_event({
              event_type:'xblock.image-explorer.hotspot.opened',
              item_id: target.data('item-id')
      });
    });

    /* close feedback action */
    function close_feedback() {
      // Close the visible feedback popup
      active_feedback.css('display', 'none');
      var hotspot = active_feedback.closest('.image-explorer-hotspot');
      var duration = new Date().getTime() - hotspot_opened_at;
      publish_event({
              event_type:'xblock.image-explorer.hotspot.closed',
              item_id: hotspot.data('item-id'),
              duration: String(duration)
      });
      active_feedback = null;
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
