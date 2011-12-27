#!/usr/bin/python
"""
TRML support of printing barcodes.
"""
# reportlab
from reportlab.platypus.flowables import Flowable
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import createBarcodeDrawing, getCodes
# trml
from trml2pdf import utils
from trml2pdf import color


class BarCode(Flowable):
    """
    Origin (x, y) is the 'left bottom corner' of boundary border
    at <pageGraphics>.

    Code types:
        Standard39
        Extended39
        EAN13
        FIM
        EAN8
        Extended93
        USPS_4State
        Codabar
        MSI
        POSTNET
        Code11
        Standard93
        I2of5
        Code128 (default)

    Attributes:
        * fontName
        * strokeWidth
        * barFillColor
        * humanReadable
        * height
        * debug
        * lquiet
        * background
        * barWidth
        * strokeColor
        * barStrokeWidth
        * barStrokeColor
        * rquiet
        * quiet
        * barHeight
        * width
        * fontSize
        * fillColor
        * textColor
        * showBoundary
    """
    XPOS, YPOS, WIDTH, HEIGHT = range(4)

    def __init__(self, node, styles, value):
        Flowable.__init__(self)

        self.node = node
        self.styles = styles
        self.value = value
        self.xpos = utils.unit_get(node.getAttribute('x'))
        self.ypos = utils.unit_get(node.getAttribute('y'))
        self.width = utils.unit_get(node.getAttribute('width'))
        self.height = utils.unit_get(node.getAttribute('height'))
        self.code_name = node.getAttribute('code')
        self.codes = getCodes()

        # set defaults
        if self.code_name == "":
            self.code_name = "Code128" # default code type
        if not self.width:
            self.width = self.get_default_bounds()[BarCode.WIDTH]
        if not self.height:
            self.height = self.get_default_bounds()[BarCode.HEIGHT]

    def get_default_bounds(self):
        "Get default size of barcode"
        bcc = self.codes[self.code_name]
        barcode = bcc(value=self.value)
        return barcode.getBounds() # x, y, width, height

    def wrap(self, *args):
        return (self.width, self.height)

    def draw(self):
        "Read attribs and draw barcode"
        kwargs = {"barStrokeWidth": 0.00001}
        for attr in ("barFillColor", "background", "strokeColor",
                     "barStrokeColor", "fillColor", "textColor"):
            if self.node.hasAttribute(attr):
                kwargs[attr] = color.get(self.node.getAttribute(attr))
        for attr in ("fontName", "humanReadable", "debug", "lquiet", "rquiet",
                     "quiet"):
            if self.node.hasAttribute(attr):
                kwargs[attr] = self.node.getAttribute(attr)
        for attr in ("strokeWidth", "barWidth", "barStrokeWidth",
                     "barHeight", "fontSize", "isoScale"):
            if self.node.hasAttribute(attr):
                kwargs[attr] = utils.unit_get(self.node.getAttribute(attr))

        bcd = createBarcodeDrawing(self.code_name, value=self.value,
                                   width=self.width, height=self.height,
                                   **kwargs)
        renderPDF.draw(bcd, self.canv, self.xpos, self.ypos,
                       showBoundary=self.node.getAttribute("showBoundary"))
