//simple chain
network SimplePN {
    submodules:
        t1: Transition;
        t2: Transition;
        p1: Place;
        p2: Place;
    connections:
        t1.out++ --> { delay = 0ms; } --> p1.in++;
        p1.out++ --> { delay = 0ms; } --> t2.in++;
        t2.out++ --> { delay = 0ms; } --> p2.in++;
}


//transition splits tokens into two
network SplitTrans {
    submodules:
        t1: Transition;
        t2: Transition;
        p1: Place;
        p2: Place;
        p3: Place;
    connections:
        t1.out++ --> { delay = 0ms; } --> p1.in++;
        p1.out++ --> { delay = 0ms; } --> t2.in++;
        t2.out++ --> { delay = 0ms; } --> p2.in++;
        t2.out++ --> { delay = 0ms; } --> p3.in++;
}


//place distributes tokens randomly
network SplitPlace {
    submodules:
        t1: Transition;
        it1: ImmTrans;
        it2: ImmTrans;
        p1: Place;
        p2: Place;
        p3: Place;
    connections:
        t1.out++ --> { delay = 0ms; } --> p1.in++;
        p1.out++ --> { delay = 0ms; } --> it1.in++;
        p1.out++ --> { delay = 0ms; } --> it2.in++;
        it1.out++ --> { delay = 0ms; } --> p2.in++;
        it2.out++ --> { delay = 0ms; } --> p3.in++;
}


//transition synchronizes incoming tokens before sending out a new one
network SyncTrans {
    submodules:
        s1: Transition;
        s2: Transition;
		t: Transition;
		p1: Place;
		p2: Place;
		p3: Place;
	connections:
	    s1.out++ --> { delay = 0ms; } --> p1.in++;
	    s2.out++ --> { delay = 0ms; } --> p2.in++;
        p1.out++ --> { delay = 0ms; } --> t.in++;
        p2.out++ --> { delay = 0ms; } --> t.in++;
        t.out++ --> { delay = 0ms; } --> p3.in++;
}