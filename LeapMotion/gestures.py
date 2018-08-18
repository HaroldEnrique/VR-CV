import Leap, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from client import data_to_send


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if not frame.hands.is_empty:

            # Gestures
            for gesture in frame.gestures():
                
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    #swipe = SwipeGesture(gesture)
                    print('Swiping!')
                    data_to_send('1')
                    time.sleep(2)
                    

                elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                    circle = CircleGesture(gesture)
                    print('circle!')
                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"

                    # Calculate the angle swept since the last frame
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                    
                    data_to_send('2')
                    time.sleep(2)


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
