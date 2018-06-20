
df = read.csv('nuc.csv')
barplot(as.matrix(df),beside=T,horiz=F,ylab='CPU time (seconds)',main = 'Nucleosome+PRC1\nComputing time comparison',legend.text = c("CG","AA"))
