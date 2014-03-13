function ImageExplorerBlock(runtime, element) {
    /* reveal feedback action */
    $(element).find('.image-explorer-hotspot').bind('click', function(eventObj) {
      eventObj.preventDefault();
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
    });

    /* close feedback action */
    $(element).find('.image-explorer-close-reveal').bind('click', function(eventObj) {
      $(element).find('.image-explorer-hotspot-reveal').css('display', 'none');
      eventObj.preventDefault();
      eventObj.stopPropagation();
      close_hotspots(element);
    });
}
