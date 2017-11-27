// Petri net elements for all ned-network files

//places simply forward tokens (queuing happens at the transitions). they distribute tokens among outputs according to firing weights.
simple Place {
    parameters:
        @display("i=place");
        volatile string probabilities = default("1");		// probabilities for each output to be chosen (eg, "0.7 0.3")
    gates:
        input in[];
        output out[];
}

//transitions are the core of a VNF: they do queuing, processing, size changes
simple Transition {
    parameters:
        @display("i=transition");
        volatile double rate @unit(s) = default(1s);
        volatile string coeffs = default("1");				// token size-changing factors for each output (eg, "1 2.5")
    gates:
        input in[];
        output out[];
}

// simple helper transitions that simply forward tokens (may change size). just for easier mapping. firing weights are implemented in places
simple ImmTrans {
    parameters:
        @display("i=immtrans");
        volatile string coeffs = default("1");				// token size-changing factors for each output (eg, "1 2.5")
    gates:
        input in[];
        output out[];
}