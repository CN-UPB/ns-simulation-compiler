network VideoFixed
{
    @display("bgb=1153.824,731.136");
    submodules:
        C_P0: Place {
            @display("p=316,237");
        }
        S_P0: Place {
            @display("p=942.48,169.93199");
        }
        V_P0: Place {
            @display("p=919.63196,432.684");
        }
        A_P0: Place {
            @display("p=985.31995,594.048");
        }
        C_P2: Place {
            @display("p=367,433");
        }
        C_P3: Place {
            @display("p=374,585");
        }
        U_P0: Place {
            @display("p=53,296");
        }
        C_P1: Place {
            @display("p=498,237");
        }
        C_T3: Transition {
            @display("p=259,495");
        }
        S_T0: Transition {
            @display("p=1092.4199,168.504");
        }
        V_T0: Transition {
            @display("p=798.25195,431.25598");
        }
        A_T0: Transition {
            @display("p=883.932,592.62");
        }
        C_T0: Transition {
            @display("p=409,236");
        }
        U_T0: Transition {
            @display("p=139,295");
        }
        C_T1: ImmTrans {
            @display("p=605,67");
        }
        C_T2: ImmTrans {
            @display("p=605,283");
        }
    connections:
        S_P0.out++ --> {  delay = 0ms; } --> S_T0.in++;
        S_T0.out++ --> {  delay = 0ms; } --> V_P0.in++;
        S_T0.out++ --> {  delay = 0ms; } --> A_P0.in++;
        A_P0.out++ --> {  delay = 0ms; } --> A_T0.in++;
        V_P0.out++ --> {  delay = 0ms; } --> V_T0.in++;
        V_T0.out++ --> {  delay = 0ms; } --> C_P2.in++;
        A_T0.out++ --> {  delay = 0ms; } --> C_P3.in++;
        C_P3.out++ --> {  delay = 0ms; } --> C_T3.in++;
        C_P2.out++ --> {  delay = 0ms; } --> C_T3.in++;
        C_T3.out++ --> {  delay = 0ms; } --> U_P0.in++;
        C_P0.out++ --> {  delay = 0ms; } --> C_T0.in++;
        C_T0.out++ --> {  delay = 0ms; } --> C_P1.in++;
        C_P1.out++ --> {  delay = 0ms; } --> C_T1.in++;
        C_P1.out++ --> {  delay = 0ms; } --> C_T2.in++;
        C_T2.out++ --> {  delay = 0ms; } --> S_P0.in++;
        C_T1.out++ --> {  delay = 0ms; } --> U_P0.in++;
        U_T0.out++ --> {  delay = 0ms; } --> C_P0.in++;
}
