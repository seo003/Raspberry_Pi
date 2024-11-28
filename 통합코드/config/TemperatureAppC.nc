configuration TemperatureAppC { }
implementation {
  components TemperatureC, MainC, ActiveMessageC, new AMSenderC(AM_OSCILLOSCOPE);

  TemperatureC.Boot -> MainC;
  TemperatureC.AMSend -> AMSenderC;
}

