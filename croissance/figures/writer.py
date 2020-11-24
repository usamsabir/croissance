import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages

from croissance.estimation import AnnotatedGrowthCurve
from croissance.figures.plot import plot_processed_curve


class PDFWriter:
    def __init__(self, filepath):
        self._handle = open(filepath, "wb")
        self._doc = PdfPages(self._handle)

    def write(self, name: str, curve: AnnotatedGrowthCurve):
        fig, _axes = plot_processed_curve(curve=curve, name=name)

        try:
            self._doc.savefig(fig)
        finally:
            plt.close(fig)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self._doc.close()
        self._handle.close()
