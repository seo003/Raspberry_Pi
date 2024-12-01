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
  uint8_t reading;  // 0부터 NREADINGS까지

  void startTimer() {
    call Timer.startPeriodic(local.interval);  // 타이머 시작
    reading = 0;
  }

  /* 시스템 초기화 */
  event void Boot.booted() {
    local.interval = DEFAULT_INTERVAL;
    local.id = TOS_NODE_ID;
    if (call RadioControl.start() != SUCCESS) {
      // 초기화 실패 에러
    }
    startTimer();
  }

  /* 타이머 이벤트 */
  event void Timer.fired() {
    if (reading == NREADINGS) {
      reading = 0;
    }

    // 온도 데이터 읽기 시도
    if (call Read.read() != SUCCESS) {
      // 읽기 실패 에러
    }

    reading++;
  }

  /* 온도 데이터 처리 */
  event void Read.readDone(error_t result, uint16_t data) {
    if (result != SUCCESS) {
      data = 0xffff;
    }

    if (reading < NREADINGS) {
      local.readings[reading] = data;
    }

    if (reading == NREADINGS) {
      if (!sendBusy && sizeof(local) <= call AMSend.maxPayloadLength()) {
        memcpy(call AMSend.getPayload(&sendBuf, sizeof(local)), &local, sizeof(local));
        if (call AMSend.send(AM_BROADCAST_ADDR, &sendBuf, sizeof(local)) == SUCCESS) {
          sendBusy = TRUE;
        }
      }
    }
  }

  /* 데이터 전송 완료 */
  event void AMSend.sendDone(message_t* msg, error_t error) {
    sendBusy = FALSE;
  }
}

