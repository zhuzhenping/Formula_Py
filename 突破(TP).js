CONST N1=5;CONST N2=10;CONST N3=30;

M1:=MA(C,N1);{短期参数：5}
M2:=MA(C,N2);{中期参数：10}
M3:=MA(C,N3);{长期参数：30}
{以下计算交叉点距今的天数}
D1:=BARSLAST(CROSS(M1,M2));{短上穿中}
D2:=BARSLAST(CROSS(M1,M3));{短上穿长}
D3:=BARSLAST(CROSS(M2,M3));{中上穿长}
T1:=CROSS(M2,M3);{今天中线上穿长线}
T2:=D1>=D2 AND D2>=D3;{交叉按指定的先后出现}
T3:=COUNT(CROSS(M2,M1) OR CROSS(M3,M2) OR CROSS(M3,M1),D1)=0;{中间无夹杂其它交叉}
T4:=REF(M1<M3 AND M2<M3,D1+1);{短上穿中前一天短、中线在长线之下}
JT:T1 AND T2 AND T3 AND T4;{价托确定}