# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import pep8


settings = sublime.load_settings("Pep8Lint.sublime-settings")


ERRORS_IN_VIEWS = {}


def update_statusbar(view):
    """
    Update status bar with error.
    """
    # get view errors (exit if no errors found)
    view_errors = ERRORS_IN_VIEWS.get(view.id())
    if view_errors is None:
        return

    # get view selection (exit if no selection)
    view_selection = view.sel()
    if not view_selection:
        return

    # get current line (line under cursor)
    current_line = view.rowcol(view_selection[0].end())[0]

    if current_line in view_errors:
        # there is an error on current line
        errors = view_errors[current_line]
        view.set_status('pep8-tip',
                        'Pep8 errors: %s' % ' / '.join(errors))
    else:
        # no errors - clear statusbar
        view.erase_status('pep8-tip')


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
        regions = []
        view_errors = {}
        is_highlight = settings.get('highlight', False)
        is_popup = settings.get('popup', True)

        for e in self.errors:
            # get error line
            error_text = e[2]
            current_line = e[0]
            text_point = self.view.text_point(current_line, 0)
            line = self.view.full_line(text_point)
            full_line_text = self.view.substr(line)
            line_text = full_line_text.strip()
            # build line error message
            errors.append([e[2], u'{0}: {1}'.format(e[0] + 1, line_text)])

            # prepare errors regions
            if is_highlight:
                # prepare line
                line_text = full_line_text.rstrip('\r\n')
                line_length = len(line_text)

                # calculate error highlight start and end positions
                start = text_point + line_length - len(line_text.lstrip())
                end = text_point + line_length

                regions.append(sublime.Region(start, end))

        # save errors for each line in view to special dict
            view_errors.setdefault(current_line, []).append(error_text)

        # save errors dict
        ERRORS_IN_VIEWS[self.view.id()] = view_errors

        # highlight error regions if defined
        if is_highlight:
            self.view.add_regions('pep8-errors', regions,
                                  'invalid.deprecated', '',
                                  sublime.DRAW_OUTLINED)

        if is_popup:
            # display errors window
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

    def on_selection_modified(self, view):
        """
        Selection was modified: update status bar.
        """
        update_statusbar(view)
