import lightkurve as lk
import numpy as np
from .data import DataRetrieving
from enum import Enum

class Method(Enum):
    SAP = "sap"
    PLD = "pld"
    CBV = "cbv"

class FluxMethod(Enum):
    SUM = "sum"
    MEAN = "mean"

class LightCurveProcessing:
    def __init__(self, data: DataRetrieving):
        self._data = data

    @staticmethod
    def _get_lightcurve(file: lk.TessTargetPixelFile, method: Method = Method.SAP, aperture_mask: str = "default", flux_method: FluxMethod = FluxMethod.SUM) -> lk.lightcurve.LightCurve:

        if method == Method.SAP:
            lc = file.to_lightcurve(aperture_mask=aperture_mask, flux_method=flux_method.value)
        elif method == Method.PLD:
            lc = file.to_lightcurve(method="pld", aperture_mask=aperture_mask)
        elif method == Method.CBV:
            lc = file.to_lightcurve(method="cbv", aperture_mask=aperture_mask)
        else:
            raise ValueError(f"Invalid method: {method}")

        if not isinstance(lc, lk.lightcurve.LightCurve):
            raise TypeError("The resulting object is not of type LightCurve")

        return lc

    def get_aristoteles_lightcurve(self, method: Method = Method.SAP, aperture_mask: str = "default", flux_method: FluxMethod = FluxMethod.SUM) -> lk.lightcurve.LightCurve:
        file = self._data.get_aristoteles_file()
        return self._get_lightcurve(file, method=method, aperture_mask=aperture_mask)

    def get_bethesda_lightcurve(self, method: Method = Method.SAP, aperture_mask: str = "default", flux_method: FluxMethod = FluxMethod.SUM) -> lk.lightcurve.LightCurve:
        file = self._data.get_bethesda_file()
        return self._get_lightcurve(file, method=method, aperture_mask=aperture_mask, flux_method=flux_method)

    @property
    def aperture_mask(self) -> np.ndarray:
        aper = np.zeros(self._data.get_aristoteles_file().shape[1:], dtype=bool)
        aper[8:14, 8:13] = True

        return aper

    # bg noise removal
    def get_bg_masks(self, threshold: float = 0.1, reference_pixel: str = "center") -> tuple[np.ndarray, np.ndarray]:
        """
        Get bg masks using the function create_threshold_mask from lightkurve. It takes a threeshold and reference pixel
        """
        aristoteles_file = self._data.get_aristoteles_file()
        bethesda_file = self._data.get_bethesda_file()

        # Create masks
        aristoteles_mask = ~aristoteles_file.create_threshold_mask(threshold=threshold, reference_pixel=reference_pixel)
        bethesda_mask = ~bethesda_file.create_threshold_mask(threshold=threshold, reference_pixel=reference_pixel)

        return aristoteles_mask, bethesda_mask