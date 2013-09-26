import sublime, sublime_plugin
import re

class SuperNavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all('.+')
        items = list(map(lambda _: self.view.substr(self.view.line(_)), regions))

        def on_done(index):
            if index >= 0:
                region = regions[index]
                self.view.sel().clear()
                self.view.sel().add(region)
                self.view.show_at_center(region)

        self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, -1, on_done)
