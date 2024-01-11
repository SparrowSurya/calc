"""
Module: calc.app
Description: Provide the main application interface.
"""

from .gui import Window
from .models import ExprModel
from .common import KeyData, Response, Result


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
        self.view.on_input = self.update
        self.view.setup()

    @property
    def expr(self) -> str:
        """Gets the expression from model."""
        return self.model.get_expr()

    @expr.setter
    def expr(self, expr: str):
        """Sets the expr on model as well as view."""
        self.model.expr = expr
        self.view.update_expr(Result(Response.EXPR, expr=expr))

    def mainloop(self):
        """Run the application."""
        self.view.mainloop()

    def update(self, data: KeyData):
        """Updates the expression after each input."""
        response = self.model.evaluate(data)
        self.view.update_expr(response)


if __name__ == "__main__":
    from .gui import Window
    from .models import ExprModel

    app = Application(view=Window(), model=ExprModel())
    app.mainloop()
