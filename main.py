import os, inspect, sys, thread, time, math

src_dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
script_dir = "../LeapSDK/lib/"
arch_dir = 'x64' if sys.maxsize > 2**32 else 'x86'
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir ) ) )
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir, arch_dir ) ) )

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener( Leap.Listener ):
	finger_names = [ 'thumb', 'index', 'middle', 'ring', 'pinky' ]
	bone_names = [ 'MetaCarpal', 'Proximal', 'Intermediate', 'Distal' ]
	state_names = [ 'STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END' ]
	
	def on_init( self, controller ):
		print "Initialized"
	
	def on_connect( self, controller ):
		print "Connected"
		controller.enable_gesture( Leap.Gesture.TYPE_CIRCLE );
		controller.enable_gesture( Leap.Gesture.TYPE_KEY_TAP );
		controller.enable_gesture( Leap.Gesture.TYPE_SCREEN_TAP );
		controller.enable_gesture( Leap.Gesture.TYPE_SWIPE );
		controller.set_policy( Leap.Controller.POLICY_BACKGROUND_FRAMES );
		controller.set_policy( Leap.Controller.POLICY_IMAGES );
		controller.set_policy( Leap.Controller.POLICY_OPTIMIZE_HMD );
		
	def has_focus( self, controller ):	
		print "Focused"
		
	def on_disconnect( self, controller ):
		print "Disconnected"
		
	def on_exit( self, controller ):
		print "Exited"
		
	def on_frame( self, controller ):
		frame = controller.frame()
		
		#print "37:",  str( frame.id ), str( frame.timestamp ), str( len( frame.hands ) ), str( len( frame.fingers ) ), str( len( frame.tools ) ), str( len( frame.gestures() ) )
		
		for hand in frame.hands:
			handType = "Left Hand" if hand.is_left else "Right Hand"
			#print handType, str( hand.id ), str(  hand.palm_position )
			normal = hand.palm_normal
			direction = hand.direction
			#print "44:", str( direction.pitch * Leap.RAD_TO_DEG ), str( normal.roll * Leap.RAD_TO_DEG ), str( direction.yaw * Leap.RAD_TO_DEG )
			
			arm = hand.arm
			#print "47:", str( arm.direction ), str( arm.wrist_position ), str( arm.elbow_position )
			
			for finger in hand.fingers:
				#print "50:", self.finger_names[ finger.type() ], str( finger.id ), str( finger.length ), str( finger.width )
				
				for b in range( 0, 4 ):
					bone = finger.bone( b )
					#print "54:", self.bone_names[ bone.type ], str( bone.prev_joint ), str( bone.next_joint ), str( bone.direction )
				
		for tool in frame.tools:
			#print "57:", str( tool.id ), str(  tool.tip_position ), str( tool.direction )
			pass
			
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture( gesture )
				
				if circle.pointable.direction.angle_to( circle.normal ) <= Leap.PI / 2:
					clockwiseness = "clockwise"
				else:
					clockwiseness = "counter-clockwise"
					
				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous = CircleGesture( controller.frame( 1 ).gesture( circle.id ) )
					swept_angle = ( circle.progress - previous.progress ) * 2 * Leap.PI
					print "73: circle", str( circle.id ), str( circle.progress ), str( circle.radius ), str( swept_angle * Leap.RAD_TO_DEG ), clockwiseness
					
			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture( gesture )
				swipe_direction  = swipe.direction
				
				if ( swipe_direction.x > 0 ) and ( math.fabs( swipe_direction.x ) > math.fabs( swipe_direction.y ) ):
					print "Swiped Right"
				elif ( swipe_direction.x < 0 ) and ( math.fabs( swipe_direction.x ) > math.fabs( swipe_direction.y ) ):
					print "Swiped Left"
				elif ( swipe_direction.y > 0 ) and ( math.fabs( swipe_direction.x ) < math.fabs( swipe_direction.y ) ):
					print "Swiped Up"
				elif ( swipe_direction.y < 0 ) and ( math.fabs( swipe_direction.x ) < math.fabs( swipe_direction.y ) ):
					print "Swiped Down"
					
				print "88: swipe", str( swipe.id ), self.state_names[ gesture.state ], str( swipe.position ), str( swipe.direction ), str( swipe.speed )
				
			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture( gesture )
				print "92: screen tap", str( gesture.id ), self.state_names[ gesture.state ], str( screentap.position ), str( screentap.direction )
				
			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture( gesture )
				print "96: key tap", str( gesture.id ), self.state_names[ gesture.state ], str( keytap.position ), str( keytap.direction )
		
def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()
	controller.add_listener( listener )
	print "Press Enter to Quit..."
	
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener( listener )
		
if __name__ == "__main__":
	main()
		
