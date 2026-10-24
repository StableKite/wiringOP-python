cmake_minimum_required(VERSION 3.18)
project(wiringop_nanobind LANGUAGES C CXX)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Local release policy: maximum safe optimization by default.
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options("$<$<CONFIG:Release>:-O3>" "$<$<CONFIG:Release>:-DNDEBUG>")
endif()
option(WIRINGOP_ENABLE_IPO "Enable interprocedural/LTO optimization in Release" ON)
if(WIRINGOP_ENABLE_IPO)
  include(CheckIPOSupported)
  check_ipo_supported(RESULT WIRINGOP_IPO_SUPPORTED OUTPUT WIRINGOP_IPO_ERROR LANGUAGES C CXX)
  if(NOT WIRINGOP_IPO_SUPPORTED)
    message(FATAL_ERROR "Release LTO/IPO is required but unsupported: ${WIRINGOP_IPO_ERROR}")
  endif()
  set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
endif()

# CPU-specific tuning is deliberately enabled only for a native Orange Pi 5 build.
set(WIRINGOP_ORANGEPI5_NATIVE OFF)
set(WIRINGOP_BOARD_MODEL "")
if(CMAKE_SYSTEM_NAME STREQUAL "Linux" AND NOT CMAKE_CROSSCOMPILING
   AND CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|arm64)$"
   AND EXISTS "/proc/device-tree/model")
  file(STRINGS "/proc/device-tree/model" WIRINGOP_BOARD_MODEL LIMIT_COUNT 1)
  if(WIRINGOP_BOARD_MODEL MATCHES "Orange Pi 5")
    set(WIRINGOP_ORANGEPI5_NATIVE ON)
  endif()
endif()
if(WIRINGOP_ORANGEPI5_NATIVE)
  if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options("$<$<CONFIG:Release>:-mcpu=native>")
  endif()
  message(STATUS "Orange Pi 5 native build: enabling -mcpu=native")
else()
  message(STATUS "Generic Release build: -O3 + LTO/IPO without CPU-specific tuning")
endif()

find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(Threads REQUIRED)
set(NB_ROOT "" CACHE PATH "Path to exact nanobind 2.14.0 package/source tree")
if(NOT NB_ROOT)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c "import pathlib, nanobind; print(pathlib.Path(nanobind.__file__).resolve().parent)"
    RESULT_VARIABLE NB_DISCOVERY_STATUS
    OUTPUT_VARIABLE NB_DISCOVERED_ROOT
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_VARIABLE NB_DISCOVERY_ERROR
  )
  if(NOT NB_DISCOVERY_STATUS EQUAL 0 OR NOT NB_DISCOVERED_ROOT)
    message(FATAL_ERROR "Unable to discover nanobind 2.14.0 from Python: ${NB_DISCOVERY_ERROR}")
  endif()
  set(NB_ROOT "${NB_DISCOVERED_ROOT}" CACHE PATH "Path to exact nanobind 2.14.0 package/source tree" FORCE)
endif()
file(READ "${NB_ROOT}/include/nanobind/nanobind.h" NB_HEADER)
if(NOT NB_HEADER MATCHES "NB_VERSION_MAJOR 2" OR NOT NB_HEADER MATCHES "NB_VERSION_MINOR 14" OR NOT NB_HEADER MATCHES "NB_VERSION_PATCH 0" OR NOT NB_HEADER MATCHES "NB_VERSION_DEV +0")
  message(FATAL_ERROR "nanobind source must be exactly version 2.14.0")
endif()
option(WIRINGOP_USE_MOCK "Build against hardware-free mock ABI" OFF)
set(WIRINGOP_SOURCE "" CACHE PATH "Prepared wiringOP source; auto-prepared from the pinned submodule when empty")
if(NOT WIRINGOP_SOURCE)
  set(WIRINGOP_SOURCE "${CMAKE_BINARY_DIR}/upstream/wiringOP")
  execute_process(
    COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_wiringop.py"
            --project-root "${CMAKE_CURRENT_SOURCE_DIR}" --output "${WIRINGOP_SOURCE}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    RESULT_VARIABLE WIRINGOP_PREPARE_STATUS
    OUTPUT_VARIABLE WIRINGOP_PREPARE_OUTPUT
    ERROR_VARIABLE WIRINGOP_PREPARE_ERROR
  )
  if(NOT WIRINGOP_PREPARE_STATUS EQUAL 0)
    message(FATAL_ERROR "Failed to prepare pinned wiringOP source: ${WIRINGOP_PREPARE_ERROR}")
  endif()
endif()
# Use the upstream nanobind build integration: it selects the correct ABI,
# backend library, and Py_mod_gil metadata for the chosen CPython.
# Defining NB_FREE_THREADED only in user wrappers is not sufficient.
find_package(nanobind 2.14.0 EXACT CONFIG REQUIRED
  PATHS "${NB_ROOT}/cmake" NO_DEFAULT_PATH)
# Nanobind's own NB_STATIC runtime is module-local. The production wiringOP C
# backend is different: it owns process-global physical device state and must
# be linked exactly once as a shared library across all extension modules.
# Hardware-free mock bindings retain their independent static shim.
set(WIRINGOP_NATIVE_SYSTEM_LIBS Threads::Threads ${CMAKE_DL_LIBS})
if(UNIX)
  list(APPEND WIRINGOP_NATIVE_SYSTEM_LIBS m)
endif()
if(WIRINGOP_USE_MOCK)
 add_library(wiringop_backend STATIC
  support/mock_backend/devLib/ds1302.c
  support/mock_backend/devLib/font.c
  support/mock_backend/devLib/gertboard.c
  support/mock_backend/devLib/lcd.c
  support/mock_backend/devLib/lcd128x64.c
  support/mock_backend/devLib/maxdetect.c
  support/mock_backend/devLib/piFace.c
  support/mock_backend/devLib/piGlow.c
  support/mock_backend/devLib/piNes.c
  support/mock_backend/devLib/scrollPhat.c
  support/mock_backend/devLib/scrollPhatFont.c
  support/mock_backend/version.c
  support/mock_backend/wiringPi/ads1115.c
  support/mock_backend/wiringPi/bmp180.c
  support/mock_backend/wiringPi/drcNet.c
  support/mock_backend/wiringPi/drcSerial.c
  support/mock_backend/wiringPi/ds18b20.c
  support/mock_backend/wiringPi/font.c
  support/mock_backend/wiringPi/htu21d.c
  support/mock_backend/wiringPi/max31855.c
  support/mock_backend/wiringPi/max5322.c
  support/mock_backend/wiringPi/mcp23008.c
  support/mock_backend/wiringPi/mcp23016.c
  support/mock_backend/wiringPi/mcp23016reg.c
  support/mock_backend/wiringPi/mcp23017.c
  support/mock_backend/wiringPi/mcp23s08.c
  support/mock_backend/wiringPi/mcp23s17.c
  support/mock_backend/wiringPi/mcp23x08.c
  support/mock_backend/wiringPi/mcp23x0817.c
  support/mock_backend/wiringPi/mcp3002.c
  support/mock_backend/wiringPi/mcp3004.c
  support/mock_backend/wiringPi/mcp3422.c
  support/mock_backend/wiringPi/mcp4802.c
  support/mock_backend/wiringPi/oled.c
  support/mock_backend/wiringPi/pcf8574.c
  support/mock_backend/wiringPi/pcf8591.c
  support/mock_backend/wiringPi/pseudoPins.c
  support/mock_backend/wiringPi/rht03.c
  support/mock_backend/wiringPi/sn3218.c
  support/mock_backend/wiringPi/softPwm.c
  support/mock_backend/wiringPi/softServo.c
  support/mock_backend/wiringPi/softTone.c
  support/mock_backend/wiringPi/sr595.c
  support/mock_backend/wiringPi/w25q64.c
  support/mock_backend/wiringPi/wiringPi.c
  support/mock_backend/wiringPi/wiringPiI2C.c
  support/mock_backend/wiringPi/wiringPiSPI.c
  support/mock_backend/wiringPi/wiringSerial.c
  support/mock_backend/wiringPi/wiringShift.c
  support/mock_backend/wiringPi/wpiExtensions.c
  support/mock_backend/wiringPiD/daemonise.c
  support/mock_backend/wiringPiD/drcNetCmd.c
  support/mock_backend/wiringPiD/network.c
  support/mock_backend/wiringPiD/runRemote.c
 )
else()
 add_library(wiringop_backend SHARED
  ${WIRINGOP_SOURCE}/wiringPi/ads1115.c
  ${WIRINGOP_SOURCE}/wiringPi/bmp180.c
  ${WIRINGOP_SOURCE}/wiringPi/drcNet.c
  ${WIRINGOP_SOURCE}/wiringPi/drcSerial.c
  ${WIRINGOP_SOURCE}/wiringPi/ds18b20.c
  ${WIRINGOP_SOURCE}/wiringPi/htu21d.c
  ${WIRINGOP_SOURCE}/wiringPi/max31855.c
  ${WIRINGOP_SOURCE}/wiringPi/max5322.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp23008.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp23016.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp23017.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp23s08.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp23s17.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp3002.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp3004.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp3422.c
  ${WIRINGOP_SOURCE}/wiringPi/mcp4802.c
  ${WIRINGOP_SOURCE}/wiringPi/oled.c
  ${WIRINGOP_SOURCE}/wiringPi/pcf8574.c
  ${WIRINGOP_SOURCE}/wiringPi/pcf8591.c
  ${WIRINGOP_SOURCE}/wiringPi/piHiPri.c
  ${WIRINGOP_SOURCE}/wiringPi/piThread.c
  ${WIRINGOP_SOURCE}/wiringPi/pseudoPins.c
  ${WIRINGOP_SOURCE}/wiringPi/rht03.c
  ${WIRINGOP_SOURCE}/wiringPi/sn3218.c
  ${WIRINGOP_SOURCE}/wiringPi/softPwm.c
  ${WIRINGOP_SOURCE}/wiringPi/softServo.c
  ${WIRINGOP_SOURCE}/wiringPi/softTone.c
  ${WIRINGOP_SOURCE}/wiringPi/sr595.c
  ${WIRINGOP_SOURCE}/wiringPi/w25q64.c
  ${WIRINGOP_SOURCE}/wiringPi/wiringPi.c
  ${WIRINGOP_SOURCE}/wiringPi/wiringPiI2C.c
  ${WIRINGOP_SOURCE}/wiringPi/wiringPiSPI.c
  ${WIRINGOP_SOURCE}/wiringPi/wiringSerial.c
  ${WIRINGOP_SOURCE}/wiringPi/wiringShift.c
  ${WIRINGOP_SOURCE}/wiringPi/wpiExtensions.c
  ${WIRINGOP_SOURCE}/devLib/ds1302.c
  ${WIRINGOP_SOURCE}/devLib/gertboard.c
  ${WIRINGOP_SOURCE}/devLib/lcd.c
  ${WIRINGOP_SOURCE}/devLib/lcd128x64.c
  ${WIRINGOP_SOURCE}/devLib/maxdetect.c
  ${WIRINGOP_SOURCE}/devLib/piFace.c
  ${WIRINGOP_SOURCE}/devLib/piGlow.c
  ${WIRINGOP_SOURCE}/devLib/piNes.c
  ${WIRINGOP_SOURCE}/devLib/scrollPhat.c
  ${WIRINGOP_SOURCE}/wiringPiD/daemonise.c
  ${WIRINGOP_SOURCE}/wiringPiD/network.c
  ${WIRINGOP_SOURCE}/wiringPiD/runRemote.c
 )
endif()
# Do not mispackage the Linux-specific physical GPIO backend as a native
# Windows hardware implementation. Windows CI validates genuine native C ABI
# mock shims only, and may not publish them as physical-hardware wheels.
if(WIN32 AND NOT WIRINGOP_USE_MOCK)
  message(FATAL_ERROR "Windows physical wiringOP backend is unsupported; do not ship a mock as production")
endif()
function(wiringop_native_windows_abi target_name)
  if(MSVC)
    target_include_directories(${target_name} BEFORE PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/support/windows_native/include")
    target_compile_options(${target_name} PRIVATE "/FI${CMAKE_CURRENT_SOURCE_DIR}/support/windows_native/include/msvc_compat.h")
  endif()
endfunction()
target_include_directories(wiringop_backend PUBLIC "${WIRINGOP_SOURCE}" "${WIRINGOP_SOURCE}/wiringPi" "${WIRINGOP_SOURCE}/devLib" "${WIRINGOP_SOURCE}/wiringPiD")
wiringop_native_windows_abi(wiringop_backend)
target_compile_definitions(wiringop_backend PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
find_library(CRYPT_LIBRARY NAMES crypt)
if(CRYPT_LIBRARY)
  target_link_libraries(wiringop_backend PUBLIC ${CRYPT_LIBRARY})
elseif(NOT WIRINGOP_USE_MOCK)
  message(FATAL_ERROR "libcrypt is required by wiringOP network/drcNet code")
endif()
if(NOT WIRINGOP_USE_MOCK)
  if(NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message(FATAL_ERROR "Physical wiringOP backend requires Linux; cannot publish a mock as production")
  endif()
  # Keep one process-wide GPIO/UART state object in the installed wheel.
  # The backend resides in wiringop/, extensions in wiringop/ or its child
  # packages; do not rely on absolute build paths or system installations.
  install(TARGETS wiringop_backend LIBRARY DESTINATION wiringop)
  set_target_properties(wiringop_backend PROPERTIES INSTALL_RPATH "$ORIGIN")
  set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/..")
  set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
endif()
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/python/wiringop" DESTINATION "${CMAKE_BINARY_DIR}/python" PATTERN "__pycache__" EXCLUDE PATTERN "*.pyc" EXCLUDE)
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/python/wiringop/" DESTINATION wiringop FILES_MATCHING PATTERN "*.py" PATTERN "py.typed" PATTERN "__pycache__" EXCLUDE PATTERN "*.pyc" EXCLUDE)
nanobind_add_module(nb_devLib_ds1302 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/ds1302.cpp)
target_include_directories(nb_devLib_ds1302 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_ds1302 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_ds1302 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_ds1302)
set_target_properties(nb_devLib_ds1302 PROPERTIES PREFIX "" OUTPUT_NAME "ds1302" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_ds1302 LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/ds1302.pyi" DESTINATION "wiringop/dev_lib" RENAME "ds1302.pyi")
nanobind_add_module(nb_devLib_font NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/font.cpp)
target_include_directories(nb_devLib_font PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_font PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_font PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_font)
set_target_properties(nb_devLib_font PROPERTIES PREFIX "" OUTPUT_NAME "font" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_font LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/font.pyi" DESTINATION "wiringop/dev_lib" RENAME "font.pyi")
nanobind_add_module(nb_devLib_gertboard NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/gertboard.cpp)
target_include_directories(nb_devLib_gertboard PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_gertboard PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_gertboard PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_gertboard)
set_target_properties(nb_devLib_gertboard PROPERTIES PREFIX "" OUTPUT_NAME "gertboard" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_gertboard LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/gertboard.pyi" DESTINATION "wiringop/dev_lib" RENAME "gertboard.pyi")
nanobind_add_module(nb_devLib_lcd NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/lcd.cpp)
target_include_directories(nb_devLib_lcd PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_lcd PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_lcd PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_lcd)
set_target_properties(nb_devLib_lcd PROPERTIES PREFIX "" OUTPUT_NAME "lcd" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_lcd LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/lcd.pyi" DESTINATION "wiringop/dev_lib" RENAME "lcd.pyi")
nanobind_add_module(nb_devLib_lcd128x64 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/lcd128x64.cpp)
target_include_directories(nb_devLib_lcd128x64 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_lcd128x64 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_lcd128x64 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_lcd128x64)
set_target_properties(nb_devLib_lcd128x64 PROPERTIES PREFIX "" OUTPUT_NAME "lcd128x64" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_lcd128x64 LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/lcd128x64.pyi" DESTINATION "wiringop/dev_lib" RENAME "lcd128x64.pyi")
nanobind_add_module(nb_devLib_maxdetect NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/maxdetect.cpp)
target_include_directories(nb_devLib_maxdetect PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_maxdetect PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_maxdetect PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_maxdetect)
set_target_properties(nb_devLib_maxdetect PROPERTIES PREFIX "" OUTPUT_NAME "maxdetect" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_maxdetect LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/maxdetect.pyi" DESTINATION "wiringop/dev_lib" RENAME "maxdetect.pyi")
nanobind_add_module(nb_devLib_piFace NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/piFace.cpp)
target_include_directories(nb_devLib_piFace PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_piFace PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_piFace PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_piFace)
set_target_properties(nb_devLib_piFace PROPERTIES PREFIX "" OUTPUT_NAME "pi_face" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_piFace LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/piFace.pyi" DESTINATION "wiringop/dev_lib" RENAME "pi_face.pyi")
nanobind_add_module(nb_devLib_piGlow NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/piGlow.cpp)
target_include_directories(nb_devLib_piGlow PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_piGlow PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_piGlow PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_piGlow)
set_target_properties(nb_devLib_piGlow PROPERTIES PREFIX "" OUTPUT_NAME "pi_glow" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_piGlow LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/piGlow.pyi" DESTINATION "wiringop/dev_lib" RENAME "pi_glow.pyi")
nanobind_add_module(nb_devLib_piNes NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/piNes.cpp)
target_include_directories(nb_devLib_piNes PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_piNes PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_piNes PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_piNes)
set_target_properties(nb_devLib_piNes PROPERTIES PREFIX "" OUTPUT_NAME "pi_nes" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_piNes LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/piNes.pyi" DESTINATION "wiringop/dev_lib" RENAME "pi_nes.pyi")
nanobind_add_module(nb_devLib_scrollPhat NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/scrollPhat.cpp)
target_include_directories(nb_devLib_scrollPhat PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_scrollPhat PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_scrollPhat PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_scrollPhat)
set_target_properties(nb_devLib_scrollPhat PROPERTIES PREFIX "" OUTPUT_NAME "scroll_phat" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_scrollPhat LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/scrollPhat.pyi" DESTINATION "wiringop/dev_lib" RENAME "scroll_phat.pyi")
nanobind_add_module(nb_devLib_scrollPhatFont NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/devLib/scrollPhatFont.cpp)
target_include_directories(nb_devLib_scrollPhatFont PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_devLib_scrollPhatFont PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_devLib_scrollPhatFont PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_devLib_scrollPhatFont)
set_target_properties(nb_devLib_scrollPhatFont PROPERTIES PREFIX "" OUTPUT_NAME "scroll_phat_font" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/dev_lib")
install(TARGETS nb_devLib_scrollPhatFont LIBRARY DESTINATION "wiringop/dev_lib" RUNTIME DESTINATION "wiringop/dev_lib")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/devLib/scrollPhatFont.pyi" DESTINATION "wiringop/dev_lib" RENAME "scroll_phat_font.pyi")
nanobind_add_module(nb_version NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/version.cpp)
target_include_directories(nb_version PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_version PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_version PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_version)
set_target_properties(nb_version PROPERTIES PREFIX "" OUTPUT_NAME "version" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop")
install(TARGETS nb_version LIBRARY DESTINATION "wiringop" RUNTIME DESTINATION "wiringop")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/version.pyi" DESTINATION "wiringop" RENAME "version.pyi")
nanobind_add_module(nb_wiringPi_ads1115 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/ads1115.cpp)
target_include_directories(nb_wiringPi_ads1115 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_ads1115 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_ads1115 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_ads1115)
set_target_properties(nb_wiringPi_ads1115 PROPERTIES PREFIX "" OUTPUT_NAME "ads1115" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_ads1115 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/ads1115.pyi" DESTINATION "wiringop/wiring_pi" RENAME "ads1115.pyi")
nanobind_add_module(nb_wiringPi_bmp180 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/bmp180.cpp)
target_include_directories(nb_wiringPi_bmp180 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_bmp180 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_bmp180 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_bmp180)
set_target_properties(nb_wiringPi_bmp180 PROPERTIES PREFIX "" OUTPUT_NAME "bmp180" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_bmp180 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/bmp180.pyi" DESTINATION "wiringop/wiring_pi" RENAME "bmp180.pyi")
nanobind_add_module(nb_wiringPi_drcNet NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/drcNet.cpp)
target_include_directories(nb_wiringPi_drcNet PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_drcNet PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_drcNet PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_drcNet)
set_target_properties(nb_wiringPi_drcNet PROPERTIES PREFIX "" OUTPUT_NAME "drc_net" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_drcNet LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/drcNet.pyi" DESTINATION "wiringop/wiring_pi" RENAME "drc_net.pyi")
nanobind_add_module(nb_wiringPi_drcSerial NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/drcSerial.cpp)
target_include_directories(nb_wiringPi_drcSerial PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_drcSerial PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_drcSerial PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_drcSerial)
set_target_properties(nb_wiringPi_drcSerial PROPERTIES PREFIX "" OUTPUT_NAME "drc_serial" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_drcSerial LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/drcSerial.pyi" DESTINATION "wiringop/wiring_pi" RENAME "drc_serial.pyi")
nanobind_add_module(nb_wiringPi_ds18b20 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/ds18b20.cpp)
target_include_directories(nb_wiringPi_ds18b20 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_ds18b20 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_ds18b20 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_ds18b20)
set_target_properties(nb_wiringPi_ds18b20 PROPERTIES PREFIX "" OUTPUT_NAME "ds18b20" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_ds18b20 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/ds18b20.pyi" DESTINATION "wiringop/wiring_pi" RENAME "ds18b20.pyi")
nanobind_add_module(nb_wiringPi_font NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/font.cpp)
target_include_directories(nb_wiringPi_font PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_font PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_font PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_font)
set_target_properties(nb_wiringPi_font PROPERTIES PREFIX "" OUTPUT_NAME "font" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_font LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/font.pyi" DESTINATION "wiringop/wiring_pi" RENAME "font.pyi")
nanobind_add_module(nb_wiringPi_htu21d NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/htu21d.cpp)
target_include_directories(nb_wiringPi_htu21d PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_htu21d PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_htu21d PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_htu21d)
set_target_properties(nb_wiringPi_htu21d PROPERTIES PREFIX "" OUTPUT_NAME "htu21d" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_htu21d LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/htu21d.pyi" DESTINATION "wiringop/wiring_pi" RENAME "htu21d.pyi")
nanobind_add_module(nb_wiringPi_max31855 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/max31855.cpp)
target_include_directories(nb_wiringPi_max31855 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_max31855 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_max31855 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_max31855)
set_target_properties(nb_wiringPi_max31855 PROPERTIES PREFIX "" OUTPUT_NAME "max31855" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_max31855 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/max31855.pyi" DESTINATION "wiringop/wiring_pi" RENAME "max31855.pyi")
nanobind_add_module(nb_wiringPi_max5322 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/max5322.cpp)
target_include_directories(nb_wiringPi_max5322 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_max5322 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_max5322 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_max5322)
set_target_properties(nb_wiringPi_max5322 PROPERTIES PREFIX "" OUTPUT_NAME "max5322" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_max5322 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/max5322.pyi" DESTINATION "wiringop/wiring_pi" RENAME "max5322.pyi")
nanobind_add_module(nb_wiringPi_mcp23008 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23008.cpp)
target_include_directories(nb_wiringPi_mcp23008 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23008 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23008 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23008)
set_target_properties(nb_wiringPi_mcp23008 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23008" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23008 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23008.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23008.pyi")
nanobind_add_module(nb_wiringPi_mcp23016 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23016.cpp)
target_include_directories(nb_wiringPi_mcp23016 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23016 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23016 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23016)
set_target_properties(nb_wiringPi_mcp23016 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23016" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23016 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23016.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23016.pyi")
nanobind_add_module(nb_wiringPi_mcp23016reg NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23016reg.cpp)
target_include_directories(nb_wiringPi_mcp23016reg PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23016reg PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23016reg PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23016reg)
set_target_properties(nb_wiringPi_mcp23016reg PROPERTIES PREFIX "" OUTPUT_NAME "mcp23016reg" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23016reg LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23016reg.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23016reg.pyi")
nanobind_add_module(nb_wiringPi_mcp23017 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23017.cpp)
target_include_directories(nb_wiringPi_mcp23017 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23017 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23017 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23017)
set_target_properties(nb_wiringPi_mcp23017 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23017" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23017 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23017.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23017.pyi")
nanobind_add_module(nb_wiringPi_mcp23s08 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23s08.cpp)
target_include_directories(nb_wiringPi_mcp23s08 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23s08 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23s08 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23s08)
set_target_properties(nb_wiringPi_mcp23s08 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23s08" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23s08 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23s08.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23s08.pyi")
nanobind_add_module(nb_wiringPi_mcp23s17 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23s17.cpp)
target_include_directories(nb_wiringPi_mcp23s17 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23s17 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23s17 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23s17)
set_target_properties(nb_wiringPi_mcp23s17 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23s17" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23s17 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23s17.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23s17.pyi")
nanobind_add_module(nb_wiringPi_mcp23x08 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23x08.cpp)
target_include_directories(nb_wiringPi_mcp23x08 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23x08 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23x08 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23x08)
set_target_properties(nb_wiringPi_mcp23x08 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23x08" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23x08 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23x08.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23x08.pyi")
nanobind_add_module(nb_wiringPi_mcp23x0817 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp23x0817.cpp)
target_include_directories(nb_wiringPi_mcp23x0817 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp23x0817 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp23x0817 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp23x0817)
set_target_properties(nb_wiringPi_mcp23x0817 PROPERTIES PREFIX "" OUTPUT_NAME "mcp23x0817" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp23x0817 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp23x0817.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp23x0817.pyi")
nanobind_add_module(nb_wiringPi_mcp3002 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp3002.cpp)
target_include_directories(nb_wiringPi_mcp3002 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp3002 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp3002 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp3002)
set_target_properties(nb_wiringPi_mcp3002 PROPERTIES PREFIX "" OUTPUT_NAME "mcp3002" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp3002 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp3002.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp3002.pyi")
nanobind_add_module(nb_wiringPi_mcp3004 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp3004.cpp)
target_include_directories(nb_wiringPi_mcp3004 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp3004 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp3004 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp3004)
set_target_properties(nb_wiringPi_mcp3004 PROPERTIES PREFIX "" OUTPUT_NAME "mcp3004" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp3004 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp3004.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp3004.pyi")
nanobind_add_module(nb_wiringPi_mcp3422 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp3422.cpp)
target_include_directories(nb_wiringPi_mcp3422 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp3422 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp3422 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp3422)
set_target_properties(nb_wiringPi_mcp3422 PROPERTIES PREFIX "" OUTPUT_NAME "mcp3422" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp3422 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp3422.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp3422.pyi")
nanobind_add_module(nb_wiringPi_mcp4802 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/mcp4802.cpp)
target_include_directories(nb_wiringPi_mcp4802 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_mcp4802 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_mcp4802 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_mcp4802)
set_target_properties(nb_wiringPi_mcp4802 PROPERTIES PREFIX "" OUTPUT_NAME "mcp4802" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_mcp4802 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/mcp4802.pyi" DESTINATION "wiringop/wiring_pi" RENAME "mcp4802.pyi")
nanobind_add_module(nb_wiringPi_oled NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/oled.cpp)
target_include_directories(nb_wiringPi_oled PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_oled PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_oled PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_oled)
set_target_properties(nb_wiringPi_oled PROPERTIES PREFIX "" OUTPUT_NAME "oled" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_oled LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/oled.pyi" DESTINATION "wiringop/wiring_pi" RENAME "oled.pyi")
nanobind_add_module(nb_wiringPi_pcf8574 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/pcf8574.cpp)
target_include_directories(nb_wiringPi_pcf8574 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_pcf8574 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_pcf8574 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_pcf8574)
set_target_properties(nb_wiringPi_pcf8574 PROPERTIES PREFIX "" OUTPUT_NAME "pcf8574" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_pcf8574 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/pcf8574.pyi" DESTINATION "wiringop/wiring_pi" RENAME "pcf8574.pyi")
nanobind_add_module(nb_wiringPi_pcf8591 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/pcf8591.cpp)
target_include_directories(nb_wiringPi_pcf8591 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_pcf8591 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_pcf8591 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_pcf8591)
set_target_properties(nb_wiringPi_pcf8591 PROPERTIES PREFIX "" OUTPUT_NAME "pcf8591" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_pcf8591 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/pcf8591.pyi" DESTINATION "wiringop/wiring_pi" RENAME "pcf8591.pyi")
nanobind_add_module(nb_wiringPi_pseudoPins NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/pseudoPins.cpp)
target_include_directories(nb_wiringPi_pseudoPins PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_pseudoPins PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_pseudoPins PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_pseudoPins)
set_target_properties(nb_wiringPi_pseudoPins PROPERTIES PREFIX "" OUTPUT_NAME "pseudo_pins" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_pseudoPins LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/pseudoPins.pyi" DESTINATION "wiringop/wiring_pi" RENAME "pseudo_pins.pyi")
nanobind_add_module(nb_wiringPi_rht03 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/rht03.cpp)
target_include_directories(nb_wiringPi_rht03 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_rht03 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_rht03 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_rht03)
set_target_properties(nb_wiringPi_rht03 PROPERTIES PREFIX "" OUTPUT_NAME "rht03" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_rht03 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/rht03.pyi" DESTINATION "wiringop/wiring_pi" RENAME "rht03.pyi")
nanobind_add_module(nb_wiringPi_sn3218 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/sn3218.cpp)
target_include_directories(nb_wiringPi_sn3218 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_sn3218 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_sn3218 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_sn3218)
set_target_properties(nb_wiringPi_sn3218 PROPERTIES PREFIX "" OUTPUT_NAME "sn3218" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_sn3218 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/sn3218.pyi" DESTINATION "wiringop/wiring_pi" RENAME "sn3218.pyi")
nanobind_add_module(nb_wiringPi_softPwm NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/softPwm.cpp)
target_include_directories(nb_wiringPi_softPwm PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_softPwm PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_softPwm PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_softPwm)
set_target_properties(nb_wiringPi_softPwm PROPERTIES PREFIX "" OUTPUT_NAME "soft_pwm" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_softPwm LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/softPwm.pyi" DESTINATION "wiringop/wiring_pi" RENAME "soft_pwm.pyi")
nanobind_add_module(nb_wiringPi_softServo NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/softServo.cpp)
target_include_directories(nb_wiringPi_softServo PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_softServo PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_softServo PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_softServo)
set_target_properties(nb_wiringPi_softServo PROPERTIES PREFIX "" OUTPUT_NAME "soft_servo" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_softServo LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/softServo.pyi" DESTINATION "wiringop/wiring_pi" RENAME "soft_servo.pyi")
nanobind_add_module(nb_wiringPi_softTone NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/softTone.cpp)
target_include_directories(nb_wiringPi_softTone PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_softTone PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_softTone PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_softTone)
set_target_properties(nb_wiringPi_softTone PROPERTIES PREFIX "" OUTPUT_NAME "soft_tone" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_softTone LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/softTone.pyi" DESTINATION "wiringop/wiring_pi" RENAME "soft_tone.pyi")
nanobind_add_module(nb_wiringPi_sr595 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/sr595.cpp)
target_include_directories(nb_wiringPi_sr595 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_sr595 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_sr595 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_sr595)
set_target_properties(nb_wiringPi_sr595 PROPERTIES PREFIX "" OUTPUT_NAME "sr595" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_sr595 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/sr595.pyi" DESTINATION "wiringop/wiring_pi" RENAME "sr595.pyi")
nanobind_add_module(nb_wiringPi_w25q64 NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/w25q64.cpp)
target_include_directories(nb_wiringPi_w25q64 PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_w25q64 PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_w25q64 PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_w25q64)
set_target_properties(nb_wiringPi_w25q64 PROPERTIES PREFIX "" OUTPUT_NAME "w25q64" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_w25q64 LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/w25q64.pyi" DESTINATION "wiringop/wiring_pi" RENAME "w25q64.pyi")
nanobind_add_module(nb_wiringPi_wiringPi NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wiringPi.cpp)
target_include_directories(nb_wiringPi_wiringPi PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wiringPi PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wiringPi PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wiringPi)
set_target_properties(nb_wiringPi_wiringPi PROPERTIES PREFIX "" OUTPUT_NAME "wiring_pi" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wiringPi LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wiringPi.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wiring_pi.pyi")
nanobind_add_module(nb_wiringPi_wiringPiI2C NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wiringPiI2C.cpp)
target_include_directories(nb_wiringPi_wiringPiI2C PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wiringPiI2C PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wiringPiI2C PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wiringPiI2C)
set_target_properties(nb_wiringPi_wiringPiI2C PROPERTIES PREFIX "" OUTPUT_NAME "wiring_pi_i2c" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wiringPiI2C LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wiringPiI2C.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wiring_pi_i2c.pyi")
nanobind_add_module(nb_wiringPi_wiringPiSPI NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wiringPiSPI.cpp)
target_include_directories(nb_wiringPi_wiringPiSPI PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wiringPiSPI PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wiringPiSPI PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wiringPiSPI)
set_target_properties(nb_wiringPi_wiringPiSPI PROPERTIES PREFIX "" OUTPUT_NAME "wiring_pi_spi" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wiringPiSPI LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wiringPiSPI.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wiring_pi_spi.pyi")
nanobind_add_module(nb_wiringPi_wiringSerial NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wiringSerial.cpp)
target_include_directories(nb_wiringPi_wiringSerial PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wiringSerial PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wiringSerial PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wiringSerial)
set_target_properties(nb_wiringPi_wiringSerial PROPERTIES PREFIX "" OUTPUT_NAME "wiring_serial" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wiringSerial LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wiringSerial.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wiring_serial.pyi")
nanobind_add_module(nb_wiringPi_wiringShift NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wiringShift.cpp)
target_include_directories(nb_wiringPi_wiringShift PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wiringShift PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wiringShift PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wiringShift)
set_target_properties(nb_wiringPi_wiringShift PROPERTIES PREFIX "" OUTPUT_NAME "wiring_shift" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wiringShift LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wiringShift.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wiring_shift.pyi")
nanobind_add_module(nb_wiringPi_wpiExtensions NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPi/wpiExtensions.cpp)
target_include_directories(nb_wiringPi_wpiExtensions PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPi_wpiExtensions PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPi_wpiExtensions PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPi_wpiExtensions)
set_target_properties(nb_wiringPi_wpiExtensions PROPERTIES PREFIX "" OUTPUT_NAME "wpi_extensions" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi")
install(TARGETS nb_wiringPi_wpiExtensions LIBRARY DESTINATION "wiringop/wiring_pi" RUNTIME DESTINATION "wiringop/wiring_pi")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPi/wpiExtensions.pyi" DESTINATION "wiringop/wiring_pi" RENAME "wpi_extensions.pyi")
nanobind_add_module(nb_wiringPiD_daemonise NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPiD/daemonise.cpp)
target_include_directories(nb_wiringPiD_daemonise PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPiD_daemonise PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPiD_daemonise PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPiD_daemonise)
set_target_properties(nb_wiringPiD_daemonise PROPERTIES PREFIX "" OUTPUT_NAME "daemonise" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi_d")
install(TARGETS nb_wiringPiD_daemonise LIBRARY DESTINATION "wiringop/wiring_pi_d" RUNTIME DESTINATION "wiringop/wiring_pi_d")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPiD/daemonise.pyi" DESTINATION "wiringop/wiring_pi_d" RENAME "daemonise.pyi")
nanobind_add_module(nb_wiringPiD_drcNetCmd NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPiD/drcNetCmd.cpp)
target_include_directories(nb_wiringPiD_drcNetCmd PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPiD_drcNetCmd PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPiD_drcNetCmd PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPiD_drcNetCmd)
set_target_properties(nb_wiringPiD_drcNetCmd PROPERTIES PREFIX "" OUTPUT_NAME "drc_net_cmd" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi_d")
install(TARGETS nb_wiringPiD_drcNetCmd LIBRARY DESTINATION "wiringop/wiring_pi_d" RUNTIME DESTINATION "wiringop/wiring_pi_d")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPiD/drcNetCmd.pyi" DESTINATION "wiringop/wiring_pi_d" RENAME "drc_net_cmd.pyi")
nanobind_add_module(nb_wiringPiD_network NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPiD/network.cpp)
target_include_directories(nb_wiringPiD_network PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPiD_network PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPiD_network PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPiD_network)
set_target_properties(nb_wiringPiD_network PROPERTIES PREFIX "" OUTPUT_NAME "network" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi_d")
install(TARGETS nb_wiringPiD_network LIBRARY DESTINATION "wiringop/wiring_pi_d" RUNTIME DESTINATION "wiringop/wiring_pi_d")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPiD/network.pyi" DESTINATION "wiringop/wiring_pi_d" RENAME "network.pyi")
nanobind_add_module(nb_wiringPiD_runRemote NB_STATIC FREE_THREADED PROTECT_STACK NOMINSIZE src/wiringPiD/runRemote.cpp)
target_include_directories(nb_wiringPiD_runRemote PRIVATE ${NB_ROOT}/include ${NB_ROOT}/ext/robin_map/include ${WIRINGOP_SOURCE} ${WIRINGOP_SOURCE}/wiringPi ${WIRINGOP_SOURCE}/devLib ${WIRINGOP_SOURCE}/wiringPiD)
target_compile_definitions(nb_wiringPiD_runRemote PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries(nb_wiringPiD_runRemote PRIVATE wiringop_backend ${WIRINGOP_NATIVE_SYSTEM_LIBS})
wiringop_native_windows_abi(nb_wiringPiD_runRemote)
set_target_properties(nb_wiringPiD_runRemote PROPERTIES PREFIX "" OUTPUT_NAME "run_remote" LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python/wiringop/wiring_pi_d")
install(TARGETS nb_wiringPiD_runRemote LIBRARY DESTINATION "wiringop/wiring_pi_d" RUNTIME DESTINATION "wiringop/wiring_pi_d")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/stubs/wiringPiD/runRemote.pyi" DESTINATION "wiringop/wiring_pi_d" RENAME "run_remote.pyi")

