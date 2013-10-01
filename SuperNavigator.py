import sublime, sublime_plugin
import os

class SuperNavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit, allTabs=False):
        if allTabs:
            self.navigate(self.view.window().views(), showFileName=True)
        else:
            self.navigate([self.view])

    def navigate(self, views, showFileName=False):
        org_sel = list(self.view.sel())

        if len(self.view.sel()) == 1 and self.view.sel()[0].size() > 0:
            pattern = ".*%s.*" % self.view.substr(self.view.sel()[0])
        else:
            pattern = ".+"

        items = []
        view_and_regions = []

        for view in views:
            regions = view.find_all(pattern)
            if showFileName:
                file_name = os.path.basename(view.file_name())
                items += [["%s: %s" % (file_name, view.substr(view.line(_)))] for _ in regions]
            else:
                items += [view.substr(view.line(_)) for _ in regions]
            view_and_regions += [[view, _] for _ in regions]

        def on_done(index):
            if index >= 0:
                (view, region) = view_and_regions[index]
                self.view.window().focus_view(view)
                view.sel().clear()
                view.sel().add(region)
                view.show_at_center(region)
            else:
                self.view.window().focus_view(self.view)
                self.view.sel().clear()
                self.view.sel().add_all(org_sel)
                self.view.show(org_sel[0])

        if int(sublime.version()) > 3000:
            self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, -1, on_done)
        else:
            self.view.window().show_quick_panel(items, on_done)
