
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
    TextArea,
)

from honemsg.controllers.ollama_chat import send_message_to_ollama

EXAMPLE_MARKDOWN = """\
Okay, here are a few options for improving that message, keeping in mind the context of needing
review and approval:

**Option 1 (Clear and Concise):**

> Hi [James],
>
> Just a quick follow-up on the task. Please share your notes/feedback after reviewing. It's
ready for publication and approval.
>
> Thanks,
> [Your Name]

**Option 2 (More Collaborative):**

> Hi [James],
>
> Just following up on the task. I'd appreciate it if you could share your notes or any
feedback you have after reviewing. Once I have that, I'm ready to proceed with publishing and
submitting for approval.
>
> Thanks,
> [Your Name]

**Option 3 (If you need specific feedback):**

> Hi [James],
>
> Just a quick reminder on the task. I'm ready to publish and submit for approval. To ensure
everything is accurate, please provide your notes and any feedback you have after reviewing.
>
> Thanks,
> [Your Name]

**Option 4 (If you're actively waiting for something):**

> Hi [James],
>
> Just checking in on the task. I'm ready to publish and submit for approval once I have your
notes and feedback.
>
> Thanks,
> [Your Name]

**Key Improvements and Why:**

*   **Clear Subject:** Start with a clear subject line if possible (e.g., "Follow-up: Task
[Task Name/Number]").
*   **Action-Oriented:** Clearly state what you need from James (notes, feedback, approval).
*   **Polite and Professional:** Use "please" and "thank you" where appropriate.
*   **Contextual Clarity:** Mention that it's ready for *publication* and *approval* to avoid
any misunderstanding.
*   **Optional: Specificity:** If you need feedback on a particular aspect, mention it.
*   **Optional: Timeframe:** If you need a response by a certain date/time, it's helpful to
include that.

By being clear, concise, and polite, you'll increase the chances of a smooth and timely review
and approval process."""

class HonemsgApp(App):

    DEFAULT_CSS = """
        ProgressBar{
            width: 100% !important;
            margin-bottom: 1;
        }

        ProgressBar Bar{
            width: 100% !important;
        }

        #suggestion_progress_bar{
            display: none;
        }

        .section{
            padding: 1 1;
        }

        .section_title{
            padding: 1 1;
            text-style: bold
        }

        .cta{
            margin-left: 1;
        }

        #suggestions_scroll{
            height: 1fr;
        }

        #chat_message_textarea{
            height: 5;
        }

        #chat_rule{
            margin: 1 0 0 0;
        }

        #chat_label{
            padding: 1 1;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with Horizontal(classes="section"):

            with Vertical(classes="column"):
                yield Label("MESSAGE", classes="section_title")
                yield TextArea(language="markdown", id="main_message")
                yield Button("IMPROVE →", variant="primary", flat=True, classes="cta", id="main_message_btn")

            yield Rule.vertical()

            with Vertical(classes="column"):
                yield Label("SUGESTIONS", classes="section_title")
                yield ProgressBar(show_bar=True, clock=None, show_eta=False, show_percentage=False, id="suggestion_progress_bar")

                with VerticalScroll(id="suggestions_scroll"):
                    yield Markdown( id="suggestions_container")

                yield Rule.horizontal(id="chat_rule")

                yield Label("Chat about it", classes="section_title", id="chat_label")
                yield TextArea(id="chat_message_textarea")
                yield Button("SEND →", flat= True, variant="primary", classes="cta", id="btn_send_chat_message")

    def on_mount(self) -> None:
        self.title = "HONEMSG"
        self.main_message = self.query_one("#main_message", TextArea)
        self.main_message_btn = self.query_one("#main_message_btn", Button)
        self.suggestion_progress_bar = self.query_one("#suggestion_progress_bar", ProgressBar)
        self.suggestions_container = self.query_one("#suggestions_container", Markdown)
        self.chat_message = self.query_one("#chat_message_textarea", TextArea)
        self.chat_message_btn = self.query_one("#btn_send_chat_message", Button)

    @on(Button.Pressed, "#main_message_btn")
    def on_improve_message(self) -> None:
        if self.main_message.text:
            self.render_ollama_response()

    @work(thread=True)
    def render_ollama_response(self):
        self.app.call_from_thread(self.toggle_progress_bar, True)
        message =  send_message_to_ollama(self.main_message.text)
        self.app.call_from_thread(self.suggestions_container.append, f"{message}")
        self.app.call_from_thread(self.toggle_progress_bar, False)

    def toggle_progress_bar(self, flag):
        self.suggestion_progress_bar.display = "block" if flag else "none"

def run() -> None:
    HonemsgApp().run()

if __name__ == "__main__":
    run()
