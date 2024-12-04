ARG IMAGE=containers.intersystems.com/intersystems/irishealth-community:2024.1
FROM $IMAGE

USER root

# Japanese language pack 
RUN apt -y update \
 && DEBIAN_FRONTEND=noninteractive apt -y install language-pack-ja-base language-pack-ja

# installing vim just for convenience
RUN apt -y update \
 && DEBIAN_FRONTEND=noninteractive apt -y install build-essential vim mosquitto-clients \
 && apt clean

USER irisowner
#RUN pip install avro fastavro -t /usr/irissys/mgr/python

COPY ./src ./src/

RUN iris start $ISC_PACKAGE_INSTANCENAME quietly \ 
 && printf 'Do ##class(Config.NLS.Locales).Install("jpuw") Do ##class(Security.Users).UnExpireUserPasswords("*") h\n' | iris session $ISC_PACKAGE_INSTANCENAME -U %SYS \
 && printf 'Set tSC=$system.OBJ.Load("/home/irisowner/src/Installer.cls","ck") Do:+tSC=0 $SYSTEM.Process.Terminate($JOB,1) h\n' | iris session $ISC_PACKAGE_INSTANCENAME \
 && printf 'Set tSC=##class(App.Installer).Initialize() Do:+tSC=0 $SYSTEM.Process.Terminate($JOB,1) h\n' | iris session $ISC_PACKAGE_INSTANCENAME \
 && iris stop $ISC_PACKAGE_INSTANCENAME quietly

# clean up
RUN iris start $ISC_PACKAGE_INSTANCENAME nostu quietly \
 && printf "kill ^%%SYS(\"JOURNAL\") kill ^SYS(\"NODE\") h\n" | iris session $ISC_PACKAGE_INSTANCENAME -B | cat \
 && iris stop $ISC_PACKAGE_INSTANCENAME quietly bypass \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/journal.log \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/IRIS.WIJ \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/iris.ids \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/alerts.log \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/journal/* \
 && rm -f $ISC_PACKAGE_INSTALLDIR/mgr/messages.log \
 && touch $ISC_PACKAGE_INSTALLDIR/mgr/messages.log

# CSP.ini変更
RUN sed -i 's/SM_Timeout=28800/SM_Timeout=28800\nSystem_Manager=*.*.*.*\nREGISTRY_METHODS=Disabled/' /usr/irissys/csp/bin/CSP.ini \
 && sed -i 's/Server_Response_Timeout=60/Server_Response_Timeout=600/' /usr/irissys/csp/bin/CSP.ini \
 && sed -i 's/Queued_Request_Timeout=60/Queued_Request_Timeout=600/' /usr/irissys/csp/bin/CSP.ini 

# 埋め込みpythonで実行するpyをcopy。これが無いとsys.pathに含めてもエラーになる
COPY share/Save*.py /usr/irissys/mgr/python/
#COPY share/SimpleClass.avsc AVRO/
