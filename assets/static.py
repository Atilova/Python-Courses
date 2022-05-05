from inspect import cleandoc


class IncorrectSetup(Exception):
    def __init__(self, message: str='Incorrect module setup') -> None: 
        self.message = message
        super().__init__(self.message)


USER_MESSAGES = {
    'import_error': '<red>Module: ({}) import error...</red>',
    'import_success': '<green>Modules import success</green>',
    'import_failed': '<red>Wrong module(s) import usage...</red>',
    'help_command': cleandoc(
        """
        <orange>-h</orange>        use to diplay commands list
        <orange>-l</orange>        get list of solved problems
        <orange>--part</orange>    set lesson part, range will be applied to the selected part
        <orange>-r</orange>        [, or -] to set a range, leave (N-), to get the end, <orange>use with --part</orange>
        <orange>--all</orange>     use to execute everything
        """
    ),
    'incorrect_argument': '<orange>You specified incorrect script argument</orange>',  
    'incorrect_solved_setup': '<white>Solved not specified...</white>',
    'incorrect_description_setup': '<white>Description not specified...</white>',
    'wrong_problem_setup': '<white>Problem: ({}) should have both callback & title</white>',
    'lesson_error': '<orange>Lesson: ({}):</orange>',
    'wrong_setup': '<red>Module: ({}) should have a SETUP</red>',
    'part_not_set': '<blue>You used -r, but have not set the --part</blue>',
    'part_value_not_set': '<blue>You used --part, but not set the part name</blue>',
    'range_not_set': '<blue>You used -r but not set the range</blue>',
    'incorrect_part_name': '<blue>Part, you set does not exists</blue>',
    'quit': '<green>Quiting...</green>',
    'bye': '<green>Bye...</green>',
    'lesson_empty': '<orange>This lesson does not have any solved problems</orange>',
    'wrong_range_values': '<blue>Range: incorrect limit values</blue>',
    'wrong_range_definition': '<blue>Range: incorrect limit definition</blue>',
    'wrong_range_order': '<blue>Range: incorrect limit order</blue>',
    'wrong_range_bound': '<blue>Range: limit is out bound</blue>',
}