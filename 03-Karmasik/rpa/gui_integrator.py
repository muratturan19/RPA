"""Integration helpers between RPA core and GUI."""

from .core_engine import EnterpriseRPABot
from ..gui import EnterpriseGUI


def launch_with_gui(files):
    """Placeholder integration running bot with GUI."""
    gui = EnterpriseGUI()
    bot = EnterpriseRPABot()
    bot.set_gui_reference(gui)
    bot.set_processing_files(files)
    return bot
