class WinningInfo:
    def __init__(self, w_type, w_values=None, w_keys=None):
        self.w_type = w_type
        self.w_values = w_values
        self.w_keys = w_keys

    def __repr__(self):
        return f"(type={self.w_type}, values={self.w_values}, keys={self.w_keys})"

    def __str__(self) -> str:
        return self.__repr__()
