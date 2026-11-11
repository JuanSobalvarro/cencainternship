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
- **Variabilidad del disco:** cambios en la densidad, geometría o precesión del disco de una estrella Be pueden producir señales cuasi-periódicas y amplitudes variables.
- **Eclipses:** una ocultación orbital produce disminuciones repetibles; eclipses primarios y secundarios pueden tener profundidades diferentes.
- **Variabilidad de mareas:** la deformación elipsoidal cambia el área proyectada de la estrella y puede producir dos máximos o mínimos por órbita.
- **Pulsaciones estelares:** oscilaciones de la estrella pueden imitar una modulación orbital, especialmente cuando se observan pocos ciclos.
- **Transferencia de masa:** un disco de acreción, una región caliente o cambios en el flujo de masa pueden producir modulación y armónicos.
- **Efectos instrumentales:** deriva de apuntado, luz dispersa, cambios de foco, contaminación de fuentes vecinas y correcciones PLD o polinomiales imperfectas pueden dejar periodicidades residuales.

Una periodicidad es más confiable si se mantiene entre aperturas, sectores, métodos de detrending y estrellas de referencia. Los períodos encontrados deben considerarse candidatos hasta descartar sistemáticos, armónicos y ruido correlacionado.

# tess julian date
BTJD = BJD - 2457000.0

BJD es la fecha juliana corregida por el tiempo de viaje de la luz hasta el baricentro del Sistema Solar. BTJD no es una escala temporal nueva: es BJD con una constante restada para hacer los números más pequeños. La conversión inversa es BJD = BTJD + 2457000.0. Al calcular períodos mediante diferencias de tiempo, BJD y BTJD producen el mismo resultado; no se debe aplicar el offset dos veces y conviene conservar la escala temporal (por ejemplo, TDB).

# ubicar en que fecha esta esa variabilidad

# Periodos segun cada uno
period = theta

## Aristoteles
### Small Aperture
11.39781895 = 0.45562195 #!
8.73832786 = 0.62747292 #!
7.28193988 = 0.70453246 #!
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
7.34574751 = 0.82478371 #!
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

# COnclusiones
discusion sobre la relacion de 8 y 7 puede estar relacioando con la orbita y deformacion de marea

para cada fenomeno importante mencionar por que puede existir o no en la curva de luz

# statistic significance
- FAP FAP FAP FAP

# Facts about sh 2-71
- The object is a planetary nebula (PN) with a complex morphology
- It has a binary central star system (star A) without sufficient temperature to ionize the nebula
- Likely the nebula progenitor is the star B
- Gaia parallax put the star A at approximately 1.62 +- 0.1 kpc but the faintness of the star B makes it difficult to measure its parallax
- The nebula is aproximately at 1.52 ± 0.54 kpc
- Stars A and B are separated by 7.4 arcsec which corresponds to a minimum physical separation of 1.2 × 10^4 au at this distance.
- The orbital period of star A (Paf) is a few days
- Mocnik et al. ( ˇ 2015) concluded that the peculiar 68-d period photometric variability, analysed in detail by Mikula´sek et al. ( ˇ 2005, 2007), is the result of obscuration by a precessing disc on a longer period than PA, f.


# About the presence of effects in light curves
Once we have the light curves detrended (after cleaning and PLD), the plot even though it is "smooth" that structure could include periodic variability, correlated aperiodic variability or any remaining instrumental noise, and we cannot distinguish between them :/

So, it is important to say that PDM can produce misleading minima from correlated noise, particularly at long periods relative to the observing baseline

For that it could be necesary to include a null hypothesis test to determine the significance of the detected periods.
