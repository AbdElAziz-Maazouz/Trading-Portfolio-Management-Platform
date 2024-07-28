from datetime import datetime
import sys
import pandas as pd
import mplfinance as mpf
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class MainWindow(QWidget):
    def __init__(self, df,parent=None):
        super().__init__()
        self.setParent(parent)
        self.initUI(df)

    def initUI(self,df):
        self.setStyleSheet("background-color:white;")
        self.layout = QVBoxLayout(self)
        # style of lines
        self.colors = mpf.make_mpf_style(
            base_mpf_style="charles",
            facecolor="white",
            edgecolor="white",
            gridcolor="white",
            gridstyle="dotted",
        )
        self.setGeometry(5, 161, 951, 471)
        # read data and create mplfinance plot
        self.df = df
        self.plots=[]
        # print(self.df)
        self.fig, _ = mpf.plot(
            self.df,
            type="line",
            volume=False,
            style=self.colors,
            returnfig=True,
            figsize=(7.09, 2.9)
        )
        # create a FigureCanvas widget to embed the mplfinance plot
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
                

    def simplePlot(self,dtyp):
        self.canvas.figure.clf()

        self.fig, _ = mpf.plot(
            self.df,
            type=dtyp,
            addplot=self.plots,
            volume=False,
            style=self.colors,
            returnfig=True,
            figsize=(9.3, 4.7)
        )
        self.canvas.figure=self.fig
        self.canvas.draw()
        self.setGeometry(5, 161, 951, 471)


    # def AjoutPlot(self):
    #     # Create the figure and axis objects
    #     fig, ax = mpf.plot(
    #         self.df_list[0],
    #         type=dtyp,
    #         addplot=self.plots,
    #         volume=False,
    #         style=self.colors,
    #         returnfig=True,
    #     )

    #     # Plot each dataframe in self.df_list on the same axis
    #     for i in range(1, len(self.df_list)):
    #         mpf.plot(
    #             self.df_list[i],
    #             type=dtyp,
    #             addplot=self.plots,
    #             volume=False,
    #             style=self.colors,
    #             ax=ax[0],  # Use the first Axes object in the list
    #             returnfig=True, 
    #         )

    #     # Set the size of the figure
    #     fig.set_size_inches(9.3, 4.7)

    #     # Update the canvas with the new plot
    #     self.canvas.figure = fig
    #     self.canvas.draw()

    #     # Set the window geometry
    #     self.setGeometry(5, 161, 951, 471)



    

    def AjoutPlot(self,dtyp):
        self.canvas.figure.clf()

        df_list_plot = []
        for df in self.df_list:
            if dtyp == "line": ap = mpf.make_addplot(df['Close'])
            else: ap = mpf.make_addplot(df ,type=dtyp)
            df_list_plot.append(ap)

        fig, _ = mpf.plot(
            self.df_list[0],
            type=dtyp,
            addplot=df_list_plot[1:],
            volume=False,
            style=self.colors,
            returnfig=True,
        )

        fig.set_size_inches(9.3, 4.7)
        self.canvas.figure = fig
        self.canvas.draw()


        # Set the window geometry
        self.setGeometry(5, 161, 951, 471)



    # def redraw_chart_with_indicators(self):
    #     # Calculate RSI, SMA and WMA
    #     rsi = talib.RSI(self.df['Close'], timeperiod=5)
    #     sma = talib.SMA(self.df['Close'], timeperiod=5)
    #     wma = talib.WMA(self.df['Close'], timeperiod=5)

    #     # Combine data into a DataFrame
    #     data = pd.DataFrame({'Close': self.df['Close'],'Open':self.df['Open'],'High':self.df['High'],'Low':self.df['Low'],'Volume':self.df['Volume'], 'RSI': rsi, 'SMA': sma, 'WMA': wma})
        
    #     # Plot the linestick chart with RSI, SMA and WMA
    #     fig, _ = mpf.plot(data, type='line', volume=True, style=self.colors,
    #                     mav=(20, 10), addplot=[mpf.make_addplot(rsi, panel=1),
    #                                             mpf.make_addplot(sma, panel=0),
    #                                             mpf.make_addplot(wma, panel=0)],
    #                     returnfig=True,figsize=(9.3, 4.7))
        
    #     self.canvas.figure=fig
    #     self.canvas.draw()

    # def setRsi(self,period=5):
    #     # Calculate RSI, SMA and WMA
    #     rsi = talib.RSI(self.df['Close'], timeperiod=period)
    #     self.plots.append(mpf.make_addplot(rsi,panel=0))
    #     # Combine data into a DataFrame
    #     data = pd.DataFrame({'Close': self.df['Close'],'Open':self.df['Open'],'High':self.df['High'],'Low':self.df['Low'],'Volume':self.df['Volume'], 'RSI': rsi})
        
    #     # Plot the linestick chart with RSI, SMA and WMA
    #     fig, _ = mpf.plot(data, type='line', volume=True, style=self.colors, addplot=self.plots, returnfig=True,figsize=(9.3, 4.7))
        
    #     # Set the new figure for the canvas widget
    #     self.canvas.figure=fig
    #     self.canvas.draw()

    # def setSma(self,period=5):
    #     # Calculate RSI, SMA and WMA
    #     sma = talib.SMA(self.df['Close'], timeperiod=period)

    #     # Combine data into a DataFrame
    #     data = pd.DataFrame({'Close': self.df['Close'],'Open':self.df['Open'],'High':self.df['High'],'Low':self.df['Low'],'Volume':self.df['Volume'], 'SMA': sma})
    #     self.plots.append(mpf.make_addplot(sma, panel=0))
    #     # Plot the linestick chart with RSI, SMA and WMA
    #     fig, _ = mpf.plot(data, type='line', volume=True, style=self.colors, addplot=self.plots, returnfig=True,figsize=(9.3, 4.7))
        
    #     # Set the new figure for the canvas widget
    #     self.canvas.figure=fig
    #     self.canvas.draw()
    # def deleteOne(self):
    #     if len(self.plots)>0:
    #       self.plots.pop()
    #     else:
    #         return

    # def setWma(self,period=5):
    #     # Calculate RSI, SMA and WMA
    #     wma = talib.WMA(self.df['Close'], timeperiod=period)
    #     # Combine data into a DataFrame
    #     data = pd.DataFrame({'Close': self.df['Close'],'Open':self.df['Open'],'High':self.df['High'],'Low':self.df['Low'],'Volume':self.df['Volume'], 'WMA': wma})
    #     self.plots.append(mpf.make_addplot(wma, panel=0))
    #     # Plot the linestick chart with RSI, SMA and WMA
    #     fig, _ = mpf.plot(data, type='line', volume=True, style=self.colors, addplot=self.plots, returnfig=True,figsize=(9.3, 4.7))
        
    #     # Set the new figure for the canvas widget
    #     self.canvas.figure=fig
    #     self.canvas.draw()


