library(reshape2)

setwd('/Users/rvhonorato/alc-data/CG-ProteinDNA-Benchmark/')

# load the data
bench.df = read.csv('benchmark.csv')
bench.df$X = NULL

# sub-set by run
###
# run1: CG default values
# run2: AA default values
# run3: AA epsilon = 78, w_desol = 0.0
# run4: CG epsilon = 78, w_desol = 0.0
##

#run1.df = bench.df[which(bench.df$run == 'run1'),]
#run2.df = bench.df[which(bench.df$run == 'run2'),]
run3.df = bench.df[which(bench.df$run == 'run3'),]
run4.df = bench.df[which(bench.df$run == 'run4'),]

# sub-set by phase
#run1.it0.df = run1.df[which(run1.df$phase == 'it0'),]
#run2.it0.df = run2.df[which(run2.df$phase == 'it0'),]
run3.it0.df = run3.df[which(run3.df$phase == 'it0'),]
run4.it0.df = run4.df[which(run4.df$phase == 'it0'),]

#run1.it1.df = run1.df[which(run1.df$phase == 'it1'),]
#run2.it1.df = run2.df[which(run2.df$phase == 'it1'),]
run3.it1.df = run3.df[which(run3.df$phase == 'it1'),]
run4.it1.df = run4.df[which(run4.df$phase == 'it1'),]

#run1.water.df = run1.df[which(run1.df$phase == 'water'),]
#run2.water.df = run2.df[which(run2.df$phase == 'water'),]
run3.water.df = run3.df[which(run3.df$phase == 'water'),]
run4.water.df = run4.df[which(run4.df$phase == 'water'),]

# calculate success rate and plot it
###
# sucess rate; number of complexes with at least one conformation below threshold
total = 43 # make sure this is consistent

######################################################################################################
# run3
#=============================#
## water
WtopList = c(1,5,100,200)

Asrates = c()
Msrates = c()
Hsrates = c()

for(i in WtopList){
  Asrates = c(Asrates, length(unique(subset(run3.water.df, rank %in% seq(1,i) & irmsd < 4.0)$name)) / total)
  Msrates = c(Msrates, length(unique(subset(run3.water.df, rank %in% seq(1,i) & irmsd < 2.0)$name)) / total)
  Hsrates = c(Hsrates, length(unique(subset(run3.water.df, rank %in% seq(1,i) & irmsd < 1.0)$name)) / total)
}

run3.water.acc.srates = Asrates
run3.water.med.srates = Msrates
run3.water.high.srates = Hsrates


######################################################################################################
# run4
#=============================#
## water

WtopList = c(1,5,100,200)

Asrates = c()
Msrates = c()
Hsrates = c()

for(i in WtopList){
  #acceptable.models = dim(subset(run4.water.df, rank %in% seq(1,i) & irmsd < 4.0))[1]
  Asrates = c(Asrates, length(unique(subset(run4.water.df, rank %in% seq(1,i) & irmsd < 4.0)$name)) / total)
  Msrates = c(Msrates, length(unique(subset(run4.water.df, rank %in% seq(1,i) & irmsd < 2.0)$name)) / total)
  Hsrates = c(Hsrates, length(unique(subset(run4.water.df, rank %in% seq(1,i) & irmsd < 1.0)$name)) / total)
}

run4.water.acc.srates = Asrates
run4.water.med.srates = Msrates
run4.water.high.srates = Hsrates

######################################################################################################
# Plots
######################################################################################################
# Comparison 1 = run1 x run2 - default values
# Comparison 2 = run4 x run3 - e78 nodesol
#######################################################################################################
# Sucess rate #
comparison2.3 = as.data.frame(t(cbind(run4.water.acc.srates, run3.water.acc.srates)))
colnames(comparison2.3) = WtopList
barplot(as.matrix(comparison2.3), beside=T, xlab='Top',ylab='Success Rate', main = 'water',ylim=c(0,1),legend.text = c("CG","AA"))

aa.suc = as.data.frame(t(cbind(run3.water.acc.srates, run3.water.med.srates, run3.water.high.srates)))
cg.suc = as.data.frame(t(cbind(run4.water.acc.srates, run4.water.med.srates, run4.water.high.srates)))
colnames(aa.suc) = WtopList
colnames(cg.suc) = WtopList

#######################################################################################################
# i-RMSDs

#run1.it0.irmsd = subset(run1.it0.df, select=c("irmsd","name"))
#run2.it0.irmsd = subset(run2.it0.df, select=c("irmsd","name"))
run3.it0.irmsd = subset(run3.it0.df, select=c("irmsd","name"))
run4.it0.irmsd = subset(run4.it0.df, select=c("irmsd","name"))

#run1.it1.irmsd = subset(run1.it1.df, select=c("irmsd","name"))
#run2.it1.irmsd = subset(run2.it1.df, select=c("irmsd","name"))
run3.it1.irmsd = subset(run3.it1.df, select=c("irmsd","name"))
run4.it1.irmsd = subset(run4.it1.df, select=c("irmsd","name"))

#run1.water.irmsd = subset(run1.water.df, select=c("irmsd","name"))
#run2.water.irmsd = subset(run2.water.df, select=c("irmsd","name"))
run3.water.irmsd = subset(run3.water.df, select=c("irmsd","name"))
run4.water.irmsd = subset(run4.water.df, select=c("irmsd","name"))

# order them according to difficulty
benchmark.targets = c('2C5R','1PT3','1MNN','1FOK','1KSY','3CRO','1H9T','1TRO','1BY4','1HJC',
                      '1RPE','1VRR','1F4K','1K79','1KC6','1EA4','1Z63','1R4O','1AZP','1W0T',
                      '1CMA','1JJ4','1VAS','1Z9C','1DDN','2IRF','1JT0','1G9Z','1A74','2FIO',
                      '1QNE','1ZS4','1QRV','1O3T','1B3T','3BAM','1RVA','1ZME','1BDT','7MHT',
                      '2FL3','1EYU','2OAA')

run3.water.irmsd$id = rep(1:200)
run3.water.irmsd.dc = dcast(data=run3.water.irmsd,formula=id~name,fun.aggregate=sum,value.var='irmsd')
run3.water.irmsd.dc$id = NULL
run3.water.irmsd.dc = run3.water.irmsd.dc[,benchmark.targets]

run4.water.irmsd$id = rep(1:200)
run4.water.irmsd.dc = dcast(data=run4.water.irmsd,formula=id~name,fun.aggregate=sum,value.var='irmsd')
run4.water.irmsd.dc$id = NULL
run4.water.irmsd.dc = run4.water.irmsd.dc[,benchmark.targets]

run4.water.irmsd.dc$label = c('CG')
run3.water.irmsd.dc$label = c('AA')

df = rbind(run4.water.irmsd.dc, run3.water.irmsd.dc)

df.aa = df[which(df$label=="AA"),]
df.cg = df[which(df$label=="CG"),]

df.aa = df.aa[,!(colnames(df.aa) %in% c('label'))]
df.cg = df.cg[,!(colnames(df.cg) %in% c('label'))]

write.table(df.aa, "aa-irmsd.csv", sep=",")
write.table(df.cg, "cg-irmsd.csv", sep=",")


df.nolabels = df[,!(colnames(df) %in% c('label'))]

#png('irmsd-boxplots.png')
boxplot(df.nolabels, xlim = c(0.5, ncol(df[,-1])+0.5), 
        boxfill=rgb(1, 1, 1, alpha=1), border=rgb(1, 1, 1, alpha=1),ylim=c(0,14),las=2,
        main = 'Protein-DNA benchmark\nAll-atom x Coarse grain\nAll models itw',ylab='i-RMSD (A)') #invisible boxes

boxplot(df.aa, xaxt = "n", yaxt = "n", add = T,  boxwex=0.25, 
        at = 1:ncol(df[,-35]) - 0.15,outline=F,col=c('springgreen3')) #shift these left by -0.15

boxplot(df.cg, xaxt = "n", yaxt = "n", add = T, boxwex=0.25,
        at = 1:ncol(df[,-35]) + 0.15,outline=F,col=c('royalblue')) #shift these right by +0.15

abline(v=seq(0.5, 43.5, 1.0), lty=6, col='lightgray')
abline(h=1.0, lty=5,col='darkgray')
abline(h=2.0, lty=5,col='darkgray')
abline(h=4.0, lty=5,col='darkgray')
abline(v=c(11.5))
abline(v=c(32.5))

legend("topleft", inset=.02,
       c("AA","CG"), fill=c('springgreen3','royalblue'), horiz=F, cex=0.8)

text(6, 13, 'EASY')
text(21, 13, 'MEDIUM')
text(39, 13, 'HARD')
#dev.off()

#######################################################################################################
# hit rates


####
# some numbers
###

(run3.it0.acc.srates - run4.it0.acc.srates) * 100
(run3.it1.acc.srates - run4.it1.acc.srates) * 100
(run3.water.acc.srates - run4.water.acc.srates) * 100








