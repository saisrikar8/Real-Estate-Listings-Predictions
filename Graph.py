import numpy
import matplotlib.pyplot as graph
from matplotlib import style
import sys

style.use('bmh')


class Graph2D:
    x_values = None
    y_values = None
    title = str()
    x_title = str()
    y_title = str()

    def __init__(self, x_values: list, y_values: list, title='', x_title='', y_title=''):
        self.x_values = numpy.array(x_values)
        self.y_values = numpy.array(y_values)
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        graph.title(self.title)
        graph.xlabel(self.x_title)
        graph.ylabel(self.y_title)

    def scatterPlot(self, label=''):
        graph.scatter(self.x_values, self.y_values, marker='x', c='r', label=label)

    def lineGraph(self, label=''):
        graph.plot(self.x_values, self.y_values, c='r', label=label)

    def line(self, slope, yintercept, label = ''):
        graph.axline((0, yintercept), slope=slope, color="black", linestyle=(0, (5, 5)), label = label)

    def plotPoint(self, x, y, label = ''):
        graph.plot(numpy.array([x]), numpy.array([y]), c = 'b', marker = 'x', label = label)

    def showGraph(self):
        graph.legend()
        graph.show()



# Features linear regression
class SmartGraph2D(Graph2D):

    def __init__(self, x_values: list, y_values: list, title='', x_title='', y_title=''):
        super().__init__(x_values, y_values, title, x_title, y_title)

    def compute_cost(self, w, b):
        m = self.x_values.shape[0]
        cost = 0

        for i in range(m):
            f_wb = w * self.x_values[i] + b
            cost = cost + (f_wb - self.y_values[i])**2
        total_cost = 1 / (2 * m) * cost

        return total_cost

    def computeGradient(self, w, b):
        d_w = numpy.int64(0)
        d_b = numpy.int64(0)
        m = self.x_values.shape[0]
        for i in range(m - 1):
            try:
                x_i = self.x_values[i]
                y_i = self.y_values[i]
                alpha = 0.001
                d_w += ((w * x_i + b) - y_i) * alpha * x_i
                d_b += ((w * x_i + b) - y_i) * alpha
            except RuntimeWarning:
                sys.tracebacklimit = 0
                raise ValueError('The values you have entered are not valid.')
                sys.tracebacklimit = None
                quit()
        d_b /= m
        d_w /= m
        return tuple((d_w, d_b))

    def linearRegression(self, showProcess=False, showResultingLine=False):
        w = -10
        b = -10
        past_w = -1
        past_b = -1
        iteration = 1
        while past_w != w and past_b != b:
            if showProcess:
                self.x_values = [0, 1]
                self.y_values = [b, w+b]
                self.lineGraph("Linear Regression Attempt " + str(iteration))
            past_w = w
            past_b = b
            gradients = self.computeGradient(w, b)
            w = w - gradients[0]
            b = b - gradients[1]
            iteration += 1
        if showResultingLine or showProcess:
            self.x_values = [0, 1]
            self.y_values = [b, w+b]
            self.line(w, b, "Best Fitting Line")
        return tuple((w, b))

