#! /usr/bin/env python


import os

###############################################################
def get_n_molecules():

    fhi = open('results.table')
    n = len(fhi.readlines())-1
    fhi.close()
    return n

###############################################################
def logp_parsing(n):

    fho = open('log_sorted.txt','w')
    fhi = open('results.table')
    
    more_m5 = []
    m4_m5 = []
    m3_m4 = []
    m2_m3= []
    m1_m2 = []
    m1_p0 = []
    p0_p1 = []
    p1_p2 = []
    p2_p3 = []
    p3_p4 = []
    p4_p5 = []
    p5_p6 = []
    p6_p7 = []
    p7_p8 = []
    p8_p9 = []
    more_9 = []
    NotCalculated = []
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        col = s[3]
        if col == 'None':
            NotCalculated.append(col)
        else:
            logp = float(s[3])
            
            if logp < -5:
                more_m5.append(id)
                
            if logp <-4 and logp >-5:
                m4_m5.append(id)
                
            if logp <-3 and logp >-4:
                m3_m4.append(id)
                    
            if logp <-2 and logp >-3:
                m2_m3.append(id)
                        
            if logp <-1 and logp >-2:
                m1_m2.append(id)
                
            if logp <0 and logp >-1:
                m1_p0.append(id)
                                
            if logp <1 and logp >0:
                p0_p1.append(id)

            if logp <2 and logp >1:
                p1_p2.append(id)
         
            if logp <3 and logp >2:
                p2_p3.append(id)
        
            if logp <4 and logp >3:
                p3_p4.append(id)
        
            if logp <5 and logp >4:
                p4_p5.append(id)
        
            if logp <6 and logp >5:
                p5_p6.append(id)

            if logp <7 and logp >6:
                p6_p7.append(id)

            if logp <7 and logp >8:
                p7_p8.append(id)

            if logp <9 and logp >8:
                p8_p9.append(id)
        
            if logp >9:
                more_9.append(id)



    fho.write('1\t'+str(len(more_m5)*100.0/n)+'\n')
    fho.write('2\t'+str(len(m4_m5)*100.0/n)+'\n')
    fho.write('3\t'+str(len(m3_m4)*100.0/n)+'\n')
    fho.write('4\t'+str(len(m2_m3)*100.0/n)+'\n')
    fho.write('5\t'+str(len(m1_m2)*100.0/n)+'\n')
    fho.write('6\t'+str(len(m1_p0)*100.0/n)+'\n')
    fho.write('7\t'+str(len(p0_p1)*100.0/n)+'\n')
    fho.write('8\t'+str(len(p1_p2)*100.0/n)+'\n')
    fho.write('9\t'+str(len(p2_p3)*100.0/n)+'\n')
    fho.write('10\t'+str(len(p3_p4)*100.0/n)+'\n')
    fho.write('11\t'+str(len(p4_p5)*100.0/n)+'\n')
    fho.write('12\t'+str(len(p5_p6)*100.0/n)+'\n')
    fho.write('13\t'+str(len(p6_p7)*100.0/n)+'\n')
    fho.write('14\t'+str(len(p7_p8)*100.0/n)+'\n')
    fho.write('15\t'+str(len(p8_p9)*100.0/n)+'\n')
    fho.write('16\t'+str(len(more_9)*100.0/n)+'\n')
    fho.write('17\t'+str(len(NotCalculated)*100.0/n)+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('log_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]
    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()
    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "LogPDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics border in scale 0,0 nomirror offset character 0, 0, 0\n')
    fho_gnu.write('set xtics rotate -45 ("  <-5  " 1," -5:-4  " 2," -4:-3  " 3,"  -3:-2  " 4," -2:-1  " 5," -1:0  " 6," 0:1  " 7, " 1:2  " 8," 2:3  " 9," 3:4  " 10," 4:5  " 11, " 5:6  " 12," 6:7  " 13," 7:8  " 14,"  8:9  " 15,"  >9  " 16," Not calc." 17)\n')
    fho_gnu.write('set title "LogP Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "log_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('log_sorted.txt')



   
###############################################################
def mw_parsing(n):

    fho = open('mw_sorted.txt','w')
    fhi = open('results.table')
    
    less_40 = []
    p40_p80 = []
    p80_p120 = []
    p120_p160 = []
    p160_p200 = []
    p200_p240 = []
    p240_p280 = []
    p280_p320 = []
    p320_p360 = []
    p360_p400 = []
    p400_p440 = []
    p440_p480 = []
    p480_p520 = []
    p520_p560 = []
    p560_p600 = []
    p600_p640 = []
    p640_p680 = []
    p680_p720 = []
    p720_p760 = []
    p760_p800 = []
    more_800 = []

    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        mw = float(s[2])

        if mw < 40:
            less_40.append(id)

        if mw <80 and mw >40:
            p40_p80.append(id)
            
        if mw <120 and mw >80:
            p80_p120.append(id)
        
        if mw <160 and mw >120:
            p120_p160.append(id)
                
        if mw <200 and mw >160:
            p160_p200.append(id)
                   
        if mw <240 and mw >200:
            p200_p240.append(id)
                       
        if mw <280 and mw >240:
            p240_p280.append(id)
                            
        if mw <320 and mw >280:
            p280_p320.append(id)

        if mw <360 and mw >320:
            p320_p360.append(id)

        if mw <400 and mw >360:
            p360_p400.append(id)
            
        if mw <440 and mw >400:
            p400_p440.append(id)

        if mw <480 and mw >440:
            p440_p480.append(id)
        
        if mw <520 and mw >480:
            p480_p520.append(id)
        
        if mw <560 and mw >520:
            p520_p560.append(id)
        
        if mw <600 and mw >560:
            p560_p600.append(id)

        if mw <640 and mw >600:
            p600_p640.append(id)

        if mw <680 and mw >640:
            p640_p680.append(id)

        if mw <720 and mw >680:
            p680_p720.append(id)

        if mw <760 and mw >720:
            p720_p760.append(id)

        if mw <800 and mw >760:
            p760_p800.append(id)
                  
        if mw >800:
            more_800.append(id)

    fho.write('1\t'+str(len(less_40)*100.0/n)+'\n')
    fho.write('2\t'+str(len(p40_p80)*100.0/n)+'\n')
    fho.write('3\t'+str(len(p80_p120)*100.0/n)+'\n')
    fho.write('4\t'+str(len(p120_p160)*100.0/n)+'\n')
    fho.write('5\t'+str(len(p160_p200)*100.0/n)+'\n')
    fho.write('6\t'+str(len(p200_p240)*100.0/n)+'\n')
    fho.write('7\t'+str(len(p240_p280)*100.0/n)+'\n')
    fho.write('8\t'+str(len(p280_p320)*100.0/n)+'\n')
    fho.write('9\t'+str(len(p320_p360)*100.0/n)+'\n')
    fho.write('10\t'+str(len(p360_p400)*100.0/n)+'\n')
    fho.write('11\t'+str(len(p400_p440)*100.0/n)+'\n')
    fho.write('12\t'+str(len(p440_p480)*100.0/n)+'\n')
    fho.write('13\t'+str(len(p480_p520)*100.0/n)+'\n')
    fho.write('14\t'+str(len(p520_p560)*100.0/n)+'\n')
    fho.write('15\t'+str(len(p560_p600)*100.0/n)+'\n')
    fho.write('16\t'+str(len(p600_p640)*100.0/n)+'\n')
    fho.write('17\t'+str(len(p640_p680)*100.0/n)+'\n')
    fho.write('18\t'+str(len(p680_p720)*100.0/n)+'\n')
    fho.write('19\t'+str(len(p720_p760)*100.0/n)+'\n')
    fho.write('20\t'+str(len(p760_p800)*100.0/n)+'\n')
    fho.write('21\t'+str(len(more_800)*100.0/n)+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('mw_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()

    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "MolecularWeightDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics border in scale 0,0 nomirror offset character 0, 0, 0\n')
    fho_gnu.write('set xtics rotate -45 ("    <40    " 1,"  40 - 80 " 2,"  80 -  120 " 3,"  120 - 160 " 4,"  160 - 200 " 5,"  200 - 240 " 6,"  240 - 280 " 7,"  280 - 320 " 8, "  320 - 360 " 9,"  360 - 400 " 10,"  400 - 440 " 11,"  440 - 480 " 12, "  480 - 520 " 13,"  520 - 560 " 14,"  560 - 600 " 15,"  600 - 640 " 16,"  640 - 680 " 17,"  680 - 720 " 18,"  720 - 760 " 19,"  760 - 800 " 20,"    >800   " 21)\n')
    fho_gnu.write('set title "Molecular Weight Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "mw_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('mw_sorted.txt') 


    
###############################################################
def psa_parsing(n):

    fho = open('psa_sorted.txt','w')
    fhi = open('results.table')
    
    p0_p15 = []
    p15_p30 = []
    p30_p45 = []
    p45_p60 = []
    p60_p75 = []
    p75_p90 = []
    p90_p105 = []
    p105_p120 = [] 
    p120_p135 = []
    p135_p150 = []
    p150_p165 = []
    p165_p180 = []
    p180_p195 = []
    p195_p210 = []
    p210_p225 = []
    p225_p240 = []
    p240_p255 = []
    p255_p270 = []
    p270_p285 = []
    p285_p300 = []
    p_more = []
    
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        psa = float(s[4])

        if psa <15 and psa >0:
            p0_p15.append(id)
        
        if psa <30 and psa >15:
            p15_p30.append(id)

        if psa <45 and psa >30:
            p30_p45.append(id)
        
        if psa <60 and psa >45:
            p45_p60.append(id)
                
        if psa <75 and psa >60:
            p60_p75.append(id)
                   
        if psa <90 and psa >75:
            p75_p90.append(id)
                       
        if psa <105 and psa >90:
            p90_p105.append(id)
                            
        if psa <120 and psa >105:
            p105_p120.append(id)

        if psa <135 and psa >120:
            p120_p135.append(id)
         
        if psa <150 and psa >135:
            p135_p150.append(id)
        
        if psa <165 and psa >150:
            p150_p165.append(id)
            
        if psa <180 and psa >165:
            p165_p180.append(id)
                  
        if psa <195 and psa >180:
            p180_p195.append(id)
                   
        if psa <210 and psa >195:
            p195_p210.append(id)
            
        if psa <225 and psa >210:
            p210_p225.append(id)

        if psa <240 and psa >225:
            p225_p240.append(id)
            
        if psa <255 and psa >240:
            p240_p255.append(id)
            
        if psa <270 and psa >255:
            p255_p270.append(id)
            
        if psa <285 and psa >270:
            p270_p285.append(id)

        if psa <300 and psa >285:
            p285_p300.append(id)
            
        if psa >300:
            p_more.append(id)
         
            
           
    fho.write('1\t'+str(len(p0_p15)*100.0/n)+'\n')
    fho.write('2\t'+str(len(p15_p30)*100.0/n)+'\n')
    fho.write('3\t'+str(len(p30_p45)*100.0/n)+'\n')
    fho.write('4\t'+str(len(p45_p60)*100.0/n)+'\n')
    fho.write('5\t'+str(len(p60_p75)*100.0/n)+'\n')
    fho.write('6\t'+str(len(p75_p90)*100.0/n)+'\n')
    fho.write('7\t'+str(len(p90_p105)*100.0/n)+'\n')
    fho.write('8\t'+str(len(p105_p120)*100.0/n)+'\n')
    fho.write('9\t'+str(len(p120_p135)*100.0/n)+'\n')
    fho.write('10\t'+str(len(p135_p150)*100.0/n)+'\n')
    fho.write('11\t'+str(len(p150_p165)*100.0/n)+'\n')
    fho.write('12\t'+str(len(p165_p180)*100.0/n)+'\n')
    fho.write('13\t'+str(len(p180_p195)*100.0/n)+'\n')
    fho.write('14\t'+str(len(p195_p210)*100.0/n)+'\n')
    fho.write('15\t'+str(len(p210_p225)*100.0/n)+'\n')
    fho.write('16\t'+str(len(p225_p240)*100.0/n)+'\n')
    fho.write('17\t'+str(len(p240_p255)*100.0/n)+'\n')
    fho.write('18\t'+str(len(p255_p270)*100.0/n)+'\n')
    fho.write('19\t'+str(len(p270_p285)*100.0/n)+'\n')          
    fho.write('20\t'+str(len(p285_p300)*100.0/n)+'\n')
    fho.write('21\t'+str(len(p_more)*100.0/n)+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('psa_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()

    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "tPSADistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics border in scale 0,0 nomirror offset character 0, 0, 0\n')
    fho_gnu.write('set xtics rotate -45 (" 0 - 15 " 1," 15 - 30 " 2," 30 - 45 " 3," 45 - 60 " 4," 60 - 75 " 5," 75 - 90 " 6," 90 - 105 " 7, " 105 - 120 " 8," 120 - 135 " 9," 135 - 150 " 10," 150 - 165 " 11," 165 - 180 " 12," 180 - 195 " 13," 195 - 210 " 14," 210 - 225 " 15," 225 - 240 " 16," 240 - 255 " 17," 255 - 270 " 18," 270 - 285 " 19," 285 - 300 " 20," > 300 " 21)\n')
    fho_gnu.write('set title "tPSA Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "psa_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('psa_sorted.txt')


###############################################################
def rigid_parsing(n):

    fho = open('rigid_sorted.txt','w')
    fhi = open('results.table')
    
    rg1 = []
    rg2 = []
    rg3 = []
    rg4 = []
    rg5 = []
    rg6 = []
    rg7 = []
    rg8 = []
    rg9 = []
    rg10 = []
    rg11 = []
    rg12 = []
    rg13 = []
    rg14 = []
    rg15 = []
    rg16 = []
    rg17 = []
    rg18 = []
    
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        rgb = int(s[6])
        
        if rgb == 0:
            rg1.append(id)
        if rgb == 1 or rgb == 2:
            rg2.append(id)
        if rgb == 3 or rgb == 4:
            rg3.append(id)
        if rgb == 5 or rgb == 6:
            rg4.append(id)  
        if rgb == 7 or rgb == 8:
            rg5.append(id)
        if rgb == 9 or rgb == 10:
            rg6.append(id)
        if rgb == 11 or rgb == 12:
            rg7.append(id)
        if rgb == 13 or rgb == 14:
            rg8.append(id)
        if rgb == 15 or rgb == 16:
            rg9.append(id)
        if rgb == 17 or rgb == 18:
            rg10.append(id)
        if rgb == 19 or rgb == 20:
            rg11.append(id)
        if rgb == 21 or rgb == 22:
            rg12.append(id)
        if rgb == 23 or rgb == 24:
            rg13.append(id)
        if rgb == 25 or rgb == 26:
            rg14.append(id)
        if rgb == 27 or rgb == 28:
            rg15.append(id)
        if rgb == 29 or rgb == 30:
            rg16.append(id)
        if rgb == 31 or rgb == 32:
            rg17.append(id)
        if rgb > 32:
            rg18.append(id)
            
    fho.write('1\t'+str(len(rg1)*100.0/n)+'\n')
    fho.write('2\t'+str(len(rg2)*100.0/n)+'\n')
    fho.write('3\t'+str(len(rg3)*100.0/n)+'\n')
    fho.write('4\t'+str(len(rg4)*100.0/n)+'\n')
    fho.write('5\t'+str(len(rg5)*100.0/n)+'\n')
    fho.write('6\t'+str(len(rg6)*100.0/n)+'\n')
    fho.write('7\t'+str(len(rg7)*100.0/n)+'\n')
    fho.write('8\t'+str(len(rg8)*100.0/n)+'\n')
    fho.write('9\t'+str(len(rg9)*100.0/n)+'\n')
    fho.write('10\t'+str(len(rg10)*100.0/n)+'\n')
    fho.write('11\t'+str(len(rg11)*100.0/n)+'\n')
    fho.write('12\t'+str(len(rg12)*100.0/n)+'\n')
    fho.write('13\t'+str(len(rg13)*100.0/n)+'\n')
    fho.write('14\t'+str(len(rg14)*100.0/n)+'\n')
    fho.write('15\t'+str(len(rg15)*100.0/n)+'\n')
    fho.write('16\t'+str(len(rg16)*100.0/n)+'\n')
    fho.write('17\t'+str(len(rg17)*100.0/n)+'\n')
    fho.write('18\t'+str(len(rg18)*100.0/n)+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('rigid_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()
    
    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "RigidBondsDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics scale 0.0 (" 0 " 1,"1-2" 2,"3-4" 3,"5-6" 4,"7-8" 5,"9-10" 6,"11-12" 7, "13-14" 8,"15-16" 9,"17-18" 10,"19-20" 11,"21-22" 12,"23-24" 13,"25-26" 14,"27-28" 15,"29-30" 16,"31-32" 17,"More" 18)\n')
    fho_gnu.write('set title "Rigid Bonds Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "rigid_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('rigid_sorted.txt')

###############################################################
def rotatable_parsing(n):

    fho = open('rotatable_sorted.txt','w')
    fhi = open('results.table')
    
    r0 = []
    r1 = []
    r2 = []
    r3 = []
    r4 = []
    r5 = []
    r6 = []
    r7 = []
    r8 = []
    r9 = []
    r10 = []
    r11 = []
    r12 = []
    r13 = []
    r14 = []
    r15 = []
    r_more = []
    
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        rotb = int(s[5])
        
        if rotb == 0:
            r0.append(id)
        if rotb == 1:
            r1.append(id)
        if rotb == 2:
            r2.append(id)
        if rotb == 3:
            r3.append(id)
        if rotb == 4:
            r4.append(id)
        if rotb == 5:
            r5.append(id)
        if rotb == 6:
            r6.append(id)
        if rotb == 7:
            r7.append(id)
        if rotb == 8:
            r8.append(id)
        if rotb == 9:
            r9.append(id)
        if rotb == 10:
            r10.append(id)
        if rotb == 11:
            r11.append(id)
        if rotb == 12:
            r12.append(id)
        if rotb == 13:
            r13.append(id)
        if rotb == 14:
            r14.append(id)
        if rotb == 15:
            r15.append(id)

        if rotb >15:
            r_more.append(id)
            
    fho.write('1\t'+str(len(r0)*100.0/n)+'\n')
    fho.write('2\t'+str(len(r1)*100.0/n)+'\n')
    fho.write('3\t'+str(len(r2)*100.0/n)+'\n')
    fho.write('4\t'+str(len(r3)*100.0/n)+'\n')
    fho.write('5\t'+str(len(r4)*100.0/n)+'\n')
    fho.write('6\t'+str(len(r5)*100.0/n)+'\n')
    fho.write('7\t'+str(len(r6)*100.0/n)+'\n')
    fho.write('8\t'+str(len(r7)*100.0/n)+'\n')
    fho.write('9\t'+str(len(r8)*100.0/n)+'\n')
    fho.write('10\t'+str(len(r9)*100.0/n)+'\n')
    fho.write('11\t'+str(len(r10)*100.0/n)+'\n')
    fho.write('12\t'+str(len(r11)*100.0/n)+'\n')
    fho.write('13\t'+str(len(r12)*100.0/n)+'\n')
    fho.write('14\t'+str(len(r13)*100.0/n)+'\n')
    fho.write('15\t'+str(len(r14)*100.0/n)+'\n')
    fho.write('16\t'+str(len(r15)*100.0/n)+'\n')
    fho.write('17\t'+str(len(r_more)*100.0/n)+'\n')
    
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('rotatable_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()

    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "RotatableBondsDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics scale 0.0 ("0" 1,"1" 2,"2" 3,"3" 4,"4" 5,"5" 6,"6" 7, "7" 8,"8" 9,"9" 10,"10" 11,"11" 12,"12" 13,"13" 14,"14" 15,"15" 16,">15" 17)\n')
    fho_gnu.write('set title "Rotatable Bonds Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "rotatable_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('rotatable_sorted.txt')


###############################################################
def HBD_parsing(n):

    fho = open('HbondDonnors_sorted.txt','w')
    fhi = open('results.table')
    
    hbd0 = []
    hbd1 = []
    hbd2 = []
    hbd3 = []
    hbd4 = []
    hbd5 = []
    hbd6 = []
    hbd7 = []
    hbd8 = []
    hbd9 = []
    hbd10 = []
    hbdmore = []

    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        hbd = int(s[7])
        
        if hbd == 0:
            hbd0.append(id)
        if hbd == 1:
            hbd1.append(id)
        if hbd == 2:
            hbd2.append(id)
        if hbd == 3:
            hbd3.append(id)
        if hbd == 4:
            hbd4.append(id)
        if hbd == 5:
            hbd5.append(id)
        if hbd == 6:
            hbd6.append(id)
        if hbd == 7:
            hbd7.append(id)
        if hbd == 8:
            hbd8.append(id)
        if hbd == 9:
            hbd9.append(id)
        if hbd == 10:
            hbd10.append(id)
        if hbd > 10:
            hbdmore.append(id)
            
            
                     
    fho.write('1\t'+str(len(hbd0)*100.0/n)+'\n')
    fho.write('2\t'+str(len(hbd1)*100.0/n)+'\n')
    fho.write('3\t'+str(len(hbd2)*100.0/n)+'\n')
    fho.write('4\t'+str(len(hbd3)*100.0/n)+'\n')
    fho.write('5\t'+str(len(hbd4)*100.0/n)+'\n')
    fho.write('6\t'+str(len(hbd5)*100.0/n)+'\n')
    fho.write('7\t'+str(len(hbd6)*100.0/n)+'\n')
    fho.write('8\t'+str(len(hbd7)*100.0/n)+'\n')
    fho.write('9\t'+str(len(hbd8)*100.0/n)+'\n')
    fho.write('10\t'+str(len(hbd9)*100.0/n)+'\n')
    fho.write('11\t'+str(len(hbd10)*100.0/n)+'\n')
    fho.write('12\t'+str(len(hbdmore)*100.0/n)+'\n')
    fho.close()
    fhi.close()


    list_results = []
    fhi = open('HbondDonnors_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()

    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "HBondDonnorsDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"35" 35,"40" 40,"45" 45,"50" 50,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics border in scale 0,0 nomirror offset character 0, 0, 0\n')
    fho_gnu.write('set xtics ("0" 1,"1" 2,"2" 3,"3" 4,"4" 5,"5" 6,"6" 7,"7" 8,"8" 9,"9" 10,"10" 11,"More" 12)\n')
    fho_gnu.write('set title "H-Bond Donnors Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "HbondDonnors_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('HbondDonnors_sorted.txt')

###############################################################
def HBA_parsing(n):

    fho = open('HbondAcceptors_sorted.txt','w')
    fhi = open('results.table')
    
    hba0 = []
    hba1 = []
    hba2 = []
    hba3 = []
    hba4 = []
    hba5 = []
    hba6 = []
    hba7 = []
    hba8 = []
    hba9 = []
    hba10 = []
    hba11 = []
    hbamore = []
        
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        hba = int(s[8])
        
        if hba == 0:
            hba0.append(id)
        if hba == 1:
            hba1.append(id)
        if hba == 2:
            hba2.append(id)
        if hba == 3:
            hba3.append(id)
        if hba == 4:
            hba4.append(id)
        if hba == 5:
            hba5.append(id)
        if hba == 6:
            hba6.append(id)
        if hba == 7:
            hba7.append(id)
        if hba == 8:
            hba8.append(id)
        if hba == 9:
            hba9.append(id)
        if hba == 10:
            hba10.append(id)
        if hba == 11:
            hba11.append(id)
        if hba > 11:
            hbamore.append(id)

    fho.write('1\t'+str(len(hba0)*100.0/n)+'\n')
    fho.write('2\t'+str(len(hba1)*100.0/n)+'\n')
    fho.write('3\t'+str(len(hba2)*100.0/n)+'\n')
    fho.write('4\t'+str(len(hba3)*100.0/n)+'\n')
    fho.write('5\t'+str(len(hba4)*100.0/n)+'\n')
    fho.write('6\t'+str(len(hba5)*100.0/n)+'\n')
    fho.write('7\t'+str(len(hba6)*100.0/n)+'\n')
    fho.write('8\t'+str(len(hba7)*100.0/n)+'\n')
    fho.write('9\t'+str(len(hba8)*100.0/n)+'\n')
    fho.write('10\t'+str(len(hba9)*100.0/n)+'\n')
    fho.write('11\t'+str(len(hba10)*100.0/n)+'\n')
    fho.write('12\t'+str(len(hba11)*100.0/n)+'\n')
    fho.write('13\t'+str(len(hbamore)*100.0/n)+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('HbondAcceptors_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()
    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "HBondAcceptorsDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"40" 40,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics border in scale 0,0 nomirror offset character 0, 0, 0\n')
    fho_gnu.write('set xtics ("0" 1,"1" 2,"2" 3,"3" 4,"4" 5,"5" 6,"6" 7, "7" 8,"8" 9,"9" 10,"10" 11,"11" 12,"More" 13)\n')
    fho_gnu.write('set title "H-Bond Acceptors Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "HbondAcceptors_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('HbondAcceptors_sorted.txt')
    
     
 ###############################################################
def Rings_parsing(n):

    fho = open('Rings_sorted.txt','w')
    fhi = open('results.table')
    
    ring0 = []
    ring1 = [] 
    ring2 = []
    ring3 = []
    ring4 = []
    ring5 = []
    ring6 = []
    ring7 = []
    ring8 = []
    ring9 = []
    ring10 = []
    morering = []
        
    fhi.readline()
    for lines in fhi:
        s = lines.split('\t')
        id = s[0]
        ring = int(s[9])
        if ring == 0:
            ring0.append(id)
        if ring == 1:
            ring1.append(id)
        if ring == 2:
            ring2.append(id)
        if ring == 3:
            ring3.append(id)
        if ring == 4:
            ring4.append(id)
        if ring == 5:
            ring5.append(id)
        if ring == 6:
            ring6.append(id)
        if ring == 7:
            ring7.append(id)
        if ring == 8:
            ring8.append(id)
        if ring == 9:
            ring9.append(id)
        if ring == 10:
            ring10.append(id)
        if ring > 10:
            morering.append(id)
             
    fho.write('1\t'+str(float(len(ring0))*float(100)/float(n))+'\n')
    fho.write('2\t'+str(float(len(ring1))*float(100)/float(n))+'\n')
    fho.write('3\t'+str(float(len(ring2))*float(100)/float(n))+'\n')
    fho.write('4\t'+str(float(len(ring3))*float(100)/float(n))+'\n')
    fho.write('5\t'+str(float(len(ring4))*float(100)/float(n))+'\n')
    fho.write('6\t'+str(float(len(ring5))*float(100)/float(n))+'\n')
    fho.write('7\t'+str(float(len(ring6))*float(100)/float(n))+'\n')
    fho.write('8\t'+str(float(len(ring7))*float(100)/float(n))+'\n')
    fho.write('9\t'+str(float(len(ring8))*float(100)/float(n))+'\n')
    fho.write('10\t'+str(float(len(ring9))*float(100)/float(n))+'\n')
    fho.write('11\t'+str(float(len(ring10))*float(100)/float(n))+'\n')
    fho.write('12\t'+str(float(len(morering))*float(100)/float(n))+'\n')
    fho.close()
    fhi.close()

    list_results = []
    fhi = open('Rings_sorted.txt')
    for lines in fhi:
        list_results.append(float(lines.split()[1]))
    list_results.sort()
    max = list_results[-1]

    max_percent = max*1.2
    if max_percent >= 100:
        max_percent = 100
    fhi.close()

    
    fho_gnu = open('plotplot','w')
    fho_gnu.write('unset key\n')
    fho_gnu.write('set output "RingsDistribution.png"\n')
    fho_gnu.write('set boxwidth 0.9 absolute\n')
    fho_gnu.write('set style fill  solid 0.20 border -1\n')
    fho_gnu.write('set ytics nomirror ("0" 0,"5" 5,"10" 10,"15" 15,"20" 20,"25" 25,"30" 30,"35" 35,"40" 40,"45" 45,"50" 50,"60" 60,"80" 80,"100" 100)\n')
    line_yrange = 'set yrange [ 0:'+str(max_percent)+' ]\n'
    fho_gnu.write(line_yrange)
    fho_gnu.write('set xtics scale 0.0 ("0" 1,"1" 2,"2" 3,"3" 4,"4" 5,"5" 6,"6" 7, "7" 8,"8" 9,"9" 10,"10" 11,"More" 12)\n')
    fho_gnu.write('set title "Number of Rings Distribution"\n')
    fho_gnu.write('set terminal png large size 1024,768 linewidth 2\n')
    fho_gnu.write('plot "Rings_sorted.txt" with boxes\n')
    fho_gnu.write('set output')
    fho_gnu.close()
    os.system('gnuplot "plotplot"')
    os.remove('plotplot')
    os.remove('Rings_sorted.txt')


if __name__ == '__main__':
    
    n = get_n_molecules()
    logp_parsing(n)
    mw_parsing(n)
    psa_parsing(n)
    rigid_parsing(n)
    rotatable_parsing(n)
    HBD_parsing(n)
    HBA_parsing(n)
    Rings_parsing(n)
    
