class Command:
    def __init__(self, name, expert_template, description) -> None:
        self.name = name
        self.expert_template = expert_template
        self.description = description
