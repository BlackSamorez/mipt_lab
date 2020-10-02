from ROOT import TCanvas, TGraph, TGraphErrors, TF1, TFitResultPtr
from ROOT import gROOT
import numpy as np
import pandas as pd
from array import array

# Load data
filename = "2318.csv"
data = pd.read_csv(filename, engine='python', sep = ';', header=None)

x = array('d')
ex = array('d')
y = array('d')
ey = array('d')

x.fromlist(list(np.array(data[1])))
y.fromlist(list(np.array(data[4])))
ex.fromlist(list(np.array(data[3])))
ey.fromlist(list(np.array(data[5])))

c1 = TCanvas('c1', 'A Simple Graph with error bars', 200, 10, 700, 500)

c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )

gr = TGraphErrors( len(x), x, y, ex, ey )

ff = TF1('ff', 'pol1', -1, 2)

# ff.SetParameters( 7.6e+02, -3.7, 1.e-01)

fit = gr.Fit(ff,'srf')

print(fit.Ndf())
print(fit.Chi2())

gr.SetTitle( 'Calibration' )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 20 )
gr.GetXaxis().SetTitle( '#omega, 10^{15} 1/s' )
gr.GetYaxis().SetTitle( 'V_{0}, V' )
gr.Draw( 'ap' )
# ff.Draw()

c1.Update()

# gr = TGraph( len(x), x, y )
# # gr.SetLineColor( 2 )
# # gr.SetLineWidth( 4 )
# # gr.SetMarkerColor( 4 )
# gr.SetMarkerStyle( 21 )
# gr.SetTitle( 'a simple graph' )
# gr.GetXaxis().SetTitle( 'X title' )
# gr.GetYaxis().SetTitle( 'Y title' )
# gr.Draw( 'ACP' )
#
# c1.Update()
# c1.GetFrame().SetFillColor( 21 )
# c1.GetFrame().SetBorderSize( 12 )
# c1.Modified()
# c1.Update()

gROOT.GetListOfCanvases().Draw()

q = input()