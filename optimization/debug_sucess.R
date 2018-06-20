setwd('~/alc-data/benchmark')

df = read.csv('sucess.debug',sep=' ',header=T,check.names=F)
df[,1] = NULL



a = as.data.frame(t(df))
