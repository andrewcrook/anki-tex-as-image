var original_fields = [];

function on_focus_tex(event) {
    /*
       Called when focus is set to the field `elem`.

       If the field is not changed, nothing occurs.
       Otherwise, set currentField value, warns python of it.
       Change buttons.
       If the change is note made by mouse, then move caret to end of field, and move the window to show the field.

    */
    elem = event.target;
    var previousCurrentField = currentField;
    currentField = elem;
    var ord = currentFieldOrdinal()
    var field = original_fields[ord];
    if (field !== null) {
        elem.innerHTML = field;
        original_fields[ord] = null;
    }
}

function current_field_ordinal_aux() {
    if (currentField) {
        return currentField.id.substring(1);
    } else {
        return null;
    }
}

function set_field(ord, fieldValue, fieldValueTexProcessed) {
    var currentOrd = current_field_ordinal_aux();
    if (currentOrd == ord) {
        return;
    }
    if (!fieldValue) {
        fieldValue = "<br>";
    }
    original_fields[ord] = fieldValue;
    if (!fieldValueTexProcessed) {
        fieldValueTexProcessed = "<br>";
    }
    field = $("#f"+ord);
    field.html(fieldValueTexProcessed);

}

function set_texs(tex){
    nb_fields = tex.length;
    original_fields = new Array(nb_fields);
    var i;
    for (i = 0; i < nb_fields; i++) {
        fieldValue = tex[i];
        if (fieldValue === "") {
            fieldValue = "<br>";
        }
        $div = $("#f" + i);
        original_fields[i] = $div.html();
        $div.html(fieldValue);
        $div.focus(on_focus_tex);
    }
}