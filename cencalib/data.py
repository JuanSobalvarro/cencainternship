import astropy as ap
import lightkurve as lk

COORDS = ap.coordinates.SkyCoord("285.5 +2.156388", unit=("deg", "deg"))
CUTOUT_SIZE = (20, 20)
QUALITY_MASK = "default"

class DataRetrieving:
    def __init__(self, coords: ap.coordinates.SkyCoord, cutout_size: tuple[int, int], quality_mask: str):
        self._coords: ap.coordinates.SkyCoord = coords
        self._cutout_size: tuple[int, int] = cutout_size
        self._quality_mask: str = quality_mask
        
        self._search: lk.SearchResult = lk.search_tesscut(coords)
        self._files: lk.TargetPixelFileCollection | None = None
        self._download_files()

    def get_search(self) -> lk.SearchResult:
        return self._search

    def get_files(self) -> lk.TargetPixelFileCollection:
        if self._files is None:
            raise ValueError("Files have not been downloaded yet.")
        return self._files

    def get_aristoteles_file(self) -> lk.TessTargetPixelFile:
            return self._get_file(0)
    
    def get_bethesda_file(self) -> lk.TessTargetPixelFile:
        return self._get_file(1)

    def _download_files(self) -> None:
        files = self._search.download_all(cutout_size=self._cutout_size, download_dir="./fitsdata", quality_bitmask=self._quality_mask)

        if files is None or len(files) < 2:
            raise ValueError("No valid files were downloaded, you should check the search result")

        if not isinstance(files, lk.TargetPixelFileCollection):
            raise TypeError("The downloaded files are not of type TargetPixelFileCollection")

        self._files = files

    def _get_file(self, index: int) -> lk.TessTargetPixelFile:
        if self._files is None:
            raise ValueError("Files have not been downloaded yet.")

        if index < 0 or index >= len(self._files):
            raise IndexError("Index out of range for the available files.")

        file = self._files[index]

        if not isinstance(file, lk.TessTargetPixelFile):
            raise TypeError(f"The file at index {index} is not of type TessTargetPixelFile")

        return file

