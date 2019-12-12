## Redshifted Spectrum with Bandpasses & Emission Lines
This script takes a model galaxy spectrum and redshifts based upon user input.  At the same time, the attenuation of the far ultravoilet (far-UV) is applied at higher redshifts.  Under-plotted are some _Keck_/MOSFIRE, _HST_/WFC3, and _Spitzer_/IRAC bandpasses.  

The bandpasses could be changed to whatever you want! As I mostly work in the NIR and IR, the bandpasses plotted only cover that wavelength space, although this code can easily be adapted to fit your needs.

One possible way to do this would be, based upon the redshift and resulting spectral range covered, you could only plot the bandpasses that would show up there.  That could cut down on the number of unnecessary filters shown in your legend.

## _How to use this script as a quick command in your terminal_
Check out [this tutorial](https://github.com/aibhleog/Quick-Tools-for-the-Observational-Astronomer/blob/master/playing-with-your-bashrc.md), which walks you through making aliases in your `.bashrc` or `.bash_profile` file, allowing you to run this script from your terminal! 

Here's how it looks in my `.bashrc`:
```
# alias for seeing what lines can pop up in NIR and IR bands given a z
alias zlines='python /path/to/bandpass_zlines.py'
```
So then all you have to type in your terminal is 
```
zlines 7.5032
```

### Planned updates
- Considering adding a quiescent galaxy spectrum.
- Considering adding bluer bandpasses, like optical ones (bleh)
