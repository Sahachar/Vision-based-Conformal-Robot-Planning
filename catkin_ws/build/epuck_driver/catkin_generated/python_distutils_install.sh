#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/sah/osbert/catkin_ws/src/epuck_driver"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/sah/osbert/catkin_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/sah/osbert/catkin_ws/install/lib/python3/dist-packages:/home/sah/osbert/catkin_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/sah/osbert/catkin_ws/build" \
    "/usr/bin/python3" \
    "/home/sah/osbert/catkin_ws/src/epuck_driver/setup.py" \
     \
    build --build-base "/home/sah/osbert/catkin_ws/build/epuck_driver" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/sah/osbert/catkin_ws/install" --install-scripts="/home/sah/osbert/catkin_ws/install/bin"
