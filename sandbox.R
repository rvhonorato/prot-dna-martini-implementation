setwd('~/alc')

par(mfrow=c(3,2))

df_it0_cg = read.table('it0_cg_bench.dat',header=T,sep='\t',check.name=F)
df_it0_aa = read.table('it0_aa_bench.dat',header=T,sep='\t',check.name=F)

df_it0_aa$"1QNE" = NULL
df_it0_cg$"1HJC" = NULL
df_it0_cg$"1O3T" = NULL
df_it0_cg$"1H9T" = NULL
df_it0_cg$"1JT0" = NULL

## it0
boxplot(df_it0_cg, las = 2,outline=F,ylim=c(0,20),main = 'it0 CG',ylab='i-RMSD')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_it0_cg, las = 2,outline=F,ylim=c(0,20), main = 'it0 CG')
#
boxplot(df_it0_aa, las = 2,outline=F,ylim=c(0,20),main = 'it0 AA')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_it0_aa, las = 2,outline=F,ylim=c(0,20), main = 'it0 AA')


## it1

df_it1_cg = read.table('it1_cg_bench.dat',header=T,sep='\t',check.name=F)
df_it1_aa = read.table('it1_aa_bench.dat',header=T,sep='\t',check.name=F)

df_it1_aa$"1QNE" = NULL
df_it1_cg$"1HJC" = NULL
df_it1_cg$"1O3T" = NULL
df_it1_cg$"1H9T" = NULL
df_it1_cg$"1JT0" = NULL

boxplot(df_it1_cg, las = 2,outline=F,ylim=c(0,20), main = 'it1 CG',ylab='i-RMSD')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_it1_cg, las = 2,outline=F,ylim=c(0,20), main = 'it1 CG')
#
boxplot(df_it1_aa, las = 2,outline=F,ylim=c(0,20), main = 'it1 AA')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_it1_aa, las = 2,outline=F,ylim=c(0,20), main = 'it1 AA')           

## water
df_water_cg = read.table('water_cg_bench.dat',header=T,sep='\t',check.name=F)
df_water_aa = read.table('water_aa_bench.dat',header=T,sep='\t',check.name=F)

df_water_aa$"1QNE" = NULL
df_water_cg$"1HJC" = NULL
df_water_cg$"1O3T" = NULL
df_water_cg$"1H9T" = NULL
df_water_cg$"1JT0" = NULL


boxplot(df_water_cg, las = 2,outline=F,ylim=c(0,20), main = 'water CG',ylab='i-RMSD')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_water_cg, las = 2,outline=F,ylim=c(0,20), main = 'water CG')
#
boxplot(df_water_aa, las = 2,outline=F,ylim=c(0,20), main = 'water AA')
abline(h=4.0)
abline(v=seq(1,33,1),col='lightgray',lty=3)
# par(new=TRUE)
# boxplot(df_water_aa, las = 2,outline=F,ylim=c(0,20), main = 'water AA')  

