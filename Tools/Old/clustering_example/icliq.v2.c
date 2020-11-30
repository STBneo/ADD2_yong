#include         <stdio.h>
#include         <stdlib.h>
#include         <unistd.h>
#include         <math.h>
#include         <string.h>
#define	MAXNC	  3000000	/* max. number of clusters */
typedef struct  {
	int bgn;	/* beginning number */
	int nm;		/* number of members */
	int nsc;	/* number of sub-clusters */
} mc_t;
mc_t 	mainc[MAXNC];
int	*org,*sorted,*nbor,*nnbor,*nbgn,ndots,nmc,*zdist,MAXND;
int	cutoff;

/*-------------------------------------------------------*/
/*
	Read z_dist matrix and establish and find all neighbor relations.
*/
int     sort_nn(char fname[])
{
	FILE	*infile,*fopen();
	int	i,j,k,m,input,*nb,a,b,oldm,neigh,*found,start;
	int	total[2], *bt, *bit, *bits, NP, np;
	char    db[120];

	mc_t	*pmc;
	pmc = mainc; 

       	strcpy(db,fname);
       	strcat(db,".idx.xcliq");
                                                                                                               
       	infile = fopen(db,"r");
	if(!infile){
		fprintf(stdout,"Failed to read %s ", db);
                return 0;
        }

	fread(total,sizeof(int),2,infile);
        NP = total[0]; // old serial
	np = total[1]; // new serial
	
	MAXND = np * np * 2;
        if ((bit=(int *)malloc((np)*sizeof(int))) == NULL) return 0;
        if ((bits=(int *)malloc((np)*sizeof(int))) == NULL) return 0;
	if ((bt=(int *)malloc((np)*sizeof(int))) == NULL) return 0;
        if ((nbor = (int *)malloc((MAXND)*sizeof(int))) == NULL) return 0;
        if ((org = (int *)malloc((NP)*sizeof(int))) == NULL) return 0;
        if ((sorted = (int *)malloc((NP)*sizeof(int))) == NULL) return 0;
        if ((nnbor= (int *)malloc((NP)*sizeof(int))) == NULL) return 0;
        if ((nbgn = (int *)malloc((NP)*sizeof(int))) == NULL) return 0;
        if ((found = (int *)malloc((NP)*sizeof(int))) == NULL) return 0;

	fread(bit ,sizeof(int),np,infile);
        fread(bits,sizeof(int),np,infile);

 	fclose(infile);

/* read z-dist list */
	strcpy(db,fname);
        strcat(db,".bin.xcliq");
                                                                                                               
        infile = fopen(db,"r");
        if(!infile){
                fprintf(stdout,"Failed to read %s ", db);
                return 0;
        }
/* make neighbor list */
	ndots = 0;
	nb = nbor;
	for (i = 0; i < np; i++) {
		input = i; 
		fseek(infile,(bits[input]-bit[input])*4,0);
		fread(bt,sizeof(int),bit[input],infile);
		nbgn[bt[0]] = ndots;
// printf("%d %d %d  nbgn[bt[0]]: %d ", i, bits[input],bit[input], ndots);
		for(k=1;k<bit[input];k++){
			if (ndots >= MAXND) {
fprintf(stdout,"Total number of neighbor relations exceeds MAXND\n");
return 0;
			}
			*nb++ = bt[k];
			ndots++;
		}
		nnbor[bt[0]] = ndots - nbgn[bt[0]];
	}
	// fprintf(stdout,"Total number of neighbor relations = %d %d\n", ndots,NP); 
	fclose(infile);
/* sorting */
	for (i = 0; i < NP; i++) org[i] = sorted[i] = i;
	for (a = 0; a < NP; a++) found[a] = 0;
        nmc = m = 0;
	while (m < NP) {
/* find a new starting protein */
                for (a = 0; a < NP; a++) {
                        if (found[a] == 0) {
                                start = a; break;
                        }
                }
		org[m] = start;
		found[start] = 1;
		oldm = m++; 
/* collect all the neighbors, neighbors of neighbors, etc. */
		for (b = oldm; b < m; b++) {
			a = org[b];
			nb = nbor + nbgn[a];
			for (i = 0; i < nnbor[a]; i++, nb++) {
				if (found[*nb]) continue;
				org[m++] = *nb;
				found[*nb] = 1;
			}
		}
		pmc->bgn = oldm;
		pmc->nm = m-oldm;
		nmc++; pmc++;
	}
	for (b = 0; b < NP; b++) {
		sorted[org[b]] = b;
	}
	return 1;
}
/*------------------------------------------------------- */
int	out(char fname[])
{
	FILE    *outfile, *fopen();
	mc_t	*pmc;
	int	c,i,a, n, maxmn=0, count;
	
//	strcat(fname, ".out");
//	outfile=fopen(fname,"w");
	if(!outfile){
		fprintf(stderr,"Failed to write %s. \n", fname);
		return 0;
	}
	for (pmc = mainc, c = 0; c < nmc; c++, pmc++){
		if(pmc->nm>maxmn) maxmn = pmc->nm;
	}
/*
2012.12
first one includes 0, so it was removed.
*/
	count = 0;
	printf("#Group_id  N_of_members members \n");
	for (pmc = mainc+1, c = 1; c < nmc; c++, pmc++) {
		//if(pmc->nm==1) continue;
		printf("%8d %8d ",count+1,pmc->nm);
		for(i=pmc->bgn;i<pmc->bgn+pmc->nm;i++){
			printf("%d ",org[i]);
			//  printf("%8d %8d %d \n",count+1,pmc->nm,org[i]);
		}
		printf("\n");
		count++;
	}
	// fprintf(stdout,"Number of main clusters = %d stored in %s.\n", nmc,fname);
	return 1;
}
/*------------------------------------------------------- */
/* make gplot output file including all neighbor relations
*/
int	gpout(int NP)
{
	FILE    *outfile,*fopen();
	int	*nb;
	int	a, i, j, n;
	n = 0;
	for (i = 0; i < NP; i++) {
		a = org[i];
		nb = nbor + nbgn[a];
		for (j = 0; j < nnbor[a]; j++, nb++) {
			printf("%4d %4d \n", i, sorted[*nb]);
			n++;
		}
	}
	return 1;
     /* printf(" Total number of neighbor relations printed = %d\n", n); */
}
int cda_pip(char fname[]){

	FILE *infile,*outfile;
        int  i,k,l,j,n,m,o,count,nb,b,bit[100000],bits[100000],bt[100000];
        int  total[2],nl,a,*mn, OLD, NEW;
        char db[120];

       infile = fopen(fname,"r");
       if (!infile) {
                printf(" Failed to open : %s\n",fname);
                exit(0);
       }
       strcpy(db,fname);
       strcat(db,".bin.xcliq");

       outfile = fopen(db,"w");
       n = nb = m = o = 0;
       while (1) {
                 if(EOF==fscanf(infile,"%d %d %d",&OLD, &NEW, &nl)) break;
                if((mn =(int *)malloc((nl)*sizeof(int)))==NULL) return 0;
                for(i=0;i<nl;i++) {
                        fscanf(infile,"%d",&mn[i]);
                }
                o = fwrite(mn,sizeof(int),nl,outfile);
                nb += o; bit[NEW] = o; bits[NEW] += nb;
// printf("%d %d \n",  bit[a], bits[a] );
                free(mn);

        }
	fclose(infile);
	fclose(outfile);
	strcpy(db,fname);
        strcat(db,".idx.xcliq");
        outfile = fopen(db,"w");
        total[0]=OLD; total[1]= NEW ;
        fwrite(total,sizeof(int),2,outfile);
        fwrite(bit, sizeof(int),NEW,outfile);
        fwrite(bits,sizeof(int),NEW,outfile);
        fclose(outfile);
	return 1;
}
int  agg_dist(char fname[], char unique_key[]) {
        FILE *infile, *outfile, *fopen();
        char line[120];
        int  i,k,l,j,n,m,count,a,b,c,d,e,np, id;
	int  nclu,max,mini,olda, *kill, *hit;

	infile = fopen(fname,"r");
        if (!infile) {
                printf(" Failed to open : %s\n",fname);
                return 0;
        }
	n = max  = 0; mini = 1000000; 
        while (1) {
                if (!fgets(line, 120,infile)) break;
                sscanf(line,"%d %d",&a,&b);
		if(a>max) max=a;
		if(b>max) max=b;
		if(a<mini) mini=a;
                if(b<mini) mini=b;
	}
	fclose(infile);
	np = max;
	if(mini==0) np++;

	if ((kill = (int *)malloc((np)*sizeof(int))) == NULL) return 0;
	if ((hit = (int *)malloc((np)*sizeof(int))) == NULL) return 0;

        infile = fopen(fname,"r");
        n = 0;  olda = 0; int oldb = 0;
        while (1) {
                if (!fgets(line, 120,infile)) break;
                sscanf(line,"%d %d",&a,&b);
		if(olda >a) {
			fprintf(stdout,"icliq requires sorted input. exit..\n"); 
			exit(1);
		}
		olda = a;
	}
	fclose(infile);

	outfile= fopen(unique_key,"w");
        infile = fopen(fname,"r");
        for(i=0;i<np;i++) {
                hit[i]=0;
        }
        m = n = 0;  olda = -1;
        while (1) {
                if (!fgets(line, 120,infile)) break;
                sscanf(line,"%d %d",&a,&b);
                if(olda == a){
                        hit[n++]=b;
			continue;
                }
                else { 
                        if(olda>=0) {
				fprintf(outfile,"%d %d %d %d ",np, m, n+1, olda);
                        	for(i=0;i<n;i++) {
                                	fprintf(outfile,"%d ",hit[i]);
                        	}
                        	fprintf(outfile," \n");
				m++;
			}
                        for(i=0;i<np;i++) hit[i]=0;
                        n = 0;
                        hit[n++]=b;
                }
                olda = a;
        }
        fprintf(outfile,"%d %d %d %d ",np, m, n+1, olda); 
        for(i=0;i<n;i++) {
                fprintf(outfile,"%d ",hit[i]);
        }
	fprintf(outfile,"\n"); 
	fprintf(outfile,"%d %d %d %d ",np, m+1, n+2, olda+1);

	fclose(outfile);

        return 0;
}

/*------------------------------------------------------- */
int	main(argc, argv)
int 	argc;
char 	*argv[];
{
        FILE    *infile, *fopen();
        char    line[120], key[120], fname[120],fname1[120], *INFILE = NULL;
        int     i, n,  nflags, flag1;
 

	if(argc==3) {
                sscanf(*++argv, "%s", fname);    
		sscanf(*++argv, "%s", key);   
        }
	else {
		fprintf(stderr,"  Usage: cliq [input][unique key] \n");
                fprintf(stderr,"  Input format:  x  y \n");
                fprintf(stderr,"  two intergers: x and y are related each other.\n");
		fprintf(stderr,"  it should be sorted by the first column\n");
		fprintf(stderr,"  it doesn't matter with 0, 1 of the starting serial number \n");
		return 0;
	}
	agg_dist(fname, key);
	cda_pip(key);
	sort_nn(key);
	out(key);
	// system("rm *.xcliq");

   /* process flags 
        nflags = 0; flag1 = 0;
        while((i = getopt(argc,argv,"d:b:c:")) != -1)
        {
                switch(i){
                case 'd':          // distance
                        INFILE = (char *) strdup(optarg); flag1 = 1;
			agg_dist(INFILE);
                        nflags++; break;
                case 'b':          // binery  
                        INFILE = (char *) strdup(optarg); flag1 = 2;
			cda_pip(INFILE);
                        nflags++; break;
                case 'c':          // clustering 
                        INFILE = (char *) strdup(optarg); flag1 = 3;
        		sort_nn(INFILE);
        		out(INFILE);
                        nflags++; break;
                }
        }
        if(!nflags){
                fprintf(stderr,"  Usage: cliq [flag: -d -b -c] [input] \n");
                fprintf(stderr,"  -d: aggresive distance \n");
                fprintf(stderr,"  -b: binary file \n");
                fprintf(stderr,"  -c: exhustive clustering \n");
                return 1;
        }
    */
}
/*-------------------------------------------------------*/
