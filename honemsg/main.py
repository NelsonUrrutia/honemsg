from textual.app import App, ComposeResult
from textual.theme import Theme
from textual.widgets import Header

from honemsg.settings import Settings
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

        .button{
            margin-left: 1;
        }

        #message_editor_column_content{
            border: hkey $primary;
        }

        #action_buttons_container, .suggestions_buttons_container{
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

        #message_editor_type_actions{
            margin-top: 1;
        }

        #message_actions{
            height: 1fr;
            margin-left: 2;
        }

        Select > SelectCurrent, #message_actions, #message_input{
            border: round $primary;
            border-title-style: bold;
            border-title-color: $primary;
            padding-top: 1;
        }

        Select:focus > SelectCurrent, #message_actions:focus, #message_input:focus{
            border: round $primary-lighten-2;
        }

        #message_language{
            margin-top: 1;
        }

        #message_input{
            margin-top: 1;
        }
    """

    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()

    def compose(self) -> ComposeResult:
        yield Header(icon="📝")
        yield HonemsgView()

    def on_mount(self) -> None:
        self.title = "HONEMSG"
        self.restore_theme()
        self.theme_changed_signal.subscribe(self, self.save_theme)
        self.push_screen(WelcomeScreen())

    def restore_theme(self) -> None:
        saved_theme = self.settings.get("theme")
        if saved_theme in self.available_themes:
            self.theme = saved_theme

    def save_theme(self, theme: Theme) -> None:
        self.settings.set("theme", theme.name)

def run() -> None:
    HonemsgApp().run()

if __name__ == "__main__":
    run()
