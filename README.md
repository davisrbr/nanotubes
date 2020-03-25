# CNT_general
For my general CNT research with Lu-Chang Qin

### TO DO: 
#### - Proposal for Bessel function mapping algorithm
         Some thoughts:
          The L2 norm will be easiest the conceptually, but I have doubts about its performance for any arbitrary iuploa of the dmage of a diffraction pattern (patterns are small and only take up a few pixels. I'm worried that an L2 norm will not be distcriminatory enough). 
          Another thought is that the L2 norm is computationally expensive. There are some pixels in an image of a diffraction pattern that should weigh considerably more than others (key intensity values in center, etc). 
          I can maybe use an edge finding algorithm (e.g. by convolution or watershed... I can research more if need be, but this should be a simple task) to find the edges, i.e. actual intensity patterns, of the diffraction pattern image. I probably need to ask Lu-Qang about some specifics-- normally, how many pixels are devoted for an intensity region?, how wide is the region? are there regions we should trust more than others?



#### - Polish stream site

#####  - I can cache so that the linear -> logarithmic transition doesn't require calculating Bessels again. Program flow can look like:
            - Run for the first time and save state ('Linear' or 'Log.')
            - Not sure what to do here. Can I save whether the previous state is linear or logarithmic? I have to look into this. I can't think of approach...


