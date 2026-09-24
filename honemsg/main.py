from textual.app import App, ComposeResult
from textual.widgets import Header

from honemsg.views.honemsg import HonemsgView
from honemsg.views.welcome import WelcomeScreen


class HonemsgApp(App):

    CSS = """
        HonemsgView{
            height: 1fr;
        }

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
            height: 12;
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
            height: 1fr;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="📝")
        yield HonemsgView()

    def on_mount(self) -> None:
        self.title = "HONEMSG"
        self.push_screen(WelcomeScreen())

def run() -> None:
    HonemsgApp().run()

if __name__ == "__main__":
    run()
