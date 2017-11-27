network VideoAuto {
    submodules:
        C_P0: Place;
        S_P0: Place;
        V_P0: Place;
        A_P0: Place;
        C_P2: Place;
        C_P3: Place;
        U_P0: Place;
        C_P1: Place;
        C_T3: Transition;
        S_T0: Transition;
        V_T0: Transition;
        A_T0: Transition;
        C_T0: Transition;
        U_T0: Transition;
        C_T1: ImmTrans;
        C_T2: ImmTrans;
    connections:
        S_P0.out++ --> { delay = 0ms; } --> S_T0.in++;
        S_T0.out++ --> { delay = 0ms; } --> V_P0.in++;
        S_T0.out++ --> { delay = 0ms; } --> A_P0.in++;
        A_P0.out++ --> { delay = 0ms; } --> A_T0.in++;
        V_P0.out++ --> { delay = 0ms; } --> V_T0.in++;
        V_T0.out++ --> { delay = 0ms; } --> C_P2.in++;
        A_T0.out++ --> { delay = 0ms; } --> C_P3.in++;
        C_P3.out++ --> { delay = 0ms; } --> C_T3.in++;
        C_P2.out++ --> { delay = 0ms; } --> C_T3.in++;
        C_T3.out++ --> { delay = 0ms; } --> U_P0.in++;
        C_P0.out++ --> { delay = 0ms; } --> C_T0.in++;
        C_T0.out++ --> { delay = 0ms; } --> C_P1.in++;
        C_P1.out++ --> { delay = 0ms; } --> C_T1.in++;
        C_P1.out++ --> { delay = 0ms; } --> C_T2.in++;
        C_T2.out++ --> { delay = 0ms; } --> S_P0.in++;
        C_T1.out++ --> { delay = 0ms; } --> U_P0.in++;
        U_T0.out++ --> { delay = 0ms; } --> C_P0.in++;
}