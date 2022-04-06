*MARISOL GARROUSTE
*501.023 AND 615 Project

Sets
        g "new generators" /w1*w8, s/
        t "time in hours" /t1*t8760/
        sol(g) "solar generator" /s/
        w(g) "wind generators" /w1*w8/ 
        ;

Parameters
        pFOC(g) "Fixed Operational costs ($/MW-year)" /w1*w8 42000, s 22030/
        pVOLL "Value Of Lost Load ($/MWh)" /9000/
        pCC(g) "Annualized capital costs ($/MW AC)" /w1*w8 1262000,s 1230000/
        ;


*Do not indent or modify any part of this parameter declaration.
Parameter pDemand(t) "Hourly demand MISO scaled down to 1000MW"
/
$ondelim
$include demand2018MISO1000MW.csv
$offdelim
/
;

*Do not indent or modify any part of this parameter declaration.
Parameter pCFSolar(sol,t)
/
$ondelim
$include solarCFBaraga.csv
$offdelim
/
;

*Do not indent or modify any part of this parameter declaration.
Parameter pCFWind(t,w)
/
$ondelim
$include windCF.csv
$offdelim
/;

Variables
        vZ
        ;

Positive variables
        vCap(g)
        vP(g,t)
        nse
        ;

Equations
        eObjFunc
        eMeetDemand(t)
        eMaxGenWind(w,t)
        eMaxGenSolar(sol,t)
        ;

eObjFunc.. vZ =e= sum(g,pCC(g)*vCap(g))+ sum(g,pFOC(g)*vCap(g))+nse*pVOLL;
eMeetDemand(t).. sum(g,vP(g,t))+nse =e= pDemand(t);
eMaxGenWind(w,t).. vP(w,t) =l= pCFWind(t,w)*vCap(w);
eMaxGenSolar(sol,t).. vP(sol,t) =l= pCFSolar(sol,t)*vCap(sol);

Model dispatch includes all equations /all/;
Solve dispatch using lp minimizing vZ;

execute_unload "results.gdx" vP.l vCap.l eMeetDemand.m nse.l
execute 'gdxxrw.exe results.gdx o=results.xlsx var=vP.l rng=Generation!a1'
execute 'gdxxrw.exe results.gdx o=results.xlsx var=vCap.l rng=Capacities!a1'
execute 'gdxxrw.exe results.gdx o=results.xlsx equ=eMeetDemand.m rng=Prices!a1'
execute 'gdxxrw.exe results.gdx o=results.xlsx var=nse.l rng=NSE!a1'



