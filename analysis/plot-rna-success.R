# data copied from the spreadsheet
df = data.frame("CG" = c(43.94,	60.61,	66.67,	84.85,	87.88,	89.39,	89.39), 'AA' = c(96.43,	100.00,	100.00,	100.00,	100.00,	100.00,	100.00))

df = data.frame(t(df/100))
colnames(df) = c(1,	5, 10, 50, 100, 400, 1000)
barplot(as.matrix(df), beside =T, xlab='Top',ylab='Success Rate', main = 'it0',ylim=c(0,1))

df = data.frame("CG" = c(28.92,286.66), "AA"=c(634.04,7310.35))
df = data.frame(t(df/60))
colnames(df)= c('it0','it1')
barplot(as.matrix(df), beside =T, xlab='Stage',ylab='Time (min)',main='AA vs CG\n16S + KsgA cpu time')
