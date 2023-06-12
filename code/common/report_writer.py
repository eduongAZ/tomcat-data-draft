import os


class ReportWriter:
    """
    Remembers where the directory is to write report files to.
    Write report files to the directory without user specifying report directory.
    """

    def __init__(self, report_dir: str):
        """
        @param report_dir: report output directory
        """
        self.report_dir = report_dir

    def __call__(self,
                 report_file_name: str,
                 report: str,
                 to_terminal: bool = False):
        """
        Write report to file and optionally to terminal.
        @param report_file_name: report file name
        @param report: report content
        @param to_terminal: whether to print report to terminal
        @return: None
        """
        if to_terminal:
            print(report)

        with open(os.path.join(self.report_dir, report_file_name), 'w') as f:
            f.write(report)
