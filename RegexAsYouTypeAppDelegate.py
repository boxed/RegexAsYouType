#
#  RegexAsYouTypeAppDelegate.py
#  RegexAsYouType
#
#  Created by Anders Hovmoller on 5/19/09.
#  Copyright Calidris 2009. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import *
import re

class RegexAsYouTypeAppDelegate(NSObject):
	window = IBOutlet()
	data = IBOutlet()
	expression = IBOutlet()
	result = IBOutlet()
	table = IBOutlet()
	error = IBOutlet()
	matchType = IBOutlet()
	
	def applicationDidFinishLaunching_(self, sender):
		NSLog("Application did finish launching.")
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, self.textDidChange_, NSControlTextDidChangeNotification, self.expression)
		self.preview = []
		self.table.setDataSource_(self)
		self.textDidChange_(None)

	def textDidChange_(self, notification):
		data = self.data.textStorage().string()
		self.preview = []
		columns = set()
		self.error.setStringValue_('')
		if self.matchType.state() == 1:
			data = data.split('\n')
			for line in data:
				try:
					m = re.match(self.expression.stringValue(), line)
					if m:
						if len(m.groupdict()) > 0:
							self.preview.append(m.groupdict())
							columns |= set(m.groupdict().keys())
						else:
							row = {}
							for i, x in enumerate(m.groups()):
								row[unicode(i)] = x
							self.preview.append(row)
							columns |= set([unicode(x) for x in range(len(m.groups()))])
				except Exception,e:
					self.error.setStringValue_('Error: '+unicode(e))
		else:
			try:
				m = re.findall(self.expression.stringValue(), data)
				if m:
					row = {}
					for i, x in enumerate(m):
						row[unicode(i)] = unicode(x)
					self.preview.append(row)
					columns |= set([unicode(x) for x in range(len(m))])
			except Exception,e:
				self.error.setStringValue_('Error: '+unicode(e))
			
		#print 'data:', columns, self.preview
		# update columns
		while self.table.tableColumns().count() != 0:
			self.table.removeTableColumn_(self.table.tableColumns()[0])
		for column in sorted(columns):
			c = NSTableColumn.alloc().initWithIdentifier_(column)
			c.headerCell().setStringValue_(column)
			self.table.addTableColumn_(c)
		self.table.reloadData()
	
	# table data source implementation
	def numberOfRowsInTableView_(self, table):
		return len(self.preview)
		
	def tableView_objectValueForTableColumn_row_(self, table, column, row):
		try:
			return self.preview[row][column.headerCell().stringValue()]
		except Exception,e:
			print e
			return ''
	#tableView:setObjectValue:forTableColumn:row
	#tableView:sortDescriptorsDidChange