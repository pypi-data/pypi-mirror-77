CMAKE_MINIMUM_REQUIRED(VERSION 2.6.0)
PROJECT(polyclipping)

SET(CMAKE_BUILD_TYPE "Release" CACHE STRING "Release type")

include(GNUInstallDirs)

SET(PYCLIPPER_BOOST_PYTHON_SRC
        clipper/clipper.cpp
        clipper_py/clipper.cpp
        clipper_py/path.cpp
        clipper_py/int-point.cpp
        clipper_py/clipper-py.cpp)

FIND_PACKAGE(Boost REQUIRED)
FIND_PACKAGE(Boost QUIET COMPONENTS python python38)

set(Python_ADDITIONAL_VERSIONS 3.8)

FIND_PACKAGE(PythonLibs 3.8 REQUIRED)
SET(PYDEXTENSION FALSE)

INCLUDE_DIRECTORIES(./clipper ./clipper_py ${PYTHON_INCLUDE_PATH} ${BOOST_INCLUDE_DIR} )
ADD_LIBRARY(clipper_py SHARED ${PYCLIPPER_BOOST_PYTHON_SRC})
SET_TARGET_PROPERTIES(clipper_py PROPERTIES PREFIX "_")
TARGET_LINK_LIBRARIES(clipper_py ${Boost_PYTHON38_LIBRARY} ${PYTHON_LIBRARIES})