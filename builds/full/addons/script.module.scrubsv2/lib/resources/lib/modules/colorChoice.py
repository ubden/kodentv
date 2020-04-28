# -*- coding: UTF-8 -*-
# Original Code from NixGates.
# ColorChart remade from a color folder, old chart can be found in Seren.

from resources.lib.modules import control

colorChart = ['none', 'aliceblue', 'aqua', 
            'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 
            'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 
            'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 
            'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 
            'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 
            'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 
            'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'kodi', 
            'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 
            'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
            'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 
            'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
            'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 
            'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 
            'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 
            'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 
            'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 
            'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 
            'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'white', 'whitesmoke', 'yellow', 'yellowgreen']


def colorStringUI(text, color=None):
    try:
        text = text.encode('utf-8')
    except:
        try:
            text = bytes(text).decode('utf-8')
            text = str(text)
        except:
            pass
        pass
    if color is 'none' or color is '' or color is None:
        color = control.setting('unaired.identify')
        if color is '': color = 'darkred'
    try:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'
    except:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'

def colorChoiceUI():
    selectList = []
    for i in colorChart:
        selectList.append(colorStringUI(i, i))
    color = control.selectDialog(selectList)
    if color == -1: return
    control.setSetting('unaired.identify', colorChart[color])
    control.openSettings(query='0.16')


def colorStringPI(text, color=None):
    try:
        text = text.encode('utf-8')
    except:
        try:
            text = bytes(text).decode('utf-8')
            text = str(text)
        except:
            pass
        pass
    if color is 'none' or color is '' or color is None:
        color = control.setting('prem.identify')
        if color is '': color = 'darkmagenta'
    try:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'
    except:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'

def colorChoicePI():
    selectList = []
    for i in colorChart:
        selectList.append(colorStringPI(i, i))
    color = control.selectDialog(selectList)
    if color == -1: return
    control.setSetting('prem.identify', colorChart[color])
    control.openSettings(query='2.3')


def colorStringTI(text, color=None):
    try:
        text = text.encode('utf-8')
    except:
        try:
            text = bytes(text).decode('utf-8')
            text = str(text)
        except:
            pass
        pass
    if color is 'none' or color is '' or color is None:
        color = control.setting('torrent.identify')
        if color is '': color = 'darkorange'
    try:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'
    except:
        return '[COLOR ' + str(color) + ']' + text + '[/COLOR]'

def colorChoiceTI():
    selectList = []
    for i in colorChart:
        selectList.append(colorStringTI(i, i))
    color = control.selectDialog(selectList)
    if color == -1: return
    control.setSetting('torrent.identify', colorChart[color])
    control.openSettings(query='7.3')


