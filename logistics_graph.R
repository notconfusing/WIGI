library(ggplot2)
library(reshape)
setwd("~/workspace/WIGI/snapshot_data/2014-10-13/property_indexes")
dob <- read.csv('dob-index.csv')
dob[is.na(dob)] <- 0
dob <- dob[,!(names(dob) %in% c('nan'))]
dob$total <- rowSums(dob[names(dob) != "X"])
dob$nm.ratio <- 1 - (dob$male / dob$total)
head(dob)


  
p <- ggplot(dob, aes(x=X, y=nm.ratio)) + geom_smooth()
show(p)
recent <- dob[ which(dob$X > 1800 & dob$X < 1988),]
head(recent)

precent <- ggplot(recent, aes(x=X, y=nm.ratio)) + geom_smooth() + xlim(1800,2500)
show(precent)

lregress = glm(formula=nm.ratio ~ X, family=binomial(logit), data=recent)
plot(nm.ratio ~ X, data=recent, xlim=c(1800,1988))
lines(recent$X, lregress$fitted, type="l", col='red', xlim=c(1800,1988))
summary(lregress)


