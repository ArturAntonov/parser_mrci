# parser_mrci
Python parser for Historical feature prices from the mrci.com


Here a website https://www.mrci.com/ohlc/2005/051212.php

There are features prices on this page (we will call them as the ticker)
The webpage url is according to date from a Date column (calendar date) on which these tickers have received.
 
The column descriptions:
Mth - a month, when a feature expires
Date - current date (the date on which features present)
Open, High, Low, Close - these values is interesting

Note:
The ticker's name + Mth uniquely identify each of time series

For this task we will parse data for some traders:
Brent Crude Oil(ICE)
Gas Oil(ICE)
Natural Gas(NYM)
Crude Oil(NYM)

I will parse data for for all of these traders.