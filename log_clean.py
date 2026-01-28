import logging


class IgnoreTerminalServerWarning(logging.Filter):
    def filter(self, record):
        # If the log message contains the annoying string, return False (drop it)
        msg1 = "Could not find details in testbed for server terminal_server."
        msg2 = "No details found in testbed for hostname terminal_server."
        if msg1 in record.getMessage():
            return False
        if msg2 in record.getMessage():
            return False
        return True


def applyFilters():
    logging.getLogger().addFilter(IgnoreTerminalServerWarning())
    logging.getLogger("genie").addFilter(IgnoreTerminalServerWarning())
    logging.getLogger("pyats").addFilter(IgnoreTerminalServerWarning())
    logging.getLogger("unicon").addFilter(IgnoreTerminalServerWarning())
    logging.getLogger("genie.libs.filetransferutils.bases.fileutils").addFilter(
        IgnoreTerminalServerWarning()
    )
