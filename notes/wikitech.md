_17th May 2015_

WikiTech
========

(Disclaimer: I'm new to WikiTech)

WikiMedia foundation provides VM(virtual machines) to developers to run bots and
analytics for wikimedia projects. They have something called "tools". I'm not
totally sure how they are different instances but "tools" can have more than
one person managing the tool account, then they can have their own web pages and
probably they have provided a lot of preinstalled infrastructure to access on "tools".
For example it already had `java` and `maven` installed.

To use tools I had to create an account on wikitech, then I had to ask to join
"tools" project and then I could ssh on `login.tools.wmflabs.org` after
uploading my ssh public key. Then I created a "tool" named `wigi` and added Max
to it.

To switch to the tool account I have to do
```
$ become wigi
```
Then I cloned the wikidata-toolkit on it. Next time I'll try to get it running.
