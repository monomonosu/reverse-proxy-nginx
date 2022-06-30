
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import BaseDocTemplate,Frame,PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle as PS

from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

from reportlab.platypus.flowables import Spacer

from reportlab.pdfgen import canvas


import json
import sys
import re
#import cStringIO
from importlib import import_module
import json
import os

import pprint


#----------　フォント定義------------
pdfmetrics.registerFont(TTFont('IPAexGothic','./ipaexg.ttf'))
pdfmetrics.registerFont(TTFont('IPAexMincho','./ipaexm.ttf'))


psize ={
    "A3":{ "short": 297, "long": 420},
    "A4":{ "short": 210, "long": 297},
    "A5":{ "short": 148, "long": 210},
    "A6":{ "short": 105, "long": 148},
    "B4":{ "short": 257, "long": 364},
    "B5":{ "short": 182, "long": 257},
    "B6":{ "short": 128, "long": 182},
}



class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        if page_count > 1 :
            self.drawRightString(200*mm, 5*mm,
                "Page %d of %d" % (self._pageNumber, page_count))


def make_table(table_info):

    if not table_info.get('table'): return

    t_data = table_info['table']

    for i,row in enumerate(t_data):
        for j,col in enumerate( row ):
            if type(col) is list:
                col_val = cv(col)          
            else:
                col_val  = col
            t_data[i][j] = col_val

    if 'row_heights' in table_info:
        ht=Table(t_data,colWidths=cv(table_info['col_widths']),rowHeights=cv(table_info['row_heights']))
    else:    
        ht=Table(t_data,colWidths=cv(table_info['col_widths']))

    t_styles = []
    if table_info.get('table_style'):
        for t_style in table_info['table_style']:
            cv_style = cv(t_style)
            if cv_style : t_styles.append(cv_style)

    ht.setStyle(TableStyle(t_styles))

    if table_info.get('hAlign'):
        ht.hAlign = table_info.get('hAlign')

    return ht


def make_row(detail,bdata):
    _ROWNUM = 0

    vals_l =[]
    fields = detail['fields']
    for b_row in bdata:
        vals = []
        col_width = 0
        for f in fields:
            k = f['key']
            val = b_row.get(k) #値の取得
            #print("row val:", val,type(val))
            if 'eval' in f:
                val = eval(str(f.get('eval')))
            if not val:
                val='&nbsp;'  #空行対応
            else:
                if 'format' in f:
                    if val:
                        fmt = f.get('format')
                        try:
                            if fmt: val = fmt.format(val)
                        except:
                            val="format error!"
            val = Paragraph(str(val),PS(**styles[f.get('p_style')]))
            vals.append(val)
        #print(vals)
        _ROWNUM += 1
        vals_l.append(vals)
    #空白行の作成
    row_max = detail.get('row_max')
    fld_len = len(fields)
    sp_row_len = row_max - len(bdata)
    sp_row = [['']*fld_len]*sp_row_len
    vals_l = vals_l + sp_row

    return vals_l

def make_detail(detail,bdata):

    th_style = detail.get('label_style')
    labels = [Paragraph(f.get('label'),PS(**styles[th_style])) for f in detail['fields']]
    vals_l = make_row(detail,bdata)
    vals_l.insert(0,labels)
    col_width_l = [int(f.get('width'))*mm for f in detail['fields']]

    bt=Table(vals_l,repeatRows=1,colWidths=col_width_l)

    t_styles = []
    for t_style in detail['styles']:
        cv_style = cv(t_style)
        if cv_style : t_styles.append(cv_style)
    #stripe設定
    if detail.get('stripe_backgrounds'):
        clr = detail['stripe_backgrounds']
        stripes = [
            ('BACKGROUND',(0,i),(-1,i),eval(clr[i%2]))
            for i in range(1,len(vals_l))
        ]
        #print("stripes:", stripes)
        t_styles = t_styles + stripes
        #print(t_styles)

    bt.setStyle(TableStyle(t_styles))

    return bt


def on_page(canvas, doc):
    canvas.saveState()


    #print(f"----- page number at footer ----- { canvas._pageNumber } ")
    canvas.setTitle(defPdf['attr']['name_jp'])

    if not (defPdf.get('footer') or defPdf.get('first_page') ): return

    if canvas._pageNumber == 1:
        if defPdf['header'].get('drawBaseImages'):
            for di in defPdf['header'].get('drawBaseImages'):
                if di:
                    cmd = f'canvas.drawImage{di[0]}'
                    #print(cmd)
                    eval(cmd)
        if defPdf.get('first_page'):
            if defPdf['first_page'].get('pos_xy') : x,y =cv(defPdf['first_page']['pos_xy'])
            for table_info in defPdf['first_page'].get('table_infos'):
                if not table_info: continue
                if table_info.get('pos_xy'): x,y =cv(table_info.get('pos_xy'))
                ft = make_table(table_info)
                ft.wrapOn(canvas, x, y)
                ft.drawOn(canvas, x, y)
                            
    if defPdf.get('footer'):
        if defPdf['footer'].get('pos_xy') : x,y =cv(defPdf['footer']['pos_xy'])
        if defPdf['footer'].get('table_infos'):
            for table_info in defPdf['footer'].get('table_infos'):
                if not table_info: continue
                if table_info.get('pos_xy'): x,y =cv(table_info.get('pos_xy'))
                ft = make_table(table_info)
                ft.wrapOn(canvas, x, y)
                ft.drawOn(canvas, x, y)

    #print("_pageNumber:",canvas._pageNumber)
    if canvas._pageNumber == 1:
        for di in defPdf['header'].get('drawImages'):
            if di:
                cmd = f'canvas.drawImage{di[0]}'
                #print(cmd)
                eval(cmd)
        if defPdf.get('first_page'):
            for di in defPdf['first_page'].get('drawImages'):
                if di:
                    cmd = f'canvas.drawImage{di[0]}'
                    #print(cmd)
                    eval(cmd)


    if defPdf.get('footer'):
        for di in defPdf['footer'].get('drawImages'):
            if di:
                cmd = f'canvas.drawImage{di[0]}'
                #print(cmd)
                eval(cmd)


    canvas.restoreState()


def firstPage(canvas):
    #print("------- first page-------------")
    pass

def coords(canvas):
    #print("-----COORDS-------")
    pass

def monitor(type,val):
    #print(type,val)
    pass

def page_break(pageno):

    #print(f"-----------Page Break {pageno}------------------------")
    pass

def cv(src_l):
    if not src_l: return
    if not src_l[1]: return ''
    #print ("src_l:" ,src_l[1])
    try:
        if src_l[0] == "P": 
            val = src_l[1] if src_l[1] else ''
            return Paragraph(src_l[1],PS(**styles[src_l[2]]))
        elif  src_l[0] == "PF":
            val = src_l[3].format(src_l[1])
            return Paragraph(val,PS(**styles[src_l[2]]))
        elif  src_l[0] == "E":
            return eval(src_l[1])
        elif  src_l[0] == "EP":
            return Paragraph(eval(src_l[1]),PS(**styles[src_l[2]]))
        elif  src_l[0] == "EPF":
            val = src_l[3].format(eval(src_l[1]))
            return Paragraph(val,PS(**styles[src_l[2]]))
        elif  src_l[0] == "NOP":
            return 
    except :
        return Paragraph("value or format error! ",PS(**styles['sm_l']))

    return Paragraph("No instraction ",PS(**styles['sm_l']))

data={}
defPdf ={}
styles ={}
def pdf_maker(d,is_BytesIO=False,file_name=''):
    global data
    data = d.get('data')

    global defPdf
    defPdf = d.get('defPdf')

    global styles
    styles = d.get('style')

    #_HEAD = data['hdata']
    #_ROWS = data['bdata']
    #_SUM = data['sum']

    #----ドキュメント本体-----

    attr_name = defPdf['attr']['name']
    alter_file_name = ''
    if is_BytesIO:
        pfile = BytesIO()
    else:
        if file_name:
            alter_file_name = file_name
        else:
            alter_file_name = defPdf['file']['file_name']
        pfile = defPdf['file']['outDir']+"/"+ alter_file_name

    size = defPdf['attr']['page_size']
    if defPdf['attr']['page_type']=="landscape":
        w = psize[size]['long']*mm
        h = psize[size]['short']*mm
    else:
        w = psize[size]['short']*mm
        h = psize[size]['long']*mm
    #w,h = A4
    os.makedirs(defPdf['file']['outDir'], exist_ok=True)

    doc = BaseDocTemplate(pfile, pagesize=[w,h])
    #doc = BaseDocTemplate(sys.stdout, pagesize=A4)

    #top_mergin = 20*mm
    top_mergin = defPdf['attr']['top_mergin']*mm
    ft_size = defPdf['attr']['footter_size']*mm

    frames = [
        Frame(0 * mm, ft_size, w, h-ft_size-top_mergin, showBoundary=0)
    ]

    page_template = PageTemplate("frames", frames=frames,onPage=on_page)
    #page_template = PageTemplate("frames", frames=frames)
    #beforeDrawPage(canv,doc):
    #    print ("----brfore draw pae------"
    doc.addPageTemplates(page_template)

    #-----タイトル表示 ------
    elements = []

    #elements.append(cv(defPdf['header']['title']))
    #elements.append(cv(defPdf['header']['title_after']))
    #drawImages(defPdf['header']['drawImages'])

    elements.append(cv(defPdf['header'].get('title')))
    elements.append(cv(defPdf['header'].get('title_after')))

    if defPdf.get('header'):
        for table_info in defPdf['header'].get('table_infos'):
            if table_info.get('before') : elements.append(cv(table_info.get('before')))
            ht = make_table(table_info)
            elements.append(ht)
            if table_info.get('after') : elements.append(cv(table_info.get('after')))

    if data.get('bdata'):
        bt = make_detail(defPdf['body']['detail'],data.get('bdata'))
        elements.append(bt)

        if defPdf['body'].get('detail_after'):
            bt = make_table(defPdf['body']['detail_after'].get('table_info'))
            elements.append(bt)

    #ft = make_table(defPdf['footer']['table_info'])
    #elements.append(ft)

    doc.setProgressCallBack(monitor)
    doc.setPageCallBack(page_break)
        

    doc.build(elements,canvasmaker=NumberedCanvas)
    #doc.build(elements)

    if is_BytesIO:
        pfile.seek(0)
        return pfile.read()
    else:
        return alter_file_name


#------- initial ---------
if __name__ == '__main__':

    args = sys.argv
    if len(args) == 1 :
        json_file_name = './data.json'
    elif len(args) ==2:
        json_file_name = args[1]
    else:
        print("パラメータエラー\n")
        sys.exit()        

    with open( json_file_name, mode='r', encoding='utf-8') as f:
        d = json.load(f)

    pdf_maker(d)


