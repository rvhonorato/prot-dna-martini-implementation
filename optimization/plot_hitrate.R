setwd('~/alc-data/benchmark')

par(mfrow=c(1,1))

df = read.csv('hitrate_it0.csv', check.names = F)
df = df[,-1]

barplot(as.matrix(df),beside=T,ylim=c(0,1), xlab='Top', ylab='Sucess rate',
        legend.text = c("CG","AA"),main='Prot-DNA benchmark (n=34)\nit0')

df = read.csv('hitrate_it1.csv', check.names = F)
df = df[,-1]

barplot(as.matrix(df),beside=T,ylim=c(0,1), xlab='Top', ylab='Sucess rate',
        legend.text = c("CG","AA"),main='Prot-DNA benchmark (n=34)\nit1')

df = read.csv('hitrate_water.csv', check.names = F)
df = df[,-1]

barplot(as.matrix(df),beside=T,ylim=c(0,1), xlab='Top', ylab='Hit rate',
        legend.text = c("CG","AA"),main='Prot-DNA benchmark (n=34)\nwater')

summary(df)
