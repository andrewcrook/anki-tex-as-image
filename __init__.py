import json
import os.path

from anki.hooks import runHook, wrap
from anki.latex import render_latex
from aqt import gui_hooks, mw
from aqt.editor import Editor, EditorWebView
from aqt.webview import WebContent
from aqt.qt import *

from .from_file import str_from_file_name


def note_loaded(editor):
    note = editor.note
    items = editor.note.items()
    model = editor.note.model()
    col = editor.note.col
    fldContentTexProcessed = [
        editor.mw.col.media.escapeImages(
            render_latex(val, model, col))
        for fld, val in items
    ]
    dumped = json.dumps(fldContentTexProcessed)
    editor.web.eval(f"""set_texs({dumped});""")


gui_hooks.editor_did_load_note.append(note_loaded)

def onBridgeCmd(handled, message, context):
    if isinstance(context, Editor) and message.startswith("blur"):
        (type, ord, txt) = message.split(":", 2)
        val = context.note.fields[int(ord)]
        fldContent = context.mw.col.media.escapeImages(val)
        fldContentTexProcessed = context.mw.col.media.escapeImages(
            render_latex(val, context.note.model(), context.note.col))
        context.web.eval(
            f"set_field({ord}, {json.dumps(fldContent)}, {json.dumps(fldContentTexProcessed)});")
    # Handling does not actually change. Actual work for blur must still be done
    return handled


gui_hooks.webview_did_receive_js_message.append(onBridgeCmd)
mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def on_webview_will_set_content(web_content: WebContent, context):
    if isinstance(context, Editor):
        addon_package = mw.addonManager.addonFromModule(__name__)
        s = f"/_addons/{addon_package}/web/js.js"
        web_content.js.append(s)


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
