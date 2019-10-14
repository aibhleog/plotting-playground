## Animated Dither Patterns for MOSFIRE
This code makes a series of images and creates a small animation showing the dither patterns of MOSFIRE, and pointing out the safe regions to place targets in the slits. **Note that this is only showing the ABAB dither pattern.**

In this plotting example, I make a series of images instead of using the `matplotlib.animation` package. My philosophy is that sometimes being more "pythonic" can make your life harder -- in this example, where I want to change things for each frame, it makes *much* more sense to make a series of images and combine them later into an animation. Also (another reason), it's good to know how to do a task in a few different ways!

### To make a GIF from the PNG files:
You can exercise a little freedom here, but I made mine using GIMP (GNU Image Manipulation Program) -- you can learn how to do this, too, by [following this solution](https://askubuntu.com/a/457449).  Otherwise, there are command line programs and online programs that can do this, too.  How you do this step is entirely up to you!
