from abc import ABCMeta, abstractmethod
from urllib.parse import urljoin

import matplotlib
import matplotlib.pyplot as plt
from pylatex import Document, Section, Figure, Itemize, NewPage, LineBreak, NoEscape


class Report:
    """Abstract Report class, it's a contract which
    the class that desire a report must impleent

    Attributes
    ----------
        Other classes:
        Report.plots : List[callable]
            List of plots desired to plot in the report
        Report.__json__ : Dict[str:Any]
            Direct link to parachutes of the Rocket. See Rocket class
            for more details.
    """
    def __init__(self, metaclass=ABCMeta):
        raise NotImplementedError

    def data_plots(self):
        plots = self.plots

        for curve_plot in plots:
            curve_plot()
            yield

    @property
    @abstractmethod
    def plots(self):
        raise NotImplementedError

    @abstractmethod
    def __json__(self):
        raise NotImplementedError

    def report_section(self, doc):
        """Builds a section with the self data,
        this function can we called with different class to
        build a report with data of various classes.

        Parameters
        ----------
        doc : pylatex.Document
            Object that manipulates the report
        Returns
        ----------
        doc
        """
        with doc.create(Section(str(self))):
            data = self.__json__()
            with doc.create(Itemize()) as itemize:
                for key, item in data.items():
                    itemize.add_item(f"{key} : {item}")
            for curve_plot in self.data_plots():
                with doc.create(Figure(position='htbp')) as plot:
                    plot.add_plot(width=300, dpi=150)
                    plt.close()
                    doc.append(LineBreak())

        doc.append(NewPage())
        return doc

    def report(self, file_path, file_name='Report'):
        """Generates a report.

        Parameters
        ----------
        file_path : str
            File path in which the file will be saved
        file_name: str
            Name of the report file
        Returns
        ----------
        doc
        """
        path = urljoin(file_path, file_name)
        standard_backend = matplotlib.get_backend()
        matplotlib.use('Agg')

        geometry_options = {"right": "2cm", "left": "2cm"}
        doc = Document(path, geometry_options=geometry_options)
        doc = self.report_section(doc)

        doc.generate_pdf(clean_tex=True)
        matplotlib.use(standard_backend)
