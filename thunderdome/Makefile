include ../Makefile.inc

LIBTD=libtd.$(LIBTYPE)
LIBTD_JULIA=libtd_julia.$(LIBTYPE)
LIBTD_PYTHON=libtd_python.$(LIBTYPE)
LIBTD_R=libtd_r.$(LIBTYPE)
LIBTD_JAVA=libtd_java.$(LIBTYPE)
LIBTD_JAVA_WINDOWS=libtd_java_windows.$(LIBTYPE)

default: examples

examples: example_client example_client_java ds_roundtrip

libs: $(LIBTD) $(LIBTD_JULIA) $(LIBTD_R) $(LIBTD_PYTHON)

test:
	@echo 'No tests here =('

$(LIBTD): td.h td_ds.h td.c td_ds.c
	$(CC) $(DEBUG) -fPIC -c td.c -o td.o
	$(CC) $(DEBUG) -fPIC -c td_ds.c -o td_ds.o
	$(CC) $(DEBUG) -shared -fPIC td.o td_ds.o -o $@ -ldl

$(LIBTD_JULIA): td.h td_julia.c $(LIBTD)
	$(CC) $(DEBUG) -fPIC -c td_julia.c -o td_julia.o $(JULIA_CFLAGS)
	$(CC) $(DEBUG) -shared -fPIC td_julia.o -o $@ $(JULIA_LDFLAGS) ./$(LIBTD)

$(LIBTD_R): td.h $(LIBTD) td_r.cpp
	$(CXX) $(DEBUG) -fPIC -c td_r.cpp -o td_r.o $(CXXFLAGS) $(CPPFLAGS)
	$(CXX) $(DEBUG) -shared -fPIC td_r.o -o $@  $(CXXFLAGS) $(CPPFLAGS) $(LDFLAGS) $(LDLIBS) ./$(LIBTD)

# for windows for now...? do we have to make a dll??
$(LIBTD_JAVA_WINDOWS): td.h td_java.c $(LIBTD)
	$(CC) $(DEBUG) -D__int64=int64_t -fPIC -c td_java.c -o td_java.o -I"$(JAVA_HOME)"/include -I"$(JAVA_HOME)"/include/win32
#	$(CC) $(DEBUG) -fPIC -c td_java.c -o td_java.o -I"$(JAVA_HOME)"/include
	$(CC) $(DEBUG) -shared -fPIC td_java.o -o $@ "$(JAVA_HOME)"/jre/bin/server/jvm.dll ./$(LIBTD)

# mac or linux
$(LIBTD_JAVA): td.h td_java.c $(LIBTD)
	$(CC) $(DEBUG) -fPIC -c td_java.c -o td_java.o -I"$(JAVA_HOME)"/include -I"$(JAVA_HOME)"/include/$(ARCH)
	$(CC) $(DEBUG) -shared -fPIC td_java.o -o $@ "$(JAVA_HOME)"/jre/lib/$(SERVER_DIR)/libjvm.$(LIBTYPE) ./$(LIBTD)

example_client: example_client.c td.h $(LIBTD_JULIA) $(LIBTD_PYTHON) $(LIBTD_JAVA) $(LIBTD_R)
	$(CC) $(DEBUG) -DTD_HAS_PYTHON=1 -DTD_PYTHON_EXE="\"$(PYTHON_EXE)\"" -DTD_HAS_JULIA=1 -DTD_JULIA_BIN="\"$(JULIA_BIN)\"" $< -o $@ ./$(LIBTD)

# remember to do ant first or point to a valid classpath
# mac or linux, maybe win32
# on the linux machine I was using JAVA_HOME was /usr/lib/jvm/java-7-openjdk-amd64
# and I set LD_LIBRARY_PATH to ${JAVA_HOME}/jre/lib/amd64/server
# you may have to do a find for libjvm with a different java installation
example_client_java: example_client.c td.h $(LIBTD_JAVA)
	$(CC) $(DEBUG) -DTD_HAS_JAVA=1 $< -o $@ ./$(LIBTD)

# NOTE: never quite got this working
example_java_client_windows: example_client.c td.h td_java.c
	$(CC) $(DEBUG) -DTD_HAS_JAVA=1 -D__int64=int64_t -fPIC -c td_java.c -o td_java.o -I"$(JAVA_HOME)"/include -I"$(JAVA_HOME)"/include/win32
	$(CC) $(DEBUG) $< -o $@ ./$(LIBTD) 

ds_roundtrip: ds_roundtrip.c td.h
	$(CC) $(DEBUG) $< -o$@ ./$(LIBTD)

$(LIBTD_PYTHON): td.h td_python.c $(LIBTD)
	$(CC) $(DEBUG) -fPIC -c td_python.c -o td_python.o $(PYTHON_CFLAGS)
	$(CC) $(DEBUG) -shared -fPIC td_python.o -o $@ -I$(PYTHON_LDFLAGS) ./$(LIBTD)

example_python: example_client.c td.h $(LIBTD_PYTHON)
	$(CC) $(DEBUG) -DTD_HAS_PYTHON=1 -DTD_PYTHON_EXE="\"$(PYTHON_EXE)\""  $< -o $@ ./$(LIBTD)

clean:
	rm -f libtd*.$(LIBTYPE) *.o
	rm -f example_client
	rm -f example_client_java
	rm -f ds_roundtrip

