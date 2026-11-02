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


# Comprension e hipotesis de los periodos encontrados
- variabilidade del disco
- eclipses
- variabilidad de mareas
- pulsaciones de las estrellas
- efectos de transferéncia de massaz

# tess julian date
BTJD = BJD - 2457000.0

# ubicar en que fecha esta esa variabilidad

# Periodos segun cada uno
period = theta

## Aristoteles
### Small Aperture
11.39781895 = 0.45562195
8.73832786 = 0.62747292
7.28193988 = 0.70453246
2.84945474 = 0.81424503
5.69890947 = 0.83463618

### Big Aperture
11.39781895 = 0.43006596
8.73832786 = 0.6363172
7.48999531 = 0.70746509
2.84945474 = 0.83393837
5.69890947 = 0.85255295

## Bethesda
### Small Aperture
7.34574751 = 0.82478371
6.61117276 = 0.89312554
3.67287376 = 0.9164735
8.5305455 = 0.91759661
11.01862127 = 0.91934953

### Big Aperture
7.34574751 = 0.86184930
6.44992464 = 0.91040557
3.67287376 = 0.92322336
11.01862127 = 0.92621476
8.5305455 = 0.92776065
