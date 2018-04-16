# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 10:03:00 2016

@author: yxl
"""
from __future__ import absolute_import
from __future__ import print_function

import wx, os.path as osp
from wx.lib.pubsub import pub

root_dir = osp.abspath(osp.dirname(__file__))

curapp = None

def load_plugins():
    from imagepy.core.loader import loader
    loader.build_plugins('menus', True)
    from glob import glob
    extends = glob('plugins/*/menus')
    for i in extends: loader.build_plugins(i, True)

def uimode():
    if curapp is None: return 'no'
    from .core import manager
    return manager.ConfigManager.get('uistyle')

def get_window():
    from .core import manager
    return manager.WindowsManager.get()

def get_twindow():
    from .core import manager
    return manager.WTableManager.get()

def get_ips():
    from .core import manager
    return manager.ImageManager.get()

def get_tps():
    from .core import manager
    return manager.TableManager.get()
    # return None if win==None else win.canvas.ips

def showips(ips):
    if uimode()=='ipy':
        from .ui.canvasframe import CanvasPanel
        canvasp = CanvasPanel(curapp.canvasnb)
        canvasp.set_ips(ips)
        curapp.canvasnb.add_page( canvasp, ips)
        #canvasp.canvas.initBuffer()
        
        curapp.auimgr.Update()
    elif uimode()=='ij':
        from .ui.canvasframe import CanvasFrame
        frame = CanvasFrame(curapp)
        frame.set_ips(ips)
        frame.Show()

pub.subscribe(showips, 'showips')
def show_ips(ips):
    if uimode()=='no':
        from .core import manager
        from .ui.canvasframe import VirturlCanvas
        frame = VirturlCanvas(ips)
        print('ImagePy New ImagePlus >>> %s'%ips.title)
    else: wx.CallAfter(pub.sendMessage, 'showips', ips=ips) 

def showimg(imgs, title):
    print('show img')
    from .imageplus import ImagePlus
    ips = ImagePlus(imgs, title)
    showips(ips)

pub.subscribe(showimg, 'showimg')
def show_img(imgs, title):
    if uimode()=='no':
        from .core import manager
        from .imageplus import ImagePlus
        from .ui.canvasframe import VirturlCanvas
        frame = VirturlCanvas(ImagePlus(imgs, title))
    else:wx.CallAfter(pub.sendMessage, 'showimg', imgs=imgs, title=title) 

def reloadplgs(report=False, menus=True, tools=False, widgets=False):
    print('reload........')
    curapp.reload_plugins(report, menus, tools, widgets)

pub.subscribe(reloadplgs, 'reload')
def reload_plgs(report=False, menus=True, tools=False, widgets=False):
    print('reload========')
    wx.CallAfter(pub.sendMessage, 'reload', report=report, menus=menus, tools=tools, widgets=widgets) 

def showmd(title, cont, url=''):
    from .ui.mkdownwindow import MkDownWindow
    MkDownWindow(curapp, title, cont, url).Show()

pub.subscribe(showmd, 'showmd')
def show_md(title, cont, url=''):
    wx.CallAfter(pub.sendMessage, 'showmd', title=title, cont=cont, url=url)
'''
def stepmacros(macros):
    macros.next()

pub.subscribe(stepmacros, 'stepmacros')
def step_macros(macros):
    wx.CallAfter(pub.sendMessage, "stepmacros", macros=macros)
'''
def alert(info, title="ImagePy Alert!"):
    if uimode()=='no':
        print('ImagePy Alert >>> %s'%title)
        print(info)
    else:
        dlg=wx.MessageDialog(curapp, info, title, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

# MT alert = lambda info, title='image-py':callafter(alert_, *(info, title))

def yes_no(info, title="ImagePy Yes-No ?!"):
    dlg = wx.MessageDialog(curapp, info, title, wx.YES_NO | wx.CANCEL)
    rst = dlg.ShowModal()
    dlg.Destroy()
    dic = {wx.ID_YES:'yes', wx.ID_NO:'no', wx.ID_CANCEL:'cancel'}
    return dic[rst]

def getpath(title, filt, k, para=None):
    """Get the defaultpath of the ImagePy"""
    from .core import manager
    dpath = manager.ConfigManager.get('defaultpath')
    if dpath ==None:
        dpath = root_dir # './'
    dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
    dialog = wx.FileDialog(curapp, title, dpath, '', filt, dic[k])
    rst = dialog.ShowModal()
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        dpath = osp.split(path)[0]
        manager.ConfigManager.set('defaultpath', dpath)
        if para!=None:para['path'] = path
    dialog.Destroy()

    return rst if para!=None else path

def getdir(title, filt, para=None):
    from .core import manager
    dpath = manager.ConfigManager.get('defaultpath')
    if dpath ==None:
        dpath = root_dir
    dialog = wx.DirDialog(curapp, title, dpath )
    rst = dialog.ShowModal()
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        if para!=None:para['path'] = path
    dialog.Destroy()
    return rst if para!=None else path

def get_para(title, view, para):
    from .ui.panelconfig import ParaDialog
    pd = ParaDialog(curapp, title)
    pd.init_view(view, para)
    rst = pd.ShowModal()
    pd.Destroy()
    return rst

def showtable(title, data):
    from .ui.tablewindow import TableFrame
    from imagepy.tableplus import TablePlus
    tps = TablePlus(title, data)
    frame = TableFrame(curapp)
    frame.set_tps(tps)
    frame.Show()   
    # MT callafter(TableLog.table, *(title, data, cols, rows))
    
pub.subscribe(showtable, 'showtable')
def table(title, data):
    wx.CallAfter(pub.sendMessage, "showtable", title=title, data=data) 

def showlog(title, cont):
    from .ui.logwindow import TextLog
    TextLog.write(cont, title)
pub.subscribe(showlog, 'showlog')

def write(cont, title='ImagePy'):
    if curapp is None:
        print('ImagePy Write >>> %s'%title)
        print(cont)
    else:
        from .ui.logwindow import TextLog
        wx.CallAfter(pub.sendMessage, 'showlog', title=title, cont=cont)

def plot(title, gtitle='Graph', labelx='X-Unit', labely='Y-Unit'):
    from .ui.plotwindow import PlotFrame
    return PlotFrame.get_frame(title, gtitle, labelx, labely)

#def set_progress(i):
#    curapp.set_progress(i)
    # MT callafter(curapp.set_progress, i)

def set_info(i):
    if curapp is None: print('ImagePy Info >>> %s'%i)
    else: wx.CallAfter(curapp.set_info, i)
    # MT callafter(curapp.set_info, i)

def run(cmd):
    from imagepy.core.engine import Macros
    Macros('', cmd.replace('\r\n', '\n').split('\n')).start()