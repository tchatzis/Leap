import os, sys, inspect

src_dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
script_dir = "../LeapSDK/lib/"
arch_dir = 'x64' if sys.maxsize > 2**32 else 'x86'
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir ) ) )
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir, arch_dir ) ) )

import Leap

GRAB_SENSITIVITY = 0.7

class LeapEventListener( Leap.Listener ):
    def on_connect(self, controller):
        print "Connected"
        
    def on_disconnect( self, controller ):
        print "Disconnected"

    def on_exit( self, controller ):
        print "Exited"

    def on_frame( self, controller ):
        frame = controller.frame()
        hands = frame.hands
        hand = frame.hands.rightmost
        position = hand.palm_position
        velocity = hand.palm_velocity
        direction = hand.direction

        if hand.grab_strength > GRAB_SENSITIVITY:
            print hand.grab_strength

listener = LeapEventListener()
controller = Leap.Controller()
controller.add_listener( listener )
