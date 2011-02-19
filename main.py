#
#  main.py
#  RegexAsYouType
#
#  Created by Anders Hovmoller on 5/19/09.
#  Copyright Calidris 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import RegexAsYouTypeAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
