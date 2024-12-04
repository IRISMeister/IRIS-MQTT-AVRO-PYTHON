Class MQTT.Dispatcher Extends %CSP.REST
{

Parameter CONVERTINPUTSTREAM = 1;

XData UrlMap [ XMLNamespace = "http://www.intersystems.com/urlmap" ]
{
<Routes>
<Route Url="/reset/:p1:/:p2" Method="POST" Call="Reset" Cors="true" />
<Route Url="/measure" Method="POST" Call='Measure' Cors="true" />
<Route Url="/wait/:p1/:p2" Method="POST" Call='Wait' Cors="true" />
</Routes>
}

ClassMethod Reset(type As %String = "avro", datacount As %Integer = 0) As %Status
{
    New $NAMESPACE

    try {
        k ^seq(type) 
        s ^seqtarget(type)=datacount

        #; 全件ロード完了の待ち合わせのためのイベントをクリア。
        if type="avro" {Do $SYSTEM.Event.Clear("NotifyAVRO")}
        if type="json" {Do $SYSTEM.Event.Clear("NotifyJSON")}

        Set sql="DELETE FROM MQTT.SimpleClass"
        Set result=##class(%SQL.Statement).%ExecDirect(,sql)
        $$$ThrowSQLIfError(result.%SQLCODE,result.%Message)
        #;Set info={"SQLCODE":(result.%SQLCODE)}
        #;do info.%ToJSON() w !

        Set tSC=##class(%SYS.Journal.File).PurgeAll()
        $$$ThrowOnError(tSC)

        Set $NAMESPACE="%SYS"
        Set tSC=##class(Backup.General).ExternalFreeze()
        $$$ThrowOnError(tSC)
        Set tSC=##class(Backup.General).ExternalThaw()
        $$$ThrowOnError(tSC)
    }
    Catch (e) {
	  Set tSC=e.AsStatus()
    }

    return tSC
}

ClassMethod Measure() As %Status
{
    Set sql="SELECT count(*) cnt,{fn TIMESTAMPDIFF(SQL_TSI_FRAC_SECOND,MIN(ReceiveTS),MAX(ReceiveTS))} diff FROM MQTT.SimpleClass"
    Set result=##class(%SQL.Statement).%ExecDirect(,sql)
    Do result.%Next()

    Set info={"SQLCODE":(result.%SQLCODE),"Count":(result.cnt),"Diff":(result.diff)}
	write info.%ToJSON()
    return $$$OK
}

ClassMethod Wait(event As %String = "NotifyAVRO", waittime As %Integer = 60) As %Status
{
    set ret=0
    Set result = $SYSTEM.Event.WaitMsg(event,waittime)
    Set resultCode=$LG(result,1)
    #; something bad happened
    If resultCode<1 {
        w {"ret":0}.%ToJSON(),!
    }
    Else {
        Set resultJson={}.%FromJSON($LG(result,2))
        Do $SYSTEM.Event.Signal(resultJson.PID)
        w {"ret":(resultJson.ret)}.%ToJSON(),!
    }

    Return $$$OK
}

}
