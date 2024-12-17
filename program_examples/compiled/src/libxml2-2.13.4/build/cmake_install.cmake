# Install script for directory: /src/libxml2-2.13.4

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libxml2/libxml" TYPE FILE FILES
    "/src/libxml2-2.13.4/include/libxml/c14n.h"
    "/src/libxml2-2.13.4/include/libxml/catalog.h"
    "/src/libxml2-2.13.4/include/libxml/chvalid.h"
    "/src/libxml2-2.13.4/include/libxml/debugXML.h"
    "/src/libxml2-2.13.4/include/libxml/dict.h"
    "/src/libxml2-2.13.4/include/libxml/encoding.h"
    "/src/libxml2-2.13.4/include/libxml/entities.h"
    "/src/libxml2-2.13.4/include/libxml/globals.h"
    "/src/libxml2-2.13.4/include/libxml/hash.h"
    "/src/libxml2-2.13.4/include/libxml/HTMLparser.h"
    "/src/libxml2-2.13.4/include/libxml/HTMLtree.h"
    "/src/libxml2-2.13.4/include/libxml/list.h"
    "/src/libxml2-2.13.4/include/libxml/nanoftp.h"
    "/src/libxml2-2.13.4/include/libxml/nanohttp.h"
    "/src/libxml2-2.13.4/include/libxml/parser.h"
    "/src/libxml2-2.13.4/include/libxml/parserInternals.h"
    "/src/libxml2-2.13.4/include/libxml/pattern.h"
    "/src/libxml2-2.13.4/include/libxml/relaxng.h"
    "/src/libxml2-2.13.4/include/libxml/SAX.h"
    "/src/libxml2-2.13.4/include/libxml/SAX2.h"
    "/src/libxml2-2.13.4/include/libxml/schemasInternals.h"
    "/src/libxml2-2.13.4/include/libxml/schematron.h"
    "/src/libxml2-2.13.4/include/libxml/threads.h"
    "/src/libxml2-2.13.4/include/libxml/tree.h"
    "/src/libxml2-2.13.4/include/libxml/uri.h"
    "/src/libxml2-2.13.4/include/libxml/valid.h"
    "/src/libxml2-2.13.4/include/libxml/xinclude.h"
    "/src/libxml2-2.13.4/include/libxml/xlink.h"
    "/src/libxml2-2.13.4/include/libxml/xmlIO.h"
    "/src/libxml2-2.13.4/include/libxml/xmlautomata.h"
    "/src/libxml2-2.13.4/include/libxml/xmlerror.h"
    "/src/libxml2-2.13.4/include/libxml/xmlexports.h"
    "/src/libxml2-2.13.4/include/libxml/xmlmemory.h"
    "/src/libxml2-2.13.4/include/libxml/xmlmodule.h"
    "/src/libxml2-2.13.4/include/libxml/xmlreader.h"
    "/src/libxml2-2.13.4/include/libxml/xmlregexp.h"
    "/src/libxml2-2.13.4/include/libxml/xmlsave.h"
    "/src/libxml2-2.13.4/include/libxml/xmlschemas.h"
    "/src/libxml2-2.13.4/include/libxml/xmlschemastypes.h"
    "/src/libxml2-2.13.4/include/libxml/xmlstring.h"
    "/src/libxml2-2.13.4/include/libxml/xmlunicode.h"
    "/src/libxml2-2.13.4/include/libxml/xmlwriter.h"
    "/src/libxml2-2.13.4/include/libxml/xpath.h"
    "/src/libxml2-2.13.4/include/libxml/xpathInternals.h"
    "/src/libxml2-2.13.4/include/libxml/xpointer.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so.2.13.4"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so.2"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/src/libxml2-2.13.4/build/libxml2.so.2.13.4"
    "/src/libxml2-2.13.4/build/libxml2.so.2"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so.2.13.4"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so.2"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/src/libxml2-2.13.4/build/libxml2.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libxml2.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xprogramsx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/src/libxml2-2.13.4/build/xmlcatalog")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog"
         OLD_RPATH "/src/libxml2-2.13.4/build:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmlcatalog")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xprogramsx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/src/libxml2-2.13.4/build/xmllint")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint"
         OLD_RPATH "/src/libxml2-2.13.4/build:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/xmllint")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/python/libxml2mod.so.2.13.4")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/python" TYPE SHARED_LIBRARY FILES "/src/libxml2-2.13.4/build/libxml2mod.so.2.13.4")
  if(EXISTS "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4"
         OLD_RPATH "/src/libxml2-2.13.4/build:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/python/libxml2mod.so.2.13.4")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/python/libxml2mod.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/python/libxml2mod.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/python/libxml2mod.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/python/libxml2mod.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/python" TYPE SHARED_LIBRARY FILES "/src/libxml2-2.13.4/build/libxml2mod.so")
  if(EXISTS "$ENV{DESTDIR}/usr/local/python/libxml2mod.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/python/libxml2mod.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/usr/local/python/libxml2mod.so"
         OLD_RPATH "/src/libxml2-2.13.4/build:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/python/libxml2mod.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/python/drv_libxml2.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/python" TYPE FILE FILES "/src/libxml2-2.13.4/python/drv_libxml2.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/python/libxml2.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/python" TYPE FILE FILES "/src/libxml2-2.13.4/build/libxml2.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdocumentationx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/man/man1" TYPE FILE FILES "/src/libxml2-2.13.4/doc/xml2-config.1")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdocumentationx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/man/man1" TYPE FILE FILES "/src/libxml2-2.13.4/doc/xmlcatalog.1")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdocumentationx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/man/man1" TYPE FILE FILES "/src/libxml2-2.13.4/doc/xmllint.1")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdocumentationx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/libxml2" TYPE DIRECTORY FILES "/src/libxml2-2.13.4/doc/" REGEX "/Makefile\\.[^/]*$" EXCLUDE REGEX "/[^/]*\\.1$" EXCLUDE REGEX "/[^/]*\\.py$" EXCLUDE REGEX "/[^/]*\\.res$" EXCLUDE REGEX "/[^/]*\\.xml$" EXCLUDE REGEX "/[^/]*\\.xsl$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4" TYPE FILE FILES "/src/libxml2-2.13.4/build/libxml2-config.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4" TYPE FILE FILES "/src/libxml2-2.13.4/build/libxml2-config-version.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4/libxml2-export.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4/libxml2-export.cmake"
         "/src/libxml2-2.13.4/build/CMakeFiles/Export/lib/cmake/libxml2-2.13.4/libxml2-export.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4/libxml2-export-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4/libxml2-export.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4" TYPE FILE FILES "/src/libxml2-2.13.4/build/CMakeFiles/Export/lib/cmake/libxml2-2.13.4/libxml2-export.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/libxml2-2.13.4" TYPE FILE FILES "/src/libxml2-2.13.4/build/CMakeFiles/Export/lib/cmake/libxml2-2.13.4/libxml2-export-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libxml2/libxml" TYPE FILE FILES "/src/libxml2-2.13.4/build/libxml/xmlversion.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/src/libxml2-2.13.4/build/libxml-2.0.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/src/libxml2-2.13.4/build/xml2-config")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/aclocal" TYPE FILE FILES "/src/libxml2-2.13.4/libxml.m4")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/src/libxml2-2.13.4/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
