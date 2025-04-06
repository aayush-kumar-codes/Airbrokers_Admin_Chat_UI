document.addEventListener('DOMContentLoaded', function () {
    const editorElements = document.querySelectorAll('.json-editor');
    editorElements.forEach(function (editorElement) {
        const initialJson = JSON.parse(editorElement.getAttribute('data-json'));
        const editor = new JSONEditor(editorElement, {
            mode: 'code',  
            onChangeJSON: function (newJson) {
                editorElement.setAttribute('data-json', JSON.stringify(newJson));
            }
        });
        editor.set(initialJson);
    });
});
