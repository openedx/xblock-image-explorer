function ImageExplorerEditBlock(runtime, element) {
    var xmlEditorTextarea = $('.block-xml-editor', element),
        xmlEditor = CodeMirror.fromTextArea(xmlEditorTextarea[0], { mode: 'xml' });

    $(element).find('.save-button').bind('click', function() {
        var data = {
            'display_name': $(element).find('.edit-display-name').val(),
            'data': xmlEditor.getValue(),
        };
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            window.location.reload(false);
        });
    });
}
