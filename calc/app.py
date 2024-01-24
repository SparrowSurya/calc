"""
Module: calc.app
Description: Provide the main application interface.
"""

from .view import AbstractView
from .models import AbstractModel


class Controller:
    """Main Control application engine for the Calculator."""

    def __init__(self, model: AbstractModel):
        """
        Initialise the control engine with a model.

        Arguments:
        - model: a model to provide the operation of various queries.

        The view attribute is by default is `None`.
        It is the respnsibility of the view to bind with it.
        """
        self.model = model
        self.view: AbstractView | None = None

    def evaluate_expression(self) -> None:
        """Evaluates the expression and provides it to the view."""
        result, success = self.model.evaluate(self.view.expression)

        if success:
            self.view.show_expression(str(result))
        else:
            self.view.show_error(result)


if __name__ == "__main__":
    from .gui import TkView
    from .models import CalcModel

    view = TkView("Calculator", Controller(CalcModel()))
    view.mainloop()
