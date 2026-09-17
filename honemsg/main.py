
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Header,
    Label,
    Markdown,
    ProgressBar,
    Rule,
    Select,
    SelectionList,
    TextArea,
)

from honemsg.controllers.ollama_chat import send_message_to_ollama

MESSAGE_TYPES = [
    ("Slack message", "slack_message"),
    ("Email", "email"),
    ("Investigation", "investigation"),
    ("Pull request description", "pull_request_description"),
    ("Status update", "status_update"),
    ("Customer response", "support_response"),
]

MESSAGE_ACTIONS = [
    ("Improve", "improve"),
    ("Shorten", "shorten"),
    ("Simplify", "simplify"),
    ("Fix grammar & spelling", "fix_grammar"),
    ("Summarize", "summarize"),
]

class HonemsgApp(App):

    DEFAULT_CSS = """
        ProgressBar{
            width: 100% !important;
            margin-bottom: 1;
        }

        ProgressBar Bar{
            width: 100% !important;
        }



        .section{
            padding: 1 1;
        }

        .section_title{
            padding: 1 1;
            text-style: bold
        }

        .field_label{
            margin: 1 0;
            text-style: bold;
        }

        .button{
            margin-left: 1;
        }

        #message_editor_column_content{
            border: hkey $primary;
        }

        #action_buttons_container{
            height: auto;
        }

        #message_editor_type_actions{
            height: 10
        }

        #suggestions_progress_bar{
            display: none;
            padding-right: 1;
        }

        #suggestions_scroll{
            height: 1fr;
            border: hkey $primary;
        }

        #message_actions{
            height: 7;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with Horizontal(classes="section"):

            with Vertical(classes="column" ):
                yield Label("MESSAGE EDITOR", classes="section_title")

                with Vertical(id="message_editor_column_content"):
                    with Horizontal(id="message_editor_type_actions"):
                        with Vertical():
                            yield Label("Message type", classes="field_label")
                            yield Select(MESSAGE_TYPES, id="message_type", prompt="Select message type", value="slack_message")
                        with Vertical():
                            yield Label("Actions", classes="field_label")
                            yield SelectionList(*MESSAGE_ACTIONS, id="message_actions")

                    yield Label("Text", classes="field_label")
                    yield TextArea(language="markdown", id="message_input")

                with Horizontal(id="action_buttons_container"):
                    yield Button("APPLY →", variant="primary", flat=True, classes="button", id="message_improve_button")
                    yield Button("CLEAR FORM", variant="primary", flat=True, classes="button", id="clear_form_btn")

            yield Rule.vertical(line_style="heavy")

            with Vertical(classes="column"):
                yield Label("SUGESTIONS", classes="section_title")
                yield ProgressBar(show_bar=True, clock=None, show_eta=False, show_percentage=False, id="suggestions_progress_bar")

                with VerticalScroll(id="suggestions_scroll"):
                    yield Markdown( id="suggestions_output")
                yield Button("CLEAR CHAT CONTEXT", variant="primary",classes="button", id="clear_chat_context_btn", flat=True)


    def on_mount(self) -> None:
        self.title = "HONEMSG"
        self.message_type = self.query_one("#message_type", Select)
        self.message_input = self.query_one("#message_input", TextArea)
        self.message_actions = self.query_one("#message_actions", SelectionList)
        self.message_improve_button = self.query_one("#message_improve_button", Button)
        self.suggestions_progress_bar = self.query_one("#suggestions_progress_bar", ProgressBar)
        self.suggestions_output = self.query_one("#suggestions_output", Markdown)

    @on(Button.Pressed, "#message_improve_button")
    def on_improve_message(self) -> None:
        if self.message_type.value is Select.NULL:
            self.notify("Please select a message type before continuing.", severity="warning")
            return

        if self.message_input.text:
            self.suggestions_output.update(markdown="")
            self.generate_suggestions()

    @on(Button.Pressed, "#clear_form_btn")
    def on_clear_form(self) -> None:
        self.message_type.value = "slack_message"
        self.message_actions.deselect_all()
        self.message_input.clear()

    @on(Button.Pressed, "#clear_chat_context_btn")
    def on_clear_chat_context(self) -> None:
        self.suggestions_output.update(markdown="")
        self.notify("Chat context cleared.", severity="information")

    @work(thread=True)
    def generate_suggestions(self):
        self.app.call_from_thread(self.toggle_progress_bar, True)
        message = send_message_to_ollama(self.message_type.value, self.message_actions.selected, self.message_input.text)
        self.app.call_from_thread(self.suggestions_output.append, f"{message}")
        self.app.call_from_thread(self.toggle_progress_bar, False)

    def toggle_progress_bar(self, visible):
        self.suggestions_progress_bar.display = "block" if visible else "none"

def run() -> None:
    HonemsgApp().run()

if __name__ == "__main__":
    run()
