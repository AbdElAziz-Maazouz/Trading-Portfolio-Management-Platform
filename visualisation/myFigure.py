from datetime import datetime
import sys
import pandas as pd
import mplfinance as mpf
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import talib






def MACD(df, window_slow, window_fast, window_signal):
    macd = pd.DataFrame()
    macd['ema_slow'] = df['Close'].ewm(span=window_slow).mean()
    macd['ema_fast'] = df['Close'].ewm(span=window_fast).mean()
    macd['macd'] = macd['ema_slow'] - macd['ema_fast']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    return macd



class MainWindow(QWidget):
    def __init__(self, df,parent=None):
        super().__init__()
        self.setParent(parent)
        self.initUI(df)

    def initUI(self,df):
        self.setStyleSheet("background-color:white;")
        self.layout = QVBoxLayout(self)
        # style of candles
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
        self.plot_exist_in_plots=False
        self.fig, _ = mpf.plot(
            self.df,
            type="candle",
            volume=True,
            style=self.colors,
            returnfig=True,
            figsize=(7.09, 2.9)
        )
        
        # create a FigureCanvas widget to embed the mplfinance plot
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.simplePlot()
        # self.ajouterSymbol()


    def getMacd(self):
        macd = MACD(self.df,12,26,9)
        macd_plot = [
        # mpf.make_addplot((macd['macd']), color='#606060', panel=2, ylabel='MACD', secondary_y=False),
        # mpf.make_addplot((macd['signal']), color='#1f77b4', panel=2, secondary_y=False),
        mpf.make_addplot((macd['bar_positive']), type='bar', color='#4dc790', panel=2),
        mpf.make_addplot((macd['bar_negative']), type='bar', color='#fd6b6c', panel=2),
        ]
        return macd_plot
    
    def affiche(self,data):
        self.fig, _ = mpf.plot(data, type='candle', volume=True, addplot=self.plots,returnfig=True,style=self.colors,figsize=(9.3, 4.7))
        self.canvas.figure=self.fig
        self.canvas.draw()
        self.setGeometry(5, 161, 951, 471)

    def simplePlot(self):
        while len(self.plots)>0:
            self.plots.pop()
        self.plot_exist_in_plots=False
        # if self.plot_exist_in_plots==False:
        #     self.plots.insert(0,self.getMacd()[0])
        #     self.plots.insert(1,self.getMacd()[1])
        #     self.plot_exist_in_plots=True
        self.affiche(self.df)


    def ajouterSymbol(self):
        # create two addplot objects, one for each data frame
        addplot1 = mpf.make_addplot(self.df, type="candle", color="green")
        addplot2 = mpf.make_addplot(self.df2, type="candle", color="blue")
        addplot3 = mpf.make_addplot(self.df3, type="candle", color="yellow")
        # plot both data frames using mpf.plot() function with addplot parameters set to the addplot objects
        mpf.plot(
            self.df,
            type="candle",
            volume=True,
            addplot=[addplot1, addplot2,addplot3],
            style=self.colors,
            figsize=(9.3, 7),
            title="Comparison of Two Symbols"
        )

    def drawIndicator(self,indicator_name,period):
        # if self.plot_exist_in_plots==False:
        #     self.plots.insert(0,self.getMacd()[0])
        #     self.plots.insert(1,self.getMacd()[1])
        #     self.plot_exist_in_plots=True
        ind=getattr(talib,indicator_name)
        indicator=ind(self.df['Close'], timeperiod=period)
        if indicator_name=="RSI":
            p=2
        else:
            p=0
        self.plots.append(mpf.make_addplot(indicator,panel=p))
        data = pd.DataFrame({'Close': self.df['Close'],'Open':self.df['Open'],'High':self.df['High'],'Low':self.df['Low'],'Volume':self.df['Volume'], f'{indicator_name}': indicator})
        self.affiche(data)
        
    def deleteOne(self):
        if len(self.plots)>2:
          self.plots.pop()
        else:
            return




