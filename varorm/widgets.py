from typing import Any


class Widget:
    input = '<input type="text" id="{id}" name="{id}" required {value_attr}>'
    def __init__(self, id: str, value: Any) -> None:
        value_attr = ""
        if value is not None:
            value_attr = f'value="{value}"'

        self.input = self.input.format(id=id, value_attr=value_attr)
    

class IntegerWidget(Widget):
    input = '<input type="number" id="{id}" name="{id}" required {value_attr}>'

class FloatWidget(Widget):
    input = '<input type="number" id="{id}" name="{id}" step="0.0000001" required {value_attr}>'

class DateWidget(Widget):
    input = '<input type="date" id="{id}" name="{id}" required {value_attr}>'

class DateTimeWidget(Widget):
    input = '<input type="datetime-local" id="{id}" name="{id}" required {value_attr}>'

class CharWidget(Widget):
    input = '<input type="text" id="{id}" name="{id}" required {value_attr}>'

class TextWidget(Widget):
    input = '<textarea id="{id}" name="{id}" required>{value}</textarea>'
    
    def __init__(self, id: str, value: Any) -> None:
        if value is None:
            value = ""
        self.input = self.input.format(id=id, value=value)


class BooleanWidget(Widget):
    input = '''<select required id="{id}" name="{id}">
                <option value="" {selected_none}>-</option>
                <option value="1" {selected_1}>True</option>
                <option value="0" {selected_0}>False</option>
               </select>'''
    def __init__(self, id: str, value: Any) -> None:
        selected_0 = ""
        selected_1 = ""
        selected_none = ""
        if value is not None:
            if value:
                selected_1 = "selected"
            else:
                selected_0 = "selected"
        else:
            selected_none = "selected"

        self.input = self.input.format(id=id, selected_0=selected_0, selected_1=selected_1, selected_none=selected_none)