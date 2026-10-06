import shutil
import subprocess
import sys

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets._select import SelectCurrent
from textual.widgets import (
    Button,
    Label,
    Markdown,
    ProgressBar,
    Rule,
    Select,
    SelectionList,
    Static,
    TextArea,
)

from honemsg.controllers.ollama_chat import OllamaChat

MESSAGE_TYPES = [
    ("Slack message", "slack_message"),
    ("Commit message", "commit_message"),
    ("Documentation", "documentation"),
    ("Email", "email"),
    ("Investigation", "investigation"),
    ("Pull request description", "pull_request_description"),
    ("Status update", "status_update"),
    ("Customer response", "support_response"),
]

MESSAGE_LANGUAGES = [
    ("English", "en"),
    ("Español", "es"),
]

MESSAGE_ACTIONS = [
    ("Improve", "improve"),
    ("Shorten", "shorten"),
    ("Simplify", "simplify"),
    ("Summarize", "summarize"),
    ("Translate", "translate"),
]


def copy_to_system_clipboard(text: str) -> bool:
    if sys.platform == "darwin":
        commands = [["pbcopy"]]
    elif sys.platform == "win32":
        commands = [["clip"]]
    else:
        commands = [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]

    for command in commands:
        if shutil.which(command[0]):
            try:
                subprocess.run(command, input=text.encode("utf-8"), check=True)
                return True
            except (OSError, subprocess.CalledProcessError):
                continue
    return False


class HonemsgView(Static):

    def compose(self) -> ComposeResult:
        with Horizontal(classes="section"):

            with Vertical(classes="column" ):
                yield Label("MESSAGE EDITOR", classes="section_title")

                with Vertical(id="message_editor_column_content"):
                    with Horizontal(id="message_editor_type_actions"):
                        with Vertical():
                            yield Select(MESSAGE_TYPES, id="message_type", prompt="Select message type", value="slack_message")
                            yield Select(MESSAGE_LANGUAGES, id="message_language", prompt="Select language", value="en")
                        yield SelectionList(*MESSAGE_ACTIONS, id="message_actions")

                    yield TextArea(language="markdown", id="message_input")

                with Horizontal(id="action_buttons_container"):
                    yield Button("APPLY →", variant="primary", flat=True, classes="button", id="message_improve_button")
                    yield Button("CLEAR FORM", variant="primary", flat=True, classes="button", id="clear_form_btn")

            yield Rule.vertical(line_style="heavy")

            with Vertical(classes="column"):
                yield Label("SUGGESTIONS", classes="section_title")
                yield ProgressBar(show_bar=True, clock=None, show_eta=False, show_percentage=False, id="suggestions_progress_bar")

                with VerticalScroll(id="suggestions_scroll"):
                    yield Markdown( id="suggestions_output")
                with Horizontal(classes="suggestions_buttons_container"):
                    yield Button("COPY", variant="primary", flat=True, classes="button", id="copy_suggestion_btn")
                    yield Button("CLEAR CHAT CONTEXT", variant="primary",classes="button", id="clear_chat_context_btn", flat=True)


    def on_mount(self) -> None:
        self.message_type = self.query_one("#message_type", Select)
        self.message_language = self.query_one("#message_language", Select)
        self.message_input = self.query_one("#message_input", TextArea)
        self.message_actions = self.query_one("#message_actions", SelectionList)
        self.message_improve_button = self.query_one("#message_improve_button", Button)
        self.suggestions_progress_bar = self.query_one("#suggestions_progress_bar", ProgressBar)
        self.suggestions_output = self.query_one("#suggestions_output", Markdown)

        # Select draws its border on its inner SelectCurrent, so the title goes there
        self.message_type.query_one(SelectCurrent).border_title = "Message type"
        self.message_language.query_one(SelectCurrent).border_title = "Language"
        self.message_actions.border_title = "Actions"
        self.message_input.border_title = "Text"

        self.suggestion_text = ""
        self.ollamaChat = OllamaChat()

    @on(Button.Pressed, "#message_improve_button")
    def on_improve_message(self) -> None:
        if self.message_type.value is Select.NULL:
            self.notify("Please select a message type before continuing.", severity="warning")
            return

        if self.message_language.value is Select.NULL:
            self.notify("Please select a language before continuing.", severity="warning")
            return

        if not self.message_input.text:
            self.notify("Please add a message to improve.", severity="warning")
            return

        if self.message_input.text:
            self.suggestions_output.update(markdown="")
            self.suggestion_text = ""
            self.generate_suggestions()

    @on(Button.Pressed, "#clear_form_btn")
    def on_clear_form(self) -> None:
        self.message_type.value = "slack_message"
        self.message_language.value = "en"
        self.message_actions.deselect_all()
        self.message_input.clear()

    @on(Button.Pressed, "#clear_chat_context_btn")
    def on_clear_chat_context(self) -> None:
        self.suggestions_output.update(markdown="")
        self.suggestion_text = ""
        self.notify("Chat context cleared.", severity="information")

    @on(Button.Pressed, "#copy_suggestion_btn")
    def on_copy_suggestion(self) -> None:
        if not self.suggestion_text:
            self.notify("There is no suggestion to copy yet.", severity="warning")
            return

        # OSC 52 only works in terminals that support it, so also try the native clipboard tool
        self.app.copy_to_clipboard(self.suggestion_text)
        copy_to_system_clipboard(self.suggestion_text)
        self.notify("Suggestion copied to clipboard.", severity="information")

    @work(thread=True)
    def generate_suggestions(self):
        self.app.call_from_thread(self.toggle_progress_bar, True)
        message = self.ollamaChat.send_message_to_ollama(self.message_type.value, self.message_language.value, self.message_actions.selected, self.message_input.text)
        self.suggestion_text = message
        self.app.call_from_thread(self.suggestions_output.append, f"{message}")
        self.app.call_from_thread(self.toggle_progress_bar, False)

    def toggle_progress_bar(self, visible):
        self.suggestions_progress_bar.display = "block" if visible else "none"
