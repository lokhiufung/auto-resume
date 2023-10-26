from enum import Enum
from rich.console import Console


print = Console(width=80, highlight=False).print


class Color(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'


class ColorPrintMixin:

    supporting_colors = Color

    def color_print(self, color, text):
        color_code = self.supporting_colors.RESET.value
        for supporting_color in self.supporting_colors:
            if supporting_color.name == color:
                color_code = supporting_color.value
        text = color_code + text + supporting_color.RESET.value
        print(text)
    
    def print_user_message(self, name, message):
        # self.color_print('BLUE', '[USER]: ' + message)
        print(f'[USER]: {name}', style='bold blue')
        print(message, style='blue')
    
    def print_agent_message(self, name, message):
        # self.color_print('GREEN', '[AGENT]: ' + message)
        print(f'[AGENT]: {name}', style='bold green')
        print(message, style='green')
    
    def print_llm_message(self, message):
        self.color_print('YELLOW', '[LLM]: ' + message)

    def print_tool_message(self, tool_name, message):
        self.color_print('CYAN', f'[TOOL({tool_name=})]: ' + message)

    


if __name__ == '__main__':
    c = ColorPrintMixin()

    c.print_user_message('hello')
    c.print_agent_message('hello')
    c.print_llm_message('hello')
    