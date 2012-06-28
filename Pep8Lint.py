# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import pep8


# TODO: add pep8 lint options
settings = sublime.load_settings("Pep8Lint.sublime-settings")


class Pep8Report(pep8.BaseReport):
    """Collect all results of the checks"""
    def __init__(self, options):
        super(Pep8Report, self).__init__(options)
        # errors "collection" =)
        self.errors = []

    def error(self, line_number, offset, text, check):
        code = super(Pep8Report, self).error(line_number, offset, text, check)
        if code:
            # save an error into collection
            self.errors.append({
                'row': self.line_offset + line_number - 1,
                'col': offset,
                'text': text
            })
        return code


class Pep8LintCommand(sublime_plugin.TextCommand):
    """Do pep8 lint on current file"""
    def run(self, edit):
        # current file name
        filename = self.view.file_name()

        # check only Python files
        if not filename.endswith('.py'):
            return

        # save file if dirty
        if self.view.is_dirty():
            self.view.run_command('save')

        # lint current file
        pep8style = pep8.StyleGuide(
            select=settings.get('select', []),
            ignore=settings.get('ignore', []),
            reporter=Pep8Report
        )
        pep8style.input_file(filename)

        # show errors
        self.show_errors(pep8style.options.report.errors)

    def show_errors(self, error_list):
        errors = []

        for e in error_list:
            # get error line
            line = self.view.full_line(self.view.text_point(e['row'], 0))
            line_text = self.view.substr(line).strip()

            # build line error message
            errors.append([
                e['text'],
                u'{0}: {1}'.format(e['row'] + 1, line_text)
            ])

        def select_error(selected_error):
            """Error was selected - go to error"""
            if selected_error == -1:
                return

            # reset selection
            selection = self.view.sel()
            selection.clear()

            # get error region
            error = error_list[selected_error]
            region_begin = self.view.text_point(error['row'], error['col'])

            # go to error
            selection.add(sublime.Region(region_begin, region_begin))
            self.view.show_at_center(region_begin)

        # view errors window
        self.view.window().show_quick_panel(errors, select_error)


class Pep8LintBackground(sublime_plugin.EventListener):
    def on_post_save(self, view):
        # do lint on file save if not denied in settings
        if settings.get('lint_on_save', True):
            view.run_command('pep8_lint')
