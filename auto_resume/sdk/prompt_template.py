import os


class PromptTemplate:
    def __init__(self, template, input_values: list=[]):
        # self.name = name
        self.template = template
        self.input_values = input_values

    def get_prompt(self, **kwargs):
        for key in kwargs:
            if key not in self.input_values:
                raise ValueError(f"Key {key} not in input values")
            # TODO, do more tests on the trim_tokens()
            # kwargs[key] = trim_tokens(kwargs[key])  # REMINDER: Fung: React agent will fail if using trim token
        return self.template.format(**kwargs)

    @classmethod
    def from_txt(
        cls, 
        prompt_template_file_path: str,
        input_values: list=[],
    ):  
        # prompt template
        with open(prompt_template_file_path, "r") as f:
            prompt_template = f.read()
        return cls(prompt_template, input_values)
    

if __name__ == '__main__':
    # prompt_template = PromptTemplate("Hello!")
    # print(prompt_template.get_prompt())
    prompt_template_1 = ""
    prompt_template_2 = ""
    prompt_template_3 = ""

    prompt_template_1.format()
    prompt_template_2.format()

    prompt_template = PromptTemplate(
        template="Here is my full introduction\n{full_intro}",
        full_intro=PromptTemplate(
            template="Here is my introduction:\n{intro}",
            intro=PromptTemplate(
                template="Hello I am {name}. My address is {address}!"
            ),
            input_values=["name", "address"]
        ),
    )
    