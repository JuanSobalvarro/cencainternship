# Info
Pixel size is 21 arcsec/pixel, so 12x12 pixels is 252x252 arcsec (4.2x4.2 arcmin)

## Important links
https://heasarc.gsfc.nasa.gov/docs/tess/Target-Pixel-File-Tutorial.html


# Inv notes
- Para calculo de ruidos el area a analizar debe ser lo suficientemente grande para que el ruido sea representativo


# Steps to get a lightcurve from TESS
- Data acquisition: TESS data is available through the MAST archive. You can use the Lightkurve package to search for and download TESS data.
- Data preprocessing: Once you have the TESS data, you may need to preprocess it. This can include background noise and instrumental effects removal, as well as normalization of the light curve.
- Light curve extraction: After preprocessing, you can extract the light curve from the TESS data. This involves selecting the appropriate pixels and summing their flux values to create a time series of brightness measurements.

https://heasarc.gsfc.nasa.gov/docs/tess/LightCurveFile-Object-Tutorial.html


# Instrumental noise by trends in light

- Ver si no hay trends de luz en multiples objetos
- Aplicar FFT (en CBVs y en PLD) y ver donde hay picos 
- En base a resultados ver si hay simulacion o no

HMM method

https://github.com/keatonb/Pyriod/tree/main

# variaciones de las estrellas
eclipsante
mareas

# Aproximacion de trend
- resttarlo a la curva total y ver como se comporta la curva de luz


# investigation
Asesor: Marco Laversveiler, Charles University

Título: A light curve investigation of the triple system hypothesis in the Sh 2-71 planetary nebula

Abstract:

The multiplicity of central stars of planetary nebulae coupled with magnetic field interaction is the favorite hypothesis for the shaping of non-round planetary nebula (PN) morphologies. Regarding multiplicity, PN Sh 2-71 is a very interesting object. It has a detected variable component, which was suggested as likely a Be binary with a misaligned precessing disk, and another component that is a bluish faint star; possibly the ionization source, as has been proposed. To date, this object is one of the best candidates for a PN formed, and shaped, by the interaction of a triple stellar system. The orbital period of the binary component in Sh 2-71 is estimated to be of a few days, which makes it possible to study it from short- to medium-term time span data. The goal of this project is to investigate Sh 2-71 variability by retrieving light curves from the TESS mission database (and other potentially available databases) in order to relate it to the triple system hypothesis.

División:  Division G – Stars and Stellar Physics


# importante bibtex aprender a usar

http://www.ita.br/posgrad/procseletivo
https://prpg.usp.br/mestrado-e-doutorado/
https://ic.ufrj.br/