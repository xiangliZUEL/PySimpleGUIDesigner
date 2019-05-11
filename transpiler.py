from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

IMPLEMENTED_CONTAINERS = [QGridLayout,
						  QVBoxLayout, QHBoxLayout, QGroupBox, QFrame, QWidget]
IMPLEMENTED_CONTROL_ELEMENTS = [
	QLabel, QSpinBox, QCheckBox, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit]
isCrate 		= lambda item: type(item) in IMPLEMENTED_CONTAINERS
isNormalWidget 	= lambda item: type(item) in IMPLEMENTED_CONTROL_ELEMENTS


def empty_widget(GUItype='tk'):
	# dummy elemets for EMPTY SPOTS in QGridLayout
	if GUItype == 'tk':
		return 'sg.T("")'
	if GUItype == 'qt':
		return 'sg.HSep()'
	if GUItype == 'web':
		raise Exception("Not IMPLEMENTED")
	if GUItype == 'wx':
		raise Exception("Not IMPLEMENTED")


def get_chidrens(node):
	elements = []

	if type(node) in [QGroupBox, QFrame]:
		items = node.children()
		item_1st = items[0]
		if type(item_1st) in [QGridLayout, QHBoxLayout, QVBoxLayout]:
			return get_chidrens(item_1st)
		else:
			raise Exception(f'HOWTO find childrens in "{node.objectName()}" -> {node}')

	elif type(node) is QHBoxLayout or type(node) is QVBoxLayout:

		for i in range(node.count()):
			el = node.itemAt(i)
			obj = el.widget() if type(el) is QWidgetItem else el
			elements.append(obj)
		return elements

	elif type(node) is QGridLayout:

		for i in range(node.rowCount()):
			row = []
			for j in range(node.columnCount()):
				item = node.itemAtPosition(i, j)
				item = item.widget() if type(item) is QWidgetItem else item
				row.append(item)
			elements.append(row)
		return elements

	else:
		raise Exception(f'HOWTO find childrens in {type(node)}')


#                       _
#                      | |
#  _ __ ___   ___  __ _| |_
# | '_ ` _ \ / _ \/ _` | __|
# | | | | | |  __/ (_| | |_
# |_| |_| |_|\___|\__,_|\__|


#   ____  __  __                  ____
#  / __ \|  \/  |                |  _ \
# | |  | | \  / | ___ _ __  _   _| |_) | __ _ _ __
# | |  | | |\/| |/ _ \ '_ \| | | |  _ < / _` | '__|
# | |__| | |  | |  __/ | | | |_| | |_) | (_| | |
#  \___\_\_|  |_|\___|_| |_|\__,_|____/ \__,_|_|

class Pepe(object):
	def __init__(self, title, ob='', nodes=[]):
		self.title = title
		self.ob = ob
		self.nodes = nodes
	def nest_2(self, lvl=0):
		# mehh...
		tabs = '\t'*lvl
		if self.nodes:
			nodes = ',\n'.join([i.nest(lvl+1) for i in self.nodes])
			nodes = f', nodes=\n{nodes})\n'
		else:
			nodes = ')'
		return f'{tabs}Node("{self.title}"{nodes}'
	def nest_1(self, lvl=0):
		# working
		tabs = '\t'*lvl if not one_line else ''
		return_line__join = ',\n'
		if self.nodes:
			nodes = ',\n'.join([i.nest(lvl+1, one_line) for i in self.nodes])
			return f'{tabs}"{self.title}", [\n{nodes}\n{tabs}]'
		else:
			return f'{tabs}"{self.title}"'
	def nest(self, lvl=0, one_line=False):
		# added keyword paramas
		if one_line:
			tabs = ''
			return_line__join = ', '
			return_line_1 = ''
			return_line_2 = ' '
		else:
			tabs = '\t'*lvl
			return_line__join = ',\n'
			return_line_1 = '\n'
			return_line_2 = '\n'
		
		if self.nodes:
			nodes = [i.nest(lvl+1, one_line) for i in self.nodes]
			nodes = return_line__join.join(nodes)
			return f'{tabs}"{self.title}", [{return_line_1}{nodes}{return_line_2}{tabs}]'
		else:
			return f'{tabs}"{self.title}"'

	def __repr__(self):
		return f'Node("{self.title}", nodes={repr(self.nodes)})'
	def __str__(self):
		childrens = ''
		ob = f':{self.ob}' if self.ob else ''
		if self.nodes:
			childrens = ', [' + ', '.join([str(i) for i in self.nodes]) + ']'
		return f"['{self.title}{ob}'{childrens}]"
def parseQMenu_obj(qmenu, lvl=0):
	try:
		actions 	= qmenu.actions()
		pepes = []
		for a in actions:
			pepe = Pepe('')
			# вывести текст
			if not a.isSeparator():
				pepe.title = a.iconText()

				# вывести вложенные менюшки
				menus = []
				try:
					menus = parseQMenu_obj(a.menu(), lvl+1)
				except Exception as e:
					pass
				pepe.nodes = menus
			else:
				pepe.title = '---'
			pepes.append(pepe)

		return pepes
	except Exception as e: # листок
		pass
		return Pepe(qmenu.title())
def make_psg_menu(qmenubar: QMenuBar, menubar_oneline=False):
	res = parseQMenu_obj(qmenubar)
	res = '[' + ',\n'.join(['[' + i.nest(menubar_oneline) + ']' for i in res]) + ']'
	return res

# ======
# ======
# ======



def to_psg_element(normal_item, size='', GUItype='tk', pass_bad_widgets=False, pure=False, menubar_oneline=False):

	if size != '' and type(size) in [tuple, list] and len(size) == 2:
		size = 'size=({0}, {1}), '.format(*size)
	elif size == '':
		pass
	else:
		raise Exception(f'BAD size: {size}')

	idd = normal_item.objectName()
	res = type(normal_item)
	print(f'res = {res}')

	#                  _        _
	#                 | |      (_)
	#   ___ ___  _ __ | |_ __ _ _ _ __   ___ _ __ ___
	#  / __/ _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
	# | (_| (_) | | | | || (_| | | | | |  __/ |  \__ \
	#  \___\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/


	if type(normal_item) in [QVBoxLayout, QHBoxLayout, QGridLayout]:
		compiler = compile_VBbox if type(
			normal_item) != QGridLayout else compile_GridLayout
		ui = compiler(normal_item, is_top=False, make_tabs=2,
					  GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		return ui if pure else f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"

	elif type(normal_item) is QWidget:
		# return to_psg_element(normal_item.children()[0], pure=pure)
		return to_psg_element(normal_item.children()[0], size=size, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets, pure=pure)
	elif type(normal_item) is QTabWidget:

		# core
		pages = normal_item.children()[0].children()
		tabs = [i for i in pages if type(i) == QWidget]
		tabs = [[	index,
				  normal_item.tabText(index),
				  to_psg_element(widget_in_tab, pure=True).strip()
				  ] for index, widget_in_tab in enumerate(tabs)]

		# 1
		variables_and_ui = '\n\n'.join([f'tab{i}_layout = [\n\t\t{ui}\n]' for i, title, ui in tabs])

		# 2
		sg_tab = ', '.join([f"sg.Tab('{title}', tab{i}_layout)" for i, title, ui in tabs])
		sg_TabGroup = f"sg.TabGroup([[{sg_tab}]], {size}key='{idd}')"

		return variables_and_ui + '\n\n' + sg_TabGroup

	elif type(normal_item) in [QFrame, QGroupBox]:

		children = normal_item.children()[0]

		if type(children) is QGridLayout:
			ui = compile_GridLayout(children,   make_tabs=2,
				GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		elif type(children) in [QVBoxLayout, QHBoxLayout]:
			ui = compile_VBbox(children,        make_tabs=2,
				GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		else:
			raise Exception(f'How do I parse {children}')

		title = ''
		if type(normal_item) is QGroupBox:
			title = normal_item.title()
		return f"sg.Frame('{title}', {size}key='{idd}', layout = [\n{ui}\n])"

	# menu
	elif type(normal_item) is QMenuBar:


		qmenubar_layout = make_psg_menu(normal_item, menubar_oneline)
		return f"qmenubar_layout = {qmenubar_layout}\n\nsg.Menu(qmenubar_layout, key='{idd}')"


	#                  _             _            _     _            _
	#                 | |           | |          (_)   | |          | |
	#   ___ ___  _ __ | |_ _ __ ___ | | __      ___  __| | __ _  ___| |_ ___
	#  / __/ _ \| '_ \| __| '__/ _ \| | \ \ /\ / / |/ _` |/ _` |/ _ \ __/ __|
	# | (_| (_) | | | | |_| | | (_) | |  \ V  V /| | (_| | (_| |  __/ |_\__ \
	#  \___\___/|_| |_|\__|_|  \___/|_|   \_/\_/ |_|\__,_|\__, |\___|\__|___/
	#                                                      __/ |
	#                                                     |___/

	# label
	elif type(normal_item) is QLabel:
		text = normal_item.text()
		return f"sg.I('{text}', {size}key='{idd}')"

	elif type(normal_item) is QGraphicsView:
		img_file = normal_item.toolTip()
		return f"sg.Image(r'{img_file}', {size}key='{idd}')"

	# items
	elif type(normal_item) is QComboBox:
		w = normal_item
		curr 	= w.currentText()
		values 	= str([w.itemText(i) for i in range(w.count())])
		return f"sg.Combo({values}, default_value=\"{curr}\", {size}key='{idd}')"
		# return f"sg.Spin({values}, initial_value=\"{curr}\", {size}key='{idd}')"

	elif type(normal_item) is QListWidget:
		w = normal_item

		curr 	= w.currentItem()
		curr 	= f'default_value={curr.text()}, ' if curr else ''

		values = str([w.item(i).text() for i in range(w.count())])
		size = "size=(30, 10), "
		return f"sg.Listbox({values}, {size}key='{idd}')"

	# int
	elif type(normal_item) is QSpinBox:
		w = normal_item
		mina, maxa, curr = w.minimum(), w.maximum(), w.value()
		return f"sg.Spin(list(range({mina}, {maxa})), initial_value={curr}, {size}key='{idd}')"

	elif type(normal_item) is QDoubleSpinBox:
		w = normal_item

		min_, max_, curr, step = float(w.minimum()), float(w.maximum()), w.value(), float(w.singleStep())
		amount = ((max_*1000000-min_*1000000)/1000000)/step
		# return f"sg.Spin(list(np.linspace({min_}, {max_}, {amount})), initial_value={curr}, {size}key='{idd}')"

		values = f"[i/10000000 for i in range(int({min_} * 10000000), int({max_} * 10000000), int({step} * 10000000))]"
		return f"sg.Spin({values}, initial_value={curr}, {size}key='{idd}')"

	elif type(normal_item) is QSlider:
		mina, maxa, curr = normal_item.minimum(), normal_item.maximum(), normal_item.value()
		orientation = 'h' if normal_item.orientation() == Qt.Horizontal else 'v'
		range_ = f'range=({mina}, {maxa}),'
		curr = f'default_value={curr},'
		orientation = f"orientation='{orientation}',"
		return f"sg.Slider({range_} {orientation} {curr} {size}key='{idd}')"

	# bool
	elif type(normal_item) is QCheckBox:
		isChecked = str(normal_item.isChecked())
		text = normal_item.text()
		return f"sg.Checkbox('{text}', default={isChecked}, {size}key='{idd}')"

	# text
	elif type(normal_item) is QLineEdit:
		text = normal_item.text()
		return f"sg.I('{text}', {size}key='{idd}')"

	elif type(normal_item) is QTextEdit:
		text = normal_item.text()
		return f"sg.Multiline('{text}', {size}key='{idd}')"

	elif type(normal_item) is QPlainTextEdit:
		text = normal_item.toPlainText()
		return f"sg.Multiline('{text}', {size}key='{idd}')"

	# button
	elif type(normal_item) is QPushButton:
		text = normal_item.text()
		return f"sg.RButton('{text}', {size}key='{idd}')"

	elif type(normal_item) is QRadioButton:
		text, group_id = normal_item.text(), normal_item.toolTip()
		if not group_id:
			raise Exception(f"Set radio_group for {idd} as a toolTip text")
		return f"sg.Radio('{text}', '{group_id}', key='{idd}')"

	else:
		if pass_bad_widgets:
			return empty_widget(GUItype='tk')
		else:
			raise Exception(f"HOWTO compile {type(normal_item)}?")

def _tab_it(make_tabs, psg_rows, is_top):

	# ▲     Add tabulation. I use '\t', not '    '
	my_tab = '\t'
	final = my_tab + f',\n{my_tab}'.join(psg_rows)
	# tabs
	space = ''
	if make_tabs != -1 and make_tabs > 0:
		space = my_tab * make_tabs
		final = '\n'.join([f'{space}{i}' for i in final.split('\n')])

	if is_top:
		# tabs
		if make_tabs != -1 and make_tabs > 0:
			return f'[\n{final}{space}\n]'
		else:
			return f'[\n{final}\n]'
	else:
		if make_tabs != -1 and make_tabs > 0:
			return final
		else:
			return space + final
# ▲
def compile_VBbox(parent_node: QVBoxLayout, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

	hbox_items = get_chidrens(parent_node)

	psg_rows = []
	for index, hbox_item in enumerate(hbox_items):

		res = type(hbox_item)

		if isNormalWidget(hbox_item) or type(hbox_item) is QGridLayout:

			el = '[' + to_psg_element(hbox_item, GUItype=GUItype,
									  pass_bad_widgets=pass_bad_widgets) + ']'
			psg_rows.append(el)

		elif type(hbox_item) is QHBoxLayout:

			elements = get_chidrens(hbox_item)
			psg_elemets = [to_psg_element(
				qt_widget, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets) for qt_widget in elements]
			el = '[' + ', '.join(psg_elemets) + ']'
			psg_rows.append(el)

		else:
			raise Exception(f'What is {type(hbox_item)}?')
	
	return _tab_it(make_tabs, psg_rows, is_top)
# ▲
def compile_GridLayout(parent_node: QGridLayout, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

	psg_elemets, psg_rows = [], []
	# ▲     Iterate thought grid
	for i in range(parent_node.rowCount()):
		psg_elemets = []
		for j in range(parent_node.columnCount()):
			# get widget
			res = parent_node.itemAtPosition(i, j)
			res = res.widget() if type(res) is QWidgetItem else res

			# this if means, that:
			# if current element is thesame as previuos element,
			# than current element has grid_span > 1,
			# and we don't need to parse,
			# because we already did it in previous step (loop step)
			if j > 0 and res == psg_elemets[-1][0]:
				continue

			if res is not None:
				# how can I use here this: size=(widthedst_elements[j],1)
				psg_elemets.append((res, to_psg_element(
					res, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)))
			else:
				# add dummy "empty lable"
				psg_elemets.append((res, empty_widget(GUItype=GUItype)))

		el = '[' + ', '.join([i[1] for i in psg_elemets]) + ']'
		psg_rows.append(el)

	return _tab_it(make_tabs, psg_rows, is_top)






'''

def parseQMenu_str(qmenu, lvl=0):
	# QMenu
	# 	actions
	# 	submenus
	str_format = ''
	try:
		actions 	= qmenu.actions()
		for a in actions:
			# вывести текст
			if a.isSeparator():
				str_format += '\t'*lvl + '-'*10 + '\n'
			else:
				str_format += '\t'*lvl + a.iconText() + '\n'

			# вывести вложенные менюшки
			try:
				menus = a.menu()
				
				# str_format += '\t'*lvl + '{'
				str_format += parseQMenu_str(menus, lvl+1)
				# str_format += '\t'*lvl + '}'
			except Exception as e:
				pass
		return str_format
	except Exception as e: # листок
		# str_format += 'листок\n'
		str_format += ''
	return str_format

'''

'''
	??? GET WIDTHEDST ELEMENTS in GRID ???

def _get_widthedst_elements(myQGridLayout):

	# iterate thought grid
	cols = []
	for i in range(myQGridLayout.columnCount()):
		items = []
		for j in range(myQGridLayout.rowCount()):

			# get widget
			el = myQGridLayout.itemAtPosition(j, i)
			el = el.widget() if type(el) is QWidgetItem else el

			if el is not None:
				items.append([el, j])

		cols.append(items)
	# get list of widthest cols (list of integers)
	return [max([item.geometry().width()
				 for item in row_data[0]])
			for i, row_data in enumerate(cols)]

# widthedst_elements = _get_widthedst_elements(parent_node)
'''