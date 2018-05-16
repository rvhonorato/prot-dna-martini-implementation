setwd('~/alc-data/benchmark')

# 
# 
# df <- data.frame(name=letters[1:4], value=c(rep(TRUE, 2), rep(FALSE, 2)))
# target <- c("b", "c", "a", "d")
# df[match(target, df$name),]
# 
# benchmark_order = c("2C5R","1PT3","1MNN","1FOK","1KSY","3CRO","1EMH","1H9T",
#   "1TRO","1BY4","1HJC","1DIZ","1RPE","1VRR","1F4K","1K79",
#   "1KC6","1EA4","1Z63","1R4O","1AZP","1W0T","1CMA","1JJ4",
#   "1VAS","4KTQ","1Z9C","1DDN","2IRF","1JT0","1G9Z","1A73",
#   "2FIO","1QNE","1ZS4","1QRV","1O3T","1B3T","3BAM","1RVA",
#   "1ZME","1DFM","1BDT","7MHT","1FL3")
# 
# df_it0_cg[match(benchmark_order, colnames(df_it0_cg))]

# par(mfrow=c(3,2))
# 
# df_it0_cg = read.table('it0_cg_bench.dat',header=T,sep='\t',check.name=F)
# df_it0_aa = read.table('it0_aa_bench.dat',header=T,sep='\t',check.name=F)
# 
# 
# df_it0_aa$"1QNE" = NULL
# df_it0_cg$"1HJC" = NULL
# df_it0_cg$"1O3T" = NULL
# df_it0_cg$"1H9T" = NULL
# df_it0_cg$"1JT0" = NULL
# 
# ## it0
# boxplot(df_it0_cg, las = 2,outline=T,ylim=c(0,20),main = 'it0 CG',ylab='i-RMSD')
# abline(h=4.0)
# abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_it0_cg, las = 2,outline=F,ylim=c(0,20), main = 'it0 CG')
# #
# boxplot(df_it0_aa, las = 2,outline=T,ylim=c(0,20),main = 'it0 AA')
# abline(h=4.0)
# abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_it0_aa, las = 2,outline=F,ylim=c(0,20), main = 'it0 AA')
# 
# 
# ## it1
# 
# df_it1_cg = read.table('it1_cg_bench.dat',header=T,sep='\t',check.name=F)
# df_it1_aa = read.table('it1_aa_bench.dat',header=T,sep='\t',check.name=F)
# 
# df_it1_aa$"1QNE" = NULL
# df_it1_cg$"1HJC" = NULL
# df_it1_cg$"1O3T" = NULL
# df_it1_cg$"1H9T" = NULL
# df_it1_cg$"1JT0" = NULL
# 
# boxplot(df_it1_cg, las = 2,outline=T,ylim=c(0,20), main = 'it1 CG',ylab='i-RMSD')
# abline(h=4.0)
# abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_it1_cg, las = 2,outline=F,ylim=c(0,20), main = 'it1 CG')
# #
# boxplot(df_it1_aa, las = 2,outline=T,ylim=c(0,20), main = 'it1 AA')
# abline(h=4.0)
# abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_it1_aa, las = 2,outline=F,ylim=c(0,20), main = 'it1 AA')           

## water
df_water_cg = read.table('water_cg_bench.dat',header=T,sep='\t',check.name=F)
df_water_aa = read.table('water_aa_bench.dat',header=T,sep='\t',check.name=F)
df_water_cg$"1O3T" = NULL
target =c('1MNN','1FOK','1KSY','3CRO','1H9T','1TRO','1BY4',
          '1HJC','1RPE','1VRR','1F4K','1K79','1KC6','1Z63',
          '1R4O','1AZP','1W0T','1CMA','1JJ4','1VAS','1Z9C',
          '1DDN','1JT0','1G9Z','2FIO','1QNE','1ZS4','1QRV',
          '1B3T','3BAM','1RVA','1ZME','1BDT','7MHT')


df_water_cg = df_water_cg[,target]
df_water_aa = df_water_aa[,target]


df_water_cg$label = c('CG')
df_water_aa$label = c('AA')

df = rbind(df_water_cg, df_water_aa)

df.aa = df[which(df$label=="AA"), -35]
df.cg = df[which(df$label=="CG"), -35]
df.nolabels = df[,-35]

#boxplot(df.nolabels, outline = F)
boxplot(df.nolabels, xlim = c(0.5, ncol(df[,-1])+0.5), 
        boxfill=rgb(1, 1, 1, alpha=1), border=rgb(1, 1, 1, alpha=1),ylim=c(0,14),las=2,
        main = 'AA x CG\nwater\nprot-dna benchmark n=34',ylab='i-RMSD (A)') #invisible boxes

boxplot(df.aa, xaxt = "n", yaxt = "n", add = T,  boxwex=0.25, 
        at = 1:ncol(df[,-35]) - 0.15,outline=F) #shift these left by -0.15

boxplot(df.cg, xaxt = "n", yaxt = "n", add = T, boxfill="gray", boxwex=0.25,
        at = 1:ncol(df[,-35]) + 0.15,outline=F) #shift these right by +0.15

abline(v=seq(0.5,34.5,1.0),lty=3,col='lightgray')
abline(h=4.0, lty=3)
abline(v=c(9.5))
abline(v=c(27.5))

legend("topleft", inset=.02,
       c("AA","CG"), fill=c('white','gray'), horiz=F, cex=0.8)

text(4,13,'EASY')
text(18,13,'MEDIUM')
text(32,13,'HARD')
#setdiff(colnames(df_water_cg), colnames(df_water_aa))
#setdiff(colnames(df_water_aa), colnames(df_water_cg))

#
# 
# #colnames(df_water_aa)
# 
# 
# par(mfrow=c(2,1))
# 
# boxplot(df_water_cg, las = 2,outline=T,ylim=c(0,20), main = 'water CG',ylab='i-RMSD')
# abline(h=4.0, lty=3)
# abline(v=c(9.5))
# abline(v=c(27.5))
# #abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_water_cg, las = 2,outline=F,ylim=c(0,20), main = 'water CG')
# #
# boxplot(df_water_aa, las = 2,outline=T,ylim=c(0,20), main = 'water AA')
# abline(h=4.0, lty=3)
# abline(v=c(9.5))
# abline(v=c(27.5))
# 
# #abline(v=seq(1,33,1),col='lightgray',lty=3)
# # par(new=TRUE)
# # boxplot(df_water_aa, las = 2,outline=F,ylim=c(0,20), main = 'water AA')  
# 
# df2 <- data.frame(id = c(rep("Good",200), rep("Bad", 200)),
#                  F1 = c(rnorm(200,10,2), rnorm(200,8,1)),
#                  F2 = c(rnorm(200,7,1),  rnorm(200,6,1)),
#                  F3 = c(rnorm(200,6,2),  rnorm(200,9,3)),
#                  F4 = c(rnorm(200,12,3), rnorm(200,8,2)))
# 
# boxplot(df[,-1], xlim = c(0.5, ncol(df[,-1])+0.5), 
#         boxfill=rgb(1, 1, 1, alpha=1), border=rgb(1, 1, 1, alpha=1)) #invisible boxes
# 
# boxplot(df_water_cg, xaxt = "n", add = TRUE, boxfill="red", boxwex=0.25, 
#         at = 1:ncol(df_water_cg[,-1]) - 0.15) #shift these left by -0.15
# 
# boxplot(df[which(df$id=="Bad"), -1], xaxt = "n", add = TRUE, boxfill="blue", boxwex=0.25,
#         at = 1:ncol(df[,-1]) + 0.15) #shift these right by +0.15
# 
# boxplot(df[which(df$id=="Good"), -1], xaxt = "n", add = TRUE, boxfill="red", boxwex=0.25, 
#         at = 1:ncol(df[,-1]) - 0.15) #shift these left by -0.15
# boxplot(df[which(df$id=="Bad"), -1], xaxt = "n", add = TRUE, boxfill="blue", boxwex=0.25,
#         at = 1:ncol(df[,-1]) + 0.15) #shift these right by +0.15


