
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

        #suggestions_progress_bar{
            display: none;
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

        #message_editor_type_actions{
            height: 10
        }

        #suggestions_scroll{
            height: 1fr;
        }

        #chat_input{
            height: 5;
        }

        #chat_divider{
            margin: 1 0 0 0;
        }

        #chat_title{
            padding: 1 1;
        }

        #message_actions{
            height: 7;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with Horizontal(classes="section"):

            with Vertical(classes="column"):
                yield Label("MESSAGE EDITOR", classes="section_title")
                with Horizontal(id="message_editor_type_actions"):
                    with Vertical():
                        yield Label("Message type", classes="field_label")
                        yield Select(MESSAGE_TYPES, id="message_type", prompt="Select message type", value="slack_message")
                    with Vertical():
                        yield Label("Actions", classes="field_label")
                        yield SelectionList(*MESSAGE_ACTIONS, id="message_actions")
                yield Label("Text", classes="field_label")
                yield TextArea(language="markdown", id="message_input")
                yield Button("APPLY →", variant="primary", flat=True, classes="button", id="message_improve_button")

            yield Rule.vertical()

            with Vertical(classes="column"):
                yield Label("SUGESTIONS", classes="section_title")
                yield ProgressBar(show_bar=True, clock=None, show_eta=False, show_percentage=False, id="suggestions_progress_bar")

                with VerticalScroll(id="suggestions_scroll"):
                    yield Markdown( id="suggestions_output")

                yield Rule.horizontal(id="chat_divider")

                yield Label("Chat about it", classes="section_title", id="chat_title")
                yield TextArea(id="chat_input")
                yield Button("SEND →", flat= True, variant="primary", classes="button", id="chat_send_button")

    def on_mount(self) -> None:
        self.title = "HONEMSG"
        self.message_type = self.query_one("#message_type", Select)
        self.message_input = self.query_one("#message_input", TextArea)
        self.message_actions = self.query_one("#message_actions", SelectionList)
        self.message_improve_button = self.query_one("#message_improve_button", Button)
        self.suggestions_progress_bar = self.query_one("#suggestions_progress_bar", ProgressBar)
        self.suggestions_output = self.query_one("#suggestions_output", Markdown)
        self.chat_input = self.query_one("#chat_input", TextArea)
        self.chat_send_button = self.query_one("#chat_send_button", Button)

    @on(Button.Pressed, "#message_improve_button")
    def on_improve_message(self) -> None:
        if self.message_type.value is Select.NULL:
            self.notify("Please select a message type before continuing.", severity="warning")
            return

        if self.message_input.text:
            self.generate_suggestions()

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
