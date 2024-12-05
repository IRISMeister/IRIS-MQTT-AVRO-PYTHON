/// Description
Class MQTT.BS.PYAVRO Extends EnsLib.MQTT.Service.Passthrough
{

Method OnProcessInput(pInput As EnsLib.MQTT.Message, pOutput As %RegisteredObject) As %Status
{
	#dim tSC As %Status = $$$OK
	#dim e As %Exception.AbstractException
	
	Try {
		#; $$$LOGINFO("Topic:"_pInput.Topic_" Value:"_pInput.StringValue)
		#; Set ^log($INCREMENT(^log))=pInput.StringValue

		Set seq=$INCREMENT(^seq("avro"))
		#; Avroはバイナリ形式なので、(文字列ではなく)バイト列として渡す。
		Do ..Save(seq,pInput.Topic,##class(%SYS.Python).Bytes(pInput.StringValue))

		Set tRequest=##class(MQTT.REQ.Simple).%New(seq,pInput.Topic)
		Set tSC=##super(tRequest,pOutput)

		#; Bench実行時の待ち合わせ処理。^seqtarget("avro")の有無がBench実行中か否かのフラグを兼ねる。
		if ^seq("avro")=$G(^seqtarget("avro")) {
			Do $SYSTEM.Event.Signal("NotifyAVRO",{"PID":($JOB)}.%ToJSON())
			$$$LOGINFO("target count reached. Count:"_^seq("avro"))
			Set res = $SYSTEM.Event.Wait("",10) ; Wait acknowledgement
			If res < 1 {
				Do $SYSTEM.Event.Clear("NotifyAVRO")
				$$$LOGERROR("Nobody was waiting.")
			}
		}
	} Catch e {
		Set tSC=e.AsStatus()
	}
		
	Quit tSC
}

Method Save(seq As %Numeric, topic As %String, avromsg As %RawString) [ Language = python ]
{
	import SaveFastAVRO as s

	try:
		s.saveFromString(seq,topic,avromsg)
	except Exception as ex:
		raise
}

Method OnInit() As %Status [ Language = python ]
{
	import sys
	import platform
	pf = platform.system()
	datadir='/share/'
	if pf == 'Windows':
		datadir="C:\\git\\IRIS-MQTT-AVRO-PYTHON\\share\\"
		sys.path += [datadir]
		
	import SaveFastAVRO as s
	
	s.init(datadir)
	self.OnInitCB()
	return True
}

Method OnInitCB() As %Status
{
  If '$SYSTEM.Event.Defined("NotifyAVRO") {
    Do $SYSTEM.Event.Create("NotifyAVRO")
  }
  Return $$$OK
}

Method OnTearDown() As %Status
{
  If $SYSTEM.Event.Defined("NotifyAVRO") {
    Do $SYSTEM.Event.Clear("NotifyAVRO")
    Do $SYSTEM.Event.Delete("NotifyAVRO")
  }
  Return $$$OK
}

}
