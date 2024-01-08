"""
This module contains gui app,
"""

from .gui import Window
from .models import ExprModel
from .common import KeyData, Response, Result


class Application:
    """Main GUI program"""

    def __init__(self, view: Window, model: ExprModel):
        self.view = view
        self.model = model
        self.view.on_input = self.update
        self.view.setup()

    @property
    def expr(self) -> str:
        """gets expression from model"""
        return self.model.get_expr()

    @expr.setter
    def expr(self, expr: str):
        """sets the expr"""
        self.model.expr = expr
        self.view.update_expr(Result(Response.EXPR, expr=expr))

    def mainloop(self):
        """Run the application forever"""
        self.view.mainloop()

    def update(self, data: KeyData):
        """updates the expression after each input"""
        response = self.model.eval_key(data)
        self.view.update_expr(response)


if __name__ == "__main__":
    from .gui import Window
    from .models import ExprModel

    app = Application(view=Window(), model=ExprModel())
    app.mainloop()
