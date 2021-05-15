#  helper functions
def tleFormat(tle: [dict]) -> [dict]:
    pass
    #  input: see excel TLE tab
    #  output: [{key="Satellite", value="ISS"}, {key="Height", value="21130"}, {key="Velocity, value="..."} ...]
    #  or some other formatting that makes processing easier


# C-style struct
class tle:
    def __init__(self) -> None:
        self.name = ""
        self.height = 0

    def __init_(self, raw: [dict]) -> None:
        #  consider using tleFormat() here?
        pass
