setwd('~/alc/dna-benchmark')

par(mfrow=c(2,1))

#df_it0_cg = read.table('it0_aa_cpu_bench.dat',header=T,check.names=F)
#df_it0_aa = read.table('it0_cg_cpu_bench.dat',header=T,check.names=F)

#df_it0_cg = read.table('act-pass-nodesol_it0_cpu_bench.dat',header=T,check.names=F)
#df_it0_aa = read.table('run1_it0_cpu_bench.dat',header=T,check.names=F)

df_it0_aa = read.table('run3_it0_cpu_bench.dat',header=T,check.names=F)
df_it0_cg = read.table('run4_it0_cpu_bench.dat',header=T,check.names=F)



df.size = read.table('run4_p_size.dat', header=T)
#df.size = df.size[df.size$complex!="1O3T", ] 

df.size = df.size[order(df.size$atomcount,decreasing=T),]

#setdiff(colnames(df_it0_aa), colnames(df_it0_cg))
#setdiff(colnames(df_it0_cg), colnames(df_it0_aa))

#df_it0_aa$"1O3T" = NULL

df = rbind(df_it0_cg, df_it0_aa)

target = as.vector(df.size$complex)

#setdiff(colnames(df),target)
#df$"1DFM" = NULL
#setdiff(target, colnames(df))

df = df[,rev(target)]

barplot(as.matrix(df),beside=T,las=2,ylab="CPU time (seconds)",main='it0\n~4.8x faster', legend.text = c("CG","AA"), 
        args.legend = list(x='topleft', inset=c(0.01,0)))

###
#df_it1_cg = read.table('it1_aa_cpu_bench.dat',header=T,check.names=F)
#df_it1_aa = read.table('it1_cg_cpu_bench.dat',header=T,check.names=F)

#df_it1_cg = read.table('act-pass-nodesol_it1_cpu_bench.dat',header=T,check.names=F)
#df_it1_aa = read.table('run1_it1_cpu_bench.dat',header=T,check.names=F)

df_it1_aa = read.table('run3_it1_cpu_bench.dat',header=T,check.names=F)
df_it1_cg = read.table('run4_it1_cpu_bench.dat',header=T,check.names=F)

#df.size = read.table('run1_p_size.dat', header=T)
#df.size = df.size[df.size$complex!="1O3T", ] 
#df.size = df.size[order(df.size$atomcount,decreasing=T),]

#setdiff(colnames(df_it0_aa), colnames(df_it0_cg))
#setdiff(colnames(df_it0_cg), colnames(df_it0_aa))
#df_it1_aa$"1O3T" = NULL

df = rbind(df_it1_cg, df_it1_aa)

target = as.vector(df.size$complex)

setdiff(colnames(df),target)
setdiff(target, colnames(df))

df = df[,rev(target)]

barplot(as.matrix(df),beside=T,las=2,ylab="CPU time (seconds)",main='it1\n~7.5x faster', legend.text = c("CG","AA"), 
        args.legend = list(x='topleft', inset=c(0.01,0)))

mean(as.numeric(df_it0_aa[1,] / df_it0_cg[1,]))
mean(as.numeric(df_it1_aa[1,] / df_it1_cg[1,]))
mean(df.size$atomcount)


#summary(df_it0_aa)
#summary(df_it0_cg)
