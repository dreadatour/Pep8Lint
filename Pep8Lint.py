# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import pep8


settings = sublime.load_settings("Pep8Lint.sublime-settings")


class Pep8Report(pep8.BaseReport):
    """
    Collect all results of the checks.
    """
    def __init__(self, options):
        """
        Initialize reporter.
        """
        super(Pep8Report, self).__init__(options)
        # errors "collection" =)
        self.errors = []

    def error(self, line_number, offset, text, check):
        """
        Get error and save it into errors collection.
        """
        code = super(Pep8Report, self).error(line_number, offset, text, check)
        if code:
            # save an error into collection
            self.errors.append(
                (self.line_offset + line_number - 1, offset, text)
            )
        return code


class Pep8LintCommand(sublime_plugin.TextCommand):
    """
    Do pep8 lint on current file.
    """
    def run(self, edit):
        """
        Run pep8 lint.
        """
        # current file name
        filename = self.view.file_name()

        # check if active view contains file
        if not filename:
            return

        # check only Python files
        if not self.view.match_selector(0, 'source.python'):
            return

        # save file if dirty
        if self.view.is_dirty():
            self.view.run_command('save')

        # lint current file
        pep8style = pep8.StyleGuide(
            select=settings.get('select', []),
            ignore=settings.get('ignore', []),
            max_line_length=settings.get('max-line-length', 79),
            reporter=Pep8Report
        )
        pep8style.input_file(filename)
        self.errors = pep8style.options.report.errors

        # show errors
        self.show_errors()

    def show_errors(self):
        """
        Show all errors.
        """
        errors = []

        for e in self.errors:
            # get error line
            line = self.view.full_line(self.view.text_point(e[0], 0))
            line_text = self.view.substr(line).strip()
            # build line error message
            errors.append([e[2], u'{0}: {1}'.format(e[0] + 1, line_text)])

        # view errors window
        self.view.window().show_quick_panel(errors, self.error_selected)

    def error_selected(self, item_selected):
        """
        Error was selected - go to error.
        """
        if item_selected == -1:
            return

        # reset selection
        selection = self.view.sel()
        selection.clear()

        # get error region
        error = self.errors[item_selected]
        region_begin = self.view.text_point(error[0], error[1])

        # go to error
        selection.add(sublime.Region(region_begin, region_begin))
        self.view.show_at_center(region_begin)


class Pep8LintBackground(sublime_plugin.EventListener):
    """
    Listen to Siblime Text 2 events.
    """
    def on_post_save(self, view):
        """
        Do lint on file save if not denied in settings.
        """
        if settings.get('lint_on_save', True):
            view.run_command('pep8_lint')
