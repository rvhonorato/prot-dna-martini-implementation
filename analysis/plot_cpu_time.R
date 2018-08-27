setwd('/Users/rvhonorato/alc-data/CG-ProteinDNA-Benchmark/')


pdf('cpu-time.pdf')
par(mfrow=c(2,1))

df_it0_aa = read.table('run3_it0_cpu_bench.dat',header=T,check.names=F)
df_it0_cg = read.table('run4_it0_cpu_bench.dat',header=T,check.names=F)

df.size = read.table('run4_p_size.dat', header=T)
df.size = df.size[order(df.size$atomcount,decreasing=T),]

target = as.vector(df.size$complex)

df = rbind(df_it0_cg, df_it0_aa)
df = df[,rev(target)]

barplot(as.matrix(df),beside=F,las=2,ylab="CPU time (seconds)",main='it0', legend.text = c("CG","AA"), 
        args.legend = list(x='topleft', inset=c(0.01,0)), cex.names=0.7, cex.axis=0.7)

###
df_it1_aa = read.table('run3_it1_cpu_bench.dat',header=T,check.names=F)
df_it1_cg = read.table('run4_it1_cpu_bench.dat',header=T,check.names=F)

df = rbind(df_it1_cg, df_it1_aa)

target = as.vector(df.size$complex)

df = df[,rev(target)]

barplot(as.matrix(df),beside=F,las=2,
        ylab="CPU time (seconds)",
        main='it1', 
        legend.text = c("CG","AA"), 
        args.legend = list(x='topleft', inset=c(0.01,0)), cex.names=0.7, cex.axis=0.7)

mean(as.numeric(df_it0_aa[1,] / df_it0_cg[1,]))
mean(as.numeric(df_it1_aa[1,] / df_it1_cg[1,]))

mean(as.numeric(df_it0_cg))
mean(as.numeric(df_it0_aa))

mean(as.numeric(df_it1_aa))
mean(as.numeric(df_it1_cg))

mean(df.size$atomcount)

dev.off()


#summary(df_it0_aa)
#summary(df_it0_cg)
