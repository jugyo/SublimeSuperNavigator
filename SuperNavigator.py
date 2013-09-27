import sublime, sublime_plugin

class SuperNavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all('.+')
        items = [self.view.substr(self.view.line(_)) for _ in regions]

        def on_done(index):
            if index >= 0:
                region = regions[index]
                self.view.sel().clear()
                self.view.sel().add(region)
                self.view.show_at_center(region)

        self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, -1, on_done)
