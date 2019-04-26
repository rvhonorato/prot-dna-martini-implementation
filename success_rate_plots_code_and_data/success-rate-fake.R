  library(ggplot2)
  library(reshape2)
  library(ggpubr)
  library(extrafont)
  library(Cairo)
  
  ss_aa = read.table("success_rates-SS-aa.txt", header=T)
  ss_aa$Quality = ifelse(
    ss_aa$i.RMSD == 3, "High", ifelse(
      ss_aa$i.RMSD == 2, "Medium", ifelse(
        ss_aa$i.RMSD == 1, "Acceptable", ifelse(
          ss_aa$i.RMSD == -1, "Near-Acceptable", "Low"
        )
      )
    )
  )
  
  ss_aa$difficulty = factor(ss_aa$difficulty, levels=c("Easy", "Intermediate", "Hard"))
  ss_aa$Quality = factor(ss_aa$Quality, levels=c("High", "Medium", "Acceptable", "Near-Acceptable", "Low"))
  ss_aa$cutoff = factor(ss_aa$cutoff, levels=c("T1", "T5", "T10", "T20", "T50", "T100", "T200"))
  ss_aa$complex = factor(ss_aa$complex, levels=(unique(rev(ss_aa$complex))))
  
  ss_aa_plot = ggplot(ss_aa, aes(cutoff, complex, fill=ss_aa$Quality)) +
    geom_tile() +
    geom_vline(xintercept=seq(0,7) + 0.5, color="dark gray", size=1) +
    geom_hline(yintercept=seq(0,100) + 0.5, color="dark gray", size =1) +
    geom_vline(xintercept = 7.55, color="white", size=6) +
    geom_vline(xintercept = 0.45, color="white", size=6) +
    geom_vline(xintercept = 0.55, color="dark gray", size=1) +
    geom_vline(xintercept = 7.45, color="dark gray", size=1) +
    facet_grid(difficulty ~ stage, scales="free", space="free_y", switch = "y") +
    scale_fill_manual(values=c("#33a02c", "#b2df8a", "#a6cee3", "light gray", "white")) +
    theme(
      panel.grid = element_blank(),
      panel.background = element_blank(),
      axis.text.y = element_text(size = 13, family = "Courier"),
      axis.ticks = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      legend.title = element_blank(),
      legend.text = element_text(size=15),
      legend.key = element_rect(color = "black"),
      legend.position = "none",
      strip.text.y = element_blank(),
      strip.text.x = element_blank(),
      strip.background = element_blank()
    ) +
    labs(
      x="",
      y=""
    )
  
  ss_cg = read.table("success_rates-SS-cg.txt", header=T)
  ss_cg$Quality = ifelse(
    ss_cg$i.RMSD == 3, "High", ifelse(
      ss_cg$i.RMSD == 2, "Medium", ifelse(
        ss_cg$i.RMSD == 1, "Acceptable", ifelse(
          ss_cg$i.RMSD == -1, "Near-Acceptable", "Low"
        )
      )
    )
  )
  
  ss_cg$difficulty = factor(ss_cg$difficulty, levels=c("Easy", "Intermediate", "Hard"))
  ss_cg$Quality = factor(ss_cg$Quality, levels=c("High", "Medium", "Acceptable", "Near-Acceptable", "Low"))
  ss_cg$cutoff = factor(ss_cg$cutoff, levels=c("T1", "T5", "T10", "T20", "T50", "T100", "T200"))
  ss_cg$complex = factor(ss_cg$complex, levels=(unique(rev(ss_cg$complex))))
  
  ss_cg_plot = ggplot(ss_cg, aes(cutoff, complex, fill=ss_cg$Quality)) +
    geom_tile() +
    geom_vline(xintercept=seq(0,7) + 0.5, color="dark gray", size=1) +
    geom_hline(yintercept=seq(0,100) + 0.5, color="dark gray", size=1) +
    geom_vline(xintercept = 7.55, color="white", size=6) +
    geom_vline(xintercept = 0.62, color="dark gray", size=1) +
    geom_vline(xintercept = 7.45, color="dark gray", size=1) +
    scale_fill_manual(values=c("#33a02c", "#b2df8a", "#a6cee3", "light gray", "white")) +
    facet_grid(difficulty ~ stage, scales="free", space="free_y") +
    theme(
      panel.grid = element_blank(),
      panel.background = element_blank(),
      axis.text.y = element_blank(),
      axis.line.y = element_line(colour = "white", size = 10),
      axis.ticks = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      legend.title = element_blank(),
      legend.text = element_text(size=15),
      legend.position = "none",
      strip.text.y = element_text(size=17, color = "white"),
      strip.text.x = element_blank(),
      strip.background = element_rect(fill = "dark gray", size = 5)
    ) +
    labs(
      x="",
      y=""
    )
  
  success_rate_per_cutoff_ss_aa = read.table("success_rates-SS-per_cutoff-aa.txt", header=T)
  success_rate_per_cutoff_ct_aa = read.table("success_rates-CT-per_cutoff-aa.txt", header=T)
  
  success_rate_per_cutoff_ss_aa = melt(success_rate_per_cutoff_ss_aa)
  success_rate_per_cutoff_ss_aa$cutoff = factor(
    success_rate_per_cutoff_ss_aa$cutoff,
    levels=c("T1", "T5", "T10", "T20", "T50", "T100", "T200")
  )
  success_rate_per_cutoff_ss_aa$variable = factor(
    success_rate_per_cutoff_ss_aa$variable,
    levels=c("Low", "Near.Acceptable", "Acceptable", "Medium", "High")
  )
  success_rate_per_cutoff_ss_aa$facet = " "
  success_rate_per_cutoff_ss_aa$value = success_rate_per_cutoff_ss_aa$value / 27 * 100
  
  success_rate_per_cutoff_ct_aa = melt(success_rate_per_cutoff_ct_aa)
  success_rate_per_cutoff_ct_aa$cutoff = factor(
    success_rate_per_cutoff_ct_aa$cutoff,
    levels=c("T1", "T2", "T3", "T4", "T5")
  )
  success_rate_per_cutoff_ct_aa$variable = factor(
    success_rate_per_cutoff_ct_aa$variable,
    levels=c("Low", "Near.Acceptable", "Acceptable", "Medium", "High")
  )
  success_rate_per_cutoff_ct_aa$facet = " "
  success_rate_per_cutoff_ct_aa$value = success_rate_per_cutoff_ct_aa$value / 27 * 100
  
  success_rate_per_cutoff_ss_plot_aa = ggplot(success_rate_per_cutoff_ss_aa, aes(cutoff, value, fill=variable)) +
    geom_bar(stat="identity") +
    facet_grid(facet ~ stage) +
    geom_hline(yintercept=c(0), color="black") +
    geom_hline(yintercept=c(25, 50, 75, 100), color="dark gray", linetype="dashed") +
    scale_fill_manual(values=c("white", "light gray", "#a6cee3", "#b2df8a", "#33a02c")) +
    theme(
      panel.grid = element_blank(),
      panel.background = element_rect(fill = "white"),
      plot.margin = unit(c(0,-1,0,2.1), "lines"),
      axis.text.y = element_text(size=15),
      axis.ticks.x = element_blank(),
      axis.ticks.y = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      axis.title.y = element_text(size=12),
      legend.title = element_blank(),
      legend.text = element_text(size=20),
      legend.position = "none",
      strip.text = element_text(size=17),
      strip.background = element_rect(fill = "white")
      ) +
    labs(
      x="",
      y="Success rate [%]"
    ) +
    ylim(0,100)
  
  success_rate_per_cutoff_ct_plot_aa = ggplot(success_rate_per_cutoff_ct_aa, aes(cutoff, value, fill=variable)) +
    geom_bar(stat="identity") +
    facet_grid(facet ~ stage) +
    geom_hline(yintercept=c(0), color="black") +
    geom_hline(yintercept=c(25, 50, 75, 100), color="dark gray", linetype="dashed") +
    scale_fill_manual(values=c("white", "light gray", "#a6cee3", "#b2df8a", "#33a02c")) +
    theme(
      panel.grid = element_blank(),
      panel.background = element_rect(fill = "white"),
      plot.margin = unit(c(0,-1,0,2), "lines"),
      axis.text.y = element_text(size=15),
      axis.ticks.x = element_blank(),
      axis.ticks.y = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      axis.title.y = element_text(size=12),
      legend.title = element_blank(),
      legend.text = element_text(size=20),
      legend.position = "none",
      strip.text = element_text(size=17),
      strip.background = element_rect(fill = "white")
    ) +
    labs(
      x="",
      y="Success rate [%]"
    ) +
    ylim(0,100)
  
  aa_plot = ggarrange(
    success_rate_per_cutoff_ss_plot_aa,
    success_rate_per_cutoff_ct_plot_aa,
    heights = c(1.5),
    common.legend = F,
    align = "h"
  )
  
 aa_plot = annotate_figure(aa_plot, top = text_grob("All-Atom \n", size = 20))
  
  success_rate_per_cutoff_ss_cg = read.table("success_rates-SS-per_cutoff-cg.txt", header=T)
  success_rate_per_cutoff_ct_cg = read.table("success_rates-CT-per_cutoff-cg.txt", header=T)
  
  success_rate_per_cutoff_ss_cg = melt(success_rate_per_cutoff_ss_cg)
  success_rate_per_cutoff_ss_cg$cutoff = factor(
    success_rate_per_cutoff_ss_cg$cutoff,
    levels=c("T1", "T5", "T10", "T20", "T50", "T100", "T200")
  )
  success_rate_per_cutoff_ss_cg$variable = factor(
    success_rate_per_cutoff_ss_cg$variable,
    levels=c("Low", "Near.Acceptable", "Acceptable", "Medium", "High")
  )
  success_rate_per_cutoff_ss_cg$facet = " "
  success_rate_per_cutoff_ss_cg$value = success_rate_per_cutoff_ss_cg$value / 27 * 100
  
  success_rate_per_cutoff_ct_cg = melt(success_rate_per_cutoff_ct_cg)
  success_rate_per_cutoff_ct_cg$cutoff = factor(
    success_rate_per_cutoff_ct_cg$cutoff,
    levels=c("T1", "T2", "T3", "T4", "T5")
  )
  success_rate_per_cutoff_ct_cg$variable = factor(
    success_rate_per_cutoff_ct_cg$variable,
    levels=c("Low", "Near.Acceptable", "Acceptable", "Medium", "High")
  )
  success_rate_per_cutoff_ct_cg$facet = " "
  success_rate_per_cutoff_ct_cg$value = success_rate_per_cutoff_ct_cg$value / 27 * 100
  
  success_rate_per_cutoff_ss_plot_cg = ggplot(success_rate_per_cutoff_ss_cg, aes(cutoff, value, fill=variable)) +
    geom_bar(stat="identity") +
    facet_grid(facet ~ stage) +
    geom_hline(yintercept=c(0), color="black") +
    geom_hline(yintercept=c(25, 50, 75, 100), color="dark gray", linetype="dashed") +
    scale_fill_manual(values=c("white", "light gray", "#a6cee3", "#b2df8a", "#33a02c")) +
    theme(
      panel.grid = element_blank(),
      panel.background = element_rect(fill = "white"),
      plot.margin = unit(c(0,-1,0,2.1), "lines"),
      axis.text.y = element_text(size=15),
      axis.ticks.x = element_blank(),
      axis.ticks.y = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      axis.title.y = element_text(size=12),
      legend.title = element_blank(),
      legend.text = element_text(size=20),
      legend.position = "none",
      strip.text = element_text(size=17),
      strip.background = element_rect(fill = "white")
    ) +
    labs(
      x="",
      y="Success rate [%]"
    ) +
    ylim(0,100)
  
  success_rate_per_cutoff_ct_plot_cg = ggplot(success_rate_per_cutoff_ct_cg, aes(cutoff, value, fill=variable)) +
    geom_bar(stat="identity") +
    facet_grid(facet ~ stage) +
    geom_hline(yintercept=c(0), color="black") +
    geom_hline(yintercept=c(25, 50, 75, 100), color="dark gray", linetype="dashed") +
    scale_fill_manual(values=c("white", "light gray", "#a6cee3", "#b2df8a", "#33a02c")) +
    theme(
      panel.grid = element_blank(),
      panel.background = element_rect(fill = "white"),
      plot.margin = unit(c(0,-1,0,2), "lines"),
      axis.text.y = element_text(size=15),
      axis.ticks.x = element_blank(),
      axis.ticks.y = element_blank(),
      axis.text.x = element_text(size=13, angle=60, hjust=1),
      axis.title = element_text(size=15),
      axis.title.y = element_text(size=12),
      legend.title = element_blank(),
      legend.text = element_text(size=20),
      legend.position = "none",
      strip.text = element_text(size=17),
      strip.background = element_rect(fill = "white")
    ) +
    labs(
      x="",
      y="Success rate [%]"
    ) +
    ylim(0,100)
  
  cg_plot = ggarrange(
    success_rate_per_cutoff_ss_plot_cg,
    success_rate_per_cutoff_ct_plot_cg,
    heights = c(1.5),
    common.legend = F,
    align = "h"
  )
  
  cg_plot = annotate_figure(cg_plot, top = text_grob("Coarse-Grained \n", size = 20))
  
  heatmap_plot = ggarrange(
  ss_aa_plot,
  ss_cg_plot,
  align = 'h',
  common.legend = T
  )
  
  top_plots = ggarrange(
    aa_plot, cg_plot, ncol=2
  )
  
  complex_plot = ggarrange(
    top_plots,
    heatmap_plot,
    nrow = 2,
    heights = c(1.2, 3)
    )
  postscript("test.eps", fonts=c("Courier"), width = 12, height = 30)
  complex_plot
  dev.off()
  #ggsave("test.eps", complex_plot, width=12, height=13)
  ggsave("legend.png", complex_plot, width=12, height=13)
