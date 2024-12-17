# CMake generated Testfile for 
# Source directory: /src/libxml2-2.13.4
# Build directory: /src/libxml2-2.13.4/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(runtest "/src/libxml2-2.13.4/build/runtest" "--out" "/src/libxml2-2.13.4/build")
set_tests_properties(runtest PROPERTIES  WORKING_DIRECTORY "/src/libxml2-2.13.4" _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;521;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(runsuite "/src/libxml2-2.13.4/build/runsuite")
set_tests_properties(runsuite PROPERTIES  WORKING_DIRECTORY "/src/libxml2-2.13.4" _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;522;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testapi "/src/libxml2-2.13.4/build/testapi")
set_tests_properties(testapi PROPERTIES  _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;527;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testchar "/src/libxml2-2.13.4/build/testchar")
set_tests_properties(testchar PROPERTIES  _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;529;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testdict "/src/libxml2-2.13.4/build/testdict")
set_tests_properties(testdict PROPERTIES  _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;530;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testparser "/src/libxml2-2.13.4/build/testparser")
set_tests_properties(testparser PROPERTIES  WORKING_DIRECTORY "/src/libxml2-2.13.4" _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;531;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testrecurse "/src/libxml2-2.13.4/build/testrecurse")
set_tests_properties(testrecurse PROPERTIES  WORKING_DIRECTORY "/src/libxml2-2.13.4" _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;532;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
add_test(testThreads "/src/libxml2-2.13.4/build/testThreads")
set_tests_properties(testThreads PROPERTIES  WORKING_DIRECTORY "/src/libxml2-2.13.4" _BACKTRACE_TRIPLES "/src/libxml2-2.13.4/CMakeLists.txt;533;add_test;/src/libxml2-2.13.4/CMakeLists.txt;0;")
