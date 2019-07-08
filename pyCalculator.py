"""

Simple calculator created using the wxPython module.

"""

import wx

"""
Code below creates the main window/frame for the GUI.
A default size is set for initial launching along with maximum/minimum resize parameters.
"""


class CalculatorFrame(wx.Frame):

    def __init__(self):
        super().__init__(
            None, title="Calculator v1.0", size=(400, 550)
        )
        panel = CalculatorPanel(self)
        self.SetSizeHints(350, 375, 600, 750)
        self.Show()


class CalculatorPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.last_button_pressed = None
        self.create_UI()

    def create_UI(self):
        mainSize = wx.BoxSizer(wx.VERTICAL)                     # Main UI sizer
        font = wx.Font(25, wx.MODERN, wx.NORMAL, wx.NORMAL)     # Font which will override default style

        self.solution = wx.TextCtrl(self, style=wx.TE_CENTER)   # Center Aligns input for equation
        self.solution.SetFont(font)
        self.solution.Disable()                                 # Disables direct input from user via keyboard
        mainSize.Add(self.solution, 0, wx.EXPAND | wx.ALL, 5)
        self.running_total = wx.StaticText(self)                # Solution to the equation displayed as read only text
        self.running_total.SetFont(font)
        mainSize.Add(self.running_total, 0, wx.ALIGN_RIGHT)

        calcButtons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['.', '0', '',  '/']
        ]

        buttonFont = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)

        """
        The calcButtons matrix above will contain the button labels for out main calculator.
        The loop below will create a horizontal box sizer for each row of buttons.
        Each individual button will then be added to this sizer.
        Each button is also bound to the updateEquation event handler.
        Once each button is added the sizers are added to the main UI sizer.
        """

        for buttonList in calcButtons:
            buttonSizer = wx.BoxSizer()
            for buttonLable in buttonList:
                button = wx.Button(self, label=buttonLable)
                button.SetFont(buttonFont)
                buttonSizer.Add(button, 1, wx.ALIGN_CENTER|wx.EXPAND, 0)
                button.Bind(wx.EVT_BUTTON, self.updateEquation)
            mainSize.Add(buttonSizer, 1, wx.ALIGN_CENTER|wx.EXPAND)

        equalsButton = wx.Button(self, label='=')               # Creates an '=' button which binds to on_total event
        equalsButton.SetFont(buttonFont)
        equalsButton.Bind(wx.EVT_BUTTON, self.on_total)
        mainSize.Add(equalsButton, 0, wx.EXPAND|wx.ALL, 3)

        clearButton = wx.Button(self, label='Clear')            # Creates a clear button which clears solution on event
        clearButton.SetFont(buttonFont)
        clearButton.Bind(wx.EVT_BUTTON, self.on_clear)
        mainSize.Add(clearButton, 0, wx.EXPAND|wx.ALL, 3)

        self.SetSizer(mainSize)                                 # Set main sizer

    """
    Since multiple buttons are bound to the same event handler we need to determine which button has triggered the event.
    This is done via GetEventObject() method which will capture the event and button label which triggered the event via the GetLabel() method.
    """

    def updateEquation(self, event):
        operands = ['/', '*', '+', '-']

        action = event.GetEventObject()
        label = action.GetLabel()
        currentEquation = self.solution.GetValue()

        """
        The following control structure is mainly for string formatting/presentation.
        The label is compared to a list of operators, if it is an operator a space is added between it and the label.
        For loop checks if an operator is contained in the equation strings;
        if found update_solution() method called and loop is broken.
        """

        if label not in operands:
            if self.last_button_pressed in operands:
                self.solution.SetValue(currentEquation + " " + label)
            else:
                self.solution.SetValue(currentEquation + label)
        elif label in operands and currentEquation is not '' and self.last_button_pressed not in operands:
            self.solution.SetValue(currentEquation + ' ' + label)

        self.last_button_pressed = label

        for operator in operands:
            if operator in self.solution.GetValue():
                self.update_solution()
                break

    """
    To catch any errors associated with math calculations I used a try/except statement with a bare except.
    The current value of the equation is evaluated into a sting and passed into the eval() method.
    This converts result back into a string.
    """

    def update_solution(self):
        try:
            current_solution = str(eval(self.solution.GetValue()))
            self.running_total.SetLabel(current_solution)
            self.Layout()
            return current_solution
        except ZeroDivisionError:
            self.solution.SetValue('ZeroDivision')
        except:
            pass

    """
    This clears both the solution and running_total fields.
    Due to wx.StaticText not having a Clear() method I simply set the label to an empty string.
    """

    def on_clear(self, event):
        self.solution.Clear()
        self.running_total.SetLabel('')

    """
    Calculates total and clears running_total.
    """

    def on_total(self, event):
        solution = self.update_solution()

        if solution:
            self.running_total.SetLabel('')


"""
Main program executed.
"""

if __name__ == "__main__":
    pyApp = wx.App(False)
    pyFrame = CalculatorFrame()
    pyApp.MainLoop()
