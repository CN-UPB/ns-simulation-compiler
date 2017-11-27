// immediate transition: only forwards tokens (immediately)
// firing weights are implemented as probabilities at the places
// immediate transitions are simply mapped from the TimeNet-xml to ensure a connected graph
#include <stdio.h>
#include <string.h>
#include <omnetpp.h>
#include "token_m.h"

using namespace omnetpp;


class ImmTrans : public cSimpleModule {
protected:
    virtual void handleMessage(cMessage *msg) override;
    double newTokenSize(double currSize, int output);
};

Define_Module(ImmTrans);

void ImmTrans::handleMessage(cMessage *msg) {
    Token *token = check_and_cast<Token *>(msg);
    token->setSize(newTokenSize(token->getSize(), 0));
    EV << "Sending token " << token->getName() << " (size: " << token->getSize() << ")\n";
    send(token, "out", 0);          // assume only 1 output (consistent with model)
}

// multiply currSize with factor specified in .ini for specified output
// simplifying assumption: only multiply by factor; no constants, squares, etc.
double ImmTrans::newTokenSize(double currSize, int output) {
    // parse and split coefficients (must have the following form: "a b c" for 3 outputs)
    const char *vstr = par("coeffs").stringValue();
    std::vector<double> coeffs = cStringTokenizer(vstr).asDoubleVector();

    return currSize * coeffs[output];
}
