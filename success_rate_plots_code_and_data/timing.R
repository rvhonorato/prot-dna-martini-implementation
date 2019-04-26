library(ggplot2)
library(reshape2)
library(ggpubr)
library(extrafont)

time_it0 = read.table("timing_it0.txt", header = T)
time_it1 = read.table("timing_it1.txt", header = T)
time_itw = read.table("timing_itw.txt", header = T)
time_total = read.table("timing_total.txt", header = T)

time_it0$approach = factor(time_it0$approach, levels = c("All-Atom", "Coarse-Grained"))
time_it1$approach = factor(time_it1$approach, levels = c("All-Atom", "Coarse-Grained"))
time_itw$approach = factor(time_itw$approach, levels = c("All-Atom", "Coarse-Grained"))
time_total$approach = factor(time_total$approach, levels = c("All-Atom", "Coarse-Grained"))

times0_plot = ggplot() +
              geom_bar(data=time_it0, aes(y = time, x = approach, fill = approach),
              stat="identity") +
              geom_hline(yintercept=c(0), color="black") +
              scale_fill_manual(values=c("#114D9C", "#B7D5FC")) +
              theme(
                panel.grid = element_blank(),
                panel.background = element_rect(fill = "white"),
                axis.text.y = element_text(size=15),
                axis.text.x = element_blank(),
                axis.title.x = element_blank(),
                axis.title.y = element_text(size=17),
                legend.title = element_blank(),
                legend.text = element_text(size=15),
                legend.position = "none",
                axis.ticks.x = element_blank(),
                strip.text.y = element_text(size=17, colour = "white", face = "bold"),
                strip.text.x = element_blank(),
                strip.background = element_rect(fill = "transparent", linetype = "solid", color = "white")
              ) +
              facet_grid(~ stage) +
              labs(
                x="",
                y="Computing time (min/model)"
              ) +
              ylim(0,0.5)

times1_plot = ggplot() +
              geom_bar(data=time_it1, aes(y = time, x = approach, fill = approach),
                       stat="identity") +
              geom_hline(yintercept=c(0), color="black") +
              scale_fill_manual(values=c("#114D9C", "#B7D5FC")) +
              theme(
                panel.grid = element_blank(),
                panel.background = element_rect(fill = "white"),
                axis.text.y = element_text(size=15),
                axis.text.x = element_blank(),
                axis.title.x = element_blank(),
                axis.title.y = element_text(size=17),
                legend.title = element_blank(),
                legend.text = element_text(size=15),
                legend.position = "none",
                axis.ticks.x = element_blank(),
                strip.text.y = element_text(size=17, colour = "white", face = "bold"),
                strip.text.x = element_blank(),
                strip.background = element_rect(fill = "transparent", linetype = "solid", color = "white")
              ) +
              facet_grid(~ stage) +
              labs(
                x="",
                y="Computing time (min/model)"
              ) +
              ylim(0,25)

times2_plot = ggplot() +
              geom_bar(data=time_itw, aes(y = time, x = approach, fill = approach),
                       stat="identity") +
              geom_hline(yintercept=c(0), color="black") +
              scale_fill_manual(values=c("#114D9C", "#B7D5FC")) +
              theme(
                panel.grid = element_blank(),
                panel.background = element_rect(fill = "white"),
                axis.text.y = element_text(size=15),
                axis.text.x = element_blank(),
                axis.title.x = element_blank(),
                axis.title.y = element_text(size=17),
                legend.title = element_blank(),
                legend.text = element_text(size=15),
                legend.position = "none",
                axis.ticks.x = element_blank(),
                strip.text.y = element_text(size=17, colour = "white", face = "bold"),
                strip.text.x = element_blank(),
                strip.background = element_rect(fill = "transparent", linetype = "solid", color = "white")
              ) +
              facet_grid(~ stage) +
              labs(
                x="",
                y="Computing time (min/model)"
              ) +
              ylim(0,30)

times_plot = ggplot() +
              geom_bar(data=time_total, aes(y = time, x = approach, fill = approach),
                       stat="identity") +
              geom_hline(yintercept=c(0), color="black") +
              scale_fill_manual(values=c("#114D9C", "#B7D5FC")) +
              theme(
                panel.grid = element_blank(),
                panel.background = element_rect(fill = "white"),
                axis.text.y = element_text(size=15),
                axis.text.x = element_blank(),
                axis.title.x = element_blank(),
                axis.title.y = element_text(size=17),
                legend.title = element_blank(),
                legend.text = element_text(size=15),
                legend.position = "bottom",
                axis.ticks.x = element_blank(),
                strip.text.y = element_text(size=17, colour = "white", face = "bold"),
                strip.text.x = element_blank(),
                strip.background = element_rect(fill = "transparent", linetype = "solid", color = "white")
              ) +
              facet_grid(~ stage) +
              labs(
                x="",
                y="Computing time (min/model)"
              ) +
              ylim(0,60)

it0_it1_plot = ggarrange(
              times0_plot,
              times1_plot,
              align='h',
              common.legend = F
              )

itw_total_plot = ggarrange(
              times2_plot,
              times_plot,
              align='h',
              common.legend = T,
              legend = c("bottom")
            )

final_plot = ggarrange(
            it0_it1_plot,
            itw_total_plot,
            align='v',
            common.legend = F,
            nrow = 2
            )

#poster_plot = annotate_figure(times_plot, top = text_grob("Total Time \n", size = 20))

#ggsave("total_time.png", poster_plot, width=6, height=7)
#ggsave("timing.png", final_plot, width=12, height=13)
svg("timing.svg",width=12, height=13)
final_plot
dev.off()