library(ggplot2)
library(reshape)
setwd("~/workspace/WIGI/snapshot_data/2014-10-13/property_indexes/")
site_links <- read.csv('site_linkss-index.csv', header=TRUE, row.names=1, check.names = FALSE)
#names(site_links)[1] <- "wiki"
head(site_links)
site_links[is.na(site_links)]  <- 0

names(site_links)

nbtotal <- rowSums(site_links[, !names(site_links) %in% c("female","male","nan")] )
total <- rowSums(site_links[, !names(site_links) %in% c("nan")])

site_links$nbtotal <- nbtotal
site_links$total <- total

site_links$femper <- site_links$female / site_links$total
site_links$nbper <- site_links$nbtotal / site_links$total

site_links
sort(x = site_links, femper)

p <- ggplot(site_links, aes(x=wiki, y=femper)) + geom_bar()



