df = data.frame("AA" = c(949.0,7310.35), "CG" = c(135.66,634.04))

colnames(df) = c('All atoms','Coarse grain')
df = df/60
barplot(as.matrix(df), beside = T, 
        ylab = 'CPU Time (minutes)', 
        main = '30S rRNA + KsgA\nCPU Time',
        legend.text = c("it0","it1"),axes=F)

axis(side=2, at=seq(0,120,10))
abline(h=c(seq(0,120,20)),col='gray',lty=2)
abline(h=c(10,60),col='red', lty=2)

text(1.5, 20, "15.8'",cex=1.5)
text(2.5, 115, "121.8'",cex=1.5)
text(4.5, 5, "2.26'",cex=1.5)
text(5.5, 14, "10.56'",cex=1.5)
