setwd('~/alc/threshold-test/1BY4/')

par(mfrow=c(3,1))

df_it0 = read.table('it0_threshold.csv',header=T,sep=',',check.name=F)
df_it0[,1] = NULL
boxplot(df_it0,outline=F,ylab='i-rmsd',xlab='ctonnb', main ='irmsd vs nb threshold\nit0')


df_it1 = read.table('it1_threshold.csv',header=T,sep=',',check.name=F)
df_it1[,1] = NULL
boxplot(df_it1,outline=F,ylab='i-rmsd',xlab='ctonnb',main='it1')


df_water = read.table('water_threshold.csv',header=T,sep=',',check.name=F)
df_water[,1] = NULL
boxplot(df_water,outline=F,ylab='i-rmsd',xlab='ctonnb',main='water')



