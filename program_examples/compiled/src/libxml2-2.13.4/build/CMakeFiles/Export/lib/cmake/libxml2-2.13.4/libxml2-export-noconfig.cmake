#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LibXml2::LibXml2" for configuration ""
set_property(TARGET LibXml2::LibXml2 APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LibXml2::LibXml2 PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libxml2.so.2.13.4"
  IMPORTED_SONAME_NOCONFIG "libxml2.so.2"
  )

list(APPEND _IMPORT_CHECK_TARGETS LibXml2::LibXml2 )
list(APPEND _IMPORT_CHECK_FILES_FOR_LibXml2::LibXml2 "${_IMPORT_PREFIX}/lib/libxml2.so.2.13.4" )

# Import target "LibXml2::xmlcatalog" for configuration ""
set_property(TARGET LibXml2::xmlcatalog APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LibXml2::xmlcatalog PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/xmlcatalog"
  )

list(APPEND _IMPORT_CHECK_TARGETS LibXml2::xmlcatalog )
list(APPEND _IMPORT_CHECK_FILES_FOR_LibXml2::xmlcatalog "${_IMPORT_PREFIX}/bin/xmlcatalog" )

# Import target "LibXml2::xmllint" for configuration ""
set_property(TARGET LibXml2::xmllint APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LibXml2::xmllint PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/xmllint"
  )

list(APPEND _IMPORT_CHECK_TARGETS LibXml2::xmllint )
list(APPEND _IMPORT_CHECK_FILES_FOR_LibXml2::xmllint "${_IMPORT_PREFIX}/bin/xmllint" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
