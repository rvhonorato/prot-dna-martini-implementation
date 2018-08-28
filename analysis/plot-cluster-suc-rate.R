setwd('/Users/rvhonorato/alc-data/CG-ProteinDNA-Benchmark/')

df.aa = read.csv('run3_water_cluster_success_rate.csv',check.names = T)
df.cg = read.csv('run4_water_cluster_success_rate.csv',check.names = T)

rownames(df.aa) = c('acceptable','medium','high')
rownames(df.cg) = c('acceptable','medium','high')

df.aa$X=NULL
df.cg$X=NULL

colnames(df.aa) = c(1,5,10,50,100,200)
colnames(df.cg) = c(1,5,10,50,100,200)

par(mfrow=c(1,2))
barplot(as.matrix(df.aa), ylim=c(0,100),
        col=c('springgreen3','royalblue','darkgoldenrod1'),
        ylab='Success Rate',
        xlab='Top',
        main = 'AA #1 cluster',beside=T)

legend("topleft", inset=.01,
       c("Acceptable", "Medium","High"), 
       fill=c('springgreen3','royalblue','darkgoldenrod1'), 
       horiz=F, cex=0.8)

barplot(as.matrix(df.cg),ylim=c(0,100),
        col=c('springgreen3','royalblue','darkgoldenrod1'),
        ylab='Success Rate',
        xlab='Top',
        main='CG #1 cluster',beside=T)

legend("topleft", inset=.01,
       c("Acceptable", "Medium","High"), 
       fill=c('springgreen3','royalblue','darkgoldenrod1'), 
       horiz=F, cex=0.8)
