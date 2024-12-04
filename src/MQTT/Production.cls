/// Interoperability production XML, should be viewed in the management portal.
Class MQTT.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="MQTT.Production" TestingEnabled="true" LogGeneralTraceEvents="true">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="From_MQTT_PT" Category="" ClassName="EnsLib.MQTT.Service.Passthrough" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">NoOp</Setting>
    <Setting Target="Adapter" Name="Topic">/XGH/PT/#</Setting>
    <Setting Target="Adapter" Name="Url">tcp://mqttbroker:1883</Setting>
  </Item>
  <Item Name="NoOp" Category="" ClassName="MQTT.BO.NoOp" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
  <Item Name="MQTT.BS.PYAVRO" Category="" ClassName="MQTT.BS.PYAVRO" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="Topic">/XGH/PYAVRO/#</Setting>
    <Setting Target="Adapter" Name="Url">tcp://mqttbroker:1883</Setting>
    <Setting Target="Adapter" Name="QOS">1</Setting>
  </Item>
  <Item Name="MQTT.BS.PYJSON" Category="" ClassName="MQTT.BS.PYJSON" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="Topic">/XGH/PYJSON/#</Setting>
    <Setting Target="Adapter" Name="Url">tcp://mqttbroker:1883</Setting>
    <Setting Target="Adapter" Name="QOS">1</Setting>
  </Item>
</Production>
}

}
