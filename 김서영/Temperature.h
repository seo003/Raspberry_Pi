#ifndef TEMPERATURE_H
#define TEMPERATURE_H

enum {
  NREADINGS = 10,

  DEFAULT_INTERVAL = 256,

  AM_OSCILLOSCOPE = 0x93
};

typedef nx_struct oscilloscope {
  nx_uint16_t version; /* 버전 */
  nx_uint16_t interval; /* 주기 */
  nx_uint16_t id; /* ID */
  nx_uint16_t count; /* 샘플 데이터  */
  nx_uint16_t readings[NREADINGS]; /* 온도 데이터 저장 배열 */
} oscilloscope_t;

#endif

