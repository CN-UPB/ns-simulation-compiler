# superclass for all PN nodes
class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        # references to in- and outgoing arcs (added later)
        self.in_arcs = []
        self.out_arcs = []

    def __str__(self):
        return self.name

    def print(self):
        in_arcs = ""
        for a in self.in_arcs:
            in_arcs += f"{a} "
        out_arcs = ""
        for a in self.out_arcs:
            out_arcs += f"{a} "
        print(f"{self} - In: {in_arcs}, Out: {out_arcs}")


class Place(Node):
    def __init__(self, id, name):
        Node.__init__(self, id, name)
        # firing weights of connected, outgoing immediate transitions
        self.probabilities = []

    # return normalized firing weights as string (eg, "0.3 0.7")
    def str_probabilities(self):
        sum_prob = sum(self.probabilities)
        str_prob = ""
        for prob in self.probabilities:
            str_prob += str(prob / sum_prob) + " "
        return str_prob[:-1]		# remove trailing space


class Transition(Node):
    # calculate and return coefficients based on in_arcs and out_arcs
    # currently only supports simple factors (no constants) and simply adds up multiple inputs (without weights)
    def coeffs(self):
        coeffs = ""
        # remove all "x.size*" to only have the factors remaining
        for o_arc in self.out_arcs:
            coeff = o_arc.inscription.replace("*","")
            for i_arc in self.in_arcs:
                coeff = coeff.replace(f"{i_arc.inscription}.size", "")
            # the result should be either the factor (eg, "1.5") or a simple input-variable (eg, "x") if the size doesn't change
            try:		# simple factor, eg "1.0"
                float(coeff)
                coeffs += coeff + " "
            except ValueError:		# variable name (eg "x") or sum of inputs (eg, "+") -> keep same size (= factor 1)
                coeffs += "1 "
        return coeffs[:-1]		# remove trailing space


class TimedTransition(Transition):
    def __init__(self, id, name, timing):
        Transition.__init__(self, id, name)
        self.timing = TimedTransition.timenet2omnetpp_timing(timing)

    # convert TimeNet's timing to Omnet++'s timing (eg, EXP(1) to exponential(1s))
    @staticmethod
    def timenet2omnetpp_timing(timenet_timing):
        if timenet_timing.startswith("EXP"):
            mean = float(timenet_timing[4:-1])
            return f"exponential({mean}s)"
        elif timenet_timing.startswith("UNI"):
            params = timenet_timing[4:-1].split(", ")
            a = float(params[0])
            b = float(params[1])
            return f"uniform({a}s, {b}s)"
        elif timenet_timing[0].isdigit():
            return timenet_timing + "s"
        else:
            raise ValueError("Unknown timing " + timenet_timing)


class ImmediateTransition(Transition):
    def __init__(self, id, name, weight):
        Transition.__init__(self, id, name)
        self.weight = float(weight)


class Arc:
    def __init__(self, src, dest, inscription):
        self.src = src
        self.dest = dest
        # cut off "new({size=" and "})" if it exists
        if inscription.startswith("new"):
            self.inscription = inscription[10:-2]
        else:
            self.inscription = inscription

    def __str__(self):
        # return f"({self.src}, {self.dest})"
        return self.inscription
