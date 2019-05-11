import numpy as np
from loguru import logger


def test():
    print('installed')


def robust_max(window):
    """Calculate max of the window while omitting outer fence values
    
    Arguments:
        window {pd.Series} -- [description]
    
    Returns:
        number -- maximum value found in the window
    """
    median = window.quantile(0.5)
    q25 = window.quantile(0.25)
    q75 = window.quantile(0.75)
    iqr = q75 - q25
    window[(window>median+1.5*iqr)|(window<median-1.5*iqr)] = np.nan

    return window.max()


def cp_fit(best_max):
    """Calculate CP by fitting 1..20 min best max values 
    
    Arguments:
        best_max {ndarray} -- best max values for [1, 2, 3, 5, 8, 10, 20] min
    
    Returns:
        CP [number] -- [Critical power as in the CP + W'/T model]
    """
    def func(x, cp, w):
        return cp + w/x
    ydata = best_max.values[~np.isnan(best_max.values)]
    assert len(ydata)==7, "best max must contain 7 values for [1, 2, 3, 5, 8, 10, 20] min"
    xdata = np.array([1, 2, 3, 5, 8, 10, 20])[~np.isnan(best_max.values)]
    try:
        popt, pcov = curve_fit(func, xdata, ydata, p0=[ydata[-1], 20000/60])
        logger.debug(f"cp_fit with values CP: {popt[0]}, W': {popt[1]} and pcov: {pcov}")
    except:
        return np.nan
    return popt[0]