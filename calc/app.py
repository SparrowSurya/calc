"""
Module: calc.app
Description: Provide the main application interface.
"""

from .gui import Window
from .models import ExprModel


class Application:
    """Main application engine.

    Controller part of the application.
    """

    def __init__(self, view: Window, model: ExprModel):
        """
        Arguments:
        - view: interface for the application.
        - model: expression model providing actions for various functionalities.
        """
        self.view = view
        self.model = model
        self.view.evaluate = self.evaluate
        self.view.setup()

    @property
    def expr(self) -> str:
        """Gets the expression from view."""
        return self.view.get_expr()

    @expr.setter
    def expr(self, expr: str):
        """Sets the expr on view."""
        self.view.set_expr(expr)

    def mainloop(self):
        """Run the application."""
        self.view.mainloop()

    def evaluate(self, expr: str):
        """Updates the expression after each input.

        Arguments:
        - expr: input expression.
        """
        result, success = self.model.evaluate(expr)
        if success:
            self.view.set_expr(str(result))
        else:
            self.view.show_error(result)


if __name__ == "__main__":
    from .gui import Window
    from .models import ExprModel

    app = Application(view=Window(), model=ExprModel())
    app.mainloop()
