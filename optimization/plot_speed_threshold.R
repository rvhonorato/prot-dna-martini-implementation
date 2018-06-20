setwd('~/alc/threshold-test/1BY4/')

df = read.table('speed.dat',header=T,sep=',')
e = rbind(df$it0, df$it1, df$water)
barplot(e, horiz=T,names.arg=df$range,las=1,xlab='CPU time (seconds)', ylab='Threshold', main='nb cutoff vs. cpu time\npdb 1by4',
        legend.text = c("it0","it1","water"), 
        args.legend = list(x='bottomright', inset=c(0.1,0.05)))

