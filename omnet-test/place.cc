#include <stdio.h>
#include <string.h>
#include <omnetpp.h>
#include "token_m.h"

using namespace omnetpp;


class Place : public cSimpleModule {
private:
    cOutVector tokenInSize;             // record size of incoming tokens
    cOutVector tokenInDelay;            // delay from creation until arrival at this place
protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    int randomOutput();
};

Define_Module(Place);

void Place::initialize() {
    tokenInSize.setName("tokenInSize");
    tokenInDelay.setName("tokenInDelay");
}

void Place::handleMessage(cMessage *msg) {
    Token *token = check_and_cast<Token *>(msg);
    tokenInDelay.record(simTime() - token->getCreationTime());
    tokenInSize.record(token->getSize());

    // distribute tokens among outputs according to specified probabilities
    if (gateSize("out") > 0) {
        int randOut = randomOutput();
        EV << "Sending token " << token->getName() << " on output " << randOut << "\n";
        send(token, "out", randOut);
    }

    // delete tokens if there is no outgoing arc
    else {
        delete msg;
    }
}

// return randomly selected output according to the specified probabilities
int Place::randomOutput() {
    // parse and split probabilities (eg, "0.3 0.2 0.5")
    const char *vstr = par("probabilities").stringValue();
    std::vector<double> probabilities = cStringTokenizer(vstr).asDoubleVector();

    // add up probabilities to have probability of a random 0<r<1 being lower (eg, "0.3 0.5 1")
    double sum_probs = 0;
    for (auto& prob: probabilities) {
        sum_probs += prob;
        prob = sum_probs;
    }

    // select random output
    int output = 0;
    double r = ((double) rand() / RAND_MAX);
    while (r > probabilities[output]) {
        r -= probabilities[output];
        output++;
    }

    return output;
}

