#include <stdio.h>
#include <string.h>
#include <omnetpp.h>
#include <stdlib.h>
#include "token_m.h"
#include <algorithm>

using namespace omnetpp;


class Transition : public cSimpleModule {
private:
    cQueue queues[5];                   // assume at most 5 inputs as the number is unknown a priori (not all of the 5 queues have to be used)
    cMessage *generationEvent;
    cMessage *processingEvent;
    cMessage *measureEvent;
    int counter = 0;                    // for naming newly generated tokens (if there are no inputs)
    bool processing = false;            // to ensure that new tokens are only processed after the previous processing has finished

    cOutVector tokenInSize;             // record size of incoming tokens
    cOutVector tokenInDelay;            // delay from creation to arrival this transition
    cOutVector queueLength[5];          // measure queue length for each queue separately
    cOutVector transitionDelay;         // processing delay or generation delay (basically par("rate"))

public:
    virtual ~Transition();
protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    double newTokenSize(double currSize, int output);
    void startProcessing();
};

Define_Module(Transition);


Transition::~Transition() {
    cancelAndDelete(generationEvent);
    cancelAndDelete(processingEvent);
    cancelAndDelete(measureEvent);
}

void Transition::initialize() {
    generationEvent = new cMessage("generationEvent");
    processingEvent = new cMessage("processingEvent");
    measureEvent = new cMessage("measureEvent");

    tokenInSize.setName("tokenInSize");
    tokenInDelay.setName("tokenInDelay");
    for (int i=0; i<gateSize("in"); i++) {
        std::string measureName = "queueLength" + std::to_string(i);
        queueLength[i].setName(measureName.c_str());
    }
    transitionDelay.setName("processingDelay");

    // trigger initial token generation
    if (gateSize("in") == 0 and gateSize("out") > 0) {
        double generationDelay = par("rate");
        transitionDelay.record(generationDelay);
        scheduleAt(simTime() + generationDelay, generationEvent);
    }
    // trigger initial measureEvent (directly)
    scheduleAt(simTime(), measureEvent);
}

void Transition::handleMessage(cMessage *msg) {
    // measure queue length every second
    if (msg == measureEvent) {
        for (int i=0; i<gateSize("in"); i++)
            queueLength[i].record(queues[i].getLength());
        scheduleAt(simTime() + 1, measureEvent);        // measure periodically every second
    }

    // transitions without inputs periodically generate new tokens
    else if (msg == generationEvent) {
        Token *token = new Token(std::to_string(counter).c_str());
        token->setCreationTime(simTime());
        token->setSize(newTokenSize(1, 0));         //set size according to value specified in ini
        counter++;

        EV << "Sending out new token " << token->getName() << "\n";
        send(token, "out", 0);
        double generationDelay = par("rate");
        transitionDelay.record(generationDelay);
        scheduleAt(simTime() + generationDelay, generationEvent);
    }

    // after processing, pop first queued token of each input queue, create new ones for each output, adjust size, and send on each output
    else if (msg == processingEvent) {
        processing = false;

        // sync: pop first token of each input queue, sum up their size, merge their names & creationTime (take earliest), and delete tokens
        // simplifying assumption: always add size of different inputs; size of inputs is not weighted
        double sumSize = 0;
        std::string mergedName = "";
        simtime_t earliestCreationTime = simTime();     // TODO: correct to take earliest?
        for (int i=0; i<gateSize("in"); i++) {
            Token *token = (Token *)queues[i].pop();
            sumSize += token->getSize();
            mergedName += token->getName();
            if (token->getCreationTime() < earliestCreationTime)
                earliestCreationTime = token->getCreationTime();
            delete token;
        }

        // split: delete token and create new ones for each output with adjusted size and name
        for (int i=0; i<gateSize("out"); i++) {
            std::string newName = mergedName;
            if (gateSize("out") > 1)
               newName += "." + std::to_string(i);
            Token *token = new Token(newName.c_str());
            token->setCreationTime(earliestCreationTime);
            token->setSize(newTokenSize(sumSize, i));
            EV << "Processing done, sending out token " << token->getName() << " on output " << i << " (size: " << token->getSize() << ")\n";
            send(token, "out", i);
        }

        startProcessing();      // start processing next tokens
    }

    // when receiving a new token, queue it (and process it)
    else if (gateSize("out") > 0) {
        Token *token = check_and_cast<Token *>(msg);
        tokenInSize.record(token->getSize());
        tokenInDelay.record(simTime() - token->getCreationTime());

        //insert in queue corresponding to input
        int in_gate = token->getArrivalGate()->getIndex();
        EV << "Queuing incoming token " << token->getName() << " on gate " << in_gate << "\n";
        queues[in_gate].insert(token);

        startProcessing();
    }
}

// multiply currSize with factor specified in .ini for specified output
// simplifying assumption: only multiply by factor; no constants, squares, etc.
double Transition::newTokenSize(double currSize, int output) {
    // parse and split coefficients (must have the following form: "a b c" for 3 outputs)
    const char *vstr = par("coeffs").stringValue();
    std::vector<double> coeffs = cStringTokenizer(vstr).asDoubleVector();

    return currSize * coeffs[output];
}

// check if all required tokens are available and start processing
void Transition::startProcessing() {
    // check all input queue have a token, i.e., are synchronized
    bool sync = true;
    for (int i=0; i<gateSize("in"); i++) {
        if (queues[i].isEmpty())
            sync = false;
    }

    // if not processing already and tokens are available at all inputs (ie, sync), start processing directly
    if (!processing and sync) {
        double processingDelay = par("rate");
        transitionDelay.record(processingDelay);
        EV << "Processing synchronized tokens for " << processingDelay << "s\n";
        processing = true;
        scheduleAt(simTime() + par("rate"), processingEvent);
    }
}
