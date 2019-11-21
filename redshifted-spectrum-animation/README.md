## Redshifted Spectrum (animation)
This code take a model galaxy spectrum and redshifts it from 0 to 10.  At the same time, the attenuation of the far ultravoilet (far-UV) is applied at higher redshifts.  (As a note, it's going to take a minute or two to run!)

Note that this version has a blue region and the words "Epoch of Reionization" appear when the spectrum has been redshifted past *z*~6 -- this can be removed if you would prefer a version without it.

### Planned updates
- Add fake photometry for major HST bands to showcase the Lyman-Break effect.
- Consider forcing the spectrum to decrease in brightness as _z_ gets higher.
- Considering adding a quiescent galaxy spectrum.
  - Likely will make it disappear after a certain redshift (like _z_ > 6?)
