module TemperatureC @safe()
{
  uses {
    interface Boot;
    interface SplitControl as RadioControl;
    interface AMSend;
    interface Timer<TMilli>;
    interface Read<uint16_t>;
  }
}

implementation
{
  message_t sendBuf;
  bool sendBusy;

  oscilloscope_t local;

  uint8_t reading;  // 0 to NREADINGS

  void startTimer() {
    call Timer.startPeriodic(local.interval);  // Start periodic timer
    reading = 0;
  }

  event void Boot.booted() {
    local.interval = DEFAULT_INTERVAL;
    local.id = TOS_NODE_ID;
    if (call RadioControl.start() != SUCCESS) {
      // Initialization failed, handle error if needed
    }
    startTimer();
  }

  /* Timer event to periodically read the temperature */
  event void Timer.fired() {
    if (reading == NREADINGS) {
      reading = 0;
    }

    /* Read the temperature data */
    if (call Read.read() != SUCCESS) {
      // Handle error if reading fails
    }

    reading++;
  }

  event void Read.readDone(error_t result, uint16_t data) {
    if (result != SUCCESS) {
      data = 0xffff;  // Error value
    }

    if (reading < NREADINGS) {
      local.readings[reading] = data;  // Store the temperature reading
    }

    if (reading == NREADINGS) {
      // Send the temperature data when readings are complete
      if (!sendBusy && sizeof(local) <= call AMSend.maxPayloadLength()) {
        memcpy(call AMSend.getPayload(&sendBuf, sizeof(local)), &local, sizeof(local));
        if (call AMSend.send(AM_BROADCAST_ADDR, &sendBuf, sizeof(local)) == SUCCESS) {
          sendBusy = TRUE;
        }
      }
    }
  }

  event void AMSend.sendDone(message_t* msg, error_t error) {
    sendBusy = FALSE;
  }
}

